---
name: lai-design-system
description: "Sistema de diseño maestro del Longevity Academic Institute (LAI), la academia médica de la Dra. Carolina Rodríguez Morales. Motor único de marca para TODA pieza visual y documento de la academia, alineado al Manual de Marca LAI v2 (logotipo v2 con llama, 21 tokens de color, Lato + Helvetica/Arimo, 27 iconos, recuadro biselado, degradados oficiales y fichas de infografía). Úsalo SIEMPRE que se construya cualquier material de LAI para que el resultado sea idéntico al estándar de marca. Es invocado por lai-infografia-modulo, lai-piezas-graficas y lai-material-curso. IMPORTANTE: LAI es una marca SEPARADA de Longevity Clinical Institute (LCI); nunca mezclar sus paletas, tipografías ni logos."
---

# Sistema de diseño · Longevity Academic Institute (Manual v2)

La fuente de verdad es el **Manual de Marca LAI v2**. Si una pieza maestra antigua contradice el manual, gana el manual.

## 0. LAI no es LCI

| | Longevity **Academic** Institute (LAI) | Longevity **Clinical** Institute (LCI) |
|---|---|---|
| Qué es | La academia: cursos, módulos, certificaciones | La clínica: pacientes, planes, historias |
| Tipografías | **Lato + Helvetica** (Arimo como sustituto libre) | Poppins + Mencken Std |
| Color | Navy `#1B1464` · azul `#3640D7` · cian `#00F6E3` | Navy `#2A3649` · gold `#D2B58A` |
| Logo | Escudo cuatripartito de punta (L · llama · A · I) en oro + wordmark | Wordmark tipográfico |
| Skill | **este** | `lci-design-system` |

Nunca se mezclan paletas, tipografías ni logos. **El logo de LCI nunca aparece en material de LAI.** Un encargo clínico (paciente, plan, historia) no es de este skill.

## 1. Cómo se usa

Todo se construye en Python con Pillow (y numpy para las mallas) sobre `assets/brand.py`.

```python
import sys; sys.path.insert(0, '<ruta_del_skill>/assets')
from brand import *

im = lienzo('story')                          # 1080x1920
fondo_profundo(im)                            # malla profunda + patrón de llama + grano
poner_logo(im, 'horizontal-blanco', im.width // 2, 90, ancho=300, anclaje='ct')
texto(im, (90, 700), 'Medicina peptídica', F('lato', 'bold', 70), 'blanco')
texto(im, (90, 790), 'Mecanismo de acción', F('lato', 'bold', 44), 'teal')
guardar(im, 'salida.png')
```

No escribas colores, tamaños ni rutas a mano: **todo sale de `brand.py`**. Si una pieza pide un color fuera de la paleta, no lo inventes: pregunta.

## 2. Paleta oficial: 21 tokens

**Fuera de esta lista no hay color LAI.**

| Token | HEX | Uso |
|---|---|---|
| `navy` | `#1B1464` | H1, bandas, wordmark |
| `indigo_hondo` | `#09052C` | Fondos profundos |
| `azul` | `#3640D7` | Secciones, iconos, resplandor sobre índigo hondo |
| `azul_electrico` | `#4E57FF` | H2 sobre claro, CTA, filete del recuadro biselado |
| `cian` | `#00F6E3` | Acento: filete de cifras, subrayado de término técnico |
| `periwinkle` | `#8D89F7` | H3 |
| `lila` | `#D2D2FC` | Captions |
| `periwinkle_cl` | `#9D9DFF` | Apoyo |
| `teal` | `#4AF1D2` | H2 sobre oscuro |
| `menta` | `#B7FFF8` | Énfasis sobre oscuro |
| `gris_fondo` | `#F6F6F6` | Fondo claro |
| `gris_linea` | `#DBDCE5` | Filetes y divisores |
| `gris_texto` | `#4D4D4D` | Cuerpo sobre claro |
| `rojo` | `#FF3131` | **Solo alerta** de seguridad del paciente |
| `blanco` | `#FFFFFF` | |
| Oro (6 paradas) | `#F6EABF → #D1BA80 → #896B38 → #BB9E66 → #D1BA80 → #8A6C39` | Ver abajo |

**El oro: solo el escudo, y nunca plano.** Siempre con las seis paradas (`GRAD_ORO`). Un degradado de dos paradas se lee bronce plano y está prohibido. Fuera del escudo, los filetes de certificado (`marco_oro`) y los sellos de aval, el oro no se usa.

**Fondos oscuros:** ninguno por debajo de saturación 70 %, porque un azul desaturado se lee lavanda. El resplandor va en `azul` sobre `indigo_hondo`.

