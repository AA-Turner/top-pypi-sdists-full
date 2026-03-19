"""Spec lifecycle API endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

from ..services import artifact_storage
from ..services.artifacts import ArtifactType, validate_fqn
from ..services.spec_schema import VALID_PHASE_NAMES, SpecMode, SpecValidationError, parse_spec_content

router = APIRouter(tags=["specs"])


def _is_pack_owned(db: Any, artifact_id: str) -> bool:
    """Check if an artifact is owned by a pack."""
    return artifact_storage.is_pack_owned(db, artifact_id)


class CreateSpecBody(BaseModel):
    namespace: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1)


class LaunchFromTaskBody(BaseModel):
    workflow_id: str = Field(min_length=1, max_length=128)
    extra_inputs: dict[str, Any] | None = None


@router.get("/specs")
async def list_specs(
    request: Request,
    attached_only: bool = Query(False),
    space_id: str | None = Query(None),
) -> list[dict[str, Any]]:
    """List all spec artifacts with phase status summaries.

    When *attached_only* is True, only returns specs from standalone
    artifacts or packs with active attachments.
    """
    db = request.app.state.db

    project_path: str | None = None
    if attached_only and space_id:
        from ..services.space_storage import get_space_local_dirs

        local_dirs = get_space_local_dirs(db, space_id)
        if local_dirs:
            project_path = local_dirs[0]

    results = artifact_storage.list_artifacts(
        db,
        artifact_type=ArtifactType.SPEC,
        attached_only=attached_only,
        space_id=space_id,
        project_path=project_path,
    )
    for r in results:
        r["mode"] = _get_mode_from_content(r.get("content", ""))
        r.pop("content", None)
        r["editable"] = not _is_pack_owned(db, r["id"])
        r["source_label"] = "pack" if not r["editable"] else r.get("source", "")
    return results


@router.post("/specs", status_code=201)
async def create_spec(request: Request, body: CreateSpecBody) -> dict[str, Any]:
    """Create a new spec artifact from YAML content."""
    db = request.app.state.db
    from ..services.spec_service import create_spec as _create_spec

    try:
        art = _create_spec(db, body.namespace, body.name, body.content)
    except SpecValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        if "UNIQUE constraint" in str(exc):
            raise HTTPException(status_code=409, detail="Spec with this FQN already exists")
        raise
    return art


@router.get("/specs/{fqn:path}/traceability")
async def get_spec_traceability(request: Request, fqn: str) -> dict[str, Any]:
    """Get task-to-run traceability for a spec."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")

    db = request.app.state.db
    from ..services.spec_service import get_traceability

    trace = get_traceability(db, fqn)
    if trace is None:
        raise HTTPException(status_code=404, detail="Spec not found")

    return {"fqn": fqn, "tasks": trace}


@router.post("/specs/{fqn:path}/tasks/{task_id}/launch", status_code=201)
async def launch_from_task(request: Request, fqn: str, task_id: str, body: LaunchFromTaskBody) -> dict[str, Any]:
    """Launch a workflow run from a spec task."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")

    db = request.app.state.db
    config = request.app.state.config
    from ..services.spec_service import launch_from_task as _launch

    _extra = dict(body.extra_inputs or {})
    _space_id = getattr(request.app.state, "space_id", None)
    if _space_id:
        _extra.setdefault("space_id", _space_id)
    _space_dirs = getattr(request.app.state, "space_local_dirs", None)
    if _space_dirs:
        _extra.setdefault("project_path", _space_dirs[0] if _space_dirs else None)

    try:
        inputs = _launch(db, fqn, task_id, body.workflow_id, extra_inputs=_extra or None)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    from ..services.workflow_resolution import resolve_workflow_path

    path = resolve_workflow_path(body.workflow_id, allow_filesystem=False)
    if not path:
        raise HTTPException(status_code=404, detail="Workflow not found")

    from ..services.workflow_engine import WorkflowEngine, load_definition
    from ..services.workflow_runners import create_default_registry

    try:
        definition = load_definition(path)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid workflow definition")

    from ..services.workflow_credentials import CredentialResolver

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
            target_kind="spec",
            target_ref=fqn,
            inputs=inputs,
            trigger_source="spec_launch",
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return {"run_id": run["id"], "spec_fqn": fqn, "task_id": task_id}


@router.get("/specs/{fqn:path}/stale")
async def get_spec_stale(request: Request, fqn: str) -> dict[str, Any]:
    """Get current stale state with derived reasons for each phase."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")

    db = request.app.state.db
    art = artifact_storage.get_artifact_by_fqn(db, fqn)
    if not art or art["type"] != "spec":
        raise HTTPException(status_code=404, detail="Spec not found")

    from ..services.spec_diff import derive_stale_reason
    from ..services.spec_schema import get_phase_status

    phases: dict[str, Any] = {}
    for phase in VALID_PHASE_NAMES:
        status = get_phase_status(art["metadata"], phase)
        reason = derive_stale_reason(db, art["id"], phase, art["metadata"]) if status.value == "stale" else None
        phases[phase] = {"status": status.value, "reason": reason}

    return {"fqn": fqn, "phases": phases}


