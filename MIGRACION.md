# Migración a fuente única (LAI)

Regla: **todo cambio de marca se edita en este repo.** Cowork y Claude Design se actualizan desde aquí; no se editan directamente.

## Cowork / Claude Code
1. Añadir el marketplace: `ladoctorafuncional-stack/lai-brand-system`.
2. Instalar `lai-suite`.
3. Desinstalar el `lai-suite` de "My Uploads" y cualquier skill suelta `lai-brand-system`.

## Claude Design
Re-importar el repo después de cada versión nueva (`VERSION`).

## Publicar un cambio
1. Editar en `plugins/lai-suite/skills/...` o `brand/`.
2. Subir `version` en `plugins/lai-suite/.claude-plugin/plugin.json`, `VERSION` y `CHANGELOG.md`.
3. Merge a `main` → actualizar plugin en Cowork → re-importar en Claude Design.
