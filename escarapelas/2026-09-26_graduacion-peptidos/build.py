#!/usr/bin/env python3
"""
Escarapelas — Graduación «Medicina Peptídica y Bioregulación Celular»
Longevity Academic Institute · 26 de septiembre de 2026

Genera:
  out/escarapelas_<tamaño>.pdf              → 1 página por cara (frente/reverso), tamaño real
  out/escarapelas_carta_<n>up_<tamaño>.pdf  → imposición en Carta (n por hoja) con marcas de corte,
                                              lista para dúplex (voltear por el borde largo)
  out/preview/*.png                         → vista previa de cada frente, reverso y hoja 1

Uso:  python3 build.py                       # 90 × 130 mm, 4 por hoja Carta (2 × 2)
      python3 build.py --size 100x150 --cols 2 --rows 1   # 10 × 15 cm, 2 por hoja
Requiere: playwright (python), qrcode, pillow. Chromium ya instalado en el contenedor.
"""
import base64
import io
import os
import re
import sys
from pathlib import Path

import qrcode
from qrcode.image.pil import PilImage

HERE = Path(__file__).parent
OUT = HERE / "out"
PREV = OUT / "preview"
OUT.mkdir(exist_ok=True)
PREV.mkdir(exist_ok=True)

# ─────────────────────────── Contenido ───────────────────────────
EVENTO = {
    "eyebrow": "FORMACIÓN ACADÉMICA EN",
    "titulo_1": "Medicina Peptídica y",
    "titulo_2": "Bioregulación Celular.",
    "sub_pre": "en escenarios clínicos ",
    "sub_bold": "reales",
    "fecha": "26 DE SEPTIEMBRE DE 2026",
    "url_texto": "www.longevityacademicinstitute.com",
    "url_qr": "https://www.longevityacademicinstitute.com",
}

# (rol vertical, líneas del nombre)
PERSONAS = [
    ("ESTUDIANTE", ["EDUARD", "CAICEDO MONDRAGÓN"]),
    ("ESTUDIANTE", ["CARMEN EDUARDA", "MEDINA AMORIM"]),
    ("ESTUDIANTE", ["MARISSA DEL CARMEN", "APARICIO POLANCO"]),
    ("ESTUDIANTE", ["DAHYANNA ANDREA", "DÍAZ OSPINA"]),
    ("ESTUDIANTE", ["MARÍA ALEJANDRA", "LUGO"]),
    ("ESTUDIANTE", ["JULIETH", "MARTINEZ OCAMPO"]),
    ("ESTUDIANTE", ["MARÍA MERCEDES", "MARTÍNEZ CADAVID"]),
    ("STAFF LOGÍSTICO", ["IVÁN VELÁSQUEZ"]),
    ("STAFF LOGÍSTICO", ["MAURA ALMANZA"]),
    ("STAFF LOGÍSTICO", ["MANUELA LEGARDA"]),
    ("STAFF LOGÍSTICO", ["TIBISAY ARAQUE"]),
    ("CONFERENCISTA", ["DRA. CAROLINA", "RODRÍGUEZ MORALES"]),
]

# ─────────────────────────── Medidas (mm) ───────────────────────────
import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument("--size", default="90x130", help="ancho x alto en mm (p. ej. 90x130 o 100x150)")
_ap.add_argument("--cols", type=int, default=2)
_ap.add_argument("--rows", type=int, default=2)
_ap.add_argument("--gap", type=float, default=5.0, help="separación entre escarapelas en la hoja (mm)")
_args = _ap.parse_args()

W, H = (float(v) for v in _args.size.lower().split("x"))   # tamaño escarapela
S = W / 100.0              # factor de escala tipográfica (diseño base: 100 × 150 mm)
HOLE_ZONE = round(14 * S, 1)   # franja superior libre para perforación / ojalete
LETTER_W, LETTER_H = 215.9, 279.4
COLS, ROWS, GAP = _args.cols, _args.rows, _args.gap
TAG = f"{W:g}x{H:g}mm"

# ─────────────────────────── Assets ───────────────────────────
def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()

def font_face(name, file, weight, style="normal"):
    return (f'@font-face{{font-family:"{name}";src:url(data:font/ttf;base64,'
            f'{b64(HERE/"assets/fonts"/file)}) format("truetype");'
            f'font-weight:{weight};font-style:{style};}}')

FONTS = "\n".join([
    font_face("Lato", "Lato-Light.ttf", 300),
    font_face("Lato", "Lato-Regular.ttf", 400),
    font_face("Lato", "Lato-Italic.ttf", 400, "italic"),
    font_face("Lato", "Lato-Bold.ttf", 700),
    font_face("Lato", "Lato-Black.ttf", 900),
])

