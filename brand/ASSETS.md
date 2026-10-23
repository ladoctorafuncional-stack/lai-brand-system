# Inventario de assets

## Logos LAI (V2, definitivos) · `logos/lai/`

Fuente: Drive › `LAI › 00_fuente_original › v2`. Cada familia viene en PNG + SVG y en tres tintas:
`-navy` (fondo claro), `-blanco` (fondo oscuro) y `-fondo-navy` (arte sobre placa navy, con 150 px de margen por lado).

| Familia | SVG (viewBox) | PNG | Fondo |
|---|---|---|---|
| `escudo` · `escudo-navy` · `escudo-blanco` | 1727×2348 | 1727×2348 | transparente |
| `logo-horizontal-navy` · `-blanco` | 2133×600 | 4266×1200 | transparente |
| `logo-horizontal-fondo-navy` | 2433×900 | 4866×1800 | placa navy opaca |
| `logo-vertical-navy` · `-blanco` | 1608×1356 | 3216×2712 | transparente |
| `logo-vertical-fondo-navy` | 2008×1756 | 4016×3512 | placa navy opaca |
| `wordmark-horizontal-navy` · `-blanco` | 1608×380 | 3216×760 | transparente |
| `wordmark-horizontal-fondo-navy` | 1852×624 | 3704×1248 | placa navy opaca |

Archivos auxiliares: `_oro.json` (rampa de 49 paradas del degradado oro del escudo) y `_vec.json` (datos vectoriales fuente).

## Logos de aliados · `logos/aliados/`

| Archivo | Tamaño (px) | Fondo |
|---|---|---|
| `longevity-clinical-institute-navy.png` · `-blanco.png` | 372×153 | transparente |
| `longevity-research-institute-navy.png` · `-blanco.png` | 365×153 | transparente |

## Credenciales y fotografía

| Archivo | Descripción | Tamaño (px) | Fondo |
|---|---|---|---|
| `credenciales/kharrazian-institute/logo-horizontal-navy.png` | Logo Kharrazian Institute, escudo + wordmark, tinta navy | 1600×2000 | transparente |
| `credenciales/kharrazian-institute/logo-horizontal-blanco.png` | Logo Kharrazian Institute, tinta blanca (para fondos oscuros) | 1600×2000 | transparente |
| `credenciales/kharrazian-institute/emblema-escudo-laurel-navy.png` | Emblema: escudo con llama + corona de laurel, sin texto | 1600×2000 | transparente |
| `credenciales/afmc/sello-afmc-advanced-functional-medicine-clinician.png` | Sello circular AFMC · Advanced Functional Medicine Clinician | 1600×2000 | transparente |
| `credenciales/cfmc/sello-cfmc-certified-functional-medicine-clinician.png` | Sello circular CFMC · Certified Functional Medicine Clinician | 1600×2000 | transparente |
| `fotografia/dra-carolina/collage-oficina-3-poses.png` | Collage de 3 retratos en consultorio (blazer blanco, beige, rosa) | 1600×2000 | transparente |
| `fotografia/dra-carolina/retrato-bata-blanca-brazos-cruzados.png` | Retrato de pie, bata blanca, brazos cruzados, fondo consultorio | 1600×2000 | opaco |
| `fotografia/dra-carolina/retrato-bata-blanca-brazos-cruzados-recorte.png` | Mismo retrato con fondo removido | 1600×2000 | transparente |
| `fotografia/dra-carolina/retrato-sentada-consultorio.png` | Retrato sentada en consultorio, traje blanco | 1600×2000 | opaco (bordes suaves) |

Cada logo y sello tiene además su variante `-trim.png`.

## Perfiles para redes · `perfiles/`

22 imágenes de perfil cuadradas, 2160×2160 PNG. Fuente: `LAI-perfiles_1-escudos.zip`
y `LAI-perfiles_2-logos-completos.zip` (copiadas byte a byte, nombres en minúsculas).
Patrón de nombre: `lai-perfil-NN_<logo>-<tinta>_<fondo>.png`.

| Carpeta | Archivos | Contenido |
|---|---|---|
| `escudos/` | 01–09 | Escudo solo: oro sobre malla profunda, navy, índigo-azul, blanco, malla clara; escudo blanco sobre azul eléctrico y navy-azul-cian; escudo navy sobre lila-menta y blanco |
| `logos-completos/` | 10–15 | Logo vertical: blanco sobre malla profunda, navy, azul eléctrico; navy sobre blanco, malla clara, editorial claro |
| `logos-completos/` | 16–19 | Logo horizontal: blanco sobre malla profunda, índigo-azul; navy sobre blanco, gris claro |
| `logos-completos/` | 20–22 | Wordmark: blanco sobre navy, navy-azul; navy sobre blanco |

## Material gráfico · `material-grafico/`

14 imágenes y 1 video de piezas producidas para la academia. Inventario y nombres
originales en `material-grafico/MATERIAL-GRAFICO.md`.

## Tipografía EB Garamond · `../fonts/eb-garamond/`

Descarga completa de Google Fonts: 2 variables (`wght`, normal e itálica) y 10
estáticas (Regular a ExtraBold, con itálicas). Licencia SIL Open Font License
(`OFL.txt`, debe acompañar siempre a las fuentes).

## Sitio web · `../sitio-web/`

Sitio publicado en `longevityacademicinstitute.com` (`CNAME`): `index.html`
(portada: "La excelencia contínua del pensamiento médico.") y `curso/index.html`
(página autocontenida de la Formación en Medicina Peptídica y Bioregulación
Celular, ~4 MB). Fuente: `LAI_brand_manual_location.zip`.

## Tipografías Lato y Arimo · `../fonts/`

- Lato (display): `lato-300.ttf` (Light), `lato-400.ttf` (Regular),
  `lato-400-italic.ttf`, `lato-700.ttf` (Bold), `lato-900.ttf` (Black).
- Arimo (cuerpo): `arimo-400.ttf`, `arimo-400-italic.ttf`, `arimo-700.ttf`.

Son los 8 archivos que declara `tokens/fonts.css`.

## Manual, componentes y páginas (Claude Design)

`../guidelines/Manual_de_Marca_LAI.dc.html`, `../components/type-jerarquia*.html`
y `../templates/paginas/`. Dependen de archivos del proyecto original que aún no
están en el repo; detalle en `../guidelines/README.md`.

## Pendientes de ingreso

- `tokens/fonts.css` apunta a `../marca/fonts/` (estructura del proyecto
  original); en este repo las fuentes están en `fonts/`.
- Dependencias `marca/…` del manual y las páginas (ver `../guidelines/README.md`).
