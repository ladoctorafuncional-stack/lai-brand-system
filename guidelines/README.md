# Guidelines, componentes y páginas LAI (fuente Claude Design)

Archivos HTML del proyecto de diseño LAI, copiados byte a byte:

| Archivo en el repo | Contenido |
|---|---|
| `guidelines/Manual_de_Marca_LAI.dc.html` | Manual de marca LAI (brandbook) |
| `components/type-jerarquia.html` | Tarjeta "Jerarquía sobre claro" (H1/H2/H3/cuerpo) |
| `components/type-jerarquia-oscuro.html` | Misma tarjeta sobre fondo oscuro |
| `templates/paginas/Pantallas_LAI.dc.html` | "Seis pantallas del producto" |
| `templates/paginas/Pagina_7_LAI.dc.html` | Página 7 |

## ⚠️ No se ven solos todavía

Estos HTML referencian archivos del proyecto original con estructura `marca/…`,
que **no** vienen con la carga. Sin ellos, las imágenes, iconos y fuentes no
cargan. Faltan:

- **Runtime de Claude Design:** `doc-page.js`, `support.js` (junto a cada `.dc.html`)
  y `styles.css` (un nivel arriba de las tarjetas de `components/`).
- **`marca/elementos/`** (10): escudo-completo-contorno.svg, escudo-contorno.svg,
  filete-oro-fino.svg, filete-oro-grueso.svg, filete-oro-horizontal.svg,
  liston-avalado.png, llama-blanco.svg, llama-contorno-blanco.svg,
  llama-contorno.svg, llama.svg
- **`marca/iconos/`** (33): 29 en `azul/`, 3 en `blanco/`, whatsapp.png
- **`marca/fotos/`** (4): dra-carolina.jpg, fgu-fachada.jpg, pag7-fondo.png,
  sellos-formacion.jpg
- **`marca/logos/`**: `v2/` (7 SVG: escudo, logo horizontal y vertical,
  wordmark), `aliados/` (2 PNG), firma-carolina.png
- **`marca/video/`**: graduacion.mp4
- **`marca/fonts/`** (8): lato-300/400/400-italic/700/900 y arimo-400/400-italic/700

Varios de estos ya existen en el repo con otra ruta (p. ej. los logos V2 en
`brand/logos/lai/`, Lato en `fonts/`). Para que los HTML rendericen tal cual,
lo más fiel es subir la exportación completa del proyecto con su carpeta
`marca/`.
