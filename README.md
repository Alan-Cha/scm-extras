# Extra Cutting Templates for Silhouette Card Maker

[Silhouette Card Maker](https://github.com/alan-cha/silhouette-card-maker) is a tool for cutting cards with Silhouette cutting machines.

SCM offers [one-size-fits-all cutting templates](https://github.com/Alan-Cha/silhouette-card-maker/tree/main/cutting_templates) but for those who want tailored-made templates such as ones designed for particular games, use the [templates from this repo](https://github.com/Alan-Cha/scm-extras/tree/main/cutting_templates) instead.

Supported games:
* Magic: The Gathering
* Sorcery: Contested Realm

## Basic Usage

Most extra templates are based on [preexisting sizes](https://github.com/Alan-Cha/silhouette-card-maker#supported-sizes) supported by SCM. 

Simply generate the PDF normally but use the desired extra template to cut.

For example, for MTG cards, generate a PDF with the `standard` card size but use a `standard_mtg` template to cut.

```shell
python create_pdf.py
```

This creates a PDF with the `letter` paper size and `standard` card size (by default).

Use the `letter-standard_mtg-v<version>.studio3` template from the [cutting templates](https://github.com/Alan-Cha/scm-extras) to cut.

## Advanced Usage

For extra templates that are not based on [preexisting sizes](https://github.com/Alan-Cha/silhouette-card-maker#supported-sizes) or if you want to use these new sizes directly in SCM like so:

```shell
python create_pdf.py --card_size standard_mtg
```

then follow these steps:

1. Download the `layouts_extra.json` file from [here](https://github.com/Alan-Cha/scm-extras/blob/main/assets/layouts_extra.json).

2. Put `layouts_extra.json` into the `assets/extra_layouts/` folder in SCM.

3. Verify that SCM can utilize the new sizes by running:

   ```shell
   python create_pdf.py --help
   ```

   Look at the `--card_size` line — you should see new sizes listed.

4. Now, you can use the new sizes. For example:

   ```shell
   python create_pdf.py --card_size standard_mtg
   ```

   Then cut with the appropriate cutting template from [here](cutting_templates).

## Extra Sizes

| Card size | Inches | Millimeters | Aspect Ratio | Notes |
| --- | --- | --- | --- | --- |
| `standard_mtg` | 2.48 x 3.465 | **63 x 88** | 0.7159 | AKA `mtg`<br>AKA `magic`<br>AKA `magic_the_gathering` |
| `standard_sorcery` | 2.48 x 3.465 | **63 x 88** | 0.7159 | AKA `sorcery`<br>AKA `sorcery_contested_realm` |

| Format | `letter` | `tabloid` | `a4` | `a3` | `arch_b` |
|---|---|---|---|---|---|
| `standard_mtg` | 4x2 (8) | 4x4 (16) | 4x2 (8) | 6x3 (18) | 6x3 (18) |
| `standard_sorcery` | 4x2 (8) | 4x4 (16) | 4x2 (8) | 6x3 (18) | 6x3 (18) |

## For maintainers

Extra card sizes are defined in [assets/layouts_extra.json](assets/layouts_extra.json). SCM has an opt-in extension point: every SCM script that loads layout config merges in extra card sizes/paper sizes/layouts:

1. Any `*.json` file dropped into `silhouette-card-maker/assets/extra_layouts/`.
2. Any file(s) listed in the `SCM_EXTRA_LAYOUTS` environment variable. Note the `SCM_CUTTING_TEMPLATES_DIR` environment variable as well.

### Generating DXF templates

From this repo (requires `scm-extras` and `silhouette-card-maker` to be sister folders, as in Setup — `generate.py` looks for `../silhouette-card-maker` relative to this repo):

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