Alias heredados de v1 (`indigo`, `azul_vivo`, `azul_cielo`, `lila_pal`, `cian_hondo`, `crema`, `gris_medio`, `negro`) siguen existiendo en `ALIAS_V1` para no romper código viejo, pero apuntan a tokens oficiales. **No los uses en piezas nuevas.**

## 3. Tipografía y jerarquía

Embebidas en `assets/fonts/`:

- **Lato:** titulares, cifras, versalitas. Pesos `thin, light, light_i, regular, italic, bold, bold_i, black`.
- **Helvetica → Arimo:** cuerpo. Pesos `regular, italic, medium, semibold, bold, bold_i`.

**Escalas** (`ESCALA_DOC_PT`, `ESCALA_INFO_PX`):

- Documento: 26 / 18 / 13 / 10.5 pt.
- Infografía: 70 / 44 / 32 / 27 px.

El cuerpo nunca baja de **24 px en infografía** ni de **9 pt en documento**. Máximo **tres niveles de encabezado** por pieza. H1 en Lato Bold. Los títulos de módulo en portada van en **Lato Light**, la única excepción al H1 Bold.

**Color por fondo** (`JERARQUIA['claro']` / `JERARQUIA['oscuro']`):

| Nivel | Fondo claro | Fondo oscuro |
|---|---|---|
| H1 | navy | blanco |
| H2 | azul eléctrico | teal |
| H3 | periwinkle | periwinkle |
| Cuerpo | Arimo regular, gris texto | Blanco pleno, **nunca rebajado con opacidad** |
| Énfasis fuerte | navy sólido | menta |
| Término técnico | subrayado cian (`subrayado_cian`) | subrayado cian |
| Remisión interna | enlace en azul | enlace en menta |

El subrayado cian es un filete de 5 px anclado bajo la línea de base con 7 px de aire. Un solo recurso de énfasis por frase. El antetítulo puede llevar un filete de oro.

## 4. Logotipo v2 y kit de logos

`assets/logos/`, todos con alfa. Son los del Manual v2.

| Nombre | Cuándo |
|---|---|
| `horizontal-navy` | Fondo claro: membrete, documentos, certificados |
| `horizontal-blanco` | Fondo oscuro: portadas, stories, bandas |
| `vertical-navy` / `vertical-blanco` | Formatos cuadrados o muy verticales |
| `escudo` | Escudo v3: punta inferior, llama en el cuadrante superior derecho |
| `wordmark-navy` / `wordmark-blanco` | Wordmark sin escudo |
| `firma` / `firma-blanco` | Firma de la Dra. Carolina para certificados (blanco sobre Bóveda) |

**Anatomía del wordmark.** Las tres piezas forman un bloque cerrado: nunca se reordenan, se separan ni se usan sueltas.

1. **LONGEVITY®:** serif original, intocable. Es un garalda de alto contraste; su clon libre más cercano es EB Garamond Bold. El original está kerneado a mano, así que **nunca se recompone con la fuente: se usa el PNG del kit.** El ® va volado a la derecha.
2. **Filete divisorio:** 1 px, al ancho exacto de LONGEVITY, a 9 % de la altura de LONGEVITY por debajo.
3. **ACADEMIC INSTITUTE:** Lato Regular en caja alta, cuerpo al 6 % del ancho del wordmark, tracking 0.371 em, llenando exactamente el ancho de LONGEVITY. Centrada, a 7 % de la altura de LONGEVITY bajo el filete.

En los lockups el escudo mide 1.58 veces la altura del bloque tipográfico. Aire mínimo alrededor del logo: la altura del escudo. Tamaño: 24–29 % del ancho en portadas e infografías, 11–13 % en pies. **Nunca** recolorear el escudo, deformarlo ni aplicarle sombra.

## 5. Elementos: la llama

**La llama sustituye al asterisco, que salió de la marca.** `asterisco()` ya no existe y lanza error.

`elemento(nombre, color, ancho|alto)` carga los elementos desde `assets/elementos/`, en SVG y en PNG navy y blanco:

- `llama-maciza`: sellos y remates.
- `llama-contorno`: patrón de fondo a gran escala, 12–22 % de opacidad.
- `escudo-silueta` y `escudo-linea` (cruz, L, A, I y llama en trazo): marca de agua por debajo del 12 %, o sello monolínea sobre foto.

`patron_lai(im, color, opacidad)` pone la llama de contorno como marca de agua. La opacidad se fuerza al rango 12–22 %.

`diamante()` se conserva como marca de viñeta.

## 6. Iconografía: 27 iconos

