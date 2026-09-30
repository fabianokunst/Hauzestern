# -*- coding: utf-8 -*-
"""
Gera as paginas de produto (colchoes, travesseiros, bases) e as partes
compartilhadas de <head>, header e footer.

Uso:  python tools/build_all.py

Todo texto de produto vem de tools/dados.py, que e transcricao do material da
marca. Este arquivo so decide COMO mostrar — nunca O QUE dizer. Se um campo
esta vazio em dados.py, a secao correspondente nao aparece na pagina.
"""
import os, sys, io, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

import dados

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.hauzestern.com'
HOJE = datetime.date.today().isoformat()

TEL_HREF = 'tel:+555135648300'
TEL_TXT = '(51) 3564-8300'

IG = 'https://www.instagram.com/hauzestern/'
IG_SVG = ('<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true">'
          '<path fill="currentColor" d="M12 2.2c3.2 0 3.6 0 4.9.07 1.2.05 1.8.25 2.2.42.6.22 1 .48 1.4.9'
          '.42.4.68.8.9 1.4.17.4.37 1 .42 2.2.07 1.3.07 1.7.07 4.9s0 3.6-.07 4.9c-.05 1.2-.25 1.8-.42 2.2'
          '-.22.6-.48 1-.9 1.4-.4.42-.8.68-1.4.9-.4.17-1 .37-2.2.42-1.3.07-1.7.07-4.9.07s-3.6 0-4.9-.07'
          'c-1.2-.05-1.8-.25-2.2-.42-.6-.22-1-.48-1.4-.9-.42-.4-.68-.8-.9-1.4-.17-.4-.37-1-.42-2.2C2.2 15.6 '
          '2.2 15.2 2.2 12s0-3.6.07-4.9c.05-1.2.25-1.8.42-2.2.22-.6.48-1 .9-1.4.4-.42.8-.68 1.4-.9.4-.17 1-.37 '
          '2.2-.42C8.4 2.2 8.8 2.2 12 2.2Zm0 1.8c-3.1 0-3.5 0-4.8.07-.9.04-1.4.2-1.7.32-.43.17-.74.37-1.06.7'
          '-.33.32-.53.63-.7 1.06-.12.3-.28.8-.32 1.7-.07 1.3-.08 1.65-.08 4.15s0 2.85.08 4.15c.4.9.2 1.4.32 1.7'
          '.17.43.37.74.7 1.06.32.33.63.53 1.06.7.3.12.8.28 1.7.32 1.3.06 1.7.07 4.8.07s3.5 0 4.8-.07c.9-.04 '
          '1.4-.2 1.7-.32.43-.17.74-.37 1.06-.7.33-.32.53-.63.7-1.06.12-.3.28-.8.32-1.7.06-1.3.07-1.65.07-4.15'
          's0-2.85-.07-4.15c-.04-.9-.2-1.4-.32-1.7a2.9 2.9 0 0 0-.7-1.06 2.9 2.9 0 0 0-1.06-.7c-.3-.12-.8-.28-1.7'
          '-.32C15.5 4 15.1 4 12 4Zm0 3.05a4.95 4.95 0 1 1 0 9.9 4.95 4.95 0 0 1 0-9.9Zm0 1.8a3.15 3.15 0 1 0 0 '
          '6.3 3.15 3.15 0 0 0 0-6.3Zm5.15-3.1a1.15 1.15 0 1 1 0 2.3 1.15 1.15 0 0 1 0-2.3Z"/></svg>')


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def paras(lista, indent='      '):
    return ('\n' + indent).join(f'<p>{t}</p>' for t in lista)


# ------------------------------------------------------------------ carrossel
# Ordem pedida: 1 fundo branco, 2 ambientada, 3 fundo cinza, 4 detalhe.
# A ambientada so entra onde a marca tem foto de ambiente (Wohl e Hemmen); o
# detalhe, onde a marca mandou close do acabamento (Krefel).
VARIANTES_ORDEM = [
    ('branco', 'sobre fundo branco'),
    ('ambiente', 'em ambiente'),
    ('cinza', 'sobre fundo cinza'),
    ('detalhe', 'em detalhe do tampo e da lateral'),
]


