# TODO — vexy-mkdocs-tools

Bigger ideas and lower-priority work, parked here so the release stays focused.
Anything that changes what `build` produces needs a test proving equivalence
first — this tool is the shared build surface for every FontLab/Vexy site.

## Path to v1.0

- [ ] Commit to a stable CLI surface (flags, path conventions) and cut `v1.0.0`.
      The pipeline is settled; the blocker is a deliberate stability promise, not
      missing features.

## Robustness

- [ ] `--version` / `-V` top-level flag in addition to the `version` subcommand
      (Fire exposes subcommands, but a flag is what users reach for first).
- [ ] Fail fast in `serve` when the port is already in use, with a clear message
      naming the port (treat the error message as the product).
- [ ] Optional `--strict` passthrough to `properdocs build` so broken links fail
      the build in CI rather than shipping silently.

## Tests

- [ ] Add an end-to-end test for the Flowmark `format` step (currently only the
      no-Flowmark path is exercised; Flowmark is an optional dep and absent in
      the default test env).
- [ ] Add a `serve`-smoke test that starts and immediately stops the server, to
      guard the `--config` resolution without a long-running process.
- [ ] Wire `pytest-cov` into CI and enforce a coverage floor.

## Supply chain / CI

- [ ] Pin GitHub Actions to commit SHAs (currently major-version tags like
      `@v4`). A portfolio-wide decision — coordinate so all repos move together.
- [ ] Add a `cache` warm step or matrix entry for Python 3.14 once released.

## Docs

- [ ] Generate `docs/assets/icon.png` via `imgpt` using the ILLUSTRATION_PROMPT
      ("One command. All your vexy plugins. Your site deploys."). Deferred:
      image generation is gated behind the bulk-image-generation checkpoint and
      must be confirmed by the user before running (irreversible, costs API
      credits). Keep the file under 500 KB.
- [ ] Add a `site-template/` example (minimal `mkdocs/mkdocs.yml` +
      `src_docs/md/index.md`) a new site repo can copy verbatim.

## Known behavior notes (not bugs — document, do not "fix" without a test)

- A `CNAME` placed only in `docs/` is wiped by MkDocs' own pre-build clean during
  a full `build`; the durable home is `src_docs/md/CNAME`, which MkDocs copies to
  `docs/` every build. `_clean_docs` preserves `docs/CNAME` only for the
  standalone `clean` command. Documented in `docs/index.md`.
