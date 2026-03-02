"""Path utilities for dev mode.

Centralizes path resolution for SDK directories.
"""

from __future__ import annotations

from pathlib import Path


def get_sdk_root() -> Path | None:
    """Get the root directory of the plato-sdk package.

    Returns the directory containing pyproject.toml when installed in editable mode.
    Used for the sync_sdk feature in dev mode.
    Returns None if the package location cannot be determined.
    """
    import plato

    # plato.__file__ is /path/to/plato/__init__.py
    # SDK root is /path/to/ (contains pyproject.toml)
    if plato.__file__ is None:
        return None
    plato_package = Path(plato.__file__).resolve().parent
    return plato_package.parent
