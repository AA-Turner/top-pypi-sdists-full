"""Workflow engine storage — CRUD for runs, steps, events, approval requests, and locks."""

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


_VALID_RUN_STATUSES = frozenset(
    {
        "pending",
        "claimed",
        "running",
        "paused",
        "waiting_for_approval",
        "waiting_for_input",
        "blocked",
        "completed",
        "failed",
        "cancelled",
        "compensating",
        "compensated",
        "compensation_failed",
    }
)

_TERMINAL_RUN_STATUSES = frozenset({"completed", "failed", "cancelled", "compensated", "compensation_failed"})

_REPAIRABLE_RUN_STATUSES = frozenset({"paused", "waiting_for_approval", "waiting_for_input", "failed"})

_RESUMABLE_RUN_STATUSES = frozenset(
    {"paused", "waiting_for_approval", "waiting_for_input", "compensating", "failed", "blocked"}
)

_REPAIRABLE_RUN_FIELDS = frozenset({"inputs"})

_REPAIRABLE_STEP_FIELDS = frozenset({"result_artifacts", "result_summary"})

_VALID_STEP_STATUSES = frozenset({"pending", "running", "completed", "failed", "interrupted", "skipped"})

_VALID_APPROVAL_STATUSES = frozenset({"pending", "approved", "denied", "expired"})

_ALLOWED_RUN_UPDATE_COLUMNS: set[str] = {
    "status",
    "current_step_id",
    "attempt_count",
    "stop_reason",
    "updated_at",
    "started_at",
    "completed_at",
    "heartbeat_at",
    "definition_hash",
    "definition_content",
    "budget_json",
    "budget_usage_json",
    "trigger_source",
    "trigger_meta_json",
    "claimed_by",
    "claimed_at",
    "cancel_requested",
    "conversation_id",
    "result_summary",
}


# ---------------------------------------------------------------------------
# Workflow Runs
# ---------------------------------------------------------------------------


def create_workflow_run(
    db: ThreadSafeConnection,
    *,
    workflow_id: str,
    workflow_version: str,
    target_kind: str,
    target_ref: str,
    inputs: dict[str, Any] | None = None,
    space_id: str | None = None,
    definition_hash: str | None = None,
    definition_content: str | None = None,
    budget: dict[str, Any] | None = None,
    trigger_source: str | None = None,
    trigger_meta: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    conversation_id: str | None = None,
) -> dict[str, Any]:
    rid = _uuid()
    now = _now()
    inputs_json = json.dumps(inputs) if inputs else None
    params_json = json.dumps(params) if params else None
    budget_json = json.dumps(budget) if budget else None
    budget_usage_json = (
        json.dumps(
            {
                "elapsed_seconds": 0,
                "steps_completed": 0,
                "total_tokens": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
            }
        )
        if budget
        else None
    )
    trigger_meta_json = json.dumps(trigger_meta) if trigger_meta else None
    db.execute(
        "INSERT INTO workflow_runs"
        " (id, workflow_id, workflow_version, status, target_kind, target_ref,"
        "  inputs_json, params_json, space_id, definition_hash, definition_content,"
        "  budget_json, budget_usage_json, trigger_source, trigger_meta_json,"
        "  conversation_id, created_at, updated_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            rid,
            workflow_id,
            workflow_version,
            "pending",
            target_kind,
            target_ref,
            inputs_json,
            params_json,
            space_id,
            definition_hash,
            definition_content,
            budget_json,
            budget_usage_json,
            trigger_source,
            trigger_meta_json,
            conversation_id,
            now,
            now,
        ),
    )
    db.commit()
    return {
        "id": rid,
        "workflow_id": workflow_id,
        "workflow_version": workflow_version,
        "status": "pending",
        "target_kind": target_kind,
        "target_ref": target_ref,
        "current_step_id": None,
        "attempt_count": 0,
        "stop_reason": None,
        "inputs": inputs,
        "params": params,
        "space_id": space_id,
        "created_at": now,
        "updated_at": now,
        "started_at": None,
        "completed_at": None,
        "definition_hash": definition_hash,
        "definition_content": definition_content,
        "budget": budget,
        "budget_usage": json.loads(budget_usage_json) if budget_usage_json else None,
        "trigger_source": trigger_source,
        "trigger_meta": trigger_meta,
        "claimed_by": None,
        "claimed_at": None,
        "cancel_requested": 0,
        "conversation_id": conversation_id,
    }


