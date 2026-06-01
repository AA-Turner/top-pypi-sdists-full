from __future__ import annotations
from pathlib import Path
from kanban_framework.infra.filesystem import Filesystem


class ProgressTracker:
    def __init__(self, fs: Filesystem):
        self._fs = fs

    def subtask_start(self, task_id: str, subtask_id: str) -> None:
        checkpoint = self._checkpoint_file(task_id)
        self._fs.ensure_dir(checkpoint.parent)
        data = (
            self._fs.read_json(checkpoint)
            if self._fs.file_exists(checkpoint)
            else {}
        )
        data[subtask_id] = {"status": "in_progress", "started": True}
        self._fs.write_json(checkpoint, data)

    def subtask_done(self, task_id: str, subtask_id: str,
                     commit_hash: str | None = None,
                     files: list[str] | None = None) -> None:
        checkpoint = self._checkpoint_file(task_id)
        data = (
            self._fs.read_json(checkpoint)
            if self._fs.file_exists(checkpoint)
            else {}
        )
        entry: dict = {"status": "completed"}
        if commit_hash:
            entry["commit_hash"] = commit_hash
        if files:
            entry["files"] = files
        data[subtask_id] = entry
        self._fs.write_json(checkpoint, data)

    def progress(self, task_id: str) -> dict:
        checkpoint = self._checkpoint_file(task_id)
        if not self._fs.file_exists(checkpoint):
            return {"total": 0, "completed": 0}
        data = self._fs.read_json(checkpoint)
        subtasks = {k: v for k, v in data.items() if not k.startswith("C-")}
        c_items = {k: v for k, v in data.items() if k.startswith("C-")}
        total = len(subtasks)
        completed = sum(
            1 for v in subtasks.values() if v.get("status") == "completed"
        )
        return {
            "total": total, "completed": completed,
            "c_class_pending": len([v for v in c_items.values()
                                    if v.get("status") != "processed"]),
        }

    def add_c_class(self, task_id: str, description: str,
                    source: str = "evaluation") -> str:
        """Add a C-class entry (evaluation improvement suggestion).
        Returns the assigned C-class ID."""
        checkpoint = self._checkpoint_file(task_id)
        self._fs.ensure_dir(checkpoint.parent)
        data = (
            self._fs.read_json(checkpoint)
            if self._fs.file_exists(checkpoint)
            else {}
        )
        c_ids = [k for k in data if k.startswith("C-")]
        next_num = len(c_ids) + 1
        c_id = f"C-{next_num:03d}"
        data[c_id] = {
            "status": "pending",
            "description": description,
            "source": source,
        }
        self._fs.write_json(checkpoint, data)
        return c_id

    def list_c_class(self, task_id: str) -> list[dict]:
        """List all pending C-class entries."""
        checkpoint = self._checkpoint_file(task_id)
        if not self._fs.file_exists(checkpoint):
            return []
        data = self._fs.read_json(checkpoint)
        return [
            {"id": k, **v}
            for k, v in data.items()
            if k.startswith("C-") and v.get("status") != "processed"
        ]

    def _checkpoint_file(self, task_id: str) -> Path:
        return self._fs.task_dir(task_id) / "progress.json"
