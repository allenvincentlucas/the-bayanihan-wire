# The Bayanihan Wire

A single-page, single-file good-news digest celebrating Filipino excellence
and community spirit — styled as a pinned-up community dispatch board.
Published via GitHub Pages.

**Live site:** `https://allenvincentlucas.github.io/the-bayanihan-wire/`

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

**The current workflow is: paste the finished articles (plus any YouTube
links) to Claude, and Claude builds and pushes the new issue directly —
no manual file editing or git commands needed on your end.**

1. Paste the day's articles and any relevant YouTube video links to Claude.
2. Provide a short-lived, fine-grained GitHub personal access token scoped
   to this repo (**Contents: Read and write** only) — see "Direct push
   access" below. Tokens expire, so expect to provide a fresh one each new
   session.
3. Claude then, in one pass:
   - Writes each story as a dispatch (paraphrased, not copy-pasted),
     embeds any valid YouTube video, and links sources.
   - Archives the outgoing issue into `archive/YYYY-MM-DD.html` and adds
     it to the `archive/index.html` ledger.
   - Generates the new issue's social preview image and fills in its
     `og:`/`twitter:` meta tags.
   - Writes ready-to-post captions for X, Facebook, and Instagram into
     `social/YYYY-MM-DD.md`.
   - Commits everything in one commit (`New issue: <date>`) and pushes.
4. Claude reports back the live URL and pastes the three social captions
   directly into the chat reply, ready to copy.
5. GitHub Pages redeploys automatically — usually within a minute, though
   the Pages "builds" status API can lag behind the actual push by up to a
   minute or two.

Full technical detail for every step above lives in `WORKFLOW.md`.

### Direct push access

To push on your behalf, Claude needs, once per session:

- A **fine-grained personal access token**
  (github.com → Settings → Developer settings → Personal access tokens →
  Fine-grained tokens → Generate new token)
  - **Repository access:** this repo only
  - **Permissions:** Contents → Read and write
  - **Expiration:** as short as you're comfortable with
- Your GitHub username (Claude can also resolve this from the token) and
  this repo's name.

Claude never prints, logs, or repeats the token back in chat, uses it only
inline for the git push, and removes the credentialed git remote once the
push completes. **Revoke the token after each session** once you've
confirmed the push landed, unless you've deliberately decided to keep a
longer-lived one — that's your call to make, not something Claude assumes.

### Doing it manually instead

If you'd rather build and push an issue yourself without Claude's direct
push access, the file changes are the same ones listed in step 3 above —
`WORKFLOW.md` documents the exact templates and placeholder tokens to fill
in by hand, and the git commands are the standard `git add . && git commit
&& git push`.

## Important: `.nojekyll`

This repo includes an empty `.nojekyll` file at the root. **Do not delete it.**
GitHub Pages runs Jekyll by default, and Jekyll's Liquid templating engine
treats `{{ ... }}` as its own syntax — which collides with the
`{{PLACEHOLDER}}` tokens in `template.html` and `WORKFLOW.md` and breaks the
build (`Liquid syntax error ... Variable '{{' was not properly terminated`).
`.nojekyll` tells GitHub Pages to skip Jekyll entirely and serve the files
as plain static HTML, which is all this site needs.

## GitHub Pages status

Pages is already live for this repo: **Deploy from a branch**, branch
`main`, folder `/ (root)`. No further setup needed. The reference steps
below are only for recreating this from scratch (e.g. a fork or a new repo
built from this project's template).

<details>
<summary>Enabling GitHub Pages from scratch</summary>

1. Push the repo to GitHub.
2. On GitHub: **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. Branch: `main`, folder: `/ (root)`. Save.
5. GitHub gives you the live URL after the first deploy.

</details>

<details>
<summary>Creating a new repo from this template, from scratch</summary>

```bash
cd bayanihan-wire-site
git init
git add .
git commit -m "Initial commit: The Bayanihan Wire site scaffold"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Then follow "Enabling GitHub Pages from scratch" above.

</details>

## Design credit / theme notes

Palette, type, and the corkboard/dispatch concept are documented in
`WORKFLOW.md` under **Design tokens** — keep future issues visually
consistent with those values unless a deliberate redesign is requested.
