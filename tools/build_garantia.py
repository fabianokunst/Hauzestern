# -*- coding: utf-8 -*-
"""
Gera garantia.html.

TODO o texto desta pagina e transcricao do documento oficial da marca:
  guide_hauzestern/Certificado de Garantia/
  2-Hauzestern_Certificado de garantia_2023_AF (1).pdf

Prazos por componente vem tambem das fichas tecnicas
("Molejo: 1 ano | Demais componentes: 180 dias").

Nao alterar o conteudo juridico sem o aval da marca.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

import dados
from build_pages import head, header, footer, write, SITE, esc

P = ''  # pagina na raiz

# ---------------------------------------------------------------- biotipos
# Transcrito do certificado, pagina 2. As faixas de altura estao exatamente
# como impressas no documento — inclusive "1,15 a 1,68", que parece ser um
# erro de digitacao da marca (a sequencia logica seria "1,51 a 1,60").
BIO_COLS = ['Até 1,50', '1,15 a 1,68', '1,61 a 1,70', '1,71 a 1,80',
            '1,81 a 1,90', 'Acima de 1,90']
BIO_ROWS = [
    ('até 50 kg',     ['D23', 'D23*/20', 'D23*/20', 'D20', '', '']),
    ('51 a 60 kg',    ['D26', 'D26*/23', 'D23', '', '', '']),
    ('61 a 70 kg',    ['D28', 'D26*/28', 'D26*/28', 'D26*/28', 'D26', '']),
    ('71 a 80 kg',    ['', 'D33', '', 'D28*/33', 'D28*/33', 'D28']),
    ('81 a 90 kg',    ['', '', '', 'D33', '', 'D33*/28']),
    ('91 a 100 kg',   ['', '', 'D40', '', 'D40*/33', 'D33']),
    ('101 a 120 kg',  ['', '', 'D45', '', 'D40', '']),
    ('121 a 150 kg',  ['', '', '', '', 'D45', '']),
]

CUIDADOS = [
    'Use o colchão Hauzestern sobre um estrado de ripas lixadas de 4 a 5 cm de largura, '
    'com intervalos de 2 a 3 cm, ou sobre um Box/Sommier. Nunca use o colchão sobre um '
    'estrado inteiriço ou com papéis, papelão, pano ou qualquer outro material que fique '
    'entre o colchão e o estrado.',
    'Gire o colchão Hauzestern a cada 14 dias, no sentido dos pés e da cabeça, para que '
    'ele se ajuste sempre de maneira uniforme ao corpo. No caso de produtos com Pillow '
    'Tipo Duplo, deve-se, além de girar, também virar o produto de uma face à outra '
    '(vire de lado).',
    'Não dobre, não pule e não fique em pé sobre o colchão Hauzestern.',
    'Não utilize o colchão Hauzestern com a embalagem plástica, pois prejudica sua '
    'ventilação.',
    'O colchão Hauzestern não deve ficar em lugar úmido, sem ventilação ou com falta de '
    'higiene. O Box ou o Sommier devem ser usados sobre superfícies planas, com todos os '
    'pés devidamente apertados e apoiados. Em caso de rangidos nos pés, deve-se verificar '
    'se não houve deslocamento do pé — se for esse o motivo, basta apertar novamente o pé '
    'na estrutura, não sendo este um motivo para assistência técnica.',
    'Em caso de colchões e colchonetes que utilizem revestimentos do tipo napa, courvin, '
    'plásticos e similares (plastificados ou emborrachados), não deve ser utilizado álcool '
    'ou qualquer tipo de solvente orgânico para a limpeza desses tipos de revestimento, '
    'uma vez que estes podem danificá-los.',
]

NAO_COBRE = [
    'Danos causados no revestimento.',
    'Não adequação do cliente ao produto.',
    'Ocorrência de bolor/mofo.',
    'Amarelamento do tecido causado pela luz — sendo, portanto, um acontecimento natural, '
    'que não justifica assistência.',
    'Ocorrência de bolinhas (peeling) no tecido, pois este é um processo natural '
    'ocasionado pelo contato com outros tecidos (roupa de cama, protetor etc.) e pela '
    'movimentação do corpo durante a utilização do produto.',
]

CONDICOES = [
    'Se a etiqueta de identificação do colchão não tiver sido danificada ou retirada do lugar;',
    'Se o colchão não foi danificado por acidente ou infiltração de líquidos ácidos — '
    'por exemplo, a urina;',
    'Se nenhum dos itens dos Cuidados e Instruções de Uso tiver sido ignorado;',
    'O colchão somente será substituído ou consertado após análise criteriosa, feita por '
    'técnicos credenciados pela Hauzestern;',
    'A Hauzestern se reserva o direito de cobrar a visita do técnico credenciado, no caso '
    'de solicitação de assistência técnica, bem como também o frete correspondente. Este '
    'valor será cobrado caso o técnico constate que o produto não apresenta defeito de '
    'fabricação. Isto deverá ser informado no momento do pedido de assistência realizada '
    'pelo cliente.',
]

INDICE = [
    ('sobre', 'Sobre a garantia'),
    ('prazos', 'Prazos por componente'),
    ('duracao', 'Duração da garantia'),
    ('condicoes', 'Condições para usar a garantia'),
    ('cuidados', 'Cuidados e instruções de uso'),
    ('nao-cobre', 'O que não está contemplado'),
    ('assentamento', 'Assentamento da espuma'),
    ('biotipos', 'Tabela de biotipos'),
    ('assistencia', 'Pedir assistência'),
]


def build():
    title = 'Garantia Hauzestern — prazos, cuidados e tabela de biotipos | Hauzestern Colchões'
    desc = ('Termos da garantia Hauzestern: molejo 1 ano e demais componentes 180 dias, '
            'cuidados de uso, o que não é coberto e a tabela de biotipos para colchões '
            'de espuma.')
    canon = f'{SITE}/garantia.html'
    g = dados.GARANTIA

    ld = [{
        '@context': 'https://schema.org', '@type': 'WebPage',
        'name': 'Garantia Hauzestern', 'url': canon, 'description': desc,
        'inLanguage': 'pt-BR',
        'isPartOf': {'@type': 'WebSite', 'name': 'Hauzestern Colchões', 'url': SITE + '/'},
        'publisher': {'@type': 'Organization', 'name': 'Hauzestern Colchões',
                      'parentOrganization': {'@type': 'Organization', 'name': 'Grupo Herval'}},
    }, {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Garantia'},
        ],
    }, {
        '@context': 'https://schema.org', '@type': 'FAQPage',
        'mainEntity': [
            {'@type': 'Question', 'name': 'Qual o prazo de garantia de um colchão Hauzestern?',
             'acceptedAnswer': {'@type': 'Answer', 'text':
              f'Em colchões de molas, o molejo tem garantia de {g["molejo"]} e os demais '
              f'componentes, {g["componentes"]}, a partir da emissão da nota fiscal. '
              'A garantia legal de 3 meses já está inclusa nesse prazo.'}},
            {'@type': 'Question', 'name': 'Quando a garantia começa a valer?',
             'acceptedAnswer': {'@type': 'Answer', 'text':
              'No dia do recebimento do colchão ou do conjunto. O tempo de garantia é '
              'contado a partir da emissão da nota fiscal de compra e depende do código '
              'de identificação na etiqueta do produto.'}},
            {'@type': 'Question', 'name': 'O assentamento da espuma é coberto pela garantia?',
             'acceptedAnswer': {'@type': 'Answer', 'text':
              'Não. Um assentamento natural de até 10% da altura total do colchão é '
              'considerado normal. Conforme a ABNT, toda espuma de poliuretano sofre '
              'desgaste natural e pode perder até 25% da rigidez original.'}},
            {'@type': 'Question', 'name': 'O que invalida a garantia?',
             'acceptedAnswer': {'@type': 'Answer', 'text':
              'Etiqueta de identificação danificada ou retirada, danos por acidente ou '
              'infiltração de líquidos ácidos, tecido sujo, urinado ou rasgado, uso sobre '
              'base inadequada e densidade incompatível com o biotipo do usuário.'}},
        ],
    }]

    idx = '\n        '.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in INDICE)
    cuidados = '\n        '.join(f'<li>{c}</li>' for c in CUIDADOS)
    nao = '\n        '.join(f'<li>{c}</li>' for c in NAO_COBRE)
    cond = '\n        '.join(f'<li>{c}</li>' for c in CONDICOES)
    codigos = '\n      '.join(
        f'<div><dt>Código {c}</dt><dd>{v}</dd></div>' for c, v in g['codigos'])

    thead = '\n            '.join(f'<th scope="col">{c}</th>' for c in BIO_COLS)
    tbody = ''
    for peso, cels in BIO_ROWS:
        tds = ''.join(f'<td>{v}</td>' for v in cels)
        tbody += f'\n          <tr><th scope="row">{peso}</th>{tds}</tr>'

    return head(P, title, desc, canon, 'assets/brand/marca-positivo.svg', 'article', ld) + f'''
<body class="interna">
{header(P)}
<main id="main">

<!-- ============================= ABERTURA ============================= -->
<section class="gar-hero" aria-labelledby="gar-title">
  <div class="wrap narrow center">
    <img class="simbolo-orn" src="assets/brand/simbolo-negativo.svg" alt="" width="479" height="572">
    <p class="eyebrow light">Certificado de Garantia</p>
    <h1 id="gar-title" class="display">A garantia do seu Hauzestern</h1>
    <p class="lede">Seu colchão possui Garantia de Fábrica, de acordo com as normas do
      Código de Defesa do Consumidor brasileiro e da ABNT, e foi produzido sob rígido
      controle de qualidade. Esta página reproduz o Certificado de Garantia que acompanha
      o produto.</p>
    <dl class="gar-resumo">
      <div>
        <dt>Molejo</dt>
        <dd>{g['molejo']}
          <small>Em colchões de molas, o prazo do certificado se refere ao molejo.</small>
        </dd>
      </div>
      <div>
        <dt>Demais componentes</dt>
        <dd>{g['componentes']}
          <small>Contados a partir da emissão da nota fiscal.</small>
        </dd>
      </div>
      <div>
        <dt>Garantia legal</dt>
        <dd>{g['legal']}
          <small>Já inclusa no tempo de Garantia Hauzestern.</small>
        </dd>
      </div>
    </dl>
  </div>
</section>

<section class="section">
  <div class="wrap gar-layout">

    <!-- ------------------------------- índice ------------------------------- -->
    <nav class="gar-index reveal" aria-labelledby="idx-title">
      <h2 id="idx-title">Nesta página</h2>
      <ul>
        {idx}
      </ul>
    </nav>

    <!-- ------------------------------ conteúdo ------------------------------ -->
    <div>

      <article class="gar-bloco reveal" id="sobre">
        <h2>Sobre a garantia</h2>
        <p>O produto Hauzestern que você escolheu possui Garantia de Fábrica, de acordo
          com as normas do Código de Defesa do Consumidor Brasileiro e da ABNT
          (Associação Brasileira de Normas Técnicas), e foi produzido sob rígido controle
          de qualidade. Ele foi desenvolvido para oferecer a você conforto para o seu bem
          dormir.</p>
        <p>É importante a leitura sobre os termos desta Garantia, assim como sobre seu Uso
          e Manutenção. Os prazos seguem o Código de Garantia de cada produto, que se
          encontra na etiqueta afixada ao seu colchão.</p>
        <h3>Código na etiqueta e tempo de garantia</h3>
        <dl class="gar-codigos">
      {codigos}
        </dl>
        <p class="nota">A garantia legal de 3 meses já está inclusa no Tempo de Garantia
          Hauzestern.</p>
      </article>

      <article class="gar-bloco reveal" id="prazos">
        <h2>Prazos por componente</h2>
        <p>Em <strong>colchões de molas</strong>, o prazo do certificado se refere ao
          molejo do produto. Os demais componentes estão cobertos pela garantia pelo prazo
          de até <strong>180 dias</strong> a partir da emissão da Nota Fiscal.</p>
        <p>Em <strong>colchões de espuma</strong>, por ela ser o principal componente, a
          garantia considerada segue a codificação estipulada na etiqueta. Os demais
          componentes estão cobertos pelo prazo legal de até <strong>90 dias</strong> a
          partir da emissão da Nota Fiscal.</p>
        <p>No <strong>box rígido</strong>, a garantia é de 6 meses. Na <strong>cama
          baú</strong>, a garantia é de 1 ano para a estrutura e de 6 meses para os demais
          componentes.</p>
        <p>A garantia só é válida mediante apresentação do Certificado de Garantia
          juntamente com a Nota Fiscal do produto. O tempo de Garantia Hauzestern inicia a
          partir da emissão da Nota Fiscal de compra.</p>
      </article>

      <article class="gar-bloco reveal" id="duracao">
        <h2>Duração da garantia</h2>
        <p>Esta garantia começa no dia do recebimento do colchão ou do conjunto e é válida
          com a apresentação da nota fiscal junto ao Certificado de Garantia. Caso o
          produto necessite de consertos ou substituição, esta garantia
          <strong>não será renovada ou estendida</strong>.</p>
        <p>Esta garantia está de acordo com o código de identificação contido na etiqueta
          do produto (Tabela de Garantia Hauzestern).</p>
        <h3>Substituição de modelo</h3>
        <p>Caso o colchão adquirido seja substituído por outro modelo, ou ocorra troca de
          tecido e/ou componentes do produto, os mesmos serão substituídos pelos modelos
          vigentes mais semelhantes.</p>
      </article>

      <article class="gar-bloco reveal" id="condicoes">
        <h2>Condições para usar a garantia</h2>
        <p>Você faz uso dos seus direitos de garantia Hauzestern observando as seguintes
          condições:</p>
        <ul class="gar-lista">
        {cond}
        </ul>
      </article>

      <article class="gar-bloco reveal" id="cuidados">
        <h2>Cuidados e instruções de uso</h2>
        <p>Sabemos que alguns cuidados são essenciais para garantir que o seu colchão dure
          por muito mais tempo. Aqui vão algumas sugestões:</p>
        <ul class="gar-lista">
        {cuidados}
        </ul>
      </article>

      <article class="gar-bloco reveal" id="nao-cobre">
        <h2>O que não está contemplado na garantia</h2>
        <ul class="gar-lista">
        {nao}
        </ul>
        <p>Não concedemos garantia para colchões que estejam com o tecido sujo, urinado ou
          rasgado, pois refletem condições de mau uso. Defeitos ocorridos por transporte
          também não estão incluídos na garantia.</p>
        <p>Atente para que a densidade e o tipo de colchão adquirido estejam de acordo com
          o biotipo das pessoas que irão utilizá-lo. No caso de aumento de peso e/ou
          altura da pessoa, dependendo do grau de alteração dessas medidas, o colchão passa
          a não ser adequado ao biotipo dela, invalidando a garantia.</p>
      </article>

      <article class="gar-bloco reveal" id="assentamento">
        <h2>Assentamento da espuma</h2>
        <p>Conforme o produto for utilizado, um assentamento natural da espuma de
          <strong>10% da altura total do colchão</strong> é considerado normal, já que não
          acarreta alteração da qualidade e do conforto do mesmo.</p>
        <p>De acordo com a ABNT (Associação Brasileira de Normas Técnicas), toda espuma de
          poliuretano sofre um desgaste natural e pode perder até <strong>25% de sua
          rigidez original</strong>. Por isso, não se concede a garantia nos casos de
          assentamento/ajustamento da espuma.</p>
      </article>

      <article class="gar-bloco reveal" id="biotipos">
        <h2>Tabela de biotipos</h2>
        <p>Para colchões de espuma, a densidade adequada depende da altura e do peso de
          quem vai dormir nele. Escolher fora da tabela invalida a garantia.</p>
        <div class="tab-scroll">
          <table class="tabela-biotipos" aria-label="Densidade indicada por altura e peso"
                 aria-describedby="bio-fonte">
            <thead>
              <tr>
                <th scope="col">Altura (m) / Peso (kg)</th>
            {thead}
              </tr>
            </thead>
            <tbody>{tbody}
            </tbody>
          </table>
        </div>
        <p class="tab-fonte" id="bio-fonte"><span class="tab-hint">Arraste a tabela para
          o lado para ver todas as faixas de altura.</span> Densidade indicada por altura
          (m) e peso (kg). Tabela oficial do INER — Instituto de Estudo do Repouso.
          Transcrita do Certificado de Garantia Hauzestern.</p>
        <h3>Casais de biotipos diferentes</h3>
        <ul class="gar-lista">
          <li><strong>A</strong> — Escolha de acordo com o cônjuge que requeira maior
            densidade; ou</li>
          <li><strong>B</strong> — Adquira, mediante encomenda na loja, colchão composto
            de 2 densidades, adequadas a cada biotipo.</li>
        </ul>
        <p class="nota">Para recém-nascidos e crianças de até 3 anos de idade, a densidade
          indicada é D18.</p>
      </article>

      <article class="gar-bloco reveal" id="assistencia">
        <h2>Pedir assistência</h2>
        <p>Guarde o Certificado de Garantia e a Nota Fiscal: os dois são necessários para
          qualquer solicitação. Com eles em mãos, fale com a loja onde comprou o produto
          ou com o nosso time.</p>
        <div class="pdp-cta">
          <a class="btn btn-dark" href="tel:+555135648300">Falar com a gente — (51) 3564-8300</a>
          <a class="btn btn-ghost-dark" href="representantes.html">Falar com um representante</a>
        </div>
        <p class="nota">Esta página é a transcrição do Certificado de Garantia Hauzestern.
          Em caso de divergência, vale o documento impresso que acompanha o produto.</p>
      </article>

    </div>
  </div>
</section>

</main>
{footer(P)}'''


if __name__ == '__main__':
    n = write('garantia.html', build())
    print(f'garantia.html  {n//1024}KB')
