# Hauzestern — site

Site estático em HTML + CSS + JS puro, sem build e sem dependências no navegador.
Basta abrir `index.html` ou subir a pasta em qualquer hospedagem.

**Todo o conteúdo de produto é transcrição do material da marca em
`guide_hauzestern/`.** Onde a marca não diz, o site não diz — a seção
correspondente simplesmente não aparece na página. Ver
[Auditoria de conteúdo](#auditoria-de-conteúdo).

## Estrutura

```
index.html                    home
garantia.html                 garantia, cuidados e tabela de biotipos
representantes.html           rede comercial por estado (gerada do CSV)
colchoes/<modelo>.html        14 PDPs (berg, dorf, eibsee, frost, gipfel, hemmen,
                              himmel, mond, motte, nebel, sylt, wachen, wohl, zonen)
bases/<modelo>.html            6 PDPs (box-root, box-c1674, box-c1705, box-c1836,
                              box-c1706, box-favo)
travesseiros/<modelo>.html     5 PDPs (alpen, harz, weich, mh7618, mh7619)
representantes.csv            planilha comercial — fonte da pagina de representantes
sitemap.xml  robots.txt  site.webmanifest
favicon.svg  favicon.ico
css/style.css                 estilos — tokens de marca no :root
js/main.js                    header ao rolar, menu mobile, submenu, reveal, ano
assets/
  brand/                      marca em SVG (ver "Marca")
  produtos/<slug>-branco.jpg  slide 1 do carrossel (1400×1050)
  produtos/<slug>-ambiente.jpg slide 2 — só Wohl e Hemmen
  produtos/<slug>-cinza.jpg   slide 3
  produtos/<slug>-card.jpg    card da home, sempre do cinza (640×480)
  bases/<slug>.jpg            idem
  travesseiros/<slug>.jpg     960×720 + -card 480×360
  camadas/<slug>.webp         diagrama das camadas (8 modelos)
  processo/1..4.jpg           fábrica, seção "Primor em cada processo"
  lifestyle/                  fotos de ambiente
  hero-frankfurt.jpg          imagem do hero
tools/                        geradores (rodam no dev, não no navegador)
_arquivo/                     páginas retiradas do site — ver _arquivo/LEIA-ME.txt
guide_hauzestern/             material da marca (não publicar)
```

## Como editar

O HTML das 28 páginas é **gerado** a partir de duas fontes: `tools/dados.py`
(produtos, garantia, textos institucionais) e `representantes.csv` (rede
comercial).

```bash
# 1. edite tools/dados.py  ou  representantes.csv
# 2. regenere o site
python tools/build_all.py
# 3. confira links, assets órfãos e SEO
python tools/check.py
```

Se as imagens do guide mudarem:

```bash
python tools/variantes.py        # 3 variantes de cada colchão (~2 min)
python tools/build_assets.py     # travesseiros, bases, fábrica, lifestyle
```

| Script | O que faz |
|---|---|
| `tools/dados.py` | **a fonte da verdade**: 14 colchões, 6 bases, 5 travesseiros, garantia |
| `tools/dados_representantes.py` | lê `representantes.csv` e normaliza a rede comercial |
| `tools/build_all.py` | gera home + garantia + representantes + 25 PDPs + sitemap |
| `tools/build_home.py` | só a home (textos institucionais e tecnologias ficam aqui) |
| `tools/build_garantia.py` | só a garantia (transcrição do certificado) |
| `tools/build_representantes.py` | só a página de representantes |
| `tools/build_pages.py` | PDPs + `head`/`header`/`footer` compartilhados |
| `tools/build_assets.py` | prepara travesseiros, bases, processo e lifestyle |
| `tools/variantes.py` | as 3 variantes de foto de cada colchão (única fonte de `assets/produtos/`) |
| `tools/fundos.py` | troca o fundo de estúdio cinza ⇄ branco, quando a variante não existe |
| `tools/check.py` | links quebrados, assets órfãos, títulos duplicados, `h1` |

Ajustes pontuais de layout podem ser feitos direto no HTML — mas serão sobrescritos
no próximo `build_all`. Mudança que precisa durar vai no gerador.

## Auditoria de conteúdo

Cada campo de `tools/dados.py` traz, no topo do arquivo, o documento de onde saiu.
Estas foram as correções da auditoria contra o guide:

**Texto reescrito por transcrição.** As 14 fichas técnicas individuais têm
parágrafos próprios da marca sobre cada material — "CAMADAS DE CONFORTO" e
"DIFERENCIAIS" — que não estavam sendo usados. Agora a seção *O que faz a
diferença* de cada PDP é esse texto, verbatim. As descrições de molejo (194 molas
ATC 2,20 mm; MaxSpring 206 molas monobloco) e de Pillow Top One Side também
passaram a ser as da ficha.

**Ordem das camadas conferida duas vezes.** Extraída pela coordenada Y da coluna
de rótulos no catálogo e comparada com os diagramas `*(Texto)` do guide. As
contagens batem com a numeração do catálogo em 14/14 modelos.

**Ícones de tecnologia conferidos na imagem.** A extração de texto do PDF
embaralha a ordem dos rótulos; as listas foram lidas na página renderizada, modelo
por modelo. Cada PDP mostra exatamente os ícones daquela página do catálogo.

**Altura e suporte de peso conferidos em dois documentos.** Catálogo 2026 e ficha
técnica batem em 14/14.

**Sistema Thermo Flow.** O manual do sistema (`Colchão Wohl/_Ficha Técnica/`)
mostra que não é só uma camada de espuma: é um colchão de aquecimento a ar
multifuncional, com três modos, controle remoto, especificações elétricas,
garantia própria de 1 ano e avisos de segurança. Tudo isso está agora na página do
Wohl, incluindo o aviso de não dormir durante o modo de eliminação de ácaros.

**Traduções.** Só entram as que o Storytelling declara (9 modelos). Gipfel, Wohl,
Hemmen, Dorf e Eibsee ficaram sem tradução no site porque nenhum documento do
guide traz uma. Antes o campo do Dorf dizia "vila", que era inferência nossa.

**Textos sem lastro, removidos.** Parágrafos que descreviam Berg, Dorf, MH 7618 e
MH 7619 e não existiam em documento nenhum saíram. Berg e Dorf receberam o texto
real da ficha; os dois moldados ficaram só com as medidas e a nomenclatura do
catálogo, e a página avisa que a marca não publicou descrição para eles.

**"Desenvolvimento de Produtos.pdf" é proposta antiga.** Traz nomes de base
(Touch, Luna, Aurora, Wave, Netuno, Stella, Awake, Zonare) que não foram
lançados, e coloca Weich em Propósitos — o Storytelling final o coloca em
Elementos. Nada dele entrou no site.

**Destaques.** Comparando o catálogo 2025 com o 2026, os lançamentos atuais são
Gipfel e Wohl. Eibsee é de 2025 e perdeu o selo de destaque.

### Divergências dentro do próprio material da marca

Estas precisam de decisão da marca — o site mostra a versão mais recente e a
divergência está registrada:

| O quê | Um documento diz | Outro diz | No site |
|---|---|---|---|
| Pés do Box C1705 | catálogo 2026: 21 cm | ficha técnica: 18,5 cm | 21 cm, com nota na página |
| Tampo do Frost | ícone: "Tecido Malha com Linho" | ficha e lista de camadas: 74,4% poliéster + 25,6% poliamida (bioamida), sem linho | os dois, como a marca publica |
| Nome do sistema do Wohl | catálogo: "Thermo Flow" | manual: "Termo Flow" / "TermoFlow"; ficha: "ThermalFlow" | "Thermo Flow" (catálogo 2026) |
| Faixa de altura na tabela de biotipos | certificado: `1,15 a 1,68` | sequência lógica seria `1,51 a 1,60` | como está impresso |
| Frost, tradução | Storytelling: "orvalho" | em alemão *Frost* é geada | "orvalho", como a marca escreve |
| Ficha do Hemmen | contém um parágrafo sobre "vilas germânicas" | esse texto é do Dorf | não usado |

Correções de grafia feitas no texto da marca, sem mudar sentido:
`Construindo através` → `Construído através`, `contém por característica` →
`tem por característica`, `mal-uso` → `mau uso`, `gira-lo` → `girá-lo`.

## Fotos de produto

Cada colchão tem três variantes, na ordem em que aparecem no carrossel da página
de produto:

1. **fundo branco** — slide 1
2. **ambientada** — slide 2, só onde a marca tem foto de ambiente
3. **fundo cinza** — slide 3, e é dela que sai o card da home

O padrão do estúdio da marca é o cinza `rgb(159,158,161)`; os fundos brancos são
255 chapado. Onde o guide tem as duas versões, as duas são fotos reais. Onde tem
só uma, a outra é **emulada** por `tools/fundos.py`.

| Modelo | branco | ambientada | cinza |
|---|---|---|---|
| Gipfel | real | — | real |
| Frost | real | — | real |
| Himmel | **emulado** | — | real |
| Mond | **emulado** | — | real |
| Nebel | **emulado** | — | real |
| Wohl | **emulado** | real | real |
| Hemmen | real | real | real (catálogo, 771 px) |
| Motte | **emulado** | — | real |
| Wachen | **emulado** | — | real |
| Zonen | **emulado** | — | real |
| Dorf | real | — | real (catálogo, 771 px) |
| Berg | **emulado** | — | real |
| Eibsee | real | — | real |
| Sylt | real | — | real |

São **8 variantes emuladas e 20 reais** — todas as 8 na direção cinza→branco. **Ambientada existe só para Wohl e Hemmen**
(`familia Wohl.png` e `familia Hemmen.png`); os outros 12 modelos ficam com dois
slides. Não usei as aberturas de coleção do catálogo como ambientada porque elas
mostram um colchão específico, que não é o do modelo em questão.

### Como a emulação funciona

`tools/fundos.py` separa produto e fundo por três critérios ao mesmo tempo: tom
próximo da superfície de fundo estimada, região lisa (gradiente baixo — o sweep do
estúdio é muito suave e a silhueta do produto sempre tem borda) e ligação com a
borda da imagem.

Quatro decisões importam para o recorte não aparecer:

1. **Trabalha em 2× a resolução de saída** (2800×2100), já com o mesmo recorte 4:3
   do arquivo final. A redução final de 2× dilui o erro de meio pixel que sobra na
   borda. A primeira versão segmentava a 820 px e ampliava a máscara 8× — daí o
   halo branco que aparecia em volta do produto.
2. **Máscara em dois estágios**: topologia numa redução de 900 px (robusta) e
   posição exata da borda na resolução de trabalho, só numa faixa em volta da
   silhueta.
3. **Erra para dentro, nunca para fora.** A máscara do produto é erodida 1 px. Um
   fio da borda do produto recebendo a correção é invisível; um anel de fundo
   antigo sem correção salta aos olhos.
4. **Recomposição aditiva**: `saída = I + (1 − α) · (alvo − estimado)`. É a conta
   de decompor e recompor sobre outro fundo — em fundo puro dá exatamente o alvo,
   em produto não muda nada, e no meio da borda dá a mistura correta. A sombra de
   contato fica à mesma distância do fundo novo, sem virar borda de máscara.

O fundo é estimado por **convolução normalizada** de raio grande sobre os pixels de
fundo, não por polinômio: o sweep tem chão claro (~195) e laterais escuras (~158),
37 níveis de amplitude, muito acima de qualquer tolerância útil.

A conversão **se autoconfere**: se o brilho médio dentro do produto mudar mais de 2
níveis, ela falha e não grava. Nas 8 emulações o desvio ficou em 0,00.

Um caso exigiu troca de origem: a foto `_D3A9225` do **Wohl** tem vinheta forte e a
segmentação não fecha. A emulação sai de `_D3A9205`, outro ângulo real do mesmo
produto com sweep uniforme. O slide cinza continua sendo `_D3A9225`.

Todas as originais seguem intactas em `guide_hauzestern/`. Os intermediários ficam
em `.cache-fundos/` (5 MB, **não publicar** — é reproduzível).

### Por que Hemmen e Dorf usam foto do catálogo

Nesses dois a emulação **não fecha**, e a razão é estrutural: colchão branco e liso
contra fundo branco e liso. Na borda traseira do colchão não existe informação
local que separe as duas coisas, e qualquer máscara come um pedaço do produto ou
deixa a sombra serrilhada. Testei seis variações de parâmetro; todas com defeito
visível a 100%.

O catálogo 2026 tem, na página de abertura de cada modelo, um shot de produto em
fundo cinza — **foto real**, inclusive dos dois. São 771×689 px: para o card
(640×480) é praticamente resolução nativa, e no slide de 1400 px fica mole. Foto
real mole é melhor que emulação com recorte visível. `tools/variantes.py` extrai
essas duas direto do PDF do catálogo, então não há arquivo derivado para manter.

Com uma foto real em fundo cinza em alta desses dois modelos, os slides deles
ganham nitidez — é a pendência registrada abaixo.

## Marca

Extraída em vetor dos PDFs de `guide_hauzestern/Identidade Visual/3-Marca/`.
Cada peça tem três variantes: `currentColor` (para inline), `-positivo` (`#1D1D1D`)
e `-negativo` (`#FFFFFF`).

| Arquivo | Uso |
|---|---|
| `marca.svg` | símbolo + logotipo + decodificador — usado no rodapé |
| `logotipo-colchoes.svg` | HAUZESTERN + COLCHÕES — usado no header |
| `logotipo.svg` | só HAUZESTERN |
| `simbolo.svg` | monograma "H" com a estrela |
| `simbolo-reduzido.svg` | versão adaptada para tamanhos pequenos |
| `marca-reduzida.svg` | marca completa adaptada |

O **símbolo** aparece em: favicon (`favicon.svg`, `favicon.ico`, `apple-touch-icon`,
`icon-192/512`), ornamento da seção "A Hauzestern", selo do bloco de garantia,
abertura da página de garantia e no lugar da foto nos produtos sem fotografia.

Reduções mínimas do brandbook (p.10), respeitadas no CSS: logotipo 75px de largura,
símbolo 50px.

## Tokens de marca (`css/style.css`, bloco `:root`)

Brandbook, p.17-18:

| Token | Valor | Origem |
|---|---|---|
| `--preto` | `#1D1D1D` | CMYK 0/0/0/100 · Pantone Process Black C |
| `--branco` | `#FFFFFF` | CMYK 0/0/0/0 |
| `--amarelo` | `#FBDB65` | CMYK 3/12/70/0 · Pantone 120 C — cor **secundária** |
| `--font-display` | Julius Sans One | aproximação de **Utile Display** |
| `--font-texto` / `--font-titulo` | Inter | a fonte de texto da marca |

O brandbook define **duas** famílias, não três. **Utile Display** é licenciada pela
Adobe Fonts e não pode ser auto-hospedada; Julius Sans One entra como aproximação.
Com um kit da Adobe Fonts, trocar **apenas** `--font-display`.

## Conteúdo — de onde vem cada coisa

| No site | Fonte no guide |
|---|---|
| Manifesto, "Zuhause + stern", Grupo Herval / Dois Irmãos / 60 anos | `Identidade Visual/Manifesto.pdf` |
| Três pilares da faixa amarela | `CATÁLOGO 2026`, p.42 |
| Coleções e seus resumos | `CATÁLOGO 2026` + `Produtos/Storytelling Hauzestern 01.09.pdf` |
| Descrição, altura, capacidade, suporte de peso e ícones de cada colchão | `CATÁLOGO 2026`, página do modelo |
| Camadas, na ordem oficial | `CATÁLOGO 2026` (coordenada Y) + `Produtos/_Imagens das camadas dos colchões/*(Texto)` |
| "O que faz a diferença" de cada colchão | `Fichas Técnica/PDF/Ficha Técnica <modelo>.pdf` |
| Sistema de molejo (194 molas ATC; MaxSpring 206 monobloco) | `Fichas Técnica/PDF/*.pdf` |
| Sistema Thermo Flow do Wohl | `Colchão Wohl/_Ficha Técnica/Manual Sistema Thermo Flow_1125-2.pdf` |
| Bases: alturas e pés | `CATÁLOGO 2026`, p.41 |
| Bases: estrutura e revestimento | `Fichas Técnica/PDF/Boxes/*.pdf` (C1705, C1706, C1707, Root) |
| Travesseiros | `CATÁLOGO 2026`, p.40 |
| Página de garantia, integral | `Certificado de Garantia/2-Hauzestern_Certificado de garantia_2023_AF (1).pdf` |
| Representantes, prepostos e assistentes por estado | `representantes.csv` (planilha comercial, na raiz) |
| Fotos de produto, de fábrica e diagramas | `Produtos/`, `Colchão Wohl/` |
| Padrão de loja (ACM preto, letreiro em LED, 7 conjuntos) | `Identidade Visual/BRANDBOOK`, p.23-38 |

Os três ícones da faixa amarela (capulho de algodão, selo com estrela, agulha com
linha) foram redesenhados em SVG a partir do JPG do site antigo — o site no ar não
tem esses ícones como arquivo.

## Carrossel da página de produto

A trilha usa `scroll-snap` com `overflow-x`. Sem JavaScript continua utilizável —
é uma faixa navegável por toque, roda do mouse e teclado; o JS só acrescenta as
setas e os pontos, que ficam escondidos por `html:not(.js)`. Respeita
`prefers-reduced-motion` (sem animação de rolagem). Slide 1 carrega com
`fetchpriority="high"`, os outros com `loading="lazy"`.

## Menu

Ordem dos itens: A Hauzestern, Produtos, Tecnologias, Garantia, Representantes,
Contato. O item **Produtos** abre um submenu com as três linhas, nesta ordem:
Colchões, Bases, Travesseiros. No desktop abre no hover, no foco do teclado e no clique;
no mobile, dentro do painel de tela cheia, abre no toque. `Esc` fecha e devolve
o foco ao botão.

## Representantes

`representantes.html` é gerada de `representantes.csv` — a planilha comercial
exportada do Excel, em CP-1252, com células multilinha. Ela substituiu o bloco
"Onde encontrar" da home: quem quer comprar fala com o representante da região.

São 55 áreas de atuação em 27 UFs (26 estados + DF), agrupadas por região do
IBGE. Cada card traz a área coberta, a equipe de vendas e os contatos —
representante, prepostos e assistentes comerciais, com telefone e e-mail.

`tools/dados_representantes.py` separa nome, telefone e e-mail de cada célula
sem inventar nada:

- telefone vira `tel:+55DDDNNNNNNNNN` e é exibido em `(DD) NNNNN-NNNN`; as
  formas `3249-4448/7773` e `98152-0665 / 99144-1015` viram dois números, o
  segundo herdando DDD e prefixo do primeiro;
- rótulo de linha vira legenda do telefone ("Vendas Online", "whats");
- `COMERCIAL` / `ASSISTÊNCIA` na primeira linha da célula é setor, não pessoa;
- o número entre parênteses depois do nome do lojista é código de cliente do
  ERP e não vai para o site — como também não vai a coluna `EMPRESA FAT.`
  (1100 / 1200) nem o prefixo numérico de `EQUIPE DE VENDAS` ("211\_").

**Caixa alta → grafia legível.** A planilha é toda em maiúsculas. Nomes de
pessoa vão para caixa de título como estão — acento faltando em nome próprio
não é corrigido, porque seria inferência nossa. Nos rótulos internos do ERP a
grafia foi corrigida (`ESCRÍTOR. CAPITAL RN` → Escritório Capital RN,
`ESCRITORIO PE` → Escritório PE, `REGIAO MG` → Região MG, `VITORIA DA
CONQUISTA` → Vitória da Conquista, `TRIANGULO MINEIRO` → Triângulo Mineiro).
Siglas e UFs ficam em caixa alta.

**A coluna COLCHOES não é usada.** Só 43 das 55 linhas têm o `X`, mas o
comercial confirmou que toda a rede atende colchões — o `X` não distingue nada
no nosso contexto. As 55 linhas entram iguais, sem selo e sem ressalva.

**Filtro.** Busca por texto, seletor de UF e chips de região, tudo no cliente (`js/main.js`, seção 7). Títulos de estado e de região
somem quando ficam sem card. `representantes.html#uf-sp` já abre a página
filtrada em São Paulo. Sem JavaScript a barra de filtros não aparece e a lista
completa fica visível.

## SEO

- `title` e `meta description` únicos nas 28 páginas (verificado por `tools/check.py`)
- `canonical` absoluto e um único `h1` por página
- **JSON-LD**: `Organization` (com `parentOrganization` Grupo Herval, endereço e
  telefone) + `ItemList` das 25 URLs de produto na home; `Product` +
  `BreadcrumbList` em cada PDP; `WebPage` + `BreadcrumbList` + `FAQPage` na garantia;
  `WebPage` + `BreadcrumbList` em representantes
- Open Graph e Twitter Card por página, com a foto do próprio produto
- `alt` descritivo e `width`/`height` em todas as imagens (evita CLS)
- `fetchpriority="high"` na imagem principal da PDP e do hero
- Sem JS, o conteúdo aparece: `main.js` adiciona `.js` no `<html>` e só então o CSS
  esconde os `.reveal`
- `sitemap.xml` com 28 URLs, `robots.txt` bloqueando `_arquivo/`,
  `guide_hauzestern/`, `tools/` e `representantes.csv`

**Ao publicar, não subir `representantes.csv`.** O `robots.txt` já o bloqueia,
mas robots não é controle de acesso: a planilha traz códigos de faturamento e de
cliente que ficaram deliberadamente fora da página. O arquivo é insumo de build,
não conteúdo do site.

Ao publicar: trocar `https://www.hauzestern.com` pelo domínio final em
`tools/build_pages.py` (constante `SITE`), regenerar e registrar o sitemap no
Google Search Console.

## Pendências / a validar com a marca

Além das divergências listadas na auditoria:

- **Medidas dos colchões** (largura × comprimento) não constam em nenhum documento
  do guide. A ficha traz altura, capacidade, camadas e suporte de peso, mas **não**
  uma tabela de medidas. Quando vierem, entram em `tools/dados.py`.
- **Eibsee** é o único modelo do catálogo 2026 sem ficha técnica no guide: a página
  dele não tem a seção "O que faz a diferença" porque não há texto para transcrever.
- **Ficha técnica das bases C1674 e C1836**: não existe no guide. As duas páginas
  trazem só o que o catálogo dá e avisam isso.
- **Foto da base C1836**: não existe no guide. A página mostra um marcador com o
  símbolo, sem foto de outro modelo no lugar.
- **Fotos dos travesseiros MH 7618 e MH 7619**: o guide não tem fotografia desses
  moldados; as imagens atuais vêm do site antigo e a PDP avisa isso.
- **Fundo das fotos**: ver a seção [Fotos de produto](#fotos-de-produto). Dez das
  28 variantes têm o fundo emulado porque a foto naquele fundo não existe no guide.
- **Resolução do Dorf**: as duas fotos do Dorf têm 1600×1600 px, a menor resolução
  de todo o banco (os outros modelos vão de 5.000 a 8.800 px). Vale pedir o
  original — as duas variantes do Dorf herdam esse limite.
- **Fotos ambientadas**: existem só para Wohl e Hemmen. Com uma foto de ambiente
  por modelo, os outros 12 carrosséis ganham o slide do meio.
- **Foto real em fundo cinza em alta** de Hemmen e Dorf: hoje o slide desses dois
  usa o shot de 771 px do catálogo, que fica mole em 1400 px.
- **Fotos reais em fundo branco** dos 8 modelos emulados encerram a necessidade de
  emulação.
- **Eiche** tem ficha técnica e diagrama no guide, mas não está no catálogo 2026.
  Não entrou no site. O diagrama ficou em `assets/camadas/eiche.webp`.
- **Quatro celulares sem o nono dígito** em `representantes.csv`, todos na forma
  `+55 51 9xxx-xxxx` (Darlei Lima, Ademir Faleiro, Guilherme Lauxen, Jaqueline
  Hermann). O gerador avisa a cada `build_all` e publica o número como está — não
  inventa o 9. Corrigir na planilha.
- **Catálogo em PDF para download**: definir se o `Hauzestern_Catalogo_2026_WEB.pdf`
  vai ficar público e onde.
- Analytics (GA4 / Tag Manager) ainda não incluído.
- `assets/logo-hauzestern*.png` e `logo-marca.png` são os logos antigos, extraídos
  do site anterior. Ficaram na pasta mas não são mais usados.
- `_harness.html` na raiz é arquivo temporário de ferramenta — pode apagar.
