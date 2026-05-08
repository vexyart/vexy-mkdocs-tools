# this_file: tests/test_cli.py
"""Smoke tests for vexy_mkdocs_tools.cli."""

from __future__ import annotations

from pathlib import Path

import pytest

from vexy_mkdocs_tools.cli import (
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
