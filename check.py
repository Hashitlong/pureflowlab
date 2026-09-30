#!/usr/bin/env python3
"""PureFlow Lab pre-commit audit. Run from the site folder:  python3 check.py
Exits non-zero if any check fails. The HTML files in this folder ARE the source of truth."""
import re, glob, os, json, sys, html
from html.parser import HTMLParser

TAG = 'pureflowlab-20'
BANNED = [r'\bwe tested\b', r'\bour testing\b', r'\bhands-on\b', r'\bI tested\b', r'PureFlow Lab Team',
          r'\$\d', r'\bstars\b', r'best-in-class', r'\[NEWTAG\]', r'DRAFT NOTES', r'we should test']
VOID = {'br', 'img', 'meta', 'link', 'hr', 'input', 'source', 'path', 'stop', 'circle', 'rect', 'line', 'area', 'base', 'col', 'embed', 'wbr'}
errors = []

class Bal(HTMLParser):
    def __init__(s): super().__init__(); s.st = []; s.bad = []
    def handle_starttag(s, t, a):
        if t not in VOID: s.st.append(t)
    def handle_endtag(s, t):
        if t in VOID: return
        if s.st and s.st[-1] == t: s.st.pop()
        else: s.bad.append(t)

pages = sorted(f for f in glob.glob('*.html') if not f.startswith('google'))
sitemap = open('sitemap.xml').read() if os.path.exists('sitemap.xml') else ''
for f in pages:
    t = open(f).read()
    b = Bal(); b.feed(t)
    if b.bad or b.st: errors.append(f'{f}: unbalanced HTML {b.bad[:3]} {b.st[-3:]}')
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try: json.loads(m.group(1))
        except Exception as e: errors.append(f'{f}: invalid JSON-LD ({e})')
    for m in re.finditer(r'(?:src|href)="((?!https?:|#|mailto:|/)[^"#?]+)', t):
        if not os.path.exists(m.group(1)): errors.append(f'{f}: missing local file {m.group(1)}')
    for u in re.findall(r'href="(https://www\.amazon\.com[^"]*)"', t):
        if f'tag={TAG}' not in u: errors.append(f'{f}: Amazon link without tag: {u[:80]}')
    for m in re.finditer(r'<a [^>]*href="https://www\.amazon\.com[^"]*"[^>]*>', t):
        if 'sponsored' not in m.group(0): errors.append(f'{f}: Amazon link missing rel=sponsored')
    title = re.search(r'<title>(.*?)</title>', t, re.S)
    if not title: errors.append(f'{f}: no <title>')
    elif len(html.unescape(title.group(1))) > 65: errors.append(f'{f}: title {len(html.unescape(title.group(1)))} chars (>65)')
    if 'rel="canonical"' not in t: errors.append(f'{f}: no canonical')
    if f not in ('404.html',) and f'pureflowlab.com/{f}' not in sitemap and not (f == 'index.html' and 'pureflowlab.com/<' in sitemap):
        errors.append(f'{f}: not in sitemap.xml')
    vis = re.sub(r'<script.*?</script>|<style.*?</style>|<head>.*?</head>', '', t, flags=re.S)
    vis = html.unescape(re.sub(r'<[^>]+>', ' ', vis))
    if f != 'privacy.html':
        for p in BANNED:
            if re.search(p, vis, re.I): errors.append(f'{f}: banned phrase /{p}/')
for loc in re.findall(r'<loc>https://pureflowlab\.com/([^<]*)</loc>', sitemap):
    if loc and not os.path.exists(loc): errors.append(f'sitemap lists missing page {loc}')

if errors:
    print(f'FAIL: {len(errors)} problem(s)'); [print(' -', e) for e in errors]; sys.exit(1)
print(f'OK: {len(pages)} pages passed (tags, rel, links, JSON-LD, HTML balance, titles, canonicals, sitemap, banned phrases)')
