# Changelog

## [Unreleased]

### Changed (docs site and release scripts)
- Documentation moved from the hand-written Jekyll site in `docs/` to ProperDocs +
  MaterialX: source in `src_docs/md/` (9 pages), config in `src_docs/mkdocs.yml`,
  built into `docs/` by `src_docs/build.sh` and the new `Docs` workflow. Published at
  https://vexy.dev/vexy-mkdocs-tools/.
- `build.sh` builds docs and/or the package (`./build.sh [all|docs|package]`);
  `publish.sh` tags with `gitnextver`, builds and uploads with `uv publish`.
- `release.yml` publishes with `skip-existing: true`, so a version already uploaded
  by `publish.sh` does not fail the workflow.
- `pyproject.toml` gains a `Documentation` URL.

### Added
- End-to-end tests that build a real fixture site (`src_docs/md` + `mkdocs.yml`
  → `docs/`) with `properdocs`, asserting the page renders, `.nojekyll` is
  written, and a `src_docs/md/CNAME` is copied into the output. Skip gracefully
  when `properdocs` is not on PATH.
- Jekyll documentation site under `docs/` (Just the Docs remote theme)
  documenting the `mkdocs/mkdocs.yml` + `src_docs/md/` → `docs/` contract, the
  `materialx` theme name, and the `CNAME` convention.
- `CLAUDE.md` with `this_file:` map and pipeline notes for contributors.
- `TODO.md` capturing path-to-v1.0, robustness ideas, and known behavior notes.

### Changed
- `.gitignore` now excludes macOS `.DS_Store` and friends.

## [0.1.0]

### Added
- First PyPI release as `vexy-mkdocs-tools`.
- `build.sh` runs `uvx hatch clean` before building; `publish.sh` runs `gitnextver .`.

## [Unreleased]

### Added
- Initial scaffolding: `pyproject.toml` with hatchling + hatch-vcs, `requires-python = ">=3.12"`.
- `src/vexy_mkdocs_tools/cli.py` — Fire CLI with `build`, `serve`, `clean`, `format`, `version`.
- Console-script entry points `vexy-mkdocs-tools` and `vmt`.
- Bundled dependencies: ProperDocs 1.6.7+, MaterialX 10.1.4+, `pymdown-extensions`, `mkdocs-awesome-nav`, `mkdocs-include-markdown-plugin`, `mkdocs-llmstxt`, `mkdocs-copy-to-llm`, `mkdocs-rss-plugin`.
- Optional `[flowmark]` extra for in-place Markdown formatting.
- `tests/test_cli.py` — pytest smoke tests for `_clean_docs` (CNAME preservation) and `_find_repo_root` (walk-up + missing-root error).
- `build.sh`, `publish.sh` — local build/publish wrappers.
- GitHub Actions: `ci.yml` (test on push/PR), `release.yml` (publish to PyPI on `v*.*.*` tag).
- README with usage, layout convention, and dev workflow.
