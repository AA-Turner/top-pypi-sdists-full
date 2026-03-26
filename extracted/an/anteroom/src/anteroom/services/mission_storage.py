"""Mission storage — CRUD for sessions, items, dependencies, executions, revisions, and events."""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

logger = logging.getLogger(__name__)


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Status and column validation
# ---------------------------------------------------------------------------

_VALID_SESSION_STATUSES = frozenset({"pending", "active", "paused", "completed", "failed", "cancelled"})

_VALID_ITEM_STATUSES = frozenset({"pending", "eligible", "active", "completed", "failed", "dropped", "blocked"})

_VALID_EXECUTION_STATUSES = frozenset({"pending", "running", "completed", "failed", "cancelled"})

_ALLOWED_SESSION_UPDATE_COLUMNS: set[str] = {
    "status",
    "title",
    "description",
    "referenced_artifacts_json",
    "lane_limits_json",
    "metadata_json",
    "updated_at",
}

_ALLOWED_ITEM_UPDATE_COLUMNS: set[str] = {
    "status",
    "summary",
    "description",
    "priority",
    "item_type",
    "adapter_type",
    "adapter_config_json",
    "concurrency_group",
    "lane",
    "hold_requested",
    "updated_at",
}

_ALLOWED_EXECUTION_UPDATE_COLUMNS: set[str] = {
    "status",
    "adapter_ref",
    "summary",
    "artifacts_json",
    "started_at",
    "finished_at",
}

_JSON_SESSION_COLUMNS = frozenset({"referenced_artifacts_json", "lane_limits_json", "metadata_json"})
_JSON_ITEM_COLUMNS = frozenset({"adapter_config_json"})
_JSON_EXECUTION_COLUMNS = frozenset({"artifacts_json"})


# ---------------------------------------------------------------------------
# Deserializers
# ---------------------------------------------------------------------------


def _deserialize_session(d: dict[str, Any]) -> dict[str, Any]:
    raw = d.pop("referenced_artifacts_json", None)
    d["referenced_artifacts"] = json.loads(raw) if raw else None
    raw = d.pop("lane_limits_json", None)
    d["lane_limits"] = json.loads(raw) if raw else None
    raw = d.pop("metadata_json", None)
    d["metadata"] = json.loads(raw) if raw else None
    return d


def _deserialize_item(d: dict[str, Any]) -> dict[str, Any]:
    raw = d.pop("adapter_config_json", None)
    d["adapter_config"] = json.loads(raw) if raw else None
    return d


def _deserialize_execution(d: dict[str, Any]) -> dict[str, Any]:
    raw = d.pop("artifacts_json", None)
    d["artifacts"] = json.loads(raw) if raw else None
    return d


def _deserialize_revision(d: dict[str, Any]) -> dict[str, Any]:
    raw = d.pop("operations_json", None)
    d["operations"] = json.loads(raw) if raw else []
    raw = d.pop("plan_snapshot_after_json", None)
    d["plan_snapshot_after"] = json.loads(raw) if raw else None
    raw = d.pop("referenced_artifacts_json", None)
    d["referenced_artifacts"] = json.loads(raw) if raw else None
    return d


def _deserialize_event(d: dict[str, Any]) -> dict[str, Any]:
    raw = d.pop("detail_json", None)
    d["detail"] = json.loads(raw) if raw else None
    return d


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------


