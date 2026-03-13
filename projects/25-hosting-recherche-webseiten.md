# Hosting-Recherche: Webseiten & Landingpages
_Nachtschicht #5, 13.03.2026_

## Ausgangssituation

- Aktuell: dogado Shared Hosting (6 Domains)
- Stefan will: Pia baut die Seiten selbst
- MailerLite bleibt (für E-Mail + Formulare)
- Hetzner-Server existiert bereits (OpenClaw/Pia)

**Kernfrage:** Wo hosten wir die Webseiten/Landingpages für Löwenstark + #kinderleicht?

---

## Option 1: dogado Shared Hosting (Status Quo)

**Was wir haben:**
- 6 Domains angelegt (diestarkmacher.de, susannehuettner.de, etc.)
- SFTP-Zugang, PHP, MySQL
- Preis: ~5-10€/Monat (Shared Hosting)

**Pro:**
- ✅ Bereits eingerichtet und bezahlt
- ✅ Stefan kennt es
- ✅ Domains + SSL + E-Mail alles an einem Ort
- ✅ Pia hat SFTP-Zugang

**Contra:**
- ⚠️ Shared Hosting = potenziell langsam
- ⚠️ Kein modernes Deployment (kein Git, kein CI/CD)
- ⚠️ PHP/WordPress = Wartungsaufwand (Updates, Sicherheit, Plugins)
- ⚠️ Wenn Pia Seiten baut: HTML/CSS direkt oder WordPress?

**Empfehlung:** Für bestehende WordPress-Seiten weiter nutzen. Neue Landingpages woanders.

---

## Option 2: Hetzner Cloud (eigener Server)

**Was wir haben:**
- Hetzner VPS (OpenClaw läuft darauf)
- Root-Zugang, volle Kontrolle

**Pro:**
- ✅ Bereits vorhanden, keine Extrakosten
- ✅ Volle Kontrolle über alles
- ✅ Pia kann direkt deployen (SSH/SFTP)
- ✅ Schnell (dedicated resources)

**Contra:**
- ❌ Sicherheitsrisiko: Webserver + OpenClaw auf gleichem Server
- ❌ Wartungsaufwand: Nginx, SSL-Zertifikate, Firewall
- ❌ Stefan ist kein Server-Experte
- ❌ Firewall aktuell nur Port 2222 + ICMP offen → Port 80/443 müsste freigeschaltet werden

**Empfehlung:** NICHT auf dem gleichen Server wie OpenClaw. Wenn Hetzner, dann separater Server.

---

## Option 3: Hetzner Cloud + Coolify (Self-Hosted PaaS)

**Was ist Coolify?** Open-Source Alternative zu Vercel/Netlify. Self-hosted auf eigenem Server.

**Setup:**
- Neuer Hetzner VPS (CX22, 2 vCPU, 4GB RAM) = 5,39€/Monat
- Coolify installieren (1-Click)
- Domains auf den neuen Server zeigen

**Pro:**
- ✅ Sehr günstig (5,39€/Monat für alles)
- ✅ Modernes Deployment (Git-Push → automatisch live)
- ✅ Let's Encrypt SSL automatisch
- ✅ Docker-basiert → alles möglich
- ✅ Open Source, aktive Community
- ✅ Dashboard für Stefan (wenn er mal reinschauen will)

**Contra:**
- ⚠️ Initialer Setup-Aufwand (1-2 Stunden)
- ⚠️ Server-Wartung (Updates, Monitoring)
- ⚠️ Wenn Server ausfällt = Seiten offline (kein CDN)

**Empfehlung:** Gute Option wenn wir volle Kontrolle wollen. Pia kann Coolify verwalten.

---

## Option 4: Vercel (Empfehlung für Landingpages)

**Was ist Vercel?** Die führende Plattform für moderne Webseiten. Next.js, aber auch statisches HTML.

**Pro:**
- ✅ **Kostenlos** für Hobby-Projekte (ausreichend!)
- ✅ Blitzschnell (Global CDN, Edge Network)
- ✅ Automatisches SSL
- ✅ Git-Push = Live in 10 Sekunden
- ✅ Custom Domains (beliebig viele)
- ✅ Pia kann direkt HTML/CSS/JS deployen
- ✅ Analytics eingebaut
- ✅ Kein Wartungsaufwand

**Contra:**
- ⚠️ Free Plan: 100GB Bandwidth/Monat (mehr als genug)
- ⚠️ Kein PHP (kein WordPress)
- ⚠️ Für komplexe Backend-Logik: Pro Plan 20$/Monat

**Kosten:**
- Free Plan: 0€ (Hobby, 1 Nutzer)
- Pro Plan: 20$/Monat (Team, Analytics, mehr Bandwidth)

**Empfehlung:** ⭐ **BESTE OPTION für neue Landingpages.** Kostenlos, schnell, kein Wartungsaufwand.

---

## Option 5: Netlify (Alternative zu Vercel)

Quasi identisch zu Vercel, etwas andere UI.

**Pro:**
- ✅ Kostenlos (300 Min Build/Monat, 100GB Bandwidth)
- ✅ Forms eingebaut (ohne Backend!)
- ✅ Netlify Identity (einfache Auth)
- ✅ Split Testing (A/B) eingebaut
- ✅ CMS (Netlify CMS) für nicht-technische Nutzer

