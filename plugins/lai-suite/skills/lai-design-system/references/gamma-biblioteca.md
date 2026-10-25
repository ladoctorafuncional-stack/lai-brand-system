# Biblioteca de imágenes de Gamma — cómo reutilizarla

La Dra. Carolina ya pagó y generó una biblioteca de imágenes en Gamma para los módulos y compendios. **Antes de generar cualquier imagen nueva, revisa si ya existe ahí.**

## Lo que sí funciona

El conector de Gamma está activo. `mcp__Gamma__read_gamma` devuelve el contenido completo de un gamma **incluyendo las URLs de sus imágenes** en `cdn.gamma.app`.

```
1. mcp__Gamma__get_gammas(limit=50, type='all')   -> lista de módulos y sus IDs
2. mcp__Gamma__read_gamma(id)                     -> HTML con src="https://cdn.gamma.app/..."
3. Extraer las URLs y su alt/caption para armar el catálogo
```

Gammas de la academia (IDs a agosto 2026):

| Gamma | ID |
|---|---|
| Módulo 1 | `g_n9fnd0ld0nkb5re` |
| Módulo 2 | `g_c71uhgr95btb31r` |
| Módulo 3 | `g_44059m5ollod4g2` |
| Módulo 4 | `g_g5k7jakny5vesi9` |
| Módulo 5 | `g_cun516y02b1c6hm` |
| Módulo 6 | `g_mm6ylwibvzyajmc` |
| Módulo 7 | `g_2mrtbr8t8q8juec` |
| Módulo 8 | `g_ese1s6n1k9jt74c` |
| Módulo 9 | `g_ntgg3v00h0cqmqf` |
| Módulo 10 | `g_5uy90y1cy30ujtr` |
| Módulo 11 | `g_1811xdkbypx44ox` |
| Módulo 1.1 | `g_junz13ypqh76u35` |
| Reconstitución de Péptidos | `g_iog7ni4ib7ci9b1` |
| Hormonas salivales | `g_6x1fr5boud9hvf5` |

Verifica la lista con `get_gammas` en cada sesión: puede haber gammas nuevos.

## La limitación

El contenedor de trabajo **no tiene salida de red hacia `cdn.gamma.app`** (devuelve 403 en el túnel). Consecuencias:

| Entregable | ¿Se pueden usar las imágenes de Gamma? |
|---|---|
| HTML, landing page, correo, artefacto web | **Sí.** Se referencian por URL y cargan en el navegador de quien lo abre. |
| Importar un diseño a Gamma (`import-claude-design-from-url`) | **Sí.** |
| Catálogo o inventario de la biblioteca | **Sí.** Se lee todo vía `read_gamma`. |
| PNG / PDF compuesto aquí con Pillow (stories, infografías, portadas) | **No directamente.** Hay que pedirle a la doctora que suelte esas imágenes concretas en el chat una sola vez; quedan en la carpeta de subidas y se componen normal. |

## Regla

1. Consulta el catálogo antes de proponer generar una imagen.
2. Si la imagen existe, úsala: por URL cuando el entregable es web, o pidiéndola una vez cuando el entregable es un PNG compuesto.
3. Solo genera imagen nueva cuando de verdad no exista equivalente, y dilo explícitamente antes de hacerlo.
