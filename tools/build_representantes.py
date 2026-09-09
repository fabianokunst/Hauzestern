# -*- coding: utf-8 -*-
"""
Gera representantes.html a partir de representantes.csv.

Uso:  python tools/build_all.py

Esta pagina substituiu o bloco "Onde encontrar" da home: quem procura onde
comprar fala com o representante da sua regiao. O conteudo inteiro vem de
tools/dados_representantes.py — este arquivo so decide COMO mostrar.

    python tools/build_representantes.py     # so esta pagina
"""
import os, sys, io, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

import build_pages as BP
import dados_representantes as DR

P = ''                       # pagina na raiz: sem prefixo de caminho
URL = BP.SITE + '/representantes.html'

TITULO = 'Representantes Hauzestern — contatos por estado | Hauzestern Colchões'
DESCRICAO = ('Encontre o representante comercial Hauzestern do seu estado: '
             'telefone, e-mail e área de atuação em todo o Brasil, dos '
             'escritórios próprios às representações parceiras.')


def sem_acento(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s or '')
                   if unicodedata.category(c) != 'Mn')


def slug(s):
    s = sem_acento(s).lower()
    return ''.join(c if c.isalnum() else '-' for c in s).strip('-')


# ----------------------------------------------------------------- contatos
def canais(c):
    itens = []
    for f in c['fones']:
        rot = (f' <span class="rep-rotulo">{BP.esc(f["rotulo"])}</span>'
               if f.get('rotulo') else '')
        itens.append(f'<li><a class="rep-tel" href="tel:{f["tel"]}">'
                     f'{f["txt"]}</a>{rot}</li>')
    for e in c['emails']:
        itens.append(f'<li><a class="rep-mail" href="mailto:{e}">'
                     f'{BP.esc(e)}</a></li>')
    if not itens:
        return ''
    return ('\n          <ul class="rep-canais">\n            '
            + '\n            '.join(itens) + '\n          </ul>')


def contato(c):
    papel = c['papel'] + (f' · {c["setor"]}' if c.get('setor') else '')
    nomes = ''.join(f'\n          <p class="rep-nome">{BP.esc(n)}</p>'
                    for n in c['nomes'])
    return (f'''<li class="rep-contato" data-papel="{slug(c['papel'])}">
          <p class="rep-papel">{BP.esc(papel)}</p>{nomes}{canais(c)}
        </li>''')


# --------------------------------------------------------------------- card
def card(r):
    """Um card por linha do CSV — uma area de atuacao dentro do estado."""
    termos = [r['uf'], r['estado'], r['atuacao'], r['equipe']]
    for c in r['contatos']:
        termos += [c['papel'], c.get('setor') or ''] + c['nomes'] + c['emails']
        termos += [f['txt'] for f in c['fones']]
        termos += [f['tel'].lstrip('+') for f in c['fones']]   # busca por digitos
    busca = sem_acento(' '.join(t for t in termos if t)).lower()
    contatos = '\n        '.join(contato(c) for c in r['contatos'])
    return f'''<article class="rep-card reveal" data-rep
             data-uf="{r['uf']}" data-regiao="{slug(r['regiao'])}"
             data-busca="{BP.esc(busca)}">
      <div class="rep-card-head">
        <h4>{BP.esc(r['atuacao'])}</h4>
        <p class="rep-equipe">{BP.esc(r['equipe'])}</p>
      </div>
      <ul class="rep-contatos">
        {contatos}
      </ul>
    </article>'''


def bloco_estado(uf, estado, registros):
    cards = '\n\n    '.join(card(r) for r in registros)
    return f'''<div class="rep-estado" data-estado id="uf-{uf.lower()}">
    <h3 class="rep-estado-tit"><span>{uf}</span> {estado}</h3>
    {cards}
  </div>'''


def bloco_regiao(regiao, estados):
    blocos = '\n\n  '.join(bloco_estado(*e) for e in estados)
    sl = slug(regiao)
    return f'''
<section class="rep-regiao" data-regiao-bloco="{sl}"
         id="regiao-{sl}" aria-labelledby="reg-{sl}">
  <div class="wrap">
    <h2 class="rep-regiao-tit" id="reg-{sl}">{regiao}</h2>
    {blocos}
  </div>
</section>'''


