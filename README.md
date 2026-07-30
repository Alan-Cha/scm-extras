# scm-extras

Extra card sizes for [Silhouette Card Maker](https://github.com/alan-cha/silhouette-card-maker): `mtg` (Magic: The Gathering) and `sorcery` (Sorcery: Contested Realm).

## Setup

1. Download this repo so it sits next to `silhouette-card-maker`:

   ```
   Documents/
   ├── silhouette-card-maker/
   └── scm-extras/
   ```

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

| Card size | Inches | Millimeters | Aspect Ratio | Notes |
| --- | --- | --- | --- | --- |
| `standard_mtg` | **2.5 x 3.5** | 63.5 x 88.9 | 0.7143 | AKA `mtg`<br>AKA `magic`<br>AKA `magic_the_gathering` |
| `standard_sorcery` | **2.5 x 3.5** | 63.5 x 88.9 | 0.7143 | AKA `sorcery`<br>AKA `sorcery_contested_realm` |

| Format | `letter` | `tabloid` | `a4` | `a3` | `arch_b` |
|---|---|---|---|---|---|
| `standard_mtg` | 4x2 (8) | 4x4 (16) | 4x2 (8) | 4x4 (16) | 6x3 (18) |
| `standard_sorcery` | 4x2 (8) | 4x4 (16) | 4x2 (8) | 4x4 (16) | 6x3 (18) |

---

## For maintainers

Extra card sizes are defined in [assets/layouts_extra.json](assets/layouts_extra.json). SCM has an opt-in extension point: every SCM script that loads layout config merges in extra card sizes/paper sizes/layouts:

1. Any `*.json` file dropped into `silhouette-card-maker/assets/extra_layouts/`.
2. Any file(s) listed in the `SCM_EXTRA_LAYOUTS` environment variable. Note the `SCM_CUTTING_TEMPLATES_DIR` environment variable as well.

### Generating DXF templates

From this repo:

```shell
python generate.py
```

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
