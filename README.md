# scm-extras

Additional cutting templates for [Silhouette Card Maker](https://github.com/alan-cha/silhouette-card-maker).

## Setup

Clone both repos as siblings:

```
Documents/
├── silhouette-card-maker/
└── scm-extras/
```

Install SCM dependencies as described in its README, then run from this repo:

```bash
python generate.py                                         # generate all packs
python generate.py --pack games/magic_the_gathering        # one pack only
python generate.py --all                                   # regenerate existing files
```

Generated DXF files are written to each pack's `dxf/` directory (gitignored).

## Adding a pack

Create a directory under `packs/` with a `pack.json`:

```json
{
  "name": "My Game",
  "card_size": {
    "width": "2.5in",
    "height": "3.5in",
    "radius": "2.5mm"
  },
  "paper_sizes": ["letter", "a4"],
  "variants": ["default", "borderless"]
}
```

Then run `python generate.py --pack <path/to/your/pack>`.

## Packs

| Pack | Card size | Corner radius |
|------|-----------|---------------|
| Magic: The Gathering | 2.5 × 3.5 in | 2.5 mm |
| Sorcery: Contested Realm | 2.61 × 3.74 in | 3.5 mm |
