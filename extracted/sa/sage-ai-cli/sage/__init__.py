"""Sage — a local-first AI coding CLI."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import re


def _read_pyproject_version() -> str | None:
    """Read the source-tree version when running from a checkout."""
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    if not pyproject.exists():
        return None

    match = re.search(r'^version = "([^"]+)"', pyproject.read_text(encoding="utf-8"), re.MULTILINE)
    if match:
        return match.group(1)
    return None


def _discover_version() -> str:
    source_version = _read_pyproject_version()
    if source_version:
        return source_version

    try:
        return version("sage-ai-cli")
    except PackageNotFoundError:
        return "0.0.0"


__version__ = _discover_version()