def create_session(
    db: ThreadSafeConnection,
    *,
    status: str = "pending",
    title: str | None = None,
    description: str | None = None,
    source_type: str | None = None,
    source_artifact_id: str | None = None,
    source_fqn: str | None = None,
    source_version: int | None = None,
    referenced_artifacts: list[dict[str, Any]] | None = None,
    lane_limits: dict[str, int] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if status not in _VALID_SESSION_STATUSES:
        raise ValueError(f"Invalid session status: {status!r}")
    sid = _uuid()
    now = _now()
    ref_json = json.dumps(referenced_artifacts) if referenced_artifacts else None
    lanes_json = json.dumps(lane_limits) if lane_limits else None
    meta_json = json.dumps(metadata) if metadata else None
    db.execute(
        "INSERT INTO mission_sessions"
        " (id, status, title, description, source_type, source_artifact_id,"
        "  source_fqn, source_version, referenced_artifacts_json,"
        "  lane_limits_json, metadata_json, created_at, updated_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            sid,
            status,
            title,
            description,
            source_type,
            source_artifact_id,
            source_fqn,
            source_version,
            ref_json,
            lanes_json,
            meta_json,
            now,
            now,
        ),
    )
    db.commit()
    return {
        "id": sid,
        "status": status,
        "title": title,
        "description": description,
        "source_type": source_type,
        "source_artifact_id": source_artifact_id,
        "source_fqn": source_fqn,
        "source_version": source_version,
        "referenced_artifacts": referenced_artifacts,
        "lane_limits": lane_limits,
        "metadata": metadata,
        "created_at": now,
        "updated_at": now,
    }


def get_session(db: ThreadSafeConnection, session_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone("SELECT * FROM mission_sessions WHERE id = ?", (session_id,))
    if not row:
        return None
    return _deserialize_session(dict(row))


def list_sessions(
    db: ThreadSafeConnection,
    *,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, Any]]:
    conditions: list[str] = []
    params: list[Any] = []
    if status and status in _VALID_SESSION_STATUSES:
        conditions.append("status = ?")
        params.append(status)
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    params.extend([limit, offset])
    rows = db.execute_fetchall(
        f"SELECT * FROM mission_sessions {where} ORDER BY created_at DESC LIMIT ? OFFSET ?",
        tuple(params),
    )
    return [_deserialize_session(dict(r)) for r in rows]


def update_session(
    db: ThreadSafeConnection,
    session_id: str,
    **updates: Any,
) -> dict[str, Any] | None:
    if not updates:
        return get_session(db, session_id)
    updates["updated_at"] = _now()
    parts: list[str] = []
    params: list[Any] = []
    for col, val in updates.items():
        if col not in _ALLOWED_SESSION_UPDATE_COLUMNS:
            raise ValueError(f"Column {col!r} not in allowed mission_sessions update columns")
        if col in _JSON_SESSION_COLUMNS and isinstance(val, (dict, list)):
            val = json.dumps(val)
        parts.append(f"{col} = ?")
        params.append(val)
    params.append(session_id)
    db.execute(f"UPDATE mission_sessions SET {', '.join(parts)} WHERE id = ?", tuple(params))
    db.commit()
    return get_session(db, session_id)


# ---------------------------------------------------------------------------
# Items
# ---------------------------------------------------------------------------


def create_item(
    db: ThreadSafeConnection,
    *,
    session_id: str,
    summary: str,
    description: str | None = None,
    status: str = "pending",
    priority: int = 50,
    item_type: str = "task",
    adapter_type: str = "noop",
    adapter_config: dict[str, Any] | None = None,
    concurrency_group: str | None = None,
    lane: str | None = None,
    hold_requested: bool = False,
) -> dict[str, Any]:
    if status not in _VALID_ITEM_STATUSES:
        raise ValueError(f"Invalid item status: {status!r}")
    iid = _uuid()
    now = _now()
    config_json = json.dumps(adapter_config) if adapter_config else None
    db.execute(
        "INSERT INTO mission_items"
        " (id, session_id, summary, description, status, priority, item_type,"
        "  adapter_type, adapter_config_json, concurrency_group, lane,"
        "  hold_requested, created_at, updated_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            iid,
            session_id,
            summary,
            description,
            status,
            priority,
            item_type,
            adapter_type,
            config_json,
            concurrency_group,
            lane,
            1 if hold_requested else 0,
            now,
            now,
        ),
    )
    db.commit()
    return {
        "id": iid,
        "session_id": session_id,
        "summary": summary,
        "description": description,
        "status": status,
        "priority": priority,
        "item_type": item_type,
        "adapter_type": adapter_type,
        "adapter_config": adapter_config,
        "concurrency_group": concurrency_group,
        "lane": lane,
        "hold_requested": 1 if hold_requested else 0,
        "created_at": now,
        "updated_at": now,
    }


