# vexy-mkdocs-tools

`vexy-mkdocs-tools` is a command-line tool that builds a documentation site
from a folder of Markdown files. It installs ProperDocs, the MaterialX theme and
a fixed set of MkDocs plugins, and runs the same build steps that every FontLab
and Vexy documentation site uses.

```bash
uvx vexy-mkdocs-tools build
```

The tool has two command names, `vexy-mkdocs-tools` and `vmt`. They run the same
program.

## What it does

A site repository that uses this tool contains only Markdown and one
configuration file:

```text
my-site/
├── mkdocs/mkdocs.yml     # site configuration
├── src_docs/md/          # Markdown source
└── docs/                 # generated site, served by GitHub Pages
```

`vmt build` turns `src_docs/md/` into a static site in `docs/` in four steps:

1. **Format.** If `flowmark` is on your `PATH`, it reformats the Markdown in
   `src_docs/md/` in place. If not, it prints a warning and continues.
2. **Clean.** It deletes everything in `docs/` except a file named `CNAME`.
3. **Build.** It runs `properdocs build` with `mkdocs/mkdocs.yml` as the
   configuration and `docs/` as the output folder.
4. **Mark.** It creates an empty `docs/.nojekyll` file, so GitHub Pages serves
   the files as they are instead of running Jekyll on them.

## Why it exists

Without this tool, each site repository has to list the same Python packages
and carry its own copy of the build script. With it, the package list and the
script live in one place, and a site repository only needs its Markdown and its
`mkdocs.yml`.

## What it installs

Installing `vexy-mkdocs-tools` also installs:

| Package | Minimum version | Purpose |
|---|---|---|
| `properdocs` | 1.6.7 | The site generator; its configuration format is MkDocs' `mkdocs.yml` |
| `mkdocs-materialx` | 10.1.4 | The `materialx` theme and its `materialx/*` plugins |
| `pymdown-extensions` | 10.2 | Markdown extensions |
| `mkdocs-awesome-nav` | 3.3 | Plugin `awesome-nav`: customize the navigation structure |
| `mkdocs-include-markdown-plugin` | 7.2 | Plugin `include-markdown`: include one Markdown file in another |
| `mkdocs-llmstxt` | 0.2 | Plugin `llmstxt`: generate an `/llms.txt` file |
| `mkdocs-copy-to-llm` | 0.2 | Plugin `copy-to-llm`: add "Copy to LLM" buttons |
| `mkdocs-rss-plugin` | 1.17 | Plugin `rss`: generate RSS and JSON feeds |
| `fire` | 0.7 | The command-line interface |
| `loguru` | 0.7 | Logging |

The optional `flowmark` extra adds `flowmark` 0.6.5 or later for the format step.

## Where to go next

- [Installation](installation.md)
- [Quick start](quickstart.md): build a new site from scratch.
- [Command reference](cli.md): every command and flag.
- [Site layout](site-layout.md): how the tool finds the site and its folders.
- [Site configuration](configuration.md): what to put in `mkdocs/mkdocs.yml`.
- [Troubleshooting](troubleshooting.md)
