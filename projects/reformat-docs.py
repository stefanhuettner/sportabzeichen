#!/usr/bin/env python3
"""Reformat Google Docs: remove markdown syntax and apply proper formatting."""

import json
import re
import requests
import subprocess
import time
import sys

TOKENS_PATH = "/root/.openclaw/.google-tokens.json"

def get_token():
    with open(TOKENS_PATH) as f:
        return json.load(f)["access_token"]

def refresh_token():
    subprocess.run(["python3", "/root/.openclaw/refresh-google-token.py"], check=True, capture_output=True)
    return get_token()

def get_doc(doc_id, token):
    url = f"https://docs.googleapis.com/v1/documents/{doc_id}"
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 401:
        token = refresh_token()
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    return r.json(), token

def batch_update(doc_id, requests_list, token):
    if not requests_list:
        return token
    url = f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate"
    body = {"requests": requests_list}
    r = requests.post(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, json=body)
    if r.status_code == 401:
        token = refresh_token()
        r = requests.post(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, json=body)
    if r.status_code != 200:
        print(f"  ERROR batch_update: {r.status_code} {r.text[:500]}")
    r.raise_for_status()
    return token

def extract_text_runs(doc):
    """Extract all text content with their start/end indices from the document body."""
    results = []
    body = doc.get("body", {})
    for elem in body.get("content", []):
        if "paragraph" in elem:
            para = elem["paragraph"]
            para_start = elem["startIndex"]
            para_end = elem["endIndex"]
            style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
            
            # Get full paragraph text
            para_text = ""
            for el in para.get("elements", []):
                if "textRun" in el:
                    para_text += el["textRun"]["content"]
            
            results.append({
                "type": "paragraph",
                "startIndex": para_start,
                "endIndex": para_end,
                "text": para_text,
                "style": style,
                "elements": para.get("elements", [])
            })
    return results

