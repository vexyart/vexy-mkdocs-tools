# this_file: tests/test_cli.py
"""Smoke tests for vexy_mkdocs_tools.cli."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from vexy_mkdocs_tools.cli import (
    CLI,
    BuildError,
    _clean_docs,
    _find_repo_root,
)


def test_clean_docs_creates_missing(tmp_path: Path) -> None:
    target = tmp_path / "docs"
    _clean_docs(target)
    assert target.is_dir()


def test_clean_docs_preserves_cname(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "CNAME").write_text("example.com\n", encoding="utf-8")
    (docs / "index.html").write_text("<html></html>", encoding="utf-8")
    nested = docs / "assets"
    nested.mkdir()
    (nested / "x.png").write_bytes(b"\x89PNG")

    _clean_docs(docs)

    assert (docs / "CNAME").read_text(encoding="utf-8") == "example.com\n"
    assert not (docs / "index.html").exists()
    assert not nested.exists()


def test_find_repo_root_walks_up(tmp_path: Path) -> None:
    root = tmp_path / "site"
    (root / "mkdocs").mkdir(parents=True)
    (root / "mkdocs" / "mkdocs.yml").write_text("site_name: x\n", encoding="utf-8")
    (root / "src_docs").mkdir()
    deep = root / "a" / "b" / "c"
    deep.mkdir(parents=True)

    assert _find_repo_root(start=deep) == root.resolve()


def test_find_repo_root_raises_when_missing(tmp_path: Path) -> None:
    with pytest.raises(BuildError, match="cannot locate site root"):
        _find_repo_root(start=tmp_path)


def _make_fixture_site(root: Path) -> None:
    """Write a minimal but real site: mkdocs/mkdocs.yml + src_docs/md/index.md.

    The theme is `materialx` because that is what the bundled MaterialX plugin
    registers; `material` is unrecognised in this stack.
    """
    (root / "mkdocs").mkdir(parents=True)
    (root / "src_docs" / "md").mkdir(parents=True)
    # docs_dir must be absolute so mkdocs resolves it independent of the config
    # file's own directory (mkdocs resolves relative dirs against the config).
    (root / "mkdocs" / "mkdocs.yml").write_text(
        f"site_name: Fixture\ndocs_dir: {root / 'src_docs' / 'md'}\ntheme:\n  name: materialx\n",
        encoding="utf-8",
    )
    (root / "src_docs" / "md" / "index.md").write_text(
        "# Fixture\n\nA tiny page.\n", encoding="utf-8"
    )


@pytest.mark.skipif(
    shutil.which("properdocs") is None,
    reason="properdocs not installed; end-to-end build cannot run",
)
def test_build_end_to_end_produces_site(tmp_path: Path) -> None:
    """Full pipeline against a real fixture: clean → properdocs build → .nojekyll.

    Proves the src_docs/md + mkdocs.yml -> docs/ contract that every consumer
    site depends on: a page is rendered and `.nojekyll` is written so GitHub
    Pages serves the built assets verbatim.
    """
    root = tmp_path / "site"
    _make_fixture_site(root)

    CLI(root=str(root)).build(no_format=True)

    docs = root / "docs"
    assert (docs / "index.html").is_file(), "page was not rendered"
    assert (docs / ".nojekyll").is_file(), ".nojekyll was not written"
    assert "Fixture" in (docs / "index.html").read_text(encoding="utf-8")


@pytest.mark.skipif(
    shutil.which("properdocs") is None,
    reason="properdocs not installed; end-to-end build cannot run",
)
def test_build_copies_cname_from_src_docs(tmp_path: Path) -> None:
    """A CNAME kept in src_docs/md/ survives into docs/ on every build.

    This is the mechanism real sites rely on for their custom domain: mkdocs
    copies non-Markdown files from docs_dir into the output, so the domain is
    reapplied on each deploy rather than depending on the pre-build clean.
    """
    root = tmp_path / "site"
    _make_fixture_site(root)
    (root / "src_docs" / "md" / "CNAME").write_text("example.com\n", encoding="utf-8")

    CLI(root=str(root)).build(no_format=True)

    assert (root / "docs" / "CNAME").read_text(encoding="utf-8").strip() == "example.com"
