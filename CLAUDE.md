# Hauzestern — instruções do projeto

Site estático da Hauzestern (colchões da Herval), gerado por scripts Python em
`tools/`. Estrutura, dados, decisões com a marca e pendências: `README.md`.

## Publicação automática no GitHub (homologação)

O repositório <https://github.com/fabianokunst/Hauzestern> é **público** e o
GitHub Pages publica o site direto dele em <https://fabianokunst.github.io/Hauzestern/>.
Não é o site oficial: é o ambiente de **homologação** do Fabiano. A fonte da
verdade é esta pasta; o GitHub só espelha o que está aqui.

O Fabiano quer que toda alteração vá para lá **automaticamente**, inclusive
trabalho pela metade. Isso já acontece sozinho: um hook `Stop` em
`.claude/settings.json` roda `python tools/publicar.py --auto` ao fim de cada
resposta do Claude e envia tudo o que mudou na pasta (em silêncio quando nada
mudou; com uma linha "GitHub: ..." na conversa quando envia ou falha). Não
pergunte antes de publicar — a autorização é permanente.

Para um commit com mensagem descritiva em vez da automática, publique você
mesmo antes de terminar:

```
python tools/publicar.py "<o que mudou, em português>" --coautor "<sua linha de atribuição>"
```

(`--coautor` recebe o texto do `Co-Authored-By` que você usa em commits, ex.:
`"Claude Opus 5.5 <noreply@anthropic.com>"`; `--dry-run` só lista o que iria.)

Se aparecer "GitHub: NÃO PUBLICADO — ..." (ou `NÃO PUBLICADO:` no modo manual):

- **arquivo interno no repositório** → nunca force; descubra por que entrou e tire.
- **login** → o GitHub pede entrar com a conta `fabianokunst`; avise o Fabiano
  (o commit local fica guardado e vai no próximo envio).
- **conflito** → alguém subiu arquivos pelo site do GitHub; traga com
  `git pull --rebase`, resolva e publique.
- **check.py acusou problema** → no modo automático o envio sai assim mesmo
  (é homologação), só com o aviso; corrija quando for o caso.

Nunca `git push --force`, `git reset --hard` nem reescrever o histórico sem o
Fabiano pedir.

### O que nunca pode ir para o repositório

`representantes.csv`, planilhas `.xlsx`, `documentos/`, `chamado/`,
`guide_hauzestern/`: têm códigos de faturamento, e-mails pessoais e material
interno da marca. O `robots.txt` não protege nada — o repositório é público.
Também ficam fora, por não serem site: `.cache-fundos/`, `_arquivo/`,
`#template-inicial/`, `.claude/`, `__pycache__/`.

O `.gitignore` já exclui tudo isso e o `publicar.py` confere de novo antes de
enviar. Arquivo novo de dados internos em outra pasta → acrescente ao
`.gitignore` **antes** de publicar.

## Sessões em paralelo

Várias conversas costumam editar o projeto ao mesmo tempo, e os arquivos mudam
no disco no meio do trabalho.

- `build_all.py` regrava todas as páginas e apaga, sem aviso, edição feita à mão
  num HTML. Antes de gravar, gere em memória e compare com o disco: só devem
  aparecer as diferenças da sua tarefa.
- Releia o trecho de arquivo compartilhado (`dados.py`, `build_pages.py`,
  `style.css`, `README.md`, `build_all.py`) antes de editar; use edição pontual,
  nunca reescreva o arquivo inteiro. CSS novo em bloco próprio no fim do `style.css`.
- O envio automático manda **tudo** o que mudou na pasta, inclusive o trabalho
  de outra conversa em andamento — combinado com o Fabiano, é homologação.

## Regras do conteúdo

- Representantes: a planilha `.xlsx` chega de tempos em tempos. Rode
  `python tools/importar_representantes.py --dry-run <xlsx>`, mostre ao Fabiano
  quais UFs ficam sem representante e só então `--build`. **Nunca** edite
  `representantes.csv` à mão (é gerado da planilha, e a página é gerada dele).
- Telefones sem o nono dígito são publicados como vêm na planilha. Não afirmar
  cobertura nacional em texto de SEO.
- Material novo da marca chega em `chamado/` (pasta temporária) e é copiado para
  `documentos/fichas/` e `documentos/produtos/<modelo>/`.
- Sem analytics por enquanto.
- Conferência geral: `python tools/check.py`.