**Contra:**
- ⚠️ Build-Minuten limitiert auf Free Plan
- ⚠️ Etwas weniger Performance als Vercel

**Empfehlung:** Gute Alternative, besonders wenn wir die eingebauten Forms nutzen wollen.

---

## Option 6: Carrd (für schnelle Landingpages)

**Was ist Carrd?** Einfacher Landingpage-Builder. Keine Programmierung nötig.

**Pro:**
- ✅ Extrem einfach (Drag & Drop)
- ✅ 19$/Jahr (!) für Pro Plus (beliebig viele Seiten)
- ✅ Custom Domains
- ✅ MailerLite-Integration
- ✅ Schnell: Landingpage in 30 Minuten
- ✅ Mobile-optimiert automatisch

**Contra:**
- ❌ Nur 1-Seiten-Layouts (keine Multi-Page-Sites)
- ❌ Begrenzte Design-Möglichkeiten
- ❌ Nicht für komplette Websites geeignet

**Empfehlung:** Ideal für einzelne Landingpages (Hackpack-Opt-in, Webinar-Anmeldung). Nicht für Hauptseiten.

---

## Option 7: MailerLite Landingpages (bereits verfügbar!)

**Was wir haben:** MailerLite Account (2× — Kinderleicht + Starkmacher)

**Pro:**
- ✅ **Bereits im Abo enthalten** (0€ extra!)
- ✅ Landing Pages + Opt-in-Formulare in einem Tool
- ✅ Drag & Drop Builder
- ✅ Custom Domains möglich
- ✅ A/B Testing
- ✅ Perfekte Integration mit E-Mail-Sequenzen

**Contra:**
- ⚠️ Design etwas limitiert (Templates-basiert)
- ⚠️ Nicht für komplette Websites
- ⚠️ MailerLite-Branding auf Free Plan

**Empfehlung:** Für Opt-in-Landingpages SOFORT nutzen! Kein Extra-Tool nötig.

---

## Empfehlung: Die Hybrid-Strategie

### Sofort (März 2026):
- **MailerLite Landingpages** für Opt-in-Seiten (Hackpack, Wuttypen-Test)
  - Kein Extra-Setup, sofort nutzbar
  - Perfekte Funnel-Integration

### Kurzfristig (April-Mai 2026):
- **Vercel (Free Plan)** für neue Landingpages (Webinar, Membership)
  - Pia baut HTML/CSS/JS direkt
  - Custom Domain z.B. kinderleicht.susannehuettner.de
  - Git-Repository → Push = Live

### Mittelfristig (ab Q3 2026):
- **dogado weiter** für bestehende WordPress-Seiten
  - diestarkmacher.de (existierende Seite pflegen)
  - susannehuettner.de (falls WordPress bleibt)
  
- **Vercel** für alle neuen Seiten
  - Moderne, schnelle Landingpages
  - Membership-Vorstellung
  - Webinar-Seiten

### Langfristig (2027):
- **Migration** der WordPress-Seiten auf statische Seiten (Vercel)
  - Weniger Wartung, schneller, sicherer
  - Oder: Headless CMS (Notion als CMS → Vercel rendert)

---

## Kostenvergleich (monatlich)

| Option | Kosten | Für |
|--------|--------|-----|
| dogado (Status Quo) | ~8€ | WordPress-Seiten |
| MailerLite LP | 0€ (im Abo) | Opt-in-Seiten |
| Vercel Free | 0€ | Neue Landingpages |
| **Gesamt** | **~8€/Monat** | **Alles abgedeckt** |

vs. Alternativen:
| Alternative | Kosten |
|------------|--------|
| Squarespace | 16€/Monat pro Seite |
| Wix | 12-36€/Monat |
| WordPress + WP Engine | 25€/Monat |
| Webflow | 14-39$/Monat |

**Ersparnis durch Hybrid-Ansatz: ~20-50€/Monat**

---

## Wie Pia Seiten baut

### Werkzeuge:
- **HTML/CSS/JS** direkt (Pia kann Code schreiben)
- **Tailwind CSS** für schnelles, responsives Design
- **Vercel** für Hosting + Deployment
- **#kinderleicht-Farbpalette** (Projekt 18)
- **Marken-Assets** (assets/marken/)

### Workflow:
1. Pia erstellt HTML/CSS im Workspace
2. Git Push → Vercel deployt automatisch
3. Stefan/Susanne reviewen
4. Domain verknüpfen → Live

### Was Pia direkt bauen kann:
- Landingpages (Opt-in, Webinar, Membership)
- Angebotsseiten (Löwenstark Kurse)
- "Über uns"-Seiten
- Blog (mit Markdown → HTML Rendering)
- Webinar-Replay-Seiten

---

## Nächste Schritte

1. ⬜ **Sofort:** MailerLite Landingpage für Hackpack-Opt-in erstellen
2. ⬜ **Diese Woche:** Vercel Account einrichten (kostenlos, mit GitHub)
3. ⬜ **April:** Erste Landingpage auf Vercel (Webinar oder Wuttypen-Test)
4. ⬜ **Entscheidung:** dogado WordPress-Seiten behalten oder mittelfristig migrieren?

---

_Kern-Empfehlung: MailerLite (Opt-in) + Vercel (Landingpages) + dogado (bestehende Seiten) = alles abgedeckt für ~8€/Monat. Pia baut die Seiten, kein WordPress-Wartungsstress. 13.03.2026_
