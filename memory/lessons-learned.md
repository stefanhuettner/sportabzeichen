# Lessons Learned — Fehler die wir nicht wiederholen

_Jedes gelöste Problem wird hier dokumentiert. Pia checkt diese Liste bevor sie etwas umsetzt._

## 12.03.2026

### Google Docs: Links immer klickbar machen!
- Wenn ich URLs in Google Docs einfüge (via insertText), sind sie NUR Plaintext — NICHT klickbar
- IMMER danach `updateTextStyle` mit `link.url` auf den URL-Bereich anwenden
- Stefan will solche Details nicht selbst im Kopf behalten müssen → meine Verantwortung
- Gilt für ALLE Google Docs die ich erstelle oder bearbeite

## 09.03.2026

### Notion-Formatierung kaputt
- **Problem:** Dokumente als Rohtext mit Unicode-Escapes hochgeladen
- **Ursache:** Einfaches JSON-Encoding statt richtige Markdown→Notion-Block-Konvertierung
- **Lösung:** Python-Script `/tmp/notion_upload.py` mit `md_to_blocks()` Parser
- **Merke:** Notion braucht native Blöcke (heading_2, bulleted_list_item, etc.), NICHT Markdown als Text

### Exec-Security blockiert Cron-Jobs
- **Problem:** npm update im Cron-Job brauchte manuelle Freigabe
- **Ursache:** `tools.exec.security: "allowlist"` — npm nicht auf der Liste
- **Lösung:** `tools.exec.security: "full"` (Stefan ist einziger Nutzer)
- **Merke:** Bei neuen Cron-Jobs immer prüfen ob exec-Rechte reichen

### Telegram doppelte Nachrichten
- **Problem:** Identische Textblöcke erscheinen doppelt
- **Ursache:** `channels.telegram.streaming: "partial"` + Gateway-Neustarts
- **Lösung:** Streaming auf "off" gesetzt
- **Merke:** Nach Gateway-Restart aufpassen — Kontext kann kurz unterbrochen sein

### Slack Channels nicht erreichbar
- **Problem:** Bot antwortet nicht in Slack Channels
- **Ursache:** `groupPolicy: "allowlist"` aber keine Channel-IDs konfiguriert
- **Lösung:** Alle 6 Channels mit `allow: true, requireMention: false` hinzugefügt
- **Merke:** Neue Slack-Channels immer auch in der Config freischalten

### Keine Markdown-Tabellen in Telegram
- **Problem:** Tabellen werden als hässlicher Monospace-Text angezeigt
- **Ursache:** Telegram unterstützt keine Markdown-Tabellen
- **Lösung:** Listen verwenden (✅/🚫 + Bullet Points). Tabellen nur in Notion + Slack.
- **Merke:** Immer ans Ausgabeformat denken!

### Token-Verschwendung durch Brute-Force-Debugging
- **Problem:** Hoher Token-Verbrauch an einem Tag
- **Ursache:** Config-Docs 5x geladen, dutzende FTP-Varianten durchprobiert statt zu fragen
- **Lösung:** Erst fragen, dann probieren. Docs einmal lesen und merken. Smarter debuggen.
- **Merke:** ZHS-Mindset auch beim Debugging: Sweet Spot finden, nicht alles durchprobieren

### Gateway-Crash durch ungültige Config-Keys
- **Problem:** Gateway in Crash-Schleife
- **Ursache:** Ungültige Keys `skills.nano-banana-pro`, `skills.ftp-deploy`, `skills.mailerlite` in openclaw.json geschrieben
- **Lösung:** Keys entfernt, Gateway neu gestartet
- **Merke:** NIEMALS freie Keys in openclaw.json schreiben! Nur dokumentierte Config-Pfade verwenden. API-Tokens als `env.*` speichern, eigene Daten in separate Dateien (z.B. .ftp-creds). Im Zweifel erst Docs lesen.

### Nachtschicht-Bericht zur falschen Uhrzeit
- **Problem:** Bericht um 1:01 Uhr Berlin statt 7:00 Uhr
- **Ursache:** Bericht direkt im Cron-Job gesendet statt zeitversetzt
- **Lösung:** Bericht in Datei vorbereiten, separaten Cron für 7:00 Uhr einrichten
- **Merke:** Nachtarbeit = still arbeiten, Ergebnisse morgens um 7:00 liefern

## 12.03.2026

### NotebookLM: Picker-Limit & Duplikate
- **Problem:** Ctrl+A im Drive-Picker wählt max 50 Dateien. Bei 57 Dateien fehlten 7. Zweiter Ctrl+A erzeugte 49 Duplikate die sich nicht automatisch löschen ließen.
- **Ursache:** Picker zeigt nur 50 Dateien pro Ordner. NotebookLM Bestätigungsdialog beim Löschen blockiert Playwright-Scripts.
- **Lösung:** Überzählige Dateien in Drive-Unterordner kopieren, dann Batch 2 separat laden.
- **Merke:** Bei >50 Dateien: aufteilen in Unterordner à max 50. NIE 2x Ctrl+A aus gleichem Ordner → erzeugt Duplikate die schwer zu löschen sind.
