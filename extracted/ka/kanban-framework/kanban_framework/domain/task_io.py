"""Task JSON serialization and deserialization helpers.

Handles reading/writing Task objects to/from JSON files, including
legacy format migration for auto_mode and control_mode fields.
"""

from __future__ import annotations

from pathlib import Path

from kanban_framework.types import Task, TaskStatus, Phase, AutoMode, ControlMode


class TaskNotFoundError(Exception):
    pass


def read_task_file(fs, path: Path) -> Task:
    """Read and parse a task.json file into a Task object."""
    import json as _json
    try:
        data = fs.read_json(path)
    except (_json.JSONDecodeError, Exception) as e:
        raise TaskNotFoundError(
            f"Failed to parse task file {path}: {e}"
        ) from e

    auto_mode = _parse_auto_mode(data.get("auto_mode", {}))
    control_mode = _parse_control_mode(
        data.get("control_mode"),
        data.get("auto_mode", {}),
    )

    return Task(
        id=data["id"],
        title=data["title"],
        description=data.get("description", ""),
        status=TaskStatus(data.get("status", "pending")),
        phase=Phase(data["phase"]) if data.get("phase") else Phase.PLAN,
        iteration=data.get("iteration", 1),
        lightweight=data.get("lightweight", False),
        mode=data.get("mode", "full"),
        control_mode=control_mode,
        custom_fsm=data.get("custom_fsm"),
        history=data.get("history", []),
        scores=data.get("scores", {}),
        score_history=data.get("score_history", []),
        auto_mode=auto_mode,
        user_decision=data.get("user_decision"),
        test_config=data.get("test_config"),
        current_run_id=data.get("current_run_id", 0),
        total_runs=data.get("total_runs", 0),
        biz_tag=data.get("biz_tag"),
    )


def write_task_file(fs, task: Task) -> None:
    """Serialize and write a Task object to its task.json file."""
    data = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "phase": task.phase.value,
        "iteration": task.iteration,
        "lightweight": task.lightweight,
        "mode": task.mode,
        "control_mode": task.control_mode.value,
        "custom_fsm": task.custom_fsm,
        "history": task.history,
        "scores": task.scores,
        "score_history": task.score_history,
        "auto_mode": {
            "auto_brainstorm": task.auto_mode.auto_brainstorm,
            "auto_iteration": task.auto_mode.auto_iteration,
            "auto_lightweight": task.auto_mode.auto_lightweight,
            "auto_archive": task.auto_mode.auto_archive,
            "auto_worktree": task.auto_mode.auto_worktree,
        },
        "user_decision": task.user_decision,
        "test_config": task.test_config,
        "current_run_id": task.current_run_id,
        "total_runs": task.total_runs,
        "biz_tag": task.biz_tag,
    }
    task_dir = fs.task_dir(task.id)
    fs.ensure_dir(task_dir)
    fs.write_json(task_dir / "task.json", data)
    # Clean up old flat format
    old_file = fs.kanban_dir / "tasks" / f"{task.id}.json"
    if old_file.is_file():
        old_file.unlink()


def _parse_auto_mode(auto_mode_data) -> AutoMode:
    """Parse auto_mode from JSON data (dict, bool, or None)."""
    if isinstance(auto_mode_data, dict):
        return AutoMode(
            auto_brainstorm=auto_mode_data.get("auto_brainstorm", False),
            auto_iteration=auto_mode_data.get("auto_iteration", False),
            auto_lightweight=auto_mode_data.get("auto_lightweight", False),
            auto_archive=auto_mode_data.get("auto_archive", False),
            auto_worktree=auto_mode_data.get("auto_worktree", False),
        )
    if isinstance(auto_mode_data, bool):
        return AutoMode(
            auto_brainstorm=auto_mode_data,
            auto_iteration=auto_mode_data,
            auto_lightweight=auto_mode_data,
            auto_archive=auto_mode_data,
            auto_worktree=auto_mode_data,
        )
    return AutoMode()


def _parse_control_mode(raw, auto_mode_data: dict) -> ControlMode:
    """Parse control_mode from JSON with legacy auto_mode fallback."""
    if raw in ("auto", "semi", "manual"):
        return ControlMode(raw)
    if isinstance(auto_mode_data, dict) and all(auto_mode_data.values()):
        return ControlMode.AUTO
    return ControlMode.SEMI
