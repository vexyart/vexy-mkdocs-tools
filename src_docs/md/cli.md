# Command reference

```text
vmt [GLOBAL FLAGS] COMMAND [COMMAND FLAGS]
```

`vexy-mkdocs-tools` and `vmt` are the same program. `python -m vexy_mkdocs_tools`
also runs it. The command line is built with
[Python Fire](https://github.com/google/python-fire), so `--help` after any
command shows its flags:

```bash
vmt --help
vmt build --help
```

## Global flags

These flags choose the folders the commands work on. Relative paths are resolved
against the current working directory.

| Flag | Short | Default | Meaning |
|---|---|---|---|
| `--root` | `-r` | Found by searching upwards | The site root folder |
| `--config` | `-c` | `<root>/mkdocs/mkdocs.yml` | The ProperDocs configuration file |
| `--docs` | `-d` | `<root>/docs` | The output folder |
| `--src` | `-s` | `<root>/src_docs/md` | The Markdown folder that Flowmark formats |

Fire accepts these flags before or after the command name, so
`vmt --root site build` and `vmt build --root site` do the same thing.

`--src` only tells the format step where the Markdown is. ProperDocs reads its
source folder from `docs_dir` in the configuration file. See
[Site configuration](configuration.md).

Without `--root`, the tool searches for the site root before it runs any
command. See [Site layout](site-layout.md#how-the-site-root-is-found).

## `build`

Runs the full pipeline.

```bash
vmt build [--verbose] [--no-format]
```

| Flag | Short | Default | Meaning |
|---|---|---|---|
| `--verbose` | `-v` | off | Log at `DEBUG` level |
| `--no-format` (also `--no_format`) | `-n` | off | Skip the Flowmark step |

Steps, in order:

1. Unless `--no-format` is given, run Flowmark over the `--src` folder (see
   [`format`](#format)). If the folder does not exist, the build stops with
   `source Markdown directory missing: <path>`.
2. Delete everything in the `--docs` folder except `CNAME`. Create the folder if
   it does not exist.
3. Stop with `mkdocs config missing: <path>` if the configuration file does not
   exist.
4. Run `properdocs build -f <config> -d <docs>` from the site root.
5. Create `<docs>/.nojekyll`.

If any step fails, the tool logs the error and exits with status 1. A failed
ProperDocs run is reported as `build failed (exit <code>)`.

## `serve`

Starts the ProperDocs development server with live reload.

```bash
vmt serve [--verbose]
```

The tool runs `properdocs serve -f <config>` from the site root. ProperDocs
builds the preview into a temporary folder, so `docs/` is left alone. Stop
the server with <kbd>Ctrl</kbd>+<kbd>C</kbd>; the tool prints `Server stopped`.

## `clean`

Empties the output folder without building.

```bash
vmt clean [--verbose]
```

Deletes every file and folder in `--docs` except `CNAME`, and logs
`Cleaned <docs> (preserved CNAME)`. Symbolic links are removed, not followed.

## `format`

Formats the Markdown source in place with Flowmark.

```bash
vmt format [--verbose]
```

The tool runs this command from the site root:

```bash
flowmark --inplace --nobackup --semantic --cleanups --smartquotes --ellipses --width 0 <src>
```

With these options Flowmark rewrites the files without keeping backups, applies
its cleanups, turns straight quotes into typographic quotes and `...` into `…`,
and does not wrap lines.

If `flowmark` is not on the `PATH`, the command logs this warning and returns
without an error:

```text
flowmark not on PATH; install the [flowmark] extra (`uv pip install vexy-mkdocs-tools[flowmark]`) to enable this step
```

## `version`

Prints the installed package version, for example `0.1.1`.

```bash
vmt version
```

## Logging

Messages go to standard error in the form `LEVEL    | message`. The default
level is `INFO`. Two settings change it:

- `--verbose` on any command except `version` sets the level to `DEBUG`. At
  that level `clean` and `build` also log every file they remove.
- The `VMT_LOG_LEVEL` environment variable sets the level when `--verbose` is
  not given, for example `VMT_LOG_LEVEL=WARNING vmt build`.

ProperDocs prints its own messages in its own format (`INFO    -  …`). The two
settings above do not affect them.
