from __future__ import annotations
import argparse
import csv
import os
import random
from datetime import date, timedelta

ATTACHMENT_TYPES = ["spec", "addresses", "quality", "packaging"]

SPEC_SNIPPETS = [
    "Material: stainless steel AISI 316L\nProtection: IP67\nVoltage: 24V DC\nOperating temp: -10..+60°C",
    "Connector: M12\nOutput: PNP NO\nSupply: 10–30V DC\nHousing: nickel-plated brass",
    "Finish: powder-coated\nColor: RAL 7035\nBending tolerance: ±0.5mm\nSurface: free of sharp edges",
    "Gear ratio: 10:1\nMax torque: 50Nm\nBacklash: < 10 arcmin\nMounting: IEC standard",
]

QUALITY_SNIPPETS = [
    "Compliance: RoHS, REACH\nRequired documents: CoC (Certificate of Conformity)",
    "Quality requirement: ISO 9001 supplier\nIncoming inspection: AQL 1.0\nTraceability: batch number required",
    "Documentation: material certificate EN 10204 3.1\nPackaging must prevent corrosion during transport",
]

PACKAGING_SNIPPETS = [
    "Packaging: individual polybag + outer carton\nLabel: RFQ ID + Part No + Quantity",
    "Shipment: pallets only, max height 1.2m\nNo mixed parts per box",
    "Marking: laser-etched part number on each unit (if applicable)",
]

def random_future_date(rng: random.Random, min_days: int, max_days: int) -> str:
    d = date.today() + timedelta(days=rng.randint(min_days, max_days))
    return d.isoformat()

def make_attachment_text(rng: random.Random, rfq_id: str, att_type: str) -> str:
    if att_type == "spec":
        return f"""Attachment: Technical Specification ({rfq_id})

{rng.choice(SPEC_SNIPPETS)}

Notes:
- Please confirm lead time and availability.
- Include datasheet in your quotation.
"""
    if att_type == "addresses":
        return f"""Attachment: Delivery / Billing Information ({rfq_id})

Delivery Address:
Example Industries GmbH
Logistics Center
Musterstraße 12
{rng.choice(["10115 Berlin", "20095 Hamburg", "80331 München", "50667 Köln"])}

Requested delivery window: {random_future_date(rng, 20, 120)} to {random_future_date(rng, 121, 180)}

Billing Address:
Example Industries GmbH
Finance Dept.
Rechnungsweg 5
{rng.choice(["10115 Berlin", "20095 Hamburg", "80331 Hamburg", "70173 Stuttgart"])}
"""
    if att_type == "quality":
        return f"""Attachment: Quality & Compliance Requirements ({rfq_id})

{rng.choice(QUALITY_SNIPPETS)}

If deviations are required, please list them explicitly in your offer.
"""
    if att_type == "packaging":
        return f"""Attachment: Packaging & Labeling Requirements ({rfq_id})

{rng.choice(PACKAGING_SNIPPETS)}

Please confirm you can meet these packaging requirements.
"""
    raise ValueError("Unknown attachment type")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--min_rfqs", type=int, default=25, help="Minimum number of RFQs to attach files to.")
    parser.add_argument("--max_rfqs", type=int, default=40, help="Maximum number of RFQs to attach files to.")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    index_path = os.path.join("data_samples", "rfq_index.csv")
    if not os.path.exists(index_path):
        raise FileNotFoundError("data_samples/rfq_index.csv not found. Run A1.3 first.")

    # Read RFQs
    with open(index_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    rfq_ids = [r["rfq_id"] for r in rows]
    rng.shuffle(rfq_ids)

    n_targets = rng.randint(args.min_rfqs, min(args.max_rfqs, len(rfq_ids)))
    target_ids = set(rfq_ids[:n_targets])

    out_dir = os.path.join("data_samples", "attachments")
    os.makedirs(out_dir, exist_ok=True)

    # Create attachments
    attachments_map = {}  # rfq_id -> list of filenames
    for rfq_id in target_ids:
        n_atts = rng.randint(1, 3)
        types = rng.sample(ATTACHMENT_TYPES, k=n_atts)

        files = []
        for i, t in enumerate(types, start=1):
            filename = f"{rfq_id}_att_{i:02d}.txt"
            path = os.path.join(out_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(make_attachment_text(rng, rfq_id, t))
            files.append(filename)

        attachments_map[rfq_id] = files

    # Update rfq_index.csv with has_attachments = true if attachments exist
    for r in rows:
        if r["rfq_id"] in attachments_map:
            r["has_attachments"] = "True"

    with open(index_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["rfq_id", "category", "dirty_flags", "customer", "product", "has_attachments", "expected_needs_review"],
        )
        writer.writeheader()
        writer.writerows(rows)

    # Write attachments index
    attachments_index_path = os.path.join("data_samples", "attachments_index.csv")
    with open(attachments_index_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rfq_id", "attachment_files"])
        for rfq_id, files in sorted(attachments_map.items()):
            writer.writerow([rfq_id, ";".join(files)])

    print(f"Created attachments for {len(attachments_map)} RFQs in {out_dir}/")
    print(f"Wrote attachments index: {attachments_index_path}")
    print(f"Updated: {index_path} (has_attachments)")
    
if __name__ == "__main__":
    main()