`assets/iconos/`, con `svg/` (`fill="currentColor"`), `azul/` y `blanco/` (PNG 512 px con fondo transparente). La lista completa está en `ICONOS`.

`icono(nombre, tam, color)` / `poner_icono(im, nombre, cx, cy, tam, color)`.

Reglas:

- Un solo color plano: **azul, navy o blanco**. Nunca oro, relleno ni degradado.
- Mínimo 24 px en pantalla y 6 mm en impreso.
- Para recolorear un SVG basta cambiar el atributo `color` del `<svg>`.
- `fgu-escudo` y `fgu-wordmark` son el aval de Florida Global University: van **en su color original** y solo donde el curso está avalado.

Iconos: molecula, jeringa-vial, jeringa-vial-2, jeringa, jeringa-reloj, frasco-pastillas, certificado, libros, docente, grupo, equipo-check, live, 24-7, reloj, reloj-dosis, calculadora, documento, historia-clinica, enlace-roto, enlace-roto-2, usuario-config, ciclo-engranaje, alerta, cerrar, no-tocar, credencial, perla.

## 7. Estilo gráfico

### 01 · Recuadro biselado: `recuadro_biselado(im, caja, tipo, titulo, cuerpo, u)`

| `tipo` | Filete | Uso |
|---|---|---|
| `nota` | Azul eléctrico | El recuadro estándar (nota de libro) |
| `dato` | Cian | Solo cifras del programa y resultados, **nunca** advertencias |
| `alerta` | Rojo | Solo seguridad del paciente: contraindicaciones, dosis techo, interacciones. Es la única entrada permitida para el rojo |

Construcción:

- Radio de 12 px.
- Filete de 4 px con puntas redondeadas, separado 18 px de arriba y de abajo.
- Relleno de blanco a `#F7F7FC`.
- Bisel con dos sombras interiores: blanca arriba-izquierda y navy al 13 % abajo-derecha.
- Asiento exterior mínimo. **Nada de sombras difusas grandes:** el recuadro se lee en relieve, no flotando.

`u` es la escala: 1 para pantalla @1x y ~3.1 para 300 dpi.

### 02 · Degradados: `degradado(tam, nombre)`

Reglas únicas: todas las paradas salen de la paleta, los halos van a transparente y nunca a blanco, y sobre fondo claro el texto pasa a navy. No hace falta usar toda la paleta.

| Familia | Nombres | Uso |
|---|---|---|
| Las dos aprobadas (favoritas) | `malla_profunda` | Portadas, stories, contraportadas |
| | `malla_clara` | Fichas, handouts, fondos de cita |
| Sobrias · académicas | `navy_profundo` | Bandas y portadas formales |
| | `boveda` | Certificados, diplomas, actas |
| | `luz_lateral` | Retratos, cubiertas de módulo |
| | `gris_academia` | Tablas, anexos, material interno |
| | `papel` | Documentos, guías, papelería |
| | `editorial_claro` | Citas, aperturas de capítulo |
| 2 colores | `navy_azul` | Cabeceras |
| | `indigo_azul` | Portadas sobrias |
| | `electrico_cian` | CTA, destacados |
| | `lila_menta` | Fichas claras |
| 3 colores | `azul_electrico_peri` | Separadores |
| | `navy_azul_cian` | Stories, banners |

Registro por tipo de pieza:

- Las sobrias se quedan en navy e índigo con un solo halo de azul contenido. Es el registro para certificados, documentos y cubiertas de módulo.
- Dos colores bastan para bandas y botones.
- Tres colores para piezas de redes.
- Las mallas quedan para portadas.

### 03 · Fichas de infografía: `ficha_infografia(im, caja, rotulo, pct, icono, titulo, cuerpo, estilo, u)`

- Panel con un degradado de la paleta.
- Encima, un recuadro blanco con el icono de marca en azul, el título en Lato Bold navy y el cuerpo en Arimo.
- El rótulo del paso y el anillo de avance (`anillo_avance`) van en blanco **sobre el extremo oscuro del degradado, nunca sobre el claro**.

### 04 · Fichas de dato: `ficha_dato(im, caja, rotulo, valor, …)` / `fichas_dato(im, y, pares, …)`

- Caja lila (o navy con borde azul sobre fondo oscuro) con rótulo en Lato Bold 24 (azul, tracking 3) y valor en Lato Bold 30 (navy).
- **La tinta va centrada**: el aire entre el borde superior y la primera letra es el MISMO que entre la última letra y el borde inferior. Se mide con `getbbox` de una referencia común (mayúsculas y cifras), de modo que las fichas de una misma fila comparten línea base aunque un valor tenga descendentes. Nunca centrar por la caja de la fuente ni con offsets fijos.
- Blanco sobre lila no se lee (1.5:1): sobre lila los textos van en azul y navy; si el valor debe ir en blanco, la ficha va en periwinkle o navy.