def carrossel(p, slug, nome, alt_base, pasta='produtos', flag=''):
    """Carrossel das fotos que existem para este produto.

    Sem JavaScript continua utilizavel: a trilha e uma faixa com scroll-snap,
    navegavel por toque, roda do mouse e teclado. O JS so acrescenta os botoes
    e os pontos.
    """
    disponiveis = [(v, d) for v, d in VARIANTES_ORDEM
                   if os.path.exists(os.path.join(
                       ROOT, 'assets', pasta, f'{slug}-{v}.jpg'))]
    n = len(disponiveis)
    slides, pontos = [], []
    for i, (v, desc) in enumerate(disponiveis, 1):
        eager = ('fetchpriority="high"' if i == 1 else 'loading="lazy"')
        slides.append(
            f'<li class="carrossel-slide" role="group" aria-roledescription="slide"\n'
            f'            aria-label="Foto {i} de {n} — {desc}">\n'
            f'          <img src="{p}assets/{pasta}/{slug}-{v}.jpg"\n'
            f'               alt="{esc(alt_base)} {desc}"\n'
            f'               width="1400" height="1050" {eager}>\n'
            f'        </li>')
        pontos.append(
            f'<li><button type="button" data-ir="{i-1}"'
            f' aria-label="Ver foto {i} de {n} — {desc}"'
            + (' aria-current="true"' if i == 1 else '') + '></button></li>')

    if n == 1:
        return (f'<figure class="pdp-media">{flag}\n'
                f'        <img src="{p}assets/{pasta}/{slug}-{disponiveis[0][0]}.jpg"\n'
                f'             alt="{esc(alt_base)}" width="1400" height="1050"'
                f' fetchpriority="high">\n      </figure>')

    return f'''<div class="pdp-media carrossel" data-carrossel role="group"
           aria-roledescription="carrossel" aria-label="Fotos do {esc(nome)}">{flag}
        <ul class="carrossel-trilha" tabindex="0">
          {chr(10).join('        ' + s for s in slides).lstrip()}
        </ul>
        <button class="carrossel-btn carrossel-prev" type="button" data-passo="-1"
                aria-label="Foto anterior" hidden>
          <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path
            d="M15 5 8 12l7 7" fill="none" stroke="currentColor" stroke-width="1.6"
            stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <button class="carrossel-btn carrossel-next" type="button" data-passo="1"
                aria-label="Próxima foto" hidden>
          <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path
            d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="1.6"
            stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <ol class="carrossel-pontos">
          {chr(10).join('          ' + x for x in pontos).lstrip()}
        </ol>
      </div>'''


# --------------------------------------------------------------------- <head>
def head(p, title, desc, canon, og_img, og_type='website', ld=(), extra=''):
    j = '\n'.join('<script type="application/ld+json">\n%s\n</script>'
                  % json.dumps(o, ensure_ascii=False, indent=2) for o in ld)
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js')</script>
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/{og_img}">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="Hauzestern Colchões">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/{og_img}">
<meta name="theme-color" content="#1d1d1d">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="{p}favicon.ico" sizes="16x16 32x32 48x48">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Julius+Sans+One&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}css/style.css">
{extra}{j}
</head>'''


# --------------------------------------------------------- header / footer
def header(p, interna=True):
    # sempre relativo: '/' quebraria em file:// e no GitHub Pages de
    # projeto, onde o site nao mora na raiz do dominio.
    home = p + 'index.html'
    return f'''
<a class="skip-link" href="#main">Pular para o conteúdo</a>

<header class="site-header" id="header">
  <div class="wrap header-inner">
    <a class="brand" href="{home}" aria-label="Hauzestern Colchões — página inicial">
      <img class="brand-marca" src="{p}assets/brand/logotipo-colchoes-negativo.svg"
           alt="Hauzestern Colchões" width="1134" height="262">
      <img class="brand-simbolo" src="{p}assets/brand/simbolo-reduzido-negativo.svg"
           alt="Hauzestern Colchões" width="479" height="572">
    </a>

    <nav class="nav" id="nav" aria-label="Navegação principal">
      <ul>
        <li><a href="{p}index.html#a-marca">A Hauzestern</a></li>
        <li class="has-sub">
          <button class="nav-sub-toggle" id="sub-btn" aria-expanded="false" aria-controls="sub-produtos">
            Produtos<span class="caret" aria-hidden="true"></span>
          </button>
          <ul class="nav-sub" id="sub-produtos" aria-labelledby="sub-btn">
            <li><a href="{p}index.html#colchoes">Colchões</a></li>
            <li><a href="{p}index.html#bases">Bases</a></li>
            <li><a href="{p}index.html#travesseiros">Travesseiros</a></li>
          </ul>
        </li>
        <li><a href="{p}index.html#tecnologias">Tecnologias</a></li>
        <li><a href="{p}garantia.html">Garantia</a></li>
        <li><a href="{p}representantes.html">Representantes</a></li>
        <li><a href="{p}index.html#contato">Contato</a></li>
      </ul>
      <a class="nav-ig" href="{IG}" target="_blank" rel="noopener">
        {IG_SVG}
        <span>@hauzestern</span>
      </a>
    </nav>

    <!-- busca de produtos: o painel e o índice são do js/busca.js -->
    <button class="busca-btn" type="button" data-busca-abrir aria-haspopup="dialog"
            aria-expanded="false" aria-label="Buscar produtos" aria-keyshortcuts="/ Control+K"
            title="Buscar produtos">
      <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="10.5" cy="10.5"
        r="6.25" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="m15.2 15.2 5.3 5.3"
        fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </button>

    <button class="burger" id="burger" aria-expanded="false" aria-controls="nav" aria-label="Abrir menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
