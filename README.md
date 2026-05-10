# Academic CV

Static CV site. Content in `content/cv.json`, rendered into HTML by `build.py`, deployed to GitHub Pages on every push to `main`.

## Structure

```
content/cv.json          — all content
templates/index.html     — Jinja2 template
templates/icons/*.svg    — icons referenced via useful_links[].icon
assets/style.css         — styling
build.py                 — renders templates → dist/
.github/workflows/       — CI/CD pipeline
```

## Local preview

```bash
pip install -r requirements.txt
python build.py --serve
```

Open <http://localhost:8000>. Re-run after editing `cv.json`.

To build only:

```bash
python build.py
```

Output goes to `dist/`.

## Deployment

1. Push the repo to GitHub.
2. In repo **Settings → Pages**, set **Source** to **GitHub Actions**.
3. Push to `main`. The workflow builds and deploys.

## Editing content

Open `content/cv.json` and edit. Schema:

- `sections_order` — controls section order on the page.
- `profile.name` — used as the page title and to highlight your own name in author lists.
- `profile.name_variants` — alternate spellings (e.g. `"F. Last"`) that should also be highlighted.
- `publications` and `talks` — sorted by `year` descending automatically.

Optional fields can be omitted or left as empty strings/arrays.

### Adding an icon for a useful link

Set `useful_links[].icon` to a name matching a file in `templates/icons/` (without the `.svg`). Bundled: `scholar`, `github`, `orcid`, `linkedin`, `dblp`, `email`. Add more SVGs in that folder as needed.
