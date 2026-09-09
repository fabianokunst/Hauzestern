# -*- coding: utf-8 -*-
"""
Gera o site inteiro: home, produtos, garantia, representantes, sitemap.

    python tools/build_all.py

As imagens sao preparadas separadamente (roda so quando o guide muda):

    python tools/build_assets.py
"""
import os, sys, io, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

import dados
import build_pages as BP
import build_home
import build_garantia
import build_representantes

HOJE = datetime.date.today().isoformat()


def sitemap():
    urls = [('', '1.0'), ('representantes.html', '0.8'), ('garantia.html', '0.8')]
    urls += [(f'colchoes/{m["slug"]}.html', '0.9') for m in dados.COLCHOES]
    urls += [(f'bases/{b["slug"]}.html', '0.7') for b in dados.BASES]
    urls += [(f'travesseiros/{t["slug"]}.html', '0.7') for t in dados.TRAVESSEIROS]
    body = '\n'.join(
        f'  <url>\n    <loc>{BP.SITE}/{u}</loc>\n'
        f'    <lastmod>{HOJE}</lastmod>\n'
        f'    <priority>{pr}</priority>\n  </url>' for u, pr in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemap' + 's.org/schemas/sitemap/0.9">\n'
            + body + '\n</urlset>\n')


if __name__ == '__main__':
    print('— home —')
    print('  index.html %dKB' % (BP.write('index.html', build_home.build()) // 1024))

    print('— garantia —')
    print('  garantia.html %dKB' % (BP.write('garantia.html', build_garantia.build()) // 1024))

    print('— representantes —')
    print('  representantes.html %dKB'
          % (BP.write('representantes.html', build_representantes.build()) // 1024))
    for a in sorted(set(build_representantes.DR.AVISOS)):
        print('  aviso: ' + a)

    print('— colchões —')
    for m in dados.COLCHOES:
        BP.write(f'colchoes/{m["slug"]}.html', BP.pdp_colchao(m, dados.COLCHOES))
    print(f'  {len(dados.COLCHOES)} páginas')

    print('— bases —')
    for b in dados.BASES:
        BP.write(f'bases/{b["slug"]}.html', BP.pdp_base(b, dados.BASES))
    print(f'  {len(dados.BASES)} páginas')

    print('— travesseiros —')
    for t in dados.TRAVESSEIROS:
        BP.write(f'travesseiros/{t["slug"]}.html', BP.pdp_travesseiro(t, dados.TRAVESSEIROS))
    print(f'  {len(dados.TRAVESSEIROS)} páginas')

    print('— sitemap —')
    n = 3 + len(dados.COLCHOES) + len(dados.BASES) + len(dados.TRAVESSEIROS)
    BP.write('sitemap.xml', sitemap())
    print(f'  sitemap.xml — {n} URLs')

    print('\nsite gerado.')
