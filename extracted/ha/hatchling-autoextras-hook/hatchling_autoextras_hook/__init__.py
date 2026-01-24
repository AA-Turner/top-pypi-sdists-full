"""Hatchling metadata hook to automatically generate 'all' extras.

This package provides a Hatchling metadata hook that automatically
creates an 'all' extra in your project's optional dependencies,
combining all dependencies from all other extras.
"""

from __future__ import annotations

__all__ = ["AutoExtrasMetadataHook", "__version__"]

from importlib.metadata import PackageNotFoundError, version

from hatchling_autoextras_hook.hooks import AutoExtrasMetadataHook

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    # Package is not installed, fallback if needed
    __version__ = "0.0.0"
