# -*- coding: utf-8 -*-
"""
brand.py — Motor de marca del Longevity Academic Institute (LAI)
Dra. Carolina Rodriguez Morales

Fuente unica de verdad para paleta, tipografias, logos, gradientes,
patron de marca, tratamiento de imagen y componentes visuales.

NO usar la paleta ni las tipografias de Longevity Clinical Institute (LCI).
LAI es una marca distinta: Lato + Helvetica/Arimo, navy + azul + cian, oro solo en el escudo.
Fuente de verdad: Manual de Marca LAI v2 (logotipo v2, llama en lugar de asterisco).

Uso:
    import sys; sys.path.insert(0, '<ruta>/lai-design-system/assets')
    from brand import *
    im = lienzo('story'); d = draw(im)
    fondo_profundo(im)
    poner_logo(im, 'horizontal-blanco', x=..., y=..., ancho=...)
"""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops

RAIZ    = os.path.dirname(os.path.abspath(__file__))
DIR_F   = os.path.join(RAIZ, 'fonts')
DIR_L   = os.path.join(RAIZ, 'logos')
DIR_R   = os.path.join(RAIZ, 'retratos')
DIR_I   = os.path.join(RAIZ, 'iconos')
DIR_E   = os.path.join(RAIZ, 'elementos')
DIR_A   = os.path.join(RAIZ, 'avales')
DIR_FO  = os.path.join(RAIZ, 'fondos')

# ─────────────────────────────────────────────────────────────────────
# PALETA OFICIAL LAI  (muestreada de las piezas maestras de marca)
# ─────────────────────────────────────────────────────────────────────
P = {
    # ── 21 tokens oficiales (Manual de Marca LAI v2). Fuera de esta lista no hay color LAI.
    'navy':          '#1B1464',   # H1, bandas, wordmark
    'indigo_hondo':  '#09052C',   # fondos profundos
    'azul':          '#3640D7',   # secciones, resplandor sobre indigo hondo, iconos
    'azul_electrico':'#4E57FF',   # H2 sobre claro, CTA, filete del recuadro biselado
    'cian':          '#00F6E3',   # acento: filete de cifras, subrayado de termino tecnico
    'periwinkle':    '#8D89F7',   # H3
    'lila':          '#D2D2FC',   # captions
    'periwinkle_cl': '#9D9DFF',
    'teal':          '#4AF1D2',   # H2 sobre oscuro
    'menta':         '#B7FFF8',   # enfasis sobre oscuro
    'gris_fondo':    '#F6F6F6',
    'gris_linea':    '#DBDCE5',
    'gris_texto':    '#4D4D4D',   # cuerpo sobre claro
    'rojo':          '#FF3131',   # SOLO alerta de seguridad del paciente
    'blanco':        '#FFFFFF',
    # oro: 6 paradas, solo escudo / filetes de certificado / sellos de aval, nunca plano
    'oro_claro':     '#F6EABF',
    'oro_medio':     '#D1BA80',
    'oro':           '#896B38',
    'oro_bronce':    '#BB9E66',
    'oro_sombra':    '#8A6C39',
}
# ── Alias heredados de v1: se conservan para no romper piezas existentes,
#    pero apuntan a tokens oficiales. NO usarlos en codigo nuevo.
ALIAS_V1 = {
    'indigo': 'navy', 'azul_vivo': 'azul_electrico', 'azul_cielo': 'azul_electrico',
    'lila_pal': 'lila', 'cian_hondo': 'azul', 'crema': 'gris_fondo',
    'gris_medio': 'gris_texto', 'negro': 'indigo_hondo',
}
for _k, _v in ALIAS_V1.items():
    P[_k] = P[_v]

# Gradiente metalico del escudo: seis paradas. Dos paradas = bronce plano = prohibido.
GRAD_ORO = [(0.00, '#F6EABF'), (0.18, '#D1BA80'), (0.42, '#896B38'),
            (0.68, '#BB9E66'), (0.86, '#D1BA80'), (1.00, '#8A6C39')]
# Lineales de apoyo (todas las paradas salen de la paleta)
GRAD_HONDO = [(0.00, '#1B1464'), (1.00, '#09052C')]
GRAD_BANDA = [(0.00, '#1B1464'), (1.00, '#09052C')]

# Escalas tipograficas oficiales (H1, H2, H3, cuerpo). Max. 3 niveles de encabezado por pieza.
ESCALA_DOC_PT  = {'h1': 26, 'h2': 18, 'h3': 13, 'cuerpo': 10.5}   # cuerpo nunca < 9 pt
ESCALA_INFO_PX = {'h1': 70, 'h2': 44, 'h3': 32, 'cuerpo': 27}     # cuerpo nunca < 24 px
# Jerarquia de color por fondo
JERARQUIA = {
    'claro':  {'h1': 'navy',   'h2': 'azul_electrico', 'h3': 'periwinkle', 'cuerpo': 'gris_texto',
               'enfasis': 'navy',   'subrayado': 'cian', 'enlace': 'azul'},
    'oscuro': {'h1': 'blanco', 'h2': 'teal',           'h3': 'periwinkle', 'cuerpo': 'blanco',
               'enfasis': 'menta',  'subrayado': 'cian', 'enlace': 'menta'},
}

LIENZOS = {
    'story':      (1080, 1920),   # Instagram / WhatsApp story
    'post':       (1080, 1080),
    'carrusel':   (1080, 1350),
    'infografia': (1125, 2000),   # infografia de modulo (formato maestro LAI)
    'carta':      (2550, 3300),   # 8.5x11 @300dpi
    'carta_h':    (3300, 2550),
    'a4':         (2480, 3508),
    'certificado':(3508, 2480),   # A4 horizontal @300dpi
    'escarapela': (1181, 1772),   # 10x15cm @300dpi
    'slide':      (1920, 1080),
    'banner':     (1600,  600),
    'firma':      (1200,  400),
}

# ─────────────────────────────────────────────────────────────────────
# TIPOGRAFIA
#   Lato        -> titulares, cifras, wordmark de apoyo, elegancia editorial
#   Arimo       -> sustituto libre metricamente compatible con Helvetica,
#                  para cuerpo tecnico y titulos de seccion en infografias
# ─────────────────────────────────────────────────────────────────────
_MAPA_F = {
    ('lato','thin'):   'lato-latin-100-normal.ttf',
    ('lato','light'):  'lato-latin-300-normal.ttf',
    ('lato','light_i'):'lato-latin-300-italic.ttf',
    ('lato','regular'):'lato-latin-400-normal.ttf',
    ('lato','italic'): 'lato-latin-400-italic.ttf',
    ('lato','bold'):   'lato-latin-700-normal.ttf',
    ('lato','bold_i'): 'lato-latin-700-italic.ttf',
    ('lato','black'):  'lato-latin-900-normal.ttf',
    ('helv','regular'):'arimo-latin-400-normal.ttf',
    ('helv','italic'): 'arimo-latin-400-italic.ttf',
    ('helv','medium'): 'arimo-latin-500-normal.ttf',
    ('helv','semibold'):'arimo-latin-600-normal.ttf',
    ('helv','bold'):   'arimo-latin-700-normal.ttf',
    ('helv','bold_i'): 'arimo-latin-700-italic.ttf',
}
_cache_f = {}

def F(familia, peso, tam):
    """Carga una fuente de marca. familia: 'lato'|'helv'. peso: ver _MAPA_F."""
    k = (familia, peso, tam)
    if k not in _cache_f:
        arch = _MAPA_F.get((familia, peso))
        if arch is None:
            raise ValueError('Combinacion no valida: %s %s. Validas: %s'
                             % (familia, peso, sorted(_MAPA_F)))
        _cache_f[k] = ImageFont.truetype(os.path.join(DIR_F, arch), tam)
    return _cache_f[k]

# ─────────────────────────────────────────────────────────────────────
# UTILIDADES DE COLOR
# ─────────────────────────────────────────────────────────────────────
def rgb(c, alfa=None):
    """'#RRGGBB' o nombre de la paleta -> tupla RGB(A)."""
    if isinstance(c, (tuple, list)):
        t = tuple(c)
    else:
        h = P.get(c, c).lstrip('#')
        t = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return t + (alfa,) if alfa is not None else t

def mezcla(a, b, t):
    a, b = rgb(a), rgb(b)
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

# ─────────────────────────────────────────────────────────────────────
# LIENZOS Y GRADIENTES
# ─────────────────────────────────────────────────────────────────────
def lienzo(formato, color='blanco'):
    tam = LIENZOS[formato] if isinstance(formato, str) else tuple(formato)
    return Image.new('RGB', tam, rgb(color))

def draw(im):
    return ImageDraw.Draw(im, 'RGBA')

