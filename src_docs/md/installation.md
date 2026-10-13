# Installation

## Requirements

- Python 3.12 or later.
- [`uv`](https://docs.astral.sh/uv/) is recommended. Plain `pip` also works.

## Run without installing

`uvx` downloads the package into a cached environment and runs it:

```bash
uvx vexy-mkdocs-tools build
```

To include the optional Flowmark formatter in the same run:

```bash
uvx --with flowmark vexy-mkdocs-tools build
```

## Install into an environment

```bash
uv pip install vexy-mkdocs-tools
```

With the Flowmark formatter:

```bash
uv pip install "vexy-mkdocs-tools[flowmark]"
```

With `pip`, use the same package names:

```bash
pip install "vexy-mkdocs-tools[flowmark]"
```

Both commands also install ProperDocs, the MaterialX theme and the bundled
plugins, listed on the [home page](index.md#what-it-installs).

## Install as a tool

To keep `vmt` on your `PATH` without activating an environment:

```bash
uv tool install vexy-mkdocs-tools
```

## Check the installation

`vmt` looks for a site before it runs any command, including `version`. Run the
check from inside a site folder (see [Site layout](site-layout.md)), or name a
folder with `--root`:

```bash
vmt --root path/to/site version
```

The command prints the installed version, for example `0.1.1`.

!!! note
    Outside a site folder and without `--root`, every command stops with a
    `BuildError: cannot locate site root …` traceback. See
    [Troubleshooting](troubleshooting.md#cannot-locate-site-root).
