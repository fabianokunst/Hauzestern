# -*- coding: utf-8 -*-
"""
Importa a planilha comercial (.xlsx) para representantes.csv.

O comercial manda uma planilha nova de tempo em tempo. Este script a converte
para o CSV que `dados_representantes.py` le, mostra o que muda em relacao ao
que esta publicado e arquiva a versao anterior.

Uso:
    python tools/importar_representantes.py "atividades/REPRES. HAUZESTERN.xlsx"
    python tools/importar_representantes.py --dry-run <arquivo.xlsx>
    python tools/importar_representantes.py --build   <arquivo.xlsx>

    --dry-run   so mostra o diff, nao escreve nada
    --build     ja regenera representantes.html depois de importar

Depois de importar sem --build, rode:
    python tools/build_representantes.py

Le o .xlsx direto pelo zipfile + ElementTree da biblioteca padrao — nao precisa
de openpyxl. So a primeira aba e lida, e so os valores (formulas viram o ultimo
valor calculado que o Excel gravou).
"""
import os, sys, io, csv, csv as _csv, shutil, zipfile, datetime
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

import dados_representantes as DR

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
ARQUIVO_DIR = os.path.join(DR.ROOT, '_arquivo')

# as 11 colunas, na ordem em que dados_representantes.py as espera
CABECALHO = ['ESTADO', 'ATUAÇÃO', 'COLCHOES', 'EMPRESA FAT.', 'EQUIPE DE VENDAS',
             'REPRESENTANTE', 'PREPOSTO', 'PREPOSTO', 'PREPOSTO',
             'ASSISTENTE COMERCIAL', 'ASSISTENTE COMERCIAL - 2']
N_COLS = len(CABECALHO)


# ------------------------------------------------------------------ leitura

def ler_xlsx(caminho):
    """[[c0..c10], ...] da primeira aba, sem linhas vazias."""
    with zipfile.ZipFile(caminho) as z:
        nomes = z.namelist()

        compartilhadas = []
        if 'xl/sharedStrings.xml' in nomes:
            raiz = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in raiz.findall(NS + 'si'):
                compartilhadas.append(''.join(t.text or '' for t in si.iter(NS + 't')))

        # a primeira aba na ordem do workbook, nao a primeira em ordem alfabetica
        aba = 'xl/worksheets/sheet1.xml'
        try:
            wb = ET.fromstring(z.read('xl/workbook.xml'))
            rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
            RNS = '{http://schemas.openxmlformats.org/package/2006/relationships}'
            RID = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
            alvo = {r.get('Id'): r.get('Target') for r in rels.findall(RNS + 'Relationship')}
            primeira = next(iter(wb.iter(NS + 'sheet')))
            destino = alvo.get(primeira.get(RID), '')
            if destino:
                aba = 'xl/' + destino.lstrip('/').replace('worksheets/../', '')
        except (KeyError, StopIteration):
            pass
        if aba not in nomes:
            aba = next(n for n in nomes if n.startswith('xl/worksheets/sheet'))

        linhas = []
        for tr in ET.fromstring(z.read(aba)).iter(NS + 'row'):
            celulas = {}
            for c in tr.findall(NS + 'c'):
                col = ''.join(ch for ch in (c.get('r') or '') if ch.isalpha())
                tipo, v = c.get('t'), c.find(NS + 'v')
                inline = c.find(NS + 'is')
                if tipo == 's' and v is not None:
                    txt = compartilhadas[int(v.text)]
                elif inline is not None:
                    txt = ''.join(x.text or '' for x in inline.iter(NS + 't'))
                elif v is not None:
                    txt = v.text or ''
                else:
                    txt = ''
                celulas[col] = txt
            vals = [celulas.get(k, '') for k in 'ABCDEFGHIJK']
            if any(x.strip() for x in vals):
                linhas.append(vals)
    return linhas


def ler_csv(caminho):
    if not os.path.exists(caminho):
        return None, []
    with io.open(caminho, 'rb') as fh:
        texto = fh.read().decode(DR.ENCODING)
    linhas = [r for r in csv.reader(io.StringIO(texto)) if any(c.strip() for c in r)]
    if not linhas:
        return None, []
    return linhas[0], [r + [''] * (N_COLS - len(r)) for r in linhas[1:]]


# ------------------------------------------------------------------ validacao

