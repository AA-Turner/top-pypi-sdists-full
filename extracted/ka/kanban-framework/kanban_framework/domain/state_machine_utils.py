"""State machine utility functions — serialization and rollback.

Pure helper functions for the FSM that don't belong in the core
next_step orchestration logic.
"""

from __future__ import annotations

import json
import time

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.step_progress import load_progress, save_progress


def next_step_to_dict(result) -> dict:
    """Serialize a NextStepResult to a plain dict."""
    return {
        "task_id": result.task_id,
        "phase": result.phase,
        "step_id": result.step_id,
        "step_index": result.step_index,
        "total_steps": result.total_steps,
        "description": result.description,
        "step_type": result.step_type,
        "actions": result.actions,
        "agent_type": result.agent_type,
        "parallel": result.parallel,
        "user_action": result.user_action,
        "phase_complete": result.phase_complete,
        "all_complete": result.all_complete,
        "context_files": result.context_files,
        "knowledge_summary": result.knowledge_summary,
        "knowledge_context": result.knowledge_context,
        "depends_on_files": result.depends_on_files,
        "knowledge_available": result.knowledge_available,
        "message": result.message,
        "spawn_prompt": result.spawn_prompt,
        "interactive": result.interactive,
        "interactive_prompt": result.interactive_prompt,
        "available_steps": result.available_steps,
        "control_mode": result.control_mode,
    }


def rollback_step(fs: Filesystem, task_id: str, target_step_id: str) -> dict:
    """Reset target step and all subsequent steps to pending. Preserve artifacts."""
    from kanban_framework.domain.step_registry import build_step_dag

    progress = load_progress(fs, task_id)
    steps = progress.get("steps", {})

    try:
        task_path = fs.task_dir(task_id) / "task.json"
        task_data = json.loads(task_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": f"task {task_id} not found or invalid", "rolled_back": []}
    lightweight = task_data.get("lightweight", False)
    quick = task_data.get("mode") == "quick"

    dag = build_step_dag(lightweight=lightweight, quick=quick,
                         mode=task_data.get("mode"))
    all_step_ids = [s["id"] for s in dag["steps"]]

    try:
        target_idx = all_step_ids.index(target_step_id)
    except ValueError:
        return {"error": f"step {target_step_id} not found in workflow", "rolled_back": []}

    rolled_back = []
    for step_id in all_step_ids[target_idx:]:
        if step_id in steps:
            old_status = steps[step_id].get("status", "pending")
            if old_status != "pending":
                steps[step_id] = {"status": "pending", "updated_at": time.time()}
                rolled_back.append({"id": step_id, "from": old_status, "to": "pending"})

    progress["steps"] = steps
    save_progress(fs, task_id, progress)
    return {"task_id": task_id, "target": target_step_id, "rolled_back": rolled_back}
