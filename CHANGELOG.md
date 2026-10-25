# Changelog

## 1.0.0 — 2026-10-25
Consolidación: el repo pasa a ser la fuente única de marca.
- Nuevo `.claude-plugin/marketplace.json` con el plugin `lai-suite`.
- `plugins/lai-suite`: tomado de `lai-suite` v1.3.1 (vigente; alineado al Manual de Marca LAI v2).
- Retirado el skill `lai-brand-system` de `.claude/skills/`: apuntaba a rutas inexistentes (`AGENTS.md`, `01_contexto_marca/`, `00_fuente_original/`, `marca/logos/v2/`, `04_produccion/`). Sustituido por `lai-suite:lai-design-system`.
- `.claude/skills/` ahora contiene symlinks a `plugins/lai-suite/skills/*`.
- Pendiente: EB Garamond sigue en `fonts/eb-garamond/` aunque el Manual v2 solo usa Lato + Arimo; confirmar con la Dra. si se retira.
- Pendiente: `guidelines/Manual_de_Marca_LAI.dc.html` no renderiza solo (faltan `doc-page.js`, `support.js`, `styles.css`); el PDF vigente está en `plugins/lai-suite/skills/lai-design-system/references/manual-marca-lai-v2.pdf`.