LOGO_SVG = (HERE / "assets/logo-vertical-blanco.svg").read_text()
LOGO_SVG = re.sub(r"<\?xml[^>]*\?>", "", LOGO_SVG)
LOGO_URI = "data:image/svg+xml;base64," + base64.b64encode(LOGO_SVG.encode()).decode()

def qr_data_uri(text: str, color="#1B1464") -> str:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=24, border=0)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(image_factory=PilImage, fill_color=color, back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

QR_URI = qr_data_uri(EVENTO["url_qr"])

def svg_uri(path: Path, color=None) -> str:
    svg = path.read_text()
    if color:
        svg = svg.replace("#FFFFFF", color)
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

# Llama LAI (marca/elementos): patrón de fondo en contorno, gran escala, 12–24 % de opacidad;
# la versión sólida solo como icono pequeño.
LLAMA_CONTORNO_URI = svg_uri(HERE / "assets/llama-contorno-blanco.svg")
LLAMA_SOLIDA_NAVY_URI = svg_uri(HERE / "assets/llama-blanco.svg", color="#1B1464")

# ─────────────────────────── CSS ───────────────────────────
CSS = f"""
{FONTS}
:root{{
  --navy:#1B1464; --indigo:#09052C; --azul:#3640D7; --electrico:#4E57FF;
  --cian:#00F6E3; --teal:#4AF1D2; --peri:#8D89F7; --lila:#D2D2FC;
  --negro:#0A0A12; --blanco:#FFFFFF; --gris-medio:#6A6F9E; --gris-linea:#DBDCE5;
}}
*{{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
html,body{{margin:0;padding:0;background:#fff;font-family:"Lato","Helvetica Neue",Arial,sans-serif;}}

.card{{
  width:{W}mm;height:{H}mm;position:relative;overflow:hidden;
  font-family:"Lato",sans-serif;
}}

/* ───────── FRENTE ───────── */
.front{{
  color:var(--blanco);
  background:
    radial-gradient(78% 58% at 90% 36%, rgba(78,87,255,.78) 0%, rgba(78,87,255,0) 62%),
    radial-gradient(70% 50% at 100% 100%, rgba(27,20,100,.85) 0%, rgba(27,20,100,0) 60%),
    linear-gradient(112deg, #0A0A12 0%, #09052C 24%, #1B1464 50%, #3640D7 82%, #3038CF 100%);
}}
.front .llama{{
  position:absolute; right:{-0.30*W:.2f}mm; top:{-0.06*H:.2f}mm; height:{1.22*H:.2f}mm; width:auto;
  opacity:.20; pointer-events:none;
}}
.front .rol{{
  position:absolute; left:{9.6*S:.2f}mm; top:{HOLE_ZONE + 4*S:.1f}mm;
  writing-mode:vertical-rl; transform:rotate(180deg);
  font-weight:400; font-size:{4.6*S:.2f}mm; letter-spacing:.38em; line-height:1;
  color:var(--lila); white-space:nowrap;
}}
.front .logo{{
  position:absolute; right:{10*S:.2f}mm; top:{HOLE_ZONE + 3.5*S:.1f}mm; width:{26*S:.2f}mm; height:auto; display:block;
}}
.front .bloque{{
  position:absolute; left:{17*S:.2f}mm; right:{9*S:.2f}mm; top:{H*0.443:.2f}mm; text-align:center;
}}
.front .pill{{
  display:inline-block; background:var(--peri); color:var(--navy);
  font-weight:700; font-size:{2.45*S:.2f}mm; letter-spacing:.17em; line-height:1;
  padding:{1.25*S:.2f}mm {3.4*S:.2f}mm {1.15*S:.2f}mm; border-radius:99mm; margin-bottom:{3.4*S:.2f}mm;
}}
.front h1{{
  margin:0; font-weight:700; font-size:{7.35*S:.2f}mm; line-height:1.12; letter-spacing:-.005em;
}}
.front h1 .l2{{ display:block; font-weight:400; color:var(--teal); }}
.front .sub{{
  margin:{1.4*S:.2f}mm 0 0; font-style:italic; font-weight:400; font-size:{4.3*S:.2f}mm; line-height:1.2;
}}
.front .sub b{{ font-weight:700; }}
.front .persona{{
  position:absolute; left:{12*S:.2f}mm; right:{9*S:.2f}mm; bottom:{H*0.103:.2f}mm;
}}
.front .nombre{{
  font-weight:700; font-size:{5.3*S:.2f}mm; letter-spacing:.2em; line-height:1.22; color:#EEEDFF;
}}
.front .nombre.dos{{ font-size:{4.9*S:.2f}mm; }}
.front .fecha{{
  margin-top:{2.2*S:.2f}mm; font-weight:400; font-size:{3.55*S:.2f}mm; letter-spacing:.2em; color:#B9B7FA;
}}

/* ───────── REVERSO ───────── */
.back{{ background:#fff; color:var(--navy); }}
.back .llama-icon{{
  position:absolute; left:50%; top:{HOLE_ZONE + 3.5*S:.1f}mm; transform:translateX(-50%);
  height:{9*S:.2f}mm; width:auto;
}}
.back .marco{{
  position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
  width:{56*S:.2f}mm; height:{56*S:.2f}mm; border:{1.35*S:.2f}mm solid var(--navy); border-radius:{4.2*S:.2f}mm;
}}
.back .scan{{
  position:absolute; left:50%; top:{-4.2*S:.2f}mm; transform:translateX(-50%);
  background:#fff; padding:0 {2.6*S:.2f}mm; font-weight:900; font-size:{6.6*S:.2f}mm; line-height:1;
  letter-spacing:.04em; white-space:nowrap; color:var(--navy);
}}
.back .qr{{
  position:absolute; left:50%; top:52%; transform:translate(-50%,-50%);
  width:{40*S:.2f}mm; height:{40*S:.2f}mm; image-rendering:pixelated;
}}
.back .url{{
  position:absolute; left:0; right:0; bottom:{H*0.107:.2f}mm; text-align:center;
  font-weight:400; font-size:{3.55*S:.2f}mm; letter-spacing:.06em; color:var(--gris-medio);
}}

/* ───────── PDF 100×150 ───────── */
@media print {{
  .single .card{{ page-break-after:always; break-after:page; }}
}}
.single .card{{ page-break-after:always; }}

/* ───────── Imposición Carta 2-up ───────── */
.sheet{{
  width:{LETTER_W}mm; height:{LETTER_H}mm; position:relative; overflow:hidden; background:#fff;
  page-break-after:always; break-after:page;
}}
.sheet .slot{{ position:absolute; }}
.crop{{ position:absolute; background:#000; }}
.crop.h{{ height:.18mm; width:3mm; }}
.crop.v{{ width:.18mm; height:3mm; }}
.sheet .nota{{
  position:absolute; left:4mm; top:{LETTER_H/2:.1f}mm; transform:translateY(-50%) rotate(180deg);
  writing-mode:vertical-rl; white-space:nowrap;
  font-size:2.4mm; color:#9a9db8; letter-spacing:.08em;
}}
"""

# ─────────────────────────── HTML ───────────────────────────
def front_html(rol, lineas):
    cls = "nombre dos" if len(lineas) > 1 else "nombre"
    nombre = "<br>".join(lineas)
    return f"""
<div class="card front">
  <img class="llama" src="{LLAMA_CONTORNO_URI}" alt="">
  <div class="rol">{rol}</div>
  <img class="logo" src="{LOGO_URI}" alt="Longevity Academic Institute">
  <div class="bloque">
    <div class="pill">{EVENTO['eyebrow']}</div>
    <h1>{EVENTO['titulo_1']}<span class="l2">{EVENTO['titulo_2']}</span></h1>
    <p class="sub">{EVENTO['sub_pre']}<b>{EVENTO['sub_bold']}</b></p>
  </div>
  <div class="persona">
    <div class="{cls}">{nombre}</div>
    <div class="fecha">{EVENTO['fecha']}</div>
  </div>
</div>"""

def back_html():
    return f"""
<div class="card back">
  <img class="llama-icon" src="{LLAMA_SOLIDA_NAVY_URI}" alt="">
  <div class="marco"><div class="scan">SCAN ME</div></div>
  <img class="qr" src="{QR_URI}" alt="QR">
  <div class="url">{EVENTO['url_texto']}</div>
</div>"""

def crop_marks(x, y):
    """Marcas de corte alrededor de una escarapela ubicada en (x, y) mm dentro de la hoja."""
    m = []
    for cx in (x, x + W):
        for cy in (y, y + H):
            # horizontales (fuera del área, a izquierda/derecha)
            m.append(f'<div class="crop h" style="left:{cx-4:.2f}mm;top:{cy:.2f}mm"></div>')
            m.append(f'<div class="crop h" style="left:{cx+1:.2f}mm;top:{cy:.2f}mm"></div>')
            # verticales (arriba/abajo)
            m.append(f'<div class="crop v" style="left:{cx:.2f}mm;top:{cy-4:.2f}mm"></div>')
            m.append(f'<div class="crop v" style="left:{cx:.2f}mm;top:{cy+1:.2f}mm"></div>')
    return "".join(m)

def page(body, size):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Escarapelas LAI</title>
<style>@page{{size:{size};margin:0;}}{CSS}</style></head><body>{body}</body></html>"""

def build_single():
    cards = "".join(front_html(r, n) + back_html() for r, n in PERSONAS)
    return page(f'<div class="single">{cards}</div>', f"{W}mm {H}mm")

def slot_positions():
    """Posiciones (x, y) en mm de cada escarapela en la hoja Carta, centradas."""
    x0 = (LETTER_W - COLS * W - (COLS - 1) * GAP) / 2
    y0 = (LETTER_H - ROWS * H - (ROWS - 1) * GAP) / 2
    return [(x0 + c * (W + GAP), y0 + r * (H + GAP)) for r in range(ROWS) for c in range(COLS)]

def build_letter():
    per = COLS * ROWS
    pos = slot_positions()
    marks = "".join(crop_marks(x, y) for x, y in pos)
    sheets = []
    groups = [PERSONAS[i:i + per] for i in range(0, len(PERSONAS), per)]
    for k, grp in enumerate(groups, 1):
        fronts = "".join(
            f'<div class="slot" style="left:{pos[j][0]:.2f}mm;top:{pos[j][1]:.2f}mm">{front_html(r, n)}</div>'
            for j, (r, n) in enumerate(grp))
        sheets.append(f'<div class="sheet">{fronts}{marks}'
                      f'<div class="nota">HOJA {k} · FRENTE · {W:g} × {H:g} mm · cortar por las marcas</div></div>')
        # Reverso espejado horizontalmente (dúplex volteando por el borde largo).
        # Los reversos son idénticos, así que el espejo solo garantiza la correspondencia.
        backs = ""
        for j in range(len(grp)):
            r, c = divmod(j, COLS)
            jm = r * COLS + (COLS - 1 - c)
            backs += f'<div class="slot" style="left:{pos[jm][0]:.2f}mm;top:{pos[jm][1]:.2f}mm">{back_html()}</div>'
        sheets.append(f'<div class="sheet">{backs}{marks}'
                      f'<div class="nota">HOJA {k} · REVERSO</div></div>')
    return page("".join(sheets), "215.9mm 279.4mm")

def slug(lineas):
    s = " ".join(lineas).lower()
    s = re.sub(r"[áà]", "a", s); s = re.sub(r"[éè]", "e", s); s = re.sub(r"[íì]", "i", s)
    s = re.sub(r"[óò]", "o", s); s = re.sub(r"[úù]", "u", s); s = s.replace("ñ", "n")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

# ─────────────────────────── Render ───────────────────────────
def render():
    from playwright.sync_api import sync_playwright

    single_html = OUT / f"escarapelas_{TAG}.html"
    letter_html = OUT / f"escarapelas_carta_{COLS*ROWS}up_{TAG}.html"
    single_html.write_text(build_single(), encoding="utf-8")
    letter_html.write_text(build_letter(), encoding="utf-8")

    chrome = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome if os.path.exists(chrome) else None)
        ctx = browser.new_context(device_scale_factor=3, viewport={"width": 800, "height": 1200})
        pg = ctx.new_page()

        pg.goto(single_html.as_uri()); pg.wait_for_load_state("networkidle"); pg.emulate_media(media="print")
        pg.pdf(path=str(OUT / f"escarapelas_{TAG}.pdf"), prefer_css_page_size=True,
               print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})

        # Previews PNG (frente de cada persona + reverso)
        pg.emulate_media(media="screen")
        cards = pg.locator(".card")
        n = cards.count()
        for i in range(n):
            idx = i // 2
            rol, lineas = PERSONAS[idx]
            if i % 2 == 0:
                name = f"{idx+1:02d}_{slug(lineas)}_frente.png"
            else:
                if idx > 0:
                    continue
                name = "00_reverso.png"
            cards.nth(i).screenshot(path=str(PREV / f"{TAG}_{name}"))

        pg.goto(letter_html.as_uri()); pg.wait_for_load_state("networkidle")
        pg.locator(".sheet").nth(0).screenshot(path=str(PREV / f"{TAG}_hoja1_frente.png"))
        pg.locator(".sheet").nth(1).screenshot(path=str(PREV / f"{TAG}_hoja1_reverso.png"))
        pg.emulate_media(media="print")
        pg.pdf(path=str(OUT / f"escarapelas_carta_{COLS*ROWS}up_{TAG}.pdf"), prefer_css_page_size=True,
               print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        browser.close()

    print("OK →", OUT)

if __name__ == "__main__":
    render()
