# RFQ Intake Automation (Private Portfolio Project)

## Project Goal
This project is a private portfolio project to build a lightweight tool that converts unstructured RFQ inputs (e.g., email text and attachment text) into structured, validated data.  
The tool extracts key RFQ fields (e.g., product/specification, quantity, requested delivery date, Incoterms) and outputs **JSON** following a defined schema.  
It also generates a simple task list for follow-up actions and flags uncertain/incomplete cases for human review.

## MVP Scope (Must-haves)
- Input: RFQ/email text + optional 0–3 attachment text files
- Output: **JSON-only** (strict schema)
- Core fields (minimum):
  - request_id
  - customer/company (if present)
  - product/product_group
  - specification (free text)
  - quantity (number + unit if possible)
  - requested_delivery_date (date or "unknown")
  - delivery_location (if present)
  - incoterms (if present)
  - deadline/response_due_date (if present)
  - clarification_questions (list)
- Validation: schema validation + basic plausibility checks (e.g., quantity > 0, dates not in the past)
- Review support: `needs_review` flag + list of missing/uncertain fields
- Task list: 3–7 standardized follow-up tasks based on missing fields
- Export: JSON per RFQ (+ optional CSV for “CRM import simulation”)
- Demo: 3 example RFQs (clean / incomplete / contradictory)

## Out of Scope (MVP)
- OCR for scanned PDFs/images
- Direct write-back to a real CRM (export files only)
- Fully automated “no review needed” processing
- Complex table extraction, drawings interpretation, advanced layout parsing
- Authentication/roles, multi-user, production deployment

## Assumptions
- RFQs are available as text or simulated as text for this project
- A portion of inputs is intentionally “dirty” (missing data, inconsistent formats)
- Focus is on robustness and traceability rather than 100% automation

## Documentation
- Detailed project scope: `docs/01_project_scope.md` (to be created)
