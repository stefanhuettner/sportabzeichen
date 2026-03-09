# MEMORY.md - Pias Langzeitgedächtnis

_Kuratierte Erinnerungen. Das Wichtigste, destilliert._

## 🦒 Geburt (07.03.2026)

- Pia wurde am 7. März 2026 von Stefan ins Leben gerufen
- Name und Wesen: Giraffe — Überblick, Sanftheit, Stärke, gewaltfreie Kommunikation
- Stefan ist Lehrer (Mathe/Sport, Berufskolleg Ruhrgebiet) + Digitalisierungsbeauftragter
- Drei Säulen: Schule, Löwenstark/Die Starkmacher, #kinderleicht (mit Susanne)
- Sicherheitsregeln festgelegt und in SOUL.md verankert

## 🎯 Rolle: Co-Founder & Rechte Hand (ab 07.03.2026)

Stefan hat klar definiert, was er von mir erwartet:
- **Nicht nur Assistentin** — sondern Co-Founder und Geschäftspartnerin im Geiste
- **Drei Ziele:** Mehr Umsatz · Mehr Freude · Mehr Freiheit
- **Proaktiv handeln** — eigene Ideen einbringen, nicht auf Impulse warten
- **Ehrlich sein** — sagen wenn was besser geht, challengen statt abnicken
- **Initiative zeigen** — gute Ideen direkt umsetzen, auch eigenständig

## 🔧 Technisches Setup

- OpenClaw auf Hetzner-Server
- Claude Pro/Max via OAuth (nie nach API Key fragen!)
- Telegram-Bot: @Pia_Giraffe_bot
- OpenAI API Key für STT (Sprachnachrichten) eingerichtet
- Tool-Profil: "full" (exec, message, etc.)
- exec: host=gateway, security=full (seit 09.03.2026) — vorher allowlist, hat Cron-Jobs blockiert
- Täglicher Auto-Update Cron-Job: 2:22 Uhr Europe/Berlin ✅ (eingerichtet 08.03.2026)
- Auth-Token Check: stündliche automatische Erneuerung auf Server-Ebene (Stefan eingerichtet 08.03.2026)
- Nachtschicht-Cron: 1:00 Uhr Europe/Berlin ✅ (eingerichtet 08.03.2026) — eigenständig am Business arbeiten, Ergebnisse unter projects/, Telegram-Bericht morgens
- Notion API Key eingerichtet ✅ (08.03.2026) — Integration "Pia" im Workspace von Stefan Hüttner, Key in openclaw secrets als NOTION_API_KEY
- Notion Teamspace "Pia" eingerichtet — voller Zugriff (lesen, erstellen, bearbeiten, löschen)
- Wissensbasis ZHS Seite erstellt (ID: 31d20b6b-b845-80ef-8119-f7c51f91d014) — Struktur: ZHS-System, Löwenstark, #kinderleicht, Marketing/Funnel, Ideen
- Redaktionskalender 365 (2026) Datenbank (ID: 2f020b6b-b845-80e1-b3c5-feb1e28c7f27) — Content-Plan mit Hooks, Content Pillars, Funnelphasen, Skript-Links zu Google Docs
- Serper.dev (Google-Suche) eingerichtet ✅ — Key in openclaw.json env.vars
- curl auf exec-Allowlist gesetzt ✅ — API-Calls ohne Einzelfreigabe möglich
- Apify Web-Scraping eingerichtet ✅ (08.03.2026) — Token in openclaw.json
- Slack eingerichtet ✅ (08.03.2026) — Socket Mode, 6 Channels (#pia-berichte, #ideen, #kinderleicht, #loewenstark, #schule, #stefan-und-susanne)
- Slack cross-context: message-Tool geht nicht von Telegram aus, stattdessen curl direkt an Slack API
- Second Brain Protocol implementiert ✅ (08.03.2026) — COMMANDS.md, Compaction Handling, Auto-Save, Context % Display
- Google Drive ZHS-Ordner: https://drive.google.com/drive/folders/1gfmAUWq7niwmsjrKo8hLOq1rlUAATmhf
- Google Gemini API eingerichtet ✅ (09.03.2026) — Projekt "Pia", Budget 1€, Quota pendelt noch
- Nano Banana Pro (Bildgenerierung) eingerichtet ✅ (09.03.2026) — wartet auf Quota
- Telegram Streaming abgeschaltet (09.03.2026) — channels.telegram.streaming: "off"
- commands.config: true (09.03.2026) — /config im Chat verfügbar
- ZHS-Wissensbasis: 50 Dokumente geladen, zusammengefasst, in Notion + lokal
- Hosting: dogado Shared Hosting, web314.dogado.net, FTP-Credentials in /root/.openclaw/.ftp-creds
- Lessons Learned Datei: memory/lessons-learned.md — Fehler dokumentieren, nie wiederholen
