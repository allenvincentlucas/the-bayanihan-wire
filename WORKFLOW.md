# The Bayanihan Wire — Build Workflow

This folder is the reusable template + instructions for turning a pasted batch of
Filipino good-news articles (with optional YouTube links) into a new dated issue
of **The Bayanihan Wire**, styled as a community dispatch board.

Use this every time the input is: *"here are today's good-news articles, format
them into the blog"* — with or without an explicit request for HTML.

## Files in this folder

- `template.html` — the master page for a single issue. All design tokens
  (color, type, layout, motion) live here. Copy it, don't rebuild it from
  scratch.
- `archive-template.html` — the master page for `archive/index.html`, the
  ledger listing every past issue.
- `scripts/generate_og_image.py` — generates the 1200×630 social preview
  card for a new issue. Requires Pillow (`pip install pillow
  --break-system-packages`). Fonts are bundled in `scripts/fonts/` — always
  run it from inside `scripts/` so it finds them.
- `assets/img/og-default.png` — generic fallback preview card (used by the
  archive listing page).
- `WORKFLOW.md` — this file.

## Favicon

The site uses a small version of the sun-ray seal as its favicon, generated
by `scripts/generate_favicon.py` into `assets/favicon/`. It only needs to be
generated once — reuse the same files for every new issue; there's no
per-issue favicon. If the brand mark ever changes, regenerate with:

```bash
cd scripts
python3 generate_favicon.py --out ../assets/favicon
```

Every page's `<head>` links to it with paths relative to that page's own
location — root-level pages (`index.html`, `template.html`) use
`assets/favicon/...`, while anything inside `archive/` uses
`../assets/favicon/...`. Keep that in mind if a new page type is ever added
at a different folder depth.

## Social preview cards & sharing

Every issue gets its own Open Graph / Twitter Card meta tags plus a
matching 1200×630 preview image, so the page shows a proper title, summary,
and image card whenever someone pastes the link into Facebook, X, Slack,
iMessage, etc. A "Pass It On" share strip at the bottom of the page also
lets readers push the post out directly.

### Generating the preview image

```bash
cd scripts
python3 generate_og_image.py \
  --date "Full weekday, Month D, YYYY" \
  --headline "The issue's lead headline or a punchy summary line" \
  --count 6 \
  --out ../assets/img/og-YYYY-MM-DD.png
```

Save the output into the live repo's `assets/img/` folder.

### Filling the meta tag placeholders

In the new issue's `<head>`, replace every token:

| Token | Value |
|---|---|
| `{{ISSUE_DATE_LONG}}` | e.g. `August 4, 2026` |
| `{{ISSUE_DATE_ISO}}` | e.g. `2026-08-04` (must match the image filename) |
| `{{ISSUE_DESCRIPTION}}` | One specific sentence naming that day's actual stories — not generic boilerplate. This is what shows under the title in link previews. |
| `{{SITE_BASE_URL}}` | The live GitHub Pages URL with no trailing slash, e.g. `https://username.github.io/repo-name`. **This must be an absolute URL** — Facebook/X/Slack crawlers fetch `og:image` directly and cannot resolve relative paths. |

