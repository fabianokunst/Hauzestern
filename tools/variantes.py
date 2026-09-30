# -*- coding: utf-8 -*-
"""
Gera as tres variantes de foto de cada colchao:

    assets/produtos/<slug>-branco.jpg     1400x1050   slide 1 do carrossel
    assets/produtos/<slug>-ambiente.jpg   1400x1050   slide 2 (so onde existe)
    assets/produtos/<slug>-cinza.jpg      1400x1050   slide 3
    assets/produtos/<slug>-detalhe.jpg    1400x1050   slide 4 (so onde existe)
    assets/produtos/<slug>-card.jpg        640x480    card da home (do cinza)

Uso:  python tools/variantes.py            (todos)
      python tools/variantes.py mond dorf  (so esses)

De onde vem cada variante esta na tabela VARIANTES abaixo. 'real' = foto do
guide. 'emular' = a variante nao existe no guide e e gerada por tools/fundos.py
a partir da outra variante; essas estao listadas no README.

Material que chegou depois do guide (Krefel, 09/2026) mora em
documentos/produtos/ — caminhos que comecam por 'documentos/' saem da raiz do
projeto, os outros de guide_hauzestern/.

Uma entrada 'real' pode ter um terceiro elemento {'recorte': (x0, y0, x1, y1)},
em fracao da foto original: o enquadramento sai dali em vez do centro. Serve
para foto vertical ou para detalhe, onde o recorte centrado corta o que importa.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image
import fundos

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, 'guide_hauzestern')
# cache dos emulados em resolucao cheia. Fica fora de assets/ para nao ser
# publicado; e reproduzivel — pode apagar a qualquer momento.
TMP = os.path.join(ROOT, '.cache-fundos')

P = 'Produtos/'
W = 'Colchão Wohl/_Fotos Fundo Infinito/'
K = 'documentos/produtos/krefel/'

# slug: {variante: ('real', caminho) | ('emular', caminho_origem, kwargs)}
VARIANTES = {
 'gipfel': {
   'branco': ('real', P + 'GIPFEL/COLCHAO MOLA C1924 GIPFEL HAUZESTERN BOX C1674 BEGE (4).jpg'),
   'cinza':  ('real', P + 'GIPFEL/COLCHAO MOLA C1924 HAUZESTERN BOX C1674 BEGE (.JPG'),
 },
 'frost': {
   'branco': ('real', P + 'FROST/COLCHÃO FROST.jpg'),
   'cinza':  ('real', P + 'FROST/FROST 01 - QUADRO PEQUENO.jpg'),
 },
 'himmel': {
   'cinza':  ('real', P + 'HIMMEL/HIMMEL (1).jpg'),
   'branco': ('emular', P + 'HIMMEL/HIMMEL (1).jpg', {}),
 },
 'mond': {
   'cinza':  ('real', P + 'MOND/MOND (1).jpg'),
   'branco': ('emular', P + 'MOND/MOND (1).jpg', {}),
 },
 'nebel': {
   'cinza':  ('real', P + 'NEBEL/NEBEL (1).jpg'),
   'branco': ('emular', P + 'NEBEL/NEBEL (1).jpg', {}),
 },
 'wohl': {
   'cinza':  ('real', W + '_D3A9225.JPG'),
   # 9225 tem vinheta forte e a segmentacao nao fecha; a emulacao sai de 9205,
   # que e outro angulo real do mesmo produto, com sweep mais uniforme.
   'branco': ('emular', W + '_D3A9205.JPG', {'tol': 18}),
   'ambiente': ('real', P + 'WOHL/familia Wohl.png'),
 },
 'hemmen': {
   'branco': ('real', P + 'HEMMEN/2D3A1031 colchao.jpg'),
   'cinza':  ('catalogo', 19),
   'ambiente': ('real', P + 'HEMMEN/familia Hemmen.png'),
 },
 'motte': {
   'cinza':  ('real', P + 'MOTTE/MOTTE (1).jpg'),
   'branco': ('emular', P + 'MOTTE/MOTTE (1).jpg', {}),
 },
 'wachen': {
   'cinza':  ('real', P + 'WACHEN/WACHEN (1).jpg'),
   'branco': ('emular', P + 'WACHEN/WACHEN (1).jpg', {}),
 },
 'zonen': {
   'cinza':  ('real', P + 'ZONEN/ZONEN (1).jpg'),
   'branco': ('emular', P + 'ZONEN/ZONEN (1).jpg', {}),
 },
 'dorf': {
   'branco': ('real', P + 'DORF/Dorf 2.jfif'),
   'cinza':  ('catalogo', 29),
 },
 'berg': {
   'cinza':  ('real', P + 'BERG/BERG (1).jpg'),
   'branco': ('emular', P + 'BERG/BERG (1).jpg', {}),
 },
 'eibsee': {
   'branco': ('real', P + 'LANÇAMENTO 2025 - Coleção Raízes/Eibsee/fundo branco/COLCHAO EIBSEE 2.JPG'),
   'cinza':  ('real', P + 'LANÇAMENTO 2025 - Coleção Raízes/Eibsee/fundo cinza/COLCHAO EIBSEE.jpg'),
 },
 'sylt': {
   'branco': ('real', P + 'SYLT/COLCHÃO SYLT.jpg'),
   'cinza':  ('real', P + 'SYLT/sylt 01 - quadro pequeno.jpg'),
 },
 # Krefel: as sete fotos do lancamento sao todas em estudio cinza-claro (~210).
 # Cinza = o 3/4 sobre a base, cujo sweep (topo ~155, chao ~190) e o do
 # estudio da marca. Branco = o frontal, emulado; a sombra de contato sai por
 # ganho abaixo do xadrez (fundos._refaz_chao), senao fica com degrau.
 # Detalhe = tampo, vivo, etiqueta e xadrez, recortado da foto vertical.
 'krefel': {
   'branco':  ('emular', K + 'COLCHÃO KREFEL C2012 (2).JPG', {'chao': (0.548, 0.585)}),
   'cinza':   ('real', K + 'COLCHÃO KREFEL C2012.JPG'),
   'detalhe': ('real', K + 'COLCHÃO KREFEL C2012 (3).JPG', {'recorte': (0, 0.33, 1, 0.83)}),
 },
}


def caminho(rel):
    """Foto de origem: documentos/ (material novo) ou guide_hauzestern/."""
    base = ROOT if rel.startswith('documentos/') else G
    return os.path.join(base, *rel.split('/'))


CATALOGO = ('CATÁLOGO', 'CATÁLOGO 2026', 'Hauzestern_Catalogo_2026_WEB.pdf')


def do_catalogo(pagina, destino):
    """Extrai a foto de produto em fundo cinza da pagina de abertura do modelo
    no catalogo 2026. E foto REAL, so em 771x689 — resolucao suficiente para o
    card e apertada para o slide de 1400px.

    Usado onde nao existe foto em fundo cinza em alta E a emulacao nao fecha:
    Hemmen e Dorf sao brancos e lisos contra fundo branco e liso, e nesses dois
    qualquer mascara come a borda traseira do colchao. Foto real mole e melhor
    que emulacao com recorte visivel.
    """
    if os.path.exists(destino):
        return destino
    import pymupdf
    doc = pymupdf.open(os.path.join(G, *CATALOGO))
    for info in doc[pagina].get_images(full=True):
        px = pymupdf.Pixmap(doc, info[0])
        if px.width >= 500:
            if px.n > 3:
                px = pymupdf.Pixmap(pymupdf.csRGB, px)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            Image.frombytes('RGB', (px.width, px.height), px.samples).save(destino)
            return destino
    raise RuntimeError(f'sem imagem grande na pagina {pagina + 1} do catalogo')


def fit(origem, destino, w, h, q=80, recorte=None):
    im = Image.open(origem)
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg
    im = im.convert('RGB')
    if recorte:
        x0, y0, x1, y1 = recorte
        W0, H0 = im.size
        im = im.crop((round(x0 * W0), round(y0 * H0), round(x1 * W0), round(y1 * H0)))
    sw, sh = im.size
    k = max(w / sw, h / sh)
    nw, nh = round(sw * k), round(sh * k)
    im = im.resize((nw, nh), Image.LANCZOS)
    im = im.crop(((nw - w) // 2, (nh - h) // 2, (nw - w) // 2 + w, (nh - h) // 2 + h))
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    im.save(destino, 'JPEG', quality=q, optimize=True, progressive=True)


def gera(slug, spec):
    os.makedirs(TMP, exist_ok=True)
    fontes = {}
    for variante, cfg in spec.items():
        if cfg[0] == 'real':
            opts = cfg[2] if len(cfg) > 2 else {}
            fontes[variante] = (caminho(cfg[1]), 'real', opts.get('recorte'))
        elif cfg[0] == 'catalogo':
            alvo = os.path.join(TMP, f'{slug}-{variante}-catalogo.png')
            fontes[variante] = (do_catalogo(cfg[1], alvo), 'real (catálogo)', None)
        else:
            origem = caminho(cfg[1])
            alvo = os.path.join(TMP, f'{slug}-{variante}.jpg')
            if not os.path.exists(alvo):
                r = fundos.converte(origem, alvo, variante, **cfg[2])
                print(f'      emulado {variante}: fundo {r["fundo_antes"]}->'
                      f'{r["fundo_depois"]}, desvio no produto {r["desvio_produto"]:.2f}')
            fontes[variante] = (alvo, 'EMULADO', None)

    saida = os.path.join(ROOT, 'assets', 'produtos')
    marcas = []
    for variante in ('branco', 'ambiente', 'cinza', 'detalhe'):
        if variante not in fontes:
            continue
        src, tipo, rec = fontes[variante]
        fit(src, os.path.join(saida, f'{slug}-{variante}.jpg'), 1400, 1050, 80, rec)
        marcas.append(f'{variante}={tipo}')
    # card da home sai sempre do cinza
    src, _, rec = fontes['cinza']
    fit(src, os.path.join(saida, f'{slug}-card.jpg'), 640, 480, 78, rec)
    return marcas


if __name__ == '__main__':
    alvos = sys.argv[1:] or list(VARIANTES)
    for slug in alvos:
        t = time.time()
        print(f'  {slug}')
        marcas = gera(slug, VARIANTES[slug])
        print(f'      {"  ".join(marcas)}   ({time.time()-t:.0f}s)')
