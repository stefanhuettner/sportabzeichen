#!/usr/bin/env python3
"""Upload project markdown files to Google Drive as Google Docs."""

import json
import time
import requests
import sys

# Load token
with open("/root/.openclaw/.google-tokens.json") as f:
    tokens = json.load(f)
ACCESS_TOKEN = tokens["access_token"]

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Document mapping: (filename, doc_title, folder_id, folder_name)
DOCS = [
    # 00 Arbeitsbereich Pia
    ("01-website-analyse.md", "Website-Analyse diestarkmacher.de & kinderleicht", "1RXez6bokt3GqTaQ0ALEu66Blym_LM_nz", "00 Arbeitsbereich Pia"),
    # 01 Löwenstark
    ("05-eltern-onlinekurs-loewenstark.md", "Eltern-Onlinekurs Löwenstark — Konzept", "1nGnYPsnyR0BWu95K_cTarLK1VGKkc17z", "01 Löwenstark"),
    ("15-loewenstark-angebotsseiten-texte.md", "Löwenstark Angebotsseiten-Texte", "1nGnYPsnyR0BWu95K_cTarLK1VGKkc17z", "01 Löwenstark"),
    # 02 kinderleicht
    ("03-funnel-strategie-kinderleicht.md", "Funnel-Strategie #kinderleicht", "1vYs3eCz7hzccI7-P3ya-B6KJAErWVY3g", "02 kinderleicht"),
    ("06-lead-magnet-kinderleicht-entwurf.md", "Lead Magnet #kinderleicht — Entwurf", "1vYs3eCz7hzccI7-P3ya-B6KJAErWVY3g", "02 kinderleicht"),
    ("11-reel-skripte-kinderleicht-maerz.md", "Reel-Skripte #kinderleicht März 2026", "1vYs3eCz7hzccI7-P3ya-B6KJAErWVY3g", "02 kinderleicht"),
    ("12-email-welcome-sequence-kinderleicht.md", "E-Mail Welcome Sequence #kinderleicht", "1vYs3eCz7hzccI7-P3ya-B6KJAErWVY3g", "02 kinderleicht"),
    ("13-hackpack-wutanfall-notfallkoffer.md", "Hackpack Wutanfall-Notfallkoffer", "1vYs3eCz7hzccI7-P3ya-B6KJAErWVY3g", "02 kinderleicht"),
    ("14-webinar-konzept-wutanfaelle-verstehen.md", "Webinar-Konzept: Wutanfälle verstehen", "1vYs3eCz7hzccI7-P3ya-B6KJAErWVY3g", "02 kinderleicht"),
    ("17-paedagogische-profilanalyse-kinderleicht.md", "Pädagogische Profilanalyse #kinderleicht", "1vYs3eCz7hzccI7-P3ya-B6KJAErWVY3g", "02 kinderleicht"),
    ("17-recherche-mama-sprache-wut.md", "Recherche Mama-Sprache & Wut", "1vYs3eCz7hzccI7-P3ya-B6KJAErWVY3g", "02 kinderleicht"),
    ("20-wutanfall-typen-test-freebie.md", "Wutanfall-Typen-Test — Freebie-Konzept", "1vYs3eCz7hzccI7-P3ya-B6KJAErWVY3g", "02 kinderleicht"),
    # 03 ZHS
    ("07-gesamtstrategie-umsatzziel.md", "Gesamtstrategie & Umsatzziel", "19AKBQIHpsipHFtHSZPAMMFKPSYt8xbnV", "03 ZHS"),
    ("16-produkt-treppe-gesamtuebersicht.md", "Produkt-Treppe Gesamtübersicht", "19AKBQIHpsipHFtHSZPAMMFKPSYt8xbnV", "03 ZHS"),
    # 05 Marketing & Design
    ("04-content-plan-instagram-30-tage.md", "Content-Plan Instagram 30 Tage", "1jyqNK27xP-iR8VhwcCZk03QNYBUizibx", "05 Marketing & Design"),
    ("09-instagram-profilanalyse-content-strategie.md", "Instagram Profilanalyse & Content-Strategie", "1jyqNK27xP-iR8VhwcCZk03QNYBUizibx", "05 Marketing & Design"),
    ("10-redaktionskalender-maerz-2026.md", "Redaktionskalender März 2026", "1jyqNK27xP-iR8VhwcCZk03QNYBUizibx", "05 Marketing & Design"),
    ("18-farbpaletten-ueberarbeitung-2026.md", "Farbpaletten-Überarbeitung 2026", "1jyqNK27xP-iR8VhwcCZk03QNYBUizibx", "05 Marketing & Design"),
]

