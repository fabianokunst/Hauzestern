# Hauzestern — instruções do projeto

Site estático da Hauzestern (colchões da Herval), gerado por scripts Python em
`tools/`. Estrutura, dados, decisões com a marca e pendências: `README.md`.

## Publicação automática — sempre, sem pedir

O repositório <https://github.com/fabianokunst/Hauzestern> é **público** e o
GitHub Pages publica o site direto dele em <https://fabianokunst.github.io/Hauzestern/>.
O Fabiano quer que toda alteração vá para lá **automaticamente**: ele não vai
pedir, e não é para perguntar. A autorização é permanente.

Ao terminar **qualquer** tarefa que altere arquivos do projeto (páginas, `css/`,
`js/`, `assets/`, `tools/`, `README.md`, este arquivo):

1. Se mexeu em fontes (`tools/*.py` ou na planilha de representantes), regenere
   com `python tools/build_all.py` — com o cuidado de "Sessões em paralelo".
2. Veja o que vai subir: `python tools/publicar.py --dry-run`.
3. Publique:

   ```
   python tools/publicar.py "<o que mudou, em português>" --coautor "<sua linha de atribuição>"
   ```

   `--coautor` recebe o texto do `Co-Authored-By` que você usa em commits
   (ex.: `"Claude Opus 5.5 <noreply@anthropic.com>"`).
4. Termine a resposta dizendo que publicou (hash do commit) ou por que não.

Publique só com a tarefa **completa e conferida**, nunca no meio dela nem antes
de fazer uma pergunta ao Fabiano: o que é enviado vai ao ar na hora. Tarefa que
só lê, tira dúvida ou gera arquivo fora do site (scratchpad) não publica nada.

Se o `publicar.py` parar (`NÃO PUBLICADO: ...`):

- **check.py acusou problema** → corrija o link, a imagem ou o índice da busca e rode de novo.
- **arquivo interno no repositório** → nunca force; descubra por que entrou e tire.
- **login** → o envio abre uma janela do GitHub; avise o Fabiano para entrar com
  a conta `fabianokunst` e rode de novo (o commit local fica guardado).
- **conflito** → alguém subiu arquivos pelo site do GitHub; traga com
  `git pull --rebase`, resolva e publique.

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
- O `publicar.py` envia **tudo** o que mudou na pasta, inclusive o trabalho de
  outra conversa. Se o `--dry-run` mostrar algo que não é seu e parece pela
  metade (ex.: `tools/dados.py` mudou e as páginas não), publique só os seus
  arquivos com `--so <caminhos>`.

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
