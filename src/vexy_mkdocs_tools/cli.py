# this_file: src/vexy_mkdocs_tools/cli.py
"""Fire CLI for vexy-mkdocs-tools.

Wraps ProperDocs build/serve with the conventions used by the FontLab/Vexy
sites: a `mkdocs/mkdocs.yml` config, a `docs/` output directory whose `CNAME`
is preserved across cleans, and an optional Flowmark formatting pass over
`src_docs/md/` before each build.

Usage::

    uvx vexy-mkdocs-tools build              # full build pipeline
    uvx vexy-mkdocs-tools serve              # live-reload preview
    uvx vexy-mkdocs-tools clean              # wipe docs/ but keep CNAME
    uvx vexy-mkdocs-tools format             # Flowmark in-place format

Site layout (overridable via flags / constructor args)::

    <root>/
        mkdocs/mkdocs.yml
        src_docs/md/
        docs/                 (build output)
"""

from __future__ import annotations

import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import fire
from loguru import logger


class BuildError(RuntimeError):
    """Raised when the build pipeline cannot proceed."""


def _configure_logging(verbose: bool) -> None:
    import os

    level = "DEBUG" if verbose else os.environ.get("VMT_LOG_LEVEL", "INFO").upper()
    logger.remove()
    logger.add(sys.stderr, level=level, format="<level>{level: <8}</level> | {message}")


def _find_repo_root(start: Path | None = None) -> Path:
    """Walk up until we find a dir containing both `mkdocs/mkdocs.yml` and `src_docs`."""
    cur = (start or Path.cwd()).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "mkdocs" / "mkdocs.yml").is_file() and (
            candidate / "src_docs"
        ).is_dir():
            return candidate
    raise BuildError(
        "cannot locate site root (no mkdocs/mkdocs.yml + src_docs/ found "
        "walking up from cwd). Pass --root explicitly."
    )


def _clean_docs(docs_dir: Path) -> None:
    """Remove everything in `docs_dir` except `CNAME`. Recreate if missing."""
    if not docs_dir.exists():
        docs_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created {docs_dir}")
        return
    cname_content: str | None = None
    cname_path = docs_dir / "CNAME"
    if cname_path.is_file():
        cname_content = cname_path.read_text(encoding="utf-8")
        logger.debug(f"Preserving CNAME: {cname_content.strip()!r}")
    for child in docs_dir.iterdir():
        if child.name == "CNAME":
            continue
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
        logger.debug(f"Removed {child}")
    if cname_content is not None:
        cname_path.write_text(cname_content, encoding="utf-8")
    logger.info(f"Cleaned {docs_dir} (preserved CNAME)")


def _run(cmd: list[str], cwd: Path) -> None:
    logger.info(f"Running: {shlex.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=cwd)


def _flowmark_available() -> bool:
    return shutil.which("flowmark") is not None


def _format_with_flowmark(src_docs_dir: Path, root: Path) -> None:
    if not src_docs_dir.is_dir():
        raise BuildError(f"source Markdown directory missing: {src_docs_dir}")
    if not _flowmark_available():
        logger.warning(
            "flowmark not on PATH; install the [flowmark] extra "
            "(`uv pip install vexy-mkdocs-tools[flowmark]`) to enable this step"
        )
        return
    cmd = [
        "flowmark",
        "--inplace",
        "--nobackup",
        "--semantic",
        "--cleanups",
        "--smartquotes",
        "--ellipses",
        "--width",
        "0",
        str(src_docs_dir),
    ]
    _run(cmd, root)
    logger.info("Formatted source Markdown with Flowmark")


class CLI:
    """vexy-mkdocs-tools build orchestrator."""

    def __init__(
        self,
        root: str | None = None,
        config: str | None = None,
        docs: str | None = None,
        src: str | None = None,
    ) -> None:
        self._root = Path(root).resolve() if root else _find_repo_root()
        self._config = (
            Path(config).resolve() if config else self._root / "mkdocs" / "mkdocs.yml"
        )
        self._docs_dir = Path(docs).resolve() if docs else self._root / "docs"
        self._src_docs_dir = Path(src).resolve() if src else self._root / "src_docs" / "md"

    def clean(self, verbose: bool = False) -> None:
        """Remove everything in docs/ except CNAME."""
        _configure_logging(verbose)
        try:
            _clean_docs(self._docs_dir)
        except BuildError as exc:
            logger.error(str(exc))
            sys.exit(1)

    def format(self, verbose: bool = False) -> None:
        """Format src_docs/md/ in place via Flowmark."""
        _configure_logging(verbose)
        try:
            _format_with_flowmark(self._src_docs_dir, self._root)
        except (BuildError, subprocess.CalledProcessError) as exc:
            logger.error(str(exc))
            sys.exit(1)

    def build(self, verbose: bool = False, no_format: bool = False) -> None:
        """Run full pipeline: format → clean → properdocs build → write .nojekyll."""
        _configure_logging(verbose)
        try:
            if not no_format:
                _format_with_flowmark(self._src_docs_dir, self._root)
            _clean_docs(self._docs_dir)
            if not self._config.is_file():
                raise BuildError(f"mkdocs config missing: {self._config}")
            _run(
                [
                    "properdocs",
                    "build",
                    "-f",
                    str(self._config),
                    "-d",
                    str(self._docs_dir),
                ],
                self._root,
            )
            (self._docs_dir / ".nojekyll").touch()
            logger.info("Build complete")
        except BuildError as exc:
            logger.error(str(exc))
            sys.exit(1)
        except subprocess.CalledProcessError as exc:
            logger.error(f"build failed (exit {exc.returncode})")
            sys.exit(1)

    def serve(self, verbose: bool = False) -> None:
        """Live-reload preview via properdocs serve."""
        _configure_logging(verbose)
        try:
            if not self._config.is_file():
                raise BuildError(f"mkdocs config missing: {self._config}")
            _run(["properdocs", "serve", "-f", str(self._config)], self._root)
        except BuildError as exc:
            logger.error(str(exc))
            sys.exit(1)
        except subprocess.CalledProcessError as exc:
            logger.error(f"properdocs serve failed (exit {exc.returncode})")
            sys.exit(1)
        except KeyboardInterrupt:
            logger.info("Server stopped")

    def version(self) -> None:
        """Print the installed package version."""
        from vexy_mkdocs_tools import __version__

        print(__version__)


def main() -> None:
    """Console-script entry point for `vexy-mkdocs-tools` and `vmt`."""
    fire.Fire(CLI)


if __name__ == "__main__":
    main()
