from __future__ import annotations
import json
from kanban_framework.infra.filesystem import Filesystem


class RecoveryManager:
    def __init__(self, fs: Filesystem):
        self._fs = fs

    def find_interrupted(self) -> list[dict]:
        interrupted = []
        for f in sorted(
            self._fs.kanban_dir.glob("tasks/TASK-*.json")
        ):
            data = json.loads(f.read_text(encoding="utf-8"))
            if data.get("status") in ("in_progress", "error"):
                interrupted.append({
                    "id": data["id"],
                    "phase": data.get("phase"),
                    "status": data.get("status"),
                })
        return interrupted

    def recover(self, task_id: str) -> dict:
        tf = self._fs.task_file(task_id)
        if not self._fs.file_exists(tf):
            return {"success": False, "reason": "task not found"}
        data = self._fs.read_json(tf)
        return {
            "success": True,
            "task_id": task_id,
            "current_phase": data.get("phase"),
        }

    def resume(self, task_id: str) -> dict:
        """Resume from current phase — return current state without changes."""
        tf = self._fs.task_file(task_id)
        if not self._fs.file_exists(tf):
            return {"success": False, "reason": "task not found"}
        data = self._fs.read_json(tf)
        return {
            "success": True,
            "task_id": task_id,
            "current_phase": data.get("phase"),
            "status": data.get("status"),
        }

    def rollback(self, task_id: str) -> dict:
        """Roll back to the previous phase and persist the change."""
        from kanban_framework.types import Phase
        from kanban_framework.infra.scheduler import Scheduler

        tf = self._fs.task_file(task_id)
        if not self._fs.file_exists(tf):
            return {"success": False, "reason": "task not found"}
        data = self._fs.read_json(tf)
        current_phase = Phase(data["phase"])
        prev = Scheduler.previous_phase(current_phase)
        if prev is None:
            return {
                "success": False,
                "reason": "no previous phase to roll back to",
            }
        data["phase"] = prev.value
        data["status"] = "in_progress"
        self._fs.write_json(tf, data)
        return {
            "success": True,
            "task_id": task_id,
            "rolled_back_to": prev.value,
            "from_phase": current_phase.value,
        }


def recover_list() -> list[dict]:
    from pathlib import Path
    fs = Filesystem(root=Filesystem.find_project_root())
    mgr = RecoveryManager(fs)
    return mgr.find_interrupted()


def recover_check_timeout(task_id: str) -> dict:
    from pathlib import Path
    fs = Filesystem(root=Filesystem.find_project_root())
    mgr = RecoveryManager(fs)
    return mgr.recover(task_id)


def resume_task(task_id: str) -> dict:
    from pathlib import Path
    fs = Filesystem(root=Filesystem.find_project_root())
    mgr = RecoveryManager(fs)
    return mgr.resume(task_id)


def rollback_task(task_id: str) -> dict:
    from pathlib import Path
    fs = Filesystem(root=Filesystem.find_project_root())
    mgr = RecoveryManager(fs)
    return mgr.rollback(task_id)
