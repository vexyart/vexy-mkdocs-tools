# Site layout

`vmt` expects every site to use the same folder structure. This page describes
that structure and how the tool finds it.

## The default layout

```text
<root>/
├── mkdocs/
│   └── mkdocs.yml      # --config
├── src_docs/
│   └── md/             # --src: Markdown source
│       ├── index.md
│       └── CNAME       # optional custom domain
└── docs/               # --docs: build output
```

| Path | Role | Flag to change it |
|---|---|---|
| `mkdocs/mkdocs.yml` | ProperDocs configuration | `--config` |
| `src_docs/md/` | Markdown source; Flowmark formats this folder | `--src` |
| `docs/` | Generated site; GitHub Pages serves it | `--docs` |

## How the site root is found

When you do not pass `--root`, the tool starts in the current working directory
and checks it and then each parent folder in turn. The first folder that
contains both of these is the site root:

- a file `mkdocs/mkdocs.yml`, and
- a folder `src_docs/`.

So you can run `vmt build` from the site root or from any folder below it, such
as `src_docs/md/chapter-1/`.

If no folder matches, the tool stops with:

```text
BuildError: cannot locate site root (no mkdocs/mkdocs.yml + src_docs/ found walking up from cwd). Pass --root explicitly.
```

The search runs before the command itself, so it applies to every command,
including `version` and `clean`. With `--root`, the search is skipped and the
named folder is used as it is; the tool does not check that it has the expected
contents.

## The output folder

`vmt build` and `vmt clean` delete everything in `docs/` except `CNAME`. Do not
keep hand-written files in `docs/`. Put files that should appear in the built
site, such as images, downloads or `CNAME`, in `src_docs/md/`. ProperDocs copies
every file that is not Markdown from there into `docs/`, keeping its relative
path.

After a build, `docs/` always contains an empty `.nojekyll` file.

## The `CNAME` file

GitHub Pages reads the custom domain from `docs/CNAME`. Keep the file in
`src_docs/md/CNAME`.

`vmt clean` keeps an existing `docs/CNAME`. A full `vmt build` does not: after
the tool's own clean step, `properdocs build` empties the output folder again
before it writes the site. A `CNAME` that exists only in `docs/` is therefore
gone after `vmt build`. A `CNAME` in `src_docs/md/` is copied back on every
build.

## Using a different layout

Pass the paths explicitly. For example, for a site that keeps its configuration
at the top level and its Markdown in `content/`:

```bash
vmt --root . --config mkdocs.yml --src content --docs public build
```

Remember to set `docs_dir: content` in that configuration file as well, because
`--src` does not change where ProperDocs reads from.
