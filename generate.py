#!/usr/bin/env python3
"""
Generate DXF cutting templates for extra card sizes defined in assets/layouts-extra.json.

Symlinks layouts-extra.json into SCM's assets/ directory so SCM picks it up
automatically, then runs generate_dxf.py batch for only the extra card sizes.

Usage:
    python generate.py               # generate missing templates
    python generate.py --all         # regenerate all
"""

import json
import subprocess
import sys
from pathlib import Path

import click

SCRIPT_DIR = Path(__file__).parent
EXTRA_LAYOUTS = SCRIPT_DIR / "assets" / "layouts-extra.json"

SCM_DIR = Path(__file__).parent.parent / "silhouette-card-maker"
SCM_EXTRA_LAYOUTS = SCM_DIR / "assets" / "layouts-extra.json"
GENERATE_DXF = SCM_DIR / "generate_dxf.py"


def ensure_symlink():
    if SCM_EXTRA_LAYOUTS.is_symlink():
        if SCM_EXTRA_LAYOUTS.resolve() == EXTRA_LAYOUTS.resolve():
            return
        SCM_EXTRA_LAYOUTS.unlink()
    elif SCM_EXTRA_LAYOUTS.exists():
        raise click.ClickException(
            f"{SCM_EXTRA_LAYOUTS} exists and is not a symlink. Remove it manually."
        )
    SCM_EXTRA_LAYOUTS.symlink_to(EXTRA_LAYOUTS.resolve())
    click.echo(f"Linked {SCM_EXTRA_LAYOUTS} -> {EXTRA_LAYOUTS.resolve()}")


def extra_card_sizes() -> list[str]:
    with open(EXTRA_LAYOUTS) as f:
        return list(json.load(f).get("card_sizes", {}).keys())


@click.command()
@click.option("--all", "regenerate_all", is_flag=True, help="Regenerate files that already exist.")
def main(regenerate_all):
    """Generate DXF templates for extra card sizes via SCM."""
    if not GENERATE_DXF.exists():
        raise click.ClickException(f"generate_dxf.py not found at {GENERATE_DXF}")

    ensure_symlink()

    sizes = extra_card_sizes()
    if not sizes:
        click.echo("No extra card sizes found.")
        return

    click.echo(f"Extra card sizes: {', '.join(sizes)}")

    paper_sizes = ["letter", "a4", "tabloid", "a3", "arch_b"]
    variants = ["default", "borderless"]

    for card_size in sizes:
        click.echo(f"\n=== {card_size} ===")
        out_dir = SCRIPT_DIR / "cutting_templates" / "games" / card_size
        out_dir.mkdir(parents=True, exist_ok=True)

        for paper in paper_sizes:
            for variant in variants:
                variant_label = "" if variant == "default" else f"_{variant}"
                filename = f"{card_size}{variant_label}_{paper}.dxf"
                out_file = out_dir / filename

                if out_file.exists() and not regenerate_all:
                    click.echo(f"  [skip] {filename}")
                    continue

                cmd = [
                    sys.executable, str(GENERATE_DXF), "single", str(out_file),
                    "--card_size", card_size,
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


if __name__ == "__main__":
    main()
