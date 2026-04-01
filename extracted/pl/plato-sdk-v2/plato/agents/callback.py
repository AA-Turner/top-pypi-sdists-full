"""Backwards-compatible ChronosCallback helper."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ChronosCallback:
    """Minimal compatibility shim for older callback imports."""

    def __init__(self, callback_url: str, session_id: str) -> None:
        self.callback_url = callback_url
        self.session_id = session_id

    @property
    def enabled(self) -> bool:
        return bool(self.callback_url and self.session_id)

    def find_trajectory(self, root: str | Path) -> dict[str, Any] | None:
        trajectory_path = Path(root) / "agent" / "trajectory.json"
        if not trajectory_path.exists():
            return None
        return json.loads(trajectory_path.read_text())
