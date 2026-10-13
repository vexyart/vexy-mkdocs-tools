# Site configuration

`vmt` does not have a configuration file of its own. It passes
`mkdocs/mkdocs.yml` to ProperDocs, which reads it with the same keys as MkDocs.
This page covers the settings that matter when the file lives in `mkdocs/` and
the bundled packages are used.

## A minimal configuration

```yaml
site_name: My site
docs_dir: ../src_docs/md
theme:
  name: materialx
```

### `docs_dir`

ProperDocs resolves a relative `docs_dir` against the folder that contains the
configuration file. The file is in `mkdocs/`, so the Markdown folder is
`../src_docs/md`. Without this line, ProperDocs looks for `mkdocs/docs/`.

`vmt` does not pass the source folder to ProperDocs. The `--src` flag only
affects the Flowmark step.

### `site_dir`

You do not need to set `site_dir`. `vmt build` passes `-d <docs>` to
`properdocs build`, which overrides it.

### `theme`

The bundled theme package, `mkdocs-materialx`, registers the theme name
`materialx`, and that is the only theme ProperDocs accepts with the bundled
packages. Other names fail:

```text
ERROR   -  Config value 'theme': Unrecognised theme name: 'material'. The available installed themes are: materialx
```

ProperDocs does not ship the classic `mkdocs` and `readthedocs` themes. Asking
for one prints a hint such as `pip install properdocs-theme-mkdocs`.

## Plugins you can enable

These plugin names are available after installing `vexy-mkdocs-tools`:

| Plugin name | Package |
|---|---|
| `search` | `properdocs` |
| `materialx/blog`, `materialx/group`, `materialx/info`, `materialx/meta`, `materialx/offline`, `materialx/optimize`, `materialx/privacy`, `materialx/search`, `materialx/social`, `materialx/tags` | `mkdocs-materialx` |
| `awesome-nav` | `mkdocs-awesome-nav` |
| `include-markdown` | `mkdocs-include-markdown-plugin` |
| `llmstxt` | `mkdocs-llmstxt` |
| `copy-to-llm` | `mkdocs-copy-to-llm` |
| `rss` | `mkdocs-rss-plugin` |
| `document-dates` | `mkdocs-document-dates`, installed as a dependency of `mkdocs-materialx` |

List them in the usual way:

```yaml
plugins:
  - search
  - awesome-nav
  - include-markdown
```

Each plugin has its own options; see the documentation of its package.

## Markdown extensions

`pymdown-extensions` is installed, so you can enable any `pymdownx.*` extension:

```yaml
markdown_extensions:
  - admonition
  - toc:
      permalink: true
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
```

## A fuller example

```yaml
site_name: My site
site_url: https://example.com/
docs_dir: ../src_docs/md
theme:
  name: materialx
  features:
    - navigation.sections
    - content.code.copy
plugins:
  - search
  - include-markdown
markdown_extensions:
  - admonition
  - pymdownx.superfences
nav:
  - Home: index.md
```

!!! note
    Some plugins need options before they run. For example, `llmstxt` without a
    `sections` option stops the build with
    `Plugin 'llmstxt' option 'sections': Required configuration not provided.`
    Check each plugin's documentation; `vmt` passes the file to ProperDocs
    unchanged.
