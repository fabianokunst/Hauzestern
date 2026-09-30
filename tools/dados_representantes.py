# -*- coding: utf-8 -*-
"""
Le representantes.csv e devolve a tabela normalizada para build_representantes.

A fonte da verdade e o proprio `representantes.csv` na raiz — planilha comercial
exportada em CP-1252, com celulas multilinha. Este arquivo nao inventa nada: so
separa nome / telefone / e-mail de cada celula, normaliza a grafia e agrupa por
regiao. Se um campo esta vazio no CSV, ele nao aparece na pagina.

Colunas do CSV:
    ESTADO  ATUACAO  COLCHOES  EMPRESA FAT.  EQUIPE DE VENDAS
    REPRESENTANTE  PREPOSTO x3  ASSISTENTE COMERCIAL x2

`EMPRESA FAT.` (1100 / 1200) nao entra no site: e codigo de faturamento interno.
Do `EQUIPE DE VENDAS` sai so o nome, sem o prefixo numerico do ERP ("211_").
A coluna `COLCHOES` tambem nao entra: o comercial confirmou que toda a rede
atende colchoes, entao o `X` da planilha nao distingue nada na pagina.

    python tools/dados_representantes.py     # confere a leitura no terminal
"""
import os, re, csv, io, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, 'representantes.csv')
ENCODING = 'cp1252'          # exportacao do Excel pt-BR

# --------------------------------------------------------------- geografia
UF_NOME = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AM': 'Amazonas', 'AP': 'Amapá',
    'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal',
    'ES': 'Espírito Santo', 'GO': 'Goiás', 'MA': 'Maranhão',
    'MG': 'Minas Gerais', 'MS': 'Mato Grosso do Sul', 'MT': 'Mato Grosso',
    'PA': 'Pará', 'PB': 'Paraíba', 'PE': 'Pernambuco', 'PI': 'Piauí',
    'PR': 'Paraná', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
    'RO': 'Rondônia', 'RR': 'Roraima', 'RS': 'Rio Grande do Sul',
    'SC': 'Santa Catarina', 'SE': 'Sergipe', 'SP': 'São Paulo',
    'TO': 'Tocantins',
}

