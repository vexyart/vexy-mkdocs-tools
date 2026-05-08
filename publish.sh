#!/usr/bin/env bash
# this_file: publish.sh
# Publish to PyPI. Requires UV_PUBLISH_TOKEN or `uv publish` interactive auth.
# Tag a release first: `git tag v0.1.0 && git push --tags`.
set -euo pipefail
cd "$(dirname "$0")"

./build.sh
uv publish dist/*
