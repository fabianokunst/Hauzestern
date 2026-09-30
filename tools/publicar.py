# -*- coding: utf-8 -*-
"""
Envia para o GitHub (fabianokunst/Hauzestern) o que mudou na pasta. O GitHub
Pages serve o site direto do repositório: publicar aqui = colocar no ar.

    python tools/publicar.py "Atualiza representantes"
    python tools/publicar.py "..." --coautor "Nome <email>"   # linha Co-Authored-By
    python tools/publicar.py "..." --so css/style.css index.html
    python tools/publicar.py --dry-run                         # só lista o que iria
    python tools/publicar.py --auto        # hook Stop do Claude Code (.claude/settings.json)

Antes de enviar, roda check.py e para se houver link quebrado ou produto fora
da busca, e confere que nenhum arquivo interno (planilha, documentos/,
chamado/...) entrou. O .gitignore já os exclui; a conferência é a segunda trava.

`--auto` roda ao fim de cada resposta do Claude: o repositório é de homologação,
então envia mesmo com aviso do check.py (só avisa), fica calado quando nada
mudou e responde em JSON (`systemMessage`) para o aviso aparecer na conversa.
Arquivo interno continua barrando o envio.
"""
import os, re, sys, json, argparse, subprocess

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SITE_NO_AR = 'https://fabianokunst.github.io/Hauzestern/'
PROIBIDO = re.compile(
    r'(^|/)(representantes\.csv|documentos/|chamado/|guide_hauzestern/|atividades/'
    r'|\.cache-fundos/|_arquivo/|#template-inicial/|\.claude/|__pycache__/)'
    r'|\.xlsx?$|\.pyc$', re.I)
PROBLEMAS_CHECK = ('QUEBRADO', 'fora do índice', 'no índice, sem página',
                   'miniatura inexistente')


AUTO = False


def diga(msg):
    if AUTO:                                # o hook lê JSON; o texto vai para a conversa
        print(json.dumps({'systemMessage': 'GitHub: ' + msg}, ensure_ascii=False))
    else:
        print(msg)


def falhe(msg):
    if AUTO:
        diga('NÃO PUBLICADO — ' + msg)
        sys.exit(0)                         # não trava a conversa; o aviso já apareceu
    sys.exit('NÃO PUBLICADO: ' + msg)


def git(*args, check=True):
    r = subprocess.run(['git', '-c', 'core.quotepath=false', *args],
                       capture_output=True, text=True, encoding='utf-8')
    if check and r.returncode:
        falhe(f'git {" ".join(args)} falhou\n{r.stderr.strip()}')
    return r.stdout


def pare(msg):
    git('reset', '-q')                      # desfaz o `add`; a pasta não é tocada
    falhe(msg)


def main():
    global AUTO
    ap = argparse.ArgumentParser()
    ap.add_argument('mensagem', nargs='?', default='Atualiza o site')
    ap.add_argument('--coautor', help='texto da linha Co-Authored-By')
    ap.add_argument('--so', nargs='+', metavar='CAMINHO',
                    help='publica só estes caminhos (padrão: tudo o que mudou)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--auto', action='store_true', help='modo hook (ver docstring)')
    a = ap.parse_args()
    AUTO = a.auto

    if AUTO and os.path.exists(os.path.join('.git', 'index.lock')):
        return                              # outra conversa publicando agora; a próxima pega

    if AUTO and not git('status', '--porcelain') and not int(
            git('rev-list', '--count', 'origin/main..HEAD').strip() or 0):
        return                              # nada mudou: sem check, sem rede, sem aviso

    r = subprocess.run([sys.executable, os.path.join('tools', 'check.py')],
                       capture_output=True, text=True, encoding='utf-8')
    ruins = [l.strip() for l in r.stdout.splitlines() if any(p in l for p in PROBLEMAS_CHECK)]
    if (r.returncode or ruins) and not AUTO:
        falhe('check.py acusou problema\n  ' + '\n  '.join(ruins or [r.stderr.strip()]))
    aviso = f' (atenção: check.py acusou {len(ruins) or "erro"})' if (r.returncode or ruins) else ''

    git('add', '-A', '--', *(a.so or ['.']))
    mudou = git('diff', '--cached', '--name-status').splitlines()
    proibidos = [f for f in git('ls-files').splitlines() if PROIBIDO.search(f)]
    if proibidos:
        pare('arquivo interno no repositório — descubra por que entrou:\n  '
             + '\n  '.join(proibidos))

    if a.dry_run:
        git('reset', '-q')
        print('\n'.join(mudou) if mudou else 'nada mudou')
        return

    if mudou:
        titulo = a.mensagem
        if AUTO:
            nomes = [l.split('\t')[-1] for l in mudou]
            titulo = (f'Atualização automática: {", ".join(nomes[:3])}'
                      + (f' e mais {len(nomes) - 3}' if len(nomes) > 3 else ''))
        msg = ['-m', titulo] + (['-m', f'Co-Authored-By: {a.coautor}'] if a.coautor else [])
        git('commit', '-q', *msg)
        if not AUTO:
            print(f'commit {git("rev-parse", "--short", "HEAD").strip()} — {len(mudou)} arquivo(s)')
            for l in mudou[:40]:
                print('  ' + l.replace('\t', '  '))
            if len(mudou) > 40:
                print(f'  ... e mais {len(mudou) - 40}')

    git('fetch', '-q', 'origin')
    atras = int(git('rev-list', '--count', 'HEAD..origin/main').strip() or 0)
    if atras:
        r = subprocess.run(['git', 'rebase', '-q', '--autostash', 'origin/main'],
                           capture_output=AUTO)
        if r.returncode:
            subprocess.run(['git', 'rebase', '--abort'], capture_output=True)
            falhe('o GitHub tem alterações que conflitam com as locais '
                  '(alguém subiu arquivos pelo site?). O commit local ficou guardado.')
    frente = int(git('rev-list', '--count', 'origin/main..HEAD').strip() or 0)
    if not frente:
        if not AUTO:
            print('nada novo para enviar — o GitHub já está igual à pasta')
        return

    # sem capturar a saída fora do modo hook: o login do GitHub pode abrir uma janela
    if subprocess.run(['git', 'push', '-q', 'origin', 'main'], capture_output=AUTO).returncode:
        falhe('o envio falhou (login?). O commit local ficou guardado; '
              'o próximo envio tenta de novo.')
    qtd = f'{len(mudou)} arquivo(s)' if mudou else f'{frente} commit(s) que tinham ficado para trás'
    diga(f'enviado {qtd}, commit '
         f'{git("rev-parse", "--short", "HEAD").strip()}{aviso}. No ar em ~1 min: {SITE_NO_AR}')


if __name__ == '__main__':
    main()
