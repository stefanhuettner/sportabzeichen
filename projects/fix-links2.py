#!/usr/bin/env python3
"""Scan ALL actual Google Docs for plain-text URLs, make them clickable, verify links."""

import json, re, time, requests

with open("/root/.openclaw/.google-tokens.json") as f:
    tokens = json.load(f)
access_token = tokens["access_token"]
headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

# Get ALL docs from Drive
resp = requests.get(
    'https://www.googleapis.com/drive/v3/files?q=mimeType="application/vnd.google-apps.document"&pageSize=50&fields=files(id,name)&orderBy=modifiedTime desc',
    headers=headers
)
all_docs = resp.json().get("files", [])
print(f"Found {len(all_docs)} documents in Drive\n")

URL_PATTERN = re.compile(r'https?://[^\s\u00A0\u200B\u2028\u2029\n\r\t\]\)>}{\"\']+')

stats = {
    "docs_checked": 0,
    "total_urls_found": 0,
    "urls_fixed": 0,
    "urls_already_linked": 0,
    "mismatched_links": [],
    "broken_urls": [],
    "errors": [],
    "fixed_details": [],
}
all_unique_urls = set()

def find_urls_in_doc(doc):
    results = []
    body = doc.get("body", {})
    
    def process_elements(elements):
        for elem in elements:
            if "paragraph" in elem:
                for pe in elem["paragraph"].get("elements", []):
                    if "textRun" in pe:
                        tr = pe["textRun"]
                        content = tr.get("content", "")
                        start = pe.get("startIndex", 0)
                        style = tr.get("textStyle", {})
                        link = style.get("link", {})
                        link_url = link.get("url", "")
                        
                        for m in URL_PATTERN.finditer(content):
                            url = m.group(0).rstrip('.,;:!?)>')
                            url_start = start + m.start()
                            url_end = url_start + len(url)
                            has_link = bool(link_url)
                            results.append((url, url_start, url_end, has_link, link_url))
            
            if "table" in elem:
                for row in elem["table"].get("tableRows", []):
                    for cell in row.get("tableCells", []):
                        process_elements(cell.get("content", []))
            if "tableOfContents" in elem:
                process_elements(elem["tableOfContents"].get("content", []))
    
    process_elements(body.get("content", []))
    return results

def fix_links_in_doc(doc_id, urls_to_fix):
    if not urls_to_fix:
        return 0
    
    reqs = []
    for url, start, end, _, _ in sorted(urls_to_fix, key=lambda x: x[1], reverse=True):
        reqs.append({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "textStyle": {"link": {"url": url}},
                "fields": "link"
            }
        })
    
    fixed = 0
    for i in range(0, len(reqs), 100):
        batch = reqs[i:i+100]
        resp = requests.post(
            f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
            headers=headers, json={"requests": batch}
        )
        if resp.status_code == 200:
            fixed += len(batch)
        else:
            stats["errors"].append(f"BatchUpdate {doc_id}: {resp.status_code} - {resp.text[:200]}")
            print(f"    ❌ BatchUpdate error: {resp.status_code} - {resp.text[:200]}")
    return fixed

def check_url(url):
    try:
        resp = requests.head(url, timeout=10, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        return resp.status_code
    except:
        try:
            resp = requests.get(url, timeout=10, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}, stream=True)
            return resp.status_code
        except:
            return -1

for doc_info in all_docs:
    doc_id = doc_info["id"]
    doc_name = doc_info["name"]
    print(f"📄 {doc_name}")
    
    resp = requests.get(f"https://docs.googleapis.com/v1/documents/{doc_id}", headers=headers)
    if resp.status_code != 200:
        print(f"  ❌ Fetch failed: {resp.status_code}")
        stats["errors"].append(f"Fetch {doc_name}: {resp.status_code}")
        continue
    
    doc = resp.json()
    stats["docs_checked"] += 1
    urls = find_urls_in_doc(doc)
    
    if not urls:
        print(f"  No URLs found")
        continue
    
    stats["total_urls_found"] += len(urls)
    print(f"  Found {len(urls)} URLs")
    
    to_fix = []
    for url, start, end, has_link, link_url in urls:
        all_unique_urls.add(url)
        if not has_link:
            to_fix.append((url, start, end, has_link, link_url))
            print(f"  🔧 Unlinked: {url[:80]} [{start}:{end}]")
        else:
            stats["urls_already_linked"] += 1
            if link_url and link_url != url and url not in link_url and link_url not in url:
                stats["mismatched_links"].append({"doc": doc_name, "displayed": url, "linked_to": link_url})
                print(f"  ⚠️ Mismatch: '{url[:60]}' → '{link_url[:60]}'")
    
    if to_fix:
        fixed = fix_links_in_doc(doc_id, to_fix)
        stats["urls_fixed"] += fixed
        for url, start, end, _, _ in to_fix:
            stats["fixed_details"].append({"doc": doc_name, "url": url})
        print(f"  ✅ Fixed {fixed} links")
    
    time.sleep(0.3)

# Check unique external URLs
print(f"\n🔍 Checking {len(all_unique_urls)} unique URLs...")
for url in sorted(all_unique_urls):
    if any(d in url for d in ["docs.google.com", "drive.google.com", "forms.google.com"]):
        print(f"  ⏭️ Skip (Google): {url[:80]}")
        continue
    status = check_url(url)
    if status not in (200, 301, 302, 303, 307, 308, 403, 405, 406):
        stats["broken_urls"].append({"url": url, "status": status})
        print(f"  ❌ {status}: {url}")
    else:
        print(f"  ✅ {status}: {url[:80]}")
    time.sleep(0.2)

print("\n" + "="*60)
print(json.dumps(stats, indent=2, ensure_ascii=False))
