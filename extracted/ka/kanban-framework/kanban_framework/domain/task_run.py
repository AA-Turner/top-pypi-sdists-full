"""TaskRun management — creation, completion, failure, listing.

Handles the lifecycle of individual agent runs within a task,
including reading/writing run JSON files and building worker context.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from kanban_framework.types import TaskRun


class RunManager:
    """Manages TaskRun records for a task."""

    def __init__(self, fs) -> None:
        self._fs = fs

    def create_run(self, task_id: str, phase: str, agent_role: str = "") -> TaskRun:
        """Create a new TaskRun. Caller is responsible for updating task counters."""
        run = TaskRun(
            run_id=0,
            task_id=task_id,
            phase=phase,
            agent_role=agent_role,
            status="active",
            started_at=str(time.time()),
        )
        return run

    def save_new_run(self, run: TaskRun) -> None:
        """Persist a newly created run (assigned run_id from caller)."""
        self._write_run(run)

    def complete_run(
        self, task_id: str, run_id: int,
        summary: str = "", metadata: dict | None = None,
    ) -> TaskRun:
        """Mark a run as completed with handoff summary and metadata."""
        run = self._read_run(task_id, run_id)
        run.status = "completed"
        run.summary = summary
        run.metadata = metadata or {}
        run.ended_at = str(time.time())
        _compute_duration(run)
        self._write_run(run)
        return run

    def fail_run(self, task_id: str, run_id: int, error: str = "") -> TaskRun:
        """Mark a run as failed with error description."""
        run = self._read_run(task_id, run_id)
        run.status = "failed"
        run.error = error
        run.ended_at = str(time.time())
        _compute_duration(run)
        self._write_run(run)
        return run

    def get_run(self, task_id: str, run_id: int) -> TaskRun | None:
        """Get a specific run record, or None if not found."""
        try:
            return self._read_run(task_id, run_id)
        except (FileNotFoundError, Exception):
            return None

    def list_runs(self, task_id: str) -> list[TaskRun]:
        """List all runs for a task, sorted by run_id."""
        runs_dir = self._fs.task_dir(task_id) / "runs"
        if not runs_dir.is_dir():
            return []
        runs = []
        for rf in sorted(runs_dir.glob("*.json")):
            try:
                data = json.loads(rf.read_text(encoding="utf-8"))
                runs.append(_run_from_dict(data))
            except (json.JSONDecodeError, Exception):
                pass
        return runs

    def build_worker_context(self, task_id: str) -> dict:
        """Build context dict for agent spawn prompt injection."""
        ctx: dict = {"prior_runs": [], "parent_handoffs": []}
        runs = self.list_runs(task_id)
        for r in runs:
            if r.status != "active":
                entry = {
                    "run_id": r.run_id,
                    "phase": r.phase,
                    "agent_role": r.agent_role,
                    "status": r.status,
                }
                if r.summary:
                    entry["summary"] = r.summary
                if r.error:
                    entry["error"] = r.error
                if r.metadata and r.metadata.get("decisions"):
                    entry["decisions"] = r.metadata["decisions"]
                ctx["prior_runs"].append(entry)
        return ctx

    # ── Internal helpers ────────────────────────────────────────────────

    def _runs_dir(self, task_id: str) -> Path:
        d = self._fs.task_dir(task_id) / "runs"
        self._fs.ensure_dir(d)
        return d

    def _run_path(self, task_id: str, run_id: int) -> Path:
        return self._runs_dir(task_id) / f"{run_id:03d}.json"

    def _write_run(self, run: TaskRun) -> None:
        data = {
            "run_id": run.run_id,
            "task_id": run.task_id,
            "phase": run.phase,
            "agent_role": run.agent_role,
            "status": run.status,
            "summary": run.summary,
            "metadata": run.metadata or {},
            "error": run.error,
            "started_at": run.started_at,
            "ended_at": run.ended_at,
            "duration_seconds": run.duration_seconds,
        }
        self._fs.write_json(self._run_path(run.task_id, run.run_id), data)

    def _read_run(self, task_id: str, run_id: int) -> TaskRun:
        data = self._fs.read_json(self._run_path(task_id, run_id))
        return _run_from_dict(data)


def _run_from_dict(data: dict) -> TaskRun:
    """Deserialize a dict into a TaskRun object."""
    return TaskRun(
        run_id=data["run_id"],
        task_id=data["task_id"],
        phase=data.get("phase", ""),
        agent_role=data.get("agent_role", ""),
        status=data.get("status", "active"),
        summary=data.get("summary", ""),
        metadata=data.get("metadata", {}),
        error=data.get("error", ""),
        started_at=data.get("started_at", ""),
        ended_at=data.get("ended_at", ""),
        duration_seconds=data.get("duration_seconds", 0.0),
    )


def _compute_duration(run: TaskRun) -> None:
    """Compute run duration from started_at to ended_at."""
    if run.started_at:
        try:
            run.duration_seconds = round(
                float(run.ended_at) - float(run.started_at), 1
            )
        except (ValueError, TypeError):
            pass
