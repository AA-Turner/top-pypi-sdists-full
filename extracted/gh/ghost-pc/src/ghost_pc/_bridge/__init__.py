"""Bridge path helper — locates bundled bridge files."""

from __future__ import annotations

import importlib.resources
import os
import sys
from pathlib import Path


def get_bundled_bridge_path() -> Path | None:
    """Return the directory containing bundled index.js and package.json.

    Search order:
      1. GHOST_BRIDGE_DIR env var (set by rthook_bridge.py in frozen builds)
      2. PyInstaller frozen exe (_MEIPASS/ghost_pc/_bridge/)
      3. Installer-bundled bridge ({app}/bridge/ — includes node_modules)
      4. PyInstaller onedir (exe parent/_internal/ghost_pc/_bridge/)
      5. importlib.resources (pip wheel install)
      6. Repository root fallback (editable/dev install)

    Returns None if the bundled files are not available.
    """
    # 1. Explicit env var (set by runtime hook or user)
    env_dir = os.environ.get("GHOST_BRIDGE_DIR")
    if env_dir:
        p = Path(env_dir)
        if (p / "index.js").exists():
            return p

    # 2. PyInstaller frozen exe — _MEIPASS (works for both onefile and onedir)
    meipass: str | None = getattr(sys, "_MEIPASS", None)
    if meipass is not None:
        frozen_dir = Path(meipass) / "ghost_pc" / "_bridge"
        if (frozen_dir / "index.js").exists():
            return frozen_dir

    # 3. Installer-bundled bridge — {app}/bridge/ (includes pre-built node_modules)
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).parent
        installer_bridge = exe_dir / "bridge"
        if (installer_bridge / "index.js").exists():
            return installer_bridge

    # 4. PyInstaller onedir — files next to the exe under _internal/
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).parent
        internal_dir = exe_dir / "_internal" / "ghost_pc" / "_bridge"
        if (internal_dir / "index.js").exists():
            return internal_dir

    # 4. importlib.resources — pip wheel install
    try:
        ref = importlib.resources.files("ghost_pc._bridge")
        bridge_dir = Path(str(ref))
        if (bridge_dir / "index.js").exists():
            return bridge_dir
    except (TypeError, FileNotFoundError):
        pass

    # 5. Repository root fallback — editable/dev install
    #    __file__ is at src/ghost_pc/_bridge/__init__.py
    #    repo root is 3 levels up, bridge/ is at repo root
    repo_bridge = Path(__file__).resolve().parent.parent.parent.parent / "bridge"
    if (repo_bridge / "index.js").exists():
        return repo_bridge

    return None
