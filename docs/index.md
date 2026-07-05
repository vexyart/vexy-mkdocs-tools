---
title: Home
layout: default
nav_order: 1
---

# vexy-mkdocs-tools

One command turns a folder of Markdown into a deployed documentation site:

```bash
uvx vexy-mkdocs-tools build
```

Every FontLab and Vexy docs site used to carry the same long dependency list and
the same fragile wrapper script. This tool owns both. A site repo shrinks to
what a writer actually edits: Markdown and one config file.

## The contract

`vexy-mkdocs-tools` expects — and every consumer site provides — this layout:

```
<repo>/
├── mkdocs/mkdocs.yml     # the MkDocs config
├── src_docs/md/          # Markdown you write
└── docs/                 # build output (committed, served by GitHub Pages)
```

The CLI walks up from the current directory until it finds a folder that holds
**both** `mkdocs/mkdocs.yml` and `src_docs/`. That folder is the site root. Pass
`--root` to name it explicitly and skip the walk.

`build` runs four steps in order:

1. **Format** — if [Flowmark](https://pypi.org/project/flowmark/) is installed,
   rewrite `src_docs/md/` in place (semantic line breaks, smart quotes). Skipped
   silently when Flowmark is absent; skip it always with `--no-format`.
2. **Clean** — empty `docs/`, but keep a `CNAME` if one already sits there.
3. **Build** — hand `mkdocs/mkdocs.yml` to `properdocs build`, output into `docs/`.
4. **Publish marker** — write `docs/.nojekyll` so GitHub Pages serves the built
   assets verbatim instead of running them back through Jekyll.

## Your custom domain

Keep your `CNAME` file in **`src_docs/md/CNAME`**, not in `docs/`. MkDocs copies
every non-Markdown file from `src_docs/md/` into `docs/` on each build, so the
domain is reapplied every time. (The clean step also preserves a `docs/CNAME`
if you keep it there, but a full build's own clean would still remove it — so
`src_docs/md/CNAME` is the durable home.)

## Commands

| Command | What it does |
|---|---|
| `vmt build` | Format → clean → `properdocs build` → write `.nojekyll` |
| `vmt build --no-format` | Same, but skip the Flowmark step |
| `vmt serve` | `properdocs serve` with the same config (live reload) |
| `vmt clean` | Empty `docs/` (keeping `CNAME`) without rebuilding |
| `vmt format` | Run Flowmark in place over `src_docs/md/` |
| `vmt version` | Print the installed version |

`vexy-mkdocs-tools` and `vmt` are the same command.

## The theme name is `materialx`

This tool bundles [MaterialX](https://pypi.org/project/mkdocs-materialx/), a
successor to Material for MkDocs. In `mkdocs/mkdocs.yml`, set:

```yaml
theme:
  name: materialx
```

`name: material` will not resolve — the stack registers `materialx`.

## Install

```bash
uv pip install vexy-mkdocs-tools            # site builds
uv pip install "vexy-mkdocs-tools[flowmark]"  # also Flowmark formatting
```

See the [GitHub repository](https://github.com/vexyart/vexy-mkdocs-tools) for
source, the changelog, and the release workflow.
