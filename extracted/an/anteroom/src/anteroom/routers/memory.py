"""Memory management API endpoints.

Scope split:
- List / show / create / edit / delete of memory artifacts (#1416).
- Propose / approve / reject / edit-and-approve review workflow,
  reviewer identity, rejection reason, lineage field (#920).
- Pin / unpin, retention preview, retention purge (#625).

All review-state mutations flow through
:mod:`anteroom.services.memory_promotion` so lineage, reviewer
identity, and rate-limits are enforced consistently with the CLI.
Retention mutations flow through :mod:`anteroom.services.memory_retention`
so audit-log events and pin semantics stay consistent.
"""

from __future__ import annotations

import logging
import re
import sqlite3
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

from ..services import lineage, memory_promotion, memory_retention, memory_service
from ..services.memory_promotion import (
    PromotionAgentDisabledError,
    PromotionRateLimitError,
    PromotionStateError,
)
from ..services.memory_service import (
    MEMORY_CATEGORIES,
    MEMORY_SCOPES,
    MEMORY_STATUSES,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["memory"])

_FQN_PATH_RE = re.compile(r"^@[a-z0-9][a-z0-9._-]{0,62}/memory/[a-z0-9][a-z0-9._-]{0,62}$")
_MAX_CONTENT_LEN = 16_000
_MAX_NAME_LEN = 63
_LIST_HARD_LIMIT = 500
_MAX_REASON_LEN = 2000  # hard cap on reject reason, per-install bound via config


def _validate_fqn(fqn: str) -> str:
    """Return *fqn* if it passes the strict memory-FQN regex; raise 400 otherwise."""
    if not _FQN_PATH_RE.match(fqn):
        raise HTTPException(status_code=400, detail="Invalid memory FQN")
    return fqn


class MemoryCreateRequest(BaseModel):
    """Request body for ``POST /api/memory``."""

    content: str = Field(..., min_length=1, max_length=_MAX_CONTENT_LEN)
    scope: str = Field(..., description="One of user / project / local")
    category: str = Field(..., description="One of preference / project_fact / decision / workflow_hint")
    name: str | None = Field(default=None, max_length=_MAX_NAME_LEN)
    project_slug: str | None = Field(default=None, max_length=_MAX_NAME_LEN)
    status: str = Field(default="active")
    created_by: str = Field(default="user", description="user or agent")


class MemoryEditRequest(BaseModel):
    """Request body for ``PATCH /api/memory/{fqn}``.

    Accepts *either* updated content, updated metadata fields, or both.
    Metadata keys are intersected with ``memory_service._MUTABLE_METADATA_FIELDS``
    server-side; any key outside that allowlist is rejected with 400.
    """

    content: str | None = Field(default=None, min_length=1, max_length=_MAX_CONTENT_LEN)
    metadata: dict[str, Any] | None = Field(default=None)


@router.get("/memory")
async def list_memory(
    request: Request,
    scope: str | None = Query(default=None),
    status: str | None = Query(default=None),
    category: str | None = Query(default=None),
    namespace: str | None = Query(default=None),
) -> list[dict[str, Any]]:
    """List memory artifacts with optional filters.

    Capped at ``_LIST_HARD_LIMIT`` entries server-side — an explicit follow-up
    can add pagination once user memory volumes justify it.
    """
    if scope is not None and scope not in MEMORY_SCOPES:
        raise HTTPException(status_code=400, detail=f"Invalid scope: {scope!r}")
    if status is not None and status not in MEMORY_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status!r}")
    if category is not None and category not in MEMORY_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category!r}")

    db = request.app.state.db
    results = memory_service.list_memories(db, scope=scope, category=category, status=status, namespace=namespace)
    return results[:_LIST_HARD_LIMIT]


