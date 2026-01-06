from __future__ import annotations

import argparse
import csv
import os
import random
from datetime import date, timedelta

CUSTOMERS = [
    "NordTech GmbH", "Alpha Industrial AG", "MechaWorks Europe", "Rheinmetall Components (Demo)",
    "Bergmann Maschinenbau", "Hanseatic Automation", "EuroFab Industries", "Kappa Process Solutions",
]

PRODUCTS = [
    ("Pneumatic valve", "Stainless steel, IP67, 24V DC"),
    ("Inductive sensor", "M12, PNP NO, 10–30V, sensing distance 4mm"),
    ("Ball bearing", "Deep groove, 6205-2RS, grease-filled"),
    ("Servo motor", "400W, 230VAC, encoder 17-bit, with brake"),
    ("PLC module", "DI/DO module, 24V, compatible with common PLC systems"),
    ("Cable harness", "Custom harness, 2m length, connectors per drawing"),
    ("Sheet metal part", "Laser cut + bend, powder-coated, per drawing"),
    ("Gearbox", "Planetary gearbox, ratio 10:1, max torque 50Nm"),
]

INCOTERMS = ["EXW", "FCA", "DAP", "DDP"]
LOCATIONS = ["Berlin, DE", "Hamburg, DE", "München, DE", "Köln, DE", "Leipzig, DE", "Stuttgart, DE"]

def iso(d: date) -> str:
    return d.isoformat()

def random_future_date(rng: random.Random, min_days: int = 7, max_days: int = 120) -> str:
    d = date.today() + timedelta(days=rng.randint(min_days, max_days))
    return iso(d)

def make_clean_email(rng: random.Random, rfq_id: str) -> dict:
    customer = rng.choice(CUSTOMERS)
    product, base_spec = rng.choice(PRODUCTS)
    qty = rng.choice([50, 100, 200, 500, 1000, 2500])
    unit = rng.choice(["pcs", "units"])
    incoterm = rng.choice(INCOTERMS)
    loc = rng.choice(LOCATIONS)
    deliv = random_future_date(rng, 14, 140)
    due = random_future_date(rng, 3, 21)

    body = f"""Subject: RFQ {rfq_id} – {product}

Hello Sales Team,

we would like to request a quotation for the following item:

- Product/Service: {product}
- Specification: {base_spec}; please include datasheet and lead time.
- Quantity: {qty} {unit}
- Requested delivery date: {deliv}
- Delivery location: {loc}
- Incoterms: {incoterm}
- Response due date: {due}

Please confirm availability and provide pricing incl. delivery.

Best regards
Procurement
{customer}
"""
    return {
        "rfq_id": rfq_id,
        "category": "clean",
        "dirty_flags": "",
        "customer": customer,
        "product": product,
        "has_attachments": rng.random() < 0.35,   # used later for A1.4
        "expected_needs_review": False,
        "text": body,
    }

def make_incomplete_email(rng: random.Random, rfq_id: str) -> dict:
    customer = rng.choice(CUSTOMERS)
    product, base_spec = rng.choice(PRODUCTS)

    missing = rng.choice(["delivery_date", "quantity", "incoterms", "due_date"])
    loc = rng.choice(LOCATIONS)
    incoterm = rng.choice(INCOTERMS)
    qty = rng.choice([100, 500, 1000])
    unit = rng.choice(["pcs", "units"])

    lines = [
        f"Subject: RFQ {rfq_id} – {product}",
        "",
        "Hello,",
        "",
        "please send us a quotation for:",
        f"- Product/Service: {product}",
        f"- Specification: {base_spec}",
    ]

    if missing != "quantity":
        lines.append(f"- Quantity: {qty} {unit}")
    else:
        lines.append("- Quantity: (not specified yet)")

    if missing != "delivery_date":
        lines.append(f"- Requested delivery date: {random_future_date(rng, 10, 120)}")
    else:
        lines.append("- Requested delivery date: ASAP / to be confirmed")

    lines.append(f"- Delivery location: {loc}")

    if missing != "incoterms":
        lines.append(f"- Incoterms: {incoterm}")
    else:
        lines.append("- Incoterms: (not specified)")

    if missing != "due_date":
        lines.append(f"- Response due date: {random_future_date(rng, 2, 14)}")
    else:
        lines.append("- Response due date: (no deadline mentioned)")

    lines += [
        "",
        "If you need additional details, please let us know.",
        "",
        f"Best regards\n{customer}\nPurchasing"
    ]

    return {
        "rfq_id": rfq_id,
        "category": "incomplete",
        "dirty_flags": missing,
        "customer": customer,
        "product": product,
        "has_attachments": rng.random() < 0.45,
        "expected_needs_review": True,
        "text": "\n".join(lines),
    }

