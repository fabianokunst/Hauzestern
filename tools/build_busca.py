# -*- coding: utf-8 -*-
"""
Gera js/busca-index.js, o índice da busca de produtos (lupa do header).

    python tools/build_all.py        (já inclui este passo)

O índice é só o texto que as páginas de produto já mostram, tirado de
tools/dados.py — nada é escrito aqui. Cada produto vira uma entrada com o
texto separado em quatro pesos, e o js/busca.js pontua pelo lugar onde o
termo aparece:

  n  nome ............. "Colchão Gipfel", "Box C1705", "Travesseiro MH 7618"
  k  identidade ....... código/referência, coleção e significado do nome
  f  características .. tecnologias, camadas, altura, capacidade, suporte,
                        medidas, pés, ficha, garantia
  x  descrição ........ textos poético, técnico, de diferenciais e de molejo

É um .js e não um .json porque o site também precisa funcionar aberto
direto do disco (file://), onde o navegador bloqueia fetch() de arquivo
local; um <script> injetado carrega nos dois casos.

Campo novo em dados.py que este arquivo ainda não conhece entra sozinho em
"características" (ou em "identidade", se for código) e o build avisa, para
decidir depois se ele merece tratamento próprio.
"""
import os, sys, re, json, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dados

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO = 'js/busca-index.js'
SEM_FOTO = 'assets/brand/simbolo-positivo.svg'

# chaves que guardam código do produto: peso de identidade, não de característica
CODIGO = ('ref', 'codigo', 'cod', 'sku', 'referencia')

# Termos da busca vazia. Não são texto de marca, são atalhos para o que já
# existe nas páginas; o build confere que cada um encontra produto.
SUGESTOES = ['Molas ensacadas', 'Maxspring', 'Látex', 'Viscoelástica',
             'Carvão ativado', 'Thermo Flow', 'Pés de ferro', 'MH 7618']


def textos(v):
    """Achata um valor de dados.py em linhas de texto."""
    if v is None or isinstance(v, bool):
        return []
    if isinstance(v, (int, float)):
        return [str(v)]
    if isinstance(v, str):
        return [v] if v.strip() else []
    if isinstance(v, dict):
        return [t for x in v.values() for t in textos(x)]
    if isinstance(v, tuple) and len(v) == 2 and all(isinstance(x, str) for x in v):
        # par (rótulo, valor) das especificações: uma linha só
        return [f'{v[0]}: {v[1]}']
    if isinstance(v, (list, tuple)):
        return [t for x in v for t in textos(x)]
    return []


def colecao(p):
    """'Coleção Elementos (céu)' — o mesmo formato da linha Coleção da página."""
    col = dados.COLECOES.get(p.get('colecao') or '')
    if not col:
        return ''
    sig = p.get('significado')
    return f'Coleção {col["nome"]}' + (f' ({sig})' if sig else '')


def thumb(caminho):
    return caminho if caminho and os.path.exists(os.path.join(ROOT, caminho)) else None


def colchao(m):
    g = dados.GARANTIA
    col = dados.COLECOES[m['colecao']]['nome']
    sis = m.get('sistema') or {}
    f = list(m['badges'])
    f += [f'Altura {m["altura"]} cm',
          f'Capacidade {m["capacidade"]} kg por pessoa',
          f'{len(m["camadas"])} camadas']
    f += m['camadas'] + m['suporte']
    if m.get('molejo2'):
        f.append(m.get('molejo2_titulo', 'Molas MaxSpring'))
    if m.get('molejo') and m.get('molejo2'):
        f.append('Duplo molejo: os dois sistemas trabalham juntos neste modelo.')
    if sis:
        f.append(sis['nome'])
    if m.get('destaque'):
        f.append(m['destaque'])
    f.append(f'Garantia: molejo {g["molejo"]}, demais componentes {g["componentes"]}')

    x = [m['poetica']] + m['tecnica'] + m['diferenciais']
    x += textos(m.get('molejo')) + textos(m.get('molejo2'))
    x += textos({k: v for k, v in sis.items() if k != 'nome'})
    x += textos(m.get('cuidados_extra'))

    e = {
        'u': f'colchoes/{m["slug"]}.html',
        't': f'Colchão {m["nome"]}',
        'g': 'Colchões',
        'c': f'Coleção {col}',
        'd': f'{m["altura"]} cm · até {m["capacidade"]} kg por pessoa',
        'i': thumb(f'assets/produtos/{m["slug"]}-card.jpg'),
        'flag': m.get('destaque', ''),
        'n': [f'Colchão {m["nome"]}'],
        'k': [colecao(m)],
        'f': f, 'x': x,
    }
    usadas = {'slug', 'nome', 'colecao', 'significado', 'altura', 'capacidade',
              'suporte', 'diagrama', 'destaque', 'lifestyle', 'poetica', 'tecnica',
              'diferenciais', 'molejo', 'molejo2', 'molejo2_titulo', 'badges',
              'camadas', 'sistema', 'cuidados_extra'}
    return e, usadas


