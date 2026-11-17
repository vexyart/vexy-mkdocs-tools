---
this_file: src_docs/md/configuration.md
tags: [Configuration]
---

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
| `materialx/search`, `materialx/meta`, `materialx/tags` | `mkdocs-materialx` |
| `materialx/blog`, `materialx/group`, `materialx/info`, `materialx/meta`, `materialx/offline`, `materialx/optimize`, `materialx/privacy`, `materialx/search`, `materialx/social`, `materialx/tags` | `mkdocs-materialx` |
| `awesome-nav` | `mkdocs-awesome-nav` |
| `include-markdown` | `mkdocs-include-markdown-plugin` |
| `llmstxt` | `mkdocs-llmstxt` |
| `copy-to-llm` | `mkdocs-copy-to-llm` |
| `rss` | `mkdocs-rss-plugin` |
| `mkdocstrings` (Python handler) | `mkdocstrings[python]` |
| `autorefs` | `mkdocs-autorefs` |
| `codeinclude` | `mkdocs-codeinclude-plugin` |
| `print-site` | `mkdocs-print-site-plugin` |
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

## The configuration used by this site

This code block is read from the actual site configuration at build time:

<!--codeinclude-->
[Site configuration](../mkdocs.yml)
<!--/codeinclude-->

## Choose plugins for the content

Use [awesome-nav](https://lukasgeiter.github.io/mkdocs-awesome-nav/) to keep the
ordered navigation beside the Markdown in `.nav.yml`. MaterialX meta merges
`.meta.yml` into page front matter; the tags plugin uses that metadata to build
the [Topics](topics.md) index. Keep `materialx/search` explicit whenever a
`plugins` list is present.

The Python reference uses [mkdocstrings](https://mkdocstrings.github.io/python/usage/)
with source paths relative to the configuration file. Autorefs resolves links
such as [the CLI class][vexy_mkdocs_tools.cli.CLI]. Static source inspection
keeps documentation builds independent of application services.

Use codeinclude for code from maintained files and include-markdown for prose
shared with the repository, as on the [changelog](changelog.md). Print-site stays
last so its combined guide contains the final navigation and resolved references.

For local browser editing, install `vexy-mkdocs-tools[authoring]` and use
`properdocs serve -f src_docs/mkdocs.authoring.yml -a 127.0.0.1:8000`.
The authoring overlay keeps the site's plugin list and adds `live-edit`.
Release builds use `mkdocs.yml`.

Categories is useful for a wiki with a separate category taxonomy. These sites
already use MaterialX tags, so a second category index would repeat the same
structure. MaterialX `navigation.path` supplies breadcrumbs in the manuals;
the breadcrumbs plugin would also generate source index files. The ToC sidebar
plugin is intended for additional sidebar Markdown, which these sites do not
have; `toc.follow` retains the native page outline. These plugins are evaluated
rather than added without content that uses them.
