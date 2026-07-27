"""Item #4 — Auto-tier on hardware change."""

from __future__ import annotations

import json
import time
from pathlib import Path

__all__ = ["note_disk_now", "should_suggest_upgrade"]


_THRESHOLD_GB = 30.0


def _state_path() -> Path:
    p = Path.home() / ".sage" / ".hardware_state.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def note_disk_now(*, free_gb: float) -> None:
    _state_path().write_text(json.dumps({
        "free_gb": free_gb,
        "ts": time.time(),
    }))


def should_suggest_upgrade(*, current_free_gb: float) -> bool:
    p = _state_path()
    if not p.exists():
        return False
    try:
        data = json.loads(p.read_text())
        baseline = float(data.get("free_gb", 0.0))
    except (json.JSONDecodeError, OSError, ValueError):
        return False
    return current_free_gb - baseline >= _THRESHOLD_GB