'''


def footer(p):
    return f'''
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="{p}assets/brand/marca-negativo.svg" alt="Hauzestern Colchões"
           width="1134" height="610" loading="lazy">
      <p>Colchões premium do Grupo Herval. Dois Irmãos, Rio Grande do Sul.</p>
    </div>
    <nav class="footer-nav" aria-label="Rodapé">
      <div>
        <h4>Institucional</h4>
        <ul>
          <li><a href="{p}index.html#a-marca">A Hauzestern</a></li>
          <li><a href="{p}index.html#processo">Como fazemos</a></li>
          <li><a href="{p}index.html#tecnologias">Tecnologias</a></li>
          <li><a href="{p}representantes.html">Representantes</a></li>
        </ul>
      </div>
      <div>
        <h4>Produtos</h4>
        <ul>
          <li><a href="{p}index.html#colchoes">Colchões</a></li>
          <li><a href="{p}index.html#bases">Bases</a></li>
          <li><a href="{p}index.html#travesseiros">Travesseiros</a></li>
        </ul>
      </div>
      <div>
        <h4>Ajuda</h4>
        <ul>
          <li><a href="{p}garantia.html">Garantia e cuidados</a></li>
          <li><a href="{p}garantia.html#biotipos">Tabela de biotipos</a></li>
          <li><a href="{TEL_HREF}">{TEL_TXT}</a></li>
          <li><a href="{IG}" target="_blank" rel="noopener">@hauzestern</a></li>
        </ul>
      </div>
    </nav>
  </div>
  <div class="wrap footer-bottom">
    <small>&copy; <span id="year">{datetime.date.today().year}</span> Hauzestern Colchões — Grupo Herval. Todos os direitos reservados.</small>
    <small><a href="{p}garantia.html">Garantia</a> &nbsp;·&nbsp; Zuhause + stern — lar + estrela</small>
  </div>
</footer>

<script src="{p}js/main.js" defer></script>
<script src="{p}js/busca.js" defer></script>
</body>
</html>
'''


def cta(p, nome):
    return f'''
<section class="cta-band" aria-labelledby="cta-title">
  <div class="wrap narrow center">
    <h2 id="cta-title" class="display">Quer conhecer o {nome} de perto?</h2>
    <p>Os produtos Hauzestern estão em uma rede selecionada de lojas parceiras.
       O representante da sua região indica a mais perto de você.</p>
    <div class="cta-band-acoes">
      <a class="btn btn-dark" href="{p}representantes.html">Onde comprar</a>
      <a class="btn btn-ghost-dark" href="{TEL_HREF}">{TEL_TXT}</a>
    </div>
  </div>
</section>
'''


def bloco_garantia(p, tipo='colchão'):
    g = dados.GARANTIA
    if tipo == 'base':
        titulo = f'Box rígido: {g["box_rigido"]}'
        txt = ('Conforme o Certificado de Garantia Hauzestern, no box rígido a garantia é '
               'de 6 meses. A garantia começa no dia do recebimento do conjunto e é '
               'válida com a apresentação da nota fiscal junto ao Certificado. O Box deve '
               'ser usado sobre superfície plana, com todos os pés devidamente apertados '
               'e apoiados — rangido por pé deslocado não caracteriza defeito de '
               'fabricação.')
    else:
        titulo = f'Molejo {g["molejo"]}, demais componentes {g["componentes"]}'
        txt = ('A garantia começa no dia do recebimento do colchão ou do conjunto e é '
               'válida com a apresentação da nota fiscal junto ao Certificado de '
               'Garantia. ' + dados.GARANTIA_FICHA_TXT)
    return f'''
<section class="section pdp-garantia" aria-labelledby="gar-title">
  <div class="wrap">
    <div class="garantia-box reveal">
      <div class="garantia-selo" aria-hidden="true">
        <img src="{p}assets/brand/simbolo-positivo.svg" alt="" width="479" height="572" loading="lazy">
      </div>
      <div class="garantia-txt">
        <p class="eyebrow">Garantia Hauzestern</p>
        <h2 id="gar-title" class="display">{titulo}</h2>
        <p>{txt}</p>
        <a class="link-arrow" href="{p}garantia.html">Ler os termos completos da garantia <span aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </div>