@router.get("/memory/candidates")
async def list_memory_candidates(
    request: Request,
    status: str = Query(default="candidate"),
    namespace: str | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=_LIST_HARD_LIMIT),
) -> list[dict[str, Any]]:
    """Return the review queue — candidates by default, pending-review or any
    valid memory status by request. Registered before ``/memory/{fqn:path}`` so
    the literal path wins over the catchall path converter."""
    if status not in MEMORY_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status!r}")
    db = request.app.state.db
    results = memory_promotion.list_candidates(db, namespace=namespace, status=status, limit=limit)
    if limit is None:
        return results[:_LIST_HARD_LIMIT]
    return results


# ---------------------------------------------------------------------------
# Retention endpoints (#625)
# ---------------------------------------------------------------------------
#
# IMPORTANT: register these BEFORE the ``/memory/{fqn:path}`` catchall
# below. FastAPI matches routes in registration order, and the ``:path``
# converter is greedy — ``/memory/retention-preview`` would otherwise be
# parsed as ``fqn="retention-preview"`` and fail the FQN regex with 400.
# The same ordering rule applies to ``/memory/candidates`` above.


class RetentionPurgeRequest(BaseModel):
    """Body for ``POST /api/memory/retention-purge``. Requires an explicit
    ``confirm=true`` flag so a stray POST cannot accidentally delete
    memories."""

    confirm: bool = Field(..., description="Must be true to actually delete")


def _retention_config(request: Request) -> Any:
    """Return the runtime memory retention config, falling back to defaults
    when ``app.state.config`` is absent (tests / recovery)."""
    config = getattr(request.app.state, "config", None)
    if config is None:
        from ..config import MemoryRetentionConfig

        return MemoryRetentionConfig()
    return config.memory.retention


def _audit_writer(request: Request) -> Any:
    """Return ``app.state.audit_writer`` when audit is enabled, else None."""
    writer = getattr(request.app.state, "audit_writer", None)
    if writer is None or not getattr(writer, "enabled", False):
        return None
    return writer


def _purge_result_to_payload(result: Any) -> dict[str, Any]:
    return {
        "dry_run": result.dry_run,
        "purged_count": result.purged_count,
        "skipped_pinned_count": result.skipped_pinned_count,
        "purged_by": result.purged_by,
        "items": [
            {
                "fqn": item.fqn,
                "reason": item.reason,
                "age_days": item.age_days,
                "last_recalled_at": item.last_recalled_at,
                "recall_count": item.recall_count,
                "status": item.status,
                "pinned": item.pinned,
            }
            for item in result.items
        ],
    }


@router.get("/memory/{fqn:path}/lineage")
async def memory_lineage(request: Request, fqn: str) -> dict[str, Any]:
    """Return the lineage view for a memory artifact (#925).

    Registered BEFORE ``/memory/{fqn:path}`` catchall so FastAPI matches
    the longer pattern first.
    """
    fqn = _validate_fqn(fqn)
    db = request.app.state.db
    return lineage.resolve_memory_lineage(db, fqn)


@router.get("/memory/retention-preview")
async def retention_preview(request: Request) -> dict[str, Any]:
    """Dry-run the retention policy and return the would-be-purged list.

    This endpoint never mutates the DB and never writes to the audit
    log — it's purely informational. Use it to review a policy before
    enabling it.
    """
    db = request.app.state.db
    result = memory_retention.purge_memories(
        db,
        _retention_config(request),
        dry_run=True,
    )
    return _purge_result_to_payload(result)


