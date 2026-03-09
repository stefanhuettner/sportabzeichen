# COMMANDS.md - Custom Slash Commands

## /save
Session-Ende. Alles sichern + Resume Prompt generieren.
1. Kontext erkennen – Projekt oder allgemeines Gespräch?
2. Projekt: ROADMAP.md updaten, Conversation Summary speichern, Learnings sichern
3. Allgemein: Summary nach memory/YYYY-MM-DD.md, MEMORY.md updaten wenn nötig
4. Resume Prompt generieren (kopierbarer Block: welche Files lesen, wo aufgehört, was als nächstes)
5. "Gespeichert! Kopier den Resume Prompt für nächstes Mal."

## /resume
Session-Start. Kontext aufnehmen.
Mit Resume Prompt: Alle genannten Files lesen, cross-referenzieren, Orientierung in eigenen Worten zeigen. Context % anzeigen.
Ohne Prompt: Core Files → Memory → Projekte scannen. Zeigen was gefunden wurde, fragen worauf fokussiert werden soll.

## /progress
Read-only Status-Snapshot. Keine Files ändern.
Zeigen: Was wurde gemacht, aktueller Stand, nächster Schritt, Context %.

## /idea {idee}
Quick Idea Capture.
1. Nach IDEAS.md (oder projekt-spezifisch)
2. Format: "## [Titel] (YYYY-MM-DD) [Die Idee]"
3. Bestätigung in einer Zeile.

## /task {beschreibung}
Quick Task Capture.
1. Nach TASKS.md mit Datum und Beschreibung
2. Bestätigung in einer Zeile.

## /meeting {context}
Meeting-Transkript verarbeiten.
1. meetings/YYYY-MM-DD-topic.md erstellen mit Zusammenfassung
2. Action Items, Key Decisions, Notable Quotes extrahieren
3. Volles Original-Transkript beibehalten (nie kürzen!)
4. meetings/INDEX.md updaten
5. Prüfen ob Meeting Auswirkungen auf andere Dateien hat (MEMORY.md, Projekte, knowledge/)

## /create {projekt} {context}
Neues Projekt anlegen.
1. projects/[name]/ Ordner erstellen
2. AGENT.md und ROADMAP.md mit Kontext füllen

## /projects
Alle Projekte mit Status auflisten.
1. projects/*/ROADMAP.md scannen
2. Status + aktuelle Phase zeigen
3. "🎯 Fokus heute: [Empfehlung]"

## /close {projekt}
Projekt archivieren.
1. ROADMAP.md als complete markieren, Final State dokumentieren
2. Ordner nach projects_archived/ verschieben

## /usermanual
Erklärt dem User das komplette System in einfacher Sprache.

## /mycommands
/save — Alles sichern + Resume Prompt
/resume — Kontext aufnehmen (oder sag einfach "weiter")
/progress — Status-Snapshot
/idea {idee} — Idee festhalten
/task {beschreibung} — Task festhalten
/meeting {context} — Meeting verarbeiten
/create {projekt} — Neues Projekt
/projects — Alle Projekte anzeigen
/close {projekt} — Projekt archivieren
/usermanual — System-Erklärung
/mycommands — Diese Liste