</section>
'''


# ------------------------------------------------------------------- colchões
def pdp_colchao(m, todos):
    p = '../'
    slug, nome = m['slug'], m['nome']
    col = dados.COLECOES[m['colecao']]
    res = dados.resumo(m)
    sig = f'{col["nome"]} ({m["significado"]})' if m['significado'] else col['nome']
    title = f'Colchão {nome} — Coleção {col["nome"]} | Hauzestern Colchões'
    desc = (f'Colchão Hauzestern {nome}: {m["altura"]} cm, {len(m["camadas"])} camadas, '
            f'até {m["capacidade"]} kg por pessoa. Composição completa e garantia.')
    canon = f'{SITE}/colchoes/{slug}.html'
    img = f'assets/produtos/{slug}-branco.jpg'
    fotos = [f'{SITE}/assets/produtos/{slug}-{v}.jpg' for v, _ in VARIANTES_ORDEM
             if os.path.exists(os.path.join(ROOT, 'assets', 'produtos', f'{slug}-{v}.jpg'))]

    ld_product = {
        '@context': 'https://schema.org', '@type': 'Product',
        'name': f'Colchão Hauzestern {nome}',
        'description': m['poetica'],
        'image': fotos,
        'url': canon, 'category': 'Colchões',
        'brand': {'@type': 'Brand', 'name': 'Hauzestern'},
        'manufacturer': {'@type': 'Organization', 'name': 'Grupo Herval'},
        'isSimilarTo': [{'@type': 'Product', 'name': f'Colchão Hauzestern {o["nome"]}',
                         'url': f'{SITE}/colchoes/{o["slug"]}.html'}
                        for o in todos if o['colecao'] == m['colecao'] and o['slug'] != slug],
        'additionalProperty': (
            [{'@type': 'PropertyValue', 'name': 'Coleção', 'value': col['nome']},
             {'@type': 'PropertyValue', 'name': 'Altura', 'value': f'{m["altura"]} cm'},
             {'@type': 'PropertyValue', 'name': 'Capacidade de peso individual',
              'value': f'{m["capacidade"]} kg'}]
            + [{'@type': 'PropertyValue', 'name': 'Tecnologia', 'value': b} for b in m['badges']]
        ),
        'hasMeasurement': {'@type': 'QuantitativeValue', 'name': 'Altura',
                           'value': m['altura'], 'unitCode': 'CMT'},
    }
    ld_crumbs = {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Colchões', 'item': SITE + '/#colchoes'},
            {'@type': 'ListItem', 'position': 3, 'name': f'Coleção {col["nome"]}',
             'item': f'{SITE}/#colecao-{m["colecao"]}'},
            {'@type': 'ListItem', 'position': 4, 'name': nome},
        ],
    }

    # --- seções que só existem se a marca escreveu algo ---------------------
    diferenciais = ''
    if m.get('diferenciais'):
        diferenciais = f'''
<section class="section pdp-dif" aria-labelledby="dif-title">
  <div class="wrap narrow">
    <p class="eyebrow reveal">Camadas de conforto</p>
    <h2 id="dif-title" class="display reveal">O que faz a diferença</h2>
    <div class="prose reveal">
      {paras(m['diferenciais'])}
    </div>
  </div>
</section>
'''

    molejos = []
    if m.get('molejo'):
        molejos.append(('Molas ensacadas', m['molejo']))
    if m.get('molejo2'):
        molejos.append((m.get('molejo2_titulo', 'Molas MaxSpring'), m['molejo2']))
    molejo_html = ''
    if molejos:
        cards = '\n      '.join(
            f'<article class="molejo-card reveal"><h3>{t}</h3><p>{d}</p></article>'
            for t, d in molejos)
        sub = ('Duplo molejo: os dois sistemas trabalham juntos neste modelo.'
               if len(molejos) > 1 else 'O sistema de molejo deste modelo.')
        molejo_html = f'''
<section class="section pdp-molejo" aria-labelledby="mol-title">
  <div class="wrap">
    <header class="section-head">
      <div>
        <p class="eyebrow reveal">Sistema de molejo</p>
        <h2 id="mol-title" class="display reveal">Como o colchão sustenta</h2>
      </div>
      <p class="section-note reveal">{sub}</p>
    </header>
    <div class="grid-molejo">
      {cards}
    </div>
  </div>
</section>
'''

    sistema_html = ''
    if m.get('sistema'):
        s = m['sistema']
        espec = '\n        '.join(
            f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in s['especificacoes'])
        modos = '\n        '.join(
            f'<article class="modo reveal"><h4>{k}</h4><p>{v}</p></article>'
            for k, v in s['modos'])
        prot = '\n        '.join(
            f'<li><strong>{k}</strong><span>{v}</span></li>' for k, v in s['protecoes'])
        aten = '\n        '.join(f'<li>{t}</li>' for t in s['atencao'])
        sistema_html = f'''
<section class="section pdp-sistema" id="sistema" aria-labelledby="sis-title">
  <div class="wrap">
    <header class="section-head">
      <div>
        <p class="eyebrow light reveal">Exclusivo deste modelo</p>
        <h2 id="sis-title" class="display reveal">{s['nome']}</h2>
      </div>
      <p class="section-note reveal">{s['intro']}</p>
    </header>

    <h3 class="sis-h3 reveal">Modos de funcionamento</h3>
    <div class="grid-modos">
        {modos}
    </div>

    <h3 class="sis-h3 reveal">Especificações</h3>
    <dl class="sis-espec reveal">
        {espec}
    </dl>

    <h3 class="sis-h3 reveal">Garantia de segurança — 4 medidas de proteção</h3>
    <ul class="sis-prot reveal">
        {prot}
    </ul>

    <div class="sis-atencao reveal">
      <h3>Atenção</h3>
      <ul>
        {aten}
      </ul>
      <p class="nota">Instruções completas no manual do Sistema Thermo Flow que
        acompanha o produto.</p>
    </div>
  </div>
