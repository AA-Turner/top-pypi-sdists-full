"""Memory promotion and review pipeline (#920).

This module is the **only** governed path for transitioning memory status
through the review lifecycle. Callers (CLI, web, future agent tools)
flow through these wrappers so reviewer identity, rejection reason, and
decision lineage are captured consistently.

``update_memory_metadata()`` in :mod:`memory_service` still accepts the
review-state fields (``reviewed_by`` / ``reviewed_at`` /
``rejected_reason`` / ``lineage``) for recovery and admin flows, but
promotion/review code MUST go through this module.

Agent-initiated proposals (``proposer="agent"``) are the contract for
the #217 ``save_memory`` tool: the tool is expected to call
:func:`propose_candidate` — it should not bypass this module to land
active memory directly.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Final

from .artifacts import ArtifactType
from .memory_service import (
    _LINEAGE_EVENT_NAMES,
    MEMORY_CATEGORIES,
    MEMORY_SCOPES,
    MEMORY_STATUSES,
    create_memory,
    get_memory,
    list_memories,
    update_memory_metadata,
)

if TYPE_CHECKING:
    from ..config import MemoryPromotionConfig
    from ..db import ThreadSafeConnection

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class PromotionError(Exception):
    """Base class for promotion-pipeline failures."""


class PromotionStateError(PromotionError):
    """Raised when a state transition is invalid for the memory's current status."""


class PromotionRateLimitError(PromotionError):
    """Raised when a conversation has hit its candidate proposal cap."""

    def __init__(self, *, conversation_id: str, cap: int, current: int) -> None:
        super().__init__(f"Candidate proposal cap reached for conversation {conversation_id}: {current}/{cap}")
        self.conversation_id = conversation_id
        self.cap = cap
        self.current = current


class PromotionAgentDisabledError(PromotionError):
    """Raised when an agent proposal arrives and agent proposals are disabled."""


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


_PROPOSERS: Final = frozenset({"user", "agent"})

# Transitions permitted by the promotion service. Direct
# update_memory_metadata calls remain free to flip status for
# recovery / admin, but this module only allows these moves.
_APPROVABLE_STATUSES: Final = frozenset({"candidate", "pending_review"})
_REJECTABLE_STATUSES: Final = frozenset({"candidate", "pending_review"})


# ---------------------------------------------------------------------------
# Lineage helpers
# ---------------------------------------------------------------------------


