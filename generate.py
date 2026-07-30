#!/usr/bin/env python3
"""
Generate DXF cutting templates for extra card sizes defined in assets/layouts-extra.json.

Points SCM at this repo's assets/layouts-extra.json (SCM_EXTRA_LAYOUTS) and
cutting_templates/ (SCM_CUTTING_TEMPLATES_DIR) via env vars, then runs generate_dxf.py's
`single --save` once per missing paper/card/variant combination. `--save` persists
the computed layout (orientation, rows/cols, registration) back into
layouts-extra.json, so later runs and dxf_to_studio3.py can look it up.

Usage:
    python generate.py               # generate missing templates
    python generate.py --all         # regenerate all

Once DXFs exist, run (from silhouette-card-maker, with the same two env vars set):
    python dxf_to_studio3.py batch --unit mm
to produce the matching .studio3 files.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import click

SCRIPT_DIR = Path(__file__).parent
EXTRA_LAYOUTS = SCRIPT_DIR / "assets" / "layouts-extra.json"
OUTPUT_DIR = SCRIPT_DIR / "cutting_templates"

SCM_DIR = Path(__file__).parent.parent / "silhouette-card-maker"
GENERATE_DXF = SCM_DIR / "generate_dxf.py"

PAPER_SIZES = ["letter", "a4", "tabloid", "a3", "arch_b"]
VARIANTS = ["default", "borderless"]


def scm_env() -> dict:
    env = os.environ.copy()
    env["SCM_EXTRA_LAYOUTS"] = str(EXTRA_LAYOUTS.resolve())
    env["SCM_CUTTING_TEMPLATES_DIR"] = str(OUTPUT_DIR.resolve())
    return env


def load_extra() -> dict:
    with open(EXTRA_LAYOUTS) as f:
        return json.load(f)


def template_name(paper_size: str, card_size: str, variant: str, version: int) -> str:
    if variant == "default":
        return f"{paper_size}-{card_size}-v{version}"
    return f"{paper_size}-{card_size}-{variant}-v{version}"


@click.command()
@click.option("--all", "regenerate_all", is_flag=True, help="Regenerate files that already exist.")
def main(regenerate_all):
    """Generate DXF templates for extra card sizes via SCM."""
    if not GENERATE_DXF.exists():
        raise click.ClickException(f"generate_dxf.py not found at {GENERATE_DXF}")

    extra = load_extra()
    card_sizes = list(extra.get("card_sizes", {}).keys())
    if not card_sizes:
        click.echo("No extra card sizes found.")
        return

    click.echo(f"Extra card sizes: {', '.join(card_sizes)}")

    env = scm_env()

    for card_size in card_sizes:
        click.echo(f"\n=== {card_size} ===")

        for paper in PAPER_SIZES:
            for variant in VARIANTS:
                layouts = extra.get("layouts", {})
                existing = layouts.get(paper, {}).get(card_size, {}).get(variant)

                if existing and not regenerate_all:
                    click.echo(f"  [skip] {paper} + {card_size} ({variant})")
                    continue

                version = existing["version"] if existing else 1
                name = template_name(paper, card_size, variant, version)
                variant_dir = "borderless/dxf" if variant == "borderless" else "dxf"
                out_file = OUTPUT_DIR / variant_dir / f"{name}.dxf"

                cmd = [
                    sys.executable, str(GENERATE_DXF), "single", str(out_file),
                    "--card_size", card_size,
                    "--paper_size", paper,
                    "--variant", variant,
                    "--orientation", "optimize",
                    "--save",
                ]
                result = subprocess.run(cmd, cwd=SCM_DIR, capture_output=True, text=True, env=env)
                if result.returncode == 0:
                    click.echo(f"  [ok]   {name}.dxf")
                    # single --save updated layouts-extra.json; reload so later
                    # combinations in this loop see the up-to-date layouts.
                    extra = load_extra()
                else:
                    click.echo(f"  [fail] {name}.dxf")
                    click.echo(result.stderr.strip(), err=True)


if __name__ == "__main__":
    main()
