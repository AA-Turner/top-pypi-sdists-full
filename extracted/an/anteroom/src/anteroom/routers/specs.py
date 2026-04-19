"""Spec lifecycle API endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
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
    creation_flow: str | None = None


class GenerateSpecBody(BaseModel):
    namespace: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=64)
    prompt: str | None = None
    issue_number: int | None = Field(default=None, ge=1)


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
        kwargs: dict[str, Any] = {}
        if body.creation_flow is not None:
            kwargs["creation_flow"] = body.creation_flow
        art = _create_spec(db, body.namespace, body.name, body.content, **kwargs)
    except SpecValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        if "UNIQUE constraint" in str(exc):
            raise HTTPException(status_code=409, detail="Spec with this FQN already exists")
        raise
    return art


@router.post("/specs/generate")
async def generate_spec(request: Request, body: GenerateSpecBody) -> dict[str, Any]:
    """Generate spec YAML from a prompt or GitHub issue via LLM."""
    if not body.prompt and body.issue_number is None:
        raise HTTPException(status_code=422, detail="Either 'prompt' or 'issue_number' is required")

    from ..services.ai_service import create_ai_service
    from ..services.spec_schema import CREATION_FLOW_FROM_ISSUE, CREATION_FLOW_PROMPT

    config = request.app.state.config
    ai_service = create_ai_service(config.ai)

    from ..services.spec_generator import generate_spec_from_issue, generate_spec_from_prompt

    try:
        if body.issue_number is not None:
            content_yaml = await generate_spec_from_issue(
                body.issue_number,
                ai_service=ai_service,
                namespace=body.namespace,
                name=body.name,
            )
            creation_flow = CREATION_FLOW_FROM_ISSUE
        else:
            content_yaml = await generate_spec_from_prompt(
                body.prompt or "",
                ai_service=ai_service,
                namespace=body.namespace,
                name=body.name,
            )
            creation_flow = CREATION_FLOW_PROMPT
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return {"content_yaml": content_yaml, "creation_flow": creation_flow}


@router.get("/specs/queue")
async def get_spec_queue(
    request: Request,
    space_id: str | None = Query(None),
) -> dict[str, Any]:
    """Return the spec review queue, filtered by attachment context."""
    db = request.app.state.db
    from ..services.spec_queue import get_review_queue

    # Auto-populate space context from app state (same pattern as list_specs)
    if space_id is None:
        space_id = getattr(request.app.state, "space_id", None)
    project_path: str | None = None
    if space_id:
        from ..services.space_storage import get_space_local_dirs

        local_dirs = get_space_local_dirs(db, space_id)
        if local_dirs:
            project_path = local_dirs[0]

    queue = get_review_queue(db, space_id=space_id, project_path=project_path)
    return {
        "needs_review": [_queue_item_to_dict(i) for i in queue.needs_review],
        "stale": [_queue_item_to_dict(i) for i in queue.stale],
        "blocked": [_queue_item_to_dict(i) for i in queue.blocked],
        "total": queue.total,
    }


def _queue_item_to_dict(item: Any) -> dict[str, Any]:
    return {
        "fqn": item.fqn,
        "category": item.category,
        "phases": item.phases,
        "stale_reasons": item.stale_reasons,
        "blocked_runs": item.blocked_runs,
        "updated_at": item.updated_at,
    }


@router.get("/specs/dashboard")
async def get_dashboard(
    request: Request,
    status: str | None = None,
    namespace: str | None = None,
    has_runs: bool | None = None,
    space_id: str | None = None,
    phase: str | None = None,
    phase_status: str | None = None,
) -> JSONResponse:
    """Spec portfolio dashboard with aggregated lifecycle state."""
    from ..services.spec_dashboard import get_spec_dashboard

    dashboard = get_spec_dashboard(
        request.app.state.db,
        space_id=space_id,
        status=status,
        namespace=namespace,
        has_runs=has_runs,
        phase=phase,
        phase_status=phase_status,
    )
    return JSONResponse(dashboard.to_dict())


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

    path = resolve_workflow_path(
        body.workflow_id,
        allow_filesystem=False,
        db=request.app.state.db,
    )
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


@router.patch("/specs/{fqn:path}")
async def update_spec(request: Request, fqn: str) -> dict[str, Any]:
    """Update spec content."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")
    db = request.app.state.db
    body = await request.json()
    content_yaml = body.get("content_yaml")
    if not content_yaml:
        raise HTTPException(status_code=422, detail="'content_yaml' is required")
    from ..services.spec_service import update_spec_content

    try:
        result = update_spec_content(db, fqn, content_yaml)
    except SpecValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    if result is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    return {"fqn": fqn, "updated": True, "version": result.get("version")}


@router.post("/specs/{fqn:path}/conformance")
async def check_spec_conformance(request: Request, fqn: str) -> dict[str, Any]:
    """Run deterministic conformance checks against a spec."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")
    db = request.app.state.db
    from ..services.spec_conformance import run_conformance_check

    result = run_conformance_check(db, fqn)
    if result is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    return result.to_dict()


@router.get("/specs/{fqn:path}/links")
async def get_spec_links(request: Request, fqn: str) -> dict[str, Any]:
    """List all git links for a spec."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")
    db = request.app.state.db
    from ..services.spec_linkage import get_spec_links as _get_links

    links = _get_links(db, fqn)
    return {
        "fqn": fqn,
        "links": [
            {
                "id": l.id,
                "type": l.type,
                "ref": l.ref,
                "url": l.url,
                "linked_at": l.linked_at,
                "linked_by": l.linked_by,
                "auto": l.auto,
            }
            for l in links  # noqa: E741
        ],
    }


@router.post("/specs/{fqn:path}/links", status_code=201)
async def create_spec_link(request: Request, fqn: str) -> dict[str, Any]:
    """Create a manual git link for a spec."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")
    db = request.app.state.db
    body = await request.json()
    link_type = body.get("type")
    ref = body.get("ref")
    if not link_type or not ref:
        raise HTTPException(status_code=422, detail="'type' and 'ref' are required")
    if link_type not in ("branch", "pr"):
        raise HTTPException(status_code=422, detail="'type' must be 'branch' or 'pr'")
    from ..services.spec_linkage import link_branch_to_spec, link_pr_to_spec

    if link_type == "branch":
        result = link_branch_to_spec(db, fqn, str(ref))
    else:
        result = link_pr_to_spec(db, fqn, str(ref), pr_url=body.get("url"))
    if result is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    return {"fqn": fqn, "linked": True}


@router.delete("/specs/{fqn:path}/links/{link_id}")
async def delete_spec_link(request: Request, fqn: str, link_id: str) -> dict[str, Any]:
    """Remove a git link from a spec."""
    if not validate_fqn(fqn):
        raise HTTPException(status_code=400, detail="Invalid FQN format")
    db = request.app.state.db
    from ..services.spec_linkage import unlink_from_spec

    result = unlink_from_spec(db, fqn, link_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    return {"fqn": fqn, "unlinked": True}


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
