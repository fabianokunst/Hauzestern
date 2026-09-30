# -*- coding: utf-8 -*-
"""
Troca o fundo de estudio de uma foto de produto: cinza <-> branco.

Usado apenas para gerar a variante que NAO EXISTE no guide. A foto original
nunca e sobrescrita e o README marca quais variantes sao emuladas.

POR QUE ESTA VERSAO
  A primeira versao segmentava numa reducao de 820px, ampliava a mascara ~8x e
  ainda dilatava alguns pixels "de seguranca". O resultado era um anel do fundo
  ORIGINAL sem correcao em volta do produto — o halo branco tipico de recorte
  malfeito. Tres mudancas resolvem:

  1. TRABALHA EM 2x A RESOLUCAO DE SAIDA (2800x2100 para uma saida de 1400x1050),
     ja com o mesmo recorte 4:3 do arquivo final. A reducao final de 2x dilui
     qualquer erro de meio pixel que sobre na borda.
  2. MASCARA EM DOIS ESTAGIOS: um flood fill rapido numa reducao de 900px para
     achar o corpo do fundo, e um refinamento na resolucao de trabalho aplicado
     SO numa faixa estreita em volta da silhueta. A borda passa a ser precisa
     nessa resolucao, em vez de ampliada de longe.
  2b. FUNDO ESTIMADO POR CONVOLUCAO NORMALIZADA, nao por polinomio: o sweep tem
     chao claro (~195) e laterais escuras (~158), 37 niveis de amplitude, muito
     acima de qualquer tolerancia util. Um polinomio de 2o grau nao acompanha e
     deixava manchas do fundo antigo nos cantos.

LIMITE CONHECIDO
  A conversao branco->cinza nao fecha quando o produto e branco e liso: na borda
  traseira do colchao nao existe informacao local que o separe do fundo. Hemmen e
  Dorf caem nesse caso e por isso usam a foto real em cinza do catalogo 2026
  (771x689) em vez de emulacao. Ver README.
  3. ERRA PARA DENTRO, NUNCA PARA FORA. A mascara do produto e erodida 1px. Um
     fio da borda do produto recebendo a correcao e invisivel; um anel de fundo
     antigo sem correcao salta aos olhos.

  A recomposicao tambem mudou: de multiplicacao para SOMA ponderada pela
  cobertura de fundo,  saida = I + (1 - alpha) * (alvo - estimado).
  Essa e a conta de descompor e recompor sobre outro fundo: em pixel de fundo
  puro (alpha=0) da exatamente o alvo, em pixel de produto (alpha=1) nao muda
  nada, e no meio da borda da a mistura correta. Sombra de contato mantem o
  mesmo desvio em relacao ao fundo novo.

O gradiente do fundo cinza foi medido nas fotos reais do estudio
(MOND (1).jpg e WACHEN (1).jpg): cantos ~158, topo-centro ~182, base ~195.
Os fundos brancos da marca sao 255 chapado, sem gradiente.
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter

Image.MAX_IMAGE_PIXELS = None
ESCALA_GROSSA = 900      # largura da segmentacao inicial


# ------------------------------------------------------------- morfologia
def _dilata(m, n=1):
    for _ in range(n):
        d = m.copy()
        d[1:, :] |= m[:-1, :]
        d[:-1, :] |= m[1:, :]
        d[:, 1:] |= m[:, :-1]
        d[:, :-1] |= m[:, 1:]
        m = d
    return m


def _erode(m, n=1):
    for _ in range(n):
        e = m.copy()
        e[1:, :] &= m[:-1, :]
        e[:-1, :] &= m[1:, :]
        e[:, 1:] &= m[:, :-1]
        e[:, :-1] &= m[:, 1:]
        m = e
    return m


def _abre(m, n=3):
    return _dilata(_erode(m, n), n)


def _propaga(semente, permitido, limite=4000):
    m = semente & permitido
    for _ in range(limite):
        antes = m.sum()
        m = _dilata(m) & permitido
        if m.sum() == antes:
            break
    return m


def _suave(a, raio):
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return np.asarray(img.filter(ImageFilter.GaussianBlur(raio))).astype(np.float32)


def _gradiente(L):
    g = _suave(L, 1.6)
    gx = np.zeros_like(g); gy = np.zeros_like(g)
    gx[:, 1:-1] = (g[:, 2:] - g[:, :-2]) * .5
    gy[1:-1, :] = (g[2:, :] - g[:-2, :]) * .5
    return np.hypot(gx, gy)


def _box1(a, r, eixo):
    """Media movel de raio r num eixo, por soma cumulativa."""
    n = a.shape[eixo]
    pad = [(0, 0), (0, 0)]
    pad[eixo] = (r, r)
    c = np.cumsum(np.pad(a, pad, mode='edge').astype(np.float64), axis=eixo)
    zc = list(c.shape); zc[eixo] = 1
    c = np.concatenate([np.zeros(zc, np.float64), c], axis=eixo)
    hi = [slice(None)] * 2; hi[eixo] = slice(2 * r + 1, None)
    lo = [slice(None)] * 2; lo[eixo] = slice(0, n)
    return ((c[tuple(hi)] - c[tuple(lo)]) / (2 * r + 1)).astype(np.float32)


def _blur_f(a, raio):
    """Desfoque em ponto flutuante. PIL nao faz gaussiana em modo 'F', entao
    usa-se box blur separavel repetido, que converge para gaussiana."""
    r = max(1, int(round(raio * .6)))
    out = a.astype(np.float32)
    for _ in range(3):
        out = _box1(_box1(out, r, 1), r, 0)
    return out


def _estima_fundo(L, sel):
    """Superficie do fundo por convolucao normalizada sobre os pixels de `sel`.

    Um polinomio de 2o grau nao da conta do sweep do estudio: ele tem o chao
    claro (~195) e as laterais escuras (~158), 37 niveis de amplitude, muito
    acima de qualquer tolerancia util. Com media ponderada de raio grande a
    estimativa acompanha o sweep de verdade e extrapola por baixo do produto.
    Duas escalas: uma larga para preencher a area do produto e uma media para
    seguir o detalhe do sweep onde ha informacao.
    """
    if sel.sum() < 400:
        return np.full_like(L, float(np.median(L)))
    w = sel.astype(np.float32)
    Lm = L * w
    est = None
    for raio in (max(L.shape[1] // 7, 24), max(L.shape[1] // 22, 12)):
        num = _blur_f(Lm, raio)
        den = _blur_f(w, raio)
        camada = num / np.maximum(den, 1e-4)
        conf = np.clip(den * 3.0, 0, 1)          # onde ha pixels de fundo perto
        est = camada if est is None else est * (1 - conf) + camada * conf
    return np.clip(est, 1, 255)


def _ajusta_poli(L, sel):     # nome antigo, mantido para nao quebrar chamadas
    return _estima_fundo(L, sel)


# ------------------------------------------------------------------- alvos
def _campo_cinza(h, w):
    """Gradiente do sweep cinza, modelado nas fotos reais do estudio."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    x = xx / (w - 1)
    y = yy / (h - 1)
    # o clip evita base negativa (sin(pi) da -1e-16 em float) com expoente fracionario
    horiz = 158 + 24 * np.clip(np.sin(np.pi * x), 0, None) ** 1.4
    vert = -6 * np.sin(np.pi * y) + 30 * np.clip((y - 0.72) / 0.28, 0, 1) ** 1.6
    return (horiz + vert).astype(np.float32)


