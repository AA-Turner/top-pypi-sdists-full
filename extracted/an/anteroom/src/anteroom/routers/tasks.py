"""Background task output API endpoint (#1312)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request

router = APIRouter(tags=["tasks"])

_TASK_ID_RE = re.compile(r"^[0-9a-zA-Z_-]{1,64}$")


def _get_db(request: Request) -> Any:
    """Resolve request-scoped database connection (same pattern as chat.py)."""
    db_name = request.query_params.get("db")
    if hasattr(request.app.state, "db_manager"):
        return request.app.state.db_manager.get(db_name)
    return request.app.state.db


@router.get("/tasks")
async def list_tasks(
    request: Request,
    conversation_id: str = Query(..., min_length=1, max_length=64, pattern=r"^[0-9a-zA-Z_-]+$"),
) -> list[dict[str, Any]]:
    """List background tasks for a conversation."""
    bg_manager = getattr(request.app.state, "bg_manager", None)
    if bg_manager is None:
        return []
    db = _get_db(request)
    tasks = bg_manager.list_tasks(conversation_id, db=db)
    return [
        {
            "id": t["id"],
            "status": t.get("status", "unknown"),
            "command": t.get("command", ""),
            "preview": t.get("preview", ""),
            "created_at": t.get("created_at", ""),
            "completed_at": t.get("completed_at"),
        }
        for t in tasks
    ]


@router.get("/tasks/{task_id}")
async def get_task(request: Request, task_id: str) -> dict[str, Any]:
    """Get details for a specific background task."""
    if not _TASK_ID_RE.match(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    bg_manager = getattr(request.app.state, "bg_manager", None)
    if bg_manager is None:
        raise HTTPException(status_code=404, detail="Background task manager not available")

    db = _get_db(request)
    task = bg_manager.get_task(task_id, db=db)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": task["id"],
        "status": task.get("status", "unknown"),
        "command": task.get("command", ""),
        "preview": task.get("preview", ""),
        "created_at": task.get("created_at", ""),
        "completed_at": task.get("completed_at"),
        "conversation_id": task.get("conversation_id"),
    }


@router.get("/tasks/{task_id}/output")
async def get_task_output(
    request: Request,
    task_id: str,
    stream: str = Query("stdout", pattern="^(stdout|stderr)$"),
    tail: int | None = Query(None, ge=1, le=10000),
) -> dict[str, Any]:
    """Retrieve stdout or stderr output from a background task."""
    if not _TASK_ID_RE.match(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    bg_manager = getattr(request.app.state, "bg_manager", None)
    if bg_manager is None:
        raise HTTPException(status_code=404, detail="Background task manager not available")

    db = _get_db(request)
    task = bg_manager.get_task(task_id, db=db)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    from ..services.task_output import read_task_output, stderr_path, stdout_path

    conversation_id = task.get("conversation_id", "")
    data_dir: Path = bg_manager.data_dir

    if stream == "stderr":
        file_path = stderr_path(data_dir, conversation_id, task_id)
    else:
        file_path = stdout_path(data_dir, conversation_id, task_id)

    content = read_task_output(file_path, tail_lines=tail)

    return {
        "task_id": task_id,
        "stream": stream,
        "content": content,
        "status": task.get("status", "unknown"),
        "lines": content.count("\n") if content else 0,
    }
