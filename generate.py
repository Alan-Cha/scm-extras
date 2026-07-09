#!/usr/bin/env python3
"""
Generate DXF cutting templates for all packs in scm-extras.

Discovers packs under packs/ by finding pack.json files, then calls
generate_dxf.py single for each paper × variant combination.

Usage:
    python generate.py                        # Generate all packs
    python generate.py --pack games/magic_the_gathering
    python generate.py --pack games/magic_the_gathering --all
"""

import json
import subprocess
import sys
from pathlib import Path

import click

SCRIPT_DIR = Path(__file__).parent
PACKS_DIR = SCRIPT_DIR / "packs"

SCM_DIR = Path(__file__).parent.parent / "silhouette-card-maker"
GENERATE_DXF = SCM_DIR / "generate_dxf.py"


def load_pack(pack_path: Path) -> dict:
    with open(pack_path / "pack.json") as f:
        return json.load(f)


def discover_packs() -> list[Path]:
    return sorted(p.parent for p in PACKS_DIR.rglob("pack.json"))


def output_dir(pack_path: Path) -> Path:
    return pack_path / "dxf"


def generate_pack(pack_path: Path, regenerate_all: bool):
    pack = load_pack(pack_path)
    name = pack["name"]
    card = pack["card_size"]
    paper_sizes = pack["paper_sizes"]
    variants = pack.get("variants", ["default"])

    out_dir = output_dir(pack_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    click.echo(f"\n=== {name} ===")

    for paper in paper_sizes:
        for variant in variants:
            variant_label = "" if variant == "default" else f"_{variant}"
            filename = f"{pack_path.name}{variant_label}_{paper}.dxf"
            out_file = out_dir / filename

            if out_file.exists() and not regenerate_all:
                click.echo(f"  [skip] {filename}")
                continue

            cmd = [
                sys.executable, str(GENERATE_DXF), "single", str(out_file),
                "--card_width", card["width"],
                "--card_height", card["height"],
                "--card_radius", card["radius"],
                "--paper_size", paper,
                "--variant", variant,
                "--orientation", "optimize",
            ]

            result = subprocess.run(cmd, cwd=SCM_DIR, capture_output=True, text=True)
            if result.returncode == 0:
                click.echo(f"  [ok]   {filename}")
            else:
                click.echo(f"  [fail] {filename}")
                click.echo(result.stderr.strip(), err=True)


@click.command()
@click.option("--pack", "pack_filter", default=None, help="Relative path to a single pack (e.g. games/magic_the_gathering).")
@click.option("--all", "regenerate_all", is_flag=True, help="Regenerate existing files instead of skipping them.")
def main(pack_filter, regenerate_all):
    """Generate DXF templates for all packs."""
    if not GENERATE_DXF.exists():
        raise click.ClickException(f"generate_dxf.py not found at {GENERATE_DXF}. Set SCM_DIR in generate.py.")

    if pack_filter:
        pack_path = PACKS_DIR / pack_filter
        if not (pack_path / "pack.json").exists():
            raise click.ClickException(f"No pack.json found at {pack_path}")
        packs = [pack_path]
    else:
        packs = discover_packs()
        if not packs:
            raise click.ClickException(f"No packs found under {PACKS_DIR}")

    for pack_path in packs:
        generate_pack(pack_path, regenerate_all)


if __name__ == "__main__":
    main()
