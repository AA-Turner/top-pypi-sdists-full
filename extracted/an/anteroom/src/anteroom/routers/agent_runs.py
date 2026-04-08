"""Detached agent run API endpoints (#1314)."""

from __future__ import annotations

import re
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request

router = APIRouter(tags=["agent-runs"])

_RUN_ID_RE = re.compile(r"^[0-9a-zA-Z_-]{1,64}$")


def _get_db(request: Request) -> Any:
    """Resolve request-scoped database connection."""
    db_name = request.query_params.get("db")
    if hasattr(request.app.state, "db_manager"):
        return request.app.state.db_manager.get(db_name)
    return request.app.state.db


def _get_manager(request: Request) -> Any:
    mgr = getattr(request.app.state, "detach_manager", None)
    if mgr is None:
        raise HTTPException(status_code=503, detail="Detached agent manager not available")
    return mgr


@router.get("/agent-runs")
async def list_agent_runs(
    request: Request,
    conversation_id: str = Query(..., min_length=1, max_length=64, pattern=r"^[0-9a-zA-Z_-]+$"),
) -> list[dict[str, Any]]:
    """List detached agent runs for a conversation."""
    mgr = _get_manager(request)
    db = _get_db(request)
    runs = mgr.list_runs(conversation_id, db=db)
    return [
        {
            "run_id": r["id"],
            "status": r.get("status", "unknown"),
            "title": r.get("title", ""),
            "started_at": r.get("started_at"),
            "completed_at": r.get("completed_at"),
            "duration_ms": r.get("duration_ms"),
        }
        for r in runs
    ]


@router.get("/agent-runs/{run_id}")
async def get_agent_run(request: Request, run_id: str) -> dict[str, Any]:
    """Get details for a specific detached agent run."""
    if not _RUN_ID_RE.match(run_id):
        raise HTTPException(status_code=400, detail="Invalid run ID")
    mgr = _get_manager(request)
    db = _get_db(request)
    run = mgr.get_run(run_id, db=db)
    if run is None:
        raise HTTPException(status_code=404, detail="Agent run not found")
    meta = run.get("metadata") or {}
    raw_result = meta.get("task_result")
    if raw_result is not None:
        from ..services.task_result import TaskResult

        task_result = TaskResult.from_dict(raw_result)
        result = task_result.to_llm_dict()
        result["run_id"] = run["id"]
        result["title"] = run.get("title", "")
        result["started_at"] = run.get("started_at")
        result["completed_at"] = run.get("completed_at")
        result["duration_ms"] = run.get("duration_ms")
        result["parent_run_id"] = run.get("parent_run_id")
        return result
    # Legacy fallback for in-progress or pre-TaskResult runs
    return {
        "run_id": run["id"],
        "status": run["status"],
        "title": run.get("title", ""),
        "started_at": run.get("started_at"),
        "completed_at": run.get("completed_at"),
        "duration_ms": run.get("duration_ms"),
        "parent_run_id": run.get("parent_run_id"),
        "error": meta.get("error"),
    }


@router.delete("/agent-runs/{run_id}")
async def cancel_agent_run(request: Request, run_id: str) -> dict[str, Any]:
    """Cancel a running detached agent."""
    if not _RUN_ID_RE.match(run_id):
        raise HTTPException(status_code=400, detail="Invalid run ID")
    mgr = _get_manager(request)
    db = _get_db(request)
    if mgr.cancel(run_id, db=db):
        return {"status": "cancelled", "run_id": run_id}
    raise HTTPException(status_code=409, detail="Run is not in a cancellable state")


@router.post("/agent-runs/{run_id}/retry")
async def retry_agent_run(request: Request, run_id: str) -> dict[str, Any]:
    """Retry a failed/cancelled detached agent. Creates a new run with parent linkage."""
    if not _RUN_ID_RE.match(run_id):
        raise HTTPException(status_code=400, detail="Invalid run ID")
    mgr = _get_manager(request)
    db = _get_db(request)
    try:
        # Recreate the same runtime context that normal web chat runs get
        from ..services.ai_service import create_ai_service
        from ..tools import ToolRegistry, register_default_tools

        config = request.app.state.config
        ai_service = create_ai_service(config.ai)
        tool_registry = ToolRegistry()
        if config.safety:
            tool_registry.set_safety_config(config.safety)
        rate_limiter = getattr(request.app.state, "tool_rate_limiter", None)
        if rate_limiter:
            tool_registry.set_rate_limiter(rate_limiter)
        register_default_tools(tool_registry)
        mcp_manager = getattr(request.app.state, "mcp_manager", None)

        result = mgr.retry(
            run_id,
            db=db,
            ai_service=ai_service,
            tool_registry=tool_registry,
            mcp_manager=mcp_manager,
            config=config.safety.subagent if config.safety else None,
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