# ------------------------------------------------------------------ filtros
def filtros(registros):
    ufs = []
    for regiao, ufs_regiao in DR.REGIOES:
        for uf in ufs_regiao:
            if any(r['uf'] == uf for r in registros):
                ufs.append(uf)
    opcoes = '\n          '.join(
        f'<option value="{uf}">{uf} — {DR.UF_NOME[uf]}</option>'
        for uf in sorted(ufs))
    chips = '\n        '.join(
        f'<button type="button" class="rep-chip" data-filtro-regiao="{slug(n)}">'
        f'{n}</button>' for n, _ in DR.REGIOES)
    return f'''
<section class="rep-filtros" aria-label="Filtrar representantes">
  <div class="wrap rep-filtros-inner">
    <div class="rep-campo">
      <label for="rep-busca">Buscar</label>
      <input type="search" id="rep-busca" name="rep-busca" autocomplete="off"
             placeholder="Estado, região, empresa ou nome">
    </div>
    <div class="rep-campo rep-campo-uf">
      <label for="rep-uf">Estado</label>
      <select id="rep-uf" name="rep-uf">
        <option value="">Todos os estados</option>
          {opcoes}
      </select>
    </div>
    <div class="rep-chips" role="group" aria-label="Filtrar por região">
        <button type="button" class="rep-chip is-on" data-filtro-regiao="">Brasil</button>
        {chips}
    </div>
    <p class="rep-contagem" id="rep-contagem" role="status" aria-live="polite"></p>
  </div>
</section>'''


# -------------------------------------------------------------------- build
def build():
    registros = DR.carregar()
    por_regiao = DR.por_regiao(registros)
    n_ufs = len({r['uf'] for r in registros})
    n_areas = len(registros)

    ld_pagina = {
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        'name': 'Representantes Hauzestern',
        'url': URL,
        'description': DESCRICAO,
        'inLanguage': 'pt-BR',
        'isPartOf': {'@type': 'WebSite', 'name': 'Hauzestern Colchões',
                     'url': BP.SITE + '/'},
        'publisher': {
            '@type': 'Organization',
            'name': 'Hauzestern Colchões',
            'parentOrganization': {'@type': 'Organization', 'name': 'Grupo Herval'},
        },
    }
    ld_trilha = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início',
             'item': BP.SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Representantes'},
        ],
    }

    regioes = '\n'.join(bloco_regiao(*x) for x in por_regiao)

    return f'''{BP.head(P, TITULO, DESCRICAO, URL,
                        'assets/brand/marca-positivo.svg',
                        ld=(ld_pagina, ld_trilha))}
<body class="interna">
{BP.header(P)}
<main id="main">

<!-- ============================= ABERTURA ============================= -->
<section class="rep-hero" aria-labelledby="rep-title">
  <div class="wrap rep-hero-inner">
    <div class="rep-hero-txt">
      <p class="eyebrow light">Rede comercial</p>
      <h1 id="rep-title">Fale com o representante da sua região</h1>
      <p class="rep-hero-sub">Escritórios próprios do Grupo Herval e representações
        parceiras — busque abaixo quem atende o seu estado.</p>
    </div>
    <dl class="rep-resumo">
      <div><dt>Cobertura</dt><dd>{n_ufs} estados</dd></div>
      <div><dt>Áreas de atuação</dt><dd>{n_areas} equipes</dd></div>
      <div><dt>Fábrica</dt><dd>Dois Irmãos — RS</dd></div>
    </dl>
  </div>
</section>

{filtros(registros)}

<div class="rep-lista" id="rep-lista">
{regioes}

  <p class="rep-vazio" id="rep-vazio" hidden>
    Nenhum representante encontrado para essa busca.
    <button type="button" class="link-arrow" data-limpar>Limpar filtros</button>
  </p>
</div>

<!-- ============================= NA LOJA ============================= -->
<section class="section rep-loja" aria-labelledby="loja-title">
  <div class="wrap where-grid">
    <div class="reveal">
      <p class="eyebrow">Na loja</p>
      <h2 id="loja-title" class="display">O ponto de venda Hauzestern</h2>
      <p>Nas lojas com o projeto Hauzestern, a exposição segue um padrão
        próprio: fachada em ACM preto fosco com letreiro em LED, sete conjuntos
        de cama box em exposição e cabeceiras em tela tensionada iluminada.</p>
      <p>Quer levar a marca para a sua loja? O representante da sua região
        apresenta a linha, as condições comerciais e o projeto de exposição.</p>
      <div class="where-cta">
        <a class="btn btn-primary" href="{BP.TEL_HREF}">Ligar: {BP.TEL_TXT}</a>
      </div>
    </div>
    <ul class="where-list reveal">
      <li><strong>Fábrica</strong><span>Dois Irmãos • Rio Grande do Sul</span></li>
      <li><strong>Grupo</strong><span>Herval • 60 anos em móveis e colchões</span></li>
      <li><strong>Coleções</strong><span>Elementos • Propósitos • Raízes</span></li>
      <li><strong>Linha</strong><span>14 colchões • 6 bases • 5 travesseiros</span></li>
    </ul>
  </div>
</section>

</main>
{BP.footer(P)}'''


if __name__ == '__main__':
    n = BP.write('representantes.html', build())
    print('representantes.html  %dKB' % (n // 1024))
    if DR.AVISOS:
        print('\navisos de dados (%d):' % len(set(DR.AVISOS)))
        for a in sorted(set(DR.AVISOS)):
            print('  ' + a)
