/* =========================================================
   HAUZESTERN — busca de produtos
   A lupa do header abre um painel que procura nos produtos por nome,
   codigo e qualquer caracteristica publicada na pagina: tecnologia,
   camada, altura, capacidade, medida, pes, material.

   O indice (js/busca-index.js) e gerado por tools/build_busca.py a
   partir de tools/dados.py e so e baixado quando a pessoa chega perto
   da lupa. Entra por <script> e nao por fetch() porque o site tambem
   roda aberto direto do disco, onde fetch de arquivo local e bloqueado.

   1. Texto: normalizacao e tokens
   2. Indice
   3. Busca e pontuacao
   4. Destaque do termo
   5. Painel
   6. Medicao (GA4)
   ========================================================= */
(function () {
  'use strict';

  var botoes = document.querySelectorAll('[data-busca-abrir]');
  if (!botoes.length) return;
  if (!String.prototype.normalize) {
    Array.prototype.forEach.call(botoes, function (b) { b.hidden = true; });
    return;
  }

  /* raiz do site a partir do proprio script: vale em subpasta (GitHub
     Pages de projeto) e em file://, como os caminhos relativos do resto */
  var eu = document.currentScript || document.querySelector('script[src*="busca.js"]');
  var RAIZ = eu.src.replace(/js\/busca\.js(?:[?#].*)?$/, '');

  /* ---------- 1. Texto ---------- */
  var ACENTOS = /[̀-ͯ]/g;
  var RE_TOKEN = /[a-z]+|\d+(?:\.\d+)?/g;

  /* minusculas, sem acento, ³ -> 3, virgula decimal -> ponto.
     Mantem o comprimento: a posicao i do texto normalizado e a posicao i
     do original, e e assim que o destaque sabe onde pintar. */
  function normaliza(s) {
    var out = '';
    for (var i = 0; i < s.length; i++) {
      var c = s.charAt(i).toLowerCase();
      if (c > '\u007f') c = c.normalize('NFKD').replace(ACENTOS, '');
      out += c.charAt(0) || ' ';
    }
    return out.replace(/(\d),(?=\d)/g, '$1.');
  }

  function tokens(norm) {
    var lista = [], m;
    RE_TOKEN.lastIndex = 0;
    while ((m = RE_TOKEN.exec(norm))) {
      lista.push({ t: m[0], a: m.index, b: m.index + m[0].length,
                   num: m[0].charCodeAt(0) < 97 });
    }
    return lista;
  }

  /* plural simples, igual no texto e na consulta: colchoes -> colchao */
  function raiz(w) {
    if (w.length > 4 && w.slice(-3) === 'oes') return w.slice(0, -3) + 'ao';
    if (w.length > 3 && w.charAt(w.length - 1) === 's') return w.slice(0, -1);
    return w;
  }

  /* "D45", "MH 7618", "38 cm", "2,2 mm": letra e numero colados ou
     separados por um espaco tambem viram um token so. E o que faz a
     busca por codigo e por medida nao casar pedacos soltos do texto. */
  function compostos(norm, toks) {
    var lista = [];
    for (var i = 0; i + 1 < toks.length; i++) {
      var p = toks[i], q = toks[i + 1], vao = q.a - p.b;
      if (p.num === q.num) continue;
      if (vao === 0 || (vao === 1 && norm.charAt(p.b) === ' ')) {
        lista.push({ t: p.t + q.t, a: p.a, b: q.b, vao: vao });
      }
    }
    return lista;
  }

  var PARADA = {};
  ('a o e as os de da do das dos em no na nos nas com para por um uma que ou ao')
    .split(' ').forEach(function (w) { PARADA[w] = 1; });

  /* palavra de categoria filtra em vez de buscar no texto: "colchao latex"
     traz so colchoes, nao o travesseiro de latex */
  var CATEGORIAS = { colchao: 'Colchões', base: 'Bases', box: 'Bases',
                     travesseiro: 'Travesseiros' };

  function categoria(r) {
    for (var k in CATEGORIAS) {
      if (k === r || (r.length >= 4 && k.lastIndexOf(r, 0) === 0)) return CATEGORIAS[k];
    }
    return '';
  }

  /* ---------- 2. Indice ---------- */
  var PESOS = { n: 10, k: 7, f: 4, x: 1 };
  var INDICE = null, VOCAB = null, SUGESTOES = [];

  function campo(txt, w, mostra) {
    var norm = normaliza(txt), toks = tokens(norm);
    toks.forEach(function (tk) { tk.r = tk.num ? tk.t : raiz(tk.t); });
    return {
      txt: txt, w: w, mostra: mostra, toks: toks,
      comps: compostos(norm, toks),
      frase: ' ' + toks.map(function (tk) { return tk.t; }).join(' ') + ' '
    };
  }

  function prepara(dados) {
    var vocab = Object.create(null);
    SUGESTOES = dados.sugestoes || [];
    INDICE = dados.produtos.map(function (p, ordem) {
      var campos = [], mapa = Object.create(null);
      function guarda(t, w) {
        if (!mapa[t] || mapa[t] < w) mapa[t] = w;
        vocab[t] = 1;
      }
      ['n', 'k', 'f', 'x'].forEach(function (nivel) {
        (p[nivel] || []).forEach(function (txt) {
          var c = campo(txt, PESOS[nivel], nivel !== 'n');
          campos.push(c);
          c.toks.forEach(function (tk) { guarda(tk.r, c.w); });
          c.comps.forEach(function (tk) { guarda(tk.t, c.w); });
        });
      });
      return { p: p, ordem: ordem, campos: campos, mapa: mapa,
               chaves: Object.keys(mapa), titulo: campo(p.t, PESOS.n, false) };
    });
    VOCAB = Object.keys(vocab);
  }

  function existe(t) {
    for (var i = 0; i < VOCAB.length; i++) {
      if (VOCAB[i].lastIndexOf(t, 0) === 0) return true;
    }
    return false;
  }

  /* ---------- 3. Busca e pontuacao ---------- */
  function consulta(q) {
    var norm = normaliza(q).replace(/(\d)\s*x\s*(?=\d)/g, '$1 ');   /* 68x47 */
    var toks = tokens(norm);
    var frase = toks.map(function (tk) { return tk.t; }).join(' ');
    var uteis = toks.filter(function (tk) { return tk.num || !PARADA[tk.t]; });
    if (uteis.length) toks = uteis;

    var termos = [], cats = [];
    for (var i = 0; i < toks.length; i++) {
      var a = toks[i], b = toks[i + 1];
      if (b && a.num !== b.num && existe(a.t + b.t)) {
        termos.push({ t: a.t + b.t, tipo: 'comp', n: a.t.length + b.t.length });
        i++;
        continue;
      }
      if (a.num) { termos.push({ t: a.t, tipo: 'num' }); continue; }
      var r = raiz(a.t), cat = categoria(r);
      if (cat) { if (cats.indexOf(cat) < 0) cats.push(cat); continue; }
      termos.push({ t: r, tipo: 'alfa', n: a.t.length });
    }
    return { termos: termos, cats: cats, frase: toks.length > 1 ? ' ' + frase : '' };
  }

  /* melhor peso do termo nesta entrada: exato vale o peso, prefixo 80% */
  function casa(ent, tm) {
    var m = ent.mapa, melhor = m[tm.t] || 0;
    if (tm.alt) {
      tm.alt.forEach(function (k) { if (m[k] && m[k] * 0.5 > melhor) melhor = m[k] * 0.5; });
      return melhor;
    }
    if (tm.tipo === 'num' || melhor >= PESOS.n) return melhor;
    for (var i = 0; i < ent.chaves.length; i++) {
      var k = ent.chaves[i];
      if (k.length > tm.t.length && k.lastIndexOf(tm.t, 0) === 0 && m[k] * 0.8 > melhor) {
        melhor = m[k] * 0.8;
      }
    }
    return melhor;
  }

  /* distancia de edicao com transposicao ("ltaex" -> "latex") */
  function distancia(a, b, max) {
    if (Math.abs(a.length - b.length) > max) return max + 1;
    var d = [], i, j;
    for (i = 0; i <= a.length; i++) d[i] = [i];
    for (j = 1; j <= b.length; j++) d[0][j] = j;
    for (i = 1; i <= a.length; i++) {
      var menor = max + 1;
      for (j = 1; j <= b.length; j++) {
        var v = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                         d[i - 1][j - 1] + (a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1));
        if (i > 1 && j > 1 && a.charAt(i - 1) === b.charAt(j - 2)
            && a.charAt(i - 2) === b.charAt(j - 1)) v = Math.min(v, d[i - 2][j - 2] + 1);
        d[i][j] = v;
        if (v < menor) menor = v;
      }
      if (menor > max) return max + 1;
    }
    return d[a.length][b.length];
  }

  /* palavras do catalogo parecidas com um termo que nao achou nada:
     compara com a palavra inteira e com o comeco dela (quem ainda esta
     digitando "maxpri" quer "maxspring") */
  function parecidas(t) {
    var max = t.length >= 7 ? 2 : 1;
    return VOCAB.filter(function (k) {
      if (k.length < 3 || !/^[a-z]+$/.test(k)) return false;
      if (distancia(t, k, max) <= max) return true;
      return k.length > t.length
        && (distancia(t, k.slice(0, t.length), max) <= max
            || distancia(t, k.slice(0, t.length + 1), max) <= max);
    });
  }

  function busca(q) {
    var c = consulta(q), aproximado = false;
    if (!c.termos.length && !c.cats.length) return null;

    c.termos.forEach(function (tm) {
      if (tm.tipo !== 'alfa' || tm.t.length < 4) return;
      var algum = INDICE.some(function (e) { return casa(e, tm) > 0; });
      if (!algum) {
        tm.alt = parecidas(tm.t);
        if (tm.alt.length) aproximado = true;
      }
    });

    var todos = [];
    INDICE.forEach(function (e) {
      if (c.cats.length && c.cats.indexOf(e.p.g) < 0) return;
      var nota = c.cats.length * 5, achou = 0;
      c.termos.forEach(function (tm) {
        var s = casa(e, tm);
        if (s > 0) { achou++; nota += s; }
      });
      if (c.frase) {
        var bonus = 0;
        e.campos.forEach(function (cp) {
          if (cp.frase.indexOf(c.frase) >= 0 && cp.w * 1.5 > bonus) bonus = cp.w * 1.5;
        });
        nota += bonus;
      }
      todos.push({ e: e, nota: nota, achou: achou });
    });

    var n = c.termos.length, modo = 'todos';
    var itens = todos.filter(function (r) { return r.achou === n; });
    if (!itens.length && n > 1) {
      modo = 'algum';
      itens = todos.filter(function (r) { return r.achou > 0; });
    }
    itens.sort(function (a, b) {
      return (b.achou - a.achou) || (b.nota - a.nota) || (a.e.ordem - b.e.ordem);
    });
    return { itens: itens, modo: modo, termos: c.termos, aproximado: aproximado };
  }

  /* ---------- 4. Destaque do termo ---------- */
  /* trechos do campo que casam com cada termo, e quantos termos casaram */
  function faixas(cp, termos) {
    var lista = [], vistos = 0;
    termos.forEach(function (tm) {
      var achou = false;
      if (tm.tipo === 'comp') {
        cp.comps.forEach(function (k) {
          if (k.t.lastIndexOf(tm.t, 0) === 0) {
            lista.push([k.a, k.t === tm.t ? k.b : Math.min(k.b, k.a + tm.n + k.vao)]);
            achou = true;
          }
        });
      } else {
        cp.toks.forEach(function (tk) {
          var ok;
          if (tm.alt) ok = tm.alt.indexOf(tk.r) >= 0;
          else if (tm.tipo === 'num') ok = tk.t === tm.t;
          else ok = tk.r.lastIndexOf(tm.t, 0) === 0;
          if (!ok) return;
          var inteiro = tm.alt || tk.r === tm.t || tm.tipo === 'num';
          lista.push([tk.a, inteiro ? tk.b : Math.min(tk.b, tk.a + tm.n)]);
          achou = true;
        });
      }
      if (achou) vistos++;
    });
    return { lista: lista, n: vistos };
  }

  function pinta(el, txt, lista) {
    lista = lista.slice().sort(function (a, b) { return a[0] - b[0]; });
    var pos = 0;
    lista.forEach(function (f) {
      if (f[1] <= pos) return;
      var a = Math.max(f[0], pos);
      if (a > pos) el.appendChild(document.createTextNode(txt.slice(pos, a)));
      var mk = document.createElement('mark');
      mk.textContent = txt.slice(a, f[1]);
      el.appendChild(mk);
      pos = f[1];
    });
    if (pos < txt.length) el.appendChild(document.createTextNode(txt.slice(pos)));
  }

  /* texto longo: recorta uma janela em volta do primeiro termo */
  var JANELA = 150;
  function recorta(txt, lista) {
    if (txt.length <= JANELA + 20) return { txt: txt, lista: lista };
    var ini = Math.min.apply(null, lista.map(function (f) { return f[0]; }));
    var a = Math.max(0, ini - 45), sp = txt.indexOf(' ', a);
    if (a > 0 && sp >= 0 && sp < ini) a = sp + 1;
    var b = Math.min(txt.length, a + JANELA);
    if (b < txt.length) b = txt.lastIndexOf(' ', b) > a ? txt.lastIndexOf(' ', b) : b;
    var pre = a > 0 ? '… ' : '', pos = b < txt.length ? ' …' : '';
    return {
      txt: pre + txt.slice(a, b) + pos,
      lista: lista.filter(function (f) { return f[0] >= a && f[1] <= b; })
                  .map(function (f) { return [f[0] - a + pre.length, f[1] - a + pre.length]; })
    };
  }

  /* o campo que melhor explica por que o produto apareceu */
  function trecho(e, termos) {
    var t = faixas(e.titulo, termos);
    if (t.n === termos.length) return null;          /* o nome ja explica */
    var melhor = null;
    e.campos.forEach(function (cp) {
      if (!cp.mostra || cp.txt === e.p.c || cp.txt === e.p.d) return;
      var f = faixas(cp, termos);
      if (!f.n) return;
      /* empate fica com o primeiro: a ordem do indice e a ordem da pagina */
      var nota = f.n * 100 + cp.w;
      if (!melhor || nota > melhor.nota) melhor = { cp: cp, lista: f.lista, nota: nota };
    });
    return melhor && recorta(melhor.cp.txt, melhor.lista);
  }

  /* ---------- 5. Painel ---------- */
  var dlg, campoBusca, lista, status, inicio, nada, ativo = -1, origem = null;
  var carregando = false, esperando = [], aviso;

  function carregaIndice(pronto) {
    if (INDICE) { if (pronto) pronto(); return; }
    if (pronto) esperando.push(pronto);
    if (carregando) return;
    carregando = true;
    var s = document.createElement('script');
    s.src = RAIZ + 'js/busca-index.js';
    s.onload = function () {
      carregando = false;
      if (!window.HZ_BUSCA) return s.onerror();
      prepara(window.HZ_BUSCA);
      var fila = esperando; esperando = [];
      fila.forEach(function (fn) { fn(); });
    };
    s.onerror = function () {
      carregando = false;
      esperando = [];
      if (status) status.textContent = 'Não foi possível carregar a busca. Tente de novo em instantes.';
    };
    document.head.appendChild(s);
  }

  var LUPA = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">'
    + '<circle cx="10.5" cy="10.5" r="6.25" fill="none" stroke="currentColor" stroke-width="1.5"/>'
    + '<path d="m15.2 15.2 5.3 5.3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';

  function monta() {
    dlg = document.createElement('dialog');
    dlg.className = 'busca';
    dlg.setAttribute('aria-label', 'Buscar produtos');
    dlg.innerHTML =
      '<div class="busca-painel">'
      + '<div class="busca-topo">' + LUPA
      +   '<input class="busca-campo" id="busca-campo" type="search" role="combobox"'
      +   ' aria-expanded="false" aria-controls="busca-lista" aria-autocomplete="list"'
      +   ' aria-label="Buscar produtos por nome, código ou característica"'
      +   ' placeholder="Nome, código ou característica" autocomplete="off"'
      +   ' autocorrect="off" autocapitalize="none" spellcheck="false" enterkeyhint="go">'
      +   '<button class="busca-fechar" type="button" aria-label="Fechar busca">'
      +     '<span class="busca-esc" aria-hidden="true">Esc</span>'
      +     '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"'
      +     ' fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
      +   '</button>'
      + '</div>'
      + '<p class="busca-status" id="busca-status" role="status" aria-live="polite"></p>'
      + '<div class="busca-corpo">'
      +   '<ul class="busca-lista" id="busca-lista" role="listbox" aria-label="Produtos encontrados"></ul>'
      +   '<div class="busca-inicio">'
      +     '<p class="busca-dica">Busque pelo nome do modelo, pelo código ou por uma característica:'
      +     ' tecnologia, camada, altura, medida, material.</p>'
      +     '<p class="busca-rotulo">Experimente</p>'
      +     '<ul class="busca-sugestoes"></ul>'
      +   '</div>'
      +   '<div class="busca-nada" hidden>'
      +     '<p class="busca-nada-tit">Nenhum produto encontrado para <q></q>.</p>'
      +     '<p>Confira a grafia ou tente um termo mais curto. Se procura um modelo'
      +     ' específico, o representante da sua região ajuda.</p>'
      +     '<p class="busca-nada-links">'
      +       '<a class="link-arrow" href="' + RAIZ + 'index.html#colchoes">Ver todos os produtos</a>'
      +       '<a class="link-arrow" href="' + RAIZ + 'representantes.html">Falar com um representante</a>'
      +     '</p>'
      +   '</div>'
      + '</div>'
      + '</div>';
    document.body.appendChild(dlg);

    campoBusca = dlg.querySelector('.busca-campo');
    lista = dlg.querySelector('.busca-lista');
    status = dlg.querySelector('.busca-status');
    inicio = dlg.querySelector('.busca-inicio');
    nada = dlg.querySelector('.busca-nada');

    campoBusca.addEventListener('input', atualiza);
    campoBusca.addEventListener('keydown', teclas);
    lista.addEventListener('click', envia);
    dlg.querySelector('.busca-fechar').addEventListener('click', fecha);
    /* clique no fundo escuro (fora do painel) fecha */
    dlg.addEventListener('click', function (e) { if (e.target === dlg) fecha(); });
    dlg.addEventListener('close', aoFechar);
    /* Esc com o foco fora do campo (no X, por exemplo) */
    dlg.addEventListener('cancel', function (e) { e.preventDefault(); fecha(); });
    dlg.querySelector('.busca-sugestoes').addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      campoBusca.value = b.textContent;
      atualiza();
      campoBusca.focus();
    });
  }

  function sugestoes() {
    var ul = dlg.querySelector('.busca-sugestoes');
    if (ul.childNodes.length || !SUGESTOES.length) return;
    SUGESTOES.forEach(function (s) {
      var li = document.createElement('li'), b = document.createElement('button');
      b.type = 'button';
      b.className = 'busca-sugestao';
      b.textContent = s;
      li.appendChild(b);
      ul.appendChild(li);
    });
  }

  function abre() {
    if (!dlg) monta();
    if (dlg.open) return;
    origem = document.activeElement;
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
    document.documentElement.classList.add('busca-aberta');
    Array.prototype.forEach.call(botoes, function (b) { b.setAttribute('aria-expanded', 'true'); });
    campoBusca.focus();
    campoBusca.select();
    if (!INDICE) status.textContent = 'Carregando os produtos…';
    carregaIndice(function () { sugestoes(); atualiza(); });
  }

  /* A limpeza roda aqui mesmo, sem esperar o evento 'close': ele chega
     numa tarefa posterior e ja houve navegador em que nao chegou, deixando
     a pagina sem rolagem. O 'close' fica so para fechamentos nativos. */
  function fecha() {
    if (!dlg || !dlg.open) return;
    if (dlg.close) dlg.close(); else dlg.removeAttribute('open');
    aoFechar();
  }

  function aoFechar() {
    envia();
    document.documentElement.classList.remove('busca-aberta');
    Array.prototype.forEach.call(botoes, function (b) { b.setAttribute('aria-expanded', 'false'); });
    /* foco volta para quem abriu; aberto pelo atalho (foco no body) ou no
       Safari (que nao foca botao no clique), volta para a lupa */
    var foco = document.activeElement;
    if (!foco || foco === document.body || dlg.contains(foco)) {
      var alvo = origem && origem !== document.body && document.contains(origem)
        ? origem : botoes[0];
      if (alvo.focus) alvo.focus();
    }
    origem = null;
  }

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt) n.textContent = txt;
    return n;
  }

  function item(r, i, termos) {
    var p = r.e.p;
    var li = el('li', 'busca-item');
    li.id = 'busca-op-' + i;
    li.setAttribute('role', 'option');
    li.setAttribute('aria-selected', 'false');

    var a = el('a', 'busca-link');
    a.href = RAIZ + p.u;
    a.tabIndex = -1;

    var fig = el('span', 'busca-thumb' + (p.i ? '' : ' is-vazia')
                 + (p.g === 'Travesseiros' ? ' is-contain' : ''));
    var img = document.createElement('img');
    img.src = RAIZ + (p.i || 'assets/brand/simbolo-positivo.svg');
    img.alt = '';
    img.width = 96;
    img.height = 72;
    img.loading = 'lazy';
    img.decoding = 'async';
    fig.appendChild(img);

    var txt = el('span', 'busca-txt');
    var cat = el('span', 'busca-cat', p.g + (p.c ? ' · ' + p.c : ''));
    if (p.flag) cat.appendChild(el('span', 'busca-flag', p.flag));
    var nome = el('span', 'busca-nome');
    pinta(nome, p.t, faixas(r.e.titulo, termos).lista);
    txt.appendChild(cat);
    txt.appendChild(nome);
    txt.appendChild(el('span', 'busca-sub', p.d));

    var tr = trecho(r.e, termos);
    if (tr) {
      var t = el('span', 'busca-trecho');
      pinta(t, tr.txt, tr.lista);
      txt.appendChild(t);
    }

    a.appendChild(fig);
    a.appendChild(txt);
    li.appendChild(a);
    li.addEventListener('mousemove', function () { if (ativo !== i) marca(i); });
    return li;
  }

  function atualiza() {
    if (!INDICE) return;
    var q = campoBusca.value;
    var r = q.trim() ? busca(q) : null;
    registra(r ? q : '', r);
    lista.textContent = '';
    ativo = -1;
    campoBusca.removeAttribute('aria-activedescendant');

    inicio.hidden = !!r;
    nada.hidden = !r || r.itens.length > 0;
    campoBusca.setAttribute('aria-expanded', String(!!(r && r.itens.length)));

    if (!r) { anuncia(''); return; }
    if (!r.itens.length) {
      nada.querySelector('q').textContent = q.trim();
      anuncia('Nenhum produto encontrado');
      return;
    }

    var frag = document.createDocumentFragment();
    r.itens.forEach(function (it, i) { frag.appendChild(item(it, i, r.termos)); });
    lista.appendChild(frag);
    lista.parentNode.scrollTop = 0;
    marca(0);

    var n = r.itens.length;
    var msg = n + (n === 1 ? ' produto' : ' produtos');
    if (r.modo === 'algum') msg = 'Nenhum produto tem todos os termos. Os mais próximos: ' + n;
    else if (r.aproximado) msg += ' com termos parecidos';
    anuncia(msg);
  }

  /* o contador espera a pessoa parar de digitar, para o leitor de tela
     nao anunciar uma contagem a cada letra */
  function anuncia(msg) {
    clearTimeout(aviso);
    if (!msg) { status.textContent = ''; return; }
    aviso = setTimeout(function () { status.textContent = msg; }, 250);
  }

  function marca(i) {
    var ops = lista.children;
    if (ops[ativo]) ops[ativo].setAttribute('aria-selected', 'false');
    ativo = i;
    if (ops[i]) {
      ops[i].setAttribute('aria-selected', 'true');
      campoBusca.setAttribute('aria-activedescendant', ops[i].id);
    }
  }

  /* rola so a lista: scrollIntoView tambem rolaria a pagina por tras */
  function visivel(op) {
    var corpo = lista.parentNode, c = corpo.getBoundingClientRect(),
        o = op.getBoundingClientRect();
    if (o.top < c.top) corpo.scrollTop -= c.top - o.top;
    else if (o.bottom > c.bottom) corpo.scrollTop += o.bottom - c.bottom;
  }

  function teclas(e) {
    var ops = lista.children, n = ops.length;
    /* Esc fecha e guarda o texto para a proxima vez (o campo search do
       Chrome apagaria o texto antes; e sem showModal ninguem fecharia) */
    if (e.key === 'Escape') {
      e.preventDefault();
      fecha();
    } else if ((e.key === 'ArrowDown' || e.key === 'ArrowUp') && n) {
      e.preventDefault();
      marca(e.key === 'ArrowDown' ? (ativo + 1) % n : (ativo - 1 + n) % n);
      visivel(ops[ativo]);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      var a = ops[ativo >= 0 ? ativo : 0] && ops[ativo >= 0 ? ativo : 0].querySelector('a');
      if (!a) return;
      envia();
      if (e.ctrlKey || e.metaKey) window.open(a.href, '_blank');
      else location.href = a.href;
    }
  }

  /* ---------- 6. Medicao (GA4) ---------- */
  /* Com o GA na pagina (tools/build_pages.py, GA_ID), cada busca vira um
     evento 'search' com o termo, o numero de resultados e o quanto do termo
     foi achado ('nada' e 'parte dos termos' sao o que o catalogo nao tem).
     Espera a pessoa parar de digitar, para nao registrar letra a letra, e
     sai antes se ela escolhe um produto ou fecha a busca. */
  var pendente = null, espera, ultimo = '';

  function registra(q, r) {
    if (!window.gtag) return;
    clearTimeout(espera);
    q = q.trim().replace(/\s+/g, ' ').toLowerCase();
    pendente = q.length >= 2 && r ? {
      q: q,
      n: r.itens.length,
      achou: !r.itens.length ? 'nada'
        : r.modo === 'algum' ? 'parte dos termos'
        : r.aproximado ? 'termo parecido' : 'todos os termos'
    } : null;
    if (pendente) espera = setTimeout(envia, 1500);
  }

  function envia() {
    clearTimeout(espera);
    if (!pendente || !window.gtag) return;
    var p = pendente;
    pendente = null;
    if (p.q === ultimo) return;   /* reabriu a busca com o mesmo texto */
    ultimo = p.q;
    window.gtag('event', 'search', { search_term: p.q, resultados: p.n, achou: p.achou });
  }

  /* ---------- gatilhos ---------- */
  Array.prototype.forEach.call(botoes, function (b) {
    b.addEventListener('click', abre);
    /* chegou perto da lupa: ja comeca a baixar o indice */
    ['pointerenter', 'focus', 'touchstart'].forEach(function (ev) {
      b.addEventListener(ev, function () { carregaIndice(); }, { passive: true, once: true });
    });
  });

  /* "/" ou Ctrl+K / Cmd+K abrem a busca, fora de campos de texto */
  document.addEventListener('keydown', function (e) {
    var alvo = e.target, digitando = alvo && (alvo.isContentEditable
      || /^(INPUT|TEXTAREA|SELECT)$/.test(alvo.tagName));
    var atalho = (e.key === '/' && !digitando && !e.ctrlKey && !e.metaKey && !e.altKey)
      || ((e.ctrlKey || e.metaKey) && !e.altKey && (e.key === 'k' || e.key === 'K'));
    if (!atalho || (dlg && dlg.open)) return;
    e.preventDefault();
    abre();
  });
})();
