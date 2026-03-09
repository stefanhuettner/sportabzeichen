# Lessons Learned — Fehler die wir nicht wiederholen

_Jedes gelöste Problem wird hier dokumentiert. Pia checkt diese Liste bevor sie etwas umsetzt._

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

### Nachtschicht-Bericht zur falschen Uhrzeit
- **Problem:** Bericht um 1:01 Uhr Berlin statt 7:00 Uhr
- **Ursache:** Bericht direkt im Cron-Job gesendet statt zeitversetzt
- **Lösung:** Bericht in Datei vorbereiten, separaten Cron für 7:00 Uhr einrichten
- **Merke:** Nachtarbeit = still arbeiten, Ergebnisse morgens um 7:00 liefern