### 05 · Franja superior: `franja_superior(im, alto, paradas, angulo=0)`

- Franja de cabecera (logo + etiqueta) con degradado **horizontal** (índigo → navy → azul, u otro par de la paleta sin cian cuando el feed ya lo repite).
- Va **limpia**: sin la llama del patrón, sin fundido hacia la foto ni hacia el contenido. Se pinta después del fondo/patrón para taparlos.
- La foto va debajo con **borde recto** (sin `fundido='arriba'`), con el velo mínimo que permita leer el texto inferior; antes de pegar un mockup, recortar sus bordes blancos (`np.where(gris < 240)`).

### Componentes heredados (actualizados a v2)

| Función | Qué produce |
|---|---|
| `header_modulo(im, n, titulo)` | Banda navy + caja de módulo con borde cian + logo |
| `footer_lai(im, rotulo)` | Banda inferior: rótulo, logo y © con el nombre legal completo |
| `circulo_numero`, `vinetas`, `caption`, `pill`, `regla` | Piezas de infografía. El lead de viñeta va en navy |
| `perla_clinica(...)` | Callout menta con borde cian e icono `perla` |
| `tarjeta_icono(im, caja, titulo, items, icono_marca='molecula')` | Tarjeta con insignia degradada e icono de marca |
| `portada_compendio(...)` | Portada de compendio o cuadernillo (malla profunda) |
| `membrete(formato)` | Hoja membreteada; devuelve `(imagen, caja_util)` |
| `marco_oro(im, margen)` | Filete dorado de seis paradas para certificados |

## 8. Tratamiento de imagen y formatos

- `mono_azul(img)`: retrato institucional (por defecto para fotos de personas).
- `duotono` / `tritono`: piezas ceremoniales.
- `recorte_llenar`, `esquinas`, `velo`.
- Fotos de la Dra. Carolina en `assets/retratos/` (`RETRATOS`):
  - `grid`: collage de tres fotos.
  - `sentada`: traje blanco.
  - `bata`: bata blanca con fondo de madera.
  - `recorte`: la misma foto de bata, con fondo transparente.

  `retrato_recorte('recorte', mono=True)` devuelve el recorte en B/N con alfa. Es el formato de las portadas de docente.

Formatos de `lienzo()`: `story` 1080×1920 · `post` 1080×1080 · `carrusel` 1080×1350 · `infografia` 1125×2000 · `carta` · `a4` · `certificado` · `escarapela` · `slide` · `banner` · `firma`.

`guardar(im, ruta)` guarda a 300 dpi.

## 9. Datos fijos de la marca

- Nombre de uso: **Longevity Academic Institute®**. Nombre legal: **Longevity & Functional Medicine Academic Institute**.
- Tagline: *La excelencia contínua del pensamiento médico.*
- longevityacademicinstitute.com · @longevityacademicinstitute · WhatsApp (+57) 301 512 39 91
- Fundadora y directora médica: **Dra. Carolina Rodríguez Morales**.
- Pie legal: `© 2026 Longevity & Functional Medicine Academic Institute. Todos los derechos reservados.`
- **Programa insignia:** *Formación Académica en Medicina Peptídica y Bioregulación Celular, en escenarios clínicos reales*. 15 módulos teóricos · 45 lecciones · +40 horas · 2 días de práctica presencial en Medellín. El contenido está en ampliación: estas cifras pueden subir, nunca bajar. Confirma las cifras vigentes antes de publicarlas.
- Aval del curso: Florida Global University, solo donde el curso está avalado.

## 9b. Credenciales, fondos de slide y portada de docente

**Avales y credenciales** (`assets/avales/`, `aval()` / `poner_aval()`). Van **siempre en su color original**; nunca se recolorean ni se adaptan a la paleta LAI.

| Nombre | Uso |
|---|---|
| `kharrazian-blanco` | Kharrazian Institute sobre fondo oscuro |
| `kharrazian-color` | Kharrazian Institute sobre fondo claro |
| `kharrazian-laurel` | Escudo con laurel |
| `afmc` | Sello Advanced Functional Medicine Clinician (circular, con alfa) |
| `cfmc` | Sello Certified Functional Medicine Clinician (circular, con alfa) |

A cada docente se le ponen solo **sus** credenciales. Las de la Dra. Carolina son Kharrazian + CFMC + AFMC.