@router.post("/memory/retention-purge")
async def retention_purge(request: Request, body: RetentionPurgeRequest) -> dict[str, Any]:
    """Governed trigger for a retention pass.

    Two gates stack here:

    1. ``confirm: true`` in the body, to prevent an accidental POST from
       deleting memories.
    2. Reviewer identity: ``_reviewer_id_from_request`` — the same
       helper used by the #920 approve/reject endpoints. The reviewer
       id is stamped into each ``memory.purge`` audit entry's
       ``user_id`` + ``details.reviewer_id`` and returned in the
       response under ``purged_by`` so the web UI can show who ran the
       pass. The scheduled worker, by contrast, leaves ``reviewer_id``
       as ``None`` and its audit entries record
       ``details.triggered_by="scheduler"``.
    """
    if not body.confirm:
        raise HTTPException(status_code=400, detail="confirm=true required to purge")
    db = request.app.state.db
    result = memory_retention.purge_memories(
        db,
        _retention_config(request),
        dry_run=False,
        audit_writer=_audit_writer(request),
        reviewer_id=_reviewer_id_from_request(request),
    )
    return _purge_result_to_payload(result)


# ---------------------------------------------------------------------------
# Pin / unpin endpoints (#625)
# ---------------------------------------------------------------------------


@router.post("/memory/{fqn:path}/pin")
async def pin_memory_endpoint(request: Request, fqn: str) -> dict[str, Any]:
    """Pin a memory so retention policies skip it by default."""
    fqn = _validate_fqn(fqn)
    db = request.app.state.db
    updated = memory_service.pin_memory(db, fqn)
    if updated is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    return updated


@router.post("/memory/{fqn:path}/unpin")
async def unpin_memory_endpoint(request: Request, fqn: str) -> dict[str, Any]:
    """Remove the pin flag from a memory."""
    fqn = _validate_fqn(fqn)
    db = request.app.state.db
    updated = memory_service.unpin_memory(db, fqn)
    if updated is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    return updated


@router.get("/memory/{fqn:path}")
async def get_memory(request: Request, fqn: str) -> dict[str, Any]:
    """Fetch a single memory artifact by FQN."""
    fqn = _validate_fqn(fqn)
    db = request.app.state.db
    result = memory_service.get_memory(db, fqn)
    if result is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    return result


@router.post("/memory")
async def create_memory(request: Request, body: MemoryCreateRequest) -> dict[str, Any]:
    """Create a new memory artifact."""
    if body.scope not in MEMORY_SCOPES:
        raise HTTPException(status_code=400, detail=f"Invalid scope: {body.scope!r}")
    if body.category not in MEMORY_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category: {body.category!r}")
    if body.status not in MEMORY_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status: {body.status!r}")
    if body.created_by not in ("user", "agent"):
        raise HTTPException(status_code=400, detail=f"Invalid created_by: {body.created_by!r}")

    db = request.app.state.db
    try:
        art = memory_service.create_memory(
            db,
            content=body.content,
            scope=body.scope,
            category=body.category,
            name=body.name,
            project_slug=body.project_slug,
            status=body.status,
            created_by=body.created_by,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except sqlite3.IntegrityError:
        # Duplicate FQN — the service layer relies on the unique constraint
        # on artifacts.fqn. Surface as 409 Conflict rather than leaking a
        # 500 with stack trace.
        raise HTTPException(status_code=409, detail="A memory with that FQN already exists")
    return art


@router.patch("/memory/{fqn:path}")
async def edit_memory(request: Request, fqn: str, body: MemoryEditRequest) -> dict[str, Any]:
    """Update content and/or mutable metadata fields of an existing memory."""
    fqn = _validate_fqn(fqn)
    if body.content is None and not body.metadata:
        raise HTTPException(status_code=400, detail="At least one of content or metadata must be provided")

    db = request.app.state.db

    if body.content is not None:
        updated = memory_service.update_memory_content(db, fqn, body.content)
        if updated is None:
            raise HTTPException(status_code=404, detail="Memory not found")

    if body.metadata:
        allowed = memory_service._MUTABLE_METADATA_FIELDS
        unknown = set(body.metadata) - allowed
        if unknown:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown metadata field(s): {sorted(unknown)}",
            )
        try:
            updated = memory_service.update_memory_metadata(db, fqn, **body.metadata)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        if updated is None:
            raise HTTPException(status_code=404, detail="Memory not found")

    # Re-fetch so the response reflects the latest row state regardless of which
    # branch(es) above wrote. get_memory itself refuses non-memory artifacts.
    latest = memory_service.get_memory(db, fqn)
    if latest is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    return latest


