# -*- coding: utf-8 -*-
"""
Dados reais dos produtos Hauzestern.

REGRA DESTE ARQUIVO: nada aqui é escrito por quem monta o site.
Todo texto de produto é transcrição do material da marca. Onde a marca não
diz, o campo fica vazio — a página se adapta e não inventa.

FONTE DE CADA CAMPO
  poetica ......... CATÁLOGO 2026, página de abertura do modelo (verbatim)
  tecnica ......... CATÁLOGO 2026 + Fichas Técnica/PDF/Ficha Técnica <modelo>.pdf
                    (bloco "COLCHÃO <modelo>", verbatim)
  diferenciais .... Fichas Técnica, blocos "CAMADAS DE CONFORTO" e
                    "DIFERENCIAIS" — o texto que a marca escreveu sobre cada
                    material daquele modelo (verbatim)
  badges .......... ícones de tecnologia da página do modelo no catálogo 2026,
                    conferidos na imagem renderizada da página (não na extração
                    de texto, que embaralha a ordem)
  camadas ......... catálogo 2026, coluna de rótulos ordenada pela coordenada Y
                    (= ordem oficial do diagrama), conferida contra
                    Produtos/_Imagens das camadas dos colchões/*(Texto)
  altura .......... catálogo 2026 e ficha técnica (os dois batem em 14/14)
  capacidade ...... ícone "150Kg"/"170Kg" da página do modelo
  suporte ......... "SUPORTE DE PESO INDIVIDUAL" do catálogo e da ficha
  significado ..... Produtos/Storytelling Hauzestern 01.09.pdf — SÓ onde a marca
                    declara a tradução. Gipfel, Wohl, Hemmen, Dorf e Eibsee não
                    têm tradução em documento nenhum: campo vazio de propósito.
  garantia ........ Fichas Técnica: "Molejo: 1 ano | Demais componentes: 180 dias"

KREFEL (lançamento de 09/2026, posterior ao catálogo 2026)
  A única fonte é documentos/fichas/Ficha Técnica Krefel.pdf. O que nos outros
  modelos vem do catálogo sai dela: poetica = quadro amarelo da p.1; tecnica =
  bloco "COLCHÃO KREFEL"; badges = ícones da p.1; altura = 35 cm (p.2);
  camadas pela coordenada Y da coluna de rótulos da p.1.
  Coleção: a ficha NÃO diz. Está em Raízes por inferência — nome tirado de uma
  cidade (Krefeld) e do que a simboliza (a seda), que é a regra declarada da
  coleção. Confirmar com a marca.

O QUE NÃO ENTRA
  - Medidas de colchão (largura × comprimento): não constam em nenhum documento.
  - Nomes de base do "Desenvolvimento de Produtos.pdf" (Touch, Luna, Aurora,
    Wave, Netuno, Stella, Awake, Zonare): era uma proposta antiga; as bases que
    existem são C1674, C1705, C1706, C1707/Favo, C1836 e Root.
  - Ficha do Eiche existe no guide, mas o modelo não está no catálogo 2026.
  - Régua de firmeza da ficha do Krefel ("Confortável"): nenhum outro modelo
    tem esse dado no site, e a página não tem onde mostrá-lo.

Correções de digitação feitas no texto da marca (só grafia, sem mudar sentido):
  "Construindo através" → "Construído através" (Sylt)
  "contém por característica" → "tem por característica" (Wachen)
  "mal-uso" → "mau uso"
  "gira-lo" → "girá-lo"
"""

COLECOES = {
    'elementos': {
        'nome': 'Elementos',
        'resumo': 'A Coleção Elementos tem como propósito buscar apoio em elementos '
                  'naturais, palpáveis ou não, tendo como base as sensações que os '
                  'colchões promovem ou com o que se parecem. Os nomes dos produtos, '
                  'em alemão, são traduções literais para o que remetem.',
    },
    'propositos': {
        'nome': 'Propósitos',
        'resumo': 'A Coleção Propósitos é a mais tecnológica das três coleções, '
                  'apresentando produtos que fogem do tradicional, seja pela escolha '
                  'de tecidos ou estruturas. Os nomes dos produtos expressam '
                  'sentimentos e sensações.',
    },
    'raizes': {
        'nome': 'Raízes',
        'resumo': 'A Coleção Raízes tem seus produtos nomeados através da análise do '
                  'país e dos pontos principais que o simbolizam. Carregados de '
                  'contextos culturais, se traduzem em um visual com cores diferentes '
                  'das outras coleções.',
    },
}

SUPORTE_PADRAO = ['Até 1,70 m e 130 kg', 'Até 1,80 m e 140 kg', 'Acima de 1,80 m e 150 kg']
SUPORTE_FROST = ['Até 1,70 m e 150 kg', 'Até 1,80 m e 160 kg', 'Acima de 1,80 m e 170 kg']

# --- textos que a marca repete em todas as fichas ---------------------------
MOLAS_ENSACADAS_TXT = (
    'Este sistema de amortecimento conta com 194 molas p/m² fabricadas com o fio de '
    'aço especial ATC (alto teor de carbono) de 2,20 mm, que proporcionam grande '
    'amortecimento ao corpo. Por serem ensacadas individualmente, resultam no '
    'benefício de que, quando um lado do colchão recebe o peso do corpo, o outro lado '
    'não recebe interferência, deixando sua noite muito mais tranquila. A estrutura de '
    'molas ensacadas é envolta por espumas de várias densidades, divididas em camadas e '
    'diversas espessuras, a fim de dar todo o suporte necessário à estrutura interna.')

MAXSPRING_TXT = (
    'Este sistema de amortecimento conta com 206 molas p/m² fabricadas com fio de aço '
    'especial ATC (Alto Teor de Carbono) de 2,00 mm de diâmetro. Um corpo único, '
    'monobloco, de molas entrelaçadas e submetido a um processo de alívio de tensão. '
    'É a tecnologia europeia diretamente para sua casa. Entre os benefícios deste '
    'sistema, o mais característico provém do alto suporte e conforto ao colchão, o que '
    'resulta em uma resiliência uniforme e perene aos seus usuários mesmo com o passar '
    'do tempo.')

# Ficha Técnica Krefel, p.2 — "MICRO MOLAS ENSACADAS / SISTEMA DE MOLEJO"
MICRO_MOLAS_TXT = (
    'Desenvolvida para proporcionar uma adaptação mais precisa aos contornos do corpo e '
    'elevar a sensação de conforto, esse sistema conta com 400 molas p/m² fabricadas com '
    'fio de aço especial ATC (alto teor de carbono) de 1,30 mm. A camada de micro molas '
    'ensacadas é posicionada acima do sistema de molejo principal do colchão. Sua função '
    'é complementar o suporte estrutural, elevando a experiência de descanso. Por serem '
    'menores e ensacadas individualmente, as micro molas distribuem o peso de forma '
    'correta, reduzem os pontos de pressão e respondem de maneira independente aos '
    'movimentos, oferecendo um acolhimento diferenciado sem comprometer o suporte e o '
    'alinhamento da coluna.')

