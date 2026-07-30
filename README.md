# scm-extras

Extra card sizes for [Silhouette Card Maker](https://github.com/alan-cha/silhouette-card-maker): `mtg` (Magic: The Gathering) and `sorcery` (Sorcery: Contested Realm).

## Setup

1. Download this repo so it sits next to `silhouette-card-maker`:

   ```
   Documents/
   ├── silhouette-card-maker/
   └── scm-extras/
   ```

2. Copy `scm-extras/assets/layouts-extra.json` into `silhouette-card-maker/assets/extra_layouts/`. No terminal needed — a regular copy-paste in File Explorer/Finder works fine.

3. Verify it worked. From `silhouette-card-maker`, run:

   ```
   python generate_dxf.py list
   ```

   You should see `standard_mtg` and `standard_sorcery` (with aliases `mtg`/`sorcery`, etc.) in the card sizes list. SCM's normal commands will now accept `--card_size mtg` (or `sorcery`) just like any built-in card size — no environment variables or per-session setup needed.

   Note: the `.studio3` conversion step further down (`dxf_to_studio3.py`) is Windows-only. On macOS/Linux you can still use the extra card sizes for PDF generation (`create_pdf.py`) etc., just not that step.

## Extra card sizes

| Name | Dimensions | Corner radius | Game |
|------|-----------|---------------|------|
| `mtg` | 2.5 × 3.5 in | 2.5 mm | Magic: The Gathering |
| `sorcery` | 2.61 × 3.74 in | 3.5 mm | Sorcery: Contested Realm |

---

## For maintainers: generating cutting templates

This section is only relevant if you're adding a new card size or regenerating cutting templates — regular users don't need any of this.

Extra card sizes are defined in `assets/layouts-extra.json`. SCM has an opt-in extension point: every SCM script that loads layout config (DXF generation, `.studio3` conversion, PDF creation, etc.) merges in extra card sizes/paper sizes/layouts from two places, with no changes to SCM's own tracked files:

1. Any `*.json` file dropped into `silhouette-card-maker/assets/extra_layouts/` (this is what regular users do, per Setup above).
2. Any file(s) listed in the `SCM_EXTRA_LAYOUTS` environment variable (`os.pathsep`-separated for more than one) — useful for a file that lives outside SCM's tree, like this repo's own `generate.py` below, which points it directly at `scm-extras/assets/layouts-extra.json` rather than requiring a copy step.

`SCM_CUTTING_TEMPLATES_DIR` similarly redirects where SCM reads/writes `cutting_templates/` — `generate.py` sets both automatically for the commands it runs, so DXFs land in `scm-extras/cutting_templates/` instead of SCM's own.

### Adding a new card size

Add an entry to `assets/layouts-extra.json` under `card_sizes`:

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

This calls SCM's `generate_dxf.py single --save` once per missing paper/card/variant combination, which both writes the DXF (into `scm-extras/cutting_templates/`) and persists the computed layout (orientation, rows/cols, registration) back into `assets/layouts-extra.json`.

### Generating .studio3 files

To produce `.studio3` files, run SCM's own batch converter with the same env vars pointed at this repo:

**PowerShell:**
```powershell
cd ..\silhouette-card-maker
$env:SCM_EXTRA_LAYOUTS = "..\scm-extras\assets\layouts-extra.json"
$env:SCM_CUTTING_TEMPLATES_DIR = "..\scm-extras\cutting_templates"
python dxf_to_studio3.py batch --unit mm
```

**bash:**
```bash
cd ../silhouette-card-maker
SCM_EXTRA_LAYOUTS=../scm-extras/assets/layouts-extra.json SCM_CUTTING_TEMPLATES_DIR=../scm-extras/cutting_templates python dxf_to_studio3.py batch --unit mm
```

Note: unlike the bash form (scoped to just that one command), PowerShell's `$env:VAR = ...` persists for the rest of the session — clear it with `$env:SCM_CUTTING_TEMPLATES_DIR = $null` (or close the terminal) before running plain SCM commands that shouldn't redirect output.

Other SCM tools (e.g. `create_pdf.py`) already see the extra sizes automatically once you've done Setup step 2 above (the file is sitting in `extra_layouts/`) — no env var needed for that. Set `SCM_CUTTING_TEMPLATES_DIR` the same way as above only if the tool reads/writes `cutting_templates/` and you want that redirected to this repo too.
