"""Web asset path resolver for GhostPC GUI."""

from __future__ import annotations

import sys
from pathlib import Path


def get_web_root() -> Path:
    """Return the directory containing ``static/`` and ``templates/``.

    Handles PyInstaller frozen builds (``sys._MEIPASS``) the same way
    ``_bridge/__init__.py`` does for bridge files.
    """
    # PyInstaller frozen exe — assets under sys._MEIPASS
    meipass: str | None = getattr(sys, "_MEIPASS", None)
    if meipass is not None:
        frozen_dir = Path(meipass) / "ghost_pc" / "web"
        if (frozen_dir / "templates").is_dir():
            return frozen_dir

    # Normal install — this file lives at ghost_pc/web/__init__.py
    return Path(__file__).parent