ONE_SIDE_TXT = (
    'Colchão Pillow Top One Side possui camada de conforto localizada na parte superior '
    'do colchão, sobre o molejo. Por sua concepção não há necessidade de virar o '
    'colchão, apenas girá-lo periodicamente para garantir que a espuma se acomode de '
    'forma mais uniforme.')

GARANTIA_FICHA_TXT = (
    'A garantia perderá a validade caso haja constatação de mau uso do colchão sobre a '
    'base sommier ou cama que não ofereça suporte adequado. O uso inadequado poderá '
    'danificar o tecido ou o molejo.')

# --- cuidados: transcrição do Certificado de Garantia -----------------------
CUIDADOS_BASE = [
    'Use o colchão Hauzestern sobre um estrado de ripas lixadas de 4 a 5 cm de largura, '
    'com intervalos de 2 a 3 cm, ou sobre um Box/Sommier. Nunca use o colchão sobre um '
    'estrado inteiriço ou com papéis, papelão, pano ou qualquer outro material que fique '
    'entre o colchão e o estrado.',
    'Gire o colchão Hauzestern a cada 14 dias, no sentido dos pés e da cabeça, para que '
    'ele se ajuste sempre de maneira uniforme ao corpo.',
    'Não dobre, não pule e não fique em pé sobre o colchão Hauzestern.',
    'Não utilize o colchão Hauzestern com a embalagem plástica, pois prejudica sua '
    'ventilação.',
    'O colchão Hauzestern não deve ficar em lugar úmido, sem ventilação ou com falta de '
    'higiene. O Box ou o Sommier devem ser usados sobre superfícies planas, com todos os '
    'pés devidamente apertados e apoiados.',
    'Em caso de revestimentos do tipo napa, courvin, plásticos e similares, não deve ser '
    'utilizado álcool ou qualquer tipo de solvente orgânico para a limpeza, uma vez que '
    'estes podem danificá-los.',
]

