"""Hatchling metadata hook to automatically generate 'all' extras.

This package provides a Hatchling metadata hook that automatically
creates an 'all' extra in your project's optional dependencies,
combining all dependencies from all other extras.
"""

from __future__ import annotations

__all__ = ["AutoExtrasMetadataHook", "__version__"]

from importlib.metadata import version

from hatchling_autoextras_hook.hooks import AutoExtrasMetadataHook

# The name of the distribution (not the import name) is a literal. The package
# must be installed to be loaded as a hatchling plugin, so a missing distribution
# is an error (`PackageNotFoundError`), not a reason to invent a version.
__version__: str = version("hatchling-autoextras-hook")