Once `SITE_BASE_URL` is known (after the repo is connected — see "Direct
push setup"), it only needs to be set once; carry it forward into every new
issue rather than re-deriving it each time.

### The share strip

The share buttons and their JS live in `template.html` unchanged — they
read the page's own `og:title`, `og:description`, and current URL at
runtime, so **no per-issue JS editing is needed.** Just make sure the meta
tags above are filled in correctly, since the share buttons pull from them.

- **Facebook** opens `facebook.com/sharer/sharer.php?u=<page URL>`. Facebook
  deprecated pre-filled quote text in the share dialog for policy reasons
  around 2018 — the preview shown is pulled from the page's `og:` tags, not
  from anything the share link can override. This is a platform limitation,
  not a bug in the button.
- **X** opens `twitter.com/intent/tweet?text=...&url=...`, which *does*
  fully pre-populate the compose box with the title, description, and link.
- **Instagram has no web share intent at all** — there is no URL scheme a
  browser can open that pre-fills an Instagram post or Story with text from
  a website. The Instagram button instead copies a ready-made caption
  (title + description + link) to the clipboard and opens instagram.com, so
  the reader can paste it into a post or Story themselves. Set expectations
  with the user accordingly — this is the practical ceiling of what's
  possible without building and shipping an Instagram Graph API integration
  (business account, app review, access tokens), which is out of scope for
  a static site.

## Concept, in one paragraph

The site is a digital corkboard of "dispatches." Each story is a torn-paper
card pinned to a linen board, styled like a community telegram/newswire —
grounded in *bayanihan* (communal spirit) as the theme, not a generic news
template. A sun-ray seal (echoing the Philippine flag's sun) is the masthead
signature. Keep that concept when writing new copy — don't drift toward a
generic "blog card grid" look.

## Step-by-step: turning pasted articles into a new issue

1. **Intake.** The user will paste one or more articles/news items, each
   typically containing: a headline, a body of 1–3 paragraphs, one or more
   source links, and sometimes a YouTube link for video coverage.

2. **Determine the issue date.** Use the date the user gives, or today's date
   if unspecified. This becomes `{{ISSUE_DATE_LONG}}` (e.g. `August 4, 2026`)
   and `{{ISSUE_DATELINE}}` (e.g. `MANILA · TUESDAY, AUGUST 4, 2026`).

3. **For each story, assign:**
   - `{{N}}` — sequential dispatch number, in the order the stories appear.
   - `{{CATEGORY}} · {{SUBCATEGORY}}` — short, all-caps-styled label pair,
     e.g. `Sport · Tennis`, `Community · Philanthropy`. Keep it to two words
     max per side.
   - `{{EMOJI}}` — one emoji that matches the story's subject (tennis ball,
     handshake, medal, etc.). Skip if nothing fits naturally — don't force one.
   - `{{HEADLINE}}` — rewritten as a punchy title, not a copy-pasted article
     headline.
   - `{{PARAGRAPH_1}}` (and optionally `_2`) — **rewrite the story in your own
     words.** Do not reproduce source text verbatim. Follow standard copyright
     practice: paraphrase, keep any direct quote under 15 words and use at
     most one per source. See the copyright rules you already follow for
     search-derived content — the same bar applies here even though the user
     pasted the text themselves, since it still originates from copyrighted
     news articles.

4. **Handle each YouTube link:**
   - Extract the video ID from any of these patterns:
     `youtube.com/watch?v=VIDEO_ID`, `youtu.be/VIDEO_ID`,
     `youtube.com/embed/VIDEO_ID`, `youtube.com/shorts/VIDEO_ID`.
   - If a clean ID is found, include the `.clipping` block from the template
     with `src="https://www.youtube.com/embed/VIDEO_ID"`. Write a short
     `{{VIDEO_CAPTION}}` (e.g. the outlet name + "Match Highlights").
   - If the URL is malformed, wrapped in an unrelated redirect (e.g. a Google
     search URL), or doesn't resolve to a real video ID — **do not guess.**
     Drop the `.clipping` block entirely and instead add a plain `Watch:`
     link in the `.links` row, pointing to the original URL as given.

5. **Assemble sources.** Every `Read:` link the user provided goes in the
   `.links` row for that dispatch, each as its own `<a>`, labelled with the
   outlet name (e.g. `Manila Bulletin`, `Philippine News Agency`).

6. **Write the intro line.** One sentence at the top of the masthead
   summarizing the day's spread (e.g. "Six dispatches pinned to today's
   board — from a historic tennis crown in Washington to a community award
   in Eastern Visayas."). Keep it specific to that day's actual stories, not
   generic.

7. **Duplicate the dispatch block** in `template.html` once per story, fill
   in every `{{PLACEHOLDER}}`, delete the HTML comments, and save the result
   as `index.html`.

8. **Sanity check before delivering:**
   - Every placeholder token has been replaced (search for `{{` to confirm
     none remain).
   - Every dispatch has at least one `Read:` link.
   - No copied sentence runs 15+ words verbatim from a source.
   - Embedded videos only appear where a real video ID was confirmed.

## Design tokens (do not change without explicit request)

| Role | Value |
|---|---|
| Paper (board) | `#EFE6D3` |
| Paper (card) | `#F8F2E4` |
| Ink (text) | `#202B22` |
| Ink soft (meta text) | `#4B5449` |
| Gold (pins, rule, accents) | `#D79A32` / deep `#B9791F` |
| Red (links, category accents) | `#A5332A` |
| Green (emphasis, em text) | `#4B6B4F` |
| Display type | Fraunces (variable serif) |
| Body type | Source Sans 3 |
| Meta/caption/mono type | JetBrains Mono |

Signature element: the sun-ray seal in the masthead + gold "pin" + torn-paper
card edges. If the user ever asks for a refresh, treat this as a deliberate
new design pass (see the frontend-design skill) rather than a token swap.

## Archiving a new issue

The site keeps a running `archive/` folder plus a ledger page
(`archive/index.html`) that lists every past issue. Every time a new issue
replaces the current one:

1. **Move, don't overwrite.** Take the outgoing `index.html` and save it to
   `archive/YYYY-MM-DD.html` (the date of that issue, not today's date).
2. **Fix its internal links** in the moved copy: the `📌 Browse Past Issues`
   nav link must point to `../archive/index.html` (one level up) instead of
   `archive/index.html`, since the file now lives one folder deeper.
3. **Add a ledger entry** to the top of the `.ledger` list in
   `archive/index.html` (newest entries go first). Each entry is:
   ```html
   <a class="entry" href="YYYY-MM-DD.html">
     <div class="stamp"><span>MON<br>DD</span></div>
     <div class="meta">
       <div class="date">Full weekday, Month D, YYYY</div>
       <h2>Short evocative title for the issue</h2>
       <p class="desc">One-sentence teaser summarizing the day's spread.</p>
     </div>
     <div class="arrow">→</div>
   </a>
   ```
4. **Publish the new issue** as the new `index.html` at the repo root, with
   a fresh `📌 Browse Past Issues` link pointing to `archive/index.html`.

## The "paste and push" workflow

Once the user has connected a GitHub repo (see "Direct push setup" below),
they can simply paste a formatted blog post — headline(s)/body text plus any
YouTube links — and expect the result pushed straight to GitHub, with no
intermediate zip/download step. Do this:

1. Build the new issue's `index.html` following "Filling a dispatch block"
   above.
2. Archive the current `index.html` per "Archiving a new issue" above.
3. Update `archive/index.html` with the new ledger entry.
4. Clone or pull the latest state of the connected repo, apply these three
   file changes, commit with a message like `New issue: <date>`, and push.
5. Confirm the push succeeded and report the commit/URL back to the user —
   don't just say "done," show what changed.

### Direct push setup

To push on the user's behalf, a fine-grained GitHub personal access token is
needed for each session (these are short-lived and should be revoked by the
user once no longer needed):

- **Repository access:** the one specific repo only
- **Permissions:** Contents → Read and write
- Provided by the user along with their GitHub username and repo name

Never store, log, or echo the token back in a response. Use it only inline
in the git remote URL for the push commands, then discard it at the end of
the session. If the user wants a standing/recurring setup instead of pasting
a token each time, that's a call for them to make and outside what this
workflow assumes by default — flag it rather than assuming.

## GitHub Pages gotcha: `.nojekyll`

GitHub Pages runs Jekyll by default, and Jekyll's Liquid engine treats
`{{ ... }}` as its own template syntax — which collides directly with the
`{{PLACEHOLDER}}` tokens used here and breaks the build with a
`Liquid syntax error ... Variable '{{' was not properly terminated` error.

Always include an empty `.nojekyll` file at the repo root of any site built
from this template. It tells GitHub Pages to serve the files as plain
static HTML and skip Jekyll/Liquid processing entirely. It's already
included in this folder — copy it into any repo scaffold you create.

## When the user says "make this into a GitHub repo / site"

Use the repo scaffold workflow below (also documented in this project) to
turn the finished `index.html` into a publishable GitHub Pages site.
