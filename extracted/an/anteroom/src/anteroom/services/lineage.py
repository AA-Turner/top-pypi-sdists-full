"""Audit lineage emitters for workflow runs, memory promotion, and hooks (#925, #1490).

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

Subagent:
    ``subagent.spawned``        — detached subagent run was enqueued
    ``subagent.started``        — detached subagent began execution
    ``subagent.completed``      — detached subagent finished successfully
    ``subagent.failed``         — detached subagent ended in failure
    ``subagent.cancelled``      — detached subagent was cancelled

Memory:
    ``memory.proposed``         — candidate memory created
    ``memory.approved``         — candidate transitioned to active
    ``memory.rejected``         — candidate transitioned to rejected

Hook (#1490, #1492):
    ``hook.completed``          — hook ran and returned allow or ask
    ``hook.denied``             — hook returned deny (tool call blocked or continuation stopped)
    ``hook.timed_out``          — hook runner timed out (fail-open, outcome=allow)
    ``hook.failed``             — hook runner raised an exception (fail-open, outcome=allow)
    ``hook.approval_resolved``  — user resolved a hook-escalated approval (approved/denied)

Category prefixes follow the ``AuditWriter.is_event_enabled`` convention
(``event_type.split('.')[0]`` is the category gated by ``audit.events``).
The ``workflow``, ``subagent``, ``memory``, and ``hook`` categories must be
registered in :class:`anteroom.config.AuditConfig.events` for emissions
to land.
"""

from __future__ import annotations

import hashlib
import json
import logging
from typing import TYPE_CHECKING, Any

from .audit import AuditEntry

if TYPE_CHECKING:
    from ..config import HooksConfig
    from ..db import ThreadSafeConnection
    from .audit import AuditWriter

logger = logging.getLogger(__name__)


# Allowed lifecycle events — matches ``workflow_executor`` terminal states.
_WORKFLOW_LIFECYCLE_EVENTS = frozenset({"started", "completed", "failed", "cancelled"})

# Allowed subagent lifecycle events — mirrors workflow terminal states plus
# ``spawned`` for the pre-start governance checkpoint.
_SUBAGENT_LIFECYCLE_EVENTS = frozenset({"spawned", "started", "completed", "failed", "cancelled"})

# Allowed memory promotion events.
_MEMORY_PROMOTION_EVENTS = frozenset({"proposed", "approved", "rejected"})

# Allowed hook lifecycle events (#1490, #1492).
_HOOK_LIFECYCLE_EVENTS = frozenset({"completed", "denied", "timed_out", "failed", "approval_resolved"})


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
# Subagent emitters
# ---------------------------------------------------------------------------