def get_item(db: ThreadSafeConnection, item_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone("SELECT * FROM mission_items WHERE id = ?", (item_id,))
    if not row:
        return None
    return _deserialize_item(dict(row))


def list_items_by_session(
    db: ThreadSafeConnection,
    session_id: str,
    *,
    status: str | None = None,
) -> list[dict[str, Any]]:
    conditions = ["session_id = ?"]
    params: list[Any] = [session_id]
    if status and status in _VALID_ITEM_STATUSES:
        conditions.append("status = ?")
        params.append(status)
    where = "WHERE " + " AND ".join(conditions)
    rows = db.execute_fetchall(
        f"SELECT * FROM mission_items {where} ORDER BY priority ASC, created_at ASC",
        tuple(params),
    )
    return [_deserialize_item(dict(r)) for r in rows]


def update_item(
    db: ThreadSafeConnection,
    item_id: str,
    **updates: Any,
) -> dict[str, Any] | None:
    if not updates:
        return get_item(db, item_id)
    updates["updated_at"] = _now()
    parts: list[str] = []
    params: list[Any] = []
    for col, val in updates.items():
        if col not in _ALLOWED_ITEM_UPDATE_COLUMNS:
            raise ValueError(f"Column {col!r} not in allowed mission_items update columns")
        if col in _JSON_ITEM_COLUMNS and isinstance(val, (dict, list)):
            val = json.dumps(val)
        parts.append(f"{col} = ?")
        params.append(val)
    params.append(item_id)
    db.execute(f"UPDATE mission_items SET {', '.join(parts)} WHERE id = ?", tuple(params))
    db.commit()
    return get_item(db, item_id)


# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------


def add_dependency(db: ThreadSafeConnection, *, item_id: str, depends_on_id: str) -> None:
    if item_id == depends_on_id:
        raise ValueError("An item cannot depend on itself")
    row = db.execute_fetchone(
        "SELECT a.session_id AS a_sid, b.session_id AS b_sid"
        " FROM mission_items a, mission_items b"
        " WHERE a.id = ? AND b.id = ?",
        (item_id, depends_on_id),
    )
    if not row:
        raise ValueError("One or both item IDs do not exist")
    if row["a_sid"] != row["b_sid"]:
        raise ValueError("Cannot add dependency across different mission sessions")
    db.execute(
        "INSERT OR IGNORE INTO mission_item_dependencies (item_id, depends_on_id) VALUES (?, ?)",
        (item_id, depends_on_id),
    )
    db.commit()


def remove_dependency(db: ThreadSafeConnection, *, item_id: str, depends_on_id: str) -> None:
    db.execute(
        "DELETE FROM mission_item_dependencies WHERE item_id = ? AND depends_on_id = ?",
        (item_id, depends_on_id),
    )
    db.commit()


def get_dependencies(db: ThreadSafeConnection, item_id: str) -> list[str]:
    rows = db.execute_fetchall(
        "SELECT depends_on_id FROM mission_item_dependencies WHERE item_id = ?",
        (item_id,),
    )
    return [r["depends_on_id"] for r in rows]


def get_dependents(db: ThreadSafeConnection, item_id: str) -> list[str]:
    rows = db.execute_fetchall(
        "SELECT item_id FROM mission_item_dependencies WHERE depends_on_id = ?",
        (item_id,),
    )
    return [r["item_id"] for r in rows]


# ---------------------------------------------------------------------------
# Executions
# ---------------------------------------------------------------------------


def create_execution(
    db: ThreadSafeConnection,
    *,
    item_id: str,
    attempt_number: int,
    status: str = "pending",
    adapter_ref: str | None = None,
) -> dict[str, Any]:
    if status not in _VALID_EXECUTION_STATUSES:
        raise ValueError(f"Invalid execution status: {status!r}")
    eid = _uuid()
    now = _now()
    db.execute(
        "INSERT INTO mission_executions"
        " (id, item_id, attempt_number, status, adapter_ref, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        (eid, item_id, attempt_number, status, adapter_ref, now),
    )
    db.commit()
    return {
        "id": eid,
        "item_id": item_id,
        "attempt_number": attempt_number,
        "status": status,
        "adapter_ref": adapter_ref,
        "summary": None,
        "artifacts": None,
        "started_at": None,
        "finished_at": None,
        "created_at": now,
    }


def get_execution(db: ThreadSafeConnection, execution_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone("SELECT * FROM mission_executions WHERE id = ?", (execution_id,))
    if not row:
        return None
    return _deserialize_execution(dict(row))


def list_executions_by_item(db: ThreadSafeConnection, item_id: str) -> list[dict[str, Any]]:
    rows = db.execute_fetchall(
        "SELECT * FROM mission_executions WHERE item_id = ? ORDER BY attempt_number ASC",
        (item_id,),
    )
    return [_deserialize_execution(dict(r)) for r in rows]


def get_latest_execution(db: ThreadSafeConnection, item_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone(
        "SELECT * FROM mission_executions WHERE item_id = ? ORDER BY attempt_number DESC LIMIT 1",
        (item_id,),
    )
    if not row:
        return None
    return _deserialize_execution(dict(row))


def update_execution(
    db: ThreadSafeConnection,
    execution_id: str,
    **updates: Any,
) -> dict[str, Any] | None:
    if not updates:
        return get_execution(db, execution_id)
    parts: list[str] = []
    params: list[Any] = []
    for col, val in updates.items():
        if col not in _ALLOWED_EXECUTION_UPDATE_COLUMNS:
            raise ValueError(f"Column {col!r} not in allowed mission_executions update columns")
        if col in _JSON_EXECUTION_COLUMNS and isinstance(val, (dict, list)):
            val = json.dumps(val)
        parts.append(f"{col} = ?")
        params.append(val)
    params.append(execution_id)
    db.execute(f"UPDATE mission_executions SET {', '.join(parts)} WHERE id = ?", tuple(params))
    db.commit()
    return get_execution(db, execution_id)


# ---------------------------------------------------------------------------
# Revisions
# ---------------------------------------------------------------------------


def create_revision(
    db: ThreadSafeConnection,
    *,
    session_id: str,
    revision_number: int,
    operations: list[dict[str, Any]],
    plan_snapshot_after: dict[str, Any] | list[dict[str, Any]],
    referenced_artifacts: list[dict[str, Any]] | None = None,
    reason: str | None = None,
) -> dict[str, Any]:
    rid = _uuid()
    now = _now()
    ops_json = json.dumps(operations)
    snap_json = json.dumps(plan_snapshot_after)
    ref_json = json.dumps(referenced_artifacts) if referenced_artifacts else None
    db.execute(
        "INSERT INTO mission_revisions"
        " (id, session_id, revision_number, operations_json,"
        "  plan_snapshot_after_json, referenced_artifacts_json, reason, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (rid, session_id, revision_number, ops_json, snap_json, ref_json, reason, now),
    )
    db.commit()
    return {
        "id": rid,
        "session_id": session_id,
        "revision_number": revision_number,
        "operations": operations,
        "plan_snapshot_after": plan_snapshot_after,
        "referenced_artifacts": referenced_artifacts,
        "reason": reason,
        "created_at": now,
    }


def list_revisions(
    db: ThreadSafeConnection,
    session_id: str,
) -> list[dict[str, Any]]:
    rows = db.execute_fetchall(
        "SELECT * FROM mission_revisions WHERE session_id = ? ORDER BY revision_number ASC",
        (session_id,),
    )
    return [_deserialize_revision(dict(r)) for r in rows]


def get_revision(db: ThreadSafeConnection, revision_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone("SELECT * FROM mission_revisions WHERE id = ?", (revision_id,))
    if not row:
        return None
    return _deserialize_revision(dict(row))


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------


def create_event(
    db: ThreadSafeConnection,
    *,
    session_id: str,
    event_type: str,
    item_id: str | None = None,
    detail: dict[str, Any] | None = None,
) -> dict[str, Any]:
    now = _now()
    detail_json = json.dumps(detail) if detail else None
    cursor = db.execute(
        "INSERT INTO mission_events (session_id, item_id, event_type, detail_json, created_at) VALUES (?, ?, ?, ?, ?)",
        (session_id, item_id, event_type, detail_json, now),
    )
    db.commit()
    return {
        "id": cursor.lastrowid,
        "session_id": session_id,
        "item_id": item_id,
        "event_type": event_type,
        "detail": detail,
        "created_at": now,
    }


def list_events(
    db: ThreadSafeConnection,
    session_id: str,
    *,
    event_type: str | None = None,
    item_id: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict[str, Any]]:
    conditions = ["session_id = ?"]
    params: list[Any] = [session_id]
    if event_type:
        conditions.append("event_type = ?")
        params.append(event_type)
    if item_id:
        conditions.append("item_id = ?")
        params.append(item_id)
    where = "WHERE " + " AND ".join(conditions)
    params.extend([limit, offset])
    rows = db.execute_fetchall(
        f"SELECT * FROM mission_events {where} ORDER BY id ASC LIMIT ? OFFSET ?",
        tuple(params),
    )
    return [_deserialize_event(dict(r)) for r in rows]


# ---------------------------------------------------------------------------
# Scheduler queries
# ---------------------------------------------------------------------------


def count_active_by_lane(db: ThreadSafeConnection, session_id: str) -> dict[str, int]:
    rows = db.execute_fetchall(
        "SELECT lane, COUNT(*) as cnt FROM mission_items"
        " WHERE session_id = ? AND status = 'active' AND lane IS NOT NULL"
        " GROUP BY lane",
        (session_id,),
    )
    return {r["lane"]: r["cnt"] for r in rows}


def count_active_by_concurrency_group(db: ThreadSafeConnection, session_id: str) -> dict[str, int]:
    rows = db.execute_fetchall(
        "SELECT concurrency_group, COUNT(*) as cnt FROM mission_items"
        " WHERE session_id = ? AND status = 'active' AND concurrency_group IS NOT NULL"
        " GROUP BY concurrency_group",
        (session_id,),
    )
    return {r["concurrency_group"]: r["cnt"] for r in rows}


def list_eligible_items(
    db: ThreadSafeConnection,
    session_id: str,
) -> list[dict[str, Any]]:
    """Return pending items with all dependencies completed and not held.

    An item is eligible when:
    - status = 'pending'
    - hold_requested = 0
    - every dependency (mission_item_dependencies) has status = 'completed'

    Note: lane limits and concurrency group limits are NOT enforced here.
    The scheduler (#1045) applies those constraints by calling
    ``count_active_by_lane()`` and ``count_active_by_concurrency_group()``
    and filtering the results of this function before launching items.
    """
    rows = db.execute_fetchall(
        "SELECT i.* FROM mission_items i"
        " WHERE i.session_id = ? AND i.status = 'pending' AND i.hold_requested = 0"
        " AND NOT EXISTS ("
        "   SELECT 1 FROM mission_item_dependencies d"
        "   JOIN mission_items dep ON dep.id = d.depends_on_id"
        "   WHERE d.item_id = i.id AND dep.status != 'completed'"
        " )"
        " ORDER BY i.priority ASC, i.created_at ASC",
        (session_id,),
    )
    return [_deserialize_item(dict(r)) for r in rows]


# ---------------------------------------------------------------------------
# Plan snapshot
# ---------------------------------------------------------------------------


def build_plan_snapshot(db: ThreadSafeConnection, session_id: str) -> dict[str, Any]:
    """Build a JSON-serializable snapshot of the current plan state."""
    items = list_items_by_session(db, session_id)
    deps: dict[str, list[str]] = {}
    for item in items:
        deps[item["id"]] = get_dependencies(db, item["id"])
    return {"items": items, "dependencies": deps}
