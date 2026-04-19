"""Audit lineage emitters for workflow runs and memory promotion (#925).

Centralises the construction and emission of structured audit events for
governed durable actions. Every emitter is safe to call with
``audit_writer=None`` (no-op) and never raises — failures are caught and
logged at WARNING level so audit emission never breaks the underlying
business operation.

Event taxonomy
--------------

Workflow:
    ``workflow.approved``       — a pending tool approval was approved
    ``workflow.denied``         — a pending tool approval was denied
    ``workflow.decision_resolved`` — a human-gate decision was answered
    ``workflow.cancel_requested``  — operator requested run cancellation
    ``workflow.run.started``    — executor claimed and started the run
    ``workflow.run.completed``  — run reached terminal success state
    ``workflow.run.failed``     — run reached terminal failure state
    ``workflow.run.cancelled``  — run terminated via cancel request

Memory:
    ``memory.proposed``         — candidate memory created
    ``memory.approved``         — candidate transitioned to active
    ``memory.rejected``         — candidate transitioned to rejected

Category prefixes follow the ``AuditWriter.is_event_enabled`` convention
(``event_type.split('.')[0]`` is the category gated by ``audit.events``).
The ``workflow`` and ``memory`` categories must be registered in
:class:`anteroom.config.AuditConfig.events` for emissions to land.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .audit import AuditEntry

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection
    from .audit import AuditWriter

logger = logging.getLogger(__name__)


# Allowed lifecycle events — matches ``workflow_executor`` terminal states.
_WORKFLOW_LIFECYCLE_EVENTS = frozenset({"started", "completed", "failed", "cancelled"})

# Allowed memory promotion events.
_MEMORY_PROMOTION_EVENTS = frozenset({"proposed", "approved", "rejected"})


def _safe_emit(writer: AuditWriter | None, entry: AuditEntry) -> None:
    """Emit *entry* via *writer*, swallowing failures.

    The audit pipeline is best-effort by contract: a failure to write an
    audit record never aborts the underlying business operation. We log
    at WARNING so operators can detect persistent emission failures via
    SIEM or log aggregation.
    """
    if writer is None:
        return
    try:
        writer.emit(entry)
    except Exception:  # pragma: no cover — defensive
        logger.warning("Failed to emit audit entry %s", entry.event_type, exc_info=True)


# ---------------------------------------------------------------------------
# Workflow emitters
# ---------------------------------------------------------------------------


def emit_workflow_approval(
    audit_writer: AuditWriter | None,
    *,
    run_id: str,
    request_id: str,
    outcome: str,
    resolved_by: str,
    tool_name: str = "",
) -> None:
    """Emit ``workflow.approved`` or ``workflow.denied`` for a tool approval.

    *outcome* must be one of ``"approved"`` or ``"denied"``. Any other
    value is logged and dropped (defence-in-depth — the router/CLI should
    only ever pass the two legal outcomes, but a future caller bug here
    must not corrupt the audit chain).
    """
    if outcome not in ("approved", "denied"):
        logger.warning("emit_workflow_approval: unknown outcome %r — dropping", outcome)
        return
    event_type = f"workflow.{outcome}"
    entry = AuditEntry.create(
        event_type=event_type,
        severity="info",
        user_id=resolved_by,
        details={
            "run_id": run_id,
            "request_id": request_id,
            "outcome": outcome,
            "tool_name": tool_name,
        },
    )
    _safe_emit(audit_writer, entry)


def emit_workflow_decision(
    audit_writer: AuditWriter | None,
    *,
    run_id: str,
    decision_id: str,
    option_id: str,
    resolved_by: str,
) -> None:
    """Emit ``workflow.decision_resolved`` for a human-gate response."""
    entry = AuditEntry.create(
        event_type="workflow.decision_resolved",
        severity="info",
        user_id=resolved_by,
        details={
            "run_id": run_id,
            "decision_id": decision_id,
            "option_id": option_id,
        },
    )
    _safe_emit(audit_writer, entry)


def emit_workflow_cancel(
    audit_writer: AuditWriter | None,
    *,
    run_id: str,
    cancelled_by: str,
    reason: str = "",
    from_status: str = "",
) -> None:
    """Emit ``workflow.cancel_requested`` for an operator-initiated cancel."""
    entry = AuditEntry.create(
        event_type="workflow.cancel_requested",
        severity="info",
        user_id=cancelled_by,
        details={
            "run_id": run_id,
            "reason": reason,
            "from_status": from_status,
        },
    )
    _safe_emit(audit_writer, entry)


def emit_workflow_run_lifecycle(
    audit_writer: AuditWriter | None,
    event: str,
    *,
    run_id: str,
    user_id: str = "",
    details: dict[str, Any] | None = None,
) -> None:
    """Emit ``workflow.run.{event}`` lifecycle event.

    *event* must be one of ``"started"``, ``"completed"``, ``"failed"``,
    or ``"cancelled"``.

    Severity is ``"info"`` for ``started``/``completed`` and ``"warning"``
    for ``failed``/``cancelled`` so SIEM dashboards can default-filter
    happy-path noise.
    """
    if event not in _WORKFLOW_LIFECYCLE_EVENTS:
        logger.warning("emit_workflow_run_lifecycle: unknown event %r — dropping", event)
        return
    severity = "warning" if event in ("failed", "cancelled") else "info"
    payload = {"run_id": run_id}
    if details:
        payload.update(details)
    entry = AuditEntry.create(
        event_type=f"workflow.run.{event}",
        severity=severity,
        user_id=user_id,
        details=payload,
    )
    _safe_emit(audit_writer, entry)


# ---------------------------------------------------------------------------
# Memory emitters
# ---------------------------------------------------------------------------


def emit_memory_promotion(
    audit_writer: AuditWriter | None,
    event: str,
    *,
    fqn: str,
    reviewer_id: str = "",
    details: dict[str, Any] | None = None,
) -> None:
    """Emit ``memory.{event}`` for proposal/approval/rejection.

    *event* must be one of ``"proposed"``, ``"approved"``, or
    ``"rejected"``.
    """
    if event not in _MEMORY_PROMOTION_EVENTS:
        logger.warning("emit_memory_promotion: unknown event %r — dropping", event)
        return
    severity = "warning" if event == "rejected" else "info"
    payload: dict[str, Any] = {"fqn": fqn}
    if details:
        payload.update(details)
    entry = AuditEntry.create(
        event_type=f"memory.{event}",
        severity=severity,
        user_id=reviewer_id,
        details=payload,
    )
    _safe_emit(audit_writer, entry)


# ---------------------------------------------------------------------------
# Read-side: lineage resolution
# ---------------------------------------------------------------------------


def resolve_memory_lineage(db: ThreadSafeConnection, fqn: str) -> dict[str, Any]:
    """Resolve the lineage view for a memory artifact.

    Returns a dict with the shape::

        {
            "fqn": str,
            "provenance": dict | None,    # source conversation / message
            "lineage": list[dict],         # promotion events from metadata
            "related_memories": list[dict], # memories from same conversation
        }

    When the memory is not found, returns ``{"fqn": fqn, "provenance":
    None, "lineage": [], "related_memories": []}`` — callers can render
    an empty result rather than 404.

    ``related_memories`` is capped at 50 entries to prevent runaway
    payloads when a long-running conversation produces many memories.
    """
    from .memory_service import get_memory, list_memories

    mem = get_memory(db, fqn)
    if mem is None:
        return {
            "fqn": fqn,
            "provenance": None,
            "lineage": [],
            "related_memories": [],
        }

    metadata = mem.get("metadata") or {}
    provenance = metadata.get("provenance") if isinstance(metadata.get("provenance"), dict) else None
    lineage = list(metadata.get("lineage") or [])

    related: list[dict[str, Any]] = []
    conversation_id = (provenance or {}).get("conversation_id") if provenance else None
    if conversation_id:
        candidates = list_memories(db)
        for other in candidates:
            if other.get("fqn") == fqn:
                continue
            other_meta = other.get("metadata") or {}
            other_prov = other_meta.get("provenance")
            if not isinstance(other_prov, dict):
                continue
            if other_prov.get("conversation_id") != conversation_id:
                continue
            related.append(
                {
                    "fqn": other.get("fqn"),
                    "memory_status": other_meta.get("memory_status"),
                    "memory_category": other_meta.get("memory_category"),
                    "created_at": other.get("created_at"),
                }
            )
            if len(related) >= 50:
                break

    return {
        "fqn": fqn,
        "provenance": provenance,
        "lineage": lineage,
        "related_memories": related,
    }