@router.delete("/memory/{fqn:path}")
async def delete_memory(request: Request, fqn: str) -> dict[str, str]:
    """Delete a memory artifact by FQN."""
    fqn = _validate_fqn(fqn)
    db = request.app.state.db
    removed = memory_service.delete_memory(db, fqn)
    if not removed:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"status": "deleted"}


# ---------------------------------------------------------------------------
# Promotion & review endpoints (#920)
# ---------------------------------------------------------------------------


class ProvenanceRequest(BaseModel):
    """Provenance fields accepted on propose requests."""

    conversation_id: str | None = Field(default=None, max_length=36)
    message_id: str | None = Field(default=None, max_length=36)
    workflow_run_id: str | None = Field(default=None, max_length=36)
    source_artifact_id: str | None = Field(default=None, max_length=36)


class ProposeCandidateRequest(BaseModel):
    """Body for ``POST /api/memory/candidates``."""

    content: str = Field(..., min_length=1, max_length=_MAX_CONTENT_LEN)
    scope: str = Field(..., description="user / project / local")
    category: str = Field(..., description="preference / project_fact / decision / workflow_hint")
    proposer: str = Field(default="user", description="user or agent")
    proposer_id: str | None = Field(default=None, max_length=_MAX_NAME_LEN)
    name: str | None = Field(default=None, max_length=_MAX_NAME_LEN)
    project_slug: str | None = Field(default=None, max_length=_MAX_NAME_LEN)
    provenance: ProvenanceRequest | None = Field(default=None)


class EditsRequest(BaseModel):
    """Optional in-line edits applied during approve."""

    content: str | None = Field(default=None, min_length=1, max_length=_MAX_CONTENT_LEN)
    category: str | None = Field(default=None)


class ApproveRequest(BaseModel):
    """Body for ``POST /api/memory/{fqn}/approve`` and
    ``POST /api/memory/{fqn}/edit-and-approve``."""

    reviewer_display: str | None = Field(default=None, max_length=_MAX_NAME_LEN)
    edits: EditsRequest | None = Field(default=None)


class RejectRequest(BaseModel):
    """Body for ``POST /api/memory/{fqn}/reject``."""

    reason: str = Field(..., min_length=1, max_length=_MAX_REASON_LEN)
    reviewer_display: str | None = Field(default=None, max_length=_MAX_NAME_LEN)


def _promotion_config(request: Request) -> Any:
    """Fetch the runtime promotion config, falling back to defaults.

    Tests and recovery flows may run without a fully-constructed AppConfig
    on ``app.state``; we fall back to a fresh default in that case so the
    route still works end-to-end.
    """
    config = getattr(request.app.state, "config", None)
    if config is None:
        from ..config import MemoryPromotionConfig

        return MemoryPromotionConfig()
    return config.memory.promotion


def _reviewer_id_from_request(request: Request) -> str:
    """Extract the reviewer's identity from the authenticated session.

    Falls back to the identity configured on ``app.state.config`` when
    available, then to a synthetic id so we never write an empty string.
    """
    # The web auth middleware stamps a stable user id on the request; if
    # unavailable, fall back to the identity uid from config, then a
    # default so a reviewer identity is always recorded.
    state_user = getattr(request.state, "user_id", None)
    if isinstance(state_user, str) and state_user:
        return state_user[:_MAX_NAME_LEN]
    config = getattr(request.app.state, "config", None)
    if config is not None and getattr(config, "identity", None) is not None:
        uid = getattr(config.identity, "user_id", None)
        if isinstance(uid, str) and uid:
            return uid[:_MAX_NAME_LEN]
    return "web-reviewer"


