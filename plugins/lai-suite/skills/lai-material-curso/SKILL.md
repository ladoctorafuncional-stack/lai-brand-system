---
name: lai-material-curso
description: "Produce el material académico del Longevity Academic Institute (LAI) — la academia de la Dra. Carolina Rodríguez Morales. Usa este skill SIEMPRE que se pida un compendio o libro de módulo, un cuadernillo de casos clínicos, una portada de compendio, un syllabus o temario, un handout, una guía de estudio, un certificado o diploma, una escarapela de asistente, una hoja membreteada, una carta institucional, un comunicado en papel de la academia, o una presentación de clase. Dispara con: compendio, libro del módulo, cuadernillo, portada, syllabus, temario, handout, certificado, diploma, constancia, membrete, carta, comunicado, deck de clase. El diseño sale 100% de lai-design-system. El contenido clínico se reproduce VERBATIM. NO es para la clínica LCI."
---

# Material académico — LAI

Carga `lai-design-system` y trabaja sobre `brand.py`.

## 1. Portada de compendio / cuadernillo

Una llamada resuelve la portada completa:

```python
im = portada_compendio(
    antetitulo = 'COMPENDIO ACADÉMICO DE',
    titulo_1   = 'Medicina Peptídica y',
    titulo_2   = 'Bioregulación Celular.',
    coletilla  = 'en escenarios clínicos reales',
    bloque     = 'Módulo 12',
    descriptor    = 'Eje Sexual, Libido y Regulación Hormonal.',
    descriptor_it = 'Neuroendocrinología del Deseo, Fertilidad y Rendimiento Íntimo.',
    formato    = 'a4')
guardar(im, 'portada-modulo-12.png')
```

Variantes del antetítulo según la pieza:
- `COMPENDIO ACADÉMICO DE` → libro de módulo (uno por cada uno de los 12 módulos)
- `FORMACIÓN ACADÉMICA EN` + `etiqueta='CUADERNILLO DE CASOS CLÍNICOS'` → cuadernillo de casos

Invariantes de la portada: la segunda línea del título **siempre** en teal `#4AF1D2`; la coletilla en Lato light italic con la última palabra en bold italic; el número de módulo alineado a la derecha en teal sobre un filete lila; la autoría en versalitas espaciadas al pie.

## 2. Hoja membreteada y cartas

```python
im, util = membrete('carta')       # util = (x0, y0, x1, y1) del área de contenido
x0, y0, x1, y1 = util
y = parrafo(im, (x0, y0), cuerpo, F('lato','regular',34), 'gris_texto',
            ancho_max=x1-x0, interlinea=1.55)
```

La banda superior lleva gradiente horizontal `indigo_hondo → navy → azul` y el logo blanco (v2) a la derecha. El pie legal va alineado a la derecha en navy, dos líneas.

Estructura de carta institucional: fecha · destinatario · asunto en negrita · cuerpo · despedida · firma de la Dra. Carolina (`logo('firma')`, ancho 380 px) · nombre y cargo debajo.

## 3. Certificados y diplomas

```python
im = lienzo('certificado')
im.paste(degradado(im.size, 'boveda'), (0, 0))       # Manual v2: Bóveda = certificados, diplomas, actas
marco_oro(im, margen=110, grosor=6, radio=14)         # oro de seis paradas: permitido en filetes de certificado
poner_logo(im, 'horizontal-blanco', im.width//2, 260, ancho=900, anclaje='cm')
texto(im, (im.width//2, 620), 'CERTIFICADO DE APROBACIÓN',
      F('lato','light',72), 'lila', anclaje='ma', espaciado=12)
texto(im, (im.width//2, 900), nombre, F('lato','bold',130), 'blanco', anclaje='ma')
# ... cuerpo, horas, fecha
poner_logo(im, 'firma-blanco', im.width//2 - 700, im.height-560, ancho=420, anclaje='cm')
```

Elementos obligatorios: fondo `boveda` (variante clara: `papel` con logo `horizontal-navy` y texto navy), filete dorado doble, logo v2, nombre completo del egresado, nombre exacto del programa, intensidad horaria, ciudad y fecha, firma de la directora, y los sellos de aval (Florida Global University y CEL) al pie. **Confirma siempre con la doctora el nombre del programa, la intensidad horaria y los avales antes de emitir** — han variado entre versiones del material.

## 4. Syllabus y handouts

Sobre `membrete()`. Jerarquía: título del módulo en Lato bold 44 navy · epígrafes de sección en Helvetica bold 30 azul · cuerpo Lato regular 30 gris_texto interlínea 1.55 · viñetas con `vinetas()` · cajas de énfasis con `perla_clinica()` para las reglas de decisión.

Un syllabus de módulo lleva: nombre y número · objetivos de aprendizaje · contenidos por sesión · metodología · evaluación · bibliografía (formato de `lai-evidencia`) · intensidad horaria.

## 5. Escarapelas

`lienzo('escarapela')`. Doble logo LAI \| LCI arriba separados por filete vertical · retrato en `mono_azul()` · nombre en azul eléctrico Lato bold · credenciales en viñetas ✦ · QR de contacto · arco índigo inferior con la instrucción de escaneo.

## 6. Presentaciones

`lienzo('slide')` 1920×1080 para PNG sueltos. Para un deck completo en PPTX, lee la skill `pptx` **después** de tener el contenido, y aplica la paleta y las fuentes de LAI. Portada de deck:

- Con docente: `portada_docente(...)`, con su foto recortada B/N y sus avales.
- Sin docente: `portada_compendio` en formato `slide`.

Las slides interiores se montan sobre `fondo_slide('diagonal' | 'llama' | 'malla' | 'escudo')`. Alterna los fondos a lo largo del deck.

La agenda replica `references/piezas-maestras/slides/agenda.jpg`. Antes de armar un deck, abre las piezas maestras de `references/piezas-maestras/slides/`.

## Reglas duras

1. **Verbatim.** Todo contenido clínico de la doctora se reproduce exacto. Nunca resumir, reinterpretar, corregir ni completar.
2. Cifras y unidades verificadas contra la fuente. Las conversiones mg↔µg pasan por `lai-evidencia`.
3. Bibliografía en el formato de `lai-evidencia`, con DOI o PMID reales.
4. Pie legal y año en toda página de documento.
5. Bilingüe: se produce una versión completa por idioma, nunca mezclado.
6. Datos institucionales que deben confirmarse antes de imprimir: número de módulos, intensidad horaria, avales vigentes y fechas.

## Verificación

Renderiza a 300 dpi, abre el resultado y revisa: márgenes de impresión (mínimo 10 mm), acentos, nada pisado, filete dorado completo en los cuatro lados, firma legible, sellos presentes.

## Reglas de lectura y márgenes (10-oct-2026)
Toda pieza que se publique o proyecte (portada, flyer, slide, certificado para redes) respeta `lai-piezas-graficas/references/correcciones-2026-10-10/REGLAS-10-OCT-2026.md`: zona segura del 10 % del lado más corto, logo horizontal ≈34 % W en piezas de redes, cuerpo legible (≥27 px a 1080 de ancho o proporcional), contraste ≥4.5:1, recuadros simétricos e interlineado de bloque uniforme. En impresos sigue el margen de 10 mm o más.
