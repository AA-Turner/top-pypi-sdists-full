"""Shared repository path utilities for the issue-template subsystem.

Provides ``_find_repo_root()`` and ``_PRESET_DIR_RELATIVE`` so that both
``commands.py`` and ``render_issue_md.py`` can use the same logic without
importing private names from each other.
"""

from __future__ import annotations

from pathlib import Path

_PRESET_DIR_RELATIVE = Path(".specify") / "presets" / "agdt-templates"


def _find_repo_root() -> Path | None:
    """Find the git repository root by walking up from cwd."""
    current = Path.cwd().resolve()
    while True:
        if (current / ".git").exists():
            return current
        parent = current.parent
        if parent == current:
            return None
        current = parent
