"""REST API for workflow monitoring and execution.

Server-mode execution: POST /workflow-runs enqueues runs for the background
executor (#888). All other endpoints remain read-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

router = APIRouter(tags=["workflows"])

_MAX_INPUTS_BYTES = 65536  # 64KB cap on serialized inputs


class EnqueueRunRequest(BaseModel):
    workflow_id: str = Field(max_length=128)
    target_kind: str = Field(default="generic", max_length=64)
    target_ref: str = Field(max_length=512)
    inputs: dict[str, Any] | None = None
    params: dict[str, str] | None = None
    space_id: str | None = None


def _get_db(request: Request) -> Any:
    if hasattr(request.app.state, "db_manager"):
        db_name = request.query_params.get("db", "personal")
        return request.app.state.db_manager.get(db_name)
    return request.app.state.db


@router.post("/workflow-runs", status_code=201)
async def enqueue_workflow_run(request: Request, body: EnqueueRunRequest) -> dict[str, str]:
    """Enqueue a workflow run for background execution.

    Returns 201 with the run ID. Requires the executor to be enabled.
    """
    config = request.app.state.config
    if not config.workflow.executor_enabled:
        raise HTTPException(status_code=503, detail="Workflow executor is not enabled")

    # Validate inputs size
    if body.inputs:
        serialized = json.dumps(body.inputs)
        if len(serialized.encode("utf-8")) > _MAX_INPUTS_BYTES:
            raise HTTPException(status_code=422, detail="Inputs exceed 64KB limit")

    # Resolve workflow
    from ..services.workflow_resolution import resolve_workflow_path

    path = resolve_workflow_path(body.workflow_id, allow_filesystem=False)
    if not path:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Load and validate definition
    from ..services.workflow_engine import WorkflowEngine, load_definition
    from ..services.workflow_runners import create_default_registry

    try:
        definition = load_definition(path)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid workflow definition")

    # Build engine with the same runtime seams as the executor dispatch path:
    # credential resolver, egress config, registries. This ensures enqueue_run()
    # validation (credentials, hooks, publish URLs) matches what execute_enqueued_run()
    # will see at dispatch time.
    db = _get_db(request)
    from ..services.workflow_credentials import CredentialResolver

    # Register spec phase gate conditions (#997)
    try:
        from ..services.spec_gates import register_spec_gates

        register_spec_gates(db)
    except Exception:
        pass

    cred_resolver = CredentialResolver(config.workflow.credentials)
    engine = WorkflowEngine(
        db,
        config.workflow,
        create_default_registry(),
        event_bus=getattr(request.app.state, "event_bus", None),
        credential_resolver=cred_resolver,
        artifact_registry=getattr(request.app.state, "artifact_registry", None),
        skill_registry=getattr(request.app.state, "skill_registry", None),
        egress_allowed_domains=config.ai.allowed_domains,
        egress_block_localhost=config.ai.block_localhost_api,
        audit_writer=getattr(request.app.state, "audit_writer", None),
    )
    try:
        run = await engine.enqueue_run(
            definition,
            target_kind=body.target_kind,
            target_ref=body.target_ref,
            inputs=body.inputs,
            space_id=body.space_id,
            trigger_source="web_api",
            param_overrides=body.params,
        )
    except ValueError:
        raise HTTPException(status_code=422, detail="Workflow validation failed")

    return {"run_id": run["id"]}


@router.get("/workflows")
async def list_workflows(request: Request) -> list[dict[str, Any]]:
    """List available workflow definitions."""
    definitions = []
    seen_ids: set[str] = set()
    # Built-in workflows
    builtin_dir = Path(__file__).parent.parent / "workflows"
    if builtin_dir.exists():
        for f in sorted(builtin_dir.glob("*.yaml")):
            definitions.append({"id": f.stem, "source": "built_in"})
            seen_ids.add(f.stem)
    # Package-shipped examples
    pkg_examples = Path(__file__).parent.parent / "workflows" / "examples"
    if pkg_examples.exists():
        for f in sorted(pkg_examples.glob("*.yaml")):
            if f.stem not in seen_ids:
                definitions.append({"id": f.stem, "source": "example"})
                seen_ids.add(f.stem)
    # Source-tree examples (development)
    src_examples = Path(__file__).parent.parent.parent.parent / "examples" / "workflows"
    if src_examples.exists():
        for f in sorted(src_examples.glob("*.yaml")):
            if f.stem not in seen_ids:
                definitions.append({"id": f.stem, "source": "example"})
                seen_ids.add(f.stem)
    return definitions


@router.get("/workflow-runs")
async def list_workflow_runs(
    request: Request,
    status: str | None = Query(default=None),
    workflow_id: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[dict[str, Any]]:
    """List workflow runs with optional filters."""
    from ..services.workflow_storage import list_workflow_runs as ws_list

    db = _get_db(request)
    runs = ws_list(db, status=status, workflow_id=workflow_id, limit=limit, offset=offset)
    return runs


@router.get("/workflow-runs/{run_id}")
async def get_workflow_run(request: Request, run_id: str) -> dict[str, Any]:
    """Get detailed status of a workflow run including step history."""
    from ..services.workflow_storage import (
        count_checkpoints,
        get_pending_approval,
        get_pending_decision,
        list_workflow_steps,
    )
    from ..services.workflow_storage import (
        get_workflow_run as ws_get,
    )

    db = _get_db(request)
    run = ws_get(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    steps = list_workflow_steps(db, run_id)
    pending_approval = get_pending_approval(db, run_id)
    pending_decision = get_pending_decision(db, run_id)
    checkpoint_count = count_checkpoints(db, run_id)

    # Strip definition_content to prevent info disclosure (#970)
    run.pop("definition_content", None)

    return {
        **run,
        "steps": steps,
        "pending_approval": pending_approval,
        "pending_decision": pending_decision,
        "checkpoint_count": checkpoint_count,
    }


@router.get("/workflow-runs/{run_id}/checkpoints")
async def get_workflow_checkpoints(request: Request, run_id: str) -> dict[str, Any]:
    """List checkpoints for a workflow run."""
    from ..services.workflow_storage import get_workflow_run as ws_get
    from ..services.workflow_storage import list_checkpoints

    db = _get_db(request)
    run = ws_get(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    checkpoints = list_checkpoints(db, run_id)
    return {"checkpoints": checkpoints}


@router.get("/workflow-runs/{run_id}/events")
async def get_workflow_events(request: Request, run_id: str) -> list[dict[str, Any]]:
    """Get durable event history for a workflow run."""
    from ..services.workflow_storage import get_workflow_run as ws_get
    from ..services.workflow_storage import list_workflow_events

    db = _get_db(request)
    run = ws_get(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    return list_workflow_events(db, run_id)


# ---------------------------------------------------------------------------
# Workflow Schedules (#969)
# ---------------------------------------------------------------------------

_UUID_RE_PATTERN = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


@router.get("/workflow-schedules")
async def list_workflow_schedules(request: Request) -> list[dict[str, Any]]:
    """List workflow schedules."""
    from ..services.workflow_storage import list_schedules

    db = _get_db(request)
    return list_schedules(db)


@router.get("/workflow-schedules/{schedule_id}")
async def get_workflow_schedule(request: Request, schedule_id: str) -> dict[str, Any]:
    """Get a specific workflow schedule."""
    import re

    from ..services.workflow_storage import get_schedule

    if not re.match(_UUID_RE_PATTERN, schedule_id, re.IGNORECASE):
        raise HTTPException(status_code=422, detail="Invalid schedule ID format")

    db = _get_db(request)
    sched = get_schedule(db, schedule_id)
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return sched
