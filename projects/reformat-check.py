#!/usr/bin/env python3
"""Check a doc for remaining markdown artifacts and fix them."""

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
    r.raise_for_status()
    return r.json()

def batch_update(doc_id, reqs, token):
    if not reqs:
        return
    r = requests.post(f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
                      headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                      json={"requests": reqs})
    if r.status_code != 200:
        print(f"ERROR: {r.status_code} {r.text[:1000]}")
    r.raise_for_status()

def main():
    token = refresh_token()
    doc = get_doc(DOC_ID, token)
    
    # Collect all delete operations needed
    delete_ops = []
    
    body = doc.get("body", {})
    for elem in body.get("content", []):
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        
        for el in para.get("elements", []):
            if "textRun" not in el:
                continue
            tr = el["textRun"]
            content = tr["content"]
            start = el["startIndex"]
            
            # Find ** markers
            for m in re.finditer(r'\*\*', content):
                delete_ops.append((start + m.start(), start + m.end()))
            
            # Find standalone * markers (italic) - not part of **
            for m in re.finditer(r'(?<!\*)\*(?!\*)', content):
                delete_ops.append((start + m.start(), start + m.end()))
            
            # Find ~~ markers
            for m in re.finditer(r'~~', content):
                delete_ops.append((start + m.start(), start + m.end()))
            
            # Find backticks
            for m in re.finditer(r'`', content):
                delete_ops.append((start + m.start(), start + m.end()))
            
            # Find heading markers at start of paragraph
            if content.startswith("### "):
                delete_ops.append((start, start + 4))
            elif content.startswith("## "):
                delete_ops.append((start, start + 3))
            elif content.startswith("# "):
                delete_ops.append((start, start + 2))
            
            # Horizontal rules
            if content.strip() in ("---", "***", "___"):
                end = el["endIndex"]
                if end - 1 > start:
                    delete_ops.append((start, end - 1))
    
    if not delete_ops:
        print("No markdown artifacts found!")
        return
    
    # Sort backwards by start position
    delete_ops.sort(key=lambda x: (-x[0], -x[1]))
    
    # Remove exact duplicates
    seen = set()
    unique_ops = []
    for op in delete_ops:
        if op not in seen:
            seen.add(op)
            unique_ops.append(op)
    
    # Check for overlaps and handle them
    final_ops = []
    for s, e in unique_ops:
        if s >= e:
            continue
        # Check if this overlaps with already added (they're sorted desc)
        overlap = False
        for fs, fe in final_ops:
            if s < fe and e > fs:
                overlap = True
                break
        if not overlap:
            final_ops.append((s, e))
    
    print(f"Found {len(final_ops)} markdown artifacts to delete")
    for s, e in final_ops[:10]:
        print(f"  Delete [{s}:{e}]")
    if len(final_ops) > 10:
        print(f"  ... and {len(final_ops) - 10} more")
    
    # Build delete requests (already sorted backwards)
    reqs = [{"deleteContentRange": {"range": {"startIndex": s, "endIndex": e}}} for s, e in final_ops]
    
    print(f"Sending {len(reqs)} delete requests...")
    batch_update(DOC_ID, reqs, token)
    print("✅ Done!")

if __name__ == "__main__":
    main()