def refresh_token():
    """Refresh the access token."""
    import subprocess
    result = subprocess.run(["python3", "/root/.openclaw/refresh-google-token.py"], capture_output=True, text=True)
    print(f"Token refresh: {result.stdout.strip()}")
    with open("/root/.openclaw/.google-tokens.json") as f:
        tokens = json.load(f)
    return tokens["access_token"]

def api_request(method, url, headers, json_data=None, retries=3):
    """Make an API request with retry logic for rate limits and auth errors."""
    global ACCESS_TOKEN, HEADERS
    for attempt in range(retries):
        if method == "POST":
            r = requests.post(url, headers=headers, json=json_data)
        else:
            r = requests.get(url, headers=headers)
        
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", 30))
            print(f"  Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue
        elif r.status_code == 401:
            print("  Token expired, refreshing...")
            ACCESS_TOKEN = refresh_token()
            HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
            headers = dict(HEADERS)
            continue
        elif r.status_code >= 400:
            print(f"  Error {r.status_code}: {r.text[:200]}")
            if attempt < retries - 1:
                time.sleep(5)
                continue
            r.raise_for_status()
        return r
    return None

def upload_doc(filename, title, folder_id, folder_name):
    """Upload a single markdown file as a Google Doc."""
    filepath = f"/root/clawd/projects/{filename}"
    with open(filepath, "r") as f:
        content = f.read()
    
    # Step 1: Create empty Google Doc in folder
    create_data = {
        "name": title,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [folder_id]
    }
    r = api_request("POST", "https://www.googleapis.com/drive/v3/files", HEADERS, create_data)
    doc_id = r.json()["id"]
    print(f"  Created doc: {doc_id}")
    
    # Step 2: Insert text content
    # We need to insert the content (without the first line which is the title)
    lines = content.split("\n")
    first_line = lines[0].lstrip("# ").strip() if lines else title
    
    # Insert all content at index 1
    batch_data = {
        "requests": [
            {
                "insertText": {
                    "location": {"index": 1},
                    "text": content
                }
            }
        ]
    }
    r = api_request("POST", f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate", HEADERS, batch_data)
    
    # Step 3: Set first line as HEADING_1
    # Find the end of the first line
    first_line_end = len(lines[0]) + 1  # +1 for newline
    heading_data = {
        "requests": [
            {
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": 1,
                        "endIndex": 1 + first_line_end
                    },
                    "paragraphStyle": {
                        "namedStyleType": "HEADING_1"
                    },
                    "fields": "namedStyleType"
                }
            }
        ]
    }
    r = api_request("POST", f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate", HEADERS, heading_data)
    
    time.sleep(1)  # Be gentle with rate limits
    
    return {
        "file": filename,
        "name": title,
        "folder": folder_name,
        "docId": doc_id,
        "url": f"https://docs.google.com/document/d/{doc_id}/edit"
    }

# Main
results = []
total = len(DOCS)
for i, (filename, title, folder_id, folder_name) in enumerate(DOCS, 1):
    print(f"[{i}/{total}] {filename} → \"{title}\" ({folder_name})")
    try:
        result = upload_doc(filename, title, folder_id, folder_name)
        results.append(result)
        print(f"  ✅ Done: {result['url']}")
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        results.append({
            "file": filename,
            "name": title,
            "folder": folder_name,
            "docId": "ERROR",
            "url": f"ERROR: {str(e)}"
        })

# Save results
with open("/root/clawd/projects/drive-links.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✅ Done! {len([r for r in results if r['docId'] != 'ERROR'])}/{total} documents uploaded.")
print("Results saved to /root/clawd/projects/drive-links.json")