COLCHOES = [
  {
    'slug': 'gipfel', 'nome': 'Gipfel', 'colecao': 'elementos', 'significado': '',
    'altura': 32, 'capacidade': 150, 'suporte': SUPORTE_PADRAO,
    'diagrama': None, 'destaque': 'Novo em 2026',
    'poetica': 'Gipfel traduz a imponência do pôr do sol no ponto mais alto da '
               'Alemanha. Inspirado nos tons intensos que tingem os cumes terrosos. '
               'Essa harmonia cromática cria uma atmosfera envolvente, transformando o '
               'colchão em um convite à pausa e ao descanso profundo.',
    'tecnica': [
      'Gipfel foi desenvolvido para atender à necessidade daqueles que buscam mais '
      'conforto e qualidade de sono. Além de possuir um design limpo e sofisticado. '
      'Construído através de uma camada de molas ensacadas de 2.2mm de espessura.',
    ],
    'diferenciais': [
      'Internamente possui uma camada de Viscogel, caracterizada principalmente por sua '
      'viscosidade, permitindo que a espuma se molde aos contornos do corpo. Enquanto a '
      'propriedade do gel auxilia no equilíbrio das temperaturas do colchão.',
      'Além disso, contém uma camada de espuma Premium Foam®, essa espuma de poliuretano '
      'apresenta um melhor desempenho em termos de suporte, complementada pela '
      'resiliência da espuma HR, que possui maior capacidade de retorno, proporcionando '
      'aporte entre o molejo e as camadas superiores.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'badges': ['Molas Ensacadas', 'Bordado Quadro a Quadro', 'Forro Antiderrapante',
               'One Side Pillow', 'Sistema Polyframe', 'Premium Foam',
               'Espuma HR Special', 'Espuma Viscogel'],
    'camadas': [
      'Tecido 62% Poliéster 38% Viscose 235 g/m²',
      'Fibra Poliéster',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Espuma Poliuretano Viscogel D45 kg/m³ — 3 cm',
      'Espuma Poliuretano Alta Resiliência HR35 kg/m³ — 3 cm',
      'Espuma Poliuretano Convencional D28 kg/m³ (PremiumFoam) — 3 cm',
      'Feltro Resinado',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'frost', 'nome': 'Frost', 'colecao': 'elementos', 'significado': 'orvalho',
    'altura': 38, 'capacidade': 170, 'suporte': SUPORTE_FROST, 'diagrama': None,
    'poetica': 'Frost é a materialização de um dia frio de inverno combinado com o '
               'aconchego de estar em um colchão que mescla resistência e '
               'personalidade. Desfrute dos melhores materiais e se permita uma noite '
               'perfeita.',
    'tecnica': [
      'Frost é o colchão que se destaca por sua qualidade e design, mesclando conforto e '
      'beleza em um único produto.',
      'Construído através de uma camada de molas ensacadas de 2.2mm de espessura, essa '
      'composição proporciona um alto nível de conforto e suporte. Além das molas, '
      'destacamos a manta de látex de 8cm em formato de copos, garantindo um conforto '
      'individualizado, acomodando naturalmente o corpo. Essa camada gera um efeito de '
      'duplo molejo, aumentando ainda mais a sensação de relaxamento.',
    ],
    'diferenciais': [
      'As camadas de conforto do colchão Frost são compostas por mantas de espuma de '
      'Poliuretano expandido. Por conta da sua densidade alta, forma um conjunto de '
      'conforto exclusivo junto à camada de molas ensacadas.',
      'Tecido do tampo em Malha com gramatura 400g/m². Construída de bioamida, essa '
      'poliamida é fabricada a partir de biomassa vegetal, garantindo um toque macio, '
      'delicado e sedoso, aumentando a resistência do tecido. A bioamida, além de '
      'sustentável, deixa o tecido com toque fresco, auxiliando a termorregulação '
      'corporal. Destaca-se também o tratamento Peachskin, um tratamento que garante '
      'mais suavidade e conforto à sua pele.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'badges': ['Molas Ensacadas 2.2mm', 'Tecido Malha com Linho', 'One Side Pillow',
               'Bordado Quadro a Quadro', 'Látex', 'Europillow',
               'Malha Antimicrobiana', 'Forro Antiderrapante', 'Flexxi Cup'],
    'camadas': [
      'Tecido 74,4% Poliéster 25,6% Poliamida 400 g/m²',
      'Fibra Poliéster',
      'Fibra Poliéster',
      'Espuma Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Camada Látex Natural D70 kg/m³ — 8 cm',
      'Feltro Resinado',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Feltro Resinado',
      'Espuma Poliuretano Convencional D20 kg/m³ — 3 cm',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'himmel', 'nome': 'Himmel', 'colecao': 'elementos', 'significado': 'céu',
    'altura': 38, 'capacidade': 150, 'suporte': SUPORTE_PADRAO, 'diagrama': 'himmel',
    'poetica': 'Himmel busca apoio em seu nome no Céu, representado pela escolha de '
               'revestimentos que variam do branco até leves tons de azul. O efeito das '
               'nuvens se traduz através do detalhe bordado do tampo e que remete a '
               'algo extremamente confortável.',
    'tecnica': [
      'Himmel foi desenvolvido para você que busca um sono tranquilo e reparador. O '
      'sistema de duplo molejo ajusta perfeitamente o colchão às suas necessidades de '
      'sono. O sistema independente de molas ensacadas combinado com a mola Maxspring '
      'garante um alto nível de conforto e maciez.',
    ],
    'diferenciais': [
      'Internamente conta com uma camada de espuma hipermacia, garantindo um conforto '
      'uniforme sem perder as características que uma espuma de médio suporte oferece. '
      'Este produto também agrega uma espuma de alta densidade em sua composição, '
      'garantindo uma durabilidade muito maior para o seu produto.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'molejo2': MAXSPRING_TXT,
    'badges': ['Molas Ensacadas', 'Molas Maxspring', 'Tecido Malha', 'Europillow',
               'Forro Antiderrapante', 'Espuma Freshcool', 'Espuma HR Special',
               'One Side Pillow'],
    'camadas': [
      'Tecido 100% Poliéster 320 g/m²',
      'Fibra Poliéster',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Camada Isolante',
      'Espuma de Poliuretano Hipermacia D28 kg/m³ (Freshcool) — 3 cm',
      'Espuma de Poliuretano Alta Resiliência D45 kg/m³ (HR Special) — 3 cm',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Feltro Resinado',
      'Molas MaxSpring 206 molas p/m² — Arame 2,0 mm — Suporte 95 kg/m²',
      'Feltro Resinado',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'mond', 'nome': 'Mond', 'colecao': 'elementos', 'significado': 'lua',
    'altura': 33, 'capacidade': 150, 'suporte': SUPORTE_PADRAO, 'diagrama': 'mond',
    'poetica': 'Mond é a representação do elemento da Lua através de um colchão. A '
               'mistura entre o branco e o cinza presentes nos tecidos de uma forma '
               'sutil nos detalhes que revestem o produto, remetem à lua em suas cores.',
    'tecnica': [
      'Mond é o colchão que se destaca por sua qualidade, mesclando o conforto e a '
      'beleza em um único produto.',
      'Construído através de dois níveis de molejo, ambos de molas ensacadas e com '
      'alturas distintas, essa composição proporciona um alto nível de conforto e '
      'maciez. O fato de ter o dobro de “efeito mola” para sustentar a camada de espuma '
      'forma uma composição repleta de conforto e aconchego, ideal para que sua noite de '
      'sono seja muito mais tranquila.',
    ],
    'diferenciais': [
      'As camadas de conforto do colchão Mond são compostas por mantas de espuma de '
      'Poliuretano expandido. Por conta da sua densidade alta, forma junto à base de '
      'duplo molejo um conjunto de conforto exclusivo.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'badges': ['Molas Ensacadas', 'Tecido Malha', 'Bordado Quadro a Quadro',
               'Forro Antiderrapante', 'Espuma de Alta Densidade', 'One Side Pillow',
               'Sistema Polyframe'],
    'camadas': [
      'Tecido 100% Poliéster 203 g/m²',
      'Fibra Poliéster',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Camada Isolante',
      'Espuma de Poliuretano Convencional D28 kg/m³ — 2 cm',
      'Feltro Agulhado',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Feltro Resinado',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'nebel', 'nome': 'Nebel', 'colecao': 'elementos', 'significado': 'névoa',
    'altura': 33, 'capacidade': 150, 'suporte': SUPORTE_PADRAO, 'diagrama': 'nebel',
    'poetica': 'O visual de Nebel dentro da coleção Elementos representa a Névoa. As '
               'cores presentes neste colchão a remeter este fenômeno e a variação de '
               'tons terrosos, criam um efeito de volume, fazendo com que se destaque.',
    'tecnica': [
      'Ideal para quem busca um colchão diferenciado, o Nebel mescla conforto, qualidade '
      'e muita beleza.',
      'Construído através de dois níveis de molejo, ambos de molas ensacadas e com '
      'alturas distintas, essa composição proporciona um alto nível de conforto e '
      'maciez. O fato de ter o dobro de “efeito mola” para sustentar a camada de espuma '
      'forma uma composição repleta de conforto e aconchego, ideal para que sua noite de '
      'sono seja muito mais tranquila.',
    ],
    'diferenciais': [
      'As camadas de conforto do colchão Nebel são compostas por mantas de espuma de '
      'Poliuretano expandido. Por conta da sua densidade alta, forma junto à base de '
      'duplo molejo um conjunto de conforto exclusivo.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'badges': ['Molas Ensacadas', 'Tecido Malha', 'Bordado Quadro a Quadro',
               'Forro Antiderrapante', 'Espuma de Alta Densidade', 'One Side Pillow',
               'Sistema Polyframe'],
    'camadas': [
      'Tecido 100% Poliéster 203 g/m²',
      'Fibra Poliéster',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Camada Isolante',
      'Espuma de Poliuretano Convencional D28 kg/m³ — 2 cm',
      'Feltro Agulhado',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Feltro Resinado',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'wohl', 'nome': 'Wohl', 'colecao': 'propositos', 'significado': '',
    'altura': 38, 'capacidade': 150, 'suporte': SUPORTE_PADRAO,
    'diagrama': None, 'destaque': 'Novo em 2026',
    'lifestyle': ('wohl-familia.jpg',
                  'Família em um quarto claro, sobre um conjunto com o colchão Wohl'),
    'poetica': 'Adaptando-se ao seu ritmo único, materializa um estilo de vida que '
               'valoriza a harmonia entre corpo e ambiente, entre o movimento do dia e a '
               'quietude da noite, criando um microclima ideal.',
    'tecnica': [
      'Wohl apresenta mais uma inovação para a linha Propósitos. Além de contar com '
      'molas ensacadas e espumas de alta qualidade, o novo modelo traz a exclusiva '
      'camada Thermo Flow, que proporciona um aconchego excepcional e uma temperatura '
      'ideal, adaptando-se perfeitamente às necessidades de cada usuário.',
    ],
    'diferenciais': [
      'Internamente, possui a inovadora camada Thermo Flow, projetada com uma série de '
      'canais que facilitam a passagem do ar. Além disso, para tornar a experiência ainda '
      'mais agradável, conta com uma manta Freshcool, caracterizada principalmente por '
      'sua maciez e por apresentar maior espaçamento entre os poros, o que contribui '
      'para uma experiência muito mais sensitiva.',
      'No tampo, apresenta uma malha confeccionada em bioamida, um tipo de fibra de toque '
      'suave e extremo frescor. Além de ser sustentável, essa fibra proporciona um toque '
      'fresco ao tecido, auxiliando na termorregulação corporal. Destaca-se ainda o '
      'tratamento Peachskin, que garante mais suavidade e conforto à pele.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'badges': ['Sistema Thermo Flow', 'Molas Ensacadas', 'Espuma Freshcool',
               'Bordado Quadro a Quadro', 'PremiumFoam', 'Malha PeachSkin',
               'One Side Pillow', 'Sistema Polyframe',
               'Acionamento por Controle Remoto'],
    'camadas': [
      'Tecido 74,4% Poliéster 25,6% Poliamida 400 g/m²',
      'Fibra Poliéster',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Espuma Poliuretano Hipermacia D28 kg/m³ — 3 cm',
      'Espuma Poliuretano Convencional D28 kg/m³ (Thermo Flow) — 4 cm',
      'Espuma Poliuretano Convencional D28 kg/m³ (PremiumFoam) — 5 cm',
      'Feltro Resinado',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 4 cm',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
    # Manual Sistema Thermo Flow_1125-2.pdf — aparelho, não só camada de espuma
    'sistema': {
      'nome': 'Sistema Thermo Flow',
      'intro': 'O Wohl integra um colchão de aquecimento a ar multifuncional. A unidade '
               'principal fica em um compartimento com zíper na parte frontal do colchão '
               'e é operada pelo painel ou pelo controle remoto.',
      'especificacoes': [
        ('Produto', 'Colchão de Aquecimento a Ar — WFN120/180-24V/36V'),
        ('Tensão de operação', '100–240 V ~2 A 50/60 Hz'),
        ('Corrente elétrica', '2,5 A máx.'),
        ('Tensão no colchão', 'DC 24 V / 36 V'),
        ('Consumo', 'não excede 1 kWh por noite'),
        ('Componentes', 'painel de controle, aquecedor de ar, tomada de energia, '
                        'controle remoto e adaptador'),
        ('Garantia do sistema', '1 ano a partir da data da compra, válida '
                                'exclusivamente para o Sistema Thermo Flow'),
      ],
      'modos': [
        ('Ventilação quente', 'Faixa de temperatura ajustável de 20 a 37 °C. '
                              'A temperatura recomendada para dormir é inferior a 34 °C.'),
        ('Ventilação natural', 'Sopra vento natural, sem definir uma temperatura '
                               'específica.'),
        ('Desumidificação e eliminação de ácaros',
         'Ajusta automaticamente a temperatura para 50 °C durante 4 horas. Um aviso '
         'sonoro é emitido ao final.'),
        ('Temporizador', 'Faixa de 0 a 18 horas, com desligamento automático.'),
      ],
      'protecoes': [
        ('Circulação de ar', 'Não há fios de aquecimento elétrico instalados dentro do '
                             'colchão — portanto não há risco de radiação '
                             'eletromagnética, vazamento de eletricidade ou outros '
                             'perigos à segurança.'),
        ('Aquecedor de ar inteligente', 'O ar quente circula uniformemente dentro do '
                                        'colchão para evitar superaquecimento localizado '
                                        'e queimaduras.'),
        ('Proteção contra superaquecimento e sobrecorrente',
         'O colchão possui um dispositivo de proteção embutido que desliga '
         'automaticamente a alimentação em caso de falha.'),
        ('Uso de tensão segura', 'DC 24 V / 36 V.'),
      ],
      'atencao': [
        'Durante o uso do modo de desumidificação e eliminação de ácaros, há risco de '
        'queimaduras térmicas de baixa intensidade. Não durma no colchão durante esse '
        'modo.',
        'Pessoas incapazes de cuidar de si mesmas, bebês, crianças pequenas e pessoas '
        'insensíveis ao calor devem usar o produto sob supervisão de um cuidador.',
        'Durante a utilização dos modos com aquecimento, não é recomendado girar o '
        'colchão em 180°. A rotação nessas condições pode direcionar o fluxo de ar quente '
        'para a parte superior do corpo, causando desconforto devido ao contato direto e '
        'prolongado com o calor durante o sono. A rotação pode ser feita normalmente '
        'quando o aparelho estiver desligado ou operando no modo ventilação.',
        'Não cubra o adaptador de energia com pano nem coloque objetos sobre ele.',
        'Não ative o sistema se o colchão estiver molhado. Limpe e seque completamente '
        'antes de usar.',
      ],
    },
    'cuidados_extra': [
      'Para garantir a durabilidade e o efetivo retorno das espumas, recomenda-se a '
      'rotação periódica do colchão em 180°. Por contemplar o Sistema Thermo Flow, '
      'porém, essa prática exige cuidados específicos — ver as instruções do sistema '
      'nesta página.',
    ],
  },
  {
    'slug': 'hemmen', 'nome': 'Hemmen', 'colecao': 'propositos', 'significado': '',
    'altura': 40, 'capacidade': 150, 'suporte': SUPORTE_PADRAO, 'diagrama': None,
    'poetica': 'Mesclando bem-estar e vitalidade, Hemmen transcende com sua abordagem '
               'inovadora, ao combinar a purificação do carvão ativado com a suavidade '
               'do tecido com percentual de seda, oferecendo um refúgio revigorante '
               'para mente e corpo.',
    'tecnica': [
      'Hemmen se destaca pela utilização de materiais nobres, que vão desde seu '
      'revestimento até seu interior. Destaca-se principalmente pela presença de uma '
      'camada de viscoelástica com carvão ativado, caracterizada por sua porosidade, '
      'permitindo a adsorção e retenção de impurezas pelas micropartículas de carvão, '
      'garantindo um interior livre de contaminantes e bactérias.',
      'Construído através de uma camada de molas ensacadas de 2.2mm de espessura, essa '
      'composição proporciona um alto nível de conforto e suporte.',
    ],
    'diferenciais': [
      'Internamente possui uma camada de viscoelástica com carvão ativado. Destacando '
      'sua maciez e viscosidade, permite a espuma se moldar ao corpo, complementada pelo '
      'carvão ativado que fará a retenção das impurezas, garantindo um sono mais '
      'tranquilo e reparador.',
      'Tecido malha Pure Silk com alto percentual de viscose e seda, com gramatura '
      '280g/m². A viscose é caracterizada pelas propriedades termorreguladoras que '
      'auxiliam no conforto durante o sono. O toque macio e acolhedor é proporcionado '
      'pela seda agregada neste tecido, tornando-o perfeito para uma noite de sono '
      'tranquila e agradável.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'badges': ['Molas Ensacadas', 'Europillow', 'Bordado Quadro a Quadro',
               'Forro Antiderrapante', 'Viscoelástica Carvão Ativado',
               'Espuma HR Special', 'One Side Pillow', 'Tecido Pure Silk'],
    'camadas': [
      'Tecido 59% Poliéster 37% Viscose 4% Seda 280 g/m²',
      'Fibra Poliéster',
      'Fibra Poliéster',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Espuma de Poliuretano Viscoelástica com Carvão Ativado D60 kg/m³ — 5 cm',
      'Espuma de Poliuretano Alta Resiliência HR D35 kg/m³ — 3 cm',
      'Feltro Agulhado',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 3 cm',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'motte', 'nome': 'Motte', 'colecao': 'propositos', 'significado': 'mariposa',
    'altura': 38, 'capacidade': 150, 'suporte': SUPORTE_PADRAO, 'diagrama': 'motte',
    'poetica': 'Motte representa o que há de puro na natureza. Seu visual clean, além '
               'do tampo com percentual de seda fazer alusão ao bicho da seda, grande '
               'responsável pela produção deste material.',
    'tecnica': [
      'Extra macio, o colchão Motte foi desenvolvido para pessoas exigentes que buscam o '
      'melhor conforto. Através de um sistema de duplo molejo, proporciona um conforto '
      'combinado entre as duas tecnologias com características distintas.',
      'Enquanto o molejo Maxspring garante um maior suporte, o molejo com molas '
      'ensacadas individualmente garante estabilidade e uma transição de conforto entre '
      'as molas e a camada de espumas. Para completar, as camadas de conforto do produto '
      'são compostas por nobres espumas HR Special® e Freshcool®.',
    ],
    'diferenciais': [
      'Internamente conta com espuma Freshcool®, uma espuma especial, desenvolvida com '
      'células mais abertas, resultando em uma maior ventilação e aeração ao produto e '
      'gerando uma sensação de maior frescor.',
      'Sua maciez absoluta é complementada pelo suporte da espuma HR Special®, que tem '
      'por característica maior resiliência e capacidade de sustentação, proporcionando '
      'aporte entre os molejos e a camada superior de toque extremamente macio.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'molejo2': MAXSPRING_TXT,
    'badges': ['Molas Ensacadas', 'Molas Maxspring', 'Bordado Quadro a Quadro',
               'Forro Antiderrapante', 'Freshcool', 'Espuma HR Special',
               'One Side Pillow', 'Tecido Pure Silk'],
    'camadas': [
      'Tecido 59% Poliéster 37% Viscose 4% Seda 280 g/m²',
      'Fibra Poliéster',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Camada Isolante',
      'Espuma de Poliuretano Hipermacia D28 kg/m³ — 3 cm',
      'Espuma de Poliuretano Alta Resiliência D45 kg/m³ — 3 cm',
      'Camada Isolante',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Feltro Resinado',
      'Mola MaxSpring 206 molas p/m² — Arame 2,0 mm — Suporte 95 kg/m²',
      'Feltro Resinado',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'wachen', 'nome': 'Wachen', 'colecao': 'propositos', 'significado': 'acordar',
    'altura': 34, 'capacidade': 150, 'suporte': SUPORTE_PADRAO, 'diagrama': 'wachen',
    'poetica': 'Dormir bem tem seu valor, mas acordar bem é melhor ainda. O colchão '
               'Wachen possui tudo para seu sono se tornar impecável. Seus detalhes '
               'feitos a mão garantem um toque único e especial para cada colchão.',
    'tecnica': [
      'Proporcionando conforto mais uniforme em seu colchão, o Wachen traz na sua '
      'estrutura o sistema de molas ensacadas, permitindo que o seu corpo se adeque a '
      'necessidade do sono. O exclusivo bordado lateral agrega beleza ao colchão, também '
      'conta com alças, facilitando a movimentação do colchão. O seu tampo conta com '
      'puxes colocados a mão, agregando nobreza ao colchão.',
    ],
    'diferenciais': [
      'A Espuma Viscoelástica tem por característica principal sua maciez e '
      'viscosidade, permitindo a espuma se moldar ao corpo, garantindo um sono mais '
      'tranquilo e reparador.',
      'Contém espuma Freshcool®, uma espuma especial, desenvolvida com células mais '
      'abertas, resultando em uma maior ventilação e aeração ao produto e gerando uma '
      'sensação de maior frescor. Sua maciez absoluta é complementada pelo suporte da '
      'espuma HR Special®, que tem por característica maior resiliência e capacidade de '
      'sustentação, proporcionando aporte entre os molejos e a camada superior de toque '
      'extremamente macio.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'badges': ['Molas Ensacada', 'Tecido Malha', 'One Side Pillow', 'Espuma Freshcool',
               'Forro Antiderrapante', 'Sistema Polyframe', 'Pillow Pastel',
               'Espuma Viscoelástica', 'Feito à Mão'],
    'camadas': [
      'Tecido 100% Poliéster 428 g/m²',
      'Fibra Poliéster',
      'Espuma de Poliuretano Hipermacia D28 kg/m³ (Freshcool) — 3 cm',
      'Espuma de Poliuretano Viscoelástica D45 kg/m³ — 3 cm',
      'Espuma de Poliuretano Convencional D28 kg/m³ (Premiumfoam) — 5 cm',
      'Feltro Resinado',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'zonen', 'nome': 'Zonen', 'colecao': 'propositos', 'significado': 'zonas',
    'altura': 36, 'capacidade': 150, 'suporte': SUPORTE_PADRAO, 'diagrama': 'zonen',
    'poetica': 'Sentir que ocupa exatamente o lugar que deveria é um dos propósitos da '
               'vida. Zonen nasceu da necessidade de tornar sua noite perfeitamente '
               'ergonômica, adequando seu colchão à sua necessidade.',
    'tecnica': [
      'Buscando o conforto ideal para uma noite tranquila de sono, o colchão Zonen traz '
      'o sistema de zoneamento de molas ensacadas (trizone) permitindo a correta '
      'distribuição do peso durante o uso. As áreas de maior impacto recebem uma camada '
      'de molas mais firmes, já as áreas de menor impacto recebem molas com arame de '
      'diâmetro menor, tudo que você precisa para dormir bem.',
      'Lateralmente conta com um detalhe de faixa em tecido malha e jacquard, agregando '
      'design e sofisticação ao seu produto.',
    ],
    'diferenciais': [
      'Internamente conta com uma camada de espuma hipermacia, garantindo um conforto '
      'uniforme sem perder as características que uma espuma de médio suporte oferece. '
      'Este produto também agrega uma espuma de alta densidade em sua composição, '
      'garantindo uma durabilidade muito maior para o seu produto.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'badges': ['Molas Ensacadas', 'Tecido Malha', 'Bordado Quadro a Quadro',
               'Forro Antiderrapante', 'One Side Pillow', 'Sistema Polyframe',
               'Espuma Freshcool', 'Trizone'],
    'camadas': [
      'Tecido 100% Poliéster 428 g/m²',
      'Fibra Poliéster',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Camada Isolante',
      'Espuma de Poliuretano Hipermacia D28 kg/m³ — 3 cm',
      'Espuma de Poliuretano Convencional D28 kg/m³ — 3 cm',
      'Feltro Agulhado',
      'Molas Ensacadas Individualmente 180 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Molas Ensacadas Individualmente 180 molas p/m² — Arame 2,0 mm — Suporte 80 kg/m²',
      'Feltro Resinado',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 7 cm',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'krefel', 'nome': 'Krefel', 'colecao': 'raizes', 'significado': '',
    'altura': 35, 'capacidade': 150, 'suporte': SUPORTE_PADRAO,
    'diagrama': None, 'destaque': 'Lançamento',
    # "Krefeld" (com d) é a cidade; o produto é "Krefel". Os dois como na ficha.
    'poetica': 'Reconhecida historicamente pela produção têxtil de seda, Krefeld '
               'inspira um produto que traduz a delicadeza, a suavidade ao toque e a '
               'elegância desse material natural. Representa, assim, a união entre a '
               'tradição da seda e uma experiência de conforto refinada.',
    'tecnica': [
      'Krefel busca unir a tradição e experiência de conforto refinado. Seu sistema de '
      'duplo molejo proporciona maior adaptabilidade, ajustando-se às necessidades do '
      'corpo e oferecendo uma experiência de sono mais confortável e envolvente.',
    ],
    'diferenciais': [
      'CloudCore™ Comfort System é uma espuma de alta resiliência que combina maciez, '
      'adaptação e suporte inteligente. Adapta-se ao corpo, aliviando pontos de pressão '
      'e proporcionando uma sensação acolhedora, semelhante à leveza de uma nuvem. Sua '
      'resiliente recuperação mantém o conforto, a estabilidade e a durabilidade do '
      'colchão ao longo do tempo. A estrutura conta ainda com uma camada de Látex '
      'Natural, material nobre, importado da Bélgica, que possui excelente elasticidade '
      'e suporte corporal.',
      # "280g/m²" aqui e "203g/m²" na lista de camadas: divergência da própria
      # ficha, registrada no README. Os dois ficam como a marca publica.
      'Tecido malha Pure Silk com alto percentual de viscose e seda, com gramatura '
      '280g/m². A viscose é caracterizada pelas propriedades termorreguladoras que '
      'auxiliam no conforto durante o sono. O toque macio e acolhedor é proporcionado '
      'pela seda agregada neste tecido, tornando-o perfeito para uma noite de sono '
      'tranquila e agradável.',
    ],
    # a ficha do Krefel escreve "quando um lado do colchão se movimenta" onde as
    # outras dizem "recebe o peso do corpo" — por isso o texto próprio
    'molejo': (
      'Este sistema de amortecimento conta com 194 molas p/m² fabricadas com o fio de '
      'aço especial ATC (alto teor de carbono) de 2,20 mm, que proporcionam grande '
      'amortecimento ao corpo. Por serem ensacadas individualmente, resultam no '
      'benefício de que, quando um lado do colchão se movimenta, o outro não recebe '
      'interferência, deixando sua noite muito mais tranquila. A estrutura de molas '
      'ensacadas é envolta por espumas de várias densidades, divididas em camadas e '
      'diversas espessuras, a fim de dar todo o suporte necessário à estrutura interna.'),
    'molejo2_titulo': 'Micro molas ensacadas',
    'molejo2': MICRO_MOLAS_TXT,
    'icones_da_ficha': True,        # não está no catálogo 2026
    'badges': ['Tecido Malha Pure Silk', 'Molas Ensacadas 2.2mm', 'Micro Molas Ensacadas',
               'Látex Natural', 'One Side Pillow', 'Forro Antiderrapante',
               'Espuma CloudCORE'],
    'camadas': [
      'Tecido 59% Poliéster 39% Viscose 4% Seda 203 g/m²',
      'Fibra Poliéster',
      'Espuma Poliuretano Convencional D29 Soft kg/m³ (CloudCORE) — 2 cm',
      'Micro Molas Ensacadas Individualmente 400 molas p/m² — Arame 1,3 mm — Suporte 80 kg/m²',
      'Feltro Agulhado',
      'Camada Látex Natural D70 kg/m³ — 2 cm',
      'Feltro Agulhado',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Feltro Resinado',
      'Espuma Poliuretano Convencional D20 kg/m³ — 7 cm',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'dorf', 'nome': 'Dorf', 'colecao': 'raizes', 'significado': '',
    'altura': 32, 'capacidade': 150, 'suporte': SUPORTE_PADRAO, 'diagrama': None,
    'poetica': 'É inspirado nas estações gélidas de inverno das vilas germânicas, '
               'apresentando tons acinzentados. As cores quentes da bandeira alemã '
               'quebram sua monotonia, trazendo vivacidade ao revestimento.',
    'tecnica': [
      'Dorf foi desenvolvido para atender à necessidade daqueles que buscam mais '
      'conforto e qualidade de sono. Além de possuir um design limpo e sofisticado.',
    ],
    'diferenciais': [
      'Internamente possui uma camada de Viscogel, caracterizada principalmente por sua '
      'viscosidade, permitindo que a espuma se molde aos contornos do corpo. Enquanto a '
      'propriedade do gel auxilia no equilíbrio das temperaturas do colchão.',
      'Além disso, contém uma camada de espuma Premium Foam®, essa espuma de poliuretano '
      'apresenta um melhor desempenho em termos de suporte, complementada pela '
      'resiliência da espuma HR, que possui maior capacidade de retorno, proporcionando '
      'aporte entre o molejo e as camadas superiores.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'badges': ['Molas Ensacadas', 'Bordado Quadro a Quadro', 'Forro Antiderrapante',
               'One Side Pillow', 'Sistema Polyframe', 'Premium Foam',
               'Espuma HR Special', 'Espuma Viscogel'],
    'camadas': [
      'Tecido 100% Poliéster 320 g/m²',
      'Fibra Poliéster',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Espuma Poliuretano Viscogel D45 kg/m³ — 3 cm',
      'Espuma Poliuretano Alta Resiliência HR35 kg/m³ — 3 cm',
      'Espuma Poliuretano Convencional D28 kg/m³ (PremiumFoam) — 3 cm',
      'Feltro Resinado',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'berg', 'nome': 'Berg', 'colecao': 'raizes', 'significado': 'montanha',
    'altura': 36, 'capacidade': 150, 'suporte': SUPORTE_PADRAO, 'diagrama': 'berg',
    'poetica': 'Berg representa as montanhas que demarcam as paisagens da Alemanha. O '
               'revestimento remete a algo cheio de elementos visuais que compõem muito '
               'bem com a estrutura interna do produto.',
    'tecnica': [
      'Para quem busca um produto diferenciado Berg é o colchão perfeito, proporcionando '
      'sensações únicas mesclando qualidade, conforto e muita beleza.',
    ],
    'diferenciais': [
      'A Espuma Viscoelástica tem por característica principal sua maciez e '
      'viscosidade, permitindo a espuma se moldar ao corpo, garantindo um sono mais '
      'tranquilo e reparador.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'badges': ['Molas Ensacadas', 'Tecido Malha', 'Forro Antiderrapante',
               'One Side Pillow', 'Premium Foam', 'Espuma Viscoelástica'],
    'camadas': [
      'Tecido 82,14% Poliéster 15,37% Algodão 2,49% Elastano — 323 g/m²',
      'Fibra Poliéster',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Espuma de Poliuretano Viscoelástica D45 kg/m³ — 3 cm',
      'Espuma de Poliuretano Convencional D28 kg/m³ (Premium Foam) — 5 cm',
      'Feltro Resinado',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Espuma de Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'eibsee', 'nome': 'Eibsee', 'colecao': 'raizes', 'significado': '',
    'altura': 41, 'capacidade': 150, 'suporte': SUPORTE_PADRAO, 'diagrama': None,
    'poetica': 'Eibsee nasce na primavera, onde o azul profundo se mescla ao dourado '
               'das folhas, tornando-o suave e delicado. Essa combinação harmônica '
               'contribui para um descanso perfeito e revigorante.',
    'tecnica': [
      'Eibsee foi desenvolvido para você que busca um sono tranquilo e reparador. O '
      'sistema de duplo molejo ajusta perfeitamente o colchão às suas necessidades de '
      'sono. O sistema independente de molas ensacadas combinado com a mola Maxspring '
      'garante um alto nível de conforto e maciez.',
    ],
    # Eibsee é o único modelo do catálogo 2026 sem ficha técnica no guide:
    # não há bloco "CAMADAS DE CONFORTO"/"DIFERENCIAIS" para transcrever.
    'diferenciais': [],
    'molejo': MOLAS_ENSACADAS_TXT,
    'molejo2': MAXSPRING_TXT,
    'badges': ['Molas Maxspring', 'Tecido Linho', 'Europillow', 'Molas Ensacadas',
               'Forro Antiderrapante', 'One Side Pillow', 'Espuma HR Special',
               'Freshcool'],
    'camadas': [
      'Tecido 59% Poliéster 29% Viscose 12% Linho 275 g/m²',
      'Fibra Poliéster',
      'Espuma Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Camada Isolante',
      'Espuma Poliuretano Hipermacia D28 kg/m³ (Freshcool) — 3 cm',
      'Espuma Poliuretano Alta Resiliência D45 kg/m³ (HR Special) — 3 cm',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Feltro Resinado',
      'Molas MaxSpring 206 molas p/m² — Arame 2,0 mm — Suporte 95 kg/m²',
      'Feltro Resinado',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
  {
    'slug': 'sylt', 'nome': 'Sylt', 'colecao': 'raizes', 'significado': 'praia',
    'altura': 38, 'capacidade': 150, 'suporte': SUPORTE_PADRAO, 'diagrama': None,
    'poetica': 'Sylt busca referência em uma incrível ilha da Alemanha cercada de areia '
               'branca e paisagens exuberantes. Os tons claros e texturas dos tecidos '
               'contribuem para um visual perfeito e garantem um sono reparador.',
    'tecnica': [
      'Sylt é o colchão que se destaca por sua qualidade e design, mesclando conforto e '
      'beleza em um único produto.',
      'Construído através de uma camada de molas ensacadas de 2.2mm de espessura, essa '
      'composição proporciona um alto nível de conforto e suporte. Além das molas, '
      'destacamos as camadas de espuma viscoelástica com acréscimo de gel e também a '
      'camada de espuma de Alta Resiliência, mantendo seu colchão intacto por muito mais '
      'tempo.',
    ],
    'diferenciais': [
      'As camadas de conforto do colchão Sylt são compostas por mantas de espuma de '
      'Poliuretano expandido. Por conta da sua densidade alta, forma um conjunto de '
      'conforto exclusivo junto à camada de molas ensacadas.',
      'Tecido Malha Jacquard com alto percentual de viscose e linho com gramatura '
      '300g/m². A viscose garante um toque macio, além de propriedades '
      'termorreguladoras que auxiliam no conforto durante o sono. Este tecido conta com '
      'tratamento à base de íons de prata que proporciona efeitos antimicrobianos, '
      'tornando sua noite mais tranquila e livre de preocupações.',
    ],
    'molejo': MOLAS_ENSACADAS_TXT,
    'badges': ['Molas Ensacadas 2.2mm', 'Tecido Malha com Linho',
               'Bordado Quadro a Quadro', 'Forro Antiderrapante',
               'Espuma de Alta Resiliência', 'One Side Pillow', 'Sistema Polyframe',
               'Espuma Viscogel'],
    'camadas': [
      'Tecido 70% Poliéster 16% Viscose 14% Linho 300 g/m²',
      'Fibra Poliéster',
      'Fibra Poliéster',
      'Espuma Poliuretano Convencional D20 kg/m³ — 2 cm',
      'Espuma Poliuretano Viscogel D45 kg/m³ — 3 cm',
      'Espuma Poliuretano Alta Resiliência D35 kg/m³ — 3 cm',
      'Feltro Resinado',
      'Molas Ensacadas Individualmente 194 molas p/m² — Arame 2,2 mm — Suporte 80 kg/m²',
      'Feltro Resinado',
      'Espuma Poliuretano Convencional D20 kg/m³ — 3 cm',
      'Tecido 100% Poliéster 65 g/m² (Antiderrapante)',
    ],
  },
]

# ------------------------------------------------------------------ travesseiros
# Fonte única: CATÁLOGO 2026, p.40. Não há ficha técnica de travesseiro no guide.
# Coleção e tradução: Produtos/Storytelling Hauzestern 01.09.pdf
TRAVESSEIROS = [
  {
    'slug': 'alpen', 'nome': 'Alpen', 'colecao': 'propositos', 'significado': 'Alpes',
    'medidas': '68 × 47 × 20 cm', 'foto': True,
    'poetica': 'Alpen é a combinação ideal entre o conforto da fibra plume e a firmeza '
               'da espuma de alta resiliência, garantindo um conforto inigualável e o '
               'suporte perfeito.',
    'ficha': ['Capa 100% algodão e fechamento em zíper',
              'Enchimento em fibra PLUME 500g',
              'Camada de espuma de alta resiliência de 3cm'],
  },
  {
    'slug': 'harz', 'nome': 'Harz', 'colecao': 'raizes', 'significado': 'formação rochosa',
    'medidas': '68 × 47 × 16 cm', 'foto': True,
    'poetica': 'Harz representa a estabilidade de uma formação natural traduzida para '
               'um travesseiro. Sua estrutura conta com uma camada de espuma de alta '
               'resiliência e uma camada de espuma hipersoft.',
    'ficha': ['Capa 100% algodão e fechamento em zíper',
              'Camada de alta resiliência 3cm',
              'Camada de espuma hipersoft de 3cm'],
  },
  {
    'slug': 'weich', 'nome': 'Weich', 'colecao': 'elementos', 'significado': 'macio',
    'medidas': '68 × 47 × 18 cm', 'foto': True,
    'poetica': 'Weich representa o conforto e a maciez da fibra plume, que combinado '
               'com a camada de espuma viscoelástica criam o suporte ideal para seu '
               'travesseiro.',
    'ficha': ['Capa 100% algodão e fechamento em zíper',
              'Enchimento em fibra PLUME 500g',
              'Espuma Viscoelástica 3cm'],
  },
  {
    # A marca não escreveu texto descritivo para os dois moldados: o catálogo
    # traz apenas as medidas e a nomenclatura em três idiomas.
    'slug': 'mh7618', 'nome': 'MH 7618', 'colecao': '', 'significado': '',
    'medidas': '70 × 40 × 12 cm', 'foto': False, 'poetica': '',
    'ficha': ['Travesseiro tipo Látex Liso',
              'Smooth latex Pillow',
              'Almofada tipo Látex Liso'],
  },
  {
    'slug': 'mh7619', 'nome': 'MH 7619', 'colecao': '', 'significado': '',
    'medidas': '60 × 42 × 12 cm', 'foto': False, 'poetica': '',
    'ficha': ['Space Dream Visco',
              'Travesseiro Premium Cervical Liso',
              'Premium Cervical Smooth Pillow',
              'Almofada Premium Cervical Liso'],
  },
]

# ------------------------------------------------------------------------ bases
# Fontes: CATÁLOGO 2026 p.41 (as seis bases),
#         Fichas Técnica/PDF/Boxes/*.pdf (C1705, C1706, C1707 e Root) e
#         documentos/fichas/Ficha Técnica Box C1836.pdf (chegou em 09/2026).
# C1674 aparece só no catálogo — a página dele é mais curta de propósito,
# com o que existe.
# 'suporte' só onde a ficha dá a carga: a do C1836 diz "Box Rígido suporte
# até 350kg"; as outras fichas não estão aqui para conferir.
BASE_ESTRUTURA = (
    'Estrutura em Madeira de Eucalipto classificada, oriunda de reflorestamento, seca em '
    'estufa antes de ser beneficiada. Sua parte superior conta com Chapa Laminada de '
    '4 mm montada com grampos de aço e fixada com cola PVA (própria para madeira), '
    'proporcionando assim grande resistência ao produto.')
BASE_REVESTIMENTO = (
    'Revestimentos liberados de acordo com a tabela de preços. São diversos '
    'revestimentos para compor peças únicas. Tecido do tampo: Forro TNT.')
BASE_SUPORTE_TXT = (
    'é o box que se destaca por sua alta resistência e durabilidade, oferece suporte '
    'para colchões de diversos tipos e tamanhos Hauzestern, aumentando a vida útil do '
    'seu colchão e qualidade do seu sono.')

BASES = [
  {
    'slug': 'box-root', 'nome': 'Box Root', 'ref': 'Root', 'colecao': 'raizes',
    'significado': 'raiz', 'foto': 'box-root', 'ficha': True,
    'box': '15 cm', 'pes': '15 cm', 'material': 'Pés de madeira',
    'poetica': 'Root significa raízes e faz alusão justamente a sua função de enraizar e '
               'suportar os incríveis colchões Hauzestern. Ter a garantia de algo sólido '
               'nunca foi tão fácil.',
  },
  {
    'slug': 'box-c1674', 'nome': 'Box C1674', 'ref': 'C1674', 'colecao': '',
    'significado': '', 'foto': 'box-c1674', 'ficha': False,
    'box': '15 cm', 'pes': '12 cm', 'material': 'Pés de madeira maciça',
    'poetica': '',
  },
  {
    'slug': 'box-c1705', 'nome': 'Box C1705', 'ref': 'C1705', 'colecao': '',
    'significado': '', 'foto': 'box-c1705', 'ficha': True,
    'box': '20 cm', 'pes': '21 cm', 'material': 'Pés de alumínio',
    'poetica': '',
    # O catálogo 2026 diz "Altura dos Pés: 21cm"; a ficha técnica diz 18,5cm.
    # Fica o valor do catálogo (documento mais recente) e a divergência está
    # registrada no README para a marca resolver.
    'nota_conflito': 'A ficha técnica deste box registra pés de 18,5 cm; o catálogo '
                     '2026 registra 21 cm.',
  },
  {
    'slug': 'box-c1836', 'nome': 'Box C1836', 'ref': 'C1836', 'colecao': '',
    'significado': '', 'foto': 'box-c1836', 'ficha': True,
    'box': '20 cm', 'pes': '14 cm', 'material': 'Pés de madeira',
    'suporte': 'até 350 kg',
    'poetica': '',
  },
  {
    'slug': 'box-c1706', 'nome': 'Box C1706', 'ref': 'C1706', 'colecao': '',
    'significado': '', 'foto': 'box-c1706', 'ficha': True,
    'box': '28 cm', 'pes': '5 cm', 'material': 'Pés de ferro',
    'poetica': '',
  },
  {
    'slug': 'box-favo', 'nome': 'Box Favo', 'ref': 'C1707 / Favo 1707', 'colecao': '',
    'significado': '', 'foto': 'box-favo', 'ficha': True,
    'box': '28 cm', 'pes': '5 cm', 'material': 'Pés de ferro',
    'poetica': '',
  },
]

# --------------------------------------------------------------------- garantia
GARANTIA = {
    'molejo': '1 ano',
    'componentes': '180 dias',
    'legal': '3 meses',
    'box_rigido': '6 meses',
    'cama_bau_estrutura': '1 ano',
    'cama_bau_componentes': '6 meses',
    'codigos': [('G 00', '06 meses'), ('G 001', '01 ano')],
}


# ---------------------------------------------------------------- derivados
def resumo(m):
    """Legenda curta do card: só nomes de ícone do catálogo, na ordem deles."""
    return ' • '.join(m['badges'][:3])