</section>
'''

    diagrama = ''
    if m['diagrama']:
        diagrama = f'''
        <figure class="camadas-fig reveal">
          <img src="{p}assets/camadas/{m['diagrama']}.webp"
               alt="Diagrama das camadas internas do colchão {nome}, do tampo à base"
               width="629" height="900" loading="lazy">
          <figcaption>As {len(m['camadas'])} camadas do {nome}, do tampo à base.</figcaption>
        </figure>'''

    chips = '\n        '.join(f'<li>{b}</li>' for b in m['badges'])
    camadas = '\n          '.join(f'<li>{c}</li>' for c in m['camadas'])
    suporte = '\n        '.join(
        f'<li><strong>{s.split(" e ")[0]}</strong><span>{s.split(" e ")[1]}</span></li>'
        for s in m['suporte'])

    cuidados = list(dados.CUIDADOS_BASE) + list(m.get('cuidados_extra', []))
    cuidados_li = '\n        '.join(f'<li>{c}</li>' for c in cuidados)

    irmaos = [o for o in todos if o['colecao'] == m['colecao'] and o['slug'] != slug][:4]
    if len(irmaos) < 4:
        irmaos += [o for o in todos if o['slug'] != slug and o not in irmaos][:4 - len(irmaos)]
    rel = '\n      '.join(
        f'<a class="card reveal" href="{o["slug"]}.html">'
        f'<figure><img src="{p}assets/produtos/{o["slug"]}-card.jpg" '
        f'alt="Colchão Hauzestern {o["nome"]}" width="640" height="480" loading="lazy"></figure>'
        f'<h3>{o["nome"]}</h3><p>{o["altura"]} cm · {dados.resumo(o)}</p></a>' for o in irmaos)

    flag = f'<span class="card-flag">{m["destaque"]}</span>' if m.get('destaque') else ''
    carr = carrossel(p, slug, f'colchão {nome}',
                     f'Colchão Hauzestern {nome}', 'produtos', flag)

    return head(p, title, desc, canon, img, 'product', [ld_product, ld_crumbs]) + f'''
<body class="interna">
{header(p)}
<main id="main">

<!-- ============================= PRODUTO ============================= -->
<section class="section pdp" aria-labelledby="pdp-title">
  <div class="wrap">
    <nav class="crumbs" aria-label="Trilha de navegação">
      <ol>
        <li><a href="{p}index.html">Início</a></li>
        <li><a href="{p}index.html#colchoes">Colchões</a></li>
        <li><a href="{p}index.html#colecao-{m['colecao']}">Coleção {col['nome']}</a></li>
        <li><span aria-current="page">{nome}</span></li>
      </ol>
    </nav>

    <div class="pdp-grid">
      {carr}

      <div class="pdp-info">
        <p class="eyebrow"><a href="{p}index.html#colecao-{m['colecao']}">Coleção {col['nome']}</a></p>
        <h1 id="pdp-title" class="display">Colchão {nome}</h1>
        <p class="pdp-sub">{res}</p>
        <p class="lede">{m['poetica']}</p>
        <ul class="specs pdp-quick">
          <li><strong>Altura</strong><span>{m['altura']} cm</span></li>
          <li><strong>Capacidade</strong><span>{m['capacidade']} kg por pessoa</span></li>
          <li><strong>Camadas</strong><span>{len(m['camadas'])}</span></li>
          <li><strong>Coleção</strong><span>{sig}</span></li>
        </ul>
        <div class="pdp-cta">
          <a class="btn btn-dark" href="{p}representantes.html">Onde comprar</a>
          <a class="btn btn-ghost-dark" href="{TEL_HREF}">{TEL_TXT}</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================= DESCRIÇÃO ============================= -->
<section class="section pdp-sobre" aria-labelledby="sobre-title">
  <div class="wrap narrow">
    <p class="eyebrow reveal">Descrição</p>
    <h2 id="sobre-title" class="display reveal">Sobre o {nome}</h2>
    <div class="prose reveal">
      {paras(m['tecnica'])}
    </div>
  </div>
</section>

<!-- ============================= TECNOLOGIAS ============================= -->
<section class="section tech pdp-tech" aria-labelledby="tec-title">
  <div class="wrap">
    <header class="section-head">
      <div>
        <p class="eyebrow light reveal">Ícones {'da ficha técnica' if m.get('icones_da_ficha') else 'do catálogo'}</p>
        <h2 id="tec-title" class="display reveal">Tecnologias no {nome}</h2>
      </div>
      <p class="section-note reveal">As tecnologias que a marca lista para este modelo.</p>
    </header>
    <ul class="chips reveal">
        {chips}
    </ul>
    <p class="center more reveal"><a class="link-arrow" href="{p}index.html#tecnologias">O que cada tecnologia faz <span aria-hidden="true">&rarr;</span></a></p>
  </div>
