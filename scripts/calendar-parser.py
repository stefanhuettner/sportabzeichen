#!/usr/bin/env python3
"""Kalender-Parser für Stefans iCloud Kalender.
Löst das Duplikat-Problem bei wiederkehrenden Events.

Regeln:
1. Bei wiederkehrenden Events mit ähnlichem Namen am gleichen Wochentag → nur das neueste
2. PSBK/Unterricht gelten als gleiche Kategorie
3. Events mit UNTIL-Datum das in der Vergangenheit liegt → ignorieren
4. Einzelevents immer anzeigen
"""

import urllib.request, re, sys, json
from datetime import datetime, timedelta
from collections import defaultdict

def load_links():
    with open('/root/.openclaw/.calendar-links') as f:
        links = {}
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, url = line.strip().split('=', 1)
                name = key.replace('CALENDAR_', '').title()
                links[name] = url
        return links

def normalize_name(name):
    """Normalize event names for dedup grouping"""
    n = name.strip().lower()
    # PSBK and Unterricht are the same category
    if n in ('psbk', 'unterricht'):
        return 'psbk_unterricht'
    return n

def parse_events(target_date):
    links = load_links()
    all_events = []
    
    for cal_name, url in links.items():
        try:
            data = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
        except:
            continue
        
        events = data.split("BEGIN:VEVENT")
        for ev in events[1:]:
            summary = dtstart_raw = dtend_raw = rrule = ""
            
            for line in ev.split("\n"):
                line = line.strip()
                if line.startswith("SUMMARY:"):
                    summary = line[8:]
                elif "DTSTART" in line:
                    dtstart_raw = line
                elif "DTEND" in line:
                    dtend_raw = line
                elif line.startswith("RRULE:"):
                    rrule = line[6:]
            
            date_match = re.search(r'(\d{8})', dtstart_raw)
            time_match = re.search(r'T(\d{2})(\d{2})', dtstart_raw)
            if not date_match:
                continue
            
            orig_date = datetime.strptime(date_match.group(1), "%Y%m%d")
            start_time = f"{time_match.group(1)}:{time_match.group(2)}" if time_match else "ganztags"
            
            end_match = re.search(r'T(\d{2})(\d{2})', dtend_raw)
            end_time = f"{end_match.group(1)}:{end_match.group(2)}" if end_match else ""
            
            # Check UNTIL
            until_match = re.search(r'UNTIL=(\d{8})', rrule)
            if until_match:
                until = datetime.strptime(until_match.group(1), "%Y%m%d")
                if until < target_date:
                    continue
            
            is_recurring = "FREQ=WEEKLY" in rrule
            is_match = False
            
            if not is_recurring:
                if date_match.group(1) == target_date.strftime("%Y%m%d"):
                    is_match = True
                # Check ganztags spanning events
                if "VALUE=DATE" in dtstart_raw:
                    end_date_match = re.search(r'(\d{8})', dtend_raw)
                    if end_date_match:
                        end_d = datetime.strptime(end_date_match.group(1), "%Y%m%d")
                        if orig_date <= target_date < end_d:
                            is_match = True
            else:
                if orig_date.weekday() == target_date.weekday() and orig_date <= target_date:
                    is_match = True
            
            if is_match:
                all_events.append({
                    "summary": summary,
                    "time": start_time,
                    "end": end_time,
                    "orig_date": orig_date,
                    "recurring": is_recurring,
                    "calendar": cal_name,
                })
    
    # Deduplicate recurring events
    groups = defaultdict(list)
    single_events = []
    
    for ev in all_events:
        if ev['recurring']:
            key = normalize_name(ev['summary'])
            groups[key].append(ev)
        else:
            single_events.append(ev)
    
    deduped = list(single_events)
    for key, evs in groups.items():
        newest = max(evs, key=lambda x: x['orig_date'])
        deduped.append(newest)
    
    deduped.sort(key=lambda e: e['time'] if e['time'] != 'ganztags' else '00:00')
    return deduped

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = datetime.strptime(sys.argv[1], "%Y-%m-%d")
    else:
        target = datetime.now()
    
    events = parse_events(target)
    
    weekdays_de = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    wd = weekdays_de[target.weekday()]
    print(f"📅 {wd}. {target.strftime('%d.%m.%Y')}")
    print()
    
    if not events:
        print("  Keine Termine")
    else:
        for ev in events:
            end = f"–{ev['end']}" if ev['end'] else ""
            emoji = {"Familie": "👨‍👩‍👧‍👦", "Psbk": "🏫", "Privat": "📌"}.get(ev['calendar'], "📅")
            print(f"  {emoji} {ev['time']}{end} — {ev['summary']}")
