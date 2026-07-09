#!/usr/bin/env python3
"""
Generate DXF cutting templates for card sizes defined in assets/layouts.json
that are not present in SCM's layouts.json.

Outputs to cutting_templates/games/<card_size>/ mirroring SCM's naming conventions.

Usage:
    python generate.py               # generate missing templates
    python generate.py --all         # regenerate all
    python generate.py --card mtg    # single card size
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import click

SCRIPT_DIR = Path(__file__).parent
EXTRAS_LAYOUTS = SCRIPT_DIR / "assets" / "layouts.json"
OUTPUT_DIR = SCRIPT_DIR / "cutting_templates" / "games"

SCM_DIR = Path(__file__).parent.parent / "silhouette-card-maker"
SCM_LAYOUTS = SCM_DIR / "assets" / "layouts.json"
GENERATE_DXF = SCM_DIR / "generate_dxf.py"


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def extra_card_sizes(extras: dict, base: dict) -> list[str]:
    """Return card size names present in extras but not in base."""
    return [k for k in extras["card_sizes"] if k not in base["card_sizes"]]


def run_single(card_size: str, paper_size: str, variant: str, out_file: Path) -> bool:
    cmd = [
        sys.executable, str(GENERATE_DXF), "single", str(out_file),
        "--card_size", card_size,
        "--paper_size", paper_size,
        "--variant", variant,
        "--orientation", "optimize",
    ]
    result = subprocess.run(cmd, cwd=SCM_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        click.echo(result.stderr.strip(), err=True)
    return result.returncode == 0


@click.command()
@click.option("--card", "card_filter", default=None, help="Generate only this card size (e.g. mtg).")
@click.option("--all", "regenerate_all", is_flag=True, help="Regenerate files that already exist.")
def main(card_filter, regenerate_all):
    """Generate DXF templates for extra card sizes in assets/layouts.json."""
    if not GENERATE_DXF.exists():
        raise click.ClickException(f"generate_dxf.py not found at {GENERATE_DXF}")

    extras = load_json(EXTRAS_LAYOUTS)
    base = load_json(SCM_LAYOUTS)

    new_sizes = extra_card_sizes(extras, base)
    if not new_sizes:
        click.echo("No extra card sizes found in assets/layouts.json.")
        return

    if card_filter:
        if card_filter not in new_sizes:
            raise click.ClickException(f"'{card_filter}' is not an extra card size. Known: {new_sizes}")
        sizes_to_generate = [card_filter]
    else:
        sizes_to_generate = new_sizes

    # Temporarily swap layouts.json so SCM can resolve the new card sizes
    scm_backup = SCM_LAYOUTS.with_suffix(".json.bak")
    shutil.copy(SCM_LAYOUTS, scm_backup)
    shutil.copy(EXTRAS_LAYOUTS, SCM_LAYOUTS)

    try:
        paper_sizes = list(extras["paper_sizes"].keys())
        variants = ["default", "borderless"]

        for card_size in sizes_to_generate:
            click.echo(f"\n=== {card_size} ===")
            card_dir = OUTPUT_DIR / card_size
            card_dir.mkdir(parents=True, exist_ok=True)

            for paper in paper_sizes:
                for variant in variants:
                    variant_label = "" if variant == "default" else f"_{variant}"
                    filename = f"{card_size}{variant_label}_{paper}.dxf"
                    out_file = card_dir / filename

                    if out_file.exists() and not regenerate_all:
                        click.echo(f"  [skip] {filename}")
                        continue

                    ok = run_single(card_size, paper, variant, out_file)
                    click.echo(f"  {'[ok]  ' if ok else '[fail]'} {filename}")
    finally:
        shutil.copy(scm_backup, SCM_LAYOUTS)
        scm_backup.unlink()


if __name__ == "__main__":
    main()
