# -*- coding: utf-8 -*-
"""
Prepara os assets do site a partir de guide_hauzestern/.

Uso:  python tools/build_assets.py
Roda uma vez, quando as imagens do guide mudarem. O site em si é estático:
nada disto executa em runtime.

Gera:
  assets/produtos/*                   ver tools/variantes.py (3 variantes)
  assets/travesseiros/<slug>.jpg       960x720 / 480x360-card
  assets/bases/<slug>.jpg             1400x1050 / 640x480-card
  assets/camadas/<slug>.webp           altura 900, fundo transparente
  assets/processo/<n>.jpg             1200x800   (fábrica, seção "processo")
  assets/lifestyle/*.jpg
"""
import os, sys, glob
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
Image.MAX_IMAGE_PIXELS = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, 'guide_hauzestern')


def out(*p):
    d = os.path.join(ROOT, *p)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    return d


def src(*p):
    return os.path.join(G, *p)


def fit(path, dest, w, h, q=80, mode='cover'):
    """Redimensiona para wxh. 'cover' recorta pelo centro; 'contain' encaixa."""
    im = Image.open(path)
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg
    im = im.convert('RGB')
    sw, sh = im.size
    if mode == 'cover':
        k = max(w / sw, h / sh)
        nw, nh = round(sw * k), round(sh * k)
        im = im.resize((nw, nh), Image.LANCZOS)
        im = im.crop(((nw - w) // 2, (nh - h) // 2, (nw - w) // 2 + w, (nh - h) // 2 + h))
    else:
        im.thumbnail((w, h), Image.LANCZOS)
    im.save(dest, 'JPEG', quality=q, optimize=True, progressive=True)
    return im.size


# ---------------------------------------------------------------- colchões
# As fotos de colchao tem TRES variantes (branco / ambiente / cinza) e algumas
# precisam de troca de fundo. Isso vive em tools/variantes.py, que e a unica
# fonte de assets/produtos/. Rode:  python tools/variantes.py
print('— colchões —')
print('  fora deste script: python tools/variantes.py')

# ------------------------------------------------------------ travesseiros
# O guide não tem fotografia por modelo de travesseiro: são 3 fotos genéricas
# em alta. Alpen/Harz/Weich recebem uma cada; MH7618/MH7619 seguem com a
# imagem antiga até a marca enviar as fotos dos moldados.
TRAVESSEIROS = {
    'alpen': 'Produtos/_TRAVESSEIROS/2D3A6878.jpg',
    'harz':  'Produtos/_TRAVESSEIROS/2D3A6896.jpg',
    'weich': 'Produtos/_TRAVESSEIROS/2D3A6886.jpg',
}
print('— travesseiros —')
for slug, rel in TRAVESSEIROS.items():
    p = src(*rel.split('/'))
    if not os.path.exists(p):
        print(f'  !! ausente: {rel}')
        continue
    fit(p, out('assets', 'travesseiros', slug + '.jpg'), 960, 720, 82)
    fit(p, out('assets', 'travesseiros', slug + '-card.jpg'), 480, 360, 80)
    print(f'  {slug:8s} ok')

# ----------------------------------------------------------------- bases
# Fonte: Produtos/_BOXES/. C1836 nao tem foto no guide.
BASES = {
    'box-root':  'Produtos/_BOXES/box root 01 - quadro pequeno.jpg',
    'box-c1674': 'Produtos/_BOXES/BOX C1674 - QUADRO PEQUENO.jpg',
    'box-c1705': 'Produtos/_BOXES/BOX C1705 - QUADRO PEQUENO.jpg',
    'box-c1706': 'Produtos/_BOXES/BOX C1706 - QUADRO PEQUENO.jpg',
    'box-favo':  'Produtos/_BOXES/BOX FAVO - QUADRO PEQUENO.jpg',
}
print('— bases —')
for slug, rel in BASES.items():
    p = src(*rel.split('/'))
    if not os.path.exists(p):
        print(f'  !! ausente: {rel}')
        continue
    fit(p, out('assets', 'bases', slug + '.jpg'), 1400, 1050, 80)
    fit(p, out('assets', 'bases', slug + '-card.jpg'), 640, 480, 78)
    print(f'  {slug:11s} ok')

# --------------------------------------------------------------- camadas
print('— camadas —')
CAM = os.path.join(G, 'Produtos', '_Imagens das camadas dos colchões', 'PNG')
for f in sorted(glob.glob(os.path.join(CAM, '*.png'))):
    base = os.path.basename(f)
    if '(Texto)' in base:
        continue
    slug = base.replace('Camadas_', '').replace('.png', '').lower()
    im = Image.open(f).convert('RGBA')
    k = 900 / im.height
    im = im.resize((round(im.width * k), 900), Image.LANCZOS)
    # WebP com alpha: o mesmo diagrama em ~1/8 do peso de um PNG
    im.save(out('assets', 'camadas', slug + '.webp'), 'WEBP', quality=82, method=6)
    print(f'  {slug:8s} {im.width}x{im.height}  {os.path.getsize(out("assets","camadas",slug+".webp"))//1024}KB')

# --------------------------------------------------------------- processo
PROC = [
    ('475A8305.jpg', 'Montagem do molejo ensacado na linha de produção'),
    ('475A8882.jpg', 'Máquina de encapsular molas, uma a uma'),
    ('475A8619.jpg', 'Costura do tampo, guiada à mão'),
    ('475A8536.jpg', 'Camadas de espuma prontas para a laminação'),
]
print('— processo —')
PD = os.path.join(G, 'Colchão Wohl', '_ Fotos  Processo Produtivo')
for i, (f, _) in enumerate(PROC, 1):
    p = os.path.join(PD, f)
    if not os.path.exists(p):
        print(f'  !! ausente: {f}')
        continue
    fit(p, out('assets', 'processo', f'{i}.jpg'), 1200, 800, 78)
    print(f'  {i}.jpg  ({f})')

# -------------------------------------------------------------- lifestyle
LS = {'wohl-familia': 'Produtos/WOHL/familia Wohl.png'}
print('— lifestyle —')
for slug, rel in LS.items():
    p = src(*rel.split('/'))
    if os.path.exists(p):
        fit(p, out('assets', 'lifestyle', slug + '.jpg'), 1600, 1000, 80)
        print(f'  {slug} ok')

print('\nconcluído.')
