"""AUDITOR DE FEED — ritmo tonal de la cuadrícula (regla de la Dra., 10-oct-2026).

«El feed tiene que tener contraste: todo se está viendo muy oscuro, muy sombrío, monótono. Hay que respetar los tintes
de marca, pero las piezas no pueden verse monocromáticas: si todas son iguales, ninguna destaca.»

Uso:  python3 auditar_feed.py portada1.png portada2.png ...   (en ORDEN DE PUBLICACIÓN; la última es la más nueva)
      → informe + feed_qa.jpg (cuadrícula como se verá en Instagram, la más nueva arriba a la izquierda)

Reglas que revisa:
  T1  ≥ 1 de cada 3 portadas CLARAS (luminancia media ≥ 0.45: crema, blanco, azul claro, foto clara)
  T2  nunca 3 portadas oscuras seguidas (luminancia < 0.30)
  T3  en la cuadrícula, ninguna fila de 3 con las tres del mismo tono (todas oscuras o todas claras)
  T4  cada portada tiene un ACENTO de color de la paleta (dorado #D2B58A o azul claro #CAD3DD/#9fb2c6 con saturación
      visible, ≥ 0.4 % del área) — como los nodos y detalles de color de la pieza «The brain ages too» de Paola
  T5  vecinas (lado a lado o arriba/abajo) no comparten la misma familia de tono (diferencia de luminancia ≥ 0.08 o de matiz)
"""
import sys, colorsys
import numpy as np
from PIL import Image, ImageDraw

def perfil(path):
    im = Image.open(path).convert('RGB').resize((216, 270))
    a = np.asarray(im).astype(float) / 255
    lum = (0.2126*a[..., 0] + 0.7152*a[..., 1] + 0.0722*a[..., 2]).mean()
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in a.reshape(-1, 3)[::7]])
    gold = ((hsv[:, 0] > 0.07) & (hsv[:, 0] < 0.13) & (hsv[:, 1] > 0.22) & (hsv[:, 2] > 0.55)).mean()
    lblue = ((hsv[:, 0] > 0.53) & (hsv[:, 0] < 0.64) & (hsv[:, 1] > 0.12) & (hsv[:, 2] > 0.62)).mean()
    hue = np.median(hsv[hsv[:, 1] > 0.08, 0]) if (hsv[:, 1] > 0.08).any() else -1
    return dict(lum=lum, acento=max(gold, lblue), hue=hue)

def auditar(paths):
    P = [perfil(p) for p in paths]; f = []
    for i, p in enumerate(P):
        if p['acento'] < 0.004: f.append(f"T4 sin acento de color: {paths[i]}")
    oscuras = [p['lum'] < 0.30 for p in P]
    for i in range(len(P) - 2):
        if all(oscuras[i:i+3]): f.append(f"T2 tres oscuras seguidas: {paths[i]} … {paths[i+2]}")
        if not any(P[j]['lum'] >= 0.45 for j in range(i, i+3)): f.append(f"T1 sin portada clara en el tramo {i+1}–{i+3}")
    # cuadrícula: la más nueva arriba a la izquierda
    G = list(reversed(P)); names = list(reversed(paths))
    for r in range(0, len(G) - 2, 3):
        fila = G[r:r+3]
        if all(x['lum'] < 0.30 for x in fila) or all(x['lum'] >= 0.45 for x in fila):
            f.append(f"T3 fila {r//3+1} monótona: {[n.split('/')[-1] for n in names[r:r+3]]}")
    for i in range(len(G)):
        for j in (i+1, i+3):
            if j < len(G) and (j != i+1 or i % 3 != 2):
                if abs(G[i]['lum'] - G[j]['lum']) < 0.08 and (G[i]['hue'] < 0 or abs(G[i]['hue'] - G[j]['hue']) < 0.04):
                    f.append(f"T5 vecinas iguales: {names[i].split('/')[-1]} / {names[j].split('/')[-1]}")
    return f, P

def hoja(paths, out='feed_qa.jpg', s=240):
    names = list(reversed(paths)); rows = (len(names) + 2) // 3
    S = Image.new('RGB', (3*s + 4*6, rows*int(s*1.25) + (rows+1)*6), 'white'); d = ImageDraw.Draw(S)
    for i, n in enumerate(names):
        im = Image.open(n).convert('RGB').resize((s, int(s*1.25)))
        x, y = 6 + (i % 3)*(s+6), 6 + (i // 3)*(int(s*1.25)+6); S.paste(im, (x, y))
        p = perfil(n); d.rectangle([x, y, x+42, y+18], fill='white'); d.text((x+3, y+3), f"{p['lum']:.2f}", fill='black')
    S.save(out, quality=88); return out

if __name__ == '__main__':
    fl, _ = auditar(sys.argv[1:]); hoja(sys.argv[1:])
    print('OK' if not fl else f'{len(fl)} avisos'); [print('  ', x) for x in fl]
