# Segments

| # | Segment | Spec | Status |
|---|---|---|---|
| 0 | Blueprint docs, assets (portrait sizes, OG image, favicons, game thumbnails), CNAME, test gate | — | done (Forge) |
| 1 | Design system (tokens.css, components.css) + header + hero + games showcase | §1, §2, §3, §8, §9 | done (mockup; awaiting Don review) |
| 2 | Projects + About/links + footer | §4, §5, §6 | done |
| 3 | SEO/OG/JSON-LD, robots.txt, sitemap.xml, 404.html | §7 | done |
| 4 | Hardening: link check, contrast/a11y audit, mobile pass, Lighthouse-style perf check, copy review with Don | §8, §9 | done (Don to eyeball final screenshots) |
| 5 | Launch (with Don's OK; steps in docs/launch.md): create GitHub repo hanoisolo/inguyen-site, push, enable Pages + custom domain, DNS at Squarespace (www CNAME → hanoisolo.github.io; apex A → GitHub IPs; Pages TXT verification), verify https://www.inguyen.ca and https://inguyen.ca | — | todo |
| 6 | portfolio.inguyen.ca: redirect to www (or remove the Vercel domain) once www is live — decide with Don | — | todo |
| side | my-games hub: add a Geo Conquest card to hanoisolo/my-games index.html in the existing `.game-card` style (separate repo, separate approval) | — | committed locally on branch add-geo-conquest-card in /workspace/my-games (cc37b17); not pushed |

## Side task plan: Geo Conquest card on games.inguyen.ca
1. `git -C /workspace/my-games pull` (or clone). 2. Add one `.game-card` inside `.game-grid` (last position: `.game-card:nth-child(1)`/`(2)` CSS assigns the Lucky Grid / Drinking Game images by position, so inserting first would swap them), copying the README template: onclick/href `https://conquest.inguyen.ca/`, emoji 🗺️, gradient `linear-gradient(135deg,#1e3a8a,#0ea5e9)`, title "Geo Conquest", description "Conquer the world: geography & math quiz, up to 4 players." 3. Optionally bump footer © to 2026 (ask Don). 4. Local http.server + screenshot. 5. Commit, show Don, push only after approval, verify live.
