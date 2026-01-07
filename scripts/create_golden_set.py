from __future__ import annotations
import argparse
import csv
import os
import random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--clean", type=int, default=6)
    parser.add_argument("--incomplete", type=int, default=3)
    parser.add_argument("--contradictory", type=int, default=1)
    args = parser.parse_args()

    rng = random.Random(args.seed)

    index_path = os.path.join("data_samples", "rfq_index.csv")
    if not os.path.exists(index_path):
        raise FileNotFoundError("data_samples/rfq_index.csv not found. Run A1.3 first.")

    with open(index_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_cat = {"clean": [], "incomplete": [], "contradictory": []}
    for r in rows:
        by_cat[r["category"]].append(r)

    def pick(cat: str, n: int):
        if len(by_cat[cat]) < n:
            raise ValueError(f"Not enough RFQs in category '{cat}'.")
        rng.shuffle(by_cat[cat])
        return by_cat[cat][:n]

    selected = pick("clean", args.clean) + pick("incomplete", args.incomplete) + pick("contradictory", args.contradictory)
    rng.shuffle(selected)

    out_dir = os.path.join("data_samples", "expected")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "golden_set.csv")

    # Minimal expectations:
    # - clean: should_needs_review False
    # - incomplete/contradictory: should_needs_review True
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rfq_id", "category", "should_needs_review", "expected_missing_fields"])
        for r in selected:
            should_review = "True" if r["category"] != "clean" else "False"
            # We don't yet have a deterministic missing_fields list (that will come after extraction).
            writer.writerow([r["rfq_id"], r["category"], should_review, ""])

    print(f"Golden set written to: {out_path}")
    print("Selected RFQs:")
    for r in selected:
        print(f"- {r['rfq_id']} ({r['category']})")

if __name__ == "__main__":
    main()
