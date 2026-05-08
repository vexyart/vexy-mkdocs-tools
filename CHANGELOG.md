# Changelog

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
