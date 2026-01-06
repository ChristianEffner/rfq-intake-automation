# RFQ Data Model (Project A) — Field List (MVP + Optional)

This document defines the RFQ fields that the system should extract from unstructured inputs (email text + optional attachment text).  
It separates **MVP fields** (required for the first working version) from **optional fields** (nice-to-have for later iterations).

---

## Conventions

- **Date format:** `YYYY-MM-DD` (ISO). If not present/unknown: use `"unknown"`.
- **Quantity:** store numeric value and unit in **separate fields** (`quantity`, `quantity_unit`) for robustness.
- **Lists:** use arrays for multi-values (`missing_fields`, `clarification_questions`, `tasks`).
- **Strings:** keep original wording where helpful (e.g., `specification`).

---

## MVP Fields

| Field | Type | Required (MVP) | Description | Example |
|------|------|-----------------|------------|---------|
| `request_id` | string | ✅ | Unique RFQ identifier (generated or from filename). | `"RFQ_0001"` |
| `customer_name` | string | ❌ | Company/customer name if present. | `"ACME GmbH"` |
| `contact_name` | string | ❌ | Contact person if present. | `"Max Mustermann"` |
| `contact_email` | string | ❌ | Contact email if present. | `"max@acme.com"` |
| `product_or_service` | string | ✅ | What is requested (product/service). | `"Pneumatic valve"` |
| `specification` | string | ✅ | Technical/commercial requirements (free text). | `"Stainless steel, IP67, 24V DC..."` |
| `quantity` | number | ❌ | Numeric quantity if present. | `1000` |
| `quantity_unit` | string | ❌ | Unit for quantity if present. | `"pcs"` |
| `requested_delivery_date` | string (date or `"unknown"`) | ✅ | Requested delivery date or `"unknown"`. | `"2026-03-15"` |
| `delivery_location` | string | ❌ | Delivery location if present. | `"Berlin, DE"` |
| `incoterms` | string | ❌ | Incoterms if present. | `"DAP"` |
| `response_due_date` | string (date or `"unknown"`) | ✅ | Deadline/response due date or `"unknown"`. | `"2026-01-31"` |
| `needs_review` | boolean | ✅ | True if missing/uncertain critical fields or low confidence. | `true` |
| `missing_fields` | list[string] | ✅ | List of missing/uncertain fields (field names). | `["requested_delivery_date"]` |
| `clarification_questions` | list[string] | ✅ | Questions to clarify missing/ambiguous information. | `["What is the requested delivery date?"]` |
| `tasks` | list[string] | ✅ | Follow-up tasks generated from the RFQ. | `["Check delivery feasibility", "Prepare quotation"]` |

---

## Optional Fields (Nice-to-have)

| Field | Type | Description | Example |
|------|------|-------------|---------|
| `target_price` | number | Target price/budget if mentioned. | `25000` |
| `currency` | string | Currency code or symbol. | `"EUR"` |
| `priority` | string (`low`/`medium`/`high`) | Priority if derivable. | `"high"` |
| `attachments_present` | boolean | Whether attachments exist (based on input). | `true` |
| `certifications_required` | list[string] | Required certifications/compliance. | `["RoHS", "REACH"]` |
| `material` | string | Material requirement if mentioned. | `"Aluminium"` |
| `tolerance` | string | Tolerances if mentioned. | `"±0.02 mm"` |
| `notes` | string | Additional notes or extracted context. | `"Customer requests express delivery."` |

---

## Notes for Implementation (next steps)

- These fields will be implemented as a **pydantic schema** in Task **A1.2**.
- `needs_review` should generally be `true` if:
  - a required field is `"unknown"` (e.g., delivery date / response due date), or
  - contradictions exist (e.g., two different quantities), or
  - extraction confidence is low (if confidence scoring is implemented).
