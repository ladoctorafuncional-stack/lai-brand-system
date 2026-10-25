---
name: lai-piezas-graficas
description: "Motor de diseño gráfico del Longevity Academic Institute (LAI) — la academia de la Dra. Carolina Rodríguez. Úsalo SIEMPRE que se pida crear, diseñar, diagramar o adaptar cualquier PIEZA GRÁFICA de la academia: Instagram story o post, carrusel, flyer, afiche, banner, portada, agenda de evento, cita, dato o estadística, invitación, aviso a alumnos, escarapela, carnet, firma de correo o pieza de convocatoria de curso. Dispara con \"diseña\", \"hazme una story\", \"post\", \"carrusel\", \"flyer\", \"banner\", \"pieza para Instagram\", \"agenda del evento\", \"escarapela\", \"diagrama esto con la marca de la academia\". Todo el material de marca está embebido (Lato + Helvetica/Arimo, kit de logos, paleta, piezas maestras). Resultado: PNG a 300 dpi. NO es para la clínica LCI ni para infografías de módulo (ese es lai-infografia-modulo)."
---

# Piezas gráficas — LAI

Carga `lai-design-system` y trabaja sobre `brand.py`. Nada se diseña "a ojo": la paleta, las fuentes y los componentes salen del motor.

## ⭐⭐ REGLAS DE LECTURA, MÁRGENES, CONTRASTE Y RITMO DEL FEED (10-oct-2026). Regla dura de la Dra.
Hay que leer `references/correcciones-2026-10-10/REGLAS-10-OCT-2026.md` y sus capturas anotadas antes de diseñar. Para LAI:
1. **Zona segura = 10 % del lado más corto, en los 4 lados** (`brand.margen(im)`; guías en `references/correcciones-2026-10-10/margenes/`): story, carrusel y post de 1080 → 108 px; banner 1200×630 → 63; portada 851×315 → 32. Esto **reemplaza** el «8 % del ancho». Solo el pie (@longevityacademicinstitute, la web, la cápsula) puede ir en la banda inferior, centrado y dentro de los márgenes laterales. Las piezas «Presentación» (01), «Bienvenido» (04) y la de la foto (14) fallaron por textos pegados al borde.
2. **Logo LAI horizontal ≈34 % del ancho** (31–37 %), el tamaño de «Nuestra visión» (10), en todas las piezas y variantes. En story y carrusel de 1080 son ≈367 px. El logo de la pieza 14 era demasiado pequeño.
3. **Piso tipográfico (a 1080 px), sin aplanar la jerarquía:** el piso solo lo usan el pie y los aclaratorios. Titular ≥ 2.4 × cuerpo, subtítulo 1.4–1.8 × cuerpo, nunca todos los textos del mismo tamaño. cuerpo de 27 px o más (= «Nuestra academia nace de una convicción», el mínimo aprobado; 10). Antetítulos y rótulos («NUESTRA VISIÓN»): 24 px o más, uno o dos tamaños más que antes. Pie y aclaratorios (*): 20 px o más, al pie (04: ese tamaño y esa ubicación están bien).
4. **Aprovechar el espacio** sin perder la jerarquía. **Interlineado de bloque uniforme** y **recuadros simétricos**.
5. **Contraste:** 4.5:1 o más. Titulares de 60 px o más: 7:1 o más. Sobre una foto cargada, se usan **soportes de lectura**: panel de vidrio opaco a media pieza o lámina vertical «tipo ducha» de alto completo (`velo()` + desenfoque), tarjeta de vidrio, resaltado que abrace el texto, cápsula o recuadro biselado. El color del logo depende de la pieza (versión blanca sobre oscuro, navy sobre claro), en una zona limpia o con una caída de luz natural de la foto (viñeta amplia de esquina, nunca una mancha local alrededor del logo). Nunca dentro de una cápsula o recuadro.
5b. **Resaltados más frecuentes:** al menos 1 lámina por carrusel y 1 de cada 3 piezas llevan un resaltado que abraza la palabra gancho, sin aire vertical, en la paleta LAI.
6. **Feed con ritmo tonal:** alternar oscuro y claro, como el carrusel «Nuestra visión», que es claro. Al menos 1 de cada 3 portadas clara y nunca 3 oscuras seguidas (`lai-design-system/assets/auditar_feed.py`).
7. **Auditoría:** `brand.guardar()` audita automáticamente los formatos sociales e imprime los fallos (F1 piso, F2 margen, F3 contraste, F7 logo). Si aparece algún fallo, no se entrega.
Referencias correctas para conservar: «Quiénes somos» (12) en tamaños, logo y distribución, y «Presentación» (01) en tamaño y jerarquía de los textos.

