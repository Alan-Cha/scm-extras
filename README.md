# scm-extras

Additional cutting templates for [Silhouette Card Maker](https://github.com/alan-cha/silhouette-card-maker).

Extra card sizes are defined in `assets/layouts-extra.json`. SCM automatically detects and merges this file if it's present in its `assets/` directory, so all SCM scripts (DXF generation, PDF creation, etc.) gain access to the extra sizes with no duplication of paper sizes or other base data.

## Setup

Clone both repos as siblings:

```
Documents/
├── silhouette-card-maker/
└── scm-extras/
```

Install SCM dependencies as described in its README, then from this repo:

```bash
python generate.py        # generate missing templates (symlinks layouts-extra.json into SCM)
python generate.py --all  # regenerate all
```

To use SCM's tools directly (e.g. `create_pdf.py`) with the extra sizes, just ensure the symlink exists first by running `generate.py` once.

## Adding a new card size

Add an entry to `assets/layouts-extra.json` under `card_sizes`:

```json
"my_game": {
  "width": "2.5in",
  "height": "3.5in",
  "radius": "2.5mm",
  "aliases": ["my_game_alias"]
}
```

Then run `python generate.py`.

## Extra card sizes

| Name | Dimensions | Corner radius | Game |
|------|-----------|---------------|------|
| `mtg` | 2.5 × 3.5 in | 2.5 mm | Magic: The Gathering |
| `sorcery` | 2.61 × 3.74 in | 3.5 mm | Sorcery: Contested Realm |
