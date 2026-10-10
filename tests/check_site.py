#!/usr/bin/env python3
"""Forge gate for inguyen-site. Usage: check_site.py ds|seg1"""
import sys, os, re, subprocess
from html.parser import HTMLParser
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def need(c, msg):
    if not c: fails.append(msg)
def read(p):
    p = os.path.join(ROOT, p); return open(p, encoding='utf8').read() if os.path.exists(p) else ''

def check_ds():
    t = read('assets/css/tokens.css'); c = read('assets/css/components.css')
    need(t, 'tokens.css missing'); need(c, 'components.css missing')
    for v in ['--bg','--bg-2','--surface','--surface-2','--border','--border-strong','--text','--text-muted','--text-dim','--accent','--accent-2','--accent-ink','--glow','--glow-strong','--warn','--font-sans','--fs-hero','--sp-4','--sp-24','--r-md','--r-pill','--container','--ease','--dur']:
        need(re.search(re.escape(v)+r'\s*:', t), f'tokens.css lacks {v}')
    need('#05080f' in t.lower() and '#38bdf8' in t.lower(), 'tokens.css palette values missing')
    for cls in ['.container','.section','.section-head','.eyebrow','.btn','.btn--primary','.btn--ghost','.tag','.badge','.badge--warn','.badge--soon','.card','.card__media','.card__body','.card__title','.card__text','.card__tags','.card__actions','.card--featured','.card--soon','.card--repo','.grid','.visually-hidden','.skip-link',':focus-visible']:
        need(cls in c, f'components.css lacks {cls}')
    need('prefers-reduced-motion' in c, 'components.css lacks reduced-motion block')
    need(not re.search(r'@import|https?://', t + c), 'CSS must not import/load external URLs')
    for f,s in (('tokens.css',t),('components.css',c)):
        need(s.count('{') == s.count('}'), f'{f} unbalanced braces')

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.tags=[]; s.stack=[]; s.a_depth=0; s.nested=False
    def handle_starttag(s, tag, a):
        a = dict(a); s.tags.append((tag, a))
        if tag == 'a':
            if s.a_depth: s.nested = True
            s.a_depth += 1
    def handle_endtag(s, tag):
        if tag == 'a': s.a_depth = max(0, s.a_depth-1)

def check_seg1():
    check_ds()
    h = read('index.html'); need(h, 'index.html missing')
    sec = read('assets/css/sections.css'); js = read('assets/js/main.js')
    need(sec, 'sections.css missing'); need(js, 'main.js missing')
    need('prefers-reduced-motion' in sec, 'sections.css lacks reduced-motion block')
    p = P(); p.feed(h); tags = p.tags
    need(not p.nested, 'nested <a> found')
    need(len([1 for t,_ in tags if t=='h1'])==1, 'need exactly one h1')
    need(re.search(r'<html[^>]*lang="en-CA"', h), 'html lang en-CA')
    need('<meta name="viewport"' in h, 'viewport meta'); need('name="description"' in h, 'meta description')
    need(re.search(r'<title>Don Nguyen', h), 'title')
    css = [a.get('href') for t,a in tags if t=='link' and a.get('rel')=='stylesheet']
    need(css == ['assets/css/tokens.css','assets/css/components.css','assets/css/sections.css'], f'css order {css}')
    need(any(t=='script' and a.get('src')=='assets/js/main.js' and 'defer' in a for t,a in tags), 'main.js defer')
    need(not any((t=='script' and (a.get('src') or '').startswith('http')) or (t=='link' and a.get('rel') in ('stylesheet','preload','modulepreload') and (a.get('href') or '').startswith('http')) for t,a in tags), 'no external scripts/styles')
    need(any(t=='link' and a.get('rel')=='canonical' and a.get('href')=='https://www.inguyen.ca/' for t,a in tags), 'canonical link')
    ids = {a.get('id') for t,a in tags}
    for i in ['top','main','games']: need(i in ids, f'id #{i} missing')
    need(any(t=='a' and 'skip-link' in (a.get('class') or '') and a.get('href')=='#main' for t,a in tags), 'skip link')
    need(any(t=='nav' and a.get('aria-label')=='Primary' for t,a in tags), 'nav aria-label Primary')
    need('Don Nguyen' in h, 'name'); need('I build games that make learning feel like play.' in h, 'tagline A')
    need(any(t=='source' and 'don-480.webp' in (a.get('srcset') or '') and 'don-800.webp' in (a.get('srcset') or '') for t,a in tags), 'portrait webp srcset')
    need(any(t=='img' and 'don-' in (a.get('src') or '') and a.get('src','').endswith('.jpg') and a.get('alt') and a.get('width') and a.get('height') for t,a in tags), 'portrait img jpg fallback with alt/size')
    for t,a in tags:
        if t=='img':
            need(a.get('alt') is not None, f'img without alt {a.get("src")}')
            s = a.get('src','')
            if s and not s.startswith('http'): need(os.path.exists(os.path.join(ROOT,s)), f'missing image {s}')
    slugs = ['geo-conquest','geo-quest-adeline','geo-quest-remy','geo-quest-seline','slice-and-solve','flip-and-solve','lucky-grid','deal-or-no-drink','fantasyquest']
    for s in slugs:
        need(any(t=='img' and a.get('src')==f'assets/games/{s}.webp' and a.get('loading')=='lazy' and a.get('width')=='640' and a.get('height')=='400' for t,a in tags), f'thumbnail img for {s}')
    hrefs = [a.get('href') for t,a in tags if t=='a']
    for u in ['https://conquest.inguyen.ca/','https://games.inguyen.ca/geo-quest-adeline.html','https://games.inguyen.ca/geo-quest-remy.html','https://games.inguyen.ca/geo-quest-seline.html','https://games.inguyen.ca/slice-and-solve.html','https://games.inguyen.ca/flip-and-solve.html','https://games.inguyen.ca/luckygrid.html','https://games.inguyen.ca/newgame/','https://github.com/hanoisolo/FantasyQuest','https://github.com/hanoisolo']:
        need(u in hrefs, f'link {u}')
    for t,a in tags:
        if t=='a' and (a.get('href') or '').startswith('https://github.com'):
            need(a.get('target')=='_blank' and 'noopener' in (a.get('rel') or ''), f'github link needs target/rel {a.get("href")}')
    cards = [a for t,a in tags if t in ('article','li','div') and re.search(r'(^|\s)card(\s|$)', a.get('class') or '') and 'card--repo' not in (a.get('class') or '')]
    need(len(cards)==9, f'expected 9 .card elements, got {len(cards)}')
    for g in ['Learning games','Just for fun','Adults only (18+)','Coming soon']: need(g in h, f'group heading {g}')
    need('card--featured' in h and 'card--soon' in h and 'badge--warn' in h, 'featured/soon/warn modifiers')
    need('aria-hidden="true"' in h, 'decorative aria-hidden')
    r = subprocess.run(['node','--check',os.path.join(ROOT,'assets/js/main.js')],capture_output=True,text=True)
    need(r.returncode==0, 'main.js syntax: '+r.stderr.strip()[:200])
    need('matchMedia' in js and 'prefers-reduced-motion' in js, 'main.js must respect reduced motion')


