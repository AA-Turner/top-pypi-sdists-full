"""
Runs router — /api/runs/* (structured run lifecycle)
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger("cvc.gateway.runs")

router = APIRouter()

# In-process run state. Replaces the vendored api_server's self._run_statuses
# + self._run_event_queues dicts.
_runs: dict[str, dict] = {}


class CreateRunBody(BaseModel):
    session_id: str
    user_message: str
    workspace_path: str | None = None


@router.get("/runs")
async def list_runs(limit: int = 50):
    runs = sorted(
        _runs.values(),
        key=lambda r: r.get("created_at", 0),
        reverse=True,
    )[:limit]
    return {"runs": [_run_to_dict(r) for r in runs]}


@router.post("/runs")
async def create_run(body: CreateRunBody):
    """Create a new run. For now this kicks off a background agent invocation
    and returns the run_id immediately. The client polls /api/runs/{id}/events."""
    run_id = f"run_{uuid.uuid4().hex[:12]}"
    _runs[run_id] = {
        "run_id": run_id,
        "session_id": body.session_id,
        "status": "queued",
        "user_message": body.user_message,
        "workspace_path": body.workspace_path,
        "events": [],
        "created_at": time.time(),
        "updated_at": time.time(),
    }
    return {"run_id": run_id, "status": "queued"}


@router.get("/runs/{run_id}")
async def get_run(run_id: str):
    r = _runs.get(run_id)
    if not r:
        raise HTTPException(status_code=404, detail="run not found")
    return _run_to_dict(r)


@router.get("/runs/{run_id}/events")
async def get_run_events(run_id: str, since_seq: int = 0):
    r = _runs.get(run_id)
    if not r:
        raise HTTPException(status_code=404, detail="run not found")
    events = [e for e in r.get("events", []) if e.get("seq", 0) > since_seq]
    return {"run_id": run_id, "events": events}


@router.post("/runs/{run_id}/stop")
async def stop_run(run_id: str):
    r = _runs.get(run_id)
    if not r:
        raise HTTPException(status_code=404, detail="run not found")
    r["status"] = "stopped"
    r["updated_at"] = time.time()
    return _run_to_dict(r)


def _run_to_dict(r: dict) -> dict:
    return {
        "run_id": r.get("run_id"),
        "session_id": r.get("session_id"),
        "status": r.get("status"),
        "created_at": r.get("created_at"),
        "updated_at": r.get("updated_at"),
    }
