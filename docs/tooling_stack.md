Ziel

Ich definiere den minimalen Tech-Stack für den MVP, um später keine unnötigen Umbauten zu haben. Fokus: schnell lauffähig, gut testbar, portfolio-tauglich.

MVP Tech-Stack (festgelegt)
Sprache & Runtime

Python 3.11+

Begründung: sehr gut für Parsing, Datenverarbeitung, schnelle Prototypen.

Projektstruktur / Dependency Management

requirements.txt (MVP)

Begründung: minimaler Overhead, schnell startklar.

(Optional später) Wechsel auf pyproject.toml/Poetry, wenn das Projekt wächst.

Datenformate

Input: .txt Dateien (RFQ-Mailtext) + optionale Attachment-Textdateien

Output: JSON pro RFQ + optional CSV (CRM-Import-Simulation)

Begründung: JSON ist ideal für Schema/Validierung; CSV gut für einfache Exports/Demos.

Validation / Schema

pydantic

Begründung: klare Schemas, starke Validierung, gute Fehlermeldungen.

Tests

pytest

Begründung: Standard in Python, schnelle Unit-Tests + “golden files”.

UI (für später im Projekt A)

Streamlit (ab EPIC 4)

Begründung: schnell eine Review-UI bauen (links Input, rechts JSON).

Logging / Messung

einfache Logs als CSV/JSONL (lokal)

Felder: rfq_id, is_valid_json, needs_review, missing_fields_count, runtime_s, timestamp

Begründung: KPIs unkompliziert auswertbar.

Integrationen (bewusst nicht im MVP)

Kein echtes CRM API Writeback (nur Export-Dateien)

Keine Auth, kein Multi-User

Kein Cloud-Deployment

LLM-Provider (MVP-Entscheidung)

Provider wird im MVP austauschbar gehalten (Adapter/Interface), damit ich später wechseln kann, ohne die Pipeline umzubauen.

Im MVP reicht ein einfacher “Extractor”-Wrapper, der:

Input: mail_text, attachment_texts

Output: rfq_json (strict JSON) + optional confidence/missing_fields

Out of Scope (Tech)

OCR / PDF-Layout-Parsing im MVP

Vektor-Datenbank / RAG (gehört eher zu Projekt B)
