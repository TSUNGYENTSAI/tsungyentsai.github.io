# tsungyentsai.github.io

Personal site of Tsung-Yen Tsai (蔡宗諺) — systems-oriented engineer for
physical-world automation: robotics, simulation, optimization.

Single static `index.html`, no build step. Content is sourced from my private
career repository (claims-controlled wording); edit there first, then update here.

## Writing workflow

- `planning/`: tracked article-series plans and writing decision records.
- `drafts/`: local working drafts; intentionally gitignored.
- `posts/`: published HTML articles.

## Visual style

The homepage, career page, and articles share the warm-white / muted-green
visual guide from `career/50_career_assets/presentations/visual-style/`
(version 1.0, 2026-09-15). Shared tokens, typography, responsive layout, and
keyboard focus states live in `stylesheets/styles.css`; existing article
figures live in `stylesheets/article-figures.css` and use the same tokens.

Lato Regular, Bold, and Italic are served locally from `assets/fonts/` under
the included OFL license. Chinese text falls back to Noto Sans TC when
installed, then PingFang TC or Microsoft JhengHei. No font CDN is required.

Preview locally with `python3 -m http.server 8765 --bind 127.0.0.1` and open
`http://127.0.0.1:8765/`. Check the homepage, career page, and all four articles
at 1440, 768, and 390 px widths after changing shared styles. Wide article
tables scroll within their own containers; comparison tables stack on mobile.

Desktop navigation stays in a sticky left sidebar; at 960 px and below it
returns to a compact top navigation so the reading column retains its width.

The website refines the source palette with neutral charcoal text (`#303438`)
and gray supporting text (`#666A70`). Headings and navigation use neutrals;
gray-blue identifies writing links. Green is reserved for hover/focus states
and diagram accents. Spacing replaces decorative section and list dividers.
