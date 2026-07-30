#!/usr/bin/env python3
"""
Generate markdown tables for the extra card sizes in assets/layouts_extra.json,
in the same format as SCM's own generate_readme_tables.py (whose format_number()
and load_layout_config() this script reuses directly).

Usage:
    python generate_readme_tables.py
"""

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
EXTRA_LAYOUTS = SCRIPT_DIR / "assets" / "layouts_extra.json"
SCM_DIR = Path(__file__).parent.parent / "silhouette-card-maker"

os.environ["SCM_EXTRA_LAYOUTS"] = str(EXTRA_LAYOUTS.resolve())
sys.path.insert(0, str(SCM_DIR))

import size_convert
from utilities import load_layout_config
from generate_readme_tables import format_number

PAPER_ORDER = ["letter", "tabloid", "a4", "a3", "arch_b"]


def extra_card_names() -> list[str]:
    with open(EXTRA_LAYOUTS) as f:
        return list(json.load(f).get("card_sizes", {}).keys())


def generate_tables():
    config = load_layout_config()
    cards = extra_card_names()

    # Table 1: paper x card grid (default layout)
    print("| Format |", " | ".join(f"`{p}`" for p in PAPER_ORDER), "|")
    print("|---|" + "---|" * len(PAPER_ORDER))

    for card in cards:
        cells = []
        for paper in PAPER_ORDER:
            layout = config.layouts.get(paper, {}).get(card, {}).get("default")
            if layout:
                cells.append(f"{layout.num_cols}x{layout.num_rows} ({layout.num_cols * layout.num_rows})")
            else:
                cells.append("❌")
        print(f"| `{card}` | {' | '.join(cells)} |")

    print()

    # Table 2: card sizes
    print("| Card size | Inches | Millimeters | Aspect Ratio | Notes |")
    print("| --- | --- | --- | --- | --- |")

    for card in cards:
        info = config.card_sizes[card]

        w_in = size_convert.size_to_in(info.width)
        h_in = size_convert.size_to_in(info.height)
        w_mm = size_convert.size_to_mm(info.width)
        h_mm = size_convert.size_to_mm(info.height)

        in_str = f"{format_number(min(w_in, h_in))} x {format_number(max(w_in, h_in))}"
        mm_str = f"{format_number(min(w_mm, h_mm))} x {format_number(max(w_mm, h_mm))}"

        if info.width.endswith("in"):
            in_str = f"**{in_str}**"
        else:
            mm_str = f"**{mm_str}**"

        aspect = min(w_mm, h_mm) / max(w_mm, h_mm)
        notes = "<br>".join(f"AKA `{a}`" for a in (info.aliases or []))

        print(f"| `{card}` | {in_str} | {mm_str} | {aspect:.4f} | {notes} |")


if __name__ == "__main__":
    generate_tables()
