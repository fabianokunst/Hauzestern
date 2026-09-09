/* =========================================================
   HAUZESTERN — comportamentos básicos da home
   1. Header sólido ao rolar
   2. Menu mobile
   3. Submenu de produtos
   4. Carrossel de fotos
   5. Reveal on scroll
   6. Ano no rodapé
   7. Filtro dos representantes
   ========================================================= */
(function () {
  'use strict';

  /* html.js: o CSS so esconde os .reveal quando ha script.
     Roda antes de tudo para nao piscar conteudo. */
  document.documentElement.classList.add('js');

  /* ---------- 1. Header sólido ao rolar ---------- */
  var header = document.getElementById('header');
  var solidAfter = 40;

  function onScroll() {
    header.classList.toggle('is-solid', window.scrollY > solidAfter);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- 2. Menu mobile ---------- */
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');

  function setMenu(open) {
    /* Recolhe Produtos ao ABRIR, nunca ao fechar. Fechando, o submenu
       recebia display:none no meio do clique num link dele — e apagar um
       ancestral do link durante o clique cancela a navegacao no iOS. */
    if (open) setSub(false);
    nav.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    document.body.classList.toggle('nav-open', open);
  }

  burger.addEventListener('click', function () {
    setMenu(nav.classList.contains('is-open') === false);
  });

  // fecha ao clicar em um link ou pressionar ESC
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) setMenu(false);
  });

  /* ---------- 3. Submenu de produtos ---------- */
  var subBtn = document.querySelector('.nav-sub-toggle');

  function setSub(open) {
    if (!subBtn) return;
    subBtn.setAttribute('aria-expanded', String(open));
  }

  if (subBtn) {
    subBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      setSub(subBtn.getAttribute('aria-expanded') !== 'true');
    });
    // clique fora fecha
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.has-sub')) setSub(false);
    });
    // ESC fecha e devolve o foco ao botao
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && subBtn.getAttribute('aria-expanded') === 'true') {
        setSub(false);
        subBtn.focus();
      }
    });
    /* Nao ha handler de clique no #sub-produtos: recolher o submenu no
       clique do proprio link e o que quebrava a navegacao. Quem fecha o
       painel e o handler do .nav, e isso e so um transform. */
  }

  /* ---------- 4. Carrossel de fotos ---------- */
  Array.prototype.forEach.call(
    document.querySelectorAll('[data-carrossel]'),
    function (car) {
      var trilha = car.querySelector('.carrossel-trilha');
      var slides = car.querySelectorAll('.carrossel-slide');
      var pontos = car.querySelectorAll('.carrossel-pontos button');
      var botoes = car.querySelectorAll('.carrossel-btn');
      if (!trilha || slides.length < 2) return;

      Array.prototype.forEach.call(botoes, function (b) { b.hidden = false; });

      var idx = 0;
      var semAnimacao = window.matchMedia
        && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      function atual() {
        return Math.round(trilha.scrollLeft / slides[0].offsetWidth);
      }
      function vaiPara(i) {
        idx = Math.max(0, Math.min(slides.length - 1, i));
        var x = idx * slides[0].offsetWidth;
        if (trilha.scrollTo) {
          trilha.scrollTo({ left: x, behavior: semAnimacao ? 'auto' : 'smooth' });
        } else {
          trilha.scrollLeft = x;
        }
        pinta();   // o scroll programatico nao dispara 'scroll' em todo lugar
      }
      function pinta() {
        var i = idx;
        Array.prototype.forEach.call(pontos, function (p, k) {
          if (k === i) { p.setAttribute('aria-current', 'true'); }
          else { p.removeAttribute('aria-current'); }
        });
        var prev = car.querySelector('.carrossel-prev');
        var next = car.querySelector('.carrossel-next');
        if (prev) prev.disabled = i <= 0;
        if (next) next.disabled = i >= slides.length - 1;
      }

      Array.prototype.forEach.call(botoes, function (b) {
        b.addEventListener('click', function () {
          vaiPara(atual() + Number(b.getAttribute('data-passo')));
        });
      });
      Array.prototype.forEach.call(pontos, function (p) {
        p.addEventListener('click', function () {
          vaiPara(Number(p.getAttribute('data-ir')));
        });
      });

      var esperando;
      trilha.addEventListener('scroll', function () {
        clearTimeout(esperando);
        esperando = setTimeout(function () { idx = atual(); pinta(); }, 90);
      }, { passive: true });
      window.addEventListener('resize', pinta, { passive: true });
      pinta();
    }
  );

  /* ---------- 5. Reveal on scroll ---------- */
  var alvos = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    alvos.forEach(function (el) { io.observe(el); });
  } else {
    alvos.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- 6. Ano no rodapé ---------- */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- 7. Filtro dos representantes ---------- */
  var lista = document.getElementById('rep-lista');

  if (lista) (function () {
    var cards = lista.querySelectorAll('[data-rep]');
    var estados = lista.querySelectorAll('[data-estado]');
    var regioes = lista.querySelectorAll('[data-regiao-bloco]');
    var busca = document.getElementById('rep-busca');
    var selUf = document.getElementById('rep-uf');
    var chips = document.querySelectorAll('[data-filtro-regiao]');
    var vazio = document.getElementById('rep-vazio');
    var contagem = document.getElementById('rep-contagem');
    var regiao = '';

    /* mesma normalizacao do data-busca gerado em Python: minusculas sem acento */
    function limpa(t) {
      t = String(t || '').toLowerCase();
      return t.normalize ? t.normalize('NFD').replace(/[\u0300-\u036f]/g, '') : t;
    }

    function aplica() {
      var termos = limpa(busca.value).split(/\s+/).filter(Boolean);
      var uf = selUf.value;
      var visiveis = 0;

      Array.prototype.forEach.call(cards, function (c) {
        var alvo = c.getAttribute('data-busca');
        var ok = (!uf || c.getAttribute('data-uf') === uf)
          && (!regiao || c.getAttribute('data-regiao') === regiao)
          && termos.every(function (t) { return alvo.indexOf(t) !== -1; });
        c.hidden = !ok;
        if (ok) visiveis++;
      });

      /* titulo de estado e de regiao somem quando nao sobra nenhum card */
      Array.prototype.forEach.call(estados, esconde);
      Array.prototype.forEach.call(regioes, esconde);

      vazio.hidden = visiveis > 0;
      contagem.textContent = visiveis === 0
        ? 'Nenhuma equipe encontrada'
        : visiveis + (visiveis === 1 ? ' equipe' : ' equipes') + ' · '
          + ufsVisiveis() + (ufsVisiveis() === 1 ? ' estado' : ' estados');
    }

    function esconde(bloco) {
      bloco.hidden = !bloco.querySelector('[data-rep]:not([hidden])');
    }

    function ufsVisiveis() {
      var vistos = {}, n = 0;
      Array.prototype.forEach.call(cards, function (c) {
        var uf = c.getAttribute('data-uf');
        if (!c.hidden && !vistos[uf]) { vistos[uf] = 1; n++; }
      });
      return n;
    }

    busca.addEventListener('input', aplica);
    selUf.addEventListener('change', aplica);

    Array.prototype.forEach.call(chips, function (chip) {
      chip.addEventListener('click', function () {
        regiao = chip.getAttribute('data-filtro-regiao');
        Array.prototype.forEach.call(chips, function (o) {
          o.classList.toggle('is-on', o === chip);
        });
        selUf.value = '';        // regiao e UF sao o mesmo recorte
        aplica();
      });
    });

    var limpar = vazio.querySelector('[data-limpar]');
    if (limpar) limpar.addEventListener('click', function () {
      busca.value = '';
      selUf.value = '';
      chips[0].click();
    });

    /* #uf-sp na URL ja abre a pagina filtrada naquele estado */
    var ancora = (location.hash || '').match(/^#uf-([a-z]{2})$/);
    if (ancora) selUf.value = ancora[1].toUpperCase();

    aplica();
  })();
})();
