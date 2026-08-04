# The Bayanihan Wire

A single-page, single-file good-news digest celebrating Filipino excellence
and community spirit — styled as a pinned-up community dispatch board.
Published via GitHub Pages.

**Live site:** `https://allenvincentlucas.github.io/the-bayanihan-wire/`
(fill in once Pages is enabled — see below)

## What's in this repo

```
.
├── index.html              ← the current/latest issue (what visitors see)
├── archive/
│   ├── index.html          ← ledger page listing every past issue
│   └── YYYY-MM-DD.html     ← one archived issue per date
├── social/
│   └── YYYY-MM-DD.md       ← ready-to-post captions (X, Facebook, Instagram)
├── assets/
│   ├── favicon/             ← favicon set (ico, svg, png, apple-touch-icon)
│   └── img/                 ← generated social preview cards (og-*.png)
├── scripts/
│   ├── generate_og_image.py ← generates the preview card for a new issue
│   └── generate_favicon.py  ← regenerates the favicon set (one-time/rare)
├── template.html           ← reusable master template for a new issue
├── archive-template.html   ← reusable master template for the ledger page
├── WORKFLOW.md              ← step-by-step build + archive + push instructions
└── README.md               ← this file
```

The live `index.html` links to `archive/index.html` via a "📌 Browse Past
Issues" nav link under the masthead, and the archive ledger links back to
the latest issue.

## Social sharing

Every issue has its own Open Graph/Twitter preview card (title, summary,
1200×630 image) so links look right when shared on Facebook, X, Slack,
iMessage, etc., plus a "Pass It On" share strip at the bottom of the page
with working Facebook and X buttons (both open with the post's
title/description/link already filled in) and an Instagram button that
copies a ready-made caption to the clipboard, since Instagram doesn't
support pre-filled posts from a website.

Every issue also comes with a `social/YYYY-MM-DD.md` file containing
ready-to-paste captions written specifically for X, Facebook, and
Instagram — no manual copywriting needed per post. Full details are in
`WORKFLOW.md`.

**Live URL is already set.** The social preview meta tags in `index.html`
and `archive/` are wired to `https://allenvincentlucas.github.io/the-bayanihan-wire`
— no placeholder replacement needed. If this repo is ever renamed or moved
to a different account, update every occurrence of that URL accordingly so
Facebook/X can still find the preview image.

## Publishing a new issue

1. Paste the day's articles (and any YouTube links) to Claude, following
   `WORKFLOW.md`.
2. Once the new `index.html` is generated:
   - Move the **current** `index.html` into `archive/` and rename it to
     its issue date, e.g. `archive/2026-08-04.html`.
   - Save the newly generated page as the new `index.html` at the repo root.
3. Commit and push:
   ```
   git add .
   git commit -m "New issue: <date>"
   git push
   ```
4. GitHub Pages redeploys automatically within a minute or two.

## Important: `.nojekyll`

This repo includes an empty `.nojekyll` file at the root. **Do not delete it.**
GitHub Pages runs Jekyll by default, and Jekyll's Liquid templating engine
treats `{{ ... }}` as its own syntax — which collides with the
`{{PLACEHOLDER}}` tokens in `template.html` and `WORKFLOW.md` and breaks the
build (`Liquid syntax error ... Variable '{{' was not properly terminated`).
`.nojekyll` tells GitHub Pages to skip Jekyll entirely and serve the files
as plain static HTML, which is all this site needs.

## Enabling GitHub Pages (first-time setup)

1. Push this repo to GitHub (see "Creating the repo" below if starting fresh).
2. On GitHub: **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. Branch: `main`, folder: `/ (root)`. Save.
5. GitHub gives you the live URL after the first deploy — update it at the
   top of this README.

## Creating the repo from scratch

```bash
cd bayanihan-wire-site
git init
git add .
git commit -m "Initial commit: The Bayanihan Wire site scaffold"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Then follow "Enabling GitHub Pages" above.

## Design credit / theme notes

Palette, type, and the corkboard/dispatch concept are documented in
`WORKFLOW.md` under **Design tokens** — keep future issues visually
consistent with those values unless a deliberate redesign is requested.
