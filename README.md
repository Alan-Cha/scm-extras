# scm-extras

Additional cutting templates for [Silhouette Card Maker](https://github.com/alan-cha/silhouette-card-maker).

`assets/layouts.json` is a drop-in superset of SCM's `assets/layouts.json` — it contains all standard sizes plus game-specific ones. `generate.py` uses it to produce templates for the extra card sizes, outputting to `cutting_templates/games/`.

## Setup

Clone both repos as siblings:

```
Documents/
├── silhouette-card-maker/
└── scm-extras/
```

Install SCM dependencies as described in its README, then from this repo:

```bash
python generate.py               # generate missing templates
python generate.py --all         # regenerate all
python generate.py --card mtg    # single card size
```

## Adding a new card size

1. Add an entry to `assets/layouts.json` under `card_sizes` (same schema as SCM):
   ```json
   "my_game": {
     "width": "2.5in",
     "height": "3.5in",
     "radius": "2.5mm",
     "aliases": ["my_game_alias"]
   }
   ```
2. Run `python generate.py --card my_game`.

## Keeping in sync with SCM

When SCM's `assets/layouts.json` is updated, re-apply the extra card sizes from this repo on top of the new base.

## Extra card sizes

| Name | Dimensions | Corner radius | Game |
|------|-----------|---------------|------|
| `mtg` | 2.5 × 3.5 in | 2.5 mm | Magic: The Gathering |
| `sorcery` | 2.61 × 3.74 in | 3.5 mm | Sorcery: Contested Realm |