**Fondos de slide 1920×1080** (`fondo_slide(nombre)`). Vienen aprobados y con el logo ya colocado:

| Nombre | Composición |
|---|---|
| `diagonal` | Navy a azul en diagonal, logo abajo a la derecha |
| `llama` | Llama de contorno a la derecha, logo abajo a la izquierda |
| `malla` | Malla con halos, filete y logo abajo a la derecha |
| `escudo` | Escudo de línea como marca de agua, logo abajo a la izquierda |

Sobre ellos se escribe con la jerarquía de fondo oscuro.

**Portada de docente**: `portada_docente(nombre, bullets, antetitulo, titulo_1, titulo_2, coletilla, foto, avales)`.

Está medida en píxeles sobre la pieza aprobada `references/piezas-maestras/slides/portada-docente-carolina.jpg`:

- **Izquierda:** foto B/N recortada a sangre, con velo índigo que se funde hacia la derecha. Si no hay foto, el espacio queda libre.
- **Superior derecha:** logo al 24 % del ancho.
- **Encabezado:** filete de oro de 34 px y antetítulo en menta, espaciado.
- **Título:** Lato Light (80 px) + Lato Bold (80 px) con subrayado cian de 5 px al ancho exacto de la segunda línea.
- **Coletilla:** en cursiva lila, con la palabra final en negrita blanca.
- **Separación:** filete lila.
- **Docente:** rótulo «DIRIGIDO POR:», nombre en Lato Bold de 36 px y viñetas Arimo de 21 px con punto periwinkle. Un ítem que empieza con `+` continúa el anterior sin viñeta.
- **Credenciales:** a la derecha, Kharrazian arriba y los sellos debajo.
- **Fondo:** marca de agua del escudo de línea al 12 %.

El perfil del docente se reproduce **verbatim**.

Piezas maestras de slides en `references/piezas-maestras/slides/`:

- Portadas de docente (Dra. Carolina y Dr. Manuel Alejandro Calderón).
- Portada del curso de obesidad.
- Agenda. Es una tabla HORA / ACTIVIDAD: horas en teal Lato Bold, filetes lila, *Coffee Break* en cursiva con fila sombreada, y el título «Agenda» en Lato Bold con subrayado cian.
- Plantilla completa.

## ⭐⭐ Reglas de lectura y márgenes para piezas (10-oct-2026)
Toda pieza gráfica de LAI cumple `lai-piezas-graficas/references/correcciones-2026-10-10/REGLAS-10-OCT-2026.md`:
- Zona segura del 10 % del lado más corto (`margen(im)`).
- Logo horizontal ≈34 % del ancho.
- Cuerpo de 27 px o más, rótulos de 24 o más y pie de 20 o más (a 1080).
- Contraste de 4.5:1 o más (titulares de 7:1 o más), interlineado de bloque uniforme y recuadros simétricos.
- Feed con ritmo tonal (`assets/auditar_feed.py`).
- **Texto dentro de cualquier caja (fichas, pastillas, recuadros): la tinta se centra midiendo glifos (`getbbox`), con el mismo aire arriba y abajo; fichas en fila con la misma línea base** (15-oct-2026, `ficha_dato`). Regla obligatoria: la Dra. la ha repetido varias veces.
- Franjas de cabecera con degradado horizontal limpias (sin patrón ni fundidos); bordes blancos de mockups recortados antes de integrarlos (`franja_superior`).
- Degradados: no repetir el cian/menta en piezas consecutivas; rotar `luz_lateral`, `boveda`, `navy_profundo` y los de dos colores sin cian.

`guardar()` audita automáticamente los formatos sociales (story, post, carrusel, banner) con `auditar(im)`.

## 10. Verificación obligatoria

Antes de entregar, **renderiza y abre la pieza**. Revisa:

1. Ningún texto sale de su caja ni pisa otro elemento. El logo tiene su aire.
2. Solo colores de los 21 tokens. El oro va únicamente en escudo, filetes de certificado o sellos, y con sus seis paradas.
3. Llama, no asterisco. Logo v2 (escudo con llama), nunca el antiguo. Nunca el logo de LCI.
4. Máximo 3 niveles de encabezado y un solo recurso de énfasis por frase. El cuerpo no baja de 24 px ni de 9 pt.
5. Iconos en un solo color plano (azul, navy o blanco), de al menos 24 px.
6. El rojo aparece solo en seguridad del paciente y el cian solo en cifras.
7. Los acentos del español se ven bien (á é í ó ú ñ ü ¿ ¡).
8. Los documentos llevan el pie legal con el nombre legal completo.
