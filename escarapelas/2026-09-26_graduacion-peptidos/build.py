#!/usr/bin/env python3
"""
Escarapelas — Graduación «Medicina Peptídica y Bioregulación Celular»
Longevity Academic Institute · 26 de septiembre de 2026

Genera:
  out/escarapelas_100x150mm.pdf      → 1 página por cara (frente/reverso), tamaño real 100 × 150 mm
  out/escarapelas_carta_2up.pdf      → imposición en Carta (2 por hoja) con marcas de corte,
                                       lista para dúplex (voltear por el borde largo)
  out/preview/*.png                  → vista previa de cada frente + reverso

Uso:  python3 build.py
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
W, H = 100, 150            # tamaño escarapela
HOLE_ZONE = 14             # franja superior libre para perforación / ojalete
LETTER_W, LETTER_H = 215.9, 279.4
GAP = 6                    # separación entre las dos escarapelas en la hoja Carta

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
.front .rol{{
  position:absolute; left:9.6mm; top:{HOLE_ZONE + 4}mm;
  writing-mode:vertical-rl; transform:rotate(180deg);
  font-weight:400; font-size:4.6mm; letter-spacing:.38em; line-height:1;
  color:var(--lila); white-space:nowrap;
}}
.front .logo{{
  position:absolute; right:10mm; top:{HOLE_ZONE + 3.5}mm; width:26mm; height:auto; display:block;
}}
.front .bloque{{
  position:absolute; left:17mm; right:9mm; top:66.5mm; text-align:center;
}}
.front .pill{{
  display:inline-block; background:var(--peri); color:var(--navy);
  font-weight:700; font-size:2.45mm; letter-spacing:.17em; line-height:1;
  padding:1.25mm 3.4mm 1.15mm; border-radius:99mm; margin-bottom:3.4mm;
}}
.front h1{{
  margin:0; font-weight:700; font-size:7.35mm; line-height:1.12; letter-spacing:-.005em;
}}
.front h1 .l2{{ display:block; font-weight:400; color:var(--teal); }}
.front .sub{{
  margin:1.4mm 0 0; font-style:italic; font-weight:400; font-size:4.3mm; line-height:1.2;
}}
.front .sub b{{ font-weight:700; }}
.front .persona{{
  position:absolute; left:12mm; right:9mm; bottom:15.5mm;
}}
.front .nombre{{
  font-weight:700; font-size:5.3mm; letter-spacing:.2em; line-height:1.22; color:#EEEDFF;
}}
.front .nombre.dos{{ font-size:4.9mm; }}
.front .fecha{{
  margin-top:2.2mm; font-weight:400; font-size:3.55mm; letter-spacing:.2em; color:#B9B7FA;
}}

/* ───────── REVERSO ───────── */
.back{{ background:#fff; color:var(--navy); }}
.back .marco{{
  position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
  width:56mm; height:56mm; border:1.35mm solid var(--navy); border-radius:4.2mm;
}}
.back .scan{{
  position:absolute; left:50%; top:-4.2mm; transform:translateX(-50%);
  background:#fff; padding:0 2.6mm; font-weight:900; font-size:6.6mm; line-height:1;
  letter-spacing:.04em; white-space:nowrap; color:var(--navy);
}}
.back .qr{{
  position:absolute; left:50%; top:52%; transform:translate(-50%,-50%);
  width:40mm; height:40mm; image-rendering:pixelated;
}}
.back .url{{
  position:absolute; left:0; right:0; bottom:16mm; text-align:center;
  font-weight:400; font-size:3.55mm; letter-spacing:.06em; color:var(--gris-medio);
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
.sheet .slot{{ position:absolute; top:{(LETTER_H - H)/2:.2f}mm; }}
.sheet .slot.a{{ left:{(LETTER_W - 2*W - GAP)/2:.2f}mm; }}
.sheet .slot.b{{ left:{(LETTER_W - 2*W - GAP)/2 + W + GAP:.2f}mm; }}
.crop{{ position:absolute; background:#000; }}
.crop.h{{ height:.18mm; width:4mm; }}
.crop.v{{ width:.18mm; height:4mm; }}
.sheet .nota{{
  position:absolute; left:0; right:0; bottom:6mm; text-align:center;
  font-size:2.6mm; color:#9a9db8; letter-spacing:.08em;
}}
"""

# ─────────────────────────── HTML ───────────────────────────
def front_html(rol, lineas):
    cls = "nombre dos" if len(lineas) > 1 else "nombre"
    nombre = "<br>".join(lineas)
    return f"""
<div class="card front">
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
            m.append(f'<div class="crop h" style="left:{cx-5:.2f}mm;top:{cy:.2f}mm"></div>')
            m.append(f'<div class="crop h" style="left:{cx+1:.2f}mm;top:{cy:.2f}mm"></div>')
            # verticales (arriba/abajo)
            m.append(f'<div class="crop v" style="left:{cx:.2f}mm;top:{cy-5:.2f}mm"></div>')
            m.append(f'<div class="crop v" style="left:{cx:.2f}mm;top:{cy+1:.2f}mm"></div>')
    return "".join(m)

def page(body, size):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Escarapelas LAI</title>
<style>@page{{size:{size};margin:0;}}{CSS}</style></head><body>{body}</body></html>"""

def build_single():
    cards = "".join(front_html(r, n) + back_html() for r, n in PERSONAS)
    return page(f'<div class="single">{cards}</div>', f"{W}mm {H}mm")

def build_letter():
    xa = (LETTER_W - 2 * W - GAP) / 2
    xb = xa + W + GAP
    y = (LETTER_H - H) / 2
    sheets = []
    pairs = [PERSONAS[i:i + 2] for i in range(0, len(PERSONAS), 2)]
    for k, pair in enumerate(pairs, 1):
        fronts = "".join(
            f'<div class="slot {"a" if j == 0 else "b"}">{front_html(r, n)}</div>'
            for j, (r, n) in enumerate(pair))
        marks = crop_marks(xa, y) + crop_marks(xb, y)
        sheets.append(f'<div class="sheet">{fronts}{marks}'
                      f'<div class="nota">HOJA {k} · FRENTE · 100 × 150 mm · cortar por las marcas</div></div>')
        # Reverso: mismas posiciones (espejo para dúplex por borde largo; al ser idénticos no cambia nada)
        backs = "".join(f'<div class="slot {"a" if j == 0 else "b"}">{back_html()}</div>'
                        for j in range(len(pair)))
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

    single_html = OUT / "escarapelas_100x150mm.html"
    letter_html = OUT / "escarapelas_carta_2up.html"
    single_html.write_text(build_single(), encoding="utf-8")
    letter_html.write_text(build_letter(), encoding="utf-8")

    chrome = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome if os.path.exists(chrome) else None)
        ctx = browser.new_context(device_scale_factor=3, viewport={"width": 800, "height": 1200})
        pg = ctx.new_page()

        pg.goto(single_html.as_uri()); pg.wait_for_load_state("networkidle"); pg.emulate_media(media="print")
        pg.pdf(path=str(OUT / "escarapelas_100x150mm.pdf"), prefer_css_page_size=True,
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
            cards.nth(i).screenshot(path=str(PREV / name))

        pg.goto(letter_html.as_uri()); pg.wait_for_load_state("networkidle"); pg.emulate_media(media="print")
        pg.pdf(path=str(OUT / "escarapelas_carta_2up.pdf"), prefer_css_page_size=True,
               print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        browser.close()

    print("OK →", OUT)

if __name__ == "__main__":
    render()
