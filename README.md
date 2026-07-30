# Extra Templates for Silhouette Card Maker

Game-specific templates for [Silhouette Card Maker](https://github.com/alan-cha/silhouette-card-maker) including:

* Magic: The Gathering
* Sorcery: Contested Realm

## Setup

1. Download this repo so it sits next to `silhouette-card-maker`:

   ```
   Documents/
   ├── silhouette-card-maker/
   └── scm-extras/
   ```

`standard_mtg` and `standard_sorcery` share the exact same dimensions as SCM's built-in `standard` card size (63mm x 88mm) — that's why they're named that way. This means you can generate your PDF with SCM's own `--card_size standard` and cut with the `standard_mtg`/`standard_sorcery` templates in [cutting_templates](cutting_templates) without doing anything else below. (Corner radius differs slightly — `standard_mtg` is 2.5mm and `standard_sorcery` is 4.5mm, vs `standard`'s 3mm default — so printed art may not perfectly hug the cut line right at the corners.)

Steps 2-4 below are only needed if you want SCM to recognize the `mtg`/`sorcery` names directly, or you're adding a template whose dimensions don't already match an existing SCM card size.

2. Copy `scm-extras/assets/layouts_extra.json` into `silhouette-card-maker/assets/extra_layouts/`.

3. Verify it worked. From `silhouette-card-maker`, run:

   ```shell
   python create_pdf.py --help
   ```

   Look at the `--card_size` line — you should see new card sizes listed.

4. Use the new card sizes. For example:

   ```shell
   python create_pdf.py --card_size mtg
   ```

   Then cut with the appropriate cutting template from [here](cutting_templates).

## Extra card sizes

`standard_mtg` and `standard_sorcery` are the same width/height as SCM's built-in `standard` card size (63mm x 88mm, see above) — only the corner radius differs.

| Card size | Inches | Millimeters | Aspect Ratio | Notes |
| --- | --- | --- | --- | --- |
| `standard_mtg` | 2.48 x 3.465 | **63 x 88** | 0.7159 | AKA `mtg`<br>AKA `magic`<br>AKA `magic_the_gathering` |
| `standard_sorcery` | 2.48 x 3.465 | **63 x 88** | 0.7159 | AKA `sorcery`<br>AKA `sorcery_contested_realm` |

| Format | `letter` | `tabloid` | `a4` | `a3` | `arch_b` |
|---|---|---|---|---|---|
| `standard_mtg` | 4x2 (8) | 4x4 (16) | 4x2 (8) | 6x3 (18) | 6x3 (18) |
| `standard_sorcery` | 4x2 (8) | 4x4 (16) | 4x2 (8) | 6x3 (18) | 6x3 (18) |

---

## For maintainers

Extra card sizes are defined in [assets/layouts_extra.json](assets/layouts_extra.json). SCM has an opt-in extension point: every SCM script that loads layout config merges in extra card sizes/paper sizes/layouts:

1. Any `*.json` file dropped into `silhouette-card-maker/assets/extra_layouts/`.
2. Any file(s) listed in the `SCM_EXTRA_LAYOUTS` environment variable. Note the `SCM_CUTTING_TEMPLATES_DIR` environment variable as well.

`generate.py` and `generate_readme_tables.py` below always use option 2, pointed at this repo's own `assets/layouts_extra.json`. If you've *also* copied that file into `silhouette-card-maker/assets/extra_layouts/` (option 1, e.g. for your own testing per Setup), both scripts will fail with `'standard_mtg' in card_sizes ... already defined` — the same file is being merged twice. Remove the copy from `extra_layouts/` before running these, or unset `SCM_EXTRA_LAYOUTS`.

### Generating DXF templates

From this repo:

```shell
python generate.py
```

### Regenerating the README tables

After running `generate.py` (so `assets/layouts_extra.json` has fresh layout data), regenerate the two tables in the "Extra card sizes" section above:

```shell
python generate_readme_tables.py
```

It prints markdown to stdout — paste the output over the existing tables above.

### Generating .studio3 files

**PowerShell:**
```powershell
cd ..\silhouette-card-maker
$env:SCM_EXTRA_LAYOUTS = "..\scm-extras\assets\layouts_extra.json"
$env:SCM_CUTTING_TEMPLATES_DIR = "..\scm-extras\cutting_templates"
python dxf_to_studio3.py batch --unit mm
```

**bash:**
```shell
cd ../silhouette-card-maker
SCM_EXTRA_LAYOUTS=../scm-extras/assets/layouts_extra.json SCM_CUTTING_TEMPLATES_DIR=../scm-extras/cutting_templates python dxf_to_studio3.py batch --unit mm
```
