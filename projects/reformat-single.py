#!/usr/bin/env python3
"""Retry reformatting for the failed Wutanfall-Typen-Test doc with safer delete handling."""

import json
import re
import requests
import subprocess
import time

TOKENS_PATH = "/root/.openclaw/.google-tokens.json"
DOC_ID = "1DUPKCRDpU42QNkF56cdcouK3_J4j3umHdnkLRkDaK2g"

def get_token():
    with open(TOKENS_PATH) as f:
        return json.load(f)["access_token"]

def refresh_token():
    subprocess.run(["python3", "/root/.openclaw/refresh-google-token.py"], check=True, capture_output=True)
    return get_token()

def get_doc(doc_id, token):
    r = requests.get(f"https://docs.googleapis.com/v1/documents/{doc_id}", 
                     headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 401:
        token = refresh_token()
        r = requests.get(f"https://docs.googleapis.com/v1/documents/{doc_id}",
                         headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    return r.json(), token

def batch_update(doc_id, reqs, token):
    if not reqs:
        return token
    r = requests.post(f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
                      headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                      json={"requests": reqs})
    if r.status_code == 401:
        token = refresh_token()
        r = requests.post(f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
                          headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                          json={"requests": reqs})
    if r.status_code != 200:
        print(f"ERROR: {r.status_code} {r.text[:1000]}")
    r.raise_for_status()
    return token

def main():
    token = refresh_token()
    doc, token = get_doc(DOC_ID, token)
    
    doc_end_index = doc["body"]["content"][-1]["endIndex"]
    
    style_requests = []
    format_requests = []
    delete_ops = []  # (start, end)
    link_requests = []
    
    body = doc.get("body", {})
    for elem in body.get("content", []):
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        pstart = elem["startIndex"]
        pend = elem["endIndex"]
        
        # Get full text
        full_text = ""
        text_start = None
        for el in para.get("elements", []):
            if "textRun" in el:
                if text_start is None:
                    text_start = el["startIndex"]
                full_text += el["textRun"]["content"]
        
        if text_start is None:
            continue
        
        # Headings
        if full_text.startswith("### "):
            style_requests.append({"updateParagraphStyle": {
                "range": {"startIndex": pstart, "endIndex": pend},
                "paragraphStyle": {"namedStyleType": "HEADING_3"}, "fields": "namedStyleType"}})
            delete_ops.append((text_start, text_start + 4))
        elif full_text.startswith("## "):
            style_requests.append({"updateParagraphStyle": {
                "range": {"startIndex": pstart, "endIndex": pend},
                "paragraphStyle": {"namedStyleType": "HEADING_2"}, "fields": "namedStyleType"}})
            delete_ops.append((text_start, text_start + 3))
        elif full_text.startswith("# "):
            style_requests.append({"updateParagraphStyle": {
                "range": {"startIndex": pstart, "endIndex": pend},
                "paragraphStyle": {"namedStyleType": "HEADING_1"}, "fields": "namedStyleType"}})
            delete_ops.append((text_start, text_start + 2))
        
        # Horizontal rules
        stripped = full_text.strip()
        if stripped in ("---", "***", "___"):
            # Delete content but keep newline
            if pend - 1 > pstart:
                delete_ops.append((pstart, pend - 1))
            continue
        
        # Bold **text**
        for m in re.finditer(r'\*\*(.+?)\*\*', full_text):
            inner_s = text_start + m.start(1)
            inner_e = text_start + m.end(1)
            format_requests.append({"updateTextStyle": {
                "range": {"startIndex": inner_s, "endIndex": inner_e},
                "textStyle": {"bold": True}, "fields": "bold"}})
            delete_ops.append((inner_e, inner_e + 2))
            delete_ops.append((text_start + m.start(), text_start + m.start() + 2))
        
        # Italic *text* (not inside **)
        for m in re.finditer(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', full_text):
            inner_s = text_start + m.start(1)
            inner_e = text_start + m.end(1)
            format_requests.append({"updateTextStyle": {
                "range": {"startIndex": inner_s, "endIndex": inner_e},
                "textStyle": {"italic": True}, "fields": "italic"}})
            delete_ops.append((inner_e, inner_e + 1))
            delete_ops.append((text_start + m.start(), text_start + m.start() + 1))
        
        # Strikethrough ~~text~~
        for m in re.finditer(r'~~(.+?)~~', full_text):
            inner_s = text_start + m.start(1)
            inner_e = text_start + m.end(1)
            format_requests.append({"updateTextStyle": {
                "range": {"startIndex": inner_s, "endIndex": inner_e},
                "textStyle": {"strikethrough": True}, "fields": "strikethrough"}})
            delete_ops.append((inner_e, inner_e + 2))
            delete_ops.append((text_start + m.start(), text_start + m.start() + 2))
        
        # Backticks
        for m in re.finditer(r'`([^`]+?)`', full_text):
            inner_e = text_start + m.end(1)
            delete_ops.append((inner_e, inner_e + 1))
            delete_ops.append((text_start + m.start(), text_start + m.start() + 1))
        
        # URLs
        for m in re.finditer(r'(https?://[^\s\)>\]]+)', full_text):
            url = m.group(1)
            link_requests.append({"updateTextStyle": {
                "range": {"startIndex": text_start + m.start(), "endIndex": text_start + m.end()},
                "textStyle": {"link": {"url": url}}, "fields": "link"}})
    
    # Step 1: Apply styles and formatting (no index changes)
    non_delete = style_requests + format_requests + link_requests
    if non_delete:
        print(f"Applying {len(non_delete)} style/format requests...")
        token = batch_update(DOC_ID, non_delete, token)
        time.sleep(1)
    
    # Step 2: Sort deletes backwards, remove overlaps, validate ranges
    delete_ops = list(set(delete_ops))
    delete_ops.sort(key=lambda x: x[0], reverse=True)
    
    # Remove overlapping ranges (keeping the larger one)
    cleaned = []
    for s, e in delete_ops:
        if s >= e or s < 1 or e > doc_end_index:
            print(f"  Skipping invalid range: ({s}, {e})")
            continue
        if cleaned and s < cleaned[-1][1]:
            # Overlap with previous (which has higher start), merge
            prev_s, prev_e = cleaned[-1]
            cleaned[-1] = (min(s, prev_s), max(e, prev_e))
        else:
            cleaned.append((s, e))
    
    delete_requests = [{"deleteContentRange": {"range": {"startIndex": s, "endIndex": e}}} for s, e in cleaned]
    
    if delete_requests:
        print(f"Applying {len(delete_requests)} delete requests (backwards)...")
        token = batch_update(DOC_ID, delete_requests, token)
    
    print("✅ Done!")

if __name__ == "__main__":
    main()
