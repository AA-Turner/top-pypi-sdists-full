"""Node.js discovery — finds bundled or system Node.js / npm."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def find_node() -> str | None:
    """Return the path to the ``node`` executable.

    Search order:
      1. Bundled Node.js next to the frozen exe (``{exe_dir}/node/node.exe``)
      2. ``GHOST_NODE_DIR`` env var
      3. System PATH via ``shutil.which``
    """
    # 1. Frozen exe — installer puts node at {app}/node/node.exe
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).parent
        bundled = exe_dir / "node" / "node.exe"
        if bundled.is_file():
            return str(bundled)

    # 2. Explicit env var
    env_dir = os.environ.get("GHOST_NODE_DIR")
    if env_dir:
        candidate = Path(env_dir) / ("node.exe" if sys.platform == "win32" else "node")
        if candidate.is_file():
            return str(candidate)

    # 3. System PATH
    return shutil.which("node")


def find_npm() -> str | None:
    """Return the path to the ``npm`` executable (or npm.cmd on Windows).

    Search order mirrors :func:`find_node`.
    """
    # 1. Frozen exe — installer puts npm.cmd at {app}/node/npm.cmd
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).parent
        for name in ("npm.cmd", "npm"):
            bundled = exe_dir / "node" / name
            if bundled.is_file():
                return str(bundled)

    # 2. Explicit env var
    env_dir = os.environ.get("GHOST_NODE_DIR")
    if env_dir:
        for name in ("npm.cmd", "npm"):
            candidate = Path(env_dir) / name
            if candidate.is_file():
                return str(candidate)

    # 3. System PATH
    return shutil.which("npm")


def get_node_env() -> dict[str, str]:
    """Return a copy of ``os.environ`` with the bundled node dir prepended to PATH.

    This ensures child processes (e.g. ``npm install``) can also find the
    bundled Node.js without relying on the system PATH.
    """
    env = dict(os.environ)
    node = find_node()
    if node:
        node_dir = str(Path(node).parent)
        current_path = env.get("PATH", "")
        if node_dir.lower() not in current_path.lower():
            env["PATH"] = node_dir + os.pathsep + current_path
    return env
