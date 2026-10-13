# Troubleshooting

## Cannot locate site root

Any command, including `vmt version`, stops with a traceback that ends in:

```text
vexy_mkdocs_tools.cli.BuildError: cannot locate site root (no mkdocs/mkdocs.yml + src_docs/ found walking up from cwd). Pass --root explicitly.
```

The tool searched the current folder and all its parents and found none that
holds both `mkdocs/mkdocs.yml` and `src_docs/`. Do one of these:

- Change into the site folder, or any folder below it, and run the command again.
- Pass the site folder: `vmt --root path/to/site build`.
- If the site uses another layout, pass every path. See
  [Site layout](site-layout.md#using-a-different-layout).

## `mkdocs config missing: <path>`

`build` or `serve` found no file at the `--config` path. The default is
`<root>/mkdocs/mkdocs.yml`. Check the file name and the `--root` you passed.

## `docs_dir` is not an existing directory

ProperDocs stops with a message like:

```text
ERROR   -  Config value 'docs_dir': The path '/…/my-site/mkdocs/docs' isn't an existing directory.
Aborted with a configuration error!
ERROR    | build failed (exit 1)
```

The configuration file has no `docs_dir`, or a wrong one. ProperDocs resolves
it against the folder of `mkdocs.yml`, so add:

```yaml
docs_dir: ../src_docs/md
```

## `Unrecognised theme name: 'material'`

ProperDocs prints:

```text
ERROR   -  Config value 'theme': Unrecognised theme name: 'material'. The available installed themes are: materialx
```

The bundled theme is called `materialx`. Change the theme block to:

```yaml
theme:
  name: materialx
```

## `flowmark not on PATH`

The format step was skipped because the `flowmark` command is not installed in
the environment. The build continues. Either install it:

```bash
uv pip install "vexy-mkdocs-tools[flowmark]"
# or, for a one-off run
uvx --with flowmark vexy-mkdocs-tools build
```

or skip the step with `vmt build --no-format`.

## `source Markdown directory missing: <path>`

The format step runs before anything else and needs the `--src` folder, by
default `<root>/src_docs/md`. Create it, pass the right path with `--src`, or
skip formatting with `--no-format`.

## `build failed (exit <code>)`

`properdocs build` returned an error. Its own messages appear above this line,
in the `ERROR   -  …` format. Fix the reported problem in `mkdocs.yml` or the
Markdown. A common case is a plugin that needs options, such as `llmstxt`
without `sections`.

## The custom domain disappears after a build

The `CNAME` file was only in `docs/`. A full build empties `docs/` twice: once in
the tool's own clean step, which keeps `CNAME`, and once inside
`properdocs build`, which does not. Move the file to `src_docs/md/CNAME`.

## Files I added to `docs/` are gone

`vmt build` and `vmt clean` delete everything in `docs/` except `CNAME`. Keep
extra files in `src_docs/md/`; ProperDocs copies them into `docs/` on each
build.

## Too much or too little output

- Add `--verbose` to see `DEBUG` messages, including every file that `clean`
  removes.
- Set `VMT_LOG_LEVEL=WARNING` to hide the tool's `INFO` messages.
