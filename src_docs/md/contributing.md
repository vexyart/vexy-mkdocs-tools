# Contributing

`vexy-mkdocs-tools` is the shared build tool for many documentation sites. A
change to what `vmt build` produces changes every one of those sites. Add a test
that proves the new output is correct before you change the pipeline.

## Set up a development environment

1. Clone the repository:

    ```bash
    git clone https://github.com/vexyart/vexy-mkdocs-tools.git
    cd vexy-mkdocs-tools
    ```

2. Install the package and the development tools (`pytest`, `pytest-cov`,
   `ruff`):

    ```bash
    uv sync --extra dev
    ```

## Run the checks

```bash
uv run python -m pytest -q
uvx ruff check src tests
```

`tests/test_cli.py` covers:

- `_clean_docs`: creates a missing folder, and keeps `CNAME` while deleting
  everything else.
- `_find_repo_root`: finds the root from a nested folder, and raises
  `BuildError` when there is none.
- End-to-end builds of a small fixture site, which check that the page is
  rendered, `.nojekyll` is written and `src_docs/md/CNAME` reaches the output.
  These tests are skipped when `properdocs` is not on the `PATH`.

CI (`.github/workflows/ci.yml`) runs `ruff`, the tests and a package build on
Python 3.12 and 3.13 for every push and pull request to `main`.

## Code layout

| File | Contents |
|---|---|
| `src/vexy_mkdocs_tools/cli.py` | The whole tool: the `CLI` class with `build`, `serve`, `clean`, `format` and `version`, plus helper functions |
| `src/vexy_mkdocs_tools/__init__.py` | Exposes `__version__` |
| `src/vexy_mkdocs_tools/__main__.py` | Lets `python -m vexy_mkdocs_tools` run the tool |
| `src/vexy_mkdocs_tools/__version__.py` | Written by `hatch-vcs` at build time; ignored by git |

Every source file starts with a `this_file:` comment that gives its path.

## Build the package and this documentation

```bash
./build.sh            # documentation and package
./build.sh docs       # documentation only
./build.sh package    # dist/*.whl and dist/*.tar.gz, then twine check
```

This documentation does not use `vmt`. Its source is in `src_docs/md/`, its
configuration in `src_docs/mkdocs.yml`, and `src_docs/build.sh` builds it into
`docs/` with ProperDocs and MaterialX in strict mode. For a live preview:

```bash
src_docs/build.sh serve
```

The `Docs` workflow rebuilds `docs/` and commits it after every push to `main`
that changes `src_docs/`.

## Release

The version comes from the latest `vX.Y.Z` git tag through `hatch-vcs`.

`./publish.sh` releases from a local machine:

1. `uvx gitnextver` commits pending changes, tags the next `vX.Y.Z` and pushes.
2. `./build.sh package` builds the wheel and source distribution.
3. `uv publish dist/*` uploads them. It needs `UV_PUBLISH_TOKEN` or another
   `uv publish` credential.

The pushed tag also starts `.github/workflows/release.yml`. It lints, tests and
builds again, uploads to PyPI with Trusted Publishing, and creates a GitHub
release. The upload uses `skip-existing: true`, so it does not fail when
`publish.sh` has already uploaded that version.
