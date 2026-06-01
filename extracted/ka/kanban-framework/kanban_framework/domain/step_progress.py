"""Progress tracking for kanban workflow steps.

Read/write progress.json per task — atomic writes via tmp+rename.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from kanban_framework.infra.filesystem import Filesystem


def _progress_path(fs: Filesystem, task_id: str) -> Path:
    return fs.task_dir(task_id) / "progress.json"


def load_progress(fs: Filesystem, task_id: str) -> dict:
    pp = _progress_path(fs, task_id)
    if pp.is_file():
        return json.loads(pp.read_text(encoding="utf-8"))
    return {"task_id": task_id, "steps": {}}


def save_progress(fs: Filesystem, task_id: str, progress: dict) -> None:
    """Atomically write progress.json via tmp + rename to prevent corruption."""
    pp = _progress_path(fs, task_id)
    pp.parent.mkdir(parents=True, exist_ok=True)
    tmp = pp.with_suffix(".tmp")
    tmp.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(pp)


def mark_step(fs: Filesystem, task_id: str, step_id: str, status: str = "completed") -> dict:
    progress = load_progress(fs, task_id)
    progress["steps"][step_id] = {
        "status": status,
        "updated_at": time.time(),
    }
    save_progress(fs, task_id, progress)
    return progress