</section>
{diferenciais}{sistema_html}{molejo_html}
<!-- ============================= COMPOSIÇÃO ============================= -->
<section class="section pdp-camadas" aria-labelledby="cam-title">
  <div class="wrap">
    <header class="section-head">
      <div>
        <p class="eyebrow reveal">Composição</p>
        <h2 id="cam-title" class="display reveal">Do tampo à base</h2>
      </div>
      <p class="section-note reveal">Altura total de {m['altura']} cm, em {len(m['camadas'])} camadas.</p>
    </header>
    <div class="camadas-grid">{diagrama}
      <div class="reveal">
        <ol class="camadas-lista">
          {camadas}
        </ol>
      </div>
    </div>
  </div>
</section>

<!-- ============================= SUPORTE DE PESO ============================= -->
<section class="section pdp-suporte" aria-labelledby="sup-title">
  <div class="wrap narrow">
    <p class="eyebrow reveal">Suporte de peso individual</p>
    <h2 id="sup-title" class="display reveal">Para qual biotipo</h2>
    <ul class="suporte reveal">
        {suporte}
    </ul>
    <p class="nota reveal">Valores por pessoa. Em cama de casal com biotipos diferentes, consulte a
      <a href="{p}garantia.html#biotipos">tabela de biotipos</a> — ela orienta a densidade adequada
      e é condição de garantia nos colchões de espuma.</p>
  </div>
</section>
{bloco_garantia(p)}
<!-- ============================= CUIDADOS ============================= -->
<section class="section pdp-cuidados" aria-labelledby="cuidados-title">
  <div class="wrap narrow">
    <p class="eyebrow reveal">Uso e conservação</p>
    <h2 id="cuidados-title" class="display reveal">Como cuidar</h2>
    <div class="prose reveal">
      <p>{dados.ONE_SIDE_TXT}</p>
    </div>
    <ul class="lista-cuidados reveal">
        {cuidados_li}
    </ul>
    <p class="nota reveal">Lista completa de cuidados e do que não é coberto na
      <a href="{p}garantia.html">página de garantia</a>.</p>
  </div>
</section>

<!-- ============================= RELACIONADOS ============================= -->
<section class="section pdp-rel" aria-labelledby="rel-title">
  <div class="wrap">
    <header class="section-head">
      <div>
        <p class="eyebrow reveal">Coleção {col['nome']}</p>
        <h2 id="rel-title" class="display reveal">Outros modelos</h2>
      </div>
      <p class="section-note reveal">{col['resumo']}</p>
    </header>
    <div class="grid-products">
      {rel}
    </div>
    <p class="center more reveal"><a class="link-arrow" href="{p}index.html#colchoes">Ver as três coleções <span aria-hidden="true">&rarr;</span></a></p>
  </div>
</section>
{cta(p, nome)}
</main>
{footer(p)}'''


# --------------------------------------------------------------------- bases
def pdp_base(b, todas):
    p = '../'
    slug, nome = b['slug'], b['nome']
    title = f'{nome} — base para colchão | Hauzestern Colchões'
    desc = (f'{nome} Hauzestern: box de {b["box"]} e pés de {b["pes"]}. '
            f'{b["material"]}, estrutura de eucalipto e forro de TNT.')
    canon = f'{SITE}/bases/{slug}.html'
    img = f'assets/bases/{b["foto"]}.jpg' if b['foto'] else 'assets/brand/marca-positivo.svg'

    ld = [{
        '@context': 'https://schema.org', '@type': 'Product',
        'name': f'{nome} Hauzestern',
        'description': b['poetica'] or desc,
        'image': [f'{SITE}/{img}'],
        'url': canon, 'category': 'Bases para colchão',
        'sku': b['ref'],
        'brand': {'@type': 'Brand', 'name': 'Hauzestern'},
        'manufacturer': {'@type': 'Organization', 'name': 'Grupo Herval'},
        'material': 'Madeira de eucalipto de reflorestamento',
        'additionalProperty': [
            {'@type': 'PropertyValue', 'name': 'Altura do box', 'value': b['box']},
            {'@type': 'PropertyValue', 'name': 'Altura dos pés', 'value': b['pes']},
            {'@type': 'PropertyValue', 'name': 'Pés', 'value': b['material']},
            {'@type': 'PropertyValue', 'name': 'Forro', 'value': 'TNT'},
        ] + ([{'@type': 'PropertyValue', 'name': 'Suporte (box rígido)',
               'value': b['suporte']}] if b.get('suporte') else []),
    }, {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Bases', 'item': SITE + '/#bases'},
            {'@type': 'ListItem', 'position': 3, 'name': nome},
        ],
    }]

    if b['foto']:
        media = (f'<img src="{p}assets/bases/{b["foto"]}.jpg" '
                 f'alt="{nome} Hauzestern, base box vista em três quartos" '
                 f'width="1400" height="1050" fetchpriority="high">')
    else:
        media = (f'<div class="sem-foto"><img src="{p}assets/brand/simbolo-positivo.svg" '
                 f'alt="" width="479" height="572">'
                 f'<p>Sem fotografia deste modelo no banco de imagens da marca.</p></div>')

    poetica = f'<p class="lede">{b["poetica"]}</p>' if b['poetica'] else ''

    # o texto de ficha técnica existe para todas menos a C1674
    if b['ficha']:
        sobre = f'''
    <div class="prose reveal">
      <p><strong>{b['ref']}</strong> é a escolha ideal para quem busca melhorar a
        qualidade do sono. Construído integralmente de materiais de alta qualidade,
        proporciona um suporte adequado aos colchões Hauzestern.</p>
      <p>{b['ref']} {dados.BASE_SUPORTE_TXT}</p>
    </div>

    <h3 class="ficha-h3 reveal">Estrutura</h3>
    <div class="prose reveal"><p>{dados.BASE_ESTRUTURA}</p></div>

    <h3 class="ficha-h3 reveal">Revestimento</h3>
    <div class="prose reveal"><p>{dados.BASE_REVESTIMENTO}</p></div>'''
    else:
        sobre = f'''
    <div class="prose reveal">
      <p>Base box com estrutura de eucalipto e forro de TNT, com {b['material'].lower()}.
        O box tem {b['box']} de altura e os pés, {b['pes']}.</p>
      <p class="nota">Este modelo consta no catálogo 2026 da marca, mas ainda não tem
        ficha técnica no material oficial. Quando a ficha existir, esta página recebe a
        descrição de estrutura e revestimento como as demais bases.</p>
    </div>'''

    conflito = (f'<p class="nota reveal">{b["nota_conflito"]}</p>'
                if b.get('nota_conflito') else '')
    suporte = (f'\n          <li><strong>Suporte</strong><span>Box rígido, '
               f'{b["suporte"]}</span></li>' if b.get('suporte') else '')

    outras = '\n      '.join(
        f'<a class="card reveal" href="{o["slug"]}.html">'
        + (f'<figure><img src="{p}assets/bases/{o["foto"]}-card.jpg" '
           f'alt="{o["nome"]} Hauzestern" width="640" height="480" loading="lazy"></figure>'
           if o['foto'] else
           f'<figure class="card-vazia"><img src="{p}assets/brand/simbolo-positivo.svg" '
           f'alt="" width="479" height="572" loading="lazy"></figure>')
        + f'<h3>{o["nome"]}</h3><p>Box {o["box"]} · pés {o["pes"]}</p></a>'
        for o in todas if o['slug'] != slug)

    return head(p, title, desc, canon, img, 'product', ld) + f'''
