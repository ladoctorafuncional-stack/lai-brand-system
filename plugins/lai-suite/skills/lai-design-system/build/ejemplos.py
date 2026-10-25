# -*- coding: utf-8 -*-
"""Ejemplos ejecutables del sistema de diseño LAI. Sirven como prueba de humo."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets'))
from brand import *

SAL = sys.argv[1] if len(sys.argv) > 1 else '.'

# 1 — Portada de compendio
guardar(portada_compendio('COMPENDIO ACADÉMICO DE', 'Medicina Peptídica y',
                          'Bioregulación Celular.', 'en escenarios clínicos reales',
                          'Módulo 12',
                          descriptor='Eje Sexual, Libido y Regulación Hormonal.',
                          descriptor_it='Neuroendocrinología del Deseo, Fertilidad y Rendimiento Íntimo.'),
        os.path.join(SAL, '1-portada-compendio.png'))

# 2 — Cuadernillo de casos
guardar(portada_compendio('FORMACIÓN ACADÉMICA EN', 'Medicina Peptídica y',
                          'Bioregulación Celular.', 'en escenarios clínicos reales',
                          'Casos clínicos', etiqueta='CUADERNILLO DE CASOS CLÍNICOS',
                          descriptor='Integración diagnóstica, decisión terapéutica y seguridad.',
                          descriptor_it='6 casos complejos basados en los 12 módulos del programa.'),
        os.path.join(SAL, '2-cuadernillo.png'))

# 3 — Infografía de módulo
im = lienzo('infografia', 'gris_fondo')
h = header_modulo(im, 1, 'Bioquímica y farmacología')
footer_lai(im, 'Módulo 01 | Bioquímica y farmacología')
y = h + 70
circulo_numero(im, 150, y + 45, 52, '01')
texto(im, (235, y + 12), 'EL NUEVO PARADIGMA', F('helv', 'bold', 44), 'azul')
y += 130
texto(im, (120, y), 'Drones, no bloqueos.', F('helv', 'bold_i', 38), 'azul'); y += 62
y = rico(im, (120, y), [('Los péptidos no bloquean: ', F('helv', 'bold', 28), 'gris_texto'),
                        ('reactivan cascadas mediante agonismo y modulación alostérica.',
                         F('helv', 'regular', 28), 'gris_texto')], ancho_max=560) + 20
y = vinetas(im, (120, y), [
      ('Regla de los 50 aa.', '<50 = péptido (alta entropía); >50 = proteína (estructura rígida).'),
      ('Agonismo y modulación.', 'Reactivan la homeostasis; no son bloqueadores sintéticos.'),
      ('Nunca agitar.', '!La cizalla forma fibrillas amiloides irreversibles.'),
    ], ancho=560) + 14
y = perla_clinica(im, (120, y), 560, 'Perla clínica',
                  'Piensa en cascadas, no en bloqueos;\nen orden molecular, no en concentración.',
                  tam=24)[3] + 90
caption(im, (700, h + 190), 'Mensajeros de señalización celular.', ancho_max=340)
circulo_numero(im, 150, y + 45, 52, '02')
texto(im, (235, y + 12), 'INGENIERÍA PEPTÍDICA', F('helv', 'bold', 44), 'azul')
guardar(im, os.path.join(SAL, '3-infografia-modulo.png'))

# 4 — Story de agenda
im = lienzo('story'); fondo_profundo(im, angulo=150)
poner_logo(im, 'horizontal-blanco', im.width - 90, 110, ancho=380, anclaje='rt')
y = 360
for seccion, bloques in [('Apertura', [('9:00 — 9:10 a.m.', 'Llegada y registro', 'Presentación de la academia')]),
                         ('Taller', [('9:10 — 10:20 a.m.', 'Dra. Carolina Rodríguez', 'Casos clínicos · Parte 1'),
                                     ('10:30 — 11:30 a.m.', 'Dra. Carolina Rodríguez', 'Taller práctico · Parte 2')]),
                         ('Certificados', [('2:50 — 3:00 p.m.', 'Dra. Carolina Rodríguez', 'Entrega de diploma por LAI')])]:
    pill(im, (150, y), seccion, F('helv', 'bold', 40), relleno='periwinkle',
         color='azul', padx=26, pady=14, radio=10)
    y += 130
    for hora, quien, que in bloques:
        texto(im, (150, y), hora, F('helv', 'regular', 34), 'blanco')
        regla(im, 470, y + 24, 590, 'gris_medio', 3)
        texto(im, (630, y - 8), quien, F('helv', 'regular', 34), 'blanco')
        texto(im, (630, y + 36), que, F('helv', 'regular', 34), 'blanco')
        y += 180
    y += 50
guardar(im, os.path.join(SAL, '4-story-agenda.png'))

# 5 — Membrete
im, util = membrete('carta')
x0, y0, x1, y1 = util
texto(im, (x0, y0), 'Medellín, 24 de agosto de 2026', F('lato', 'regular', 34), 'gris_texto')
parrafo(im, (x0, y0 + 110), 'Nos complace compartir con toda nuestra comunidad académica que '
        'nuestra directora médica y fundadora ha sido seleccionada para participar en el workshop '
        'internacional de la institución anfitriona.', F('lato', 'regular', 34), 'gris_texto',
        ancho_max=x1 - x0, interlinea=1.55)
poner_logo(im, 'firma', x0, y1 - 420, ancho=380)
guardar(im, os.path.join(SAL, '5-membrete.png'))
print('5 piezas generadas en', SAL)