## Catálogo

| Pieza | Lienzo | Fondo | Estructura |
|---|---|---|---|
| Story de agenda | `story` | `fondo_profundo` | Logo arriba dcha · bloques de hora con pastilla periwinkle por sección · filete fino entre ítems |
| Story de convocatoria | `story` | `fondo_profundo` | Antetítulo versalita lila · titular Lato bold blanco + segunda línea teal · pastilla CTA azul eléctrico abajo |
| Post / cita | `post` | `fondo_profundo` o blanco | Comillas grandes periwinkle · frase en Lato light italic · firma de la doctora |
| Carrusel | `carrusel` | alterna oscuro/claro | Portada oscura, láminas interiores claras con `tarjeta_icono`, cierre con CTA |
| Flyer / afiche | `carta` | `fondo_profundo` | Igual que portada de compendio, con bloque de datos abajo |
| Banner web | `banner` | gradiente horizontal | Logo izq · titular · CTA dcha |
| Escarapela | `escarapela` | blanco + arco índigo | Doble logo LAI \| LCI arriba · nombre en azul eléctrico · credenciales en viñetas ✦ · QR · arco inferior |
| Firma de correo | `firma` | blanco | Logo horizontal navy · nombre · cargo · datos de contacto en `azul` |

## Story de agenda — la pieza más frecuente

Formato real de la marca (ver `references/piezas-maestras/story-agenda-*.jpg`):

```python
im = lienzo('story'); fondo_profundo(im, angulo=150)
poner_logo(im, 'horizontal-blanco', im.width-margen(im), margen(im), ancho=round(.34*im.width), anclaje='rt')

y = 320
for seccion, bloques in agenda:
    pill(im, (150, y), seccion, F('helv','bold',40),
         relleno='#8D89F7', color='azul', padx=26, pady=14, radio=10)
    y += 120
    for hora, quien, qué in bloques:
        texto(im, (150, y), hora, F('helv','regular',34), 'blanco')
        regla(im, 400, y+22, 520, 'gris_medio', 3)
        texto(im, (560, y-8), quien, F('helv','regular',34), 'blanco')
        texto(im, (560, y+34), qué,  F('helv','regular',34), 'blanco')
        y += 175
    y += 60
guardar(im, 'agenda.png')
```

Detalles que hacen que se vea de la marca: la pastilla de sección va en periwinkle `#8D89F7` con texto azul; el filete corto entre la hora y el contenido; el interlineado generoso; el patrón de polígonos apenas visible al fondo.

## Reglas

- **Jerarquía:** un solo titular por pieza. Si hay dos ideas, son dos piezas.
- **Contraste:** sobre `fondo_profundo`, el texto es blanco o teal; el periwinkle solo para antetítulos y etiquetas. Nunca cuerpo largo en teal.
- **Aire:** zona segura = 10 % del lado más corto en los 4 lados (`brand.margen(im)`, regla del 10-oct-2026). En las stories, además, ningún texto clave en los 200 px superiores ni en los 250 inferiores por la interfaz de Instagram.
- **Logo:** siempre presente, versión blanca sobre oscuro, navy sobre claro.
- **Sin emojis** en piezas institucionales.
- **Fotos de personas** siempre en `mono_azul()`.
- **Copy:** si hay que escribirlo, pásalo por `lai-marketing`. Este skill diagrama, no redacta.
- **Doble marca:** en escarapelas y piezas donde conviven LAI y LCI, van separados por un filete vertical, LAI a la izquierda, mismo alto óptico.

## Imágenes existentes

La doctora ya pagó una biblioteca de imágenes en Gamma. **Antes de generar cualquier imagen nueva**, consulta `references/gamma-biblioteca.md` en `lai-design-system` y reutiliza lo que ya existe.

## Verificación

Renderiza con `guardar()` (audita solo) y abre el PNG. Comprueba la salida del auditor (sin fallos) y además: nada pisado, acentos correctos, zonas seguras de Instagram respetadas, logo con aire, paleta LAI (no LCI).
