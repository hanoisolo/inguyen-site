# www.inguyen.ca — portfolio spec

Owner: Don Nguyen (GitHub hanoisolo). Replaces the retired Google Sites page; nothing carries over.
Absorbs portfolio.inguyen.ca (template content is dropped; only real work is shown).
Static site on GitHub Pages, custom domain www.inguyen.ca. Single page (`index.html`) with anchored sections.

## 1. Global layout and header
- Sticky header: wordmark "Don Nguyen" (links to `#top`), nav links: Games (`#games`), Projects (`#projects`), About (`#about`).
- Header gets a translucent near-black background with backdrop blur once scrolled (class `is-scrolled` on `<header>`).
- Skip link "Skip to content" → `#main` is the first focusable element.
- Acceptance: nav works with keyboard; on ≤ 640px the nav stays on one line (links shrink) — no hamburger needed for 3 links.

## 2. Hero (`#top`)
- Two columns on desktop (text left, portrait right), stacked on mobile (portrait first, max 280px wide).
- Portrait: `<picture>` with `assets/img/don-480.webp` / `don-800.webp` (srcset, `sizes`) and a `.jpg` fallback; explicit `width="800" height="1200"`; alt "Don Nguyen as a lightning-wielding hero". `fetchpriority="high"`, not lazy.
- Portrait frame: rounded, thin cyan border, soft electric glow behind it; a subtle pulsing glow (disabled under reduced motion).
- Eyebrow: "Developer · Game maker". H1: "Don Nguyen". Tagline (see §2a). Sub-line: "Learning games for kids, party games for grown-ups, and side projects in progress."
- CTAs: primary "Play the games" → `#games`; secondary ghost "GitHub" → https://github.com/hanoisolo (new tab, rel="noopener").
- Background: near-black with a faint radial blue glow and a decorative lightning SVG/CSS layer (`aria-hidden="true"`), with an occasional flicker animation that is off under `prefers-reduced-motion: reduce`.
- Acceptance: H1 is the only `<h1>`; hero fits above the fold at 1280×800; no horizontal scroll at 390px.

### 2a. Tagline options (Don picks one; mockup uses option A)
- A. "I build games that make learning feel like play."
- B. "Bringing the thunder to games that teach."
- C. "Code, games, and a little lightning."

## 3. Games showcase (`#games`)
Section heading "Games", intro "Everything here runs in the browser — no installs, no accounts."
Four groups, each an `<section>` with an `<h3>` group title and a short description, then a responsive card grid.

Card (primitive `.card`): thumbnail (`assets/games/<slug>.webp`, 640×400, `loading="lazy"`, `width`/`height` set, meaningful alt "Screenshot of <title>"), title (`<h4>`), one-liner, tag chips (`.tag`), and an action button. The whole card lifts and glows on hover/focus-within; only the button is the link (no nested links).

| Group | Slug | Title | One-liner | Tags | Action |
|---|---|---|---|---|---|
| Learning games | geo-conquest | Geo Conquest | Conquer the world one question at a time: 1,100+ geography questions, grade 7 math with step-by-step hints, and local multiplayer for up to 4. | Geography, Math, Multiplayer | Play → https://conquest.inguyen.ca/ (card is `.card--featured`, spans 2 columns on desktop) |
| Learning games | geo-quest-adeline | Geo Quest: Adeline | Ages 9–10: continents, oceans, Canada and map skills. Calm, no timers. | Geography, Ages 9–10 | Play → https://games.inguyen.ca/geo-quest-adeline.html |
| Learning games | geo-quest-remy | Geo Quest: Remy | Ages 11–12: capitals, landforms, rivers and map skills. | Geography, Ages 11–12 | Play → https://games.inguyen.ca/geo-quest-remy.html |
| Learning games | geo-quest-seline | Geo Quest: Seline | Ages 14–15: tectonics, biomes, climate and oceans. | Geography, Ages 14–15 | Play → https://games.inguyen.ca/geo-quest-seline.html |
| Learning games | slice-and-solve | Slice & Solve | Fractions practice: adding and subtracting. Calm, no timers. | Math, Fractions | Play → https://games.inguyen.ca/slice-and-solve.html |
| Learning games | flip-and-solve | Flip & Solve | Fractions practice: multiplying and dividing. Calm, no timers. | Math, Fractions | Play → https://games.inguyen.ca/flip-and-solve.html |
| Just for fun | lucky-grid | Lucky Grid | Pick a square and test your luck in this grid-based game of chance. | Luck, Party | Play → https://games.inguyen.ca/luckygrid.html |
| Adults only (18+) | deal-or-no-drink | Deal or No Drink | A party game for grown-ups. Please drink responsibly. | 18+, Party | Play → https://games.inguyen.ca/newgame/ |
| Coming soon | fantasyquest | FantasyQuest | A 2D RPG paying homage to Dragon Warrior. In development. | RPG, In progress | "View on GitHub" → https://github.com/hanoisolo/FantasyQuest |

