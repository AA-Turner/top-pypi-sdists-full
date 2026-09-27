"""The hosted browser worker image is `uv sync --extra server`; the checkpoint
engine (zstd + AES-GCM) must ride that extra or every save is uncompressed.

Break caught 2026-09-26: six days of "zstandard is not installed" on every
worker task, 28 GB of uncompressed checkpoints, because `server` never named
`cloud_browser`.
"""

from __future__ import annotations

import tomllib
from pathlib import Path


def _extras() -> dict[str, list[str]]:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    return tomllib.loads(pyproject.read_text())["project"]["optional-dependencies"]


def test_server_extra_includes_the_checkpoint_engine() -> None:
    extras = _extras()
    assert "matrx-scraper[cloud_browser]" in extras["server"]
    engine = " ".join(extras["cloud_browser"])
    assert "zstandard" in engine and "cryptography" in engine


def test_dockerfile_builds_the_worker_from_the_server_extra() -> None:
    dockerfile = Path(__file__).resolve().parents[1] / "Dockerfile"
    text = dockerfile.read_text()
    assert "--extra server" in text, "the worker image must install the server extra"
