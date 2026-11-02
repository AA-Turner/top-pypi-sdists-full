"""Checks for optional Dreamscale dependency bundles."""

from __future__ import annotations

from importlib import metadata

from dreamscale import errors


def require_so101_extra() -> None:
    """Raise an actionable Dreamscale error when SO-101 dependencies are absent."""
    try:
        metadata.version("lerobot")
    except metadata.PackageNotFoundError as exc:
        raise errors.catalog("so101_not_installed") from exc
