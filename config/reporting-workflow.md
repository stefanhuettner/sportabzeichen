# Berichts- & Übersichts-Workflow

## Regel: Kein doppeltes Posten. Jeder Kanal hat EINE Aufgabe.

### Notion = Wissensspeicher
- **Nachtschicht-Berichte** komplett mit allen Dokumenten als Unterseiten
- **To-Do-Datenbank** mit allen Aufgaben (erledigte bleiben, Spalte "Wer": Stefan/Pia)
- **Dashboard** als Stefans Startseite (Links zu allem)

### Telegram = Täglicher Dialog mit Stefan
- **06:00 Morgen-Briefing:** ALLE Kalender-Termine (inkl. PSBK/Schule!), Top 3 To-Dos, kurze Nachtschicht-Zusammenfassung
- **20:00 Abend-Report:** Tagesrückblick (Motivation!), was offen ist, Nachtschicht-Plan, "Änderungswünsche?"
- Direkter Chat für alles andere

### Slack = Projekt-Dashboard + Arbeitslog
- Jeder Channel hat eine **GEPINNTE STATUS-NACHRICHT** → regelmäßig aktualisieren
- Struktur: ✅ Fertig / 🔄 In Arbeit / ⏳ Wartet auf Stefan / ⏭️ Nächste Schritte
- Bei fertiggestellter Arbeit → kurze Info im passenden Channel
- Susanne sieht #kinderleicht-Updates direkt
- Stefan öffnet Slack → sieht sofort den aktuellen Stand pro Projekt

## Nach JEDER Nachtschicht (Checkliste!)
1. ✅ Bericht in Notion anlegen (unter "Berichte" → Hauptseite + Dokumente)
2. ✅ Gepinnte Slack-Status-Nachrichten aktualisieren
3. ✅ Notion To-Dos aktualisieren (Top 3 + Optional, "Wer"-Spalte pflegen)
4. ✅ 06:00 Telegram: Kurze Zusammenfassung + Kalender

## Gepinnte Slack-Nachrichten
- #kinderleicht (C0AK7H2GQ86): ts=1773239798.680659
- #loewenstark (C0AK37BL56F): ts=1773239800.349849
- #pia-berichte (C0AKD6ZL4BE): ts=1773239801.982709

## Notion-Struktur (Pias Workspace)
- 🦒 Dashboard: 32020b6b-b845-8143-8965-fee6eed2d20e
- 🌙 Berichte: 32020b6b-b845-81d8-9187-fc3572baf642
- 📚 Wissensbasis: 32020b6b-b845-8186-861c-f2b4e7cf6579
- 📋 To-Dos DB: 49c0cc2d-76c0-4318-af06-da2fb00dccaf
- Workspace (Parent): 31d20b6b-b845-80ef-8119-f7c51f91d014

## Notion API Limits
- Kann KEINE Top-Level Seiten erstellen (nur unter parent page)
- Kann Seiten NICHT zwischen Parents verschieben
- Kann KEINE Views/Ansichten erstellen (nur in Notion-App)
- Neue Berichte als Unterseiten unter "Berichte" anlegen (parent: Berichte-ID)

## Susannes Workflow
- **Slack #susannes-bereich** (C0AKJ8WA6UF) = ihr einziger Kanal
- **Google Drive "Für Susanne"** = alle fertigen Dokumente als Google Docs
  - Ordner: https://drive.google.com/drive/folders/1VgN_KHJHLxF5rECI_op-25GWvzHFLwrV
  - Unterordner: Skripte & Texte, Reel-Vorlagen, Newsletter, Bilder & Design
- Gepinnte Nachricht in #susannes-bereich = ihr Dashboard (mit Drive-Links!)
- Susanne kann direkt in Google Docs kommentieren

## AUTOMATISCH bei jedem neuen #kinderleicht-Dokument:
1. Als Google Doc in "Für Susanne" hochladen (passender Unterordner)
2. Gepinnte Nachricht in #susannes-bereich aktualisieren (mit Link)
3. Kurze Info in #susannes-bereich posten ("Neues Dokument: ...")
→ Das passiert OHNE Erinnerung, automatisch!