def norm(s):
    return ' '.join((s or '').split()).upper()


def validar(cabecalho, dados):
    """(erros, avisos) — erro impede a importacao, aviso so alerta."""
    erros, avisos = [], []

    if [norm(c) for c in cabecalho] != [norm(c) for c in CABECALHO]:
        erros.append('cabeçalho diferente do esperado — as colunas podem ter '
                     'mudado de ordem. Esperado:\n      ' + ' | '.join(CABECALHO)
                     + '\n    Encontrado:\n      ' + ' | '.join(cabecalho))

    for i, r in enumerate(dados, start=2):
        uf = r[0].strip().upper()
        if uf not in DR.UF_NOME:
            # dados_representantes.py descarta UF desconhecida em silencio:
            # um "SVP" digitado errado sumiria com o representante sem avisar
            erros.append(f'linha {i}: UF "{r[0].strip()}" não existe — a linha '
                         f'seria descartada em silêncio pelo gerador')
        if not r[4].strip():
            avisos.append(f'linha {i} ({uf}): EQUIPE DE VENDAS vazia')
        if not r[5].strip():
            avisos.append(f'linha {i} ({uf}): sem REPRESENTANTE')
        for j, cel in enumerate(r):
            try:
                cel.encode(DR.ENCODING)
            except UnicodeEncodeError as e:
                ruim = cel[e.start:e.end]
                erros.append(f'linha {i} col {chr(65+j)}: caractere {ruim!r} '
                             f'não existe em {DR.ENCODING}')
    return erros, avisos


# ------------------------------------------------------------------ diff

def chave(r):
    return (norm(r[0]), norm(r[4]))


def diff(antigas, novas):
    a = {}
    for r in antigas:
        a.setdefault(chave(r), []).append(r)
    n = {}
    for r in novas:
        n.setdefault(chave(r), []).append(r)

    saem = [r for k, v in a.items() if k not in n for r in v]
    entram = [r for k, v in n.items() if k not in a for r in v]
    mudam = []
    for k in n:
        if k in a:
            va, vn = a[k][0], n[k][0]
            campos = [CABECALHO[i] for i in range(N_COLS)
                      if norm(va[i]) != norm(vn[i])]
            if campos:
                mudam.append((vn, campos, va))
    return saem, entram, mudam


def uma_linha(s, n=38):
    """Celula multilinha em uma linha, para caber na tabela do relatorio."""
    t = ' / '.join(p.strip() for p in (s or '').split('\n') if p.strip())
    t = ' '.join(t.split())
    return t if len(t) <= n else t[:n - 1] + '…'


def relatorio(antigas, novas):
    saem, entram, mudam = diff(antigas, novas)
    ufs_a = {norm(r[0]) for r in antigas}
    ufs_n = {norm(r[0]) for r in novas}

    print(f'\n== o que muda ==')
    print(f'  áreas de atuação: {len(antigas)} -> {len(novas)}')
    print(f'  UFs cobertas:     {len(ufs_a)} -> {len(ufs_n)}')

    if entram:
        print(f'\n  ENTRAM ({len(entram)}):')
        for r in entram:
            print(f'    + {r[0].strip():3} | {uma_linha(r[1]):38} | {uma_linha(r[4], 40)}')
    if saem:
        print(f'\n  SAEM ({len(saem)}):')
        for r in saem:
            print(f'    - {r[0].strip():3} | {uma_linha(r[1]):38} | {uma_linha(r[4], 40)}')
    if mudam:
        print(f'\n  ALTERADAS ({len(mudam)}):')
        for vn, campos, va in mudam:
            print(f'    ~ {vn[0].strip():3} | {uma_linha(vn[1]):38} | {uma_linha(vn[4], 40)}')
            for c in campos:
                i = CABECALHO.index(c)
                print(f'        {c}:')
                print(f'          antes: {" / ".join(va[i].split(chr(10)))[:90]}')
                print(f'          agora: {" / ".join(vn[i].split(chr(10)))[:90]}')
    if not (entram or saem or mudam):
        print('\n  nada — a planilha é idêntica ao CSV publicado')

    orfas = sorted(ufs_a - ufs_n)
    if orfas:
        print(f'\n  !! estas UFs ficam SEM NENHUM representante e saem da página '
              f'(card e seletor): {", ".join(orfas)}')
    novas_ufs = sorted(ufs_n - ufs_a)
    if novas_ufs:
        print(f'  UFs que voltam/estreiam na página: {", ".join(novas_ufs)}')
    return saem, entram, mudam


