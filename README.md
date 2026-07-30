# scm-extras

Extra card sizes for [Silhouette Card Maker](https://github.com/alan-cha/silhouette-card-maker): `mtg` (Magic: The Gathering) and `sorcery` (Sorcery: Contested Realm).

## Setup

1. Download this repo so it sits next to `silhouette-card-maker`:

   ```
   Documents/
   ├── silhouette-card-maker/
   └── scm-extras/
   ```

2. Copy `scm-extras/assets/layouts_extra.json` into `silhouette-card-maker/assets/extra_layouts/`. No terminal needed — a regular copy-paste in File Explorer/Finder works fine.

3. Verify it worked. From `silhouette-card-maker`, run:

   ```shell
   python create_pdf.py --help
   ```

   Look at the `--card_size` line — you should see new card sizes listed. You can now use new card sizes like any built-in card size.

   For example:

   ```shell
   create_pdf.py --card_size mtg
   ```

   You can find the appropriate cutting template in [cutting_templates](cutting_templates).

## Extra card sizes

| Card size | Inches | Millimeters | Aspect Ratio | Notes |
| --- | --- | --- | --- | --- |
| `standard_mtg` | **2.5 x 3.5** | 63.5 x 88.9 | 0.7143 | AKA `mtg`<br>AKA `magic`<br>AKA `magic_the_gathering` |
| `standard_sorcery` | **2.5 x 3.5** | 63.5 x 88.9 | 0.7143 | AKA `sorcery`<br>AKA `sorcery_contested_realm` |

| Format | `letter` | `tabloid` | `a4` | `a3` | `arch_b` |
|---|---|---|---|---|---|
| `standard_mtg` | 4x2 (8) | 4x4 (16) | 4x2 (8) | 4x4 (16) | 6x3 (18) |
| `standard_sorcery` | 4x2 (8) | 4x4 (16) | 4x2 (8) | 4x4 (16) | 6x3 (18) |

---

## For maintainers: generating cutting templates

This section is only relevant if you're adding a new card size or regenerating cutting templates — regular users don't need any of this.

Extra card sizes are defined in `assets/layouts_extra.json`. SCM has an opt-in extension point: every SCM script that loads layout config (DXF generation, `.studio3` conversion, PDF creation, etc.) merges in extra card sizes/paper sizes/layouts from two places, with no changes to SCM's own tracked files:

1. Any `*.json` file dropped into `silhouette-card-maker/assets/extra_layouts/` (this is what regular users do, per Setup above).
2. Any file(s) listed in the `SCM_EXTRA_LAYOUTS` environment variable (`os.pathsep`-separated for more than one) — useful for a file that lives outside SCM's tree, like this repo's own `generate.py` below, which points it directly at `scm-extras/assets/layouts_extra.json` rather than requiring a copy step.

`SCM_CUTTING_TEMPLATES_DIR` similarly redirects where SCM reads/writes `cutting_templates/` — `generate.py` sets both automatically for the commands it runs, so DXFs land in `scm-extras/cutting_templates/` instead of SCM's own.

### Adding a new card size

Add an entry to `assets/layouts_extra.json` under `card_sizes`:

```json
"my_game": {
  "width": "2.5in",
  "height": "3.5in",
  "radius": "2.5mm",
  "aliases": ["my_game_alias"]
}
```

### Generating DXF templates

From this repo (same command in PowerShell or bash):

```
python generate.py        # generate missing DXF templates for extra card sizes
python generate.py --all  # regenerate all
```

This calls SCM's `generate_dxf.py single --save` once per missing paper/card/variant combination, which both writes the DXF (into `scm-extras/cutting_templates/`) and persists the computed layout (orientation, rows/cols, registration) back into `assets/layouts_extra.json`.

### Regenerating the README tables

After running `generate.py` (so `assets/layouts_extra.json` has layout data to read), regenerate the two tables in the "Extra card sizes" section above:

```
python generate_readme_tables.py
```

This mirrors SCM's own `generate_readme_tables.py` (reusing its `format_number()` and `load_layout_config()` directly) but scoped to just this repo's extra card sizes. It prints markdown to stdout — paste the output over the existing tables above.

### Generating .studio3 files

To produce `.studio3` files, run SCM's own batch converter with the same env vars pointed at this repo:

**PowerShell:**
```powershell
cd ..\silhouette-card-maker
$env:SCM_EXTRA_LAYOUTS = "..\scm-extras\assets\layouts_extra.json"
$env:SCM_CUTTING_TEMPLATES_DIR = "..\scm-extras\cutting_templates"
python dxf_to_studio3.py batch --unit mm
```

**bash:**
```bash
cd ../silhouette-card-maker
SCM_EXTRA_LAYOUTS=../scm-extras/assets/layouts_extra.json SCM_CUTTING_TEMPLATES_DIR=../scm-extras/cutting_templates python dxf_to_studio3.py batch --unit mm
```

Note: unlike the bash form (scoped to just that one command), PowerShell's `$env:VAR = ...` persists for the rest of the session — clear it with `$env:SCM_CUTTING_TEMPLATES_DIR = $null` (or close the terminal) before running plain SCM commands that shouldn't redirect output.

Other SCM tools (e.g. `create_pdf.py`) already see the extra sizes automatically once you've done Setup step 2 above (the file is sitting in `extra_layouts/`) — no env var needed for that. Set `SCM_CUTTING_TEMPLATES_DIR` the same way as above only if the tool reads/writes `cutting_templates/` and you want that redirected to this repo too.