def process_document(doc_id, doc_name, token):
    """Process a single document to remove markdown and apply formatting."""
    print(f"\nProcessing: {doc_name} ({doc_id})")
    
    doc, token = get_doc(doc_id, token)
    paragraphs = extract_text_runs(doc)
    
    # Collect all operations
    style_requests = []  # paragraph style changes (don't affect indices)
    delete_ops = []      # (start, end) pairs to delete, will sort backwards
    format_ops = []      # (start, end, style_dict) for bold/italic/strikethrough
    link_ops = []        # (start, end, url) for making URLs clickable
    
    changes_made = 0
    
    for para in paragraphs:
        text = para["text"]
        pstart = para["startIndex"]
        
        # --- HEADING detection ---
        # Check for ### first, then ##, then #
        heading_match = None
        if text.startswith("### "):
            heading_match = ("HEADING_3", "### ")
        elif text.startswith("## "):
            heading_match = ("HEADING_2", "## ")
        elif text.startswith("# "):
            heading_match = ("HEADING_1", "# ")
        
        if heading_match:
            style_name, prefix = heading_match
            style_requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": pstart, "endIndex": para["endIndex"]},
                    "paragraphStyle": {"namedStyleType": style_name},
                    "fields": "namedStyleType"
                }
            })
            # Delete the prefix markers
            delete_ops.append((pstart, pstart + len(prefix)))
            changes_made += 1
            # Update text for further processing (adjust offsets)
            text = text[len(prefix):]
            # We need to account for the prefix removal in subsequent matches
            # Actually, we track absolute positions, so let's recompute from elements
        
        # --- Horizontal rules (--- on its own line) ---
        stripped = text.strip()
        if stripped == "---" or stripped == "***" or stripped == "___":
            # Delete the entire paragraph content (replace with empty or just newline)
            delete_ops.append((pstart, para["endIndex"] - 1))  # keep the newline
            changes_made += 1
            continue
        
        # --- Find markdown patterns in the full paragraph text with absolute positions ---
        # We need to work with the actual text runs to get correct positions
        full_text = ""
        text_start = None
        for el in para["elements"]:
            if "textRun" in el:
                if text_start is None:
                    text_start = el["startIndex"]
                full_text += el["textRun"]["content"]
        
        if text_start is None:
            continue
            
        # Bold: **text**
        for m in re.finditer(r'\*\*(.+?)\*\*', full_text):
            abs_start = text_start + m.start()
            abs_end = text_start + m.end()
            # Format the inner text as bold
            inner_start = text_start + m.start(1)
            inner_end = text_start + m.end(1)
            format_ops.append((inner_start, inner_end, {"bold": True}))
            # Delete closing **
            delete_ops.append((inner_end, inner_end + 2))
            # Delete opening **
            delete_ops.append((abs_start, abs_start + 2))
            changes_made += 1
        
        # Italic: *text* (but not **text**)
        # Need to avoid matching inside ** pairs
        # Use a cleaned version where ** is removed
        for m in re.finditer(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', full_text):
            abs_start = text_start + m.start()
            inner_start = text_start + m.start(1)
            inner_end = text_start + m.end(1)
            format_ops.append((inner_start, inner_end, {"italic": True}))
            delete_ops.append((inner_end, inner_end + 1))
            delete_ops.append((abs_start, abs_start + 1))
            changes_made += 1
        
        # Italic: _text_
        for m in re.finditer(r'(?<!\w)_([^_]+?)_(?!\w)', full_text):
            abs_start = text_start + m.start()
            inner_start = text_start + m.start(1)
            inner_end = text_start + m.end(1)
            format_ops.append((inner_start, inner_end, {"italic": True}))
            delete_ops.append((inner_end, inner_end + 1))
            delete_ops.append((abs_start, abs_start + 1))
            changes_made += 1
        
        # Strikethrough: ~~text~~
        for m in re.finditer(r'~~(.+?)~~', full_text):
            abs_start = text_start + m.start()
            inner_start = text_start + m.start(1)
            inner_end = text_start + m.end(1)
            format_ops.append((inner_start, inner_end, {"strikethrough": True}))
            delete_ops.append((inner_end, inner_end + 2))
            delete_ops.append((abs_start, abs_start + 2))
            changes_made += 1
        
        # Backticks: `code`
        for m in re.finditer(r'`([^`]+?)`', full_text):
            abs_start = text_start + m.start()
            inner_end = text_start + m.end(1)
            delete_ops.append((inner_end, inner_end + 1))
            delete_ops.append((abs_start, abs_start + 1))
            changes_made += 1
        
        # URLs: make plain text URLs clickable
        for m in re.finditer(r'(https?://[^\s\)>\]]+)', full_text):
            url = m.group(1)
            url_start = text_start + m.start()
            url_end = text_start + m.end()
            link_ops.append((url_start, url_end, url))
            changes_made += 1
        
        # Markdown link syntax: [text](url)
        for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\)]+)\)', full_text):
            link_text = m.group(1)
            url = m.group(2)
            abs_start = text_start + m.start()
            abs_end = text_start + m.end()
            # We'll need to: apply link to the text part, then delete the markdown syntax
            # The final text should just be the link_text with the URL linked
            # Delete ](url) part
            bracket_close = text_start + m.start() + 1 + len(link_text)  # position of ]
            delete_ops.append((bracket_close, abs_end))
            # Delete opening [
            delete_ops.append((abs_start, abs_start + 1))
            # Apply link to the text (after [ is removed, positions shift, but we apply before delete)
            link_ops.append((abs_start + 1, abs_start + 1 + len(link_text), url))
            changes_made += 1
    
    if changes_made == 0:
        print(f"  No markdown found, skipping.")
        return token, 0
    
    # Build the final requests list
    # 1. Paragraph styles first (they don't change indices)
    all_requests = list(style_requests)
    
    # 2. Format operations (bold, italic, strikethrough) - these don't change indices
    for start, end, style in format_ops:
        req = {
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "textStyle": style,
                "fields": ",".join(style.keys())
            }
        }
        all_requests.append(req)
    
    # 3. Link operations - these don't change indices
    for start, end, url in link_ops:
        req = {
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "textStyle": {"link": {"url": url}},
                "fields": "link"
            }
        }
        all_requests.append(req)
    
    # 4. Delete operations - MUST be sorted backwards (highest index first)
    # Remove duplicates and overlapping ranges
    delete_ops = list(set(delete_ops))
    delete_ops.sort(key=lambda x: x[0], reverse=True)
    
    # Merge overlapping deletes
    merged_deletes = []
    for start, end in delete_ops:
        if merged_deletes and start >= merged_deletes[-1][0] and start < merged_deletes[-1][1]:
            # Overlapping, extend
            merged_deletes[-1] = (min(start, merged_deletes[-1][0]), max(end, merged_deletes[-1][1]))
        else:
            merged_deletes.append((start, end))
    
    for start, end in merged_deletes:
        if start < end:
            all_requests.append({
                "deleteContentRange": {
                    "range": {"startIndex": start, "endIndex": end}
                }
            })
    
    print(f"  Found {changes_made} markdown elements. Sending {len(all_requests)} API requests...")
    
    # Send in batches if too many (API limit)
    BATCH_SIZE = 100
    for i in range(0, len(all_requests), BATCH_SIZE):
        batch = all_requests[i:i+BATCH_SIZE]
        token = batch_update(doc_id, batch, token)
        if i + BATCH_SIZE < len(all_requests):
            time.sleep(1)
    
    print(f"  ✅ Done! {changes_made} changes applied.")
    return token, changes_made


def main():
    token = get_token()
    
    # Load document list
    with open("/root/clawd/projects/drive-links.json") as f:
        docs = json.load(f)
    
    # Add Preisstruktur doc
    docs.append({
        "docId": "1g9ufW_S7KOVhFa3Ur7yAEQiQZHjcpfmWlvVxXIqCdAI",
        "name": "Preisstruktur",
        "file": "preisstruktur.md"
    })
    
    results = []
    total_changes = 0
    errors = []
    
    for doc_info in docs:
        doc_id = doc_info["docId"]
        doc_name = doc_info["name"]
        try:
            token, changes = process_document(doc_id, doc_name, token)
            results.append({"name": doc_name, "changes": changes, "status": "ok"})
            total_changes += changes
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            errors.append({"name": doc_name, "error": str(e)})
            results.append({"name": doc_name, "changes": 0, "status": f"error: {e}"})
            # Try to refresh token in case it expired
            try:
                token = refresh_token()
            except:
                pass
    
    # Summary
    docs_changed = sum(1 for r in results if r["changes"] > 0)
    print(f"\n{'='*60}")
    print(f"SUMMARY: {docs_changed}/{len(docs)} documents reformatted, {total_changes} total changes")
    if errors:
        print(f"ERRORS: {len(errors)}")
        for e in errors:
            print(f"  - {e['name']}: {e['error']}")
    
    # Write results to JSON for the caller
    with open("/root/clawd/projects/reformat-results.json", "w") as f:
        json.dump({"results": results, "total_changes": total_changes, "docs_changed": docs_changed, "errors": errors}, f, indent=2)

if __name__ == "__main__":
    main()