- Group descriptions: Learning — "Geography and math games built for kids, with hints instead of timers."; Just for fun — "Quick games for game night."; Adults — "Party games for players 18 and over."; Coming soon — "Work in progress."
- The 18+ group has a visible amber "18+" badge on the group title and on the card, and its heading text says "Adults only (18+)". The card thumbnail is not blurred.
- Coming-soon card has a "Coming soon" ribbon/badge and a muted look; its button is secondary style.
- Links to *.inguyen.ca open in the same tab; GitHub links open in a new tab with rel="noopener".
- Grid: 3 columns ≥ 1024px, 2 columns ≥ 640px, 1 column below.
- Acceptance: 9 cards; every thumbnail file exists; every card has title, one-liner, ≥1 tag, exactly one action link.

## 4. GitHub projects (`#projects`)  — segment 2
Heading "Projects", intro "The code behind it all, on GitHub." Cards (`.card--repo`, no thumbnail): repo name, description, language chip, "View repo" link (new tab).
- geo-conquest — "Geo Conquest: a browser geography conquest quiz (vanilla JS, Natural Earth map)." JavaScript
- my-games — "The Games Hub at games.inguyen.ca: small learning and party games." HTML
- FantasyQuest — "2D RPG homage to Dragon Warrior (in progress)." JavaScript
- inguyen-site — "This site." HTML/CSS (add once the repo exists)
- Footer link "All repos on GitHub →" https://github.com/hanoisolo?tab=repositories
- Static content (no GitHub API calls at runtime).

## 5. About / links (`#about`) — segment 2
Short bio paragraph (placeholder until Don supplies text: "I'm Don, a Toronto-based builder who makes browser games — mostly learning games my kids actually want to play."), then three icon-buttons with inline SVG icons and text labels: GitHub (github.com/hanoisolo), X (x.com/hanoi_solo), LinkedIn (linkedin.com/in/don-nguyen). New tab, rel="noopener me". No email, no form.

## 6. Footer — segment 2
"© <current year> Don Nguyen · inguyen.ca" (year filled by JS with a static fallback), repeated small social links, and "Back to top" link.

## 7. SEO and social meta — segment 3 (hero segment adds the basics)
- `<title>` "Don Nguyen — Games & Projects", meta description, `<link rel="canonical" href="https://www.inguyen.ca/">`, `lang="en-CA"`, theme-color `#05080f`.
- Open Graph + Twitter card: og:title, og:description, og:url, og:type=website, og:image https://www.inguyen.ca/assets/img/og.jpg (1200×630), twitter:card=summary_large_image, twitter:site @hanoi_solo.
- JSON-LD `Person` (name, url, sameAs: the 3 profile URLs).
- Favicons: `assets/img/favicon-32.png`, `apple-touch-icon.png`. `robots.txt`, `sitemap.xml`, `404.html` (styled, link home).

## 8. Accessibility — all segments
- WCAG AA contrast for text on the dark theme; visible `:focus-visible` ring (cyan, 2px offset).
- Landmarks: header, nav (aria-label "Primary"), main, footer. Logical heading order h1 → h2 → h3 → h4.
- All motion (glow pulse, lightning flicker, card lift transitions, smooth scroll) disabled under `prefers-reduced-motion: reduce`.
- Decorative graphics `aria-hidden="true"`; external links say so for screen readers ("(opens in new tab)" visually hidden text).
- Works without JavaScript (JS only adds header scroll state, year, and non-essential effects).

## 9. Responsive and performance — all segments
- Tested at 390×844, 768×1024, 1280×800, 1440×900. No horizontal scroll anywhere.
- No frameworks, no CDNs, no web fonts (system font stack). Total page weight target < 600 KB on first load at 390px.
- Images: webp with jpg fallback for the portrait; thumbnails lazy-loaded.
