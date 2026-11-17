---
this_file: DEPENDENCIES.md
---

# Documentation dependencies

The project manifest is authoritative for version bounds; `uv.lock` records the resolved environment.

- ProperDocs and MaterialX: build the documentation and supply metadata, search and tags.
- PyMdown: code highlighting, fences, tabs, details and task lists.
- Awesome-nav: preserve curated navigation alongside the Markdown.
- Include-markdown and codeinclude: render maintained prose and code without duplicated copies.
- Mkdocstrings with its Python handler and autorefs: collect Python source documentation and resolve references.
- Print-site: provide a combined guide; it runs after the other plugins.
- Live-edit (authoring extra): edit Markdown in a local preview.
- Existing llmstxt, copy-to-llm and RSS packages remain available for sites that configure them.