def section_html(h, sid):
    m = re.search(r'<section[^>]*id="%s"(.*?)</section>\s*(?=<section|</main>)' % sid, h, re.S)
    return m.group(0) if m else ''

def check_seg2():
    check_seg1()
    h = read('index.html'); p = P(); p.feed(h); tags = p.tags
    pr = section_html(h, 'projects'); ab = section_html(h, 'about')
    need(pr, '#projects section missing'); need(ab, '#about section missing')
    need('Coming in the next update' not in h, 'placeholder text still present')
    for r in ['geo-conquest','my-games','FantasyQuest']:
        need(f'https://github.com/hanoisolo/{r}' in pr, f'projects: repo link {r}')
    need(pr.count('card--repo') == 3, f'projects: expected 3 .card--repo, got {pr.count("card--repo")}')
    need('k3-portfolio' not in h, 'k3-portfolio must not appear')
    need('https://github.com/hanoisolo?tab=repositories' in pr, 'projects: all repos link')
    for lang in ['JavaScript','HTML']: need(lang in pr, f'projects: language {lang}')
    need("I'm Don, a Toronto-based builder who makes browser games — mostly learning games my kids actually want to play." in ab.replace('&rsquo;',"'").replace('’',"'"), 'about: bio text')
    for u in ['https://github.com/hanoisolo','https://x.com/hanoi_solo','https://www.linkedin.com/in/don-nguyen/']:
        need(u in ab, f'about: link {u}')
    for t,a in tags:
        href = a.get('href') or ''
        if t=='a' and any(href.startswith(x) for x in ('https://x.com','https://www.linkedin.com','https://github.com')):
            need(a.get('target')=='_blank' and 'noopener' in (a.get('rel') or ''), f'external link target/rel {href}')
    need(ab.count('<svg') >= 3, 'about: 3 inline svg icons')
    need('mailto:' not in h and '<form' not in h, 'no email/form')
    f = re.search(r'<footer.*?</footer>', h, re.S); f = f.group(0) if f else ''
    need('data-year' in f and 'Don Nguyen' in f and 'inguyen.ca' in f, 'footer: year, name, inguyen.ca')
    need('href="#top"' in f, 'footer: back to top')
    need(f.count('<a') >= 4, 'footer: social links + back to top')

mode = sys.argv[1] if len(sys.argv)>1 else 'seg1'
{'ds':check_ds,'seg1':check_seg1,'seg2':check_seg2}[mode]()
if fails:
    print('FAIL ('+str(len(fails))+'):'); [print(' - '+f) for f in fails[:25]]; sys.exit(1)
print('PASS', mode)