def _utcnow_iso() -> str:
    """ISO-8601 UTC timestamp with Z suffix, second resolution."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _append_lineage(
    metadata: dict[str, Any],
    event: str,
    *,
    actor: str,
    actor_id: str | None = None,
    notes: str | None = None,
    from_status: str | None = None,
    to_status: str | None = None,
    max_entries: int,
) -> list[dict[str, Any]]:
    """Return a new lineage list with *event* appended, bounded by *max_entries*.

    Mutates nothing on the input ``metadata``; callers are expected to
    pass the returned list back through ``update_memory_metadata``.

    When the existing lineage plus the new entry would exceed
    *max_entries*, the oldest non-creation entries are dropped (FIFO) and
    a ``{"event": "truncated", ...}`` marker is appended so audit-trail
    intent is preserved. The caller's new entry is never truncated.
    """
    if event not in _LINEAGE_EVENT_NAMES:
        raise ValueError(f"Unknown lineage event: {event!r}")

    existing = list(metadata.get("lineage") or [])
    entry: dict[str, Any] = {
        "event": event,
        "actor": actor,
        "at": _utcnow_iso(),
    }
    if actor_id is not None:
        entry["actor_id"] = actor_id
    if notes is not None:
        entry["notes"] = notes
    if from_status is not None:
        entry["from_status"] = from_status
    if to_status is not None:
        entry["to_status"] = to_status

    combined = existing + [entry]
    if len(combined) <= max_entries:
        return combined

    # Need to truncate. Keep the new entry and the most recent entries
    # up to ``max_entries - 1``, then reserve the last slot for a
    # truncated-marker so callers can see that history was dropped.
    kept_tail = combined[-(max_entries - 1) :] if max_entries > 1 else [entry]
    truncated_marker = {
        "event": "truncated",
        "actor": "system",
        "at": _utcnow_iso(),
    }
    return [truncated_marker, *kept_tail]


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------


def _check_candidate_rate_limit(
    db: ThreadSafeConnection,
    conversation_id: str | None,
    *,
    max_per_conversation: int,
) -> None:
    """Raise :class:`PromotionRateLimitError` when a conversation has hit its cap.

    A ``None`` or empty *conversation_id* disables the check — proposals
    from outside a live conversation (CLI `memory propose` without a
    session, workflow outcomes, admin imports) are not rate-limited.
    """
    if not conversation_id:
        return
    if max_per_conversation < 1:
        return

    # Count candidate / pending_review memories whose provenance matches
    # this conversation. We use the existing storage query surface
    # (list_memories) and filter in Python; per-conversation volumes are
    # expected to stay well below the cap.
    existing = list_memories(db)
    count = sum(
        1
        for m in existing
        if (m.get("metadata") or {}).get("provenance", {}).get("conversation_id") == conversation_id
        and (m.get("metadata") or {}).get("memory_status") in _APPROVABLE_STATUSES
    )
    if count >= max_per_conversation:
        raise PromotionRateLimitError(
            conversation_id=conversation_id,
            cap=max_per_conversation,
            current=count,
        )


# ---------------------------------------------------------------------------
# Proposals
# ---------------------------------------------------------------------------


def propose_candidate(
    db: ThreadSafeConnection,
    *,
    content: str,
    scope: str,
    category: str,
    proposer: str,
    proposer_id: str | None,
    provenance: dict[str, str | None] | None = None,
    project_slug: str | None = None,
    config: MemoryPromotionConfig,
    name: str | None = None,
) -> dict[str, Any]:
    """Propose a new memory candidate and return the persisted artifact.

    The candidate lands in the status specified by
    ``config.default_review_state`` (``"candidate"`` or
    ``"pending_review"``) unless ``config.local_auto_approve`` is true,
    in which case it is created with ``memory_status="active"`` and an
    ``auto_approved`` lineage entry.

    Agent proposals (``proposer="agent"``) are rejected with
    :class:`PromotionAgentDisabledError` when
    ``config.agent_proposals_enabled`` is false.

    Each successful proposal consumes one of the
    ``config.max_candidates_per_conversation`` slots tied to
    ``provenance["conversation_id"]`` (when present).
    """
    if proposer not in _PROPOSERS:
        raise ValueError(f"proposer must be one of {sorted(_PROPOSERS)}; got {proposer!r}")
    if scope not in MEMORY_SCOPES:
        raise ValueError(f"Invalid memory scope: {scope!r}")
    if category not in MEMORY_CATEGORIES:
        raise ValueError(f"Invalid memory category: {category!r}")

    if proposer == "agent" and not config.agent_proposals_enabled:
        raise PromotionAgentDisabledError(
            "Agent memory proposals are disabled by config (memory.promotion.agent_proposals_enabled=false)"
        )

    prov = dict(provenance or {})
    conversation_id = prov.get("conversation_id") if isinstance(prov.get("conversation_id"), str) else None

    # Rate-limit check before we spend any DB work on creating the artifact.
    _check_candidate_rate_limit(
        db,
        conversation_id,
        max_per_conversation=config.max_candidates_per_conversation,
    )

    if config.local_auto_approve:
        initial_status = "active"
        initial_event = "auto_approved"
        initial_actor = "system"
    else:
        initial_status = config.default_review_state
        initial_event = "proposed"
        initial_actor = proposer

    art = create_memory(
        db,
        content,
        scope=scope,
        category=category,
        project_slug=project_slug,
        name=name,
        provenance=prov,
        status=initial_status,
        created_by=proposer,
    )

    # Stamp initial lineage.  A proposal always starts the audit trail.
    metadata = dict(art.get("metadata") or {})
    lineage = _append_lineage(
        metadata,
        initial_event,
        actor=initial_actor,
        actor_id=proposer_id,
        from_status=None,
        to_status=initial_status,
        max_entries=config.max_lineage_entries,
    )
    updates: dict[str, Any] = {"lineage": lineage}
    if config.local_auto_approve:
        # Record the auto-approver so downstream consumers can tell these
        # apart from reviewer-approved memories.
        updates["reviewed_by"] = "system:auto_approve"
        updates["reviewed_at"] = _utcnow_iso()

    updated = update_memory_metadata(db, art["fqn"], **updates)
    if updated is None:
        # Extremely unlikely — we just created the memory — but be defensive.
        raise PromotionError("Failed to re-read memory after lineage stamp")
    return updated


# ---------------------------------------------------------------------------
# Review actions
# ---------------------------------------------------------------------------


def _load_memory_or_raise(db: ThreadSafeConnection, fqn: str) -> dict[str, Any]:
    mem = get_memory(db, fqn)
    if mem is None:
        raise PromotionStateError(f"Memory not found: {fqn}")
    if mem.get("type") != ArtifactType.MEMORY.value:
        # Defence-in-depth; get_memory already filters non-memory rows.
        raise PromotionStateError(f"Memory not found: {fqn}")
    return mem


def approve_candidate(
    db: ThreadSafeConnection,
    fqn: str,
    *,
    reviewer_id: str,
    reviewer_display: str | None = None,
    edits: dict[str, Any] | None = None,
    config: MemoryPromotionConfig,
) -> dict[str, Any]:
    """Approve a candidate / pending-review memory.

    Optional *edits* can adjust ``content`` or ``memory_category`` in the
    same commit, so a reviewer doesn't have to run a separate ``edit``
    then approve. Raises :class:`PromotionStateError` when the memory is
    in a non-approvable status (``active``, ``rejected``, ``archived``).
    """
    mem = _load_memory_or_raise(db, fqn)
    current_status = (mem.get("metadata") or {}).get("memory_status")
    if current_status not in _APPROVABLE_STATUSES:
        raise PromotionStateError(
            f"Cannot approve memory in status {current_status!r}; "
            f"approvable statuses are {sorted(_APPROVABLE_STATUSES)}"
        )

    # Apply content edit first (if present) — content edits don't touch lineage.
    from .memory_service import update_memory_content

    if edits:
        new_content = edits.get("content")
        new_category = edits.get("category")
        unknown = set(edits) - {"content", "category"}
        if unknown:
            raise ValueError(f"Unknown edit field(s): {sorted(unknown)}")
        if new_content is not None:
            if not isinstance(new_content, str) or not new_content:
                raise ValueError("edits.content must be a non-empty string")
            if update_memory_content(db, fqn, new_content) is None:
                raise PromotionStateError(f"Memory not found during edit: {fqn}")
        if new_category is not None:
            if new_category not in MEMORY_CATEGORIES:
                raise ValueError(f"Invalid edit.category: {new_category!r}")
            if update_memory_metadata(db, fqn, memory_category=new_category) is None:
                raise PromotionStateError(f"Memory not found during category edit: {fqn}")
        # Re-read after edits so the lineage call sees the latest metadata.
        mem = _load_memory_or_raise(db, fqn)

    metadata = dict(mem.get("metadata") or {})
    if edits and "content" in (edits or {}):
        lineage_after_edit = _append_lineage(
            metadata,
            "edit_applied",
            actor=reviewer_display or reviewer_id,
            actor_id=reviewer_id,
            max_entries=config.max_lineage_entries,
        )
        updated = update_memory_metadata(db, fqn, lineage=lineage_after_edit)
        if updated is None:
            raise PromotionStateError(f"Memory not found during lineage update: {fqn}")
        metadata = dict(updated.get("metadata") or {})

    lineage = _append_lineage(
        metadata,
        "approved",
        actor=reviewer_display or reviewer_id,
        actor_id=reviewer_id,
        from_status=current_status,
        to_status="active",
        max_entries=config.max_lineage_entries,
    )
    updated = update_memory_metadata(
        db,
        fqn,
        memory_status="active",
        reviewed_by=reviewer_id,
        reviewed_at=_utcnow_iso(),
        lineage=lineage,
    )
    if updated is None:
        raise PromotionStateError(f"Memory not found during approval commit: {fqn}")
    return updated


def reject_candidate(
    db: ThreadSafeConnection,
    fqn: str,
    *,
    reviewer_id: str,
    reviewer_display: str | None = None,
    reason: str,
    config: MemoryPromotionConfig,
) -> dict[str, Any]:
    """Reject a candidate / pending-review memory with a bounded reason string.

    The ``reason`` is truncated server-side to
    ``config.max_reject_reason_chars`` so a malicious client cannot inflate
    the metadata JSON payload unboundedly.
    """
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reject reason must be a non-empty string")

    mem = _load_memory_or_raise(db, fqn)
    current_status = (mem.get("metadata") or {}).get("memory_status")
    if current_status not in _REJECTABLE_STATUSES:
        raise PromotionStateError(
            f"Cannot reject memory in status {current_status!r}; rejectable statuses are {sorted(_REJECTABLE_STATUSES)}"
        )

    bounded_reason = reason[: max(1, config.max_reject_reason_chars)]

    metadata = dict(mem.get("metadata") or {})
    lineage = _append_lineage(
        metadata,
        "rejected",
        actor=reviewer_display or reviewer_id,
        actor_id=reviewer_id,
        notes=bounded_reason,
        from_status=current_status,
        to_status="rejected",
        max_entries=config.max_lineage_entries,
    )
    updated = update_memory_metadata(
        db,
        fqn,
        memory_status="rejected",
        rejected_reason=bounded_reason,
        reviewed_by=reviewer_id,
        reviewed_at=_utcnow_iso(),
        lineage=lineage,
    )
    if updated is None:
        raise PromotionStateError(f"Memory not found during rejection commit: {fqn}")
    return updated


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------


def list_candidates(
    db: ThreadSafeConnection,
    *,
    namespace: str | None = None,
    status: str = "candidate",
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Return reviewable memories filtered by *status* and optional *namespace*.

    Default *status* is ``"candidate"``; pass ``"pending_review"`` to
    filter the pending-review queue instead. Any valid memory status is
    accepted.
    """
    if status not in MEMORY_STATUSES:
        raise ValueError(f"Invalid status: {status!r}")
    results = list_memories(db, namespace=namespace, status=status)
    if limit is not None and limit >= 0:
        return results[:limit]
    return results
