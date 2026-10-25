---
name: lai-evidencia
description: Produce, verifica y cita el contenido científico del Longevity Academic Institute (LAI), la academia de la Dra. Carolina Rodríguez Morales. Usa este skill SIEMPRE que se pida una revisión de evidencia, bibliografía, referencias, citar un estudio, buscar en PubMed, un DOI o PMID, un metaanálisis o ensayo clínico, declarar el nivel de evidencia, respaldar una afirmación clínica, verificar un dato o una conversión de unidades, actualizar un módulo, una ficha de péptido, un mecanismo de acción, contraindicaciones, seguridad o farmacocinética, o revisar el contenido científico del curso antes de publicarlo.
---

# Evidencia y contenido científico — LAI

## 1. Herramientas

Servidor MCP de PubMed disponible. Cárgalas con `ToolSearch` antes de llamarlas:

`mcp__PubMed__search_articles` · `get_article_metadata` · `get_full_text_article` · `find_related_articles` · `lookup_article_by_citation` · `convert_article_ids` · `get_copyright_status`. También `WebSearch` / `WebFetch`.

**Flujo obligatorio:** buscar en PubMed → verificar metadatos del artículo → citar. **Nunca citar de memoria.** Si una referencia no se verificó con una herramienta en esta sesión, se marca `[POR VERIFICAR]` y no se publica.

## 2. Jerarquía de evidencia

Todo material de LAI declara explícitamente el nivel de lo que afirma.

| Nivel | Qué lo compone | Cómo se enuncia |
|---|---|---|
| **Sólida** | Revisiones sistemáticas, metaanálisis, ECA bien diseñados en humanos | "Existe evidencia sólida de que…" |
| **Moderada** | Ensayos pequeños, cohortes prospectivas, observacionales | "Datos de cohortes sugieren…" |
| **Emergente** | Estudios piloto, series de casos, fase I/II | "Evidencia emergente, aún no confirmada…" |
| **Preclínica** | In vitro, modelos animales | "En modelo murino… **no extrapolable a dosificación humana**" |
| **Off-label / RUO** | Uso fuera de indicación aprobada, o material *research use only* | Se marca **siempre**, sin excepción |

En medicina peptídica gran parte del cuerpo de literatura es preclínica o *off-label*. El material de LAI lo dice sin ambigüedad. Presentar un hallazgo murino como si fuera clínico es el error más grave que puede cometer este skill.

## 3. Formato de cita

```
Autores (hasta 3, luego et al.). Título. Revista. Año;Volumen(Número):Páginas. DOI: 10.xxxx/xxxxx. PMID: xxxxxxxx.
```

Sin DOI, se da el PMID. Sin ninguno de los dos, la afirmación no se publica.

## 4. Reglas duras

1. **El contenido clínico de la Dra. Carolina se reproduce VERBATIM.** Este skill nunca resume, reinterpreta, corrige ni completa lo que ella escribió. Si detecta una posible discrepancia con la literatura, la señala **aparte**, como nota al margen para su revisión, dejando el original intacto.
2. **Nunca inventar** un DOI, PMID, autor, año, revista, cifra ni dosis.
3. **Distinguir dosis de investigación de dosis clínicas.** Nunca presentar una dosis de protocolo animal como pauta humana.
4. **Verificar toda conversión de unidades.** `1 mg = 1000 µg`. Un error de un cero es una sobredosis de diez veces. Toda cifra con unidad que salga en un material se recalcula a mano antes de publicar.
5. Toda ficha de péptido declara contraindicaciones absolutas, interacciones, estado regulatorio y calidad farmacéutica exigible.
6. No se afirma eficacia terapéutica en materiales de marketing.

## 5. Ficha de péptido — plantilla

```
Nombre y sinónimos
Clase y secuencia
Mecanismo de acción            [nivel de evidencia]
Farmacocinética                vía · biodisponibilidad · vida media
Dosificación reportada         cifra + unidad + [nivel de evidencia] + humano/animal
Indicaciones estudiadas        [nivel por indicación]
Contraindicaciones absolutas
Contraindicaciones relativas
Interacciones
Eventos adversos               locales · sistémicos leves · graves
Wash-out y taquifilaxia
Criterios de calidad           pureza HPLC >98,5 % · endotoxinas <5 EU/mg ·
                               sal de acetato (nunca TFA) · COA de tercero · MS de identidad
Estado regulatorio             país por país · off-label · RUO
Bibliografía                   formato de la sección 3
```

## 6. Revisión de evidencia de un módulo

Pregunta en formato **PICO** · estrategia de búsqueda con los términos MeSH usados · resultados agrupados por nivel de evidencia · síntesis · limitaciones · **y lo que NO se puede afirmar todavía**. Esta última sección es obligatoria.

## 7. Checklist antes de publicar

1. ¿Cada afirmación clínica tiene referencia verificada con DOI o PMID real?
2. ¿El nivel de evidencia está declarado en cada afirmación?
3. ¿Los hallazgos preclínicos están marcados como tales?
4. ¿El uso off-label o RUO está señalado?
5. ¿Todas las cifras coinciden con la fuente original?
6. ¿Todas las unidades están escritas completas (mg, µg, mL, EU/mg, °C)?
7. ¿Cada conversión mg↔µg fue recalculada a mano?
8. ¿Las contraindicaciones absolutas están presentes y completas?
9. ¿Las interacciones relevantes están listadas?
10. ¿Los criterios de calidad del producto están incluidos?
11. ¿No hay ninguna promesa de eficacia ni de resultado?
12. ¿El contenido original de la doctora quedó intacto, palabra por palabra?
13. ¿Las discrepancias detectadas se anotaron aparte, sin tocar el original?
14. ¿Hay algo marcado `[POR VERIFICAR]` que todavía no se resolvió?

## 8. Cómo se conecta

El contenido verificado aquí alimenta `lai-infografia-modulo` y `lai-material-curso`. `lai-marketing` no puede publicar ninguna afirmación clínica sin pasar por este skill.
