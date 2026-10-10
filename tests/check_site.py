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

def check_seg3():
    check_seg2()
    import json
    h = read('index.html'); p = P(); p.feed(h); tags = p.tags
    metas = {}
    for t,a in tags:
        if t=='meta':
            k = a.get('property') or a.get('name')
            if k: metas[k] = a.get('content')
    want = {'og:title':None,'og:description':None,'og:url':'https://www.inguyen.ca/','og:type':'website','og:image':'https://www.inguyen.ca/assets/img/og.jpg','og:image:width':'1200','og:image:height':'630','og:image:alt':None,'og:site_name':None,'og:locale':'en_CA','twitter:card':'summary_large_image','twitter:site':'@hanoi_solo','twitter:title':None,'twitter:description':None,'twitter:image':'https://www.inguyen.ca/assets/img/og.jpg'}
    for k,v in want.items():
        need(k in metas and metas[k], f'meta {k} missing')
        if v and k in metas: need(metas[k]==v, f'meta {k} should be {v}, got {metas[k]}')
    d = metas.get('description') or ''
    need(50 <= len(d) <= 160, f'meta description length {len(d)} not 50-160')
    m = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    need(len(m)==1, 'exactly one JSON-LD block')
    if m:
        try:
            j = json.loads(m[0])
            need(j.get('@context')=='https://schema.org' and j.get('@type')=='Person', 'JSON-LD Person/@context')
            need(j.get('name')=='Don Nguyen' and j.get('url')=='https://www.inguyen.ca/', 'JSON-LD name/url')
            need(set(j.get('sameAs') or [])=={'https://github.com/hanoisolo','https://x.com/hanoi_solo','https://www.linkedin.com/in/don-nguyen/'}, 'JSON-LD sameAs')
            need((j.get('image') or '').startswith('https://www.inguyen.ca/assets/img/'), 'JSON-LD image')
        except Exception as e: need(False, f'JSON-LD invalid: {e}')
    r = read('robots.txt')
    need('User-agent: *' in r and 'Allow: /' in r and 'Sitemap: https://www.inguyen.ca/sitemap.xml' in r, 'robots.txt content')
    sm = read('sitemap.xml')
    need(sm.startswith('<?xml') and 'http://www.sitemaps.org/schemas/sitemap/0.9' in sm and '<loc>https://www.inguyen.ca/</loc>' in sm, 'sitemap.xml')
    need('404.html' not in sm, 'sitemap must not list 404')
    f = read('404.html'); need(f, '404.html missing')
    if f:
        q = P(); q.feed(f); ft = q.tags
        need(re.search(r'<html[^>]*lang="en-CA"', f), '404 lang')
        css = [a.get('href') for t,a in ft if t=='link' and a.get('rel')=='stylesheet']
        need(css == ['/assets/css/tokens.css','/assets/css/components.css','/assets/css/sections.css'], f'404 css must be root-absolute in order, got {css}')
        need(any(t=='meta' and a.get('name')=='robots' and 'noindex' in (a.get('content') or '') for t,a in ft), '404 noindex')
        need(len([1 for t,_ in ft if t=='h1'])==1, '404 one h1')
        need(any(t=='a' and a.get('href')=='/' for t,a in ft), '404 link home "/"')
        need(any(t=='a' and a.get('href')=='/#games' for t,a in ft), '404 link /#games')
        need('Page not found' in f, '404 text')
        for t,a in ft:
            for k in ('href','src','srcset'):
                v = a.get(k) or ''
                if v and not v.startswith(('/','http','#','mailto')) and t in ('link','script','img','source','a'):
                    need(False, f'404 relative URL {v} (use root-absolute)')
        need(not re.search(r'https?://(?!www\.inguyen\.ca|github\.com|x\.com|www\.linkedin\.com)', f), '404 external URL')

def hexrgb(x):
    x = x.strip().lstrip('#'); return tuple(int(x[i:i+2],16)/255 for i in (0,2,4))
def lum(c):
    f = lambda v: v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4
    r,g,b = map(f, c); return 0.2126*r + 0.7152*g + 0.0722*b
def contrast(a, b):
    la, lb = sorted((lum(hexrgb(a)), lum(hexrgb(b))), reverse=True); return (la+0.05)/(lb+0.05)

def check_seg4():
    check_seg3()
    t = read('assets/css/tokens.css')
    tok = dict(re.findall(r'(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{6})', t))
    pairs = [('--text','--bg'),('--text','--surface'),('--text-muted','--bg'),('--text-muted','--surface'),('--text-dim','--bg'),('--text-dim','--surface'),('--accent','--bg'),('--accent','--surface'),('--accent-2','--surface'),('--accent-ink','--accent'),('--warn','--surface'),('--muted-badge','--surface')]
    for a,b in pairs:
        if a in tok and b in tok:
            c = contrast(tok[a], tok[b]); need(c >= 4.5, f'contrast {a} on {b} = {c:.2f} < 4.5')
        else: need(False, f'token {a} or {b} not a 6-digit hex')
    r = subprocess.run(['node', os.path.join(ROOT,'tests','browser_audit.js')], capture_output=True, text=True, timeout=300)
    need(r.returncode == 0, 'browser audit: ' + (r.stdout.strip().splitlines() or ['no output'])[-1][:400])

mode = sys.argv[1] if len(sys.argv)>1 else 'seg1'
{'ds':check_ds,'seg1':check_seg1,'seg2':check_seg2,'seg3':check_seg3,'seg4':check_seg4}[mode]()
if fails:
    print('FAIL ('+str(len(fails))+'):'); [print(' - '+f) for f in fails[:25]]; sys.exit(1)
print('PASS', mode)