# ------------------------------------------------------------------ escrita

def montar_csv(cabecalho, dados):
    """Mesma forma da exportacao do Excel pt-BR: linha vazia inicial, CRLF
    entre registros, LF dentro das celulas, cp1252."""
    buf = io.StringIO(newline='')
    w = _csv.writer(buf, lineterminator='\r\n', quoting=_csv.QUOTE_MINIMAL)
    w.writerow([''] * N_COLS)
    w.writerow(cabecalho)
    for r in dados:
        w.writerow(r)
    return buf.getvalue().encode(DR.ENCODING)


def arquivar(caminho):
    """Guarda o CSV atual em _arquivo/, datado. Devolve o caminho ou None."""
    if not os.path.exists(caminho):
        return None
    os.makedirs(ARQUIVO_DIR, exist_ok=True)
    dia = datetime.date.fromtimestamp(os.path.getmtime(caminho)).isoformat()
    destino = os.path.join(ARQUIVO_DIR, f'representantes-{dia}.csv')
    n = 2
    while os.path.exists(destino):
        destino = os.path.join(ARQUIVO_DIR, f'representantes-{dia}-{n}.csv')
        n += 1
    shutil.copy2(caminho, destino)
    return destino


# ------------------------------------------------------------------ main

def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    dry = '--dry-run' in argv
    build = '--build' in argv
    if len(args) != 1:
        print(__doc__.strip())
        return 2
    xlsx = args[0]
    if not os.path.exists(xlsx):
        print(f'erro: não achei "{xlsx}"')
        return 1

    linhas = ler_xlsx(xlsx)
    if not linhas:
        print('erro: a planilha está vazia')
        return 1
    cabecalho, dados = linhas[0], [r for r in linhas[1:]]
    # tolera uma linha de titulo antes do cabecalho
    if norm(cabecalho[0]) != 'ESTADO':
        for i, r in enumerate(linhas):
            if norm(r[0]) == 'ESTADO':
                cabecalho, dados = r, linhas[i + 1:]
                break

    print(f'planilha: {xlsx}')
    print(f'  {len(dados)} linhas de dados, {len({norm(r[0]) for r in dados})} UFs')

    erros, avisos = validar(cabecalho, dados)
    if avisos:
        print(f'\n== avisos ({len(avisos)}) ==')
        for a in avisos:
            print('  ' + a)
    if erros:
        print(f'\n== ERROS ({len(erros)}) — nada foi escrito ==')
        for e in erros:
            print('  ' + e)
        return 1

    antigo_cab, antigas = ler_csv(DR.CSV_PATH)
    relatorio(antigas, dados)

    if dry:
        print('\n--dry-run: nada foi escrito.')
        return 0

    novo = montar_csv(CABECALHO, dados)
    atual = None
    if os.path.exists(DR.CSV_PATH):
        with io.open(DR.CSV_PATH, 'rb') as fh:
            atual = fh.read()

    # nao arquiva copia identica: so gera lixo em _arquivo/
    bak = None if atual == novo else arquivar(DR.CSV_PATH)
    with io.open(DR.CSV_PATH, 'wb') as fh:
        fh.write(novo)

    print(f'\nrepresentantes.csv atualizado ({len(dados)} linhas)')
    if bak:
        print(f'versão anterior em {os.path.relpath(bak, DR.ROOT)}')
    elif atual == novo:
        print('conteúdo idêntico ao que já estava — nada arquivado')

    # confere que o gerador consegue ler o que acabamos de escrever
    import importlib
    importlib.reload(DR)
    regs = DR.carregar()
    print(f'gerador leu {len(regs)} registros em '
          f'{len({r["uf"] for r in regs})} UFs')
    if len(regs) != len(dados):
        print(f'  !! atenção: {len(dados) - len(regs)} linha(s) não viraram '
              f'registro — confira as UFs')
    for a in sorted(set(DR.AVISOS)):
        print('  aviso de dados: ' + a)

    if build:
        print()
        import build_representantes
        import build_pages as BP
        n = BP.write('representantes.html', build_representantes.build())
        print(f'representantes.html  {n // 1024}KB')
    else:
        print('\npróximo passo:  python tools/build_representantes.py')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