# ---------------------------------------------------------------- recorte
def _recorta(im, w, h):
    """Cover-crop centrado — o mesmo enquadramento do arquivo final."""
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg
    im = im.convert('RGB')
    sw, sh = im.size
    k = max(w / sw, h / sh)
    nw, nh = round(sw * k), round(sh * k)
    im = im.resize((nw, nh), Image.LANCZOS)
    return im.crop(((nw - w) // 2, (nh - h) // 2, (nw - w) // 2 + w, (nh - h) // 2 + h))


# ----------------------------------------------------------------- mascara
def _semente_borda(h, w):
    s = np.zeros((h, w), bool)
    s[0, :] = s[-1, :] = True
    s[:, 0] = s[:, -1] = True
    return s


def _fundo_ligado(L, grad, sat, est, tol, grad_max, sat_max, resgata_claro,
                  limite=4000):
    """Fundo = liso, proximo da superficie estimada e ligado a borda da imagem.

    `resgata_claro` (opcional) tambem aceita como fundo o que for liso e mais
    claro que esse valor. Serve para a sombra de contato sobre fundo branco, que
    e clara e lisa, enquanto o produto naquela foto e escuro ou texturizado.
    Nao da para usar sempre: no Hemmen o proprio colchao e branco e liso em
    partes, e o resgate entraria nele.
    """
    liso = (sat < sat_max) & (grad < grad_max)
    ok = (np.abs(L - est) < tol) & liso
    if resgata_claro is not None:
        ok |= (L > resgata_claro) & liso
    h, w = L.shape
    return _propaga(_semente_borda(h, w), ok, limite)


def _mascara_grossa(rgb, tol, grad_max, sat_max, resgata_claro):
    """Produto na escala reduzida. Duas voltas: estima o fundo, refaz a mascara."""
    L = rgb.mean(axis=2)
    sat = rgb.max(axis=2) - rgb.min(axis=2)
    grad = _gradiente(L)
    h, w = L.shape

    borda = np.concatenate([L[:5].ravel(), L[-5:].ravel(),
                            L[:, :5].ravel(), L[:, -5:].ravel()])
    base = float(np.median(borda))
    sel = _propaga(_semente_borda(h, w),
                   (np.abs(L - base) < 22) & (sat < sat_max) & (grad < 3.0))
    est = _estima_fundo(L, sel)

    fundo = None
    for _ in range(2):
        fundo = _fundo_ligado(L, grad, sat, est, tol, grad_max, sat_max,
                              resgata_claro)
        fundo = _propaga(_semente_borda(h, w), _abre(fundo, 3))
        est = _estima_fundo(L, fundo)
    return ~fundo


def _refina_borda(rgb, prod_grosso, tol, grad_max, sat_max, resgata_claro,
                  banda=22):
    """Redecide so a faixa em volta da silhueta, na resolucao de trabalho.

    A topologia vem da escala reduzida, que e robusta; a posicao exata da borda
    vem daqui, que e precisa. Fora da faixa, mantem o que a escala reduzida
    decidiu — e isso que impede a mascara de mudar de ideia no meio do produto.
    """
    L = rgb.mean(axis=2)
    sat = rgb.max(axis=2) - rgb.min(axis=2)
    grad = _gradiente(L)
    est = _estima_fundo(L, ~prod_grosso)

    liso = (sat < sat_max) & (grad < grad_max)
    local_fundo = (np.abs(L - est) < tol) & liso
    if resgata_claro is not None:
        local_fundo |= (L > resgata_claro) & liso

    faixa = _dilata(prod_grosso, banda) & _dilata(~prod_grosso, banda)
    prod = np.where(faixa, ~local_fundo, prod_grosso)
    prod = _dilata(_erode(prod, 1), 1)          # tira pixels soltos na faixa
    return prod, _estima_fundo(L, ~prod), L


def _refaz_chao(rgb, final, L, alvo, faixa, sat_lo=6, sat_hi=16):
    """Recompoe o chao abaixo de `faixa` por GANHO, nao por soma.

    A mascara normal trata a sombra de contato como produto: ela e escura
    demais para ficar a `tol` do fundo e a transicao para o chao tem gradiente
    alto demais para contar como lisa. O resultado e um degrau onde a penumbra
    encontra o fundo novo. No chao, abaixo do produto, o que existe e so luz
    sobre uma superficie neutra; trocar o tom dessa superficie e multiplicar
    pela razao alvo/estimado. Assim a sombra inteira acompanha o fundo novo, do
    nucleo escuro a penumbra, sem mascara.

    So pixels neutros entram (peso cai de 1 a 0 entre `sat_lo` e `sat_hi`):
    os pes de madeira sao saturados e ficam com o resultado normal. A faixa so
    pode comecar abaixo de qualquer parte clara e neutra do produto — o tampo
    branco e o tecido xadrez tambem sao neutros. Tecido escuro pode ficar
    dentro: o ganho (~1,2) num pixel de L 20 da L 24, imperceptivel.

    `faixa` = (inicio, fim) em fracao da altura: o peso sobe de 0 a 1 nesse
    intervalo, para a passagem do resultado normal para o ganho nao deixar
    emenda na penumbra. Um numero so = comeco seco.
    Devolve a imagem e a mascara da faixa tocada.
    """
    h, w = L.shape
    sat = rgb.max(axis=2) - rgb.min(axis=2)
    ini, fim = faixa if isinstance(faixa, (tuple, list)) else (faixa, faixa)
    y = np.arange(h, dtype=np.float32)[:, None] / h
    rampa = np.clip((y - ini) / max(fim - ini, 1e-6), 0, 1)
    zona = np.broadcast_to(y >= ini, (h, w))
    peso = np.clip((sat_hi - sat) / float(sat_hi - sat_lo), 0, 1) * rampa
    # chao limpo = neutro e no tom das margens da mesma linha; a estimativa
    # extrapola por baixo da sombra a partir dele
    margens = np.r_[0:int(w * .1), int(w * .9):w]
    ref = np.median(L[:, margens], axis=1)[:, None]
    limpo = zona & (sat < sat_lo) & (np.abs(L - ref) < 6)
    est = _estima_fundo(L, limpo)
    mult = np.clip(rgb * (alvo / np.maximum(est, 1))[:, :, None], 0, 255)
    p = peso[:, :, None]
    return final * (1 - p) + mult * p, peso > 0


# ---------------------------------------------------------------- conversao
def converte(entrada, saida, para='cinza', largura=2800, altura=2100,
             tol=11, grad_max=2.2, sat_max=34, resgata_claro=None,
             encolhe=1, feather=1.2, qualidade=93, tolera_produto=2.0,
             chao=None):
    """Grava em `saida` a foto no fundo `para`, em `largura`x`altura` (4:3).

    `chao` (opcional, fracao da altura ou par (inicio, fim) de rampa): dali
    para baixo, recompoe o chao e a sombra de contato por ganho — ver
    _refaz_chao. Usar so quando a sombra sai com degrau.
    """
    trabalho = _recorta(Image.open(entrada), largura, altura)
    rgb = np.asarray(trabalho).astype(np.float32)

    peq = trabalho.resize((ESCALA_GROSSA,
                           max(1, round(ESCALA_GROSSA * altura / largura))),
                          Image.LANCZOS)
    prod_p = _mascara_grossa(np.asarray(peq).astype(np.float32),
                             tol, grad_max, sat_max, resgata_claro)
    grosso = np.asarray(
        Image.fromarray((prod_p * 255).astype(np.uint8))
             .resize((largura, altura), Image.BILINEAR)) > 127

    produto, est, L = _refina_borda(rgb, grosso, tol, grad_max, sat_max,
                                    resgata_claro)
    if encolhe:
        produto = _erode(produto, encolhe)

    alpha = _suave(produto.astype(np.float32) * 255, feather) / 255.0
    alvo = _campo_cinza(altura, largura) if para == 'cinza'         else np.full((altura, largura), 254.0, np.float32)

    delta = ((alvo - est) * (1.0 - alpha))[:, :, None]
    final = np.clip(rgb + delta, 0, 255)

    nucleo = alpha > .995
    if chao is not None:
        final, tocado = _refaz_chao(rgb, final, L, alvo, chao)
        nucleo &= ~tocado       # a sombra deixou de ser "produto"
    desvio = 0.0
    if nucleo.sum() > 500:
        desvio = abs(float(final.mean(axis=2)[nucleo].mean()) - float(L[nucleo].mean()))

    rel = {
        'entrada': os.path.basename(entrada),
        'fundo_antes': round(float(np.median(L[:10].ravel()))),
        'fundo_depois': round(float(np.median(final.mean(axis=2)[:10].ravel()))),
        'produto_pct': round(100 * float((alpha > .5).mean()), 1),
        'desvio_produto': round(desvio, 2),
    }
    if desvio > tolera_produto:
        raise ValueError(f'conversao reprovada: o produto mudou {desvio:.1f} '
                         f'niveis (limite {tolera_produto}). {rel}')

    os.makedirs(os.path.dirname(saida) or '.', exist_ok=True)
    Image.fromarray(final.astype(np.uint8)).save(
        saida, 'JPEG', quality=qualidade, optimize=True, progressive=True)
    return rel


if __name__ == '__main__':
    print(converte(sys.argv[1], sys.argv[2],
                   sys.argv[3] if len(sys.argv) > 3 else 'cinza'))
