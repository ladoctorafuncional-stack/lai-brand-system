# Escarapelas · Graduación «Medicina Peptídica y Bioregulación Celular»

**Longevity Academic Institute · 26 de septiembre de 2026**
Estado: `validado_localmente`

## Entregables (`out/`)

| Archivo | Uso |
|---|---|
| `escarapelas_100x150mm.pdf` | 24 páginas a tamaño real (frente + reverso por persona). Para imprimir directo en 10 × 15 cm o enviar a litografía. |
| `escarapelas_carta_2up.pdf` | 12 hojas Carta, 2 escarapelas por hoja con marcas de corte. Frente y reverso alternados: imprimir a doble cara **volteando por el borde largo**. |
| `preview/*.png` | Vista previa de cada frente, el reverso y la hoja Carta 1. |

## Especificaciones

- Tamaño: **100 × 150 mm** (escarapela vertical estándar para porta-carnet / cordón).
- **Franja superior de 14 mm libre** en frente y reverso para ojalete o perforación: el logo empieza a 17,5 mm del borde y no hay texto en esa zona.
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
python3 build.py
```

Nombres, roles, fecha, título y URL del QR se editan en la cabecera de `build.py`
(`EVENTO` y `PERSONAS`). Cada nombre se define por líneas para controlar el corte.
