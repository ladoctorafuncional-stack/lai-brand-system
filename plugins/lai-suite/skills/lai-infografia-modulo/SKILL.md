---
name: lai-infografia-modulo
description: "Construye las infografías de módulo y las guías rápidas de una página del Longevity Academic Institute (LAI), con el formato maestro de la academia. Usa este skill SIEMPRE que se pida una infografía, un resumen visual de módulo, una guía rápida, un one-pager clínico, un póster de buenas prácticas, un mapa de un tema del curso, o cuando se aporte contenido de un módulo para convertirlo en pieza visual. Formatos: infografía vertical de módulo (banda índigo, secciones numeradas, viñetas y Perla clínica) y one-pager de tarjetas. El diseño sale 100% del skill lai-design-system. El contenido clínico se reproduce VERBATIM. NO es para la clínica LCI."
---

# Infografías de módulo — LAI

Carga primero `lai-design-system` y trabaja sobre su `brand.py`.

## Dos formatos

**A. Infografía de módulo** (`lienzo('infografia')`, 1125×2000). Es la pieza insignia: una por módulo del programa.
**B. One-pager de tarjetas** (`lienzo('carta')`). Guía rápida de consulta, tipo "Buenas prácticas en Medicina Peptídica", en rejilla de 2 columnas con `tarjeta_icono`.

## Anatomía de la infografía de módulo

```
┌───────────────────────────────────────┐
│ BANDA ÍNDIGO (15% alto)               │  header_modulo()
│  ┌──────────┐          [logo blanco]  │  caja cian: "Módulo N"
│  │ Módulo 7 │                         │  subtítulo periwinkle
│  └──────────┘                         │
│  Nombre del módulo                    │
├───────────────────────────────────────┤
│ FONDO gris_fondo #F6F6F6              │
│                                       │
│ (01) TÍTULO DE SECCIÓN      [imagen]  │  circulo_numero + F('helv','bold',44)
│                             [caption] │  caption() en bloque lila
│ Frase gancho.                         │  F('helv','bold_i',38) azul
│ Bajada de una o dos líneas.           │  rico(): lead bold + cuerpo regular
│                                       │
│ ✦ Lead. Cuerpo de la viñeta.          │  vinetas()
│ ✦ Lead. Cuerpo.                       │
│                                       │
│ ╭─── Perla clínica ───╮               │  perla_clinica()
│ │ ◎  Una o dos líneas │               │
│ ╰─────────────────────╯               │
│                                       │
│ (02) SIGUIENTE SECCIÓN                │
│  ...                                  │
├───────────────────────────────────────┤
│ BANDA NAVY — rótulo · logo · ©        │  footer_lai()
└───────────────────────────────────────┘
```

Tres secciones numeradas por infografía es lo habitual; cuatro es el máximo. Cada sección lleva **una** Perla clínica.

## Rejilla y medidas

- Margen lateral: 120 px (10,7 % del ancho).
- Columna de texto: 520-580 px cuando hay imagen al lado; 890 px a ancho completo.
- Alternancia: sección 01 texto izquierda / imagen derecha, 02 imagen izquierda / texto derecha, 03 vuelve a alternar.
- Cuerpo 27-28 px, título de sección 44 px, frase gancho 38 px cursiva, caption 24 px.
- Aire vertical entre secciones: 90-120 px.

## Receta

```python
import sys; sys.path.insert(0,'<lai-design-system>/assets')
from brand import *

im = lienzo('infografia', 'gris_fondo')
h  = header_modulo(im, 7, 'Eje somatotropo y regeneración')
footer_lai(im, 'Módulo 07 | Eje somatotropo')

y = h + 70
circulo_numero(im, 150, y+45, 52, '01')
texto(im, (235, y+12), 'EL NUEVO PARADIGMA', F('helv','bold',44), 'azul')
y += 130
texto(im, (120, y), 'Drones, no bloqueos.', F('helv','bold_i',38), 'azul'); y += 62
y = rico(im, (120, y), [('Los péptidos no bloquean: ', F('helv','bold',28), 'gris_texto'),
                        ('reactivan cascadas mediante agonismo.', F('helv','regular',28), 'gris_texto')],
         ancho_max=560) + 20
y = vinetas(im, (120, y), [
      ('Regla de los 50 aa.', '<50 = péptido; >50 = proteína.'),
      ('Nunca agitar.',       '!La cizalla forma fibrillas amiloides irreversibles.'),
    ], ancho=560) + 14
perla_clinica(im, (120, y), 560, 'Perla clínica',
              'Piensa en cascadas, no en bloqueos.', tam=24)
guardar(im, 'infografia-modulo-07.png')
```

## Reglas de contenido

1. **Verbatim.** El contenido clínico que aporte la doctora se reproduce exacto: cifras, unidades, nombres de moléculas, contraindicaciones. Nunca resumir, reinterpretar ni completar de memoria.
2. Toda advertencia dura va en rojo: prefija el cuerpo de la viñeta con `!`.
3. Las cifras con unidades se escriben completas (`<5 EU/mg`, `2–8 °C`, `1 mg = 1000 µg`). Verifica cada conversión mg↔µg con `lai-evidencia` antes de renderizar.
4. La Perla clínica es una regla de decisión, no un resumen. Máximo dos líneas.
5. Bilingüe: si se pide versión en inglés, se rehace la pieza completa; nunca se mezclan idiomas en una misma pieza.

## Imágenes

- Ilustraciones científicas y fotos ya existen en la biblioteca de Gamma de la doctora. **Antes de generar una imagen nueva, consulta `references/gamma-biblioteca.md` del skill `lai-design-system`.**
- Fotos de personas: `mono_azul()`. Ilustraciones moleculares: se usan tal cual, sobre `gris_fondo`.
- Toda imagen lleva `caption()` en bloque lila.

## Reglas de lectura y márgenes (10-oct-2026)
Las versiones para redes (post, story o carrusel de una infografía o guía rápida) cumplen las reglas de `lai-piezas-graficas/references/correcciones-2026-10-10/REGLAS-10-OCT-2026.md`: zona segura del 10 % del lado más corto, cuerpo de 27 px o más a 1080 de ancho, logo horizontal ≈34 % W y contraste de 4.5:1 o más. En la infografía maestra (1125×2000), ningún texto puede ir debajo de 24 px, y los bloques no tocan el margen del 10 %.

## Verificación

Renderiza, abre el PNG y comprueba: nada se sale de caja, los acentos se ven, el rojo solo está en advertencias reales, el pie tiene rótulo y año, y las cifras coinciden con la fuente.
