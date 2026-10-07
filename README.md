# tsungyentsai.github.io

Personal site of Tsung-Yen Tsai (蔡宗諺) — systems-oriented engineer for
physical-world automation: robotics, simulation, optimization.

Static HTML, no build step. Career facts are sourced from my private career
repository (claims-controlled wording); correct those sources before updating
the website. Homepage editorial copy and layout are authored in `index.html`,
using the user-selected visual prototype v3 as the baseline.

## Writing workflow

- `planning/`: tracked article-series plans and writing decision records.
- `drafts/`: local working drafts; intentionally gitignored.
- `posts/`: published HTML articles.

## Visual style

The homepage and articles share the warm-white / muted-green
visual guide from `career/50_career_assets/presentations/visual-style/`
(version 1.0, 2026-09-15). Shared tokens, typography, responsive layout, and
keyboard focus states live in `stylesheets/styles.css`; homepage layout is
scoped to `.home-page` in `stylesheets/homepage.css`. Existing article
figures live in `stylesheets/article-figures.css` and use the same tokens.

Lato Regular, Bold, and Italic are served locally from `assets/fonts/` under
the included OFL license. Chinese text falls back to Noto Sans TC when
installed, then PingFang TC or Microsoft JhengHei. No font CDN is required.

Preview locally with `python3 -m http.server 8765 --bind 127.0.0.1` and open
`http://127.0.0.1:8765/`. Check the homepage (Career collapsed and expanded) and all four articles
at 1440, 768, and 390 px widths after changing shared styles. Wide article
tables scroll within their own containers; comparison tables stack on mobile.

The homepage uses top navigation and the sequence Hero → compact Career strip
→ Simulation judgment → Current Thinking. It has one mature judgment and links
to the three existing English simulation articles. Unfinished questions are
plain text. Career details and education expand inline with a native `details`
control; article navigation targets `index.html#career-history`, which reveals
that disclosure when followed. The standalone career page has been removed.
The Hero uses `assets/images/yen-cutout.png`, a transparent-background illustration
made with built-in ImageGen from the user-supplied `assets/images/yen.jpg`.
The original is preserved; the background-extraction prompt is in
`assets/images/yen-cutout.prompt.txt`. The homepage applies a mild CSS saturation /
contrast reduction and an outer-edge mask; the source image stays unchanged.
On mobile the illustration
sits beside the name, and the six-entry Career strip scrolls horizontally
instead of stacking into multiple rows. Main containers own horizontal gutters;
sections use vertical padding only.

Article pages keep their existing sticky left sidebar on desktop;
at 960 px and below it returns to compact top navigation. Homepage changes do
not require edits to article content or shared styles.

Hero and footer Resume links point to `resume.html`, an HTML reading version
with local fonts, a mobile layout, and a PDF download button. Its content comes
from `career/90_generated/resumes/general/general.html`. The download at
`assets/resume/tsung-yen-tsai-general.pdf` is a byte-for-byte copy of the latest checked General PDF from
`career/90_generated/resumes/general/Tsung-Yen Tsai - General.pdf`, built from
`career/50_career_assets/role_positioning/resume_variants/general.yaml`.
After updating that source, regenerate and visually verify its HTML/PDF in the
career repository, then run `python3 tools/sync_general_resume.py` in this
website repository. The script owns web presentation and synchronizes both
artifacts. Do not edit generated `resume.html` or the PDF copy directly.

The website refines the source palette with neutral charcoal text (`#303438`)
and gray supporting text (`#666A70`). Headings and navigation use neutrals;
gray-blue identifies writing links. The homepage uses muted green for small
section labels and illustration accents, with thin dividers and open layouts.
Article pages retain their existing spacing and interaction treatment.
