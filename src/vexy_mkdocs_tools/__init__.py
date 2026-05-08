# this_file: src/vexy_mkdocs_tools/__init__.py
"""vexy-mkdocs-tools: Fire CLI wrapper around ProperDocs/MaterialX."""

from __future__ import annotations

try:
    from vexy_mkdocs_tools.__version__ import __version__
except ImportError:  # editable install before hatch-vcs has run
    __version__ = "0.0.0+local"

__all__ = ["__version__"]
