"""Shared helpers for reading workflow issue state from git worktrees."""

from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def git_common_dir(root: Path) -> Path:
    """Return the git common directory for *root* (handles worktrees)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-common-dir"],
            capture_output=True,
            text=True,
            cwd=str(root),
            timeout=10,
        )
        if result.returncode != 0:
            raise ValueError(f"git rev-parse failed: {result.stderr.strip()}")
        raw = result.stdout.strip()
        path = Path(raw)
        if not path.is_absolute():
            path = (root / path).resolve()
        return path
    except FileNotFoundError:
        raise ValueError("git is not available on PATH")


def issue_state_dir(root: Path, issue_number: int) -> Path:
    """Return the shared state directory for an issue workflow."""
    common = git_common_dir(root)
    return common / "anteroom-workflows" / f"issue-{issue_number}"


def read_issue_state(root: Path, issue_number: int) -> dict[str, Any] | None:
    """Read and parse the state.json for an issue workflow, or None if missing."""
    state_file = issue_state_dir(root, issue_number) / "state.json"
    if not state_file.exists():
        return None
    try:
        return json.loads(state_file.read_text(encoding="utf-8"))  # type: ignore[no-any-return]
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read issue state %s: %s", state_file, exc)
        return None