@router.get("/specs/{fqn:path}/diff")
async def get_spec_diff(
    request: Request,
    fqn: str,
    v1: int | None = Query(None, ge=1),
    v2: int | None = Query(None, ge=1),
) -> dict[str, Any]:
    """Diff between two spec versions."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")

    db = request.app.state.db
    art = artifact_storage.get_artifact_by_fqn(db, fqn)
    if not art or art["type"] != "spec":
        raise HTTPException(status_code=404, detail="Spec not found")

    versions = artifact_storage.list_artifact_versions(db, art["id"])
    if len(versions) < 2:
        raise HTTPException(status_code=422, detail="Need at least 2 versions to diff")

    from ..services.spec_diff import diff_spec_versions
    from ..services.spec_schema import parse_spec_content

    # Default: diff previous vs current
    ver_to = v2 or versions[0]["version"]
    ver_from = v1 or (versions[1]["version"] if len(versions) >= 2 else 1)

    old_content = None
    new_content = None
    for v in versions:
        if v["version"] == ver_from:
            old_content = v["content"]
        if v["version"] == ver_to:
            new_content = v["content"]

    if old_content is None or new_content is None:
        raise HTTPException(status_code=404, detail="Version not found")

    old_spec = parse_spec_content(old_content)
    new_spec = parse_spec_content(new_content)
    diff = diff_spec_versions(old_spec, new_spec, version_from=ver_from, version_to=ver_to)

    return {
        "fqn": fqn,
        "version_from": diff.version_from,
        "version_to": diff.version_to,
        "phase_changes": [
            {"phase": pc.phase, "content_changed": pc.content_changed, "content_diff": pc.content_diff}
            for pc in diff.phase_changes
        ],
        "task_changes": [
            {
                "task_id": tc.task_id,
                "change_type": tc.change_type,
                "summary_before": tc.summary_before,
                "summary_after": tc.summary_after,
            }
            for tc in diff.task_changes
        ],
    }


@router.get("/specs/{fqn:path}")
async def get_spec(request: Request, fqn: str) -> dict[str, Any]:
    """Get a spec with parsed phase statuses and stale reasons."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")

    db = request.app.state.db
    from ..services.spec_service import get_spec as _get_spec

    result = _get_spec(db, fqn)
    if result is None:
        raise HTTPException(status_code=404, detail="Spec not found")

    art, spec_content = result
    art["mode"] = spec_content.mode.value
    versions = artifact_storage.list_artifact_versions(db, art["id"])
    art["version"] = versions[0]["version"] if versions else 1
    art["versions"] = versions

    from ..services.spec_diff import derive_stale_reason
    from ..services.spec_schema import get_phase_status

    phase_info: dict[str, Any] = {}
    for phase in VALID_PHASE_NAMES:
        status = get_phase_status(art["metadata"], phase)
        reason = derive_stale_reason(db, art["id"], phase, art["metadata"]) if status.value == "stale" else None
        phase_info[phase] = {"status": status.value, "reason": reason}
    art["phase_info"] = phase_info
    art["editable"] = not _is_pack_owned(db, art["id"])
    art["source_label"] = "pack" if not art["editable"] else art.get("source", "")

    return art


@router.post("/specs/{fqn:path}/phases/{phase}/approve")
async def approve_spec_phase(request: Request, fqn: str, phase: str) -> dict[str, Any]:
    """Approve a spec phase."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")
    if phase not in VALID_PHASE_NAMES:
        raise HTTPException(status_code=400, detail=f"Invalid phase: must be one of {sorted(VALID_PHASE_NAMES)}")

    db = request.app.state.db
    from ..services.spec_service import approve_phase

    try:
        art = approve_phase(db, fqn, phase)
    except (ValueError, SpecValidationError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if art is None:
        raise HTTPException(status_code=404, detail="Spec not found")

    return {"status": "approved", "fqn": fqn, "phase": phase}


@router.post("/specs/{fqn:path}/phases/{phase}/unapprove")
async def unapprove_spec_phase(request: Request, fqn: str, phase: str) -> dict[str, Any]:
    """Reset a spec phase to draft."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")
    if phase not in VALID_PHASE_NAMES:
        raise HTTPException(status_code=400, detail=f"Invalid phase: must be one of {sorted(VALID_PHASE_NAMES)}")

    db = request.app.state.db
    from ..services.spec_service import unapprove_phase

    try:
        art = unapprove_phase(db, fqn, phase)
    except (ValueError, SpecValidationError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if art is None:
        raise HTTPException(status_code=404, detail="Spec not found")

    return {"status": "draft", "fqn": fqn, "phase": phase}


def _get_mode_from_content(content: str) -> str:
    """Extract spec mode from YAML content, defaulting to 'feature'."""
    if not content:
        return SpecMode.FEATURE.value
    try:
        spec = parse_spec_content(content)
        return spec.mode.value
    except Exception:
        return SpecMode.FEATURE.value