def make_contradictory_email(rng: random.Random, rfq_id: str) -> dict:
    customer = rng.choice(CUSTOMERS)
    product, base_spec = rng.choice(PRODUCTS)
    loc = rng.choice(LOCATIONS)
    incoterm = rng.choice(INCOTERMS)

    contradiction = rng.choice(["two_quantities", "two_dates"])
    if contradiction == "two_quantities":
        qty1 = rng.choice([100, 500, 1000])
        qty2 = rng.choice([200, 750, 1500])
        deliv = random_future_date(rng, 14, 120)
        body = f"""Subject: RFQ {rfq_id} – {product}

Hello,

please quote the following:

- Product/Service: {product}
- Specification: {base_spec}
- Quantity: {qty1} pcs (please also provide pricing for {qty2} pcs)
- Requested delivery date: {deliv}
- Delivery location: {loc}
- Incoterms: {incoterm}

We need a quick response.

Regards
{customer}
"""
        flags = "two_quantities"
    else:
        qty = rng.choice([100, 500, 1000])
        d1 = random_future_date(rng, 14, 60)
        d2 = random_future_date(rng, 61, 140)
        body = f"""Subject: RFQ {rfq_id} – {product}

Hi,

requesting a quotation:

- Product/Service: {product}
- Specification: {base_spec}
- Quantity: {qty} pcs
- Requested delivery date: {d1} (alternatively {d2} depending on availability)
- Delivery location: {loc}
- Incoterms: {incoterm}

Please confirm which delivery date you can meet.

Thanks
{customer}
"""
        flags = "two_dates"

    return {
        "rfq_id": rfq_id,
        "category": "contradictory",
        "dirty_flags": flags,
        "customer": customer,
        "product": product,
        "has_attachments": rng.random() < 0.55,
        "expected_needs_review": True,
        "text": body,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=80, help="Number of RFQs to generate (50–100 recommended).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    n = args.n

    # Distribution: 60% clean, 30% incomplete, 10% contradictory
    n_clean = int(n * 0.60)
    n_incomplete = int(n * 0.30)
    n_contra = n - n_clean - n_incomplete

    rows = []
    out_dir = os.path.join("data_samples", "raw")
    os.makedirs(out_dir, exist_ok=True)

    def rfq_name(i: int) -> str:
        return f"RFQ_{i:04d}"

    i = 1
    for _ in range(n_clean):
        rid = rfq_name(i)
        rows.append(make_clean_email(rng, rid))
        i += 1
    for _ in range(n_incomplete):
        rid = rfq_name(i)
        rows.append(make_incomplete_email(rng, rid))
        i += 1
    for _ in range(n_contra):
        rid = rfq_name(i)
        rows.append(make_contradictory_email(rng, rid))
        i += 1

    # Shuffle so the dataset isn't grouped by category
    rng.shuffle(rows)

    # Write files
    for r in rows:
        path = os.path.join(out_dir, f"{r['rfq_id']}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(r["text"])

    # Write index CSV
    index_path = os.path.join("data_samples", "rfq_index.csv")
    os.makedirs("data_samples", exist_ok=True)

    with open(index_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["rfq_id", "category", "dirty_flags", "customer", "product", "has_attachments", "expected_needs_review"],
        )
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "rfq_id": r["rfq_id"],
                "category": r["category"],
                "dirty_flags": r["dirty_flags"],
                "customer": r["customer"],
                "product": r["product"],
                "has_attachments": r["has_attachments"],
                "expected_needs_review": r["expected_needs_review"],
            })

    print(f"Generated {len(rows)} RFQs:")
    print(f"- Raw texts: {out_dir}/RFQ_XXXX.txt")
    print(f"- Index: {index_path}")

if __name__ == "__main__":
    main()
