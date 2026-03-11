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
- Hosting: dogado Shared Hosting, web314.dogado.net, SFTP verbunden ✅ (User: h606421, PW in .ftp-creds)
- dogado Ordner: diestarkmacherde, susannehuettnerde, kinderleichtmitsusannede, stefanhuettnerde, susannehuettnercom, susanne-kinderleichtde
- MailerLite: 2 Accounts (MAILERLITE_TOKEN_KINDERLEICHT + MAILERLITE_TOKEN_STARKMACHER), IP-restricted auf 178.104.16.167
- Lessons Learned Datei: memory/lessons-learned.md — Fehler dokumentieren, nie wiederholen
- Gmail Account: piagiraffe04@gmail.com — App-Passwort in .gmail-creds, IMAP verbunden
- Google Drive Wissensbasis-Ordner: https://drive.google.com/drive/folders/16EPViHuPoRD-MJwcVe3dXmbsni1L44CR (Löwenstark Kurs + ZHS Hintergrund)
- Referenzfotos: assets/stefan/ (4 Fotos) + assets/susanne/ (3 Fotos)
- Kalender-Zugang: 3 iCloud webcal-Links (Familie, PSBK, Privat) in .calendar-links — direkt lesbar
- Google Kalender (Starkmacher + #kinderleicht): Einladungen da, braucht OAuth2
- Google Drive: Öffentliche Links geschlossen, Zugang jetzt über piagiraffe04@gmail.com Einladung → OAuth2 nötig
- dogado E-Mail pia@stefanhuettner.de gelöscht (MX zeigt auf Google Workspace)
- Stefan hat Google Workspace für stefanhuettner.de (Business Standard, 16,20€/Mo)
- Hetzner Cloud Firewall aktiv: nur TCP 2222 + ICMP, alles andere blockiert
- ufw/iptables geht nicht auf Hetzner (Kernel-Einschränkung) → Hetzner Cloud Firewall nutzen
- Notion "Stefans To-Dos" DB: 49c0cc2d-76c0-4318-af06-da2fb00dccaf (Top 3 + Optional nach jeder Nachtschicht)
- Tagesrhythmus: 06:00 Morgen-Briefing, 20:00 Abend-Report
- Susanne: Slack + Notion Gast-Zugriff eingerichtet ✅
- Notion API Lesson: Properties über 2022-06-28 API Version updaten, 2025-09-03 ignoriert sie beim Create
- Notion scraping: undokumentierte API www.notion.so/api/v3/loadPageChunk für öffentliche Seiten
- Google OAuth2 eingerichtet ✅ (11.03.2026) — Scopes: Drive (rw), Calendar (ro), Gmail (ro)
- OAuth Client: "Pia Server" (Desktop-App), Client ID: 809456498194-...apps.googleusercontent.com
- OAuth Tokens: /root/.openclaw/.google-tokens.json (mit Refresh Token), OAuth Config: .google-oauth.json
- Token-Refresh Script: /root/.openclaw/refresh-google-token.py
- Redirect für OAuth: localhost (nicht oob, wird von Google nicht mehr unterstützt)
- Google Drive: 7 Ordner angelegt, IDs in /root/.openclaw/.drive-folders.json
- Google Calendar API: aktiviert, Starkmacher/#kinderleicht müssen noch neu geteilt werden
- Wöchentlicher Security-Audit Cron: Samstag 03:00 Berlin (eingerichtet 11.03.2026)
- Slack Token: nicht als env var verfügbar, aus openclaw.json lesen
- Telegram Bot-Limit: kann nur eigene + kürzlich empfangene Nachrichten löschen, nicht User-Nachrichten