REGIOES = [
    ('Norte',        ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO']),
    ('Nordeste',     ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']),
    ('Centro-Oeste', ['DF', 'GO', 'MS', 'MT']),
    ('Sudeste',      ['ES', 'MG', 'RJ', 'SP']),
    ('Sul',          ['PR', 'RS', 'SC']),
]
UF_REGIAO = {uf: nome for nome, ufs in REGIOES for uf in ufs}

# ------------------------------------------------------------- normalizacao
# Siglas que continuam em caixa alta ao titular o texto da planilha.
SIGLAS = set(UF_NOME) | {
    'ABC', 'ABCD', 'ME', 'POA', 'VVR', 'LCV', 'SHP', 'MSS', 'FRI', 'MER', 'BR',
}
# Palavras que ficam em caixa baixa quando nao sao a primeira do texto.
MINUSCULAS = {'de', 'da', 'do', 'dos', 'das', 'e', 'em', 'no', 'na', 'a', 'o'}

# Grafia corrigida nos rotulos internos do ERP — so acento e abreviacao aberta,
# sem mudar sentido. NAO se aplica a nome de pessoa: esses ficam como na planilha.
CORRECOES = [
    ('ESCRITOR. CAPITAL', 'ESCRITORIO CAPITAL'),
    ('ESCRITORIO', 'ESCRITÓRIO'),
    ('REGIAO', 'REGIÃO'),
    ('VITORIA DA CONQUISTA', 'VITÓRIA DA CONQUISTA'),
    ('TRIANGULO MINEIRO', 'TRIÂNGULO MINEIRO'),
]

# Nomes de pessoa que a planilha grafa errado, com a grafia confirmada pelo
# Fabiano. So entra aqui o que ele confirmou: o resto fica como na planilha.
# Fica no gerador, e nao no CSV, para sobreviver a proxima importacao.
NOMES_CORRIGIDOS = {
    'TIAGO SPHOR': 'TIAGO SPOHR',       # e-mail tiago.spohr@ (2026-09-28)
    'TIAGO SPORH': 'TIAGO SPOHR',
}


def corrigir(txt):
    bruto = (txt or '').replace('Í', 'I').replace('Ó', 'O').replace('Ã', 'A')
    for errado, certo in CORRECOES:
        if errado in bruto.upper():
            i = bruto.upper().index(errado)
            txt = txt[:i] + certo + txt[i + len(errado):]
            bruto = bruto[:i] + certo + bruto[i + len(errado):]
    return txt


def _palavra(w, primeira):
    nu = re.sub(r'[^A-Za-zÀ-ÿ]', '', w).upper()
    if nu and nu in SIGLAS:
        return w.upper()
    if not primeira and w.lower() in MINUSCULAS:
        return w.lower()
    # capitaliza cada trecho alfabetico: "i.f.lima" -> "I.F.Lima"
    return re.sub(r'[A-Za-zÀ-ÿ]+', lambda m: m.group(0).capitalize(), w.lower())


def titulo(txt):
    """Caixa alta da planilha -> grafia legivel, preservando siglas e UFs."""
    txt = re.sub(r'\s+', ' ', (txt or '').replace('\n', ' · ')).strip(' ·')
    saida, primeira = [], True
    for bruto in txt.split(' '):
        if not bruto:
            continue
        partes = [_palavra(p, primeira and i == 0) if p else p
                  for i, p in enumerate(bruto.split('/'))]
        saida.append('/'.join(partes))
        primeira = False
    return ' '.join(saida)


# ------------------------------------------------------- leitura das celulas
RE_EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
RE_CODIGO = re.compile(r'\s*\(\d{5,}\)')            # (3551148) — codigo de cliente
RE_PREFIXO = re.compile(r'^[\d/]+_\s*')             # 211_ , 167/132_
RE_FONE = re.compile(
    r'(?:\+?55[\s.]*)?(?:\((\d{2})\)|(\d{2}))[\s.]*(\d{4,5})[-.\s]?(\d{4})(?!\d)')
RE_FONE_SEM_DDD = re.compile(r'(\d{4,5})[-.\s]?(\d{4})(?!\d)')
RE_RAMAL = re.compile(r'^\s*(\d{4})(?!\d)\s*$')

AVISOS = []


def _fone(ddd, numero, bruto):
    if len(numero) == 9:
        txt = '(%s) %s-%s' % (ddd, numero[:5], numero[5:])
    elif len(numero) == 8:
        txt = '(%s) %s-%s' % (ddd, numero[:4], numero[4:])
    else:
        txt = '(%s) %s' % (ddd, numero)
    if len(numero) == 8 and numero[0] == '9':
        AVISOS.append('celular sem o nono dígito: "%s" -> %s' % (bruto.strip(), txt))
    elif len(numero) not in (8, 9):
        AVISOS.append('telefone fora do padrão: "%s" -> %s' % (bruto.strip(), txt))
    return {'txt': txt, 'tel': '+55' + ddd + numero}


def _linha_fones(linha):
    """Telefones de uma linha. Devolve (fones, rotulo) ou (None, None)."""
    fones, ddd, prefixo = [], None, None
    antes, depois = '', ''
    for i, parte in enumerate(linha.split('/')):
        m = RE_FONE.search(parte)
        if m:
            ddd = m.group(1) or m.group(2)
            prefixo = m.group(3)
            fones.append(_fone(ddd, m.group(3) + m.group(4), parte))
            if i == 0:
                antes = parte[:m.start()]
            depois = parte[m.end():]
            continue
        if not ddd:
            if i == 0:
                antes = parte
            continue
        m = RE_FONE_SEM_DDD.search(parte)
        if m:
            prefixo = m.group(1)
            fones.append(_fone(ddd, m.group(1) + m.group(2), parte))
            depois = parte[m.end():]
            continue
        m = RE_RAMAL.match(parte)          # "3249-4448/7773" -> 3249-7773
        if m and prefixo and len(prefixo) == 4:
            fones.append(_fone(ddd, prefixo + m.group(1), parte))
            depois = ''
    if not fones:
        return None, None
    rotulo = re.sub(r'\s+', ' ', (antes + ' ' + depois)).strip(' :;-–—,.')
    if rotulo.startswith('(') and rotulo.endswith(')'):
        rotulo = rotulo[1:-1].strip()          # "(whats)" -> "whats"
    return fones, (rotulo or None)


def contato(celula, papel):
    """Separa nomes, telefones e e-mails de uma celula do CSV."""
    celula = RE_CODIGO.sub('', (celula or '').replace('\r', ''))
    if not celula.strip():
        return None
    nomes, fones, emails = [], [], []
    for linha in celula.split('\n'):
        linha = linha.strip()
        if not linha:
            continue
        achados = RE_EMAIL.findall(linha)
        if achados:
            emails += [e.lower() for e in achados]
            linha = RE_EMAIL.sub(' ', linha).strip()
            if not linha:
                continue
        fs, rotulo = _linha_fones(linha)
        if fs:
            for f in fs:
                f['rotulo'] = rotulo
            fones += fs
        else:
            chave = re.sub(r'\s+', ' ', linha).upper()
            nomes.append(titulo(NOMES_CORRIGIDOS.get(chave, linha)))
    # "COMERCIAL" / "ASSISTENCIA" na primeira linha e o setor, nao uma pessoa
    setor = None
    if len(nomes) > 1 and ' ' not in nomes[0]:
        setor = nomes.pop(0)
    return {'papel': papel, 'setor': setor, 'nomes': nomes,
            'fones': _unicos(fones, lambda f: f['tel']),
            'emails': _unicos(emails, lambda e: e)}


def _unicos(seq, chave):
    vistos, saida = set(), []
    for x in seq:
        k = chave(x)
        if k not in vistos:
            vistos.add(k)
            saida.append(x)
    return saida


# ------------------------------------------------------------------ tabela
PAPEIS = [(5, 'Representante'), (6, 'Preposto'), (7, 'Preposto'),
          (8, 'Preposto'), (9, 'Assistente comercial'),
          (10, 'Assistente comercial')]


def carregar():
    del AVISOS[:]
    with io.open(CSV_PATH, 'rb') as fh:
        texto = fh.read().decode(ENCODING)
    linhas = [r for r in csv.reader(io.StringIO(texto)) if any(c.strip() for c in r)]
    registros = []
    for r in linhas[1:]:                       # linha 0 e o cabecalho
        r = r + [''] * (11 - len(r))
        uf = r[0].strip().upper()
        if uf not in UF_NOME:
            continue
        contatos = [c for c in (contato(r[i], p) for i, p in PAPEIS) if c]
        registros.append({
            'uf': uf,
            'estado': UF_NOME[uf],
            'regiao': UF_REGIAO[uf],
            'atuacao': titulo(corrigir(RE_CODIGO.sub('', r[1]))),
            'equipe': titulo(corrigir(RE_PREFIXO.sub('', r[4].strip()))),
            'contatos': contatos,
        })
    return registros


def por_regiao(registros):
    """[(regiao, [(uf, estado, [registros...]), ...]), ...] na ordem do IBGE."""
    saida = []
    for regiao, ufs in REGIOES:
        estados = []
        for uf in ufs:
            rs = [x for x in registros if x['uf'] == uf]
            if rs:
                estados.append((uf, UF_NOME[uf], rs))
        if estados:
            saida.append((regiao, estados))
    return saida


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    regs = carregar()
    print('%d registros · %d UFs · %d contatos\n'
          % (len(regs), len({r['uf'] for r in regs}),
             sum(len(r['contatos']) for r in regs)))
    for regiao, estados in por_regiao(regs):
        print('== %s ==' % regiao)
        for uf, estado, rs in estados:
            for x in rs:
                print('  %s · %s · %s' % (uf, x['atuacao'], x['equipe']))
                for c in x['contatos']:
                    print('      %s%s: %s' % (
                        c['papel'], (' · ' + c['setor']) if c['setor'] else '',
                        ' / '.join(c['nomes']) or '—'))
                    for f in c['fones']:
                        print('         tel %s  %s%s' % (f['txt'], f['tel'],
                              ('   (%s)' % f['rotulo']) if f['rotulo'] else ''))
                    for e in c['emails']:
                        print('         @   %s' % e)
    if AVISOS:
        print('\n== avisos (%d) ==' % len(AVISOS))
        for a in sorted(set(AVISOS)):
            print('  ' + a)