<body class="interna">
{header(p)}
<main id="main">

<section class="section pdp" aria-labelledby="pdp-title">
  <div class="wrap">
    <nav class="crumbs" aria-label="Trilha de navegação">
      <ol>
        <li><a href="{p}index.html">Início</a></li>
        <li><a href="{p}index.html#bases">Bases</a></li>
        <li><span aria-current="page">{nome}</span></li>
      </ol>
    </nav>

    <div class="pdp-grid">
      <figure class="pdp-media">
        {media}
      </figure>

      <div class="pdp-info">
        <p class="eyebrow">Bases</p>
        <h1 id="pdp-title" class="display">{nome}</h1>
        <p class="pdp-sub">Referência {b['ref']}</p>
        {poetica}
        <ul class="specs pdp-quick">
          <li><strong>Altura do box</strong><span>{b['box']}</span></li>
          <li><strong>Altura dos pés</strong><span>{b['pes']}</span></li>
          <li><strong>Pés</strong><span>{b['material'].replace('Pés de ', '').capitalize()}</span></li>
          <li><strong>Estrutura</strong><span>Eucalipto · forro de TNT</span></li>{suporte}
        </ul>
        {conflito}
        <div class="pdp-cta">
          <a class="btn btn-dark" href="{p}representantes.html">Onde comprar</a>
          <a class="btn btn-ghost-dark" href="{TEL_HREF}">{TEL_TXT}</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section pdp-sobre" aria-labelledby="sobre-title">
  <div class="wrap narrow">
    <p class="eyebrow reveal">Descrição</p>
    <h2 id="sobre-title" class="display reveal">Sobre o {nome}</h2>
    {sobre}
  </div>
</section>
{bloco_garantia(p, 'base')}
<section class="section pdp-rel" aria-labelledby="rel-title">
  <div class="wrap">
    <header class="section-head">
      <div>
        <p class="eyebrow reveal">Complementos</p>
        <h2 id="rel-title" class="display reveal">Outras bases</h2>
      </div>
      <p class="section-note reveal">Seis modelos de box, de 15 a 28 cm de altura.
        A base correta é condição de garantia do colchão.</p>
    </header>
    <div class="grid-products">
      {outras}
    </div>
  </div>
