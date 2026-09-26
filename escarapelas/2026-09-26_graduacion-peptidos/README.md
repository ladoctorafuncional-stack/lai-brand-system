# Escarapelas · Graduación «Medicina Peptídica y Bioregulación Celular»

**Longevity Academic Institute · 26 de septiembre de 2026**
Estado: `validado_localmente`

## Entregables (`out/`)

| Archivo | Uso |
|---|---|
| **`escarapelas_carta_4up_90x130mm.pdf`** | **Archivo para imprimir.** 6 hojas Carta, 4 escarapelas de 9 × 13 cm por hoja con marcas de corte. Frente y reverso alternados: imprimir a doble cara **volteando por el borde largo** (3 hojas físicas). |
| `escarapelas_90x130mm.pdf` | 24 páginas a tamaño real 9 × 13 cm (frente + reverso por persona), para litografía. |
| `escarapelas_carta_2up_100x150mm.pdf` · `escarapelas_100x150mm.pdf` | Variante 10 × 15 cm (2 por hoja Carta). |
| `preview/*.png` | Vista previa de cada frente, el reverso y la hoja Carta 1, por tamaño. |

## Especificaciones

- Tamaño: **90 × 130 mm** (escarapela vertical estándar; variante 100 × 150 mm disponible).
- **Franja superior libre** (12,6 mm en 9 × 13; 14 mm en 10 × 15) en frente y reverso para ojalete o perforación: ningún elemento la toca.
- Llama LAI (`marca/elementos/llama-contorno`) como patrón de fondo en contorno, gran escala, 20 % de opacidad, según guía `brand-llama`; llama sólida navy como icono en el reverso.
- Logo: kit v2 `marca/logos/v2/logo-vertical-blanco.svg` (escudo oro + wordmark blanco), sin redibujar.
- Tipografía: Lato (300 / 400 / 400 it / 700 / 900) embebida.
- Paleta: tokens LAI (`navy #1B1464`, `índigo #09052C`, `azul #3640D7`, `eléctrico #4E57FF`, `teal #4AF1D2`, `periwinkle #8D89F7`, `lila #D2D2FC`).
- Reverso: QR (navy) a `https://www.longevityacademicinstitute.com` + URL en texto.

## Roles

| Rol vertical | Personas |
|---|---|
| ESTUDIANTE | Eduard Caicedo Mondragón · Carmen Eduarda Medina Amorim · Marissa del Carmen Aparicio Polanco · Dahyanna Andrea Díaz Ospina · María Alejandra Lugo · Julieth Martinez Ocampo · María Mercedes Martínez Cadavid |
| STAFF LOGÍSTICO | Iván Velásquez · Maura Almanza · Manuela Legarda · Tibisay Araque |
| CONFERENCISTA | Dra. Carolina Rodríguez Morales |

## Regenerar

```bash
pip install playwright qrcode pillow
python3 build.py                                    # 9 × 13 cm, 4 por hoja Carta
python3 build.py --size 100x150 --cols 2 --rows 1   # 10 × 15 cm, 2 por hoja Carta
```

Nombres, roles, fecha, título y URL del QR se editan en la cabecera de `build.py`
(`EVENTO` y `PERSONAS`). Cada nombre se define por líneas para controlar el corte.