@router.post("/memory/candidates")
async def propose_memory_candidate(request: Request, body: ProposeCandidateRequest) -> dict[str, Any]:
    """Propose a new memory candidate."""
    if body.scope not in MEMORY_SCOPES:
        raise HTTPException(status_code=400, detail=f"Invalid scope: {body.scope!r}")
    if body.category not in MEMORY_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category: {body.category!r}")
    if body.proposer not in ("user", "agent"):
        raise HTTPException(status_code=400, detail=f"Invalid proposer: {body.proposer!r}")

    db = request.app.state.db
    cfg = _promotion_config(request)
    prov = body.provenance.model_dump() if body.provenance else None

    try:
        mem = memory_promotion.propose_candidate(
            db,
            content=body.content,
            scope=body.scope,
            category=body.category,
            proposer=body.proposer,
            proposer_id=body.proposer_id,
            provenance=prov,
            project_slug=body.project_slug,
            config=cfg,
            name=body.name,
        )
    except PromotionAgentDisabledError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
    except PromotionRateLimitError as exc:
        raise HTTPException(
            status_code=429,
            detail={
                "error": str(exc),
                "conversation_id": exc.conversation_id,
                "cap": exc.cap,
                "current": exc.current,
                "retry_hint": "Review existing candidates before proposing more in this conversation.",
            },
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="A memory with that FQN already exists")
    lineage.emit_memory_promotion(
        _audit_writer(request),
        "proposed",
        fqn=mem["fqn"],
        reviewer_id=body.proposer_id or _reviewer_id_from_request(request),
        details={"proposer": body.proposer},
    )
    return mem


@router.post("/memory/{fqn:path}/approve")
async def approve_memory(request: Request, fqn: str, body: ApproveRequest) -> dict[str, Any]:
    """Approve a candidate / pending-review memory."""
    fqn = _validate_fqn(fqn)
    db = request.app.state.db
    cfg = _promotion_config(request)
    reviewer_id = _reviewer_id_from_request(request)
    edits = body.edits.model_dump(exclude_none=True) if body.edits else None
    try:
        mem = memory_promotion.approve_candidate(
            db,
            fqn,
            reviewer_id=reviewer_id,
            reviewer_display=body.reviewer_display,
            edits=edits,
            config=cfg,
        )
    except PromotionStateError as exc:
        # "Memory not found" versus "Cannot approve ..." both surface here.
        msg = str(exc)
        if "not found" in msg.lower():
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=409, detail=msg)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    lineage.emit_memory_promotion(
        _audit_writer(request),
        "approved",
        fqn=fqn,
        reviewer_id=reviewer_id,
        details={"edits_applied": bool(edits)},
    )
    return mem


@router.post("/memory/{fqn:path}/edit-and-approve")
async def edit_and_approve_memory(request: Request, fqn: str, body: ApproveRequest) -> dict[str, Any]:
    """Alias for approve that requires inline *edits*. 400 when edits missing."""
    if body.edits is None:
        raise HTTPException(status_code=400, detail="edits are required for edit-and-approve")
    return await approve_memory(request, fqn, body)


@router.post("/memory/{fqn:path}/reject")
async def reject_memory(request: Request, fqn: str, body: RejectRequest) -> dict[str, Any]:
    """Reject a candidate / pending-review memory with a bounded reason string."""
    fqn = _validate_fqn(fqn)
    db = request.app.state.db
    cfg = _promotion_config(request)
    reviewer_id = _reviewer_id_from_request(request)
    try:
        mem = memory_promotion.reject_candidate(
            db,
            fqn,
            reviewer_id=reviewer_id,
            reviewer_display=body.reviewer_display,
            reason=body.reason,
            config=cfg,
        )
    except PromotionStateError as exc:
        msg = str(exc)
        if "not found" in msg.lower():
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=409, detail=msg)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    lineage.emit_memory_promotion(
        _audit_writer(request),
        "rejected",
        fqn=fqn,
        reviewer_id=reviewer_id,
        details={"reason_length": len(body.reason)},
    )
    return mem