def get_workflow_run(db: ThreadSafeConnection, run_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone("SELECT * FROM workflow_runs WHERE id = ?", (run_id,))
    if not row:
        return None
    return _deserialize_run(dict(row))


def resolve_workflow_run_id(db: ThreadSafeConnection, run_ref: str, *, max_matches: int = 5) -> str:
    """Resolve an exact run ID or a unique prefix to a full workflow run ID."""
    row = db.execute_fetchone("SELECT id FROM workflow_runs WHERE id = ?", (run_ref,))
    if row:
        return str(row["id"])

    rows = db.execute_fetchall(
        "SELECT id FROM workflow_runs WHERE id LIKE ? ORDER BY created_at DESC LIMIT ?",
        (f"{run_ref}%", max_matches + 1),
    )
    if not rows:
        raise ValueError(f"Run not found: {run_ref}")
    if len(rows) == 1:
        return str(rows[0]["id"])

    samples = ", ".join(str(r["id"])[:12] for r in rows[:max_matches])
    if len(rows) > max_matches:
        samples += ", ..."
    raise ValueError(f"Ambiguous run ID prefix: {run_ref} ({samples})")


def _deserialize_run(d: dict[str, Any]) -> dict[str, Any]:
    raw_inputs = d.pop("inputs_json", None)
    d["inputs"] = json.loads(raw_inputs) if raw_inputs else None
    raw_params = d.pop("params_json", None)
    d["params"] = json.loads(raw_params) if raw_params else None
    raw_budget = d.pop("budget_json", None)
    d["budget"] = json.loads(raw_budget) if raw_budget else None
    raw_usage = d.pop("budget_usage_json", None)
    d["budget_usage"] = json.loads(raw_usage) if raw_usage else None
    raw_trigger_meta = d.pop("trigger_meta_json", None)
    d["trigger_meta"] = json.loads(raw_trigger_meta) if raw_trigger_meta else None
    return d


_JSON_RUN_COLUMNS = frozenset({"budget_json", "budget_usage_json"})


def update_workflow_run(
    db: ThreadSafeConnection,
    run_id: str,
    **updates: Any,
) -> dict[str, Any] | None:
    if not updates:
        return get_workflow_run(db, run_id)
    updates["updated_at"] = _now()
    parts: list[str] = []
    params: list[Any] = []
    for col, val in updates.items():
        if col not in _ALLOWED_RUN_UPDATE_COLUMNS:
            raise ValueError(f"Column {col!r} not in allowed workflow_runs update columns")
        # Auto-serialize dict/list values for JSON columns
        if col in _JSON_RUN_COLUMNS and isinstance(val, (dict, list)):
            val = json.dumps(val)
        parts.append(f"{col} = ?")
        params.append(val)
    params.append(run_id)
    db.execute(f"UPDATE workflow_runs SET {', '.join(parts)} WHERE id = ?", tuple(params))
    db.commit()
    return get_workflow_run(db, run_id)


def list_workflow_runs(
    db: ThreadSafeConnection,
    *,
    status: str | None = None,
    workflow_id: str | None = None,
    target_kind: str | None = None,
    target_ref: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[dict[str, Any]]:
    conditions: list[str] = []
    params: list[Any] = []
    if status and status in _VALID_RUN_STATUSES:
        conditions.append("status = ?")
        params.append(status)
    if workflow_id:
        conditions.append("workflow_id = ?")
        params.append(workflow_id)
    if target_kind:
        conditions.append("target_kind = ?")
        params.append(target_kind)
    if target_ref:
        conditions.append("target_ref = ?")
        params.append(target_ref)
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    params.extend([limit, offset])
    rows = db.execute_fetchall(
        f"SELECT * FROM workflow_runs {where} ORDER BY created_at DESC LIMIT ? OFFSET ?",
        tuple(params),
    )
    results = []
    for r in rows:
        d = _deserialize_run(dict(r))
        d.pop("definition_content", None)  # Exclude bulky content from list
        results.append(d)
    return results


def delete_workflow_run(db: ThreadSafeConnection, run_id: str) -> bool:
    row = db.execute_fetchone("SELECT id FROM workflow_runs WHERE id = ?", (run_id,))
    if not row:
        return False
    db.execute("DELETE FROM workflow_runs WHERE id = ?", (run_id,))
    db.commit()
    return True


def claim_pending_runs(
    db: ThreadSafeConnection,
    worker_id: str,
    limit: int = 3,
) -> list[dict[str, Any]]:
    """Atomically claim up to *limit* pending runs for a worker.

    Uses UPDATE ... WHERE id IN (subselect) + rowcount + follow-up SELECT
    scoped by both *worker_id* and the exact *claimed_at* timestamp.
    """
    now_iso = _now()
    cursor = db.execute(
        "UPDATE workflow_runs SET status = 'claimed', claimed_by = ?, claimed_at = ?"
        " WHERE id IN ("
        "   SELECT id FROM workflow_runs"
        "   WHERE status = 'pending' AND claimed_by IS NULL"
        "   ORDER BY created_at ASC LIMIT ?"
        " )",
        (worker_id, now_iso, limit),
    )
    db.commit()
    if cursor.rowcount == 0:
        return []
    rows = db.execute_fetchall(
        "SELECT * FROM workflow_runs WHERE claimed_by = ? AND claimed_at = ?",
        (worker_id, now_iso),
    )
    return [_deserialize_run(dict(r)) for r in rows]


def claim_workflow_run(
    db: ThreadSafeConnection,
    run_id: str,
    worker_id: str,
) -> dict[str, Any] | None:
    """Atomically claim a specific pending run for a worker."""
    now_iso = _now()
    cursor = db.execute(
        "UPDATE workflow_runs SET status = 'claimed', claimed_by = ?, claimed_at = ?"
        " WHERE id = ? AND status = 'pending' AND claimed_by IS NULL",
        (worker_id, now_iso, run_id),
    )
    db.commit()
    if cursor.rowcount == 0:
        return None
    row = db.execute_fetchone("SELECT * FROM workflow_runs WHERE id = ?", (run_id,))
    return _deserialize_run(dict(row)) if row else None


def reset_stale_claims(
    db: ThreadSafeConnection,
    stale_threshold_seconds: int = 50,
) -> int:
    """Reset claimed runs whose claim is older than threshold back to pending.

    Returns the number of runs reset.
    """
    from datetime import timedelta

    cutoff = (datetime.now(timezone.utc) - timedelta(seconds=stale_threshold_seconds)).isoformat()
    cursor = db.execute(
        "UPDATE workflow_runs SET status = 'pending', claimed_by = NULL, claimed_at = NULL,"
        " updated_at = ? WHERE status = 'claimed' AND claimed_at < ?",
        (_now(), cutoff),
    )
    db.commit()
    return cursor.rowcount


def find_stale_runs(
    db: ThreadSafeConnection,
    stale_threshold_seconds: int = 60,
) -> list[dict[str, Any]]:
    """Find runs stuck in 'running' or 'compensating' with heartbeat older than threshold."""
    from datetime import timedelta

    cutoff = (datetime.now(timezone.utc) - timedelta(seconds=stale_threshold_seconds)).isoformat()
    rows = db.execute_fetchall(
        "SELECT * FROM workflow_runs WHERE status IN ('running', 'compensating')"
        " AND (heartbeat_at IS NULL OR heartbeat_at < ?)",
        (cutoff,),
    )
    return [_deserialize_run(dict(r)) for r in rows]


def find_running_steps(
    db: ThreadSafeConnection,
    run_id: str,
) -> list[dict[str, Any]]:
    """Find step records with status='running' for a given run."""
    rows = db.execute_fetchall(
        "SELECT * FROM workflow_steps WHERE run_id = ? AND status = 'running'",
        (run_id,),
    )
    return [_deserialize_step(dict(r)) for r in rows]


def list_completed_step_ids(
    db: ThreadSafeConnection,
    run_id: str,
) -> set[str]:
    """Return step_ids of completed steps for a given run."""
    rows = db.execute_fetchall(
        "SELECT step_id FROM workflow_steps WHERE run_id = ? AND status = 'completed'",
        (run_id,),
    )
    return {r["step_id"] for r in rows}


# ---------------------------------------------------------------------------
# Cancel-request helpers (#890)
# ---------------------------------------------------------------------------


def set_cancel_requested(db: ThreadSafeConnection, run_id: str) -> None:
    """Mark a workflow run as cancel-requested."""
    db.execute("UPDATE workflow_runs SET cancel_requested = 1 WHERE id = ?", (run_id,))
    db.commit()


def is_cancel_requested(db: ThreadSafeConnection, run_id: str) -> bool:
    """Check whether cancel has been requested for a workflow run."""
    row = db.execute_fetchone("SELECT cancel_requested FROM workflow_runs WHERE id = ?", (run_id,))
    if not row:
        return False
    return bool(row["cancel_requested"])


def get_active_run_for_conversation(db: ThreadSafeConnection, conversation_id: str) -> dict[str, Any] | None:
    """Return the most recent non-terminal workflow run for a conversation."""
    terminal = tuple(_TERMINAL_RUN_STATUSES)
    placeholders = ", ".join("?" for _ in terminal)
    row = db.execute_fetchone(
        f"SELECT * FROM workflow_runs WHERE conversation_id = ? AND status NOT IN ({placeholders})"
        " ORDER BY created_at DESC LIMIT 1",
        (conversation_id, *terminal),
    )
    if not row:
        return None
    return _deserialize_run(dict(row))


# ---------------------------------------------------------------------------
# Workflow Steps
# ---------------------------------------------------------------------------


_VALID_STEP_TYPES = frozenset({"runner", "gate", "loop", "human_gate", "publish", "llm", "parallel", "emit"})


def create_workflow_step(
    db: ThreadSafeConnection,
    *,
    run_id: str,
    step_id: str,
    step_type: str,
    runner_type: str | None = None,
    attempt: int = 1,
    idempotency_key: str | None = None,
    branch_id: str | None = None,
    is_compensation: int = 0,
) -> dict[str, Any]:
    if step_type not in _VALID_STEP_TYPES:
        raise ValueError(f"Invalid step_type: {step_type!r}")
    sid = _uuid()
    now = _now()
    db.execute(
        "INSERT INTO workflow_steps"
        " (id, run_id, step_id, step_type, runner_type, status, attempt,"
        "  idempotency_key, branch_id, is_compensation, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            sid,
            run_id,
            step_id,
            step_type,
            runner_type,
            "pending",
            attempt,
            idempotency_key,
            branch_id,
            is_compensation,
            now,
        ),
    )
    db.commit()
    return {
        "id": sid,
        "run_id": run_id,
        "step_id": step_id,
        "step_type": step_type,
        "runner_type": runner_type,
        "status": "pending",
        "attempt": attempt,
        "result_status": None,
        "result_summary": None,
        "result_artifacts": None,
        "result_findings": None,
        "raw_output_path": None,
        "duration_ms": None,
        "idempotency_key": idempotency_key,
        "branch_id": branch_id,
        "is_compensation": is_compensation,
        "created_at": now,
        "started_at": None,
        "completed_at": None,
    }


def get_workflow_step(db: ThreadSafeConnection, step_record_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone("SELECT * FROM workflow_steps WHERE id = ?", (step_record_id,))
    if not row:
        return None
    return _deserialize_step(dict(row))


def list_workflow_steps(db: ThreadSafeConnection, run_id: str) -> list[dict[str, Any]]:
    rows = db.execute_fetchall(
        "SELECT * FROM workflow_steps WHERE run_id = ? ORDER BY created_at",
        (run_id,),
    )
    return [_deserialize_step(dict(r)) for r in rows]


def list_branch_steps(
    db: ThreadSafeConnection,
    run_id: str,
    branch_id: str,
) -> list[dict[str, Any]]:
    """Return step records for a specific branch within a parallel step (#976)."""
    rows = db.execute_fetchall(
        "SELECT * FROM workflow_steps WHERE run_id = ? AND branch_id = ? ORDER BY created_at",
        (run_id, branch_id),
    )
    return [_deserialize_step(dict(r)) for r in rows]


def list_compensation_steps(
    db: ThreadSafeConnection,
    run_id: str,
) -> list[dict[str, Any]]:
    """Return step records for compensation steps within a run (#978)."""
    rows = db.execute_fetchall(
        "SELECT * FROM workflow_steps WHERE run_id = ? AND is_compensation = 1 ORDER BY created_at",
        (run_id,),
    )
    return [_deserialize_step(dict(r)) for r in rows]


def update_workflow_step(
    db: ThreadSafeConnection,
    step_record_id: str,
    *,
    status: str | None = None,
    result_status: str | None = None,
    result_summary: str | None = None,
    result_artifacts: dict[str, Any] | None = None,
    result_findings: list[dict[str, Any]] | None = None,
    result_outputs: dict[str, Any] | None = None,
    raw_output_path: str | None = None,
    duration_ms: int | None = None,
    started_at: str | None = None,
    completed_at: str | None = None,
    approval_request_id: str | None = None,
    decision_id: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any] | None:
    parts: list[str] = []
    params: list[Any] = []
    if status is not None:
        parts.append("status = ?")
        params.append(status)
    if result_status is not None:
        parts.append("result_status = ?")
        params.append(result_status)
    if result_summary is not None:
        parts.append("result_summary = ?")
        params.append(result_summary)
    if result_artifacts is not None:
        parts.append("result_artifacts_json = ?")
        params.append(json.dumps(result_artifacts))
    if result_findings is not None:
        parts.append("result_findings_json = ?")
        params.append(json.dumps(result_findings))
    if result_outputs is not None:
        parts.append("result_outputs_json = ?")
        params.append(json.dumps(result_outputs))
    if raw_output_path is not None:
        parts.append("raw_output_path = ?")
        params.append(raw_output_path)
    if duration_ms is not None:
        parts.append("duration_ms = ?")
        params.append(duration_ms)
    if started_at is not None:
        parts.append("started_at = ?")
        params.append(started_at)
    if completed_at is not None:
        parts.append("completed_at = ?")
        params.append(completed_at)
    if approval_request_id is not None:
        parts.append("approval_request_id = ?")
        params.append(approval_request_id)
    if decision_id is not None:
        parts.append("decision_id = ?")
        params.append(decision_id)
    if idempotency_key is not None:
        parts.append("idempotency_key = ?")
        params.append(idempotency_key)
    if not parts:
        return get_workflow_step(db, step_record_id)
    params.append(step_record_id)
    db.execute(f"UPDATE workflow_steps SET {', '.join(parts)} WHERE id = ?", tuple(params))
    db.commit()
    return get_workflow_step(db, step_record_id)


def _deserialize_step(d: dict[str, Any]) -> dict[str, Any]:
    raw_artifacts = d.pop("result_artifacts_json", None)
    d["result_artifacts"] = json.loads(raw_artifacts) if raw_artifacts else None
    raw_findings = d.pop("result_findings_json", None)
    d["result_findings"] = json.loads(raw_findings) if raw_findings else None
    raw_outputs = d.pop("result_outputs_json", None)
    d["result_outputs"] = json.loads(raw_outputs) if raw_outputs else None
    return d


# ---------------------------------------------------------------------------
# Workflow Events
# ---------------------------------------------------------------------------


def create_workflow_event(
    db: ThreadSafeConnection,
    *,
    run_id: str,
    event_type: str,
    step_id: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    now = _now()
    payload_json = json.dumps(payload) if payload else None
    cursor = db.execute(
        "INSERT INTO workflow_events (run_id, step_id, event_type, payload_json, created_at) VALUES (?, ?, ?, ?, ?)",
        (run_id, step_id, event_type, payload_json, now),
    )
    db.commit()
    return {
        "id": cursor.lastrowid,
        "run_id": run_id,
        "step_id": step_id,
        "event_type": event_type,
        "payload": payload,
        "created_at": now,
    }


def list_workflow_events(db: ThreadSafeConnection, run_id: str) -> list[dict[str, Any]]:
    rows = db.execute_fetchall(
        "SELECT * FROM workflow_events WHERE run_id = ? ORDER BY id",
        (run_id,),
    )
    results = []
    for r in rows:
        d = dict(r)
        raw = d.pop("payload_json", None)
        d["payload"] = json.loads(raw) if raw else None
        results.append(d)
    return results


def get_run_replay_events(
    db: ThreadSafeConnection,
    run_id: str,
) -> list[dict[str, Any]]:
    """Return transcript + lifecycle events merged for replay, ordered by id."""
    rows = db.execute_fetchall(
        "SELECT id, run_id, step_id, event_type, payload_json, created_at "
        "FROM workflow_events "
        "WHERE run_id = ? AND ("
        "  event_type LIKE 'transcript_%' "
        "  OR event_type IN ('step_started', 'step_finished', 'step_failed')"
        ") ORDER BY id",
        (run_id,),
    )
    results = []
    for r in rows:
        d = dict(r)
        raw = d.pop("payload_json", None)
        d["payload"] = json.loads(raw) if raw else None
        results.append(d)
    return results


def list_transcript_events(
    db: ThreadSafeConnection,
    run_id: str,
    step_id: str | None = None,
    *,
    since_id: int = 0,
) -> list[dict[str, Any]]:
    """Return transcript events for a run, optionally filtered by step and since_id."""
    if step_id:
        rows = db.execute_fetchall(
            "SELECT * FROM workflow_events "
            "WHERE run_id = ? AND step_id = ? AND event_type LIKE 'transcript_%' AND id > ? "
            "ORDER BY id",
            (run_id, step_id, since_id),
        )
    else:
        rows = db.execute_fetchall(
            "SELECT * FROM workflow_events WHERE run_id = ? AND event_type LIKE 'transcript_%' AND id > ? ORDER BY id",
            (run_id, since_id),
        )
    results = []
    for r in rows:
        d = dict(r)
        raw = d.pop("payload_json", None)
        d["payload"] = json.loads(raw) if raw else None
        results.append(d)
    return results


# ---------------------------------------------------------------------------
# Workflow Approval Requests
# ---------------------------------------------------------------------------


def create_approval_request(
    db: ThreadSafeConnection,
    *,
    run_id: str,
    step_id: str,
    tool_name: str,
    tool_args: dict[str, Any],
    risk_tier: str,
    timeout_at: str | None = None,
) -> dict[str, Any]:
    aid = _uuid()
    now = _now()
    db.execute(
        "INSERT INTO workflow_approval_requests"
        " (id, run_id, step_id, tool_name, tool_args_json, risk_tier, status, timeout_at, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (aid, run_id, step_id, tool_name, json.dumps(tool_args), risk_tier, "pending", timeout_at, now),
    )
    db.commit()
    return {
        "id": aid,
        "run_id": run_id,
        "step_id": step_id,
        "tool_name": tool_name,
        "tool_args": tool_args,
        "risk_tier": risk_tier,
        "status": "pending",
        "resolved_by": None,
        "resolved_at": None,
        "timeout_at": timeout_at,
        "created_at": now,
    }


def get_approval_request(db: ThreadSafeConnection, request_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone("SELECT * FROM workflow_approval_requests WHERE id = ?", (request_id,))
    if not row:
        return None
    return _deserialize_approval(dict(row))


def get_pending_approval(db: ThreadSafeConnection, run_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone(
        "SELECT * FROM workflow_approval_requests WHERE run_id = ? AND status = 'pending' ORDER BY created_at DESC",
        (run_id,),
    )
    if not row:
        return None
    return _deserialize_approval(dict(row))


def resolve_approval_request(
    db: ThreadSafeConnection,
    request_id: str,
    *,
    status: str,
    resolved_by: str | None = None,
) -> dict[str, Any] | None:
    if status not in ("approved", "denied", "expired"):
        raise ValueError(f"Invalid approval resolution: {status!r}")
    now = _now()
    cursor = db.execute(
        "UPDATE workflow_approval_requests SET status = ?, resolved_by = ?, resolved_at = ?"
        " WHERE id = ? AND status = 'pending'",
        (status, resolved_by, now, request_id),
    )
    db.commit()
    if cursor.rowcount == 0:
        existing = get_approval_request(db, request_id)
        if existing and existing["status"] != "pending":
            raise ValueError(
                f"Approval request {request_id} already resolved as"
                f" {existing['status']!r}; cannot transition to {status!r}"
            )
        return None
    return get_approval_request(db, request_id)


def _deserialize_approval(d: dict[str, Any]) -> dict[str, Any]:
    raw = d.pop("tool_args_json", None)
    d["tool_args"] = json.loads(raw) if raw else None
    return d


# ---------------------------------------------------------------------------
# Workflow Locks
# ---------------------------------------------------------------------------


def acquire_lock(
    db: ThreadSafeConnection,
    *,
    target_kind: str,
    target_ref: str,
    run_id: str,
) -> bool:
    import sqlite3

    now = _now()
    try:
        db.execute(
            "INSERT INTO workflow_locks (target_kind, target_ref, run_id, acquired_at) VALUES (?, ?, ?, ?)",
            (target_kind, target_ref, run_id, now),
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def release_lock(db: ThreadSafeConnection, *, run_id: str) -> bool:
    cursor = db.execute("DELETE FROM workflow_locks WHERE run_id = ?", (run_id,))
    db.commit()
    return cursor.rowcount > 0


def release_lock_by_target(
    db: ThreadSafeConnection,
    *,
    target_kind: str,
    target_ref: str,
) -> bool:
    cursor = db.execute(
        "DELETE FROM workflow_locks WHERE target_kind = ? AND target_ref = ?",
        (target_kind, target_ref),
    )
    db.commit()
    return cursor.rowcount > 0


def get_lock(
    db: ThreadSafeConnection,
    *,
    target_kind: str,
    target_ref: str,
) -> dict[str, Any] | None:
    row = db.execute_fetchone(
        "SELECT * FROM workflow_locks WHERE target_kind = ? AND target_ref = ?",
        (target_kind, target_ref),
    )
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# Human Decisions (#955)
# ---------------------------------------------------------------------------


def create_human_decision(
    db: ThreadSafeConnection,
    *,
    run_id: str,
    step_id: str,
    prompt: str,
    context: str | None = None,
    options: list[dict[str, Any]],
    timeout_at: str | None = None,
) -> dict[str, Any]:
    did = _uuid()
    now = _now()
    db.execute(
        "INSERT INTO workflow_human_decisions"
        " (id, run_id, step_id, status, prompt, context_json, options_json, timeout_at, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (did, run_id, step_id, "pending", prompt, context, json.dumps(options), timeout_at, now),
    )
    db.commit()
    return {
        "id": did,
        "run_id": run_id,
        "step_id": step_id,
        "status": "pending",
        "prompt": prompt,
        "context": context,
        "options": options,
        "selected_option": None,
        "resolved_by": None,
        "resolved_at": None,
        "timeout_at": timeout_at,
        "created_at": now,
    }


def get_human_decision(db: ThreadSafeConnection, decision_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone("SELECT * FROM workflow_human_decisions WHERE id = ?", (decision_id,))
    if not row:
        return None
    return _deserialize_decision(dict(row))


def get_pending_decision(db: ThreadSafeConnection, run_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone(
        "SELECT * FROM workflow_human_decisions WHERE run_id = ? AND status = 'pending' ORDER BY created_at DESC",
        (run_id,),
    )
    if not row:
        return None
    return _deserialize_decision(dict(row))


def resolve_human_decision(
    db: ThreadSafeConnection,
    decision_id: str,
    *,
    selected_option: str,
    resolved_by: str | None = None,
) -> dict[str, Any] | None:
    now = _now()
    cursor = db.execute(
        "UPDATE workflow_human_decisions SET status = 'resolved', selected_option = ?,"
        " resolved_by = ?, resolved_at = ? WHERE id = ? AND status = 'pending'",
        (selected_option, resolved_by, now, decision_id),
    )
    db.commit()
    if cursor.rowcount == 0:
        existing = get_human_decision(db, decision_id)
        if existing and existing["status"] != "pending":
            raise ValueError(
                f"Human decision {decision_id} already resolved as {existing['status']!r}; cannot resolve again"
            )
        return None
    return get_human_decision(db, decision_id)


def check_approval_timeouts(db: ThreadSafeConnection) -> int:
    """Check and expire pending approval requests past their timeout. Returns count."""
    now = _now()
    cursor = db.execute(
        "UPDATE workflow_approval_requests SET status = 'expired', resolved_by = 'timeout',"
        " resolved_at = ? WHERE status = 'pending' AND timeout_at IS NOT NULL AND timeout_at < ?",
        (now, now),
    )
    db.commit()
    return cursor.rowcount


def check_decision_timeouts(db: ThreadSafeConnection) -> int:
    """Check and expire pending human decisions past their timeout. Returns count."""
    now = _now()
    cursor = db.execute(
        "UPDATE workflow_human_decisions SET status = 'expired',"
        " resolved_at = ? WHERE status = 'pending' AND timeout_at IS NOT NULL AND timeout_at < ?",
        (now, now),
    )
    db.commit()
    return cursor.rowcount


def _deserialize_decision(d: dict[str, Any]) -> dict[str, Any]:
    raw_ctx = d.pop("context_json", None)
    d["context"] = raw_ctx  # context is stored as plain text, not JSON
    raw_opts = d.pop("options_json", None)
    d["options"] = json.loads(raw_opts) if raw_opts else []
    return d


# ---------------------------------------------------------------------------
# Workflow Checkpoints (#979)
# ---------------------------------------------------------------------------


def create_checkpoint(
    db: ThreadSafeConnection,
    *,
    run_id: str,
    label: str,
    step_id: str | None,
    step_results: dict[str, Any],
    budget_usage: dict[str, Any] | None,
    run_status: str,
) -> dict[str, Any]:
    sid = _uuid()
    now = _now()
    db.execute(
        "INSERT INTO workflow_checkpoints"
        " (id, run_id, label, step_id, step_results_json, budget_usage_json, run_status, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            sid,
            run_id,
            label,
            step_id,
            json.dumps(step_results),
            json.dumps(budget_usage) if budget_usage else None,
            run_status,
            now,
        ),
    )
    db.commit()
    return {
        "id": sid,
        "run_id": run_id,
        "label": label,
        "step_id": step_id,
        "step_results": step_results,
        "budget_usage": budget_usage,
        "run_status": run_status,
        "created_at": now,
    }


def list_checkpoints(db: ThreadSafeConnection, run_id: str) -> list[dict[str, Any]]:
    rows = db.execute(
        "SELECT id, run_id, label, step_id, step_results_json, budget_usage_json, run_status, created_at"
        " FROM workflow_checkpoints WHERE run_id = ? ORDER BY created_at",
        (run_id,),
    ).fetchall()
    return [_checkpoint_row_to_dict(r) for r in rows]


def get_latest_checkpoint(db: ThreadSafeConnection, run_id: str) -> dict[str, Any] | None:
    row = db.execute(
        "SELECT id, run_id, label, step_id, step_results_json, budget_usage_json, run_status, created_at"
        " FROM workflow_checkpoints WHERE run_id = ? ORDER BY created_at DESC LIMIT 1",
        (run_id,),
    ).fetchone()
    return _checkpoint_row_to_dict(row) if row else None


def count_checkpoints(db: ThreadSafeConnection, run_id: str) -> int:
    row = db.execute(
        "SELECT COUNT(*) FROM workflow_checkpoints WHERE run_id = ?",
        (run_id,),
    ).fetchone()
    return row[0] if row else 0


def list_runs_by_spec(db: ThreadSafeConnection, spec_fqn: str) -> list[dict[str, Any]]:
    """List workflow runs linked to a spec artifact via ``inputs_json``.

    Returns run summaries with ``task_id`` extracted from inputs.
    """
    rows = db.execute_fetchall(
        "SELECT id, workflow_id, status, inputs_json, created_at, completed_at"
        " FROM workflow_runs"
        " WHERE json_extract(inputs_json, '$.spec_fqn') = ?"
        " ORDER BY created_at DESC",
        (spec_fqn,),
    )
    results: list[dict[str, Any]] = []
    for row in rows:
        d = dict(row)
        raw_inputs = d.pop("inputs_json", None)
        inputs = json.loads(raw_inputs) if raw_inputs else {}
        d["task_id"] = inputs.get("task_id")
        d["spec_fqn"] = inputs.get("spec_fqn")
        results.append(d)
    return results


def count_runs_by_spec(db: ThreadSafeConnection, spec_fqn: str) -> dict[str, int]:
    """Return aggregate run counts for a spec FQN."""
    row = db.execute(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed,
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed,
            SUM(CASE WHEN status IN ('running', 'claimed') THEN 1 ELSE 0 END) AS running,
            SUM(CASE WHEN status = 'blocked' THEN 1 ELSE 0 END) AS blocked
        FROM workflow_runs
        WHERE json_extract(inputs_json, '$.spec_fqn') = ?
        """,
        (spec_fqn,),
    ).fetchone()
    if row is None:
        return {"total": 0, "completed": 0, "failed": 0, "running": 0, "blocked": 0}
    return {
        "total": row[0] or 0,
        "completed": row[1] or 0,
        "failed": row[2] or 0,
        "running": row[3] or 0,
        "blocked": row[4] or 0,
    }


def list_spec_blocked_runs(db: ThreadSafeConnection, spec_fqn: str) -> list[dict[str, Any]]:
    """List workflow runs blocked at spec-gate steps for a specific spec."""
    sql = (
        "SELECT r.id, r.workflow_id, r.status, r.stop_reason,"
        "       r.current_step_id, r.created_at"
        " FROM workflow_runs r"
        " JOIN workflow_steps s ON s.run_id = r.id"
        " WHERE json_extract(r.inputs_json, '$.spec_fqn') = ?"
        "   AND r.status = 'blocked'"
        "   AND s.step_type = 'gate'"
        "   AND s.result_status = 'blocked'"
        "   AND s.result_summary LIKE 'Phase%'"
        " ORDER BY r.created_at DESC"
    )
    rows = db.execute_fetchall(sql, (spec_fqn,))
    return [dict(r) for r in rows]


def _checkpoint_row_to_dict(row: Any) -> dict[str, Any]:
    if isinstance(row, dict):
        d = dict(row)
    else:
        d = dict(row)
    raw_results = d.pop("step_results_json", None)
    d["step_results"] = json.loads(raw_results) if raw_results else {}
    raw_budget = d.pop("budget_usage_json", None)
    d["budget_usage"] = json.loads(raw_budget) if raw_budget else None
    return d


# ---------------------------------------------------------------------------
# Workflow Repair (#995)
# ---------------------------------------------------------------------------


def apply_run_repair(
    db: ThreadSafeConnection,
    run_id: str,
    field: str,
    value: Any,
    *,
    actor: str = "operator",
) -> dict[str, Any]:
    """Apply a repair to a repairable field on a paused/waiting run.

    Validates the run is in a repairable status and the field is allowed.
    Records the repair as a workflow event with before/after context.
    Returns the updated run dict.
    """
    if field not in _REPAIRABLE_RUN_FIELDS:
        raise ValueError(f"Field {field!r} is not repairable. Allowed: {sorted(_REPAIRABLE_RUN_FIELDS)}")

    run = get_workflow_run(db, run_id)
    if not run:
        raise ValueError(f"Run not found: {run_id}")
    if run["status"] not in _REPAIRABLE_RUN_STATUSES:
        raise ValueError(
            f"Run {run_id} is not repairable (status: {run['status']}). "
            f"Only {sorted(_REPAIRABLE_RUN_STATUSES)} runs can be repaired."
        )

    old_value = run.get(field)

    # Apply the repair via direct column update
    if field == "inputs":
        serialized = json.dumps(value) if value is not None else None
        if serialized and len(serialized.encode("utf-8")) > _MAX_INPUTS_SIZE:
            raise ValueError("Repaired inputs exceed 64KB limit")
        db.execute(
            "UPDATE workflow_runs SET inputs_json = ?, updated_at = ? WHERE id = ?",
            (serialized, _now(), run_id),
        )
    else:
        raise ValueError(f"No update handler for repairable field {field!r}")
    db.commit()

    # Record as event
    create_workflow_event(
        db,
        run_id=run_id,
        event_type="repair_applied",
        payload={
            "scope": "run",
            "field": field,
            "old_value": old_value,
            "new_value": value,
            "actor": actor,
        },
    )

    return get_workflow_run(db, run_id)  # type: ignore[return-value]


def apply_step_repair(
    db: ThreadSafeConnection,
    run_id: str,
    step_id: str,
    field: str,
    value: Any,
    *,
    actor: str = "operator",
) -> dict[str, Any]:
    """Apply a repair to a repairable field on a completed step within a paused/waiting run.

    Validates the run status, the step exists and is completed, and the field
    is allowed. Records the repair as a workflow event.
    Returns the updated step dict.
    """
    if field not in _REPAIRABLE_STEP_FIELDS:
        raise ValueError(f"Field {field!r} is not repairable. Allowed: {sorted(_REPAIRABLE_STEP_FIELDS)}")

    run = get_workflow_run(db, run_id)
    if not run:
        raise ValueError(f"Run not found: {run_id}")
    if run["status"] not in _REPAIRABLE_RUN_STATUSES:
        raise ValueError(
            f"Run {run_id} is not repairable (status: {run['status']}). "
            f"Only {sorted(_REPAIRABLE_RUN_STATUSES)} runs can be repaired."
        )

    # Find the latest step record for this step_id
    steps = list_workflow_steps(db, run_id)
    step_record = None
    for s in reversed(steps):
        if s["step_id"] == step_id:
            step_record = s
            break
    if not step_record:
        raise ValueError(f"Step {step_id!r} not found in run {run_id}")
    if step_record["status"] != "completed":
        raise ValueError(
            f"Step {step_id!r} is not completed (status: {step_record['status']}). "
            f"Only completed steps can be repaired."
        )

    old_value = step_record.get(field)

    # Apply the repair
    update_kwargs: dict[str, Any] = {}
    if field == "result_artifacts":
        update_kwargs["result_artifacts"] = value
    elif field == "result_summary":
        update_kwargs["result_summary"] = value

    update_workflow_step(db, step_record["id"], **update_kwargs)

    # Record as event
    create_workflow_event(
        db,
        run_id=run_id,
        step_id=step_id,
        event_type="repair_applied",
        payload={
            "scope": "step",
            "step_id": step_id,
            "field": field,
            "old_value": old_value,
            "new_value": value,
            "actor": actor,
        },
    )

    return get_workflow_step(db, step_record["id"])  # type: ignore[return-value]


def list_repairs(db: ThreadSafeConnection, run_id: str) -> list[dict[str, Any]]:
    """List all repair events for a run."""
    events = list_workflow_events(db, run_id)
    return [e for e in events if e["event_type"] == "repair_applied"]


# ---------------------------------------------------------------------------
# Workflow Schedules (#969)
# ---------------------------------------------------------------------------


_ALLOWED_SCHEDULE_UPDATE_COLUMNS: frozenset[str] = frozenset(
    {
        "enabled",
        "cron_expr",
        "inputs_json",
        "target_kind",
        "target_ref",
        "missed_policy",
        "min_interval_seconds",
        "next_run_at",
        "last_run_at",
        "last_run_id",
        "advance_after_run_id",
        "claimed_by",
        "claimed_at",
        "updated_at",
    }
)

_MAX_INPUTS_SIZE = 65536


def _deserialize_schedule(d: dict[str, Any]) -> dict[str, Any]:
    raw_inputs = d.pop("inputs_json", None)
    d["inputs"] = json.loads(raw_inputs) if raw_inputs else None
    return d


def create_schedule(
    db: ThreadSafeConnection,
    *,
    workflow_ref: str,
    ref_type: str,
    cron_expr: str,
    target_ref: str,
    next_run_at: str,
    target_kind: str = "generic",
    inputs: dict[str, Any] | None = None,
    space_id: str | None = None,
    missed_policy: str = "skip",
    min_interval_seconds: int = 60,
) -> dict[str, Any]:
    """Create a new workflow schedule."""
    from .cron import parse_cron

    parse_cron(cron_expr)  # Validate expression

    if ref_type not in ("builtin", "package", "path"):
        raise ValueError(f"Invalid ref_type: {ref_type!r}")
    if missed_policy not in ("skip", "queue"):
        raise ValueError(f"Invalid missed_policy: {missed_policy!r}")
    if min_interval_seconds < 60:
        raise ValueError("min_interval_seconds must be >= 60")

    inputs_json = json.dumps(inputs) if inputs else "{}"
    if len(inputs_json.encode("utf-8")) > _MAX_INPUTS_SIZE:
        raise ValueError("inputs_json exceeds 64KB limit")

    sid = _uuid()
    now = _now()
    db.execute(
        "INSERT INTO workflow_schedules"
        " (id, workflow_ref, ref_type, cron_expr, inputs_json, target_kind, target_ref,"
        "  space_id, enabled, missed_policy, min_interval_seconds, next_run_at,"
        "  created_at, updated_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            sid,
            workflow_ref,
            ref_type,
            cron_expr,
            inputs_json,
            target_kind,
            target_ref,
            space_id,
            1,
            missed_policy,
            min_interval_seconds,
            next_run_at,
            now,
            now,
        ),
    )
    db.commit()
    return {
        "id": sid,
        "workflow_ref": workflow_ref,
        "ref_type": ref_type,
        "cron_expr": cron_expr,
        "inputs": inputs,
        "target_kind": target_kind,
        "target_ref": target_ref,
        "space_id": space_id,
        "enabled": 1,
        "missed_policy": missed_policy,
        "min_interval_seconds": min_interval_seconds,
        "next_run_at": next_run_at,
        "last_run_at": None,
        "last_run_id": None,
        "advance_after_run_id": None,
        "claimed_by": None,
        "claimed_at": None,
        "created_at": now,
        "updated_at": now,
    }


def get_schedule(db: ThreadSafeConnection, schedule_id: str) -> dict[str, Any] | None:
    row = db.execute_fetchone("SELECT * FROM workflow_schedules WHERE id = ?", (schedule_id,))
    if not row:
        return None
    return _deserialize_schedule(dict(row))


def list_schedules(
    db: ThreadSafeConnection,
    *,
    enabled_only: bool = False,
    limit: int = 50,
) -> list[dict[str, Any]]:
    conditions: list[str] = []
    params: list[Any] = []
    if enabled_only:
        conditions.append("enabled = 1")
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    params.append(limit)
    rows = db.execute_fetchall(
        f"SELECT * FROM workflow_schedules {where} ORDER BY next_run_at ASC LIMIT ?",
        tuple(params),
    )
    return [_deserialize_schedule(dict(r)) for r in rows]


def update_schedule(
    db: ThreadSafeConnection,
    schedule_id: str,
    **updates: Any,
) -> dict[str, Any] | None:
    if not updates:
        return get_schedule(db, schedule_id)
    updates["updated_at"] = _now()
    parts: list[str] = []
    params: list[Any] = []
    for col, val in updates.items():
        if col not in _ALLOWED_SCHEDULE_UPDATE_COLUMNS:
            raise ValueError(f"Column {col!r} not in allowed schedule update columns")
        parts.append(f"{col} = ?")
        params.append(val)
    params.append(schedule_id)
    db.execute(f"UPDATE workflow_schedules SET {', '.join(parts)} WHERE id = ?", tuple(params))
    db.commit()
    return get_schedule(db, schedule_id)


def delete_schedule(db: ThreadSafeConnection, schedule_id: str) -> bool:
    row = db.execute_fetchone("SELECT id FROM workflow_schedules WHERE id = ?", (schedule_id,))
    if not row:
        return False
    db.execute("DELETE FROM workflow_schedules WHERE id = ?", (schedule_id,))
    db.commit()
    return True


def claim_due_schedules(
    db: ThreadSafeConnection,
    worker_id: str,
    limit: int = 5,
    now: str | None = None,
) -> list[dict[str, Any]]:
    """Atomically claim due schedules for processing."""
    now_iso = now or _now()
    cursor = db.execute(
        "UPDATE workflow_schedules SET claimed_by = ?, claimed_at = ?"
        " WHERE id IN ("
        "   SELECT id FROM workflow_schedules"
        "   WHERE enabled = 1 AND next_run_at <= ?"
        "   AND claimed_by IS NULL AND advance_after_run_id IS NULL"
        "   ORDER BY next_run_at ASC LIMIT ?"
        " )",
        (worker_id, now_iso, now_iso, limit),
    )
    db.commit()
    if cursor.rowcount == 0:
        return []
    rows = db.execute_fetchall(
        "SELECT * FROM workflow_schedules WHERE claimed_by = ? AND claimed_at = ?",
        (worker_id, now_iso),
    )
    return [_deserialize_schedule(dict(r)) for r in rows]


def release_schedule_claim(db: ThreadSafeConnection, schedule_id: str) -> None:
    db.execute(
        "UPDATE workflow_schedules SET claimed_by = NULL, claimed_at = NULL, updated_at = ? WHERE id = ?",
        (_now(), schedule_id),
    )
    db.commit()


def advance_schedule(
    db: ThreadSafeConnection,
    schedule_id: str,
    *,
    next_run_at: str,
    last_run_at: str,
    last_run_id: str,
) -> None:
    """Advance a schedule to its next occurrence after a successful enqueue."""
    db.execute(
        "UPDATE workflow_schedules SET next_run_at = ?, last_run_at = ?, last_run_id = ?,"
        " advance_after_run_id = NULL, claimed_by = NULL, claimed_at = NULL, updated_at = ?"
        " WHERE id = ?",
        (next_run_at, last_run_at, last_run_id, _now(), schedule_id),
    )
    db.commit()


def set_advance_after_run(db: ThreadSafeConnection, schedule_id: str, run_id: str) -> None:
    """Set a schedule to wait for a specific run to complete before advancing (queue policy)."""
    db.execute(
        "UPDATE workflow_schedules SET advance_after_run_id = ?,"
        " claimed_by = NULL, claimed_at = NULL, updated_at = ? WHERE id = ?",
        (run_id, _now(), schedule_id),
    )
    db.commit()


def check_pending_advances(db: ThreadSafeConnection) -> list[dict[str, Any]]:
    """Find schedules waiting on a run that has reached terminal status."""
    rows = db.execute_fetchall(
        "SELECT s.* FROM workflow_schedules s"
        " JOIN workflow_runs r ON s.advance_after_run_id = r.id"
        " WHERE s.advance_after_run_id IS NOT NULL"
        " AND r.status IN ('completed', 'failed', 'cancelled', 'compensated', 'compensation_failed')"
        " LIMIT 20",
    )
    return [_deserialize_schedule(dict(r)) for r in rows]


def reset_stale_schedule_claims(
    db: ThreadSafeConnection,
    stale_threshold_seconds: int = 300,
) -> int:
    """Reset schedule claims older than threshold."""
    from datetime import timedelta

    cutoff = (datetime.now(timezone.utc) - timedelta(seconds=stale_threshold_seconds)).isoformat()
    cursor = db.execute(
        "UPDATE workflow_schedules SET claimed_by = NULL, claimed_at = NULL, updated_at = ?"
        " WHERE claimed_by IS NOT NULL AND claimed_at < ?",
        (_now(), cutoff),
    )
    db.commit()
    return cursor.rowcount
