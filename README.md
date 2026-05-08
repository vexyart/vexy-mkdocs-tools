# vexy-mkdocs-tools

Fire-based CLI that bundles [ProperDocs](https://github.com/jaywhj/properdocs) + [MaterialX](https://github.com/jaywhj/mkdocs-materialx) and the standard `vexy-` plugin set, so a site builds in one shot:

```bash
uvx vexy-mkdocs-tools build
```

## Why

Every FontLab/Vexy MkDocs-style site repeats the same dependency list and the same wrapper script (clean `docs/` but keep `CNAME`, optionally Flowmark-format `src_docs/md/` first, then `properdocs build`, then write `.nojekyll`). This package owns the dependency set and the wrapper, so site repos shrink to "Markdown + `mkdocs.yml`".

## Install

```bash
uv pip install vexy-mkdocs-tools           # site builds
uv pip install "vexy-mkdocs-tools[flowmark]" # also Flowmark formatting
```

Or ad-hoc without installing:

```bash
uvx vexy-mkdocs-tools build
uvx --with flowmark vexy-mkdocs-tools build
```

## Commands

| Command | What it does |
|---|---|
| `vmt build` | Flowmark-format `src_docs/md/` (if available) → wipe `docs/` (preserving `CNAME`) → `properdocs build` → write `.nojekyll` |
| `vmt build --no-format` | Skip the Flowmark step |
| `vmt serve` | `properdocs serve` with the same config |
| `vmt clean` | Wipe `docs/` (preserving `CNAME`) without rebuilding |
| `vmt format` | Run Flowmark in place over `src_docs/md/` |
| `vmt version` | Print installed version |

`vexy-mkdocs-tools` and `vmt` are aliases.

## Site layout assumed

```
<repo>/
├── mkdocs/mkdocs.yml     # config (--config to override)
├── src_docs/md/          # Markdown source (--src to override)
└── docs/                 # build output (--docs to override)
```

The CLI walks up from `cwd` until it finds a directory containing both `mkdocs/mkdocs.yml` and `src_docs/`. Pass `--root` to skip the walk.

## Bundled dependencies

ProperDocs 1.6.7+, MaterialX 10.1.4+, plus `pymdown-extensions`, `mkdocs-awesome-nav`, `mkdocs-include-markdown-plugin`, `mkdocs-llmstxt`, `mkdocs-copy-to-llm`, `mkdocs-rss-plugin`. The `[flowmark]` extra adds `flowmark`.

## Develop

```bash
uv sync --extra dev
uv run python -m pytest -q
uvx ruff check src tests
./build.sh    # full build + test + wheel/sdist
./publish.sh  # upload to PyPI (needs UV_PUBLISH_TOKEN)
```

Releases are tag-driven — push a `vX.Y.Z` tag and the `release` workflow ships to PyPI.

## License

Apache-2.0.
