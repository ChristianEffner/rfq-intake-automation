Ziel

Ein einfacher, konsequenter Arbeitsprozess, der Fokus hält, Fortschritt sichtbar macht und Qualität sicherstellt (ohne Overhead).

Board-Spalten

Backlog – Ideen/Tasks, noch nicht bereit

Next Up (Ready) – klar definierte Tasks, bereit zum Start

In Progress – gerade in Arbeit

Review / Test – fertig gebaut, wird geprüft

Done – abgeschlossen nach Definition of Done

Blocked / Parking Lot – hängt an Abhängigkeiten oder bewusst pausiert

WIP-Limits (Work in Progress)

In Progress: max. 2 Karten

Review / Test: max. 2 Karten

Regel: Nichts Neues starten, bevor „Review/Test“ leerer wird.

Karten-Template (Standard)

Titel: A1.2 JSON-Schema definieren
Beschreibung: 2–5 Sätze, was gebaut wird
Akzeptanzkriterien: 3–5 Bulletpoints (prüfbar)
Aufwand: S / M / L
Abhängigkeiten: Links oder Kartennummern
Labels: Scope + Type + Area + Risk

Labels (wie sie genutzt werden)

Scope: MVP / Nice-to-have

Type: Feature / Tech / Bug / Doku

Area: Data / Extraction / Validation / UI / Export / QA

Risk: High risk / Low

Regel: Jede Karte bekommt mindestens Scope + Type + Area.

Definition of Ready (DoR) – wann darf eine Karte in “Next Up”?

Eine Karte ist „Ready“, wenn:

Ziel ist klar (kein „irgendwas mit…“)

Akzeptanzkriterien sind vorhanden

Abhängigkeiten sind bekannt

Aufwand ist grob eingeschätzt (S/M/L)

Definition of Done (DoD) – wann ist eine Karte “Done”?

Eine Karte ist “Done”, wenn:

Ergebnis läuft lokal reproduzierbar (oder Doku ist vollständig)

Mindestens 1 Testfall oder manueller Check ist dokumentiert

Relevante Doku (README oder docs) ist aktualisiert

Beispiel-Input/Output ist vorhanden, wenn sinnvoll

Review-Regeln (Self-Review)

Bei Karten in Review/Test:

Einmal Diff anschauen (falls Code)

Kurz prüfen: erfüllt sie wirklich alle Akzeptanzkriterien?

Wenn es ein Feature ist: 1–2 „Happy path“ + 1 „Edge case“ testen

Danach erst nach Done

Commit-/PR-Regeln (GitHub, Browser)

Arbeiten bevorzugt in Feature-Branches (feature/<topic>)

Merge nach main via Pull Request (auch solo, als Review-Nachweis)

PR-Titel: EPIC X: <kurzer Nutzen>

main bleibt jederzeit demo-fähig

Blocked-Regel

Wenn eine Karte > 2 Tage blockiert ist:

Karte nach Blocked schieben

Kurz notieren: „Warum blockiert?“ + „Nächster Schritt“