</section>
{cta(p, nome)}
</main>
{footer(p)}'''


# --------------------------------------------------------------- travesseiros
def pdp_travesseiro(t, todos):
    p = '../'
    slug, nome = t['slug'], t['nome']
    col = dados.COLECOES.get(t['colecao'])
    title = f'Travesseiro {nome} | Hauzestern Colchões'
    desc = f'Travesseiro Hauzestern {nome}, {t["medidas"]}. Composição e cuidados.'
    canon = f'{SITE}/travesseiros/{slug}.html'
    img = f'assets/travesseiros/{slug}.jpg'

    ld = [{
        '@context': 'https://schema.org', '@type': 'Product',
        'name': f'Travesseiro Hauzestern {nome}',
        'description': t['poetica'] or desc, 'image': [f'{SITE}/{img}'],
        'url': canon, 'category': 'Travesseiros',
        'brand': {'@type': 'Brand', 'name': 'Hauzestern'},
        'manufacturer': {'@type': 'Organization', 'name': 'Grupo Herval'},
        'additionalProperty': [{'@type': 'PropertyValue', 'name': 'Medidas', 'value': t['medidas']}]
        + ([{'@type': 'PropertyValue', 'name': 'Coleção', 'value': col['nome']}] if col else []),
    }, {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Travesseiros', 'item': SITE + '/#travesseiros'},
            {'@type': 'ListItem', 'position': 3, 'name': nome},
        ],
    }]

    ficha = '\n        '.join(f'<li>{x}</li>' for x in t['ficha'])
    eyebrow = (f'<a href="{p}index.html#colecao-{t["colecao"]}">Coleção {col["nome"]}</a>'
               if col else 'Travesseiros')
    sig = (f'<li><strong>Coleção</strong><span>{col["nome"]} ({t["significado"]})</span></li>'
           if col else '')
    poetica = f'<p class="lede">{t["poetica"]}</p>' if t['poetica'] else ''
    sem_texto = ('' if t['poetica'] else
                 '<p class="nota reveal">A marca não publicou texto descritivo para este '
                 'moldado: o catálogo traz apenas as medidas e a nomenclatura.</p>')
    outros = [o for o in todos if o['slug'] != slug]
    rel = '\n      '.join(
        f'<a class="card card-sm reveal" href="{o["slug"]}.html">'
        f'<figure><img src="{p}assets/travesseiros/{o["slug"]}-card.jpg" '
        f'alt="Travesseiro Hauzestern {o["nome"]}" width="480" height="360" loading="lazy"></figure>'
        f'<h3>{o["nome"]}</h3><p>{o["medidas"]}</p></a>' for o in outros)
    nota_foto = ('' if t['foto'] else
                 '<p class="nota reveal">Imagem ilustrativa: a fotografia oficial deste '
                 'moldado ainda não faz parte do banco de imagens da marca.</p>')

    return head(p, title, desc, canon, img, 'product', ld) + f'''
<body class="interna">
{header(p)}
<main id="main">

<section class="section pdp" aria-labelledby="pdp-title">
  <div class="wrap">
    <nav class="crumbs" aria-label="Trilha de navegação">
      <ol>
        <li><a href="{p}index.html">Início</a></li>
        <li><a href="{p}index.html#travesseiros">Travesseiros</a></li>
        <li><span aria-current="page">{nome}</span></li>
      </ol>
    </nav>

    <div class="pdp-grid">
      <figure class="pdp-media">
        <img src="{p}assets/travesseiros/{slug}.jpg"
             alt="Travesseiro Hauzestern {nome}"
             width="960" height="720" fetchpriority="high">
      </figure>

      <div class="pdp-info">
        <p class="eyebrow">{eyebrow}</p>
        <h1 id="pdp-title" class="display">Travesseiro {nome}</h1>
        <p class="pdp-sub">{t['medidas']}</p>
        {poetica}
        <ul class="specs pdp-quick">
          <li><strong>Medidas</strong><span>{t['medidas']}</span></li>
          {sig}
        </ul>
        <div class="pdp-cta">
          <a class="btn btn-dark" href="{p}representantes.html">Onde comprar</a>
          <a class="btn btn-ghost-dark" href="{TEL_HREF}">{TEL_TXT}</a>
        </div>
        {nota_foto}
      </div>
    </div>
  </div>
</section>

<section class="section pdp-camadas" aria-labelledby="cam-title">
  <div class="wrap narrow">
    <p class="eyebrow reveal">Composição</p>
    <h2 id="cam-title" class="display reveal">O que tem dentro</h2>
    <ul class="lista-cuidados reveal">
        {ficha}
    </ul>
    {sem_texto}
  </div>
</section>
{bloco_garantia(p, 'travesseiro')}
<section class="section pdp-rel" aria-labelledby="rel-title">
  <div class="wrap">
    <header class="section-head">
      <div>
        <p class="eyebrow reveal">Complementos</p>
        <h2 id="rel-title" class="display reveal">Outros travesseiros</h2>
      </div>
      <p class="section-note reveal">Cinco modelos, entre fibra PLUME, viscoelástica e látex.</p>
    </header>
    <div class="grid-pillows">
      {rel}
    </div>
  </div>
</section>
{cta(p, nome)}
</main>
{footer(p)}'''


# -------------------------------------------------------------------- escrita
def write(path, txt):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    io.open(full, 'w', encoding='utf-8', newline='\n').write(txt)
    return len(txt)
