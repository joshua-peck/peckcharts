# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project Scope

This project produces **Jupyter notebooks and short Python scripts** that generate
charts for posting on social media. Every chart should match the visual style of
the website **https://joshuampeck.com/** so the output is consistent and on-brand.

The deliverables are throwaway-friendly: short, self-contained notebooks/scripts.
Do **not** build a large application framework. Keep each script focused on making
one chart (or a small related set).

## Tooling

- **`uv` manages this project.** Always use `uv`, never bare `pip` or `python`.
  - Add a dependency: `uv add <package>`
  - Add a dev/notebook tool: `uv add --dev <package>`
  - Run a script: `uv run python path/to/script.py`
  - Run/launch notebooks: `uv run jupyter lab` (or `uv run jupyter notebook`)
  - Sync the environment: `uv sync`
- Do not edit `uv.lock` by hand. Let `uv` manage it.
- Pin Python in `pyproject.toml` / `.python-version` and respect it.

## The Style Module (central requirement)

There is **one shared styling module** that configures Matplotlib to match the
joshuampeck.com theme. Nearly every script/notebook imports it to stay consistent.

- Location: `src/jmpstyle/` (importable as `jmpstyle`), exposing at minimum:
  - `apply_style()` — applies the theme to the global Matplotlib `rcParams`.
  - `COLORS` — a dict/namespace of the brand palette (background, foreground,
    accent, muted, plus a categorical cycle) for direct use in plot calls.
  - A registered named style (e.g. a `.mplstyle` file) so `plt.style.use("jmp")`
    also works.
- Typical usage at the top of a script/notebook:
  ```python
  import matplotlib.pyplot as plt
  from jmpstyle import apply_style, COLORS
  apply_style()
  ```
- The module is the single source of truth for the look. Change the theme **here**,
  not in individual scripts. Individual charts may override specific colors from
  `COLORS` but should not redefine the base theme.

### Theme reference (joshuampeck.com)

The site is a dark, minimal quantitative-research aesthetic. The style module
should encode, at minimum:

- **Mode:** dark background, light foreground text.
- **Palette:** a near-black background, off-white text, a single strong accent for
  emphasis/series highlights, plus muted grays for secondary elements and a small
  categorical color cycle for multi-series charts.
- **Typography:** clean sans-serif for labels/ticks; a serif may be used for titles
  to echo the site's editorial headings. Fall back gracefully to common system fonts
  if brand fonts aren't installed.
- **Chart chrome:** minimal — thin or no top/right spines, light/subtle gridlines,
  generous margins, no heavy borders.

> **Verify the exact values.** The precise hex colors and font families should be
> confirmed against the live site's CSS before locking them in (the homepage HTML is
> JS-rendered, so pull the actual values from the site's stylesheet or browser
> dev-tools and put them in `jmpstyle`). Treat the description above as the intended
> direction, not final tokens.

## Output Conventions (social media)

- Default export at social-friendly sizes and high DPI. Provide helpers/defaults for:
  - **Square** (1:1, e.g. 1080×1080) — feed posts.
  - **Portrait** (4:5, e.g. 1080×1350) — feed posts.
  - **Landscape** (16:9) — link previews / wide charts.
- Save with `dpi >= 200`, `bbox_inches="tight"`, and a matching (or transparent)
  background. Default to **PNG**; offer SVG when a vector asset is useful.
- Write rendered images to an `output/` (or `exports/`) directory; do not commit
  large binaries unless asked.

## Repository Layout (suggested)

```
pyproject.toml
uv.lock
src/jmpstyle/        # the shared style module
notebooks/           # exploratory / chart-building notebooks
scripts/             # short standalone chart scripts
output/              # rendered images (gitignore-able)
```

## Conventions for Claude

- Prefer **short, readable** scripts over abstraction. One chart per file is fine.
- Every new chart script/notebook should `apply_style()` first.
- Don't hardcode brand colors in individual charts — pull from `jmpstyle.COLORS`.
- When adding packages, use `uv add`; keep the dependency set lean
  (matplotlib, jupyter, and only what a given chart needs).
- Don't introduce a web framework, database, or build system — this is a
  notebook/script project.