def emit_subagent_lifecycle(
    audit_writer: AuditWriter | None,
    event: str,
    *,
    run_id: str,
    conversation_id: str = "",
    user_id: str = "",
    model: str = "",
    parent_run_id: str = "",
    details: dict[str, Any] | None = None,
) -> None:
    """Emit ``subagent.{event}`` lifecycle event.

    *event* must be one of ``"spawned"``, ``"started"``, ``"completed"``,
    ``"failed"``, or ``"cancelled"``.

    Severity is ``"info"`` for ``spawned``/``started``/``completed`` and
    ``"warning"`` for ``failed``/``cancelled`` to match the ``workflow.run.*``
    emitter's convention so SIEM dashboards can default-filter happy-path
    noise consistently across durable governed actions.
    """
    if event not in _SUBAGENT_LIFECYCLE_EVENTS:
        logger.warning("emit_subagent_lifecycle: unknown event %r — dropping", event)
        return
    severity = "warning" if event in ("failed", "cancelled") else "info"
    payload: dict[str, Any] = {"run_id": run_id}
    if conversation_id:
        payload["conversation_id"] = conversation_id
    if model:
        payload["model"] = model
    if parent_run_id:
        payload["parent_run_id"] = parent_run_id
    if details:
        payload.update(details)
    entry = AuditEntry.create(
        event_type=f"subagent.{event}",
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
# Hook emitters (#1490)
# ---------------------------------------------------------------------------


def _hook_snapshot_hash(entry_payload: dict[str, Any]) -> str:
    """Return a stable SHA-256 hash for one hook-config entry payload."""
    canonical = json.dumps(entry_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def emit_hook_snapshot(audit_writer: AuditWriter | None, hooks_config: "HooksConfig") -> None:
    """Emit ``hook.snapshot`` for the resolved hook config in effect at startup."""
    entries_payload: list[dict[str, Any]] = []
    for entry in [*hooks_config.pre_tool, *hooks_config.post_tool]:
        hash_payload = {
            "id": entry.id,
            "event": entry.event,
            "matcher": {
                "tool_name": entry.matcher.tool_name,
                "arguments": dict(entry.matcher.arguments),
            },
            "runner": {
                "type": entry.runner.type,
                "command": entry.runner.command,
                "url": entry.runner.url,
                "timeout": entry.runner.timeout,
            },
            "message": entry.message,
            "trust_source": entry.trust_source,
        }
        entries_payload.append(
            {
                "id": entry.id,
                "event": entry.event,
                "trust_source": entry.trust_source,
                "is_executable": entry.is_executable,
                "runner_type": entry.runner.type,
                "entry_sha256": _hook_snapshot_hash(hash_payload),
            }
        )

    audit_entry = AuditEntry.create(
        event_type="hook.snapshot",
        severity="info",
        details={"hook_count": len(entries_payload), "entries": entries_payload},
    )
    _safe_emit(audit_writer, audit_entry)


def emit_hook_lifecycle(
    audit_writer: AuditWriter | None,
    event: str,
    *,
    hook_id: str,
    hook_event: str,
    tool_name: str,
    outcome: str,
    execution_ms: float = 0.0,
    message: str = "",
    tool_call_id: str = "",
    conversation_id: str = "",
    user_id: str = "",
    details: dict[str, Any] | None = None,
) -> None:
    """Emit ``hook.{event}`` for a single resolved hook execution.

    *event* must be one of ``"completed"``, ``"denied"``, ``"timed_out"``,
    or ``"failed"``.

    Payload fields:

    - ``hook_id``      — stable identifier from :class:`HookEntryConfig`
    - ``hook_event``   — ``"pre_tool"`` or ``"post_tool"``
    - ``tool_name``    — the tool being intercepted
    - ``tool_call_id`` — stable identifier for the intercepted tool call
    - ``outcome``      — the routing decision (``allow``, ``deny``, ``ask``)
    - ``execution_ms`` — wall-clock time of the runner in milliseconds
    - ``message``      — optional message from the hook response

    Severity is ``"warning"`` for ``denied``, ``timed_out``, and ``failed``
    (operator attention warranted); ``"info"`` for ``completed``.
    """
    if event not in _HOOK_LIFECYCLE_EVENTS:
        logger.warning("emit_hook_lifecycle: unknown event %r — dropping", event)
        return
    severity = "warning" if event != "completed" else "info"
    payload: dict[str, Any] = {
        "hook_id": hook_id,
        "hook_event": hook_event,
        "tool_name": tool_name,
        "outcome": outcome,
        "execution_ms": round(execution_ms, 2),
    }
    if message:
        payload["message"] = message
    if tool_call_id:
        payload["tool_call_id"] = tool_call_id
    if conversation_id:
        payload["conversation_id"] = conversation_id
    if details:
        payload.update(details)
    entry = AuditEntry.create(
        event_type=f"hook.{event}",
        severity=severity,
        user_id=user_id,
        details=payload,
    )
    _safe_emit(audit_writer, entry)


def emit_hook_approval_resolved(
    audit_writer: AuditWriter | None,
    *,
    hook_id: str,
    tool_name: str,
    resolution: str,
    tool_call_id: str = "",
    conversation_id: str = "",
    user_id: str = "",
) -> None:
    """Emit ``hook.approval_resolved`` when a user resolves a hook-escalated approval.

    Called after the approval callback returns for a hook ``ask`` outcome so
    the audit trail can distinguish hook-driven escalations from tier-based
    approval prompts.

    *resolution* must be ``"approved"`` or ``"denied"``.
    Severity is ``"info"`` for approved and ``"warning"`` for denied.
    """
    if resolution not in ("approved", "denied"):
        logger.warning("emit_hook_approval_resolved: unknown resolution %r — dropping", resolution)
        return
    severity = "warning" if resolution == "denied" else "info"
    payload: dict[str, Any] = {
        "hook_id": hook_id,
        "tool_name": tool_name,
        "resolution": resolution,
    }
    if tool_call_id:
        payload["tool_call_id"] = tool_call_id
    if conversation_id:
        payload["conversation_id"] = conversation_id
    entry = AuditEntry.create(
        event_type="hook.approval_resolved",
        severity=severity,
        user_id=user_id,
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
