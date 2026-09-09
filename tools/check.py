# -*- coding: utf-8 -*-
"""Confere links internos, assets orfaos, titles/descriptions duplicados e h1.

    python tools/check.py
"""
import os, re, io, glob, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PAGES = (['index.html', 'garantia.html', 'representantes.html']
         + sorted(glob.glob('colchoes/*.html'))
         + sorted(glob.glob('bases/*.html'))
         + sorted(glob.glob('travesseiros/*.html')))

missing, refs = set(), set()
titles, descs, h1s = collections.Counter(), collections.Counter(), {}

for pg in PAGES:
    base = os.path.dirname(pg)
    s = io.open(pg, encoding='utf-8').read()
    for m in re.finditer(r'(?:src|href)="([^"#][^"]*)"', s):
        u = m.group(1)
        if u.startswith(('http', 'mailto:', 'tel:', 'data:', '/')):
            continue
        t = os.path.normpath(os.path.join(base, u.split('#')[0]))
        if not t or t == '.':
            continue
        refs.add(t.replace(os.sep, '/'))
        if not os.path.exists(t):
            missing.add((pg, u))
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    d = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
    if t: titles[t.group(1).strip()] += 1
    if d: descs[d.group(1).strip()] += 1
    h1s[pg] = len(re.findall(r'<h1[\s>]', s))

print(f'páginas: {len(PAGES)}   referências locais: {len(refs)}')
print('\n== links e assets ==')
if missing:
    for p, u in sorted(missing):
        print(f'  QUEBRADO  {p} -> {u}')
else:
    print('  nenhum quebrado')

assets = {f.replace(os.sep, '/') for f in glob.glob('assets/**/*', recursive=True)
          if os.path.isfile(f)}
assets |= {f for f in ('favicon.svg', 'favicon.ico', 'site.webmanifest') if os.path.exists(f)}
orfaos = sorted(a for a in assets if a not in refs)
print(f'\n== assets não referenciados ({len(orfaos)}) ==')
for a in orfaos:
    print(f'  {a}  {os.path.getsize(a)//1024}KB')

linked = {r for r in refs if r.endswith('.html')}
todas = {p.replace(os.sep, '/') for p in glob.glob('*.html') + glob.glob('*/*.html')}
todas -= {p.replace(os.sep, '/') for p in glob.glob('_arquivo/**/*.html', recursive=True)}
orfa = sorted(todas - linked - {'index.html'})
print(f'\n== páginas não linkadas ({len(orfa)}) ==')
for p in orfa:
    print(f'  {p}')

print('\n== SEO ==')
dup_t = [t for t, n in titles.items() if n > 1]
dup_d = [d for d, n in descs.items() if n > 1]
print(f'  titles duplicados: {len(dup_t)}')
for t in dup_t: print(f'    {t}')
print(f'  descriptions duplicadas: {len(dup_d)}')
for d in dup_d: print(f'    {d[:80]}')
bad_h1 = {p: n for p, n in h1s.items() if n != 1}
print(f'  páginas sem exatamente um h1: {len(bad_h1)}')
for p, n in bad_h1.items(): print(f'    {p}: {n}')
