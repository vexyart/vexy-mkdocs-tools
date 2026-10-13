# Quick start

This page creates a new documentation site and builds it with `vmt`.

## Prerequisites

- `uv` installed.
- An empty folder for the site, here called `my-site`.

## Create the site

1. Create the three folders the tool expects:

    ```bash
    mkdir -p my-site/mkdocs my-site/src_docs/md my-site/docs
    cd my-site
    ```

2. Create `mkdocs/mkdocs.yml` with this content:

    ```yaml
    site_name: My site
    docs_dir: ../src_docs/md
    theme:
      name: materialx
    ```

    `docs_dir` is resolved against the folder that holds `mkdocs.yml`, so
    `../src_docs/md` points from `mkdocs/` to the Markdown folder. The theme
    name is `materialx`, not `material`.

3. Create the first page, `src_docs/md/index.md`:

    ```markdown
    # Hello

    This is my site.
    ```

4. Build the site:

    ```bash
    uvx vexy-mkdocs-tools build
    ```

The tool prints its steps:

```text
WARNING  | flowmark not on PATH; install the [flowmark] extra (`uv pip install vexy-mkdocs-tools[flowmark]`) to enable this step
INFO     | Cleaned /…/my-site/docs (preserved CNAME)
INFO     | Running: properdocs build -f /…/my-site/mkdocs/mkdocs.yml -d /…/my-site/docs
INFO     | Build complete
```

`docs/` now holds the site: `index.html`, `404.html`, `assets/`, `search/`,
`sitemap.xml`, `sitemap.xml.gz` and an empty `.nojekyll`.

The warning only means that the format step was skipped. To run it, use
`uvx --with flowmark vexy-mkdocs-tools build`. To skip it without a warning,
add `--no-format`.

## Preview while you write

```bash
uvx vexy-mkdocs-tools serve
```

This runs `properdocs serve` with the same configuration. Press
<kbd>Ctrl</kbd>+<kbd>C</kbd> to stop it; the tool then prints `Server stopped`.

## Add a custom domain

1. Put the domain in `src_docs/md/CNAME`:

    ```bash
    echo docs.example.com > src_docs/md/CNAME
    ```

2. Build again.

ProperDocs copies every file that is not Markdown from `src_docs/md/` to
`docs/`, so `docs/CNAME` is written on every build. A `CNAME` that exists only in
`docs/` does not survive a full build; see [Site layout](site-layout.md#the-cname-file).

## Publish with GitHub Pages

1. Commit `mkdocs/`, `src_docs/` and the built `docs/` folder.
2. In the repository settings on GitHub, set **Pages** to deploy from the
   default branch and the `/docs` folder.

The `.nojekyll` file that `vmt build` writes tells GitHub Pages to publish the
files without running Jekyll.
