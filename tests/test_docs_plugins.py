# this_file: tests/test_docs_plugins.py
"""Build the supported plugin combination and inspect its reader-facing output."""

import json
import subprocess
import sys
from pathlib import Path


def test_plugin_stack_renders_sources_navigation_tags_and_print(tmp_path: Path) -> None:
    docs = tmp_path / "md"
    docs.mkdir()
    (tmp_path / "example.py").write_text(
        'def greet(name: str) -> str:\n    """Return a greeting."""\n    return f"Hello {name}"\n'
    )
    (tmp_path / "shared.md").write_text("A maintained shared paragraph.\n")
    (docs / ".meta.yml").write_text("tags: [Guide]\n")
    (docs / ".nav.yml").write_text("nav:\n  - Home: index.md\n  - API: api.md\n")
    (docs / "index.md").write_text(
        '# Plugin fixture\n\n{% include-markdown "../shared.md" %}\n\n'
        "<!--codeinclude-->\n[Greeting](../example.py)\n<!--/codeinclude-->\n\n"
        "Read [the greeting API][example.greet].\n"
    )
    (docs / "api.md").write_text("# API\n\n::: example.greet\n")
    config = tmp_path / "mkdocs.yml"
    config.write_text(
        "site_name: Plugin fixture\ndocs_dir: md\ntheme:\n  name: materialx\n"
        "plugins:\n  - materialx/search\n  - materialx/meta\n  - materialx/tags\n"
        "  - awesome-nav\n  - include-markdown\n"
        "  - codeinclude:\n      title_mode: mkdocs-material\n"
        "  - autorefs\n  - mkdocstrings:\n      handlers:\n        python:\n"
        "          paths: [.]\n          options:\n            allow_inspection: false\n"
        "  - print-site\nmarkdown_extensions:\n  - pymdownx.highlight\n"
        "  - pymdownx.superfences\n"
    )
    result = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "-f", str(config)],
        text=True,
        capture_output=True,
        cwd=tmp_path,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    home = (tmp_path / "site/index.html").read_text()
    api = (tmp_path / "site/api/index.html").read_text()
    assert "A maintained shared paragraph." in home, "Markdown include was not rendered"
    assert "Hello" in home and "codeinclude--&gt;" not in home, "source include was not rendered"
    assert 'href="api/#example.greet"' in home, "autorefs did not resolve the API link"
    assert "md-tag" in home and "Guide" in home, "inherited tags were not rendered"
    assert 'id="example.greet"' in api, "Python source documentation is missing"
    printed = (tmp_path / "site/print_page/index.html").read_text()
    assert "Return a greeting." in printed, "print view omitted API content"
    search = json.loads((tmp_path / "site/search/search_index.json").read_text())
    assert any("maintained shared paragraph" in x["text"] for x in search["docs"]), (
        "included content was not indexed"
    )
