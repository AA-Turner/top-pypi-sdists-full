"""CLI version output helpers."""
from __future__ import annotations

import re


def get_version() -> str:
    """Return the installed kanban-framework version string."""
    try:
        from importlib.metadata import version
        return version("kanban-framework")
    except Exception:
        pass
    try:
        from pathlib import Path
        cfg = Path(__file__).resolve().parent.parent / "pyproject.toml"
        if cfg.is_file():
            text = cfg.read_text(encoding="utf-8")
            m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
            if m:
                return m.group(1)
    except Exception:
        pass
    return "unknown"
