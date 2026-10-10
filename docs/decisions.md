# Decisions

- 2026-10-10 — **Hosting: GitHub Pages** (repo hanoisolo/inguyen-site, custom domain www.inguyen.ca). Static site, no framework; free and allowed for commercial use (Vercel Hobby is non-commercial only). Same setup as games/conquest.
- 2026-10-10 — **Single page, plain HTML/CSS/JS, no build step.** Small content set; keeps it fast and editable without tooling.
- 2026-10-10 — **Content in HTML, not JSON.** Works without JS and is indexable; the spec table is the source of truth.
- 2026-10-10 — **Theme from Don's portrait:** near-black navy + electric blue/ice cyan glow; motion is subtle and off under prefers-reduced-motion.
- 2026-10-10 — **No web fonts / CDNs.** System font stack; performance and privacy.
- 2026-10-10 — **Groups:** Learning games, Just for fun, Adults only (18+), Coming soon (Don's call). Kids' names in Geo Quest titles are fine (Don).
- 2026-10-10 — **portfolio.inguyen.ca is folded in;** its template projects are dropped. Its future (redirect vs remove) is segment 6.
- 2026-10-10 — **Google Sites posts retired;** nothing carried over (Don).
- 2026-10-10 — **Thumbnails** captured headlessly from the live games at 1280×800, cropped to the content and saved as 640×400 webp. FantasyQuest has no live site, so its thumbnail is from a local run of the repo.
- 2026-10-10 — **Contact = links only** (GitHub, X, LinkedIn). No email, no form (Don).
- 2026-10-10 — **Games layout after visual review:** Geo Conquest is a full-row horizontal featured card; the three single-card groups (Just for fun, Adults 18+, Coming soon) sit side by side in one `.group-row` on desktop instead of three near-empty rows.
- 2026-10-10 — **Canonical link** added in segment 1 (the gate's external-link check was narrowed to scripts/stylesheets only).