def gradiente(tam, paradas, angulo=90):
    """Gradiente lineal. paradas=[(pos0..1, color)], angulo en grados (90=vertical)."""
    w, h = tam
    diag = int(math.hypot(w, h)) + 2
    tira = Image.new('RGB', (diag, 1))
    px = tira.load()
    ps = sorted(paradas)
    for x in range(diag):
        t = x / (diag - 1)
        for i in range(len(ps) - 1):
            p0, c0 = ps[i]; p1, c1 = ps[i + 1]
            if p0 <= t <= p1:
                u = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                px[x, 0] = mezcla(c0, c1, u); break
        else:
            px[x, 0] = rgb(ps[-1][1])
    g = tira.resize((diag, diag), Image.NEAREST).rotate(-angulo, expand=True,
                                                        resample=Image.BICUBIC)
    return g.crop(((g.width - w) // 2, (g.height - h) // 2,
                   (g.width - w) // 2 + w, (g.height - h) // 2 + h))

def gradiente_oro(tam, angulo=0):
    return gradiente(tam, GRAD_ORO, angulo)

def fondo_profundo(im, angulo=None, ruido=True, patron=True, estilo='malla_profunda'):
    """Fondo oscuro de portadas, stories y contraportadas (malla profunda por defecto)."""
    im.paste(degradado(im.size, estilo), (0, 0))
    if patron:
        patron_lai(im, color='blanco', opacidad=16)
    if ruido:
        grano(im, 5)
    return im

def fondo_banda(im, caja, angulo=0):
    """Banda indigo (encabezado/pie de infografias y documentos)."""
    x0, y0, x1, y1 = caja
    im.paste(gradiente((x1 - x0, y1 - y0), GRAD_BANDA, angulo), (x0, y0))
    return im

def grano(im, fuerza=6):
    import random
    r = random.Random(7)
    ruido = Image.new('L', (im.width // 3 or 1, im.height // 3 or 1))
    ruido.putdata([r.randint(128 - fuerza, 128 + fuerza)
                   for _ in range(ruido.width * ruido.height)])
    ruido = ruido.resize(im.size, Image.BILINEAR)
    im.paste(ImageChops.overlay(im, Image.merge('RGB', (ruido,) * 3)), (0, 0))
    return im

# ─────────────────────────────────────────────────────────────────────
# DEGRADADOS OFICIALES (Manual v2, seccion 02)
#   Todas las paradas salen de la paleta; los halos van a transparente,
#   nunca a blanco. Sobre los claros el texto pasa a navy.
#   Mallas -> portadas. Sobrias -> certificados, documentos, cubiertas de modulo.
#   2 colores -> bandas y botones. 3 colores -> piezas de redes.
# ─────────────────────────────────────────────────────────────────────
#  base: (angulo, paradas) ; halos: (cx, cy, radio, color, intensidad)  en fracciones del lienzo
DEGRADADOS = {
    # Las dos aprobadas (favoritas)
    'malla_profunda': ((90, [(0, 'navy'), (0.55, 'indigo_hondo'), (1, 'indigo_hondo')]),
                       [(0.08, 0.02, 0.55, 'azul_electrico', 0.95), (0.95, 0.12, 0.40, 'periwinkle', 0.75),
                        (0.30, 0.92, 0.70, 'azul', 0.60), (0.72, 1.06, 0.62, 'cian', 0.92)]),
    'malla_clara':    ((90, [(0, 'gris_fondo'), (1, 'gris_fondo')]),
                       [(0.0, 0.0, 0.75, 'lila', 0.95), (1.0, 0.0, 0.70, 'menta', 0.95),
                        (0.05, 1.0, 0.55, 'periwinkle_cl', 0.85)]),
    # Sobrias / academicas
    'navy_profundo':  ((90, [(0, 'navy'), (1, 'indigo_hondo')]), []),
    'boveda':         ((90, [(0, 'navy'), (1, 'indigo_hondo')]),
                       [(0.25, -0.05, 0.60, 'azul', 0.55)]),
    'luz_lateral':    ((90, [(0, 'indigo_hondo'), (1, 'navy')]),
                       [(0.95, 0.10, 0.55, 'azul', 0.65)]),
    'gris_academia':  ((90, [(0, 'navy'), (1, 'periwinkle')]), []),   # se sirve al 70 % sobre navy
    'papel':          ((90, [(0, 'blanco'), (0.65, 'gris_fondo'), (1, 'lila')]), []),
    'editorial_claro':((90, [(0, 'gris_fondo'), (1, 'gris_fondo')]),
                       [(0.95, 0.05, 0.75, 'lila', 0.9), (0.08, 0.0, 0.35, 'blanco', 0.9)]),
    # Dos y tres colores (redes)
    'navy_azul':            ((70, [(0, 'navy'), (1, 'azul')]), []),
    'indigo_azul':          ((70, [(0, 'indigo_hondo'), (1, 'azul')]), []),
    'electrico_cian':       ((55, [(0, 'azul_electrico'), (1, 'cian')]), []),
    'lila_menta':           ((70, [(0, 'lila'), (1, 'menta')]), []),
    'azul_electrico_peri':  ((70, [(0, 'azul'), (0.5, 'azul_electrico'), (1, 'periwinkle')]), []),
    'navy_azul_cian':       ((70, [(0, 'navy'), (0.55, 'azul'), (1, 'cian')]), []),
}

def degradado(tam, nombre):
    """Devuelve una imagen RGB con el degradado oficial `nombre` (ver DEGRADADOS)."""
    import numpy as np
    (ang, paradas), halos = DEGRADADOS[nombre]
    base = gradiente(tam, [(p, rgb(c)) for p, c in paradas], ang)
    if nombre == 'gris_academia':
        base = Image.blend(Image.new('RGB', tam, rgb('navy')), base, 0.7)
    if not halos:
        return base
    w, h = tam
    arr = np.asarray(base, dtype=np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    esc = (w * h) ** 0.5
    for cx, cy, r, col, k in halos:
        d = np.hypot(xx - cx * w, yy - cy * h) / (r * esc)
        t = np.clip(1 - d, 0, 1)
        a = t * t * (3 - 2 * t) * k                 # halo suave a transparente
        arr = arr * (1 - a[..., None]) + np.array(rgb(col), np.float32) * a[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype('uint8'), 'RGB')

# ─────────────────────────────────────────────────────────────────────
# PATRON DE MARCA
#   La LLAMA sustituye al asterisco (que salio de la marca). Patron de fondo:
#   llama de contorno a gran escala, 12-22 % de opacidad.
# ─────────────────────────────────────────────────────────────────────
def elemento(nombre, color='navy', ancho=None, alto=None):
    """Elementos de marca: llama-maciza, llama-contorno, escudo-silueta, escudo-linea.
    color: 'navy' | 'blanco' (o cualquier token: se recolorea el trazo plano)."""
    base = 'navy' if color not in ('navy', 'blanco') else color
    im = Image.open(os.path.join(DIR_E, '%s-%s.png' % (nombre, base))).convert('RGBA')
    im = im.crop(im.getbbox())
    if color not in ('navy', 'blanco'):
        plano = Image.new('RGBA', im.size, rgb(color) + (255,)); plano.putalpha(im.getchannel('A')); im = plano
    if ancho or alto:
        ancho = ancho or round(im.width * alto / im.height)
        alto = alto or round(im.height * ancho / im.width)
        im = im.resize((ancho, alto), Image.LANCZOS)
    return im

def patron_lai(im, color='blanco', opacidad=16, escala=1.0, semilla=3):
    """Llama de contorno a gran escala como marca de agua. opacidad en % (12-22 recomendado;
    valores > 30 se interpretan en escala 0-255 por compatibilidad v1)."""
    pct = opacidad if opacidad <= 30 else opacidad / 2.55
    pct = max(12, min(22, pct))
    alto = int(max(im.size) * 0.95 * escala)
    ll = elemento('llama-contorno', 'blanco' if color == 'blanco' else 'navy', alto=alto)
    a = ll.getchannel('A').point(lambda v: int(v * pct / 100))
    ll.putalpha(a)
    capa = Image.new('RGBA', im.size, (0, 0, 0, 0))
    x = int(im.width * (0.62 if semilla % 2 else 0.05)) - ll.width // 4
    y = int(im.height * 0.5) - ll.height // 2
    capa.alpha_composite(ll, (x, y))
    im.paste(Image.alpha_composite(im.convert('RGBA'), capa).convert('RGB'), (0, 0))
    return im

def asterisco(*a, **k):
    raise RuntimeError('El asterisco salio de la marca LAI (Manual v2). Usa elemento("llama-maciza").')

# ─────────────────────────────────────────────────────────────────────
# ICONOS (27 de linea, un solo color plano: azul, navy o blanco;
#   nunca oro, relleno ni degradado. Minimo 24 px pantalla / 6 mm impreso)
# ─────────────────────────────────────────────────────────────────────
ICONOS = sorted(n[:-4] for n in os.listdir(os.path.join(DIR_I, 'svg'))) if os.path.isdir(os.path.join(DIR_I, 'svg')) else []

def icono(nombre, tam, color='azul'):
    """Icono de marca a `tam` px, recoloreado a un solo color plano.
    fgu-escudo y fgu-wordmark (aval Florida Global University) van SIEMPRE en su color original."""
    if color not in ('azul', 'navy', 'blanco') and not nombre.startswith('fgu'):
        raise ValueError('Iconos LAI solo en azul, navy o blanco.')
    tam = max(24, int(tam))
    src = Image.open(os.path.join(DIR_I, 'azul', nombre + '.png')).convert('RGBA')
    if not nombre.startswith('fgu'):
        plano = Image.new('RGBA', src.size, rgb(color) + (255,)); plano.putalpha(src.getchannel('A')); src = plano
    return src.resize((tam, tam), Image.LANCZOS)

def poner_icono(im, nombre, cx, cy, tam, color='azul'):
    ic = icono(nombre, tam, color)
    im.paste(ic, (int(cx - ic.width / 2), int(cy - ic.height / 2)), ic)
    return im

# ─────────────────────────────────────────────────────────────────────
# LOGOS
# ─────────────────────────────────────────────────────────────────────
LOGOS = {
    'horizontal-navy':   'logo-horizontal-navy.png',    # sobre fondo claro
    'horizontal-blanco': 'logo-horizontal-blanco.png',  # sobre fondo oscuro
    'vertical-navy':     'logo-vertical-navy.png',
    'vertical-blanco':   'logo-vertical-blanco.png',
    'escudo':            'escudo.png',                  # escudo v3: punta inferior, llama arriba-derecha
    'wordmark-navy':     'wordmark-navy.png',           # wordmark sin escudo (claro)
    'wordmark-blanco':   'wordmark-blanco.png',         # wordmark sin escudo (oscuro)
    'firma':             'firma-carolina.png',          # firma Dra. Carolina
    'firma-blanco':      'firma-carolina-blanco.png',   # firma sobre fondo oscuro (certificado Boveda)
}

def diamante(im, cx, cy, r, color='cian', opacidad=255):
    """Marca de vineta LAI: estrella de cuatro puntas concava (sparkle)."""
    k = r * 0.30
    pts = [(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
           (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)]
    ImageDraw.Draw(im, 'RGBA').polygon(pts, fill=rgb(color, opacidad))
    return im


def logo(nombre, ancho=None, alto=None):
    im = Image.open(os.path.join(DIR_L, LOGOS[nombre])).convert('RGBA')
    if ancho:
        alto = alto or round(im.height * ancho / im.width)
    elif alto:
        ancho = round(im.width * alto / im.height)
    else:
        return im
    return im.resize((ancho, alto), Image.LANCZOS)

def poner_logo(im, nombre, x, y, ancho=None, alto=None, anclaje='lt'):
    """anclaje: combinacion de l/c/r + t/m/b, ej 'rt' = esquina superior derecha."""
    lg = logo(nombre, ancho, alto)
    px = x - (lg.width // 2 if anclaje[0] == 'c' else lg.width if anclaje[0] == 'r' else 0)
    py = y - (lg.height // 2 if anclaje[1] == 'm' else lg.height if anclaje[1] == 'b' else 0)
    im.paste(lg, (int(px), int(py)), lg)
    _reg(im, 'logo', (px, py, px + lg.width, py + lg.height), nombre=nombre)
    return (int(px), int(py), int(px) + lg.width, int(py) + lg.height)

def retrato(nombre):
    return Image.open(os.path.join(DIR_R, nombre)).convert('RGB')

RETRATOS = {
    'grid':    'carolina-grid.jpg',          # collage de tres fotos (brochure)
    'sentada': 'carolina-sentada.jpg',       # traje blanco, sentada, interior calido
    'bata':    'carolina-bata.jpg',          # bata blanca, brazos cruzados, fondo madera
    'recorte': 'carolina-bata-recorte.png',  # misma foto, recortada con fondo transparente
}

def retrato_recorte(nombre='recorte', mono=True):
    """Retrato con alfa (fondo transparente). mono=True -> blanco y negro (portadas de docente)."""
    im = Image.open(os.path.join(DIR_R, RETRATOS.get(nombre, nombre))).convert('RGBA')
    if mono:
        a = im.getchannel('A')
        g = ImageOps.autocontrast(im.convert('L'), cutoff=1)
        im = Image.merge('RGBA', (g, g, g, a))
    return im

# Avales y credenciales de la fundadora. Van SIEMPRE en su color original (no se recolorean),
# salvo las versiones blancas provistas para fondo oscuro.
AVALES = {
    'kharrazian-color':  'kharrazian-institute-color.png',   # sobre claro
    'kharrazian-blanco': 'kharrazian-institute-blanco.png',  # sobre oscuro
    'kharrazian-laurel': 'kharrazian-escudo-laurel.png',     # escudo con laurel
    'afmc':              'sello-afmc.png',                   # Advanced Functional Medicine Clinician
    'cfmc':              'sello-cfmc.png',                   # Certified Functional Medicine Clinician
    'fgu-escudo':        None, 'fgu-wordmark': None,         # ver iconos/ (Florida Global University)
}

def aval(nombre, ancho=None, alto=None):
    if AVALES.get(nombre) is None and nombre.startswith('fgu'):
        im = Image.open(os.path.join(DIR_I, 'azul', nombre + '.png')).convert('RGBA'); im = im.crop(im.getbbox())
    else:
        im = Image.open(os.path.join(DIR_A, AVALES[nombre])).convert('RGBA')
    if ancho or alto:
        ancho = ancho or round(im.width * alto / im.height)
        alto = alto or round(im.height * ancho / im.width)
        im = im.resize((ancho, alto), Image.LANCZOS)
    return im

def poner_aval(im, nombre, x, y, ancho=None, alto=None, anclaje='lt'):
    a = aval(nombre, ancho, alto)
    px = x - (a.width // 2 if anclaje[0] == 'c' else a.width if anclaje[0] == 'r' else 0)
    py = y - (a.height // 2 if anclaje[1] == 'm' else a.height if anclaje[1] == 'b' else 0)
    im.paste(a, (int(px), int(py)), a)
    return (int(px), int(py), int(px) + a.width, int(py) + a.height)

# Fondos de slide 1920x1080 aprobados (el logo ya viene colocado)
FONDOS_SLIDE = {
    'diagonal':      'slide-diagonal-logo-der.png',      # navy -> azul en diagonal, logo abajo-der
    'llama':         'slide-llama-logo-izq.png',         # llama de contorno a la derecha, logo abajo-izq
    'malla':         'slide-malla-filete-logo-der.png',  # malla con halos periwinkle/cian, filete + logo abajo-der
    'escudo':        'slide-escudo-linea-logo-izq.png',  # escudo de linea como marca de agua, logo abajo-izq
}

def fondo_slide(nombre):
    """Devuelve el fondo de slide oficial (RGB 1920x1080) listo para escribir encima."""
    return Image.open(os.path.join(DIR_FO, FONDOS_SLIDE[nombre])).convert('RGB')

# ─────────────────────────────────────────────────────────────────────
# TRATAMIENTO DE IMAGEN
#   LAI usa dos acabados: monocromo azul (retratos institucionales del
#   brochure) y duotono indigo-oro (piezas ceremoniales / certificados).
# ─────────────────────────────────────────────────────────────────────
def duotono(img, sombra='indigo_hondo', luz='blanco', contraste=1.12):
    g = ImageOps.autocontrast(img.convert('L'), cutoff=1)
    if contraste != 1:
        g = g.point(lambda v: max(0, min(255, int((v - 128) * contraste + 128))))
    return ImageOps.colorize(g, rgb(sombra), rgb(luz))

def tritono(img, sombra='indigo_hondo', medio='azul', luz='crema'):
    g = ImageOps.autocontrast(img.convert('L'), cutoff=1)
    return ImageOps.colorize(g, rgb(sombra), rgb(luz), mid=rgb(medio))

def mono_azul(img):
    """Acabado de retrato institucional LAI (paginas de fundadora, escarapelas)."""
    return duotono(img, sombra='#141428', luz='#FFFFFF', contraste=1.18)

def esquinas(img, radio):
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1],
                                        radio, fill=255)
    out = img.convert('RGBA'); out.putalpha(m); return out

def recorte_llenar(img, tam):
    """Recorta y escala tipo object-fit: cover."""
    w, h = tam
    r = max(w / img.width, h / img.height)
    n = img.resize((max(1, round(img.width * r)), max(1, round(img.height * r))), Image.LANCZOS)
    return n.crop(((n.width - w) // 2, (n.height - h) // 2,
                   (n.width - w) // 2 + w, (n.height - h) // 2 + h))

def velo(im, caja, color='indigo_hondo', desde=0, hasta=210, vertical=True):
    """Degradado de legibilidad sobre foto."""
    x0, y0, x1, y1 = caja
    w, h = x1 - x0, y1 - y0
    capa = Image.new('RGBA', (w, h))
    d = ImageDraw.Draw(capa)
    n = h if vertical else w
    for i in range(n):
        a = int(desde + (hasta - desde) * i / max(1, n - 1))
        if vertical: d.line([(0, i), (w, i)], fill=rgb(color, a))
        else:        d.line([(i, 0), (i, h)], fill=rgb(color, a))
    im.paste(Image.alpha_composite(im.convert('RGBA').crop(caja), capa).convert('RGB'), (x0, y0))
    return im

# ─────────────────────────────────────────────────────────────────────
# MOTOR DE TEXTO
#   texto()     -> una linea, devuelve la caja ocupada
#   parrafo()   -> texto con ajuste de linea, devuelve y final
#   rico()      -> parrafo con tramos de estilo mezclados en la misma linea
#                  (asi se compone "Nunca agitar: la cizalla forma..." donde
#                   el lead va en negrita azul y el cuerpo en gris regular)
# ─────────────────────────────────────────────────────────────────────
# ── REGISTRO PARA EL AUDITOR (reglas de la Dra., 10-oct-2026) ─────────────────────────────
_REG = {}
def _reg(im, tipo, caja, tam=0, txt='', color=None, nombre=''):
    _REG.setdefault(id(im), []).append(dict(tipo=tipo, caja=tuple(int(v) for v in caja), tam=tam, txt=txt, color=color, nombre=nombre))

def ancho_texto(txt, fnt):
    return ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(txt, font=fnt)

def texto(im, xy, txt, fnt, color='navy', anclaje='la', espaciado=0):
    """espaciado = tracking en px entre caracteres (letter-spacing)."""
    d = draw(im); x, y = xy
    if not espaciado:
        d.text((x, y), txt, font=fnt, fill=rgb(color), anchor=anclaje)
        bb = d.textbbox((x, y), txt, font=fnt, anchor=anclaje)
        _reg(im, 'texto', bb, fnt.size, txt, color); return bb
    total = sum(ancho_texto(c, fnt) for c in txt) + espaciado * (len(txt) - 1)
    if anclaje[0] == 'm': x -= total / 2
    elif anclaje[0] == 'r': x -= total
    x0 = x
    for c in txt:
        d.text((x, y), c, font=fnt, fill=rgb(color), anchor='l' + anclaje[1])
        x += ancho_texto(c, fnt) + espaciado
    asc, desc = fnt.getmetrics()
    _reg(im, 'rotulo', (x0, y, x0 + total, y + asc + desc), fnt.size, txt, color)
    return (x0, y, x0 + total, y + asc + desc)

def _cortar(txt, fnt, ancho_max):
    lineas, actual = [], ''
    for pal in txt.split():
        prueba = (actual + ' ' + pal).strip()
        if ancho_texto(prueba, fnt) <= ancho_max or not actual:
            actual = prueba
        else:
            lineas.append(actual); actual = pal
    if actual: lineas.append(actual)
    return lineas

def parrafo(im, xy, txt, fnt, color='gris_texto', ancho_max=600,
            interlinea=1.35, anclaje='l'):
    """Devuelve la coordenada Y inmediatamente debajo del ultimo renglon."""
    d = draw(im); x, y = xy
    salto = int(fnt.size * interlinea)
    for bloque in txt.split('\n'):
        for ln in (_cortar(bloque, fnt, ancho_max) or ['']):
            px = x if anclaje == 'l' else (x - ancho_texto(ln, fnt) / 2 if anclaje == 'c'
                                           else x - ancho_texto(ln, fnt))
            d.text((px, y), ln, font=fnt, fill=rgb(color))
            if ln.strip(): _reg(im, 'cuerpo', d.textbbox((px, y), ln, font=fnt), fnt.size, ln, color)
            y += salto
    return y

def rico(im, xy, tramos, ancho_max=600, interlinea=1.35, salto=None):
    """
    tramos = [(texto, fuente, color), ...]  -> se concatenan y se ajustan
    a ancho_max respetando el estilo de cada tramo. Usa '\n' para forzar salto.
    Devuelve el Y final.
    """
    d = draw(im); x0, y = xy
    x = x0
    alto = salto or int(max(f.size for _, f, _ in tramos) * interlinea)
    for txt, fnt, color in tramos:
        for i, bloque in enumerate(txt.split('\n')):
            if i: x, y = x0, y + alto
            for pal in bloque.split(' '):
                if pal == '': continue
                w = ancho_texto(pal + ' ', fnt)
                if x + w > x0 + ancho_max and x > x0:
                    x, y = x0, y + alto
                d.text((x, y), pal, font=fnt, fill=rgb(color))
                _reg(im, 'cuerpo', d.textbbox((x, y), pal, font=fnt), fnt.size, pal, color)
                x += w
    return y + alto

# ─────────────────────────────────────────────────────────────────────
# COMPONENTES VISUALES LAI
# ─────────────────────────────────────────────────────────────────────
def caja(im, cxy, radio=0, relleno=None, borde=None, grosor=2, sombra=0):
    """Rectangulo redondeado. cxy=(x0,y0,x1,y1)."""
    if sombra:
        s = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(s).rounded_rectangle(
            [cxy[0] + 2, cxy[1] + sombra // 2, cxy[2] + 2, cxy[3] + sombra // 2],
            radio, fill=rgb('negro', 46))
        s = s.filter(ImageFilter.GaussianBlur(sombra))
        im.paste(Image.alpha_composite(im.convert('RGBA'), s).convert('RGB'), (0, 0))
    draw(im).rounded_rectangle(list(cxy), radio,
                               fill=rgb(relleno) if relleno else None,
                               outline=rgb(borde) if borde else None, width=grosor)
    return cxy

def ficha_dato(im, cxy, rotulo, valor, relleno='lila', c_rot='azul', c_val='navy',
               f_rot=None, f_val=None, gap=14, pad_x=20, radio=12, borde=None, ref=('ACCESO', '30 1')):
    """Ficha de dato (rótulo + valor) con la TINTA centrada en la caja — regla de la Dra. (15-oct-2026):
    el aire entre el borde superior y la primera letra es IGUAL al aire entre la última letra y el borde inferior.
    Se mide con getbbox de una referencia común (`ref`: mayúsculas/cifras sin descendentes) para que varias fichas
    en fila compartan la misma línea base aunque un valor lleve descendentes (q, $, p). Nunca centrar por la caja
    de la fuente ni con offsets fijos."""
    x0, y0, x1, y1 = cxy
    f_rot = f_rot or F('lato', 'bold', 24); f_val = f_val or F('lato', 'bold', 30)
    caja(im, cxy, radio, relleno=relleno, borde=borde)
    bR, bV = f_rot.getbbox(ref[0]), f_val.getbbox(ref[1])
    hR, hV = bR[3] - bR[1], bV[3] - bV[1]
    aire = ((y1 - y0) - (hR + gap + hV)) / 2
    texto(im, (x0 + pad_x, round(y0 + aire - bR[1])), rotulo, f_rot, c_rot, espaciado=3)
    texto(im, (x0 + pad_x, round(y0 + aire + hR + gap - bV[1])), valor, f_val, c_val)
    return cxy

def fichas_dato(im, y, pares, x=None, ancho=None, alto=90, sep=20, **kw):
    """Fila de fichas de dato iguales (3 típicas) entre márgenes. Devuelve y final."""
    W, H = im.size; m = margen(im); x = m if x is None else x; ancho = (W - 2 * m) if ancho is None else ancho
    n = len(pares); fw = (ancho - sep * (n - 1)) // n
    for i, (rot, val) in enumerate(pares):
        fx = x + i * (fw + sep); ficha_dato(im, (fx, y, fx + fw, y + alto), rot, val, **kw)
    return y + alto

def franja_superior(im, alto, paradas=None, angulo=0):
    """Franja de cabecera (logo + etiqueta) con degradado HORIZONTAL y LIMPIA: sin patrón de llama, sin grano
    extra y sin fundido hacia la foto o el contenido de abajo (regla de la Dra., 15-oct-2026). Se pinta DESPUÉS
    de `patron_lai`/`fondo_profundo` para tapar la llama; la foto va debajo con borde recto. Devuelve y inferior."""
    W, H = im.size
    paradas = paradas or [(0, rgb('indigo_hondo')), (0.55, rgb('navy')), (1, rgb('azul'))]
    im.paste(gradiente((W, alto), paradas, angulo), (0, 0))
    return alto

def pill(im, xy, txt, fnt, relleno='azul_electrico', color='blanco',
         padx=34, pady=16, radio=None, anclaje='l', espaciado=0):
    """Pastilla de LAI: consignas, etiquetas, CTAs, 'CUADERNILLO DE CASOS'."""
    x, y = xy
    tw = sum(ancho_texto(c, fnt) for c in txt) + espaciado * (len(txt) - 1) if espaciado \
         else ancho_texto(txt, fnt)
    asc, desc = fnt.getmetrics()
    w, h = tw + padx * 2, asc + desc + pady * 2
    if anclaje == 'c': x -= w // 2
    elif anclaje == 'r': x -= w
    r = radio if radio is not None else h // 2
    caja(im, (x, y, x + w, y + h), r, relleno=relleno)
    texto(im, (x + w // 2, y + h // 2), txt, fnt, color, anclaje='mm', espaciado=espaciado)
    return (x, y, x + w, y + h)

def circulo_numero(im, cx, cy, r, n, fnt=None, relleno='lila', color='azul', cursiva=True):
    """Circulo lila con el numero de seccion, en cursiva negrita. Formato LAI."""
    f = fnt or F('lato', 'bold_i' if cursiva else 'bold', int(r * 1.15))
    draw(im).ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgb(relleno))
    texto(im, (cx, cy), str(n), f, color, anclaje='mm')
    return (cx - r, cy - r, cx + r, cy + r)

def perla_clinica(im, xy, ancho, titulo, cuerpo, tam=27, titulo_txt='Perla clínica'):
    """
    Caja menta con borde cian y estrella: el callout distintivo de las
    infografias de modulo LAI. `titulo` sustituye el rotulo si se pasa.
    """
    x, y = xy
    f_t = F('helv', 'bold_i', tam)
    f_c = F('helv', 'regular', tam)
    px, py, r_ic = 92, 26, int(tam * 1.05)
    lineas = []
    for b in cuerpo.split('\n'):
        lineas += _cortar(b, f_c, ancho - px - 28) or ['']
    alto = py * 2 + int(tam * 1.45) * (len(lineas) + 1)
    caja(im, (x, y, x + ancho, y + alto), 26, relleno='menta', borde='cian', grosor=3)
    cy = y + py + r_ic
    poner_icono(im, 'perla', x + 20 + r_ic, cy, int(r_ic * 1.9), 'azul')
    ty = y + py
    texto(im, (x + px, ty), titulo or titulo_txt, f_t, 'cian_hondo')
    ty += int(tam * 1.45)
    for ln in lineas:
        texto(im, (x + px, ty), ln, f_c, 'gris_texto'); ty += int(tam * 1.45)
    return (x, y, x + ancho, y + alto)

def vinetas(im, xy, items, ancho, tam=27, color_lead='navy',
            color_cuerpo='gris_texto', marca='cian', interlinea=1.42, sep=18):
    """
    Vinetas con diamante LAI.
    items = [(lead, cuerpo), ...]  el lead va en negrita de color, el cuerpo regular.
    Un cuerpo que empiece por '!' se pinta en rojo de alerta.
    """
    x, y = xy
    f_b = F('helv', 'bold', tam); f_r = F('helv', 'regular', tam)
    sangria = int(tam * 1.55)
    for lead, cuerpo in items:
        col = 'rojo' if cuerpo.startswith('!') else color_cuerpo
        cuerpo = cuerpo.lstrip('!').lstrip()
        diamante(im, x + tam * 0.55, y + tam * 0.70, tam * 0.46, marca)
        y = rico(im, (x + sangria, y),
                 [(lead + ' ', f_b, color_lead), (cuerpo, f_r, col)],
                 ancho_max=ancho - sangria, interlinea=interlinea)
        y += sep
    return y

def caption(im, xy, txt, tam=24, relleno='lila', color='azul', anclaje='l', ancho_max=520):
    """Etiqueta de pie de imagen sobre bloque lila (formato infografia LAI)."""
    f = F('helv', 'regular', tam)
    x, y = xy
    for ln in _cortar(txt, f, ancho_max):
        w = ancho_texto(ln, f) + 24
        px = x if anclaje == 'l' else x - w
        caja(im, (px, y, px + w, y + int(tam * 1.6)), 4, relleno=relleno)
        texto(im, (px + 12, y + int(tam * 0.16)), ln, f, color)
        y += int(tam * 1.85)
    return y

def regla(im, x0, y, x1, color='gris_linea', grosor=2):
    draw(im).line([(x0, y), (x1, y)], fill=rgb(color), width=grosor)
    return y + grosor

def header_modulo(im, numero, titulo, alto=None, logo_ancho=None, rotulo='Módulo'):
    """
    Banda superior de infografia de modulo:
    banda indigo + 'Modulo N' en caja de borde cian + subtitulo periwinkle
    + logo horizontal blanco arriba a la derecha.
    """
    W = im.width
    h = alto or int(im.height * 0.15)
    fondo_banda(im, (0, 0, W, h))
    patron_lai(im, 'blanco', 14, escala=0.6, semilla=11)
    lw = logo_ancho or int(W * 0.29)
    poner_logo(im, 'horizontal-blanco', W - int(W * 0.055), int(h * 0.16), ancho=lw, anclaje='rt')
    mx = int(W * 0.085)
    f_m = F('lato', 'light', int(h * 0.165))
    r = pill(im, (mx, int(h * 0.47)), '%s %s' % (rotulo, numero), f_m,
             relleno=None, color='cian', padx=28, pady=int(h * 0.018), radio=6)
    caja(im, r, 6, borde='cian', grosor=3)
    f_s = F('helv', 'bold', int(h * 0.155))
    texto(im, (mx + 22, r[3] + int(h * 0.045)), titulo, f_s, 'periwinkle_cl')
    return h

def footer_lai(im, izquierda='', alto=None, anio=2026,
               entidad='Longevity & Functional Medicine Academic Institute',
               sitio='www.longevityacademicinstitute.com'):
    """Banda inferior indigo: rotulo a la izquierda, escudo al centro, copyright a la derecha."""
    W, H = im.size
    h = alto or int(H * 0.043)
    y0 = H - h
    fondo_banda(im, (0, y0, W, H))
    f = F('helv', 'bold', int(h * 0.21))
    if izquierda:
        texto(im, (int(W * 0.032), y0 + h // 2), izquierda.upper(), f,
              'periwinkle_cl', anclaje='lm')
    poner_logo(im, 'horizontal-blanco', W // 2, y0 + h // 2,
               ancho=int(W * 0.115), anclaje='cm')
    der = '© %s %s.\nTodos los derechos reservados · %s' % (anio, entidad, sitio.replace('www.', ''))
    tf = int(h * 0.19)
    while tf > 8 and max(ancho_texto(l, F('helv', 'regular', tf)) for l in der.split('\n')) > W * 0.36:
        tf -= 1
    f2 = F('helv', 'regular', tf)
    yy = y0 + h // 2 - int(h * 0.21)
    for ln in der.split('\n'):
        texto(im, (W - int(W * 0.032), yy), ln, f2, 'periwinkle_cl', anclaje='rm')
        yy += int(h * 0.26)
    return y0

def marco_oro(im, margen, grosor=4, radio=0, doble=True):
    """Filete dorado de certificados y diplomas."""
    W, H = im.size
    g = gradiente_oro((W, H), 0)
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    d.rounded_rectangle([margen, margen, W - margen, H - margen], radio,
                        outline=255, width=grosor)
    if doble:
        o = margen + grosor * 4
        d.rounded_rectangle([o, o, W - o, H - o], max(0, radio - grosor * 2),
                            outline=255, width=max(1, grosor // 3))
    im.paste(g, (0, 0), m)
    return im

SOCIAL = ('story', 'post', 'carrusel', 'banner')

def margen(im):
    """Zona segura = 10 % del lado más corto, en los 4 lados (guía de márgenes de la Dra., 10-oct-2026).
    story 1080×1920 → 108 · carrusel 1080×1350 → 108 · post 1080 → 108 · banner 1200×630 → 63 · portada 851×315 → 32.
    Solo el pie (@usuario, web, cápsula) vive en la banda del margen inferior, centrado y dentro de los márgenes laterales."""
    return round(0.10 * min(im.size))

def auditar(im, social=True, pie_y=None):
    """Revisa la pieza con lo que registraron texto()/parrafo()/rico()/poner_logo(). Devuelve lista de fallos.
    F1 piso (a 1080 de ancho): ningún texto < 20 px (pie/aclaratorios (*)); rótulos/antetítulos ≥ 24; cuerpo ≥ 27
       (= «Nuestra academia nace de una convicción», el mínimo de cuerpo aprobado). F2 zona segura. F3 contraste ≥ 4.5:1
       (titulares ≥ 60 px: ≥ 7:1). F7 logo horizontal ≈ 34 % del ancho (pieza «Nuestra visión»: 31–37 %)."""
    W, H = im.size; m = margen(im); k = W / 1080; f = []
    pie_y = pie_y if pie_y is not None else H - m
    rgbim = im.convert('RGB')
    import numpy as _np
    A = _np.asarray(rgbim).astype(float)
    def _l(c):
        c = _np.asarray(c, float) / 255; c = _np.where(c <= .03928, c / 12.92, ((c + .055) / 1.055) ** 2.4)
        return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
    for r in _REG.get(id(im), []):
        x0, y0, x1, y1 = r['caja']
        if r['tipo'] == 'logo':
            if x0 < m - 2 or y0 < m - 2 or x1 > W - m + 2 or y1 > H - m + 2: f.append(f"F7 logo {r['nombre']} fuera de la zona segura")
            if social and 'horizontal' in r['nombre'] and not (.31 * W <= x1 - x0 <= .37 * W):
                f.append(f"F7 logo {r['nombre']} {x1-x0}px — estándar 31–37 % del ancho ({round(.34*W)}px)")
            continue
        pie = y0 >= pie_y - 2
        if social:
            fs = r['tam'] / k
            fl = 20 if pie else (27 if (r['tipo'] == 'cuerpo' and len(r['txt']) > 3) else (24 if r['tipo'] == 'rotulo' else 20))
            if fs + .3 < fl: f.append(f"F1 piso: «{r['txt'][:30]}» {fs:.0f}px < {fl}px")
        if not pie and (x0 < m - 2 or x1 > W - m + 2 or y0 < m - 2 or y1 > H - m + 2):
            f.append(f"F2 margen: «{r['txt'][:30]}» sale de la zona segura ({m}px)")
        if r['color'] is not None and x1 > x0 and y1 > y0:
            reg = A[max(0, y0):min(H, y1), max(0, x0):min(W, x1)].reshape(-1, 3)
            if len(reg):
                fg = _np.array(rgb(r['color'])[:3], float); dist = _np.abs(reg - fg).sum(1)
                bgp = reg[dist > 90]
                if len(bgp) > 10:
                    la, lb = _l(fg), _l(_np.median(bgp, 0)); cr = (max(la, lb) + .05) / (min(la, lb) + .05)
                    need = 7.0 if r['tam'] / k >= 60 else 4.5
                    if cr < need: f.append(f"F3 contraste {cr:.1f}:1 (<{need}) «{r['txt'][:30]}»")
    tx = [r for r in _REG.get(id(im), []) if r['tipo'] != 'logo']
    if social and len(tx) >= 3:
        fss = sorted(set(round(r['tam'] / k) for r in tx)); cu = [r['tam'] / k for r in tx if r['tipo'] == 'cuerpo']
        if cu and len(tx) >= 4 and len(fss) < 3: f.append(f"F8 jerarquía plana: solo {len(fss)} tamaños {fss}")
        if cu and max(fss) < 2.4 * max(cu): f.append(f"F8 jerarquía: titular {max(fss)}px < 2.4 × cuerpo ({max(cu):.0f}px)")
        if sum(1 for r in tx if r['tam'] / k <= 20.5) > len(tx) / 2: f.append("F8 jerarquía: más de la mitad de los textos en el tamaño mínimo")
    return f

def guardar(im, ruta, dpi=300, auditoria=True):
    if auditoria and im.size in [LIENZOS[k] for k in SOCIAL if k in LIENZOS]:
        _f = auditar(im)
        if _f: print('AUDITOR LAI —', os.path.basename(ruta)); [print('   ', x) for x in _f]
    ext = os.path.splitext(ruta)[1].lower()
    if ext in ('.jpg', '.jpeg'):
        im.convert('RGB').save(ruta, quality=94, dpi=(dpi, dpi), optimize=True)
    elif ext == '.pdf':
        im.convert('RGB').save(ruta, resolution=dpi)
    else:
        im.save(ruta, dpi=(dpi, dpi), optimize=True)
    return ruta

# ─────────────────────────────────────────────────────────────────────
# PLANTILLAS MAESTRAS
# ─────────────────────────────────────────────────────────────────────
def portada_compendio(antetitulo, titulo_1, titulo_2, coletilla, bloque,
                      subbloque='', autor='DRA. CAROLINA RODRÍGUEZ MORALES',
                      etiqueta=None, formato='a4', descriptor='',
                      descriptor_it=''):
    """
    Portada de compendio academico / cuadernillo de casos LAI.

    antetitulo  'COMPENDIO ACADÉMICO DE'  (versalita espaciada, periwinkle)
    titulo_1    'Medicina Peptídica y'    (blanco, Lato bold)
    titulo_2    'Bioregulación Celular.'  (teal #4AF1D2, Lato bold)
    coletilla   'en escenarios clínicos reales'  (blanco cursiva; la ultima
                palabra va en negrita, como en las portadas maestras)
    bloque      'Módulo 12'               (teal, alineado a la derecha)
    descriptor  titulo del modulo (blanco, centrado bajo el filete)
    descriptor_it  bajada en cursiva
    etiqueta    pastilla opcional, ej 'CUADERNILLO DE CASOS CLÍNICOS'
    """
    im = lienzo(formato)
    fondo_profundo(im, angulo=118)
    W, H = im.size
    u = W / 1000.0                              # unidad relativa al ancho
    mx = int(W * 0.115)
    poner_logo(im, 'horizontal-blanco', W - mx, int(H * 0.052),
               ancho=int(W * 0.245), anclaje='rt')

    y = int(H * 0.175)
    texto(im, (mx, y), antetitulo.upper(), F('lato', 'light', int(28 * u)),
          'lila', espaciado=int(3.2 * u))
    y += int(58 * u)
    f_t = F('lato', 'bold', int(70 * u))
    texto(im, (mx, y), titulo_1, f_t, 'blanco');              y += int(88 * u)
    texto(im, (mx, y), titulo_2, f_t, 'teal');                y += int(84 * u)
    partes = coletilla.rsplit(' ', 1)
    rico(im, (mx, y), [(partes[0] + ' ', F('lato', 'light_i', int(46 * u)), 'blanco'),
                       (partes[-1] if len(partes) > 1 else '',
                        F('lato', 'bold_i', int(46 * u)), 'blanco')],
         ancho_max=W - mx * 2)
    y += int(96 * u)
    if etiqueta:
        pill(im, (mx, y), etiqueta.upper(), F('lato', 'regular', int(24 * u)),
             relleno='azul', color='blanco', padx=int(34 * u), pady=int(12 * u),
             espaciado=int(2.4 * u))

    yb = int(H * 0.645)
    texto(im, (W - mx, yb), bloque, F('lato', 'bold', int(56 * u)), 'teal', anclaje='ra')
    yb += int(88 * u)
    regla(im, int(W * 0.36), yb, W - mx, 'lila', 2); yb += int(32 * u)
    cx = int((W * 0.36 + W - mx) / 2)
    if descriptor:
        for ln in _cortar(descriptor, F('lato', 'regular', int(30 * u)), W * 0.60):
            texto(im, (cx, yb), ln, F('lato', 'regular', int(30 * u)), 'blanco', anclaje='ma')
            yb += int(44 * u)
    if descriptor_it:
        for ln in _cortar(descriptor_it, F('lato', 'light_i', int(29 * u)), W * 0.60):
            texto(im, (cx, yb), ln, F('lato', 'light_i', int(29 * u)), 'lila', anclaje='ma')
            yb += int(42 * u)

    texto(im, (W // 2, int(H * 0.905)), autor.upper(),
          F('lato', 'light', int(24 * u)), 'lila', anclaje='ma', espaciado=int(3.4 * u))
    return im


def membrete(formato='carta', pie=True, alto_banda=0.164):
    """
    Hoja membreteada LAI: banda superior con gradiente horizontal
    (indigo profundo a la izquierda -> azul electrico a la derecha),
    logo horizontal blanco arriba a la derecha, pie de pagina legal.
    Devuelve (imagen, caja_util) donde caja_util = (x0,y0,x1,y1) del area
    de contenido.
    """
    im = lienzo(formato, 'blanco')
    W, H = im.size
    hb = int(H * alto_banda)
    im.paste(gradiente((W, hb), [(0.0, 'indigo_hondo'), (0.5, 'navy'),
                                 (1.0, 'azul')], 0), (0, 0))
    patron_lai(im, 'blanco', 12, escala=0.5, semilla=5)
    poner_logo(im, 'horizontal-blanco', W - int(W * 0.075), int(hb * 0.30),
               ancho=int(W * 0.235), anclaje='rt')
    if pie:
        f = F('lato', 'light', max(10, int(W * 0.0125)))
        yy = H - int(H * 0.048)
        for ln in ['© %d Longevity & Functional Medicine Academic Institute.' % 2026,
                   'Todos los derechos reservados. longevityacademicinstitute.com']:
            texto(im, (W - int(W * 0.075), yy), ln, f, 'navy', anclaje='ra')
            yy += int(W * 0.019)
    return im, (int(W * 0.10), hb + int(H * 0.055), W - int(W * 0.10), H - int(H * 0.085))


def tarjeta_icono(im, caja_xy, titulo, items, icono_marca=None, radio=18,
                  relleno='#FFFFFF', borde='lila', tam_t=30, tam=24):
    """
    Tarjeta de la infografia de una pagina ('Buenas practicas en...'):
    insignia circular con degradado + titulo azul + vinetas compactas.
    """
    x0, y0, x1, y1 = caja_xy
    caja(im, caja_xy, radio, relleno=relleno, borde=borde, grosor=2)
    r = int(tam_t * 0.95)
    cx, cy = x0 + 28 + r, y0 + 26 + r
    ins = gradiente((r * 2, r * 2), [(0, '#4E57FF'), (1, '#8D89F7')], 45)
    m = Image.new('L', (r * 2, r * 2), 0)
    ImageDraw.Draw(m).ellipse([0, 0, r * 2 - 1, r * 2 - 1], fill=255)
    im.paste(ins, (cx - r, cy - r), m)
    if icono_marca: poner_icono(im, icono_marca, cx, cy, int(r * 1.15), 'blanco')
    else: diamante(im, cx, cy, r * 0.5, 'blanco')
    texto(im, (cx + r + 20, cy), titulo, F('helv', 'bold', tam_t), 'azul', anclaje='lm')
    return vinetas(im, (x0 + 28, y0 + 26 + r * 2 + 18), items,
                   ancho=x1 - x0 - 56, tam=tam, sep=10)


# ─────────────────────────────────────────────────────────────────────
# ESTILO GRAFICO v2 — recuadro biselado, subrayado cian, fichas de infografia
# ─────────────────────────────────────────────────────────────────────
RECUADRO = {                     # tipo -> color del filete
    'nota':  'azul_electrico',   # recuadro estandar (nota de libro)
    'dato':  'cian',             # solo cifras del programa y resultados, nunca advertencias
    'alerta':'rojo',             # solo seguridad del paciente: contraindicaciones, dosis techo, interacciones
}

def recuadro_biselado(im, cxy, tipo='nota', titulo=None, cuerpo=None, u=1.0, radio=None):
    """
    Recuadro biselado LAI (Manual v2 · 01). Relleno blanco -> #F7F7FC, bisel con dos
    sombras interiores (blanco arriba-izq, navy 13 % abajo-der), asiento exterior minimo,
    filete vertical de 4 px con puntas redondeadas separado 18 px de arriba y abajo.
    u = factor de escala (1.0 = pantalla @1x; usar ~3.1 para 300 dpi impreso).
    """
    x0, y0, x1, y1 = [int(v) for v in cxy]
    r = int((radio or 12) * u); b = max(1, int(2 * u))
    w, h = x1 - x0, y1 - y0
    # asiento exterior minimo (no sombra difusa grande)
    s = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle([x0, y0 + b, x1, y1 + b], r, fill=rgb('navy', 22))
    s = s.filter(ImageFilter.GaussianBlur(max(1, b)))
    im.paste(Image.alpha_composite(im.convert('RGBA'), s).convert('RGB'), (0, 0))
    relleno = gradiente((w, h), [(0, '#FFFFFF'), (1, '#F7F7FC')], 90).convert('RGBA')
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    # bisel: inset 2px 2px 0 #FFF (arriba-izq) / inset -2px -2px 0 rgba(27,20,100,.13) (abajo-der)
    bis = Image.new('RGBA', (w, h), (0, 0, 0, 0)); bd = ImageDraw.Draw(bis)
    bd.rounded_rectangle([0, 0, w - 1, h - 1], r, fill=rgb('navy', 33))
    bd.rounded_rectangle([0, 0, w - 1 - b, h - 1 - b], r, fill=(255, 255, 255, 255))
    bd.rounded_rectangle([b, b, w - 1 - b, h - 1 - b], r, fill=(0, 0, 0, 0))
    relleno.alpha_composite(bis)
    im.paste(relleno.convert('RGB'), (x0, y0), m)
    # filete
    g = max(2, int(4 * u)); sep = int(18 * u); fx = x0 + int(18 * u)
    draw(im).line([(fx, y0 + sep), (fx, y1 - sep)], fill=rgb(RECUADRO[tipo]), width=g)
    for yy in (y0 + sep, y1 - sep):
        draw(im).ellipse([fx - g / 2, yy - g / 2, fx + g / 2, yy + g / 2], fill=rgb(RECUADRO[tipo]))
    y = y0 + int(22 * u); tx = fx + int(22 * u); ancho = x1 - tx - int(20 * u)
    if titulo:
        y = parrafo(im, (tx, y), titulo, F('lato', 'bold', int(17 * u)), 'navy',
                    ancho_max=ancho, interlinea=1.2) + int(6 * u)
    if cuerpo:
        y = parrafo(im, (tx, y), cuerpo, F('helv', 'regular', int(13.5 * u)), 'gris_texto',
                    ancho_max=ancho, interlinea=1.5)
    return (x0, y0, x1, y1)

def subrayado_cian(im, xy, txt, fnt, color='navy', u=1.0):
    """Termino tecnico con subrayado de cian: filete de 5 px anclado bajo la linea de base
    con 7 px de aire (se lee igual sobre claro y oscuro). Un solo recurso de enfasis por frase."""
    x, y = xy
    asc, desc = fnt.getmetrics()
    w = ancho_texto(txt, fnt)
    yb = y + asc + desc + int(7 * u) - int(5 * u)
    draw(im).rectangle([x, yb, x + w, yb + int(5 * u)], fill=rgb('cian'))
    texto(im, (x, y), txt, fnt, color)
    return x + w

def anillo_avance(im, cx, cy, r, pct, color='blanco', u=1.0):
    """Anillo de avance de las fichas (va en blanco sobre el extremo oscuro del degradado)."""
    g = max(2, int(2.5 * u))
    d = draw(im)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=rgb(color, 90), width=g)
    d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * pct / 100, fill=rgb(color), width=g)
    texto(im, (cx, cy), '%d%%' % pct, F('lato', 'bold', int(r * 0.62)), color, anclaje='mm')

def ficha_infografia(im, cxy, rotulo, pct, icono_nombre, titulo, cuerpo,
                     estilo='navy_azul', u=1.0):
    """
    Ficha de infografia (Manual v2 · 03): panel con degradado de la paleta; encima,
    recuadro blanco con icono de marca en azul, titulo Lato Bold navy y cuerpo Arimo.
    Rotulo del paso y anillo de avance en blanco sobre el extremo OSCURO del degradado.
    """
    x0, y0, x1, y1 = [int(v) for v in cxy]
    w, h = x1 - x0, y1 - y0
    r = int(14 * u)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    im.paste(degradado((w, h), estilo), (x0, y0), m)
    pad = int(12 * u)
    texto(im, (x0 + pad + int(4 * u), y0 + int(22 * u)), rotulo.upper(),
          F('lato', 'bold', int(11 * u)), 'blanco', anclaje='lm', espaciado=int(1.4 * u))
    anillo_avance(im, x1 - pad - int(12 * u), y0 + int(22 * u), int(11 * u), pct, 'blanco', u)
    cx0, cy0, cx1, cy1 = x0 + pad, y0 + int(44 * u), x1 - pad, y1 - pad
    cw, ch = cx1 - cx0, cy1 - cy0
    mm = Image.new('L', (cw, ch), 0); ImageDraw.Draw(mm).rounded_rectangle([0, 0, cw - 1, ch - 1], int(10 * u), fill=255)
    im.paste(gradiente((cw, ch), [(0, '#FFFFFF'), (1, '#F7F7FC')], 90), (cx0, cy0), mm)
    ccx = (cx0 + cx1) // 2
    poner_icono(im, icono_nombre, ccx, cy0 + int(30 * u), max(24, int(30 * u)), 'azul')
    texto(im, (ccx, cy0 + int(56 * u)), titulo, F('lato', 'bold', int(14 * u)), 'navy', anclaje='ma')
    f = F('helv', 'regular', int(10.5 * u)); yy = cy0 + int(80 * u)
    for ln in _cortar(cuerpo, f, cw - int(24 * u)):
        texto(im, (ccx, yy), ln, f, 'gris_texto', anclaje='ma'); yy += int(15 * u)
    return (x0, y0, x1, y1)


# ─────────────────────────────────────────────────────────────────────
# PLANTILLA MAESTRA · PORTADA DE DOCENTE (slide 1920x1080)
#   Medida en pixeles sobre la pieza aprobada (references/piezas-maestras/slides/
#   portada-docente-carolina.png). Todas las cotas estan a 1920 px de ancho y se
#   escalan con u = W/1920.
# ─────────────────────────────────────────────────────────────────────
def _fondo_portada_docente(tam):
    w, h = tam
    base = gradiente(tam, [(0, 'indigo_hondo'), (0.55, 'navy'), (1, 'navy')], 20)
    import numpy as np
    arr = np.asarray(base, dtype=np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    for cx, cy, r, col, k in [(1.0, -0.05, 0.75, 'azul', 0.55), (0.0, 1.05, 0.55, 'navy', 0.6),
                              (0.46, 0.0, 0.35, 'indigo_hondo', 0.7)]:
        d = np.hypot(xx - cx * w, yy - cy * h) / (r * (w * h) ** 0.5)
        t = np.clip(1 - d, 0, 1); a = t * t * (3 - 2 * t) * k
        arr = arr * (1 - a[..., None]) + np.array(rgb(col), np.float32) * a[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype('uint8'), 'RGB')

def avatar_circular(foto, diametro, anillo='lila', mono=True, encuadre=(0.5, 0.20, 0.62)):
    """Retrato en circulo (cabeza y hombros) sobre fondo navy, con anillo fino.
    encuadre = (centro_x, centro_y, lado) como fraccion del ancho/alto del recorte."""
    f = foto.convert('RGBA')
    cx, cy, lado = encuadre
    L = int(f.width * lado)
    x0 = int(f.width * cx - L / 2); y0 = max(0, int(f.height * cy - L * 0.42))
    f = f.crop((x0, y0, x0 + L, y0 + L)).resize((diametro, diametro), Image.LANCZOS)
    if mono:
        a = f.getchannel('A'); g = ImageOps.autocontrast(f.convert('L'), cutoff=1)
        f = Image.merge('RGBA', (g, g, g, a))
        t = Image.new('RGBA', f.size, rgb('indigo_hondo') + (255,)); f = Image.blend(f, t, 0.18); f.putalpha(a)
    fondo = degradado((diametro, diametro), 'navy_azul').convert('RGBA')
    fondo.alpha_composite(f)
    m = Image.new('L', (diametro, diametro), 0); ImageDraw.Draw(m).ellipse([0, 0, diametro - 1, diametro - 1], fill=255)
    fondo.putalpha(m)
    if anillo:
        ImageDraw.Draw(fondo).ellipse([1, 1, diametro - 2, diametro - 2], outline=rgb(anillo, 120), width=max(2, diametro // 80))
    return fondo

def portada_docente(nombre, bullets, antetitulo='FORMACIÓN ACADÉMICA EN',
                    titulo_1='Medicina Peptídica y', titulo_2='Bioregulación Celular',
                    coletilla=(('en escenarios clínicos ', False), ('reales', True)),
                    foto=None, avales=('kharrazian-blanco', 'cfmc', 'afmc'), variante='B',
                    tam=(1920, 1080)):
    """
    Portada de docente / conferencista (slide 1920x1080). Medida en pixeles sobre las piezas
    aprobadas (references/piezas-maestras/slides/). Cotas a 1920 px, escaladas con u = W/1920.

    variante 'B' (POR DEFECTO, aprobada): composicion tipografica a todo el ancho desde x=160;
      la foto del docente va SOLO como avatar circular (Ø 168 px) junto al bloque "DIRIGIDO POR".
    variante 'A': foto B/N recortada a sangre en el panel izquierdo (uso excepcional).

      nombre   'Dra. Carolina Rodríguez Morales'
      bullets  [[('texto', negrita), ...], ...]; un item que empieza con '+' continua el anterior
               sin viñeta (segunda linea del mismo logro). VERBATIM: no se corrige ni se completa.
      foto     Image RGBA recortada (retrato_recorte(mono=False)) o None -> circulo vacio con anillo.
      avales   nombres de AVALES del docente; kharrazian arriba, sellos debajo.
    """
    W, H = tam; u = W / 1920
    im = _fondo_portada_docente(tam)
    esc = elemento('escudo-linea', 'blanco', alto=int(1160 * u))
    esc.putalpha(esc.getchannel('A').point(lambda v: int(v * 0.15)))
    im.paste(Image.alpha_composite(im.convert('RGBA'), _capa(im.size, esc, int(1315 * u), int(252 * u))).convert('RGB'), (0, 0))
    if variante == 'A':
        X, XD, XB, DER = 880 * u, 880 * u, 901 * u, 1840 * u
        if foto is not None:
            f = foto.copy()
            f = f.resize((int(f.width * (H * 0.96) / f.height), int(H * 0.96)), Image.LANCZOS)
            tinte = Image.new('RGBA', f.size, rgb('indigo_hondo') + (255,))
            a = f.getchannel('A'); f = Image.blend(f, tinte, 0.22); f.putalpha(a)
            capa = _capa(im.size, f, int(430 * u - f.width / 2), H - f.height)
            grad = Image.linear_gradient('L').rotate(-90, expand=True).resize((int(340 * u), H))
            mask = Image.new('L', im.size, 255)
            mask.paste(grad, (int(540 * u), 0)); mask.paste(0, (int(880 * u), 0, W, H))
            capa.putalpha(ImageChops.multiply(capa.getchannel('A'), mask))
            im.paste(Image.alpha_composite(im.convert('RGBA'), capa).convert('RGB'), (0, 0))
    else:
        X, XD, XB, DER = 160 * u, 371 * u, 390 * u, 1760 * u
        d = int(168 * u); cx, cy = int(244 * u), int(816 * u)
        if foto is not None:
            av = avatar_circular(foto, d)
            im.paste(av, (cx - d // 2, cy - d // 2), av)
        else:
            draw(im).ellipse([cx - d // 2, cy - d // 2, cx + d // 2, cy + d // 2], outline=rgb('lila', 90), width=max(2, int(2 * u)))
    X, XD, XB, DER = int(X), int(XD), int(XB), int(DER)
    poner_logo(im, 'horizontal-blanco', DER, int(80 * u), ancho=int(460 * u), anclaje='rt')
    im.paste(gradiente_oro((int(34 * u), max(2, int(3 * u)))), (X, int(299 * u)))
    texto(im, (X, int(318 * u)), antetitulo.upper(), F('lato', 'regular', int(20 * u)), 'menta', espaciado=int(6.2 * u))
    texto(im, (X, int(366 * u)), titulo_1, F('lato', 'light', int(80 * u)), 'blanco')
    f2 = F('lato', 'bold', int(80 * u))
    texto(im, (X, int(450 * u)), titulo_2, f2, 'blanco')
    draw(im).rectangle([X, int(542 * u), X + ancho_texto(titulo_2, f2), int(546 * u)], fill=rgb('cian'))
    rico(im, (X, int(556 * u)), [(t, F('lato', 'bold_i' if b else 'italic', int(35 * u)), 'blanco' if b else 'lila')
                                 for t, b in coletilla], ancho_max=int(960 * u))
    draw(im).line([(X, int(656 * u)), (DER, int(656 * u))], fill=rgb('lila', 46), width=max(1, int(u)))
    texto(im, (XD, int(689 * u)), 'DIRIGIDO POR:', F('lato', 'bold', int(15 * u)), 'lila', espaciado=int(2.6 * u))
    texto(im, (XD, int(714 * u)), nombre, F('lato', 'bold', int(36 * u)), 'blanco')
    y = int(774 * u); fr = F('helv', 'regular', int(22 * u)); fb = F('helv', 'bold', int(22 * u))
    for it in bullets:
        if it and it[0][0].startswith('+'):
            y -= int(8 * u); it = [(it[0][0][1:].lstrip(), it[0][1])] + list(it[1:])
        else:
            draw(im).ellipse([XB - 19 * u, y + 10 * u, XB - 12 * u, y + 17 * u], fill=rgb('periwinkle'))
        rico(im, (XB, y), [(t, fb if b else fr, 'blanco') for t, b in it], ancho_max=int(740 * u), interlinea=1.3)
        y += int(38 * u)
    ax = DER - int(92 * u)
    sellos = [a for a in avales if a in ('cfmc', 'afmc')]
    ks = [a for a in avales if a.startswith('kharrazian')]
    if ks:
        poner_aval(im, ks[0], ax, int(766 * u), ancho=int(180 * u), anclaje='cm')
    xs = [ax] if len(sellos) == 1 else [ax - int(51 * u), ax + int(51 * u)]
    for a, cx in zip(sellos, xs):
        poner_aval(im, a, cx, int(857 * u), ancho=int(86 * u), anclaje='cm')
    return im

def _capa(tam, pieza, x, y):
    c = Image.new('RGBA', tam, (0, 0, 0, 0)); x, y = int(x), int(y)
    sx, sy = max(0, -x), max(0, -y)
    c.alpha_composite(pieza.crop((sx, sy, pieza.width, pieza.height)), (max(0, x), max(0, y)))
    return c
