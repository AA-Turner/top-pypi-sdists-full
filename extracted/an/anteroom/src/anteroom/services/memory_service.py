"""Memory artifact service — typed, scoped, governed memory CRUD.

Wraps artifact storage with memory-specific validation: scope→namespace
derivation, category/status constraints, provenance validation, and
freshness tracking.  All memory-specific fields live in the artifact
``metadata`` JSON column — no schema migration required.

FQN convention: ``@{namespace}/memory/{slug}``

Scope→namespace mapping (enforced here, not by callers):

==========  ==============  ====================================
Scope       Namespace       When
==========  ==============  ====================================
``user``    ``"user"``      Global / cross-project memories
``project`` *project_slug*  Project-specific memories
``local``   ``"local"``     Space-local / ephemeral memories
==========  ==============  ====================================
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

from .artifact_storage import (
    create_artifact,
    delete_artifact,
    get_artifact_by_fqn,
    list_artifacts,
    update_artifact,
)
from .artifacts import ArtifactType, build_fqn

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MEMORY_SCOPES: Final = frozenset({"user", "project", "local"})
MEMORY_CATEGORIES: Final = frozenset({"preference", "project_fact", "decision", "workflow_hint"})
MEMORY_STATUSES: Final = frozenset({"active", "candidate", "pending_review", "rejected", "archived"})

# Namespaces reserved for non-project scopes.  A project_slug must never
# collide with these — otherwise a ``project``-scoped memory would land in
# the same namespace as a ``user`` or ``local`` memory and break the
# scope-boundary contract that the rest of the service assumes.
_RESERVED_NAMESPACES: Final = frozenset({"user", "local"})

# Memory metadata fields that are mutable via ``update_memory_metadata``.
# Any key not in this set is rejected.  ``memory_scope`` and ``created_by``
# are immutable by design (scope is encoded in the FQN; created_by is
# provenance).
#
# The review-state fields (``reviewed_by``, ``reviewed_at``,
# ``rejected_reason``, ``lineage``) live here so that promotion-service
# commits go through the same validation path.  Direct callers of
# ``update_memory_metadata()`` can still write these for recovery /
# admin flows, but governed promotion transitions MUST go through
# ``services.memory_promotion`` (#920).
_MUTABLE_METADATA_FIELDS: Final = frozenset(
    {
        "memory_status",
        "memory_category",
        "promoted_by",
        "last_recalled_at",
        "recall_count",
        "provenance",
        "reviewed_by",
        "reviewed_at",
        "rejected_reason",
        "lineage",
        # #625 retention — pin flag is load-bearing for eviction policy.
        "pinned",
    }
)

# Hard cap on a single rejection reason's length in SQLite.  The service
# layer enforces a per-install bound via ``MemoryPromotionConfig`` as
# well, but this backstop prevents pathological writes even if a caller
# bypasses the service.
_MAX_REJECTED_REASON_LEN: Final = 2000

# Allowed lineage event names.  Defence-in-depth: callers must use one
# of these so metadata consumers can safely pattern-match on the event.
_LINEAGE_EVENT_NAMES: Final = frozenset(
    {
        "proposed",
        "auto_approved",
        "approved",
        "rejected",
        "edit_applied",
        "truncated",
    }
)

_FQN_NAMESPACE_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,62}$")
_UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)
_MAX_PROVENANCE_LEN = 36

# Ensure every category value is FQN-safe (only [a-z0-9_]).
_FQN_NAME_SAFE = re.compile(r"^[a-z0-9_]+$")
for _cat in MEMORY_CATEGORIES:
    assert _FQN_NAME_SAFE.match(_cat), f"Category {_cat!r} is not FQN-safe"

# Short prefixes for auto-generated slug names.
_CATEGORY_PREFIX: Final[dict[str, str]] = {
    "preference": "pref",
    "project_fact": "fact",
    "decision": "dec",
    "workflow_hint": "hint",
}


# ---------------------------------------------------------------------------
# Scope → namespace
# ---------------------------------------------------------------------------


def namespace_for_scope(scope: str, project_slug: str | None = None) -> str:
    """Derive the artifact namespace from a memory scope.

    Raises ``ValueError`` for invalid scope or missing *project_slug* when
    ``scope="project"``.
    """
    if scope not in MEMORY_SCOPES:
        raise ValueError(f"Invalid memory scope: {scope!r} — expected one of {sorted(MEMORY_SCOPES)}")
    if scope == "user":
        return "user"
    if scope == "local":
        return "local"
    # scope == "project"
    if not project_slug:
        raise ValueError("project_slug is required when scope is 'project'")
    if not _FQN_NAMESPACE_RE.match(project_slug):
        raise ValueError(f"Invalid project_slug: {project_slug!r} — must match [a-z0-9][a-z0-9._-]{{0,62}}")
    if project_slug in _RESERVED_NAMESPACES:
        raise ValueError(
            f"Invalid project_slug: {project_slug!r} — value collides with a reserved scope namespace "
            f"({sorted(_RESERVED_NAMESPACES)}). Use a project-specific slug."
        )
    return project_slug


# ---------------------------------------------------------------------------
# Metadata helpers
# ---------------------------------------------------------------------------


def _validate_provenance_id(value: str | None, field_name: str) -> None:
    """Validate a provenance ID is a UUID or within length bounds."""
    if value is None:
        return
    if not isinstance(value, str):
        raise ValueError(f"Provenance field {field_name!r} must be a string or None")
    if len(value) > _MAX_PROVENANCE_LEN:
        raise ValueError(f"Provenance field {field_name!r} exceeds max length ({_MAX_PROVENANCE_LEN}): {len(value)}")


def _build_memory_metadata(
    scope: str,
    category: str,
    status: str,
    provenance: dict[str, str | None] | None,
    created_by: str,
) -> dict[str, Any]:
    """Assemble and validate a memory metadata dict."""
    if scope not in MEMORY_SCOPES:
        raise ValueError(f"Invalid memory scope: {scope!r}")
    if category not in MEMORY_CATEGORIES:
        raise ValueError(f"Invalid memory category: {category!r}")
    if status not in MEMORY_STATUSES:
        raise ValueError(f"Invalid memory status: {status!r}")
    if created_by not in ("user", "agent"):
        raise ValueError(f"Invalid created_by: {created_by!r} — expected 'user' or 'agent'")

    prov = provenance or {}
    for key in ("conversation_id", "message_id", "workflow_run_id", "source_artifact_id"):
        _validate_provenance_id(prov.get(key), key)

    return {
        "memory_scope": scope,
        "memory_category": category,
        "memory_status": status,
        "provenance": {
            "conversation_id": prov.get("conversation_id"),
            "message_id": prov.get("message_id"),
            "workflow_run_id": prov.get("workflow_run_id"),
            "source_artifact_id": prov.get("source_artifact_id"),
        },
        "created_by": created_by,
        "promoted_by": None,
        "last_recalled_at": None,
        "recall_count": 0,
    }


def _generate_memory_slug(content: str, category: str) -> str:
    """Generate a deterministic slug: ``{prefix}-{hash6}-{date}``."""
    prefix = _CATEGORY_PREFIX.get(category, category[:4])
    h = hashlib.sha256(content.encode("utf-8")).hexdigest()[:6]
    date = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"{prefix}-{h}-{date}"


# ---------------------------------------------------------------------------
# Type-boundary helpers
# ---------------------------------------------------------------------------


def _fetch_memory_or_none(db: ThreadSafeConnection, fqn: str) -> dict[str, Any] | None:
    """Fetch an artifact by FQN, returning it only if it is a memory artifact.

    Returns ``None`` when the FQN does not exist **or** when it resolves to an
    artifact of a different type.  This enforces the service-level boundary:
    non-memory FQNs cannot be read, mutated, or deleted through the memory
    service.
    """
    existing = get_artifact_by_fqn(db, fqn)
    if not existing:
        return None
    if existing.get("type") != ArtifactType.MEMORY.value:
        return None
    return existing


def _validate_mutable_metadata(fields: dict[str, Any]) -> None:
    """Validate kwargs passed to ``update_memory_metadata``.

    Rejects unknown keys and validates the typed contract for each recognised
    memory metadata field.  ``memory_scope`` is handled separately by the
    caller (immutable) and must not appear here.
    """
    unknown = set(fields) - _MUTABLE_METADATA_FIELDS
    if unknown:
        raise ValueError(
            f"Unknown memory metadata field(s): {sorted(unknown)} — "
            f"allowed fields are {sorted(_MUTABLE_METADATA_FIELDS)}"
        )

    if "memory_status" in fields and fields["memory_status"] not in MEMORY_STATUSES:
        raise ValueError(f"Invalid memory_status: {fields['memory_status']!r}")

    if "memory_category" in fields and fields["memory_category"] not in MEMORY_CATEGORIES:
        raise ValueError(f"Invalid memory_category: {fields['memory_category']!r}")

    if "promoted_by" in fields:
        _validate_provenance_id(fields["promoted_by"], "promoted_by")

    if "last_recalled_at" in fields:
        value = fields["last_recalled_at"]
        if value is not None and not isinstance(value, str):
            raise ValueError("last_recalled_at must be an ISO-8601 string or None")

    if "recall_count" in fields:
        value = fields["recall_count"]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("recall_count must be a non-negative integer")

    if "provenance" in fields:
        prov = fields["provenance"]
        if prov is None or not isinstance(prov, dict):
            raise ValueError("provenance must be a dict")
        allowed_keys = {"conversation_id", "message_id", "workflow_run_id", "source_artifact_id"}
        extra = set(prov) - allowed_keys
        if extra:
            raise ValueError(f"Unknown provenance field(s): {sorted(extra)}")
        for key in allowed_keys:
            _validate_provenance_id(prov.get(key), key)

    if "reviewed_by" in fields:
        value = fields["reviewed_by"]
        if value is not None and not isinstance(value, str):
            raise ValueError("reviewed_by must be a string or None")
        if isinstance(value, str) and len(value) > _MAX_PROVENANCE_LEN:
            raise ValueError(f"reviewed_by exceeds max length ({_MAX_PROVENANCE_LEN}): {len(value)}")

    if "reviewed_at" in fields:
        value = fields["reviewed_at"]
        if value is not None and not isinstance(value, str):
            raise ValueError("reviewed_at must be an ISO-8601 string or None")

    if "rejected_reason" in fields:
        value = fields["rejected_reason"]
        if value is not None and not isinstance(value, str):
            raise ValueError("rejected_reason must be a string or None")
        if isinstance(value, str) and len(value) > _MAX_REJECTED_REASON_LEN:
            raise ValueError(f"rejected_reason exceeds hard cap ({_MAX_REJECTED_REASON_LEN} chars): {len(value)}")

    if "lineage" in fields:
        lineage = fields["lineage"]
        if not isinstance(lineage, list):
            raise ValueError("lineage must be a list of dicts")
        for idx, entry in enumerate(lineage):
            if not isinstance(entry, dict):
                raise ValueError(f"lineage[{idx}] must be a dict")
            event = entry.get("event")
            if event not in _LINEAGE_EVENT_NAMES:
                raise ValueError(f"lineage[{idx}].event must be one of {sorted(_LINEAGE_EVENT_NAMES)}; got {event!r}")
            at_value = entry.get("at")
            if not isinstance(at_value, str) or not at_value:
                raise ValueError(f"lineage[{idx}].at must be a non-empty ISO-8601 string")
            actor = entry.get("actor")
            if actor is not None and not isinstance(actor, str):
                raise ValueError(f"lineage[{idx}].actor must be a string or absent")
            # Optional fields validated only if present.
            for opt_key in ("actor_id", "notes", "from_status", "to_status"):
                if opt_key in entry and entry[opt_key] is not None and not isinstance(entry[opt_key], str):
                    raise ValueError(f"lineage[{idx}].{opt_key} must be a string or None")

    if "pinned" in fields:
        value = fields["pinned"]
        # ``isinstance(True, int)`` is True, so check bool explicitly to
        # reject int/float inputs that would silently truthy-convert.
        if not isinstance(value, bool):
            raise ValueError("pinned must be a bool")


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------


def create_memory(
    db: ThreadSafeConnection,
    content: str,
    scope: str,
    category: str,
    *,
    project_slug: str | None = None,
    name: str | None = None,
    provenance: dict[str, str | None] | None = None,
    status: str = "active",
    created_by: str = "user",
    user_id: str | None = None,
    user_display_name: str | None = None,
) -> dict[str, Any]:
    """Create a new memory artifact.

    The namespace and FQN are derived from *scope* (and *project_slug* when
    ``scope="project"``).  Callers do **not** pass a namespace directly.
    """
    namespace = namespace_for_scope(scope, project_slug)
    metadata = _build_memory_metadata(scope, category, status, provenance, created_by)
    slug = name or _generate_memory_slug(content, category)
    fqn = build_fqn(namespace, ArtifactType.MEMORY.value, slug)

    return create_artifact(
        db,
        fqn=fqn,
        artifact_type=ArtifactType.MEMORY,
        namespace=namespace,
        name=slug,
        content=content,
        metadata=metadata,
        user_id=user_id,
        user_display_name=user_display_name,
    )


def get_memory(db: ThreadSafeConnection, fqn: str) -> dict[str, Any] | None:
    """Fetch a single memory artifact by FQN.

    Returns ``None`` if the FQN does not resolve to a memory-typed artifact,
    even when a different artifact exists at that FQN.  This prevents the
    memory service from reading other artifact types.
    """
    return _fetch_memory_or_none(db, fqn)


def get_memory_provenance(db: ThreadSafeConnection, fqn: str) -> dict[str, Any] | None:
    """Return the ``provenance`` dict stored on a memory's metadata.

    Helper for #925 lineage resolution. Returns ``None`` when the memory
    does not exist or has no provenance recorded. Values are returned as
    stored (conversation_id, message_id, etc.) without transformation.
    """
    mem = _fetch_memory_or_none(db, fqn)
    if mem is None:
        return None
    prov = (mem.get("metadata") or {}).get("provenance")
    if not isinstance(prov, dict):
        return None
    return dict(prov)


def list_memories(
    db: ThreadSafeConnection,
    *,
    scope: str | None = None,
    category: str | None = None,
    status: str | None = None,
    namespace: str | None = None,
) -> list[dict[str, Any]]:
    """List memory artifacts with optional metadata-based filters.

    *namespace* is passed through to the storage query for efficient DB-level
    filtering.  *scope*, *category*, and *status* are post-filtered from
    metadata (acceptable at V1 scale).
    """
    results = list_artifacts(db, artifact_type=ArtifactType.MEMORY, namespace=namespace)
    if scope is not None:
        results = [r for r in results if r.get("metadata", {}).get("memory_scope") == scope]
    if category is not None:
        results = [r for r in results if r.get("metadata", {}).get("memory_category") == category]
    if status is not None:
        results = [r for r in results if r.get("metadata", {}).get("memory_status") == status]
    return results


def update_memory_content(
    db: ThreadSafeConnection,
    fqn: str,
    content: str,
) -> dict[str, Any] | None:
    """Update a memory's content, preserving its metadata.

    Passes ``metadata=None`` to ``update_artifact()`` so existing metadata is
    not overwritten.  Returns ``None`` if the FQN does not resolve to a
    memory-typed artifact.
    """
    existing = _fetch_memory_or_none(db, fqn)
    if not existing:
        return None
    return update_artifact(db, existing["id"], content=content, metadata=None)


def update_memory_metadata(
    db: ThreadSafeConnection,
    fqn: str,
    **fields: Any,
) -> dict[str, Any] | None:
    """Update memory-domain metadata fields using a read-then-merge pattern.

    Only the specified *fields* are updated; all others are preserved.

    Recognised (mutable) fields: ``memory_status``, ``memory_category``,
    ``promoted_by``, ``last_recalled_at``, ``recall_count``, ``provenance``.

    Immutable fields:
      * ``memory_scope`` — encoded in the FQN; create a new memory instead.
      * ``created_by`` — provenance, never rewritten.

    Raises ``ValueError`` if any unknown key or invalid value is supplied —
    the typed metadata contract is enforced on update, not just on create.
    Returns ``None`` if the FQN does not resolve to a memory-typed artifact.
    """
    if "memory_scope" in fields:
        raise ValueError("Cannot change memory_scope — scope is encoded in the FQN. Create a new memory instead.")
    if "created_by" in fields:
        raise ValueError("Cannot change created_by — this field is immutable provenance.")

    # Validate the caller's kwargs against the typed contract before any DB
    # read.  Unknown keys and invalid values are rejected here.
    _validate_mutable_metadata(fields)

    existing = _fetch_memory_or_none(db, fqn)
    if not existing:
        return None

    merged = dict(existing.get("metadata") or {})
    merged.update(fields)
    return update_artifact(db, existing["id"], content=None, metadata=merged)


def delete_memory(db: ThreadSafeConnection, fqn: str) -> bool:
    """Delete a memory artifact by FQN.

    Returns ``False`` if the FQN does not exist **or** resolves to a
    non-memory artifact — the memory service must not delete other types.
    """
    existing = _fetch_memory_or_none(db, fqn)
    if not existing:
        return False
    return delete_artifact(db, existing["id"])


# ---------------------------------------------------------------------------
# Pin / unpin (#625)
# ---------------------------------------------------------------------------


def pin_memory(db: ThreadSafeConnection, fqn: str) -> dict[str, Any] | None:
    """Mark a memory as pinned so retention workers will skip it by default.

    Returns the updated artifact dict, or ``None`` if the FQN does not
    resolve to a memory artifact.
    """
    return update_memory_metadata(db, fqn, pinned=True)


def unpin_memory(db: ThreadSafeConnection, fqn: str) -> dict[str, Any] | None:
    """Remove the pin flag from a memory.

    Returns the updated artifact dict, or ``None`` if the FQN does not
    resolve to a memory artifact.
    """
    return update_memory_metadata(db, fqn, pinned=False)
