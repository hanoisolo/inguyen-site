# Launch checklist (do NOT run without Don's explicit OK)

Pre-flight (local)
1. `python3 -m unittest tests.test_site.Seg4` → OK (gates + axe + tap targets + overflow + reduced motion).
2. `git status` clean on `main`; `CNAME` = `www.inguyen.ca`; `.nojekyll` present.

GitHub (needs Don's OK — creates a public repo and pushes)
3. `gh repo create hanoisolo/inguyen-site --public --source /workspace/inguyen-site --remote origin --description "Don Nguyen — games & projects (www.inguyen.ca)" --homepage https://www.inguyen.ca`
4. `git -C /workspace/inguyen-site push -u origin main` (once; never force).
5. Enable Pages from main, root: `gh api -X POST repos/hanoisolo/inguyen-site/pages -f 'source[branch]=main' -f 'source[path]=/'`
   then set the domain: `gh api -X PUT repos/hanoisolo/inguyen-site/pages -f cname=www.inguyen.ca`
6. Recommended: verify the domain for the account (GitHub → Settings → Pages → Verified domains → add inguyen.ca) to get the TXT record value.

DNS at Squarespace (Domains → inguyen.ca → DNS; needs Don's OK)
7. `www` CNAME: `ghs.googlehosted.com` → `hanoisolo.github.io`
8. Apex `@`: turn off Squarespace domain forwarding; delete A `198.49.23.144`; add A `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (optional AAAA `2606:50c0:8000::153` … `8003::153`).
9. TXT `_github-pages-challenge-hanoisolo` = value from step 6.
   Leave untouched: `games` and `conquest` (CNAME hanoisolo.github.io), `portfolio` (Vercel CNAME). No MX exists, so mail is unaffected.

Verify
10. `gh api repos/hanoisolo/inguyen-site/pages --jq '.status,.https_certificate.state'` → built / approved (cert can take up to ~1 h after DNS resolves); then enforce HTTPS: `gh api -X PUT repos/hanoisolo/inguyen-site/pages -F https_enforced=true`.
11. `curl -sI https://www.inguyen.ca` → 200 `server: GitHub.com`; `curl -sI https://inguyen.ca` → 301 to https://www.inguyen.ca/; `/nope` → 404 page; og.jpg, robots.txt, sitemap.xml → 200.
12. Headless screenshot of the live site at 1280 and 390; share with Don.

After launch
13. Add the `inguyen-site` repo card to #projects (spec §4).
14. Segment 6: decide portfolio.inguyen.ca (redirect to www vs remove the domain from Vercel project k3-portfolio).
15. Optional: remove the custom URL mapping in the old Google Sites settings.
