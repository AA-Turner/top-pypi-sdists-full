"""Replay dropped ops from system_write_failure.

When a coordinator flush fails, the fallback writer captures every op
(table, op_type, primary_key, payload, depends_on) to system_write_failure
on a fresh connection. The data is intact — only the original
transaction failed.

This module reads back those rows, reconstructs :class:`WriteOp` instances,
groups them by ``request_id`` (so each replay attempt covers one request's
ops as a single transaction), and runs them through the same
:func:`matrx_ai.persistence.flush.execute_tiers` path that the live
coordinator uses. On successful replay, the row's ``recovered_at`` and
``recovery_op_id`` are stamped so the watchdog stops re-alerting.

Usage::

    from matrx_ai.persistence.replay import replay_pending

    report = await replay_pending(dry_run=False)
    print(report.recovered_count, report.still_failed_count)

The replay is conservative — only ops with the InterfaceError signature
(the gather-in-transaction bug fixed in this PR) are eligible by default.
Other failure modes likely indicate semantic bugs that need investigation
before blindly retrying.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from matrx_orm.session.dag import tier_ops
from matrx_orm.session.fallback import (
    DIRECT_WRITE_PRESERVED_MARKER,
    DISK_SPILL_RECOVERED_MARKER,
)
from matrx_orm.session.flush import execute_tiers
from matrx_orm.session.op import SessionOp, make_delete, make_insert, make_update
from matrx_utils import vcprint

from matrx_ai.persistence.registry import get_model

logger = logging.getLogger("matrx_ai.persistence.replay")


@dataclass(slots=True)
class ReplayReport:
    candidates: int = 0
    eligible: int = 0
    recovered_count: int = 0
    still_failed_count: int = 0
    quarantined_count: int = 0
    """Rows given up on this sweep — permanent failures, no longer retried/alerted."""
    skipped_count: int = 0
    by_request: dict[str, str] = field(default_factory=dict)
    """request_id → 'recovered' | 'failed' | 'skipped' (with reason)."""
    errors: list[str] = field(default_factory=list)


# Default eligibility filter — only retry the failure mode we know is now fixed.
DEFAULT_RETRY_ERRORS: tuple[str, ...] = (
    "InterfaceError: cannot perform operation: another operation is in progress",
)

# Error-CLASS signatures that are SELF-HEALING — a later sweep simply succeeds
# once the world catches up, with no code change and no human judgement needed:
#
#   * ForeignKeyViolationError — the op references a parent row that wasn't in
#     the DB yet at flush time (the canonical case: a sub-agent CHILD
#     conversation persisted by one request/Coordinator races ahead of the
#     PARENT conversation's fire-and-forget commit in another request — the
#     single-Session FK-DAG can't order across sessions). Once the parent lands,
#     the replay just works.
#   * InterfaceError (concurrent op on a shared connection) — a transient
#     asyncpg collision; the replay runs on a clean connection.
#
# Everything ELSE (check-constraint violations, schema drift, unique
# violations, NOT-NULL) is a genuine bug, NOT an ordering race — it must NOT be
# blindly auto-retried, because retrying can't fix it and would mask it. Those
# stay stuck for a human (the watchdog keeps alerting). This list is the
# precise boundary between "the platform self-heals" and "stop the line".
#   * DiskSpillRecovered — an op that was spilled to disk during a TOTAL DB
#     outage (record_failures couldn't even reach system_write_failure) and then
#     re-landed into the table by drain_spilled_ops once the DB returned. The
#     outage is definitionally self-healing, so the re-applied write just works.
#   * DirectWritePreserved — a DIRECT (non-Session) write of an already-paid-for
#     artifact that failed and had its payload preserved by
#     ``matrx_orm.create_or_capture``. The failures that kill such a write are
#     environmental (statement timeout, connection reset, pool exhaustion), so
#     re-applying it is exactly right; and the alternative — leaving it parked —
#     means a user is billed again for output we are already holding.
#   * commit hard-deadline — a Coordinator background flush exceeded its hard
#     database deadline. The full operation payload was durably captured after
#     the transaction was cancelled, so replay is the required completion of a
#     transient infrastructure failure, not a blind retry of ambiguous SQL.
RECOVERABLE_RETRY_ERRORS: tuple[str, ...] = (
    "ForeignKeyViolationError",
    "InterfaceError: cannot perform operation: another operation is in progress",
    DISK_SPILL_RECOVERED_MARKER,
    DIRECT_WRITE_PRESERVED_MARKER,
    "commit hard-deadline",
)

# Auto-replay loop cadence. A minute is plenty: the only thing it waits on is a
# parent row from a sibling request landing, which happens in seconds. A short
# interval keeps stuck-row dwell time (and the watchdog's CRITICAL window) low
# without hammering the DB.
DEFAULT_AUTO_REPLAY_INTERVAL_SECS: float = 60.0
DEFAULT_AUTO_REPLAY_LIMIT: int = 200

# Give-up boundary for SELF-HEALING failures. A cross-session FK-ordering race
# resolves within seconds (once the sibling request's parent row lands); a
# transient asyncpg collision clears on the very next clean-connection replay.
# A row that is STILL failing after this many auto-replay sweeps is therefore
# NOT a race — it is a PERMANENT orphan (e.g. a cx_tool_call whose parent
# cx_user_request was never created at all). Past this point the auto-replay
# loop stops re-fetching it AND the lifecycle watchdog stops alerting on it
# (both bound their attention by `retry_count < AUTO_REPLAY_MAX_ATTEMPTS`).
#
# The row is NOT marked recovered — `recovered_at` stays NULL because it was
# never actually written. It is simply quarantined: honestly visible to a
# human via `WHERE recovered_at IS NULL AND retry_count >= AUTO_REPLAY_MAX_ATTEMPTS`
# (the admin /persistence views), but no longer spamming the log every minute
# or holding the watchdog at CRITICAL forever.
#
# 5 sweeps × 60s = ~5 min, orders of magnitude beyond any real race window.
# IMPORTANT: aidream/db/watchdog_configs.py imports this constant to build the
# system_write_failure watchdog predicate — keep them in lockstep (single
# source of truth) by referencing this value, never hardcoding a copy.
AUTO_REPLAY_MAX_ATTEMPTS: int = 5

# A genuine cross-session FK race is resolved within seconds. Any recoverable
# failure already OLDER than this at sweep time is structurally permanent (the
# parent row is never coming), so it is quarantined on the FIRST failed sweep
# rather than burning the full attempt budget — this clears a startup backlog
# of stale orphans immediately instead of logging them ~5 times each first.
FK_RACE_MAX_AGE_SECONDS: float = 900.0


def _row_to_op(row: Any) -> SessionOp:
    """Reconstruct a SessionOp from a system_write_failure row.

    The row carries primary_key as a jsonb mapping ({column: value}) and
    depends_on as a jsonb list of [table, value] pairs (ignored — Session
    derives ordering from FK declarations). payload is jsonb.

    Resolves table_target → matrx-orm Model class via the persistence
    registry so the SessionOp carries the actual class, which is what
    the new tier_ops / execute_tiers expect.
    """
    payload_raw = row["payload"]
    payload = json.loads(payload_raw) if isinstance(payload_raw, str) else payload_raw

    pk_raw = row["primary_key"]
    pk_map = json.loads(pk_raw) if isinstance(pk_raw, str) else pk_raw
    pk_col, pk_val = next(iter(pk_map.items()))

    table = row["table_target"]
    try:
        model_cls = get_model(table)
    except KeyError:
        # The persistence registry only pre-registers Coordinator-owned tables.
        # A row captured by `matrx_orm.create_or_capture` can name ANY table
        # (its whole point is direct writes outside the Coordinator), so fall
        # back to the ORM's own (schema, table) → Model registry rather than
        # refusing to replay a preserved artifact.
        from matrx_orm.core.registry import get_model_by_table_name

        schema, _, table_name = table.partition(".")
        model_cls = get_model_by_table_name(schema, table_name)
    op_type = row["op_type"]

    if op_type == "insert":
        merged = dict(payload)
        merged.setdefault(pk_col, str(pk_val))
        return make_insert(model_cls, merged, pk_value=str(pk_val))
    if op_type == "update":
        return make_update(model_cls, str(pk_val), dict(payload))
    if op_type == "delete":
        return make_delete(model_cls, str(pk_val))
    raise ValueError(f"Unknown op_type {op_type!r} in system_write_failure row")


def _payload_dict(row: Any) -> dict[str, Any]:
    payload_raw = row["payload"]
    payload = json.loads(payload_raw) if isinstance(payload_raw, str) else payload_raw
    return dict(payload or {})


async def _upgrade_legacy_chat_payloads(rows: Sequence[Any]) -> list[dict[str, Any]]:
    """Restore attribution omitted by pre-org-schema chat write payloads.

    Failure rows are durable artifacts and may outlive the schema version that
    created them. The 2026 chat schema moved ownership from ``user_id`` to
    ``created_by`` and made ``organization_id`` mandatory. A preserved
    ``chat.user_request`` can therefore carry its old actor but not the current
    columns, while its sibling ``chat.request`` identifies the authoritative
    conversation. Rebuild both rows from those preserved relationships before
    replaying them through today's models.

    This stays inside matrx-ai: chat relations belong to the package, and all
    lookups go through its injected matrx-orm models. No aidream host import or
    privileged database path is needed.
    """
    upgraded = [dict(row) for row in rows]
    for row in upgraded:
        row["payload"] = _payload_dict(row)

    request_rows = [row for row in upgraded if row["table_target"] == "chat.request"]
    snapshot_rows = [
        row for row in upgraded if row["table_target"] == "chat.request_snapshot"
    ]
    user_request_rows = {
        str(row["primary_key"].get("id")): row
        for row in upgraded
        if row["table_target"] == "chat.user_request"
        and isinstance(row.get("primary_key"), dict)
        and row["primary_key"].get("id")
    }
    if not request_rows and not user_request_rows and not snapshot_rows:
        return upgraded

    conversation_attribution: dict[str, dict[str, Any]] = {}
    for row in upgraded:
        if row["table_target"] != "chat.conversation":
            continue
        payload = row["payload"]
        conversation_id = payload.get("id")
        if conversation_id:
            conversation_attribution[str(conversation_id)] = {
                "organization_id": payload.get("organization_id"),
                "created_by": payload.get("created_by"),
            }

    conversation_ids = {
        str(row["payload"]["conversation_id"])
        for row in [*request_rows, *snapshot_rows]
        if row["payload"].get("conversation_id")
    }
    missing_ids = conversation_ids - conversation_attribution.keys()
    if missing_ids:
        Conversation = get_model("chat.conversation")
        for conversation_id in sorted(missing_ids):
            found = await Conversation.filter(id=conversation_id).values(
                "organization_id", "created_by"
            )
            if found:
                conversation_attribution[conversation_id] = dict(found[0])

    conversation_by_user_request: dict[str, str] = {}
    for row in request_rows:
        payload = row["payload"]
        user_request_id = payload.get("user_request_id")
        conversation_id = payload.get("conversation_id")
        if user_request_id and conversation_id:
            conversation_by_user_request[str(user_request_id)] = str(conversation_id)

    user_request_attribution: dict[str, dict[str, Any]] = {}
    for user_request_id, row in user_request_rows.items():
        payload = row["payload"]
        conversation_id = conversation_by_user_request.get(user_request_id)
        conversation = conversation_attribution.get(conversation_id or "", {})
        owner_id = (
            payload.get("created_by")
            or payload.get("user_id")
            or row.get("created_by")
            or row.get("user_id")
            or conversation.get("created_by")
        )
        organization_id = (
            payload.get("organization_id")
            or conversation.get("organization_id")
            or row.get("organization_id")
        )
        if owner_id:
            payload.setdefault("created_by", owner_id)
        if organization_id:
            payload.setdefault("organization_id", organization_id)
        user_request_attribution[user_request_id] = {
            "created_by": owner_id,
            "organization_id": organization_id,
        }

    for row in request_rows:
        payload = row["payload"]
        user_request = user_request_attribution.get(str(payload.get("user_request_id") or ""), {})
        conversation = conversation_attribution.get(str(payload.get("conversation_id") or ""), {})
        owner_id = (
            payload.get("created_by")
            or user_request.get("created_by")
            or row.get("created_by")
            or row.get("user_id")
            or conversation.get("created_by")
        )
        organization_id = (
            payload.get("organization_id")
            or conversation.get("organization_id")
            or user_request.get("organization_id")
            or row.get("organization_id")
        )
        if owner_id:
            payload.setdefault("created_by", owner_id)
        if organization_id:
            payload.setdefault("organization_id", organization_id)

    for row in snapshot_rows:
        payload = row["payload"]
        conversation = conversation_attribution.get(
            str(payload.get("conversation_id") or ""), {}
        )
        organization_id = (
            payload.get("organization_id")
            or conversation.get("organization_id")
            or row.get("organization_id")
        )
        if organization_id:
            payload.setdefault("organization_id", organization_id)

    return upgraded


async def _op_already_satisfied(op: SessionOp) -> bool:
    """Return whether an idempotent replay op already has its final state.

    An INSERT whose primary-key row exists already landed, even if the process
    died before marking its failure artifact recovered. A DELETE whose row is
    absent is likewise complete. Updates remain strict because absence cannot
    satisfy an update intent.
    """
    if op.op_type not in {"insert", "delete"}:
        return False
    meta = getattr(op.model_cls, "_meta", None)
    primary_keys = tuple(getattr(meta, "primary_keys", ()) or (op.pk_field,))
    if len(primary_keys) == 1:
        primary_key = primary_keys[0]
        primary_value = op.payload.get(primary_key, op.pk_value)
        filters = {primary_key: primary_value} if primary_value is not None else {}
    else:
        filters = {
            primary_key: op.payload.get(primary_key)
            for primary_key in primary_keys
            if op.payload.get(primary_key) is not None
        }
    if len(filters) != len(primary_keys):
        return False
    exists = await op.model_cls.exists(**filters)
    return exists if op.op_type == "insert" else not exists


def _swf_model() -> Any:
    from matrx_ai.db._registry import get_model as get_db_model

    return get_db_model("SystemWriteFailure")


async def _fetch_pending(
    *,
    retry_errors: Sequence[str] | None,
    limit: int,
    max_attempts: int | None = None,
    ids: Sequence[str] | None = None,
) -> list[Any]:
    """Fetch unrecovered failure rows, optionally filtered by error_text.

    Two-stage fetch:
      1. SELECT id+error_text only (small, fast) for ALL unrecovered rows.
         Filter by error_text in Python.
      2. SELECT the full payload columns ONLY for the eligible ids, in
         small batches. Avoids Supavisor's prepared-statement caching
         quirks on large multi-row SELECTs (which timed out in testing).

    ``max_attempts`` (when set) excludes rows that have already been retried
    that many times — the auto-replay loop's give-up boundary, so a permanent
    orphan is fetched at most ``max_attempts`` times and then left alone.

    ``ids`` (when set) restricts the sweep to exactly those failure rows — the
    per-row admin "Replay" button. Without it, a single-row retry has to be
    expressed as an error_text filter, which fans out to every unrelated row
    sharing that message.
    """
    Swf = _swf_model()
    id_qb = Swf.filter(recovered_at__isnull=True)
    if ids is not None:
        if not ids:
            return []
        id_qb = id_qb.filter(id__in=list(ids))
    if max_attempts is not None:
        id_qb = id_qb.filter(retry_count__lt=int(max_attempts))
    id_rows = await id_qb.order_by("failed_at").limit(int(limit)).values("id", "error_text")
    if retry_errors is not None:
        # SUBSTRING match, not exact. A failure's error_text carries variable
        # per-row detail (e.g. a FK violation embeds the specific key/UUID), so
        # eligibility is keyed off an error-CLASS signature appearing anywhere
        # in the text. Exact-match would never catch the FK-ordering class.
        signatures = tuple(retry_errors)
        eligible_ids = [
            r["id"]
            for r in id_rows
            if r["error_text"] and any(sig in r["error_text"] for sig in signatures)
        ]
    else:
        eligible_ids = [r["id"] for r in id_rows]
    if not eligible_ids:
        return []

    # Stage 2: per-id fetch (one round-trip per row keeps each query tiny
    # and avoids the array-binding Supavisor hiccup).
    out: list[Any] = []
    for row_id in eligible_ids:
        full_rows = await Swf.filter(id=row_id).values(
            "id",
            "op_id",
            "request_id",
            "table_target",
            "op_type",
            "primary_key",
            "payload",
            "depends_on",
            "error_text",
            "retry_count",
            "failed_at",
            "user_id",
            "conversation_id",
            "organization_id",
            "created_by",
        )
        if full_rows:
            out.append(full_rows[0])
    return out


async def _mark_recovered(ids: Sequence[str], recovery_op_id: str) -> None:
    if not ids:
        return
    from datetime import UTC, datetime

    await _swf_model().update_where(
        {"id__in": list(ids)},
        recovered_at=datetime.now(UTC),
        recovery_op_id=recovery_op_id,
    )


async def _record_failed_attempt(rows: Sequence[Any], *, max_attempts: int | None) -> int:
    """Account for a failed replay of ``rows``: increment each row's
    ``retry_count``, and quarantine (jump ``retry_count`` to the cap) any row
    that has now exhausted its attempt budget or aged past the FK-race window.

    Returns the number of rows quarantined this call. When ``max_attempts`` is
    None (e.g. a manual/admin force-replay) rows are only incremented, never
    quarantined — a human asked for the retry, so don't silently give up.

    The quarantine signal is ``retry_count`` itself (NOT ``recovered_at``): the
    row was never written, so it stays honestly unrecovered, but both the
    auto-replay loop and the lifecycle watchdog bound their attention by
    ``retry_count < AUTO_REPLAY_MAX_ATTEMPTS``.
    """
    if not rows:
        return 0
    from datetime import UTC, datetime

    now = datetime.now(UTC)
    bump_ids: list[str] = []
    giveup_ids: list[str] = []
    for r in rows:
        retry_count = r["retry_count"] or 0
        failed_at = r["failed_at"]
        age = (now - failed_at).total_seconds() if failed_at else 0.0
        if max_attempts is not None and (
            retry_count + 1 >= max_attempts or age > FK_RACE_MAX_AGE_SECONDS
        ):
            giveup_ids.append(r["id"])
        else:
            bump_ids.append(r["id"])

    from matrx_orm import F

    Swf = _swf_model()
    if bump_ids:
        # atomic column-relative increment — F() renders retry_count = retry_count + 1
        await Swf.filter(id__in=bump_ids).update(retry_count=F("retry_count") + 1)
    if giveup_ids and max_attempts is not None:
        await Swf.update_where({"id__in": giveup_ids}, retry_count=int(max_attempts))
    return len(giveup_ids)


async def _capture_replay_failure(
    exc: Exception,
    *,
    request_id: str,
    rows: Sequence[Any],
    phase: str,
) -> None:
    """Capture a replay failure at the boundary that intentionally absorbs it."""
    try:
        from matrx_connect.streaming.error_capture import capture_error

        first = rows[0] if rows else {}
        await capture_error(
            exc,
            kind="persistence_replay_failed",
            route="matrx_ai.persistence.replay.replay_pending",
            error_type=type(exc).__name__,
            request_id=None if request_id == "_orphan" else request_id,
            user_id=first.get("user_id"),
            conversation_id=first.get("conversation_id"),
            context={
                "phase": phase,
                "failure_row_ids": [str(row["id"]) for row in rows],
                "table_targets": sorted({str(row["table_target"]) for row in rows}),
            },
        )
    except Exception:
        # The preserved system_write_failure rows remain authoritative. Error
        # capture is a safety-net signal and cannot block later replay groups.
        logger.exception("persistence_replay_error_capture_failed")


async def replay_pending(
    *,
    dry_run: bool = True,
    retry_errors: Sequence[str] | None = DEFAULT_RETRY_ERRORS,
    limit: int = 500,
    database: str | None = None,
    max_attempts: int | None = None,
    ids: Sequence[str] | None = None,
) -> ReplayReport:
    """Read pending failures and try to land them.

    ``retry_errors=None`` skips error-class filtering — replays every
    unrecovered row regardless of cause. Use sparingly; the default
    restricts to the bug class fixed by the flush-sequentialization PR.

    ``ids`` restricts the sweep to those exact failure rows (the admin
    per-row Replay). It composes with ``retry_errors``; pass
    ``retry_errors=None`` alongside it to retry a specific row whatever
    its error class.

    Each ``request_id`` group is replayed as one transaction. If that
    transaction succeeds, every contributing failure row is marked
    ``recovered_at``. If it fails, the rows stay unrecovered and the
    new failure is captured by the same fallback path (which would
    re-fire the watchdog with a different error_text, surfacing it).
    """
    from matrx_orm import transaction
    from matrx_orm.core.config import get_all_database_project_names

    # Ensure every cx_ table has a Model bound in the persistence registry.
    # In a live request this happens inside get_coordinator() on first queue;
    # replay bypasses that path and needs explicit registration.
    from matrx_ai.persistence.queue_helpers import _ensure_cx_registered

    _ensure_cx_registered()

    if database is None:
        names = get_all_database_project_names()
        database = names[0] if names else "matrx"

    report = ReplayReport()

    # Phase 1: SELECT candidate failures.
    rows = await _fetch_pending(
        retry_errors=retry_errors, limit=limit, max_attempts=max_attempts, ids=ids
    )

    report.candidates = len(rows)
    report.eligible = len(rows)
    if not rows:
        return report

    # Group by request_id; rows without a request_id form one synthetic
    # "_orphan" group so they still get replayed.
    by_request: dict[str, list[Any]] = {}
    for r in rows:
        key = r["request_id"] or "_orphan"
        by_request.setdefault(key, []).append(r)

    vcprint(
        f"[Replay] {len(rows)} eligible op(s) across {len(by_request)} request(s)"
        + (" (DRY RUN)" if dry_run else ""),
        color="cyan",
    )

    # Phase 2: per-request replay. Each request gets its own transaction so
    # one bad request can't poison the others.
    for request_id, group_rows in by_request.items():
        try:
            group_rows = await _upgrade_legacy_chat_payloads(group_rows)
            ops = [_row_to_op(r) for r in group_rows]
            pending_ops = [op for op in ops if not await _op_already_satisfied(op)]
        except Exception as exc:
            report.still_failed_count += len(group_rows)
            report.by_request[request_id] = f"failed: replay preparation: {exc}"
            report.errors.append(f"{request_id}: prepare {exc}")
            await _capture_replay_failure(
                exc, request_id=request_id, rows=group_rows, phase="prepare"
            )
            continue

        try:
            tiers = tier_ops(pending_ops)
        except Exception as exc:
            report.still_failed_count += len(group_rows)
            report.by_request[request_id] = f"failed: DAG: {exc}"
            report.errors.append(f"{request_id}: dag {exc}")
            await _capture_replay_failure(
                exc, request_id=request_id, rows=group_rows, phase="dag"
            )
            continue

        if dry_run:
            report.recovered_count += len(group_rows)
            report.by_request[request_id] = "would-recover"
            continue

        recovery_op_id = str(uuid4())
        try:
            if pending_ops:
                async with transaction(database) if database else transaction():
                    await execute_tiers(tiers)
            # Mark the rows recovered outside the replay transaction so we
            # don't block the replay path.
            await _mark_recovered([r["id"] for r in group_rows], recovery_op_id)
            report.recovered_count += len(group_rows)
            report.by_request[request_id] = "recovered"
            vcprint(
                f"[Replay] recovered {len(group_rows)} op(s) for request {request_id} "
                f"(recovery_op_id={recovery_op_id})",
                color="green",
            )
        except Exception as exc:
            report.still_failed_count += len(group_rows)
            report.by_request[request_id] = f"failed: {type(exc).__name__}: {exc}"
            report.errors.append(f"{request_id}: {type(exc).__name__}: {exc}")
            vcprint(
                f"[Replay] FAILED for request {request_id}: {type(exc).__name__}: {exc}",
                color="red",
            )
            await _capture_replay_failure(
                exc, request_id=request_id, rows=group_rows, phase="execute"
            )
            # Record the failed attempt so a permanent orphan stops being
            # retried forever (and the watchdog stops alerting on it). No-op
            # accounting for dry runs.
            if not dry_run:
                try:
                    gave_up = await _record_failed_attempt(group_rows, max_attempts=max_attempts)
                    report.quarantined_count += gave_up
                    if gave_up:
                        report.by_request[request_id] = (
                            f"quarantined (permanent): {type(exc).__name__}"
                        )
                except Exception as bump_exc:  # noqa: BLE001 — accounting must never crash the sweep
                    vcprint(
                        f"[Replay] failed to record attempt for request "
                        f"{request_id}: {type(bump_exc).__name__}: {bump_exc}",
                        color="red",
                    )

    return report


async def run_auto_replay_loop(
    *,
    interval_secs: float = DEFAULT_AUTO_REPLAY_INTERVAL_SECS,
    limit: int = DEFAULT_AUTO_REPLAY_LIMIT,
    retry_errors: Sequence[str] | None = RECOVERABLE_RETRY_ERRORS,
    database: str | None = None,
    max_attempts: int = AUTO_REPLAY_MAX_ATTEMPTS,
) -> None:
    """Periodically self-heal SELF-HEALING write failures from
    ``system_write_failure`` so the app never has to think about cross-session
    write ordering.

    This is the recovery counterpart to the lifecycle watchdog: the watchdog
    *detects + alerts* on stuck rows; this loop *fixes* the subset that is
    structurally recoverable (FK-ordering races, transient asyncpg collisions).
    A row only survives a sweep if it is a genuine bug the platform should NOT
    silently paper over — that's exactly when a human should look.

    Cancel the task to stop. The outer guard keeps the loop alive across any
    transient failure (sleep, retry); only cancellation stops it.
    """
    import asyncio

    vcprint(
        f"[Replay] Auto-replay loop started (every {interval_secs:.0f}s, "
        f"batch {limit}, classes={len(retry_errors or ())}, "
        f"give-up after {max_attempts} attempts)",
        color="green",
    )
    while True:
        try:
            # Disk-spill drain runs FIRST each tick: re-land any ops that were
            # spilled to disk during a total DB outage (record_failures couldn't
            # even reach system_write_failure) back INTO system_write_failure, so
            # the replay below then re-applies them to the real tables. The first
            # tick (at boot) is the "startup drain"; every tick after is the
            # periodic watcher — one wiring point covers both. Best-effort.
            try:
                from matrx_orm import drain_spilled_ops

                await drain_spilled_ops(database=database)
            except Exception as drain_exc:  # noqa: BLE001 — never kill the loop
                vcprint(
                    f"[Replay] disk-spill drain raised {type(drain_exc).__name__}: "
                    f"{drain_exc} — continuing",
                    color="yellow",
                )

            report = await replay_pending(
                dry_run=False,
                retry_errors=retry_errors,
                limit=limit,
                database=database,
                max_attempts=max_attempts,
            )
            if report.recovered_count or report.still_failed_count:
                msg = (
                    f"[Replay] Auto-replay swept {report.candidates} eligible op(s): "
                    f"{report.recovered_count} recovered, "
                    f"{report.still_failed_count} still failed"
                )
                if report.quarantined_count:
                    msg += (
                        f", {report.quarantined_count} given up as PERMANENT "
                        f"(no longer retried/alerted — inspect via /admin persistence)"
                    )
                vcprint(
                    msg,
                    color="green" if not report.still_failed_count else "yellow",
                )
        except asyncio.CancelledError:
            vcprint("[Replay] Auto-replay loop stopping", color="green")
            raise
        except Exception as exc:  # noqa: BLE001 — loop must never die on a tick
            vcprint(
                f"[Replay] Auto-replay tick raised {type(exc).__name__}: {exc} "
                f"— continuing after interval",
                color="red",
            )
            logger.exception("auto_replay_tick_failed")
        try:
            await asyncio.sleep(interval_secs)
        except asyncio.CancelledError:
            vcprint("[Replay] Auto-replay loop stopping", color="green")
            raise