def base(b):
    g = dados.GARANTIA
    f = [f'Altura do box {b["box"]}', f'Altura dos pés {b["pes"]}', b['material'],
         'Estrutura em eucalipto, forro de TNT',
         f'Garantia: box rígido {g["box_rigido"]}']
    if b.get('suporte'):
        f.append(f'Suporte: box rígido, {b["suporte"]}')
    f += textos(b.get('nota_conflito'))
    x = textos(b.get('poetica'))
    if b['ficha']:
        x += [f'{b["ref"]} {dados.BASE_SUPORTE_TXT}',
              dados.BASE_ESTRUTURA, dados.BASE_REVESTIMENTO]

    foto = thumb(f'assets/bases/{b["foto"]}-card.jpg') if b['foto'] else None
    e = {
        'u': f'bases/{b["slug"]}.html',
        't': b['nome'],
        'g': 'Bases',
        'c': colecao(b).split(' (')[0],
        'd': f'Box {b["box"]} · pés {b["pes"]}',
        'i': foto,
        'n': [b['nome'], 'Base box'],
        'k': [f'Referência {b["ref"]}', colecao(b)],
        'f': f, 'x': x,
    }
    usadas = {'slug', 'nome', 'ref', 'colecao', 'significado', 'foto', 'ficha',
              'box', 'pes', 'material', 'suporte', 'poetica', 'nota_conflito'}
    return e, usadas


def travesseiro(t):
    col = colecao(t)
    e = {
        'u': f'travesseiros/{t["slug"]}.html',
        't': f'Travesseiro {t["nome"]}',
        'g': 'Travesseiros',
        'c': col.split(' (')[0],
        'd': t['medidas'],
        'i': thumb(f'assets/travesseiros/{t["slug"]}-card.jpg'),
        'n': [f'Travesseiro {t["nome"]}'],
        'k': [col],
        'f': [f'Medidas {t["medidas"]}'] + t['ficha'],
        'x': textos(t.get('poetica')),
    }
    usadas = {'slug', 'nome', 'colecao', 'significado', 'medidas', 'foto',
              'poetica', 'ficha'}
    return e, usadas


def sem_acento(s):
    s = unicodedata.normalize('NFKD', s.lower())
    return ''.join(c for c in s if not unicodedata.combining(c))


def palavras(s):
    return re.findall(r'[a-z]+|\d+', sem_acento(s))


def build():
    """Devolve (conteúdo do js, número de produtos, avisos)."""
    avisos, produtos = [], []
    for lista, fn in ((dados.COLCHOES, colchao), (dados.BASES, base),
                      (dados.TRAVESSEIROS, travesseiro)):
        for p in lista:
            e, usadas = fn(p)
            # campo que o gerador ainda não conhece: entra do mesmo jeito
            for k in sorted(set(p) - usadas):
                linhas = textos(p[k])
                if not linhas:
                    continue
                e['k' if k in CODIGO else 'f'] += linhas
                avisos.append(f'campo "{k}" ({p["slug"]}) indexado sem tratamento próprio')
            for nivel in 'nkfx':
                e[nivel] = [s for s in e[nivel] if s]
            produtos.append({k: v for k, v in e.items() if v})

    # cada sugestão precisa encontrar produto, senão a busca vazia mente
    vocab = set()
    for e in produtos:
        for nivel in 'nkfx':
            for s in e.get(nivel, []):
                vocab.update(palavras(s))
    for s in SUGESTOES:
        faltam = [w for w in palavras(s) if w not in vocab and len(w) > 2]
        if faltam:
            avisos.append(f'sugestão "{s}" não encontra produto ({", ".join(faltam)})')
    sugestoes = [s for s in SUGESTOES
                 if all(w in vocab or len(w) <= 2 for w in palavras(s))]

    corpo = json.dumps({'v': 1, 'sugestoes': sugestoes, 'produtos': produtos},
                       ensure_ascii=True, separators=(',', ':'))
    js = ('/* Gerado por tools/build_busca.py a partir de tools/dados.py'
          ' - nao editar a mao. */\nwindow.HZ_BUSCA=' + corpo + ';\n')
    return js, len(produtos), avisos


if __name__ == '__main__':
    import build_pages as BP
    js, n, avisos = build()
    print(f'{ARQUIVO} {BP.write(ARQUIVO, js) // 1024}KB — {n} produtos')
    for a in avisos:
        print('  aviso: ' + a)
