# -*- coding: utf-8 -*-
"""
Gera index.html.

Conteudo institucional transcrito de:
  guide_hauzestern/Identidade Visual/Manifesto.pdf
  guide_hauzestern/CATÁLOGO/CATÁLOGO 2026/... (p.2, p.42)
  guide_hauzestern/Produtos/Storytelling Hauzestern 01.09.pdf
  guide_hauzestern/Identidade Visual/BRANDBOOK/... (p.23-38, padrao de loja)

A secao Tecnologias usa o texto que a marca escreveu sobre cada material nas
Fichas Técnica — nada e reescrito aqui. A lista "presente em" e derivada dos
icones do catalogo, modelo por modelo.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

import dados
from build_pages import head, header, footer, write, SITE, IG, esc, paras, TEL_HREF, TEL_TXT

P = ''

# Bloco "Lançamento" da home: o modelo mais recente. Texto e selo saem de
# dados.py (poetica + tecnica, verbatim da marca); so a descricao da foto e daqui.
# Era o Wohl ate a chegada do Krefel (09/2026).
LANCAMENTO = 'krefel'
LANCAMENTO_ALT = ('Colchão Hauzestern Krefel, de lateral xadrez, sobre base box '
                  'azul-marinho com pés de madeira')

# os tres icones da faixa amarela — redesenhados a partir do site atual
ICO = {
 'algodao': '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.82" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"> <path d="M 14.43 10.97 A 9.75 9.75 0 0 1 33.57 10.97"/> <path d="M 19.87 12.51 A 10.40 10.40 0 1 0 18.18 31.85"/> <path d="M 28.13 12.51 A 10.40 10.40 0 1 1 29.82 31.85"/> <path d="M 12.60 21.58 C 12.60 27.56 17.44 34.13 24 34.42"/> <path d="M 12.60 21.58 C 15.10 21.95 17.50 22.85 19.44 24.14"/> <path d="M 35.40 21.58 C 35.40 27.56 30.56 34.13 24 34.42"/> <path d="M 35.40 21.58 C 32.90 21.95 30.50 22.85 28.56 24.14"/> <path d="M 24 17.02 C 18.87 22.24 18.87 29.20 24 34.42 C 29.13 29.20 29.13 22.24 24 17.02 Z"/> <path d="M 24 34.42 L 24 44.95"/> </svg>',
 'selo': '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.82" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"> <path d="M 44.00 25.42 Q 45.26 24.00 44.00 22.58 L 41.75 20.06 Q 40.48 18.64 40.67 16.75 L 41.01 13.39 Q 41.20 11.50 39.34 11.10 L 36.04 10.38 Q 34.19 9.98 33.23 8.34 L 31.53 5.42 Q 30.57 3.78 28.83 4.55 L 25.74 5.91 Q 24.00 6.67 22.26 5.91 L 19.17 4.55 Q 17.43 3.78 16.47 5.42 L 14.77 8.34 Q 13.81 9.98 11.96 10.38 L 8.66 11.10 Q 6.80 11.50 6.99 13.39 L 7.33 16.75 Q 7.52 18.64 6.25 20.06 L 4.00 22.58 Q 2.74 24.00 4.00 25.42 L 6.25 27.94 Q 7.52 29.36 7.33 31.25 L 6.99 34.61 Q 6.80 36.50 8.66 36.90 L 11.96 37.62 Q 13.81 38.02 14.77 39.66 L 16.47 42.58 Q 17.43 44.22 19.17 43.45 L 22.26 42.09 Q 24.00 41.33 25.74 42.09 L 28.83 43.45 Q 30.57 44.22 31.53 42.58 L 33.23 39.66 Q 34.19 38.02 36.04 37.62 L 39.34 36.90 Q 41.20 36.50 41.01 34.61 L 40.67 31.25 Q 40.48 29.36 41.75 27.94 Z"/> <circle cx="24" cy="24" r="11.54"/> <path d="M 24.15 18.10 L 22.28 21.88 L 18.11 22.49 L 21.13 25.43 L 20.42 29.59 L 24.15 27.63 L 27.88 29.59 L 27.17 25.43 L 30.19 22.49 L 26.02 21.88 Z" fill="currentColor" stroke-width="0.5"/> </svg>',
 'agulha': '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.82" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"> <path d="M 32.72 3.48 C 34.60 5.60 37.80 7.90 39.30 9.70 C 40.45 11.30 38.70 12.25 36.15 11.85 C 35.10 11.70 34.05 11.40 32.99 11.16 L 25.14 11.17 A 16.99 16.99 0 0 0 19.95 44.60"/> <path d="M 13.91 36.83 L 36.45 6.78 L 38.15 8.04 Z"/> <ellipse cx="38.11" cy="6.31" rx="1.05" ry="2.10" transform="rotate(36.4 38.11 6.31)"/> </svg>',
}

PROCESSO = [
    ('1.jpg', 'Montagem do molejo ensacado na linha de produção'),
    ('2.jpg', 'A encapsuladora fecha as molas, uma a uma'),
    ('3.jpg', 'Costura do tampo, guiada à mão'),
    ('4.jpg', 'Camadas de espuma prontas para a laminação'),
]


def modelos_com(*termos):
    """Modelos cujos ícones do catálogo contêm um dos termos. Derivado dos dados."""
    out = []
    for m in dados.COLCHOES:
        alvo = ' | '.join(m['badges']).lower()
        if any(t.lower() in alvo for t in termos):
            out.append(m['nome'])
    return out


# Tecnologias — texto verbatim das Fichas Técnica / catálogo 2026.
# (titulo, texto, termos para achar em quais modelos aparece)
TECNOLOGIAS = [
 ('Molas ensacadas', dados.MOLAS_ENSACADAS_TXT, ('Molas Ensacada',)),
 ('Molas MaxSpring', dados.MAXSPRING_TXT, ('Maxspring',)),
 ('Duplo molejo',
  'O sistema de duplo molejo ajusta perfeitamente o colchão às suas necessidades de '
  'sono. O sistema independente de molas ensacadas combinado com a mola Maxspring '
  'garante um alto nível de conforto e maciez.',
  ('Maxspring',)),
 ('Trizone',
  'O sistema de zoneamento de molas ensacadas (trizone) permite a correta distribuição '
  'do peso durante o uso. As áreas de maior impacto recebem uma camada de molas mais '
  'firmes, já as áreas de menor impacto recebem molas com arame de diâmetro menor.',
  ('Trizone',)),
 ('Micro molas ensacadas',
  'Camada de 400 molas p/m² de fio de aço especial ATC de 1,30 mm, posicionada acima do '
  'sistema de molejo principal do colchão. Por serem menores e ensacadas '
  'individualmente, as micro molas distribuem o peso de forma correta, reduzem os '
  'pontos de pressão e respondem de maneira independente aos movimentos.',
  ('Micro Molas',)),
 ('Sistema Thermo Flow',
  'Camada projetada com uma série de canais que facilitam a passagem do ar, em um '
  'colchão de aquecimento a ar multifuncional com acionamento por controle remoto. '
  'Tem três modos: ventilação quente ajustável de 20 a 37 °C, ventilação natural e '
  'desumidificação com eliminação de ácaros.',
  ('Thermo Flow',)),
 ('Espuma Viscogel',
  'Caracterizada principalmente por sua viscosidade, permite que a espuma se molde aos '
  'contornos do corpo. Enquanto a propriedade do gel auxilia no equilíbrio das '
  'temperaturas do colchão.',
  ('Viscogel',)),
 ('Espuma HR Special®',
  'Tem por característica maior resiliência e capacidade de sustentação, proporcionando '
  'aporte entre os molejos e a camada superior de toque extremamente macio.',
  ('HR Special',)),
 ('Espuma Freshcool®',
  'Uma espuma especial, desenvolvida com células mais abertas, resultando em uma maior '
  'ventilação e aeração ao produto e gerando uma sensação de maior frescor.',
  ('Freshcool',)),
 ('CloudCore™ Comfort System',
  'Espuma de alta resiliência que combina maciez, adaptação e suporte inteligente. '
  'Adapta-se ao corpo, aliviando pontos de pressão e proporcionando uma sensação '
  'acolhedora, semelhante à leveza de uma nuvem.',
  ('CloudCORE',)),
 ('Espuma viscoelástica',
  'Tem por característica principal sua maciez e viscosidade, permitindo a espuma se '
  'moldar ao corpo, garantindo um sono mais tranquilo e reparador.',
  ('Viscoelástica',)),
 ('Viscoelástica com carvão ativado',
  'Caracterizada por sua porosidade, permite a adsorção e retenção de impurezas pelas '
  'micropartículas de carvão, garantindo um interior livre de contaminantes e bactérias.',
  ('Carvão Ativado',)),
 ('Premium Foam®',
  'Essa espuma de poliuretano apresenta um melhor desempenho em termos de suporte, '
  'complementada pela resiliência da espuma HR, que possui maior capacidade de retorno, '
  'proporcionando aporte entre o molejo e as camadas superiores.',
  ('Premium Foam', 'PremiumFoam')),
 # so 'Flexxi': o texto e da manta de 8 cm em copos do Frost. O Krefel tambem
 # tem latex natural, mas em camada de 2 cm — nao e o que este card descreve.
 ('Látex natural e Flexxi Cup',
  'A manta de látex de 8 cm em formato de copos garante um conforto individualizado, '
  'acomodando naturalmente o corpo. Essa camada gera um efeito de duplo molejo, '
  'aumentando ainda mais a sensação de relaxamento.',
  ('Flexxi',)),
 ('Tecido Pure Silk',
  'Malha com alto percentual de viscose e seda. A viscose é caracterizada pelas '
  'propriedades termorreguladoras que auxiliam no conforto durante o sono. O toque macio '
  'e acolhedor é proporcionado pela seda agregada neste tecido.',
  ('Pure Silk',)),
 ('Malha PeachSkin em bioamida',
  'A bioamida é fabricada a partir de biomassa vegetal, garantindo um toque macio, '
  'delicado e sedoso, e aumentando a resistência do tecido. Além de sustentável, deixa o '
  'tecido com toque fresco, auxiliando a termorregulação corporal. O tratamento Peachskin '
  'garante mais suavidade e conforto à pele.',
  ('PeachSkin',)),
 ('Tecido malha com linho',
  'Malha jacquard com alto percentual de viscose e linho. A viscose garante um toque '
  'macio, além de propriedades termorreguladoras. Este tecido conta com tratamento à base '
  'de íons de prata que proporciona efeitos antimicrobianos.',
  ('com Linho', 'Tecido Linho')),
 ('Pillow Top One Side', dados.ONE_SIDE_TXT, ('One Side',)),
]


def cards_colchoes(cs):
    out = []
    for m in cs:
        flag = f'<span class="card-flag">{m["destaque"]}</span>' if m.get('destaque') else ''
        out.append(
            f'<a class="card reveal" href="colchoes/{m["slug"]}.html">{flag}'
            f'<figure><img src="assets/produtos/{m["slug"]}-card.jpg" '
            f'alt="Colchão Hauzestern {m["nome"]}" width="640" height="480" loading="lazy">'
            f'</figure><h3>{m["nome"]}</h3>'
            f'<p>{m["altura"]} cm · {dados.resumo(m)}</p></a>')
    return '\n        '.join(out)


def build():
    title = 'Hauzestern Colchões | Colchões premium com herança alemã — Grupo Herval'
    desc = (f'Hauzestern é a marca de colchões premium do Grupo Herval. '
            f'{len(dados.COLCHOES)} colchões em três coleções, {len(dados.BASES)} bases e '
            f'{len(dados.TRAVESSEIROS)} travesseiros — com molas ensacadas, duplo molejo e '
            f'espumas técnicas.')
    canon = SITE + '/'

    ld = [{
        '@context': 'https://schema.org', '@type': 'Organization',
        'name': 'Hauzestern Colchões', 'url': canon,
        'logo': f'{SITE}/assets/brand/marca-positivo.svg',
        'image': f'{SITE}/assets/produtos/wohl-cinza.jpg',
        'description': 'Marca de colchões premium do Grupo Herval, de Dois Irmãos (RS).',
        'parentOrganization': {'@type': 'Organization', 'name': 'Grupo Herval'},
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Dois Irmãos',
                    'addressRegion': 'RS', 'addressCountry': 'BR'},
        'telephone': '+55-51-3564-8300',
        'contactPoint': {'@type': 'ContactPoint', 'telephone': '+55-51-3564-8300',
                         'contactType': 'customer service', 'areaServed': 'BR',
                         'availableLanguage': 'Portuguese'},
        'sameAs': [IG],
    }, {
        '@context': 'https://schema.org', '@type': 'ItemList',
        'name': 'Produtos Hauzestern',
        'itemListOrder': 'https://schema.org/ItemListOrderAscending',
        'numberOfItems': (len(dados.COLCHOES) + len(dados.BASES)
                          + len(dados.TRAVESSEIROS)),
        'itemListElement': (
            [{'@type': 'ListItem', 'position': i,
              'name': f'Colchão Hauzestern {m["nome"]}',
              'url': f'{SITE}/colchoes/{m["slug"]}.html'}
             for i, m in enumerate(dados.COLCHOES, 1)]
            + [{'@type': 'ListItem', 'position': len(dados.COLCHOES) + i,
                'name': f'{b["nome"]} Hauzestern',
                'url': f'{SITE}/bases/{b["slug"]}.html'}
               for i, b in enumerate(dados.BASES, 1)]
            + [{'@type': 'ListItem',
                'position': len(dados.COLCHOES) + len(dados.BASES) + i,
                'name': f'Travesseiro Hauzestern {t["nome"]}',
                'url': f'{SITE}/travesseiros/{t["slug"]}.html'}
               for i, t in enumerate(dados.TRAVESSEIROS, 1)]
        ),
    }]

    # ---------------------------------------------------------- coleções
    colecoes_html = ''
    for key in ('elementos', 'propositos', 'raizes'):
        c = dados.COLECOES[key]
        membros = [m for m in dados.COLCHOES if m['colecao'] == key]
        colecoes_html += f'''
    <div class="colecao" id="colecao-{key}">
      <header class="colecao-head reveal">
        <h3>Coleção {c['nome']}</h3>
        <p>{c['resumo']}</p>
      </header>
      <div class="grid-products">
        {cards_colchoes(membros)}
      </div>
    </div>'''

    travesseiros = '\n        '.join(
        f'<a class="card card-sm reveal" href="travesseiros/{t["slug"]}.html">'
        f'<figure><img src="assets/travesseiros/{t["slug"]}-card.jpg" '
        f'alt="Travesseiro Hauzestern {t["nome"]}" width="480" height="360" loading="lazy">'
        f'</figure><h3>{t["nome"]}</h3><p>{t["medidas"]}</p></a>'
        for t in dados.TRAVESSEIROS)

    bases = '\n        '.join(
        f'<a class="card reveal" href="bases/{b["slug"]}.html">'
        + (f'<figure><img src="assets/bases/{b["foto"]}-card.jpg" '
           f'alt="{b["nome"]} Hauzestern" width="640" height="480" loading="lazy"></figure>'
           if b['foto'] else
           '<figure class="card-vazia"><img src="assets/brand/simbolo-positivo.svg" '
           'alt="" width="479" height="572" loading="lazy"></figure>')
        + f'<h3>{b["nome"]}</h3><p>Box {b["box"]} · pés {b["pes"]} · '
          f'{b["material"].replace("Pés de ", "").capitalize()}</p></a>'
        for b in dados.BASES)

    processo = '\n        '.join(
        f'<figure class="reveal"><img src="assets/processo/{f}" alt="{esc(cap)}" '
        f'width="1200" height="800" loading="lazy"><figcaption>{cap}</figcaption></figure>'
        for f, cap in PROCESSO)

    tec = []
    for i, (n, d, termos) in enumerate(TECNOLOGIAS, 1):
        modelos = modelos_com(*termos)
        onde = ''
        if modelos and len(modelos) < len(dados.COLCHOES):
            plural = 'modelo' if len(modelos) == 1 else 'modelos'
            onde = (f'<p class="tech-onde">Em {len(modelos)} {plural}: '
                    f'{", ".join(modelos)}</p>')
        elif modelos:
            onde = f'<p class="tech-onde">Em todos os {len(dados.COLCHOES)} colchões</p>'
        tec.append(f'<article class="tech-card reveal"><span class="num">{i:02d}</span>'
                   f'<h3>{n}</h3><p>{d}</p>{onde}</article>')
    tec = '\n        '.join(tec)

    g = dados.GARANTIA
    lanc = next(m for m in dados.COLCHOES if m['slug'] == LANCAMENTO)

    return head(P, title, desc, canon, 'assets/produtos/wohl-cinza.jpg', 'website', ld) + f'''
<body>
{header(P, interna=False)}
<main id="main">

<!-- ============================= HERO ============================= -->
<section class="hero" aria-labelledby="hero-title">
  <img class="hero-bg" src="assets/hero-frankfurt.jpg" alt="" aria-hidden="true" width="1920" height="568">

  <div class="wrap hero-inner">
    <div class="hero-content">
      <p class="eyebrow light reveal">Zuhause + stern — lar + estrela</p>
      <h1 id="hero-title" class="reveal">A casa das estrelas</h1>
      <p class="lede reveal">Sob o céu noturno de cada lar brilha a estrela mais especial:
        o colchão. Hauzestern é a marca de colchões premium do Grupo Herval — 60 anos de
        tradição em Dois Irmãos, no Rio Grande do Sul.</p>
      <div class="hero-cta reveal">
        <a class="btn btn-primary" href="#colchoes">Veja nossas coleções</a>
        <a class="btn btn-ghost" href="#a-marca">A Hauzestern</a>
      </div>
    </div>

    <figure class="hero-media reveal">
      <img src="assets/hero-frankfurt.jpg" alt="Skyline de Frankfurt ao anoitecer, com as torres iluminadas refletidas no rio Main" width="1920" height="568" fetchpriority="high">
      <figcaption class="hero-credit">Frankfurt&nbsp;|&nbsp;Alemanha</figcaption>
    </figure>
  </div>

  <a class="scroll-hint" href="#a-marca" aria-label="Rolar para o conteúdo"><span></span></a>
</section>

<!-- ============================= CONCEITO ============================= -->
<section class="section concept" id="a-marca" aria-labelledby="concept-title">
  <div class="wrap narrow center">
    <img class="simbolo-orn reveal" src="assets/brand/simbolo-positivo.svg" alt="" width="479" height="572">
    <p class="eyebrow reveal">A Hauzestern</p>
    <h2 id="concept-title" class="display reveal">Zuhause <span class="plus">+</span> stern</h2>
    <p class="sub reveal">( LAR &nbsp;+&nbsp; ESTRELA )</p>
    <div class="prose reveal">
      <p>Segundo a ciência, as estrelas são grandes esferas com luz própria, formadas por
        plasma aquecido a milhares de graus, que se mantêm íntegras graças à gravidade e à
        pressão de radiação. Os astrônomos, inclusive, dizem que elas não podem ser
        tocadas. E quem nunca se imaginou tocando uma delas?</p>
      <p>É essa sensação de estar próximo de algo tão incrível que esperamos proporcionar a
        você, como se pudéssemos transformar o seu lar na casa das estrelas, aproximando
        sonho e realidade.</p>
      <p>Exclusivo, forte e repleto de significado, o nome Hauzestern foi desenvolvido a
        partir da combinação de <em>Zuhause</em> — lar — e <em>stern</em> — estrela.
        O idioma alemão foi escolhido como forma de homenagear as origens da cidade em que
        o Grupo Herval nasceu e se consolidou.</p>
      <p>Localizado em Dois Irmãos, uma das regiões colonizadas pelos alemães no Rio Grande
        do Sul, o Grupo Herval tem 60 anos de tradição na produção de móveis e colchões.
        Com a qualidade e a precisão típicas da indústria alemã, os colchões Hauzestern são
        feitos para os sonos mais exigentes.</p>
    </div>
  </div>
</section>

<!-- ============================= PILARES ============================= -->
<section class="pillars" aria-label="Diferenciais Hauzestern">
  <div class="wrap pillars-grid">
    <article class="pillar reveal">
      {ICO['algodao']}
      <h3>Matérias-primas selecionadas</h3>
      <p>Vindas dos principais fabricantes do mundo, proporcionam muito mais qualidade e
        durabilidade aos nossos colchões.</p>
    </article>
    <article class="pillar reveal">
      {ICO['selo']}
      <h3>Primor em cada processo</h3>
      <p>Produtos de alto valor agregado, compostos por matérias-primas selecionadas,
        tecnologias inovadoras e design único e exclusivo.</p>
    </article>
    <article class="pillar reveal">
      {ICO['agulha']}
      <h3>Qualidade que é herança alemã</h3>
      <p>Projetados por especialistas e desenvolvidos a partir dos mais rigorosos padrões
        de qualidade alemão.</p>
    </article>
  </div>
</section>

<!-- ============================= LANÇAMENTO ============================= -->
<section class="section launch" aria-labelledby="launch-title">
  <div class="wrap launch-grid">
    <figure class="launch-media reveal">
      <img src="assets/produtos/{lanc['slug']}-cinza.jpg" alt="{esc(LANCAMENTO_ALT)}"
           width="1400" height="1050" loading="lazy">
    </figure>
    <div class="launch-text reveal">
      <span class="badge">{lanc['destaque']}</span>
      <h2 id="launch-title" class="display">{lanc['nome']}</h2>
      <p class="sub left">Coleção {dados.COLECOES[lanc['colecao']]['nome']} · {lanc['altura']} cm</p>
      <p>{lanc['poetica']}</p>
      {paras(lanc['tecnica'])}
      <a class="link-arrow" href="colchoes/{lanc['slug']}.html">Conhecer o {lanc['nome']} <span aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
</section>

<!-- ============================= PROCESSO ============================= -->
<section class="section processo" id="processo" aria-labelledby="proc-title">
  <div class="wrap">
    <header class="section-head">
      <div>
        <p class="eyebrow light reveal">Como fazemos</p>
        <h2 id="proc-title" class="display reveal">Primor em cada processo</h2>
      </div>
      <p class="section-note reveal">Dois Irmãos, Rio Grande do Sul. O primor em cada
        processo é qualidade de herança alemã.</p>
    </header>
    <div class="grid-processo">
        {processo}
    </div>
  </div>
</section>

<!-- ============================= COLCHÕES ============================= -->
<section class="section products" id="colchoes" aria-labelledby="products-title">
  <div class="wrap">
    <header class="section-head stack">
      <div>
        <p class="eyebrow reveal">Catálogo</p>
        <h2 id="products-title" class="display reveal">Três coleções, diferentes formas de viver o conforto</h2>
      </div>
      <div class="section-note reveal">
        <p>Na Hauzestern, cada colchão nasce da combinação entre design, tecnologia e
          conforto, traduzindo uma inspiração alemã em experiências de descanso pensadas
          para diferentes estilos e necessidades.</p>
        <p>Nossas coleções apresentam propostas distintas, com materiais, tecnologias e
          sensações cuidadosamente selecionados para proporcionar uma experiência de
          conforto única. Do toque dos tecidos à composição interna de cada produto, cada
          detalhe é pensado para transformar o momento de descanso.</p>
        <p>Descubra as coleções Hauzestern e encontre o colchão que traduz a sua forma de
          descansar.</p>
      </div>
    </header>
    {colecoes_html}
  </div>
</section>

<!-- ============================= BASES ============================= -->
<section class="section boxes" id="bases" aria-labelledby="boxes-title">
  <div class="wrap">
    <header class="section-head">
      <div>
        <p class="eyebrow reveal">Complementos</p>
        <h2 id="boxes-title" class="display reveal">Bases</h2>
      </div>
      <p class="section-note reveal">Seis modelos de box, de 15 a 28 cm de altura, todos
        com estrutura em madeira de eucalipto de reflorestamento. A base correta é
        condição de garantia do colchão.</p>
    </header>
    <div class="grid-products">
        {bases}
    </div>
  </div>
</section>

<!-- ============================= TRAVESSEIROS ============================= -->
<section class="section pillows" id="travesseiros" aria-labelledby="pillows-title">
  <div class="wrap">
    <header class="section-head">
      <div>
        <p class="eyebrow reveal">Complementos</p>
        <h2 id="pillows-title" class="display reveal">Travesseiros</h2>
      </div>
      <p class="section-note reveal">Cinco modelos, entre fibra PLUME, viscoelástica e
        látex. Alpen, Harz e Weich seguem as coleções dos colchões.</p>
    </header>
    <div class="grid-pillows">
        {travesseiros}
    </div>
  </div>
</section>

<!-- ============================= TECNOLOGIAS ============================= -->
<section class="section tech" id="tecnologias" aria-labelledby="tech-title">
  <div class="wrap">
    <header class="section-head">
      <div>
        <p class="eyebrow light reveal">Engenharia do descanso</p>
        <h2 id="tech-title" class="display reveal">Tecnologias</h2>
      </div>
      <p class="section-note reveal">Como a marca descreve cada sistema e material, e em
        quais modelos eles aparecem.</p>
    </header>

    <div class="grid-tech">
        {tec}
    </div>
  </div>
</section>

<!-- ============================= GARANTIA ============================= -->
<section class="section pdp-garantia" aria-labelledby="gar-home-title">
  <div class="wrap">
    <div class="garantia-box reveal">
      <div class="garantia-selo" aria-hidden="true">
        <img src="assets/brand/simbolo-positivo.svg" alt="" width="479" height="572" loading="lazy">
      </div>
      <div class="garantia-txt">
        <p class="eyebrow">Garantia Hauzestern</p>
        <h2 id="gar-home-title" class="display">Molejo {g['molejo']}, demais componentes {g['componentes']}</h2>
        <p>Garantia de Fábrica de acordo com o Código de Defesa do Consumidor e as normas
          da ABNT. A página de garantia traz os prazos por componente, os cuidados de uso,
          o que não é coberto e a tabela de biotipos que orienta a densidade certa para
          cada pessoa.</p>
        <a class="link-arrow" href="garantia.html">Ler a garantia completa <span aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </div>
</section>

<!-- ============================= CONTATO ============================= -->
<section class="section contact" id="contato" aria-labelledby="contact-title">
  <div class="wrap narrow center">
    <p class="eyebrow light reveal">Contato</p>
    <h2 id="contact-title" class="display reveal">Vamos conversar</h2>
    <p class="lede reveal">Dúvidas sobre modelos, biotipo, garantia ou revenda: o nosso
      time responde.</p>
    <div class="contact-channels reveal">
      <a class="channel" href="representantes.html">
        <span class="channel-label">Representantes</span>
        <span class="channel-value">Quem atende a sua região</span>
      </a>
      <a class="channel" href="{TEL_HREF}">
        <span class="channel-label">Telefone</span>
        <span class="channel-value">{TEL_TXT}</span>
      </a>
      <a class="channel" href="{IG}" target="_blank" rel="noopener">
        <span class="channel-label">Instagram</span>
        <span class="channel-value">@hauzestern</span>
      </a>
    </div>
  </div>
</section>

</main>
{footer(P)}'''


if __name__ == '__main__':
    n = write('index.html', build())
    print(f'index.html  {n//1024}KB')
