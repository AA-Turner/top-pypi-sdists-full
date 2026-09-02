"""Coordinator — the per-request façade over ``matrx_orm.Session``.

This module is what `queue_helpers` (and any legacy call site that imports
``WriteCoordinator``) reaches when persistence needs to be wired into the
request lane. The implementation delegates entirely to
:class:`matrx_orm.Session` — coalescing, FK-inferred DAG ordering,
transactional flush, fresh-connection fallback to
``system_write_failure`` — and only translates the matrx-orm Session's
FlushReport into the matrx-ai shape that the lane finalizer and
operator-facing observers consume.

This file replaced the legacy ``WriteCoordinator`` and
``SessionCoordinator`` modules in May 2026 (Phase G). The legacy
WriteCoordinator (its own coalesce/dag/flush/fallback) is deleted.
``WriteCoordinator`` remains as a back-compat alias for one PR cycle so
nothing breaks during the rollout window; new code uses ``Coordinator``.

Public API:

    coord = Coordinator(database=..., request_id=..., user_id=...,
                        conversation_id=...)
    op_id = coord.queue(table, payload, op_type=..., primary_key=...)
    report = await coord.flush(reason="stream_end")
    coord.phase     # CoordinatorPhase
    coord.report    # FlushReport
    coord.ops_count

``depends_on`` is accepted for back-compat but **ignored** — Session
derives ordering from each Model's declared FK fields.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Literal

from matrx_utils import vcprint

from matrx_ai.persistence.postgres_text import sanitize_postgres_text
from matrx_ai.persistence.registry import get_model

logger = logging.getLogger("matrx_ai.persistence.coordinator")

# Literal type for diagnostic strings carried on FlushReport. Not enforced
# at runtime; useful for type-checkers and operator log scans.
FlushReason = Literal["stream_end", "error", "cancelled", "manual"]


def _scream_lost_write(
    table: str,
    op_type: str,
    primary_key: tuple[str, str] | None,
    reason: str,
    request_id: str | None,
    conversation_id: str | None,
) -> None:
    """Loud, self-documenting alarm when the Coordinator could not queue a write.

    A future agent who pastes the resulting error into a chat must get the STORY,
    not a context-free symptom they will paper over. Lands on stdout (red) AND in
    public.app_log via the root logging handler.
    """
    pk = primary_key[1] if primary_key else "?"
    banner = "\n".join([
        "",
        "████████████████████████████████████████████████████████████████████████████",
        "██  COORDINATOR COULD NOT QUEUE A WRITE — CAPTURED FOR REPLAY — NOT NORMAL ██",
        "████████████████████████████████████████████████████████████████████████████",
        "WHO I AM      : matrx_ai.persistence.Coordinator (the per-request write path).",
        f"WHAT HAPPENED : a {op_type} on {table} (pk={pk}) could NOT be queued onto the",
        f"                request's Session. reason: {reason}",
        "WHAT I DID    : captured the op to public.system_write_failure on a FRESH",
        "                connection so the write is NOT lost and can be replayed.",
        "WHAT'S WRONG  : a write reaching a non-OPEN coordinator means either an earlier",
        "                commit barrier already failed, OR a LATE write arrived after the",
        "                request sealed — classically a sub-agent-spawning tool's",
        "                completion write landing after the fork/join finalize.",
        "WHERE TO LOOK : persistence/queue_helpers.py (fork/join finalize),",
        "                tools/executor.py::_persist_tool_outcome (tool completion write),",
        "                and this request's earlier PersistenceBarrierError, if any.",
        "DO NOT        : 'handle' or suppress this downstream. The data is safe in",
        "                system_write_failure — REPLAY it: scripts/replay_write_failures.py",
        f"CONTEXT       : request_id={request_id} conversation_id={conversation_id}",
        "████████████████████████████████████████████████████████████████████████████",
        "",
    ])
    vcprint(banner, color="red")
    logger.error(
        "coordinator_dropped_write table=%s op_type=%s reason=%s pk=%s — captured to "
        "system_write_failure for replay (NOT lost). See banner for where to look.",
        table,
        op_type,
        reason,
        pk,
        extra={
            "event": "coordinator_dropped_write",
            "table": table,
            "op_type": op_type,
            "reason": reason,
            "request_id": request_id,
            "conversation_id": conversation_id,
        },
    )


class CoordinatorPhase(Enum):
    OPEN = "open"
    FLUSHING = "flushing"
    FLUSHED = "flushed"
    ERRORED = "errored"


@dataclass(slots=True)
class FlushReport:
    """Diagnostic snapshot returned by ``Coordinator.flush()``.

    Same shape as the legacy WriteCoordinator FlushReport — preserved so
    operator observers (lane finalizers, telemetry, the dashboard) read
    the same fields they always did.
    """

    reason: FlushReason
    ops_queued: int = 0
    ops_after_coalesce: int = 0
    tiers: int = 0
    ops_written: int = 0
    ops_lost: int = 0
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error: str | None = None
    by_table: dict[str, int] = field(default_factory=dict)
    tier_summary: list[dict[str, int]] = field(default_factory=list)

    @property
    def duration_secs(self) -> float | None:
        if self.started_at is None or self.finished_at is None:
            return None
        return (self.finished_at - self.started_at).total_seconds()


# OpType is a string literal carrier in this layer — Session has its own
# OpType. The matrx-ai surface deliberately uses strings so callers don't
# need to import the Session type.
OpType = Literal["insert", "update", "delete"]


class PersistenceBarrierError(Exception):
    """A per-turn commit barrier failed — the request MUST stop.

    Raised by :meth:`Coordinator.finalize` when a turn's writes did not
    durably commit (flush error) or had to be dropped. This is a
    STOP-EVERYTHING signal, per the persistence contract in CLAUDE.md:
    a finalized write is never optional and never swallowed. Do NOT
    catch-and-continue — let it propagate to the streaming handler, which
    surfaces ``fatal_error`` to the client and records ``system_error``.
    The dropped/uncommitted ops are in ``system_write_failure`` for replay.
    """

    def __init__(
        self,
        *,
        reason: str,
        report: FlushReport,
        conversation_id: str | None = None,
        request_id: str | None = None,
    ) -> None:
        self.reason = reason
        self.report = report
        self.conversation_id = conversation_id
        self.request_id = request_id
        message = (
            f"Persistence commit barrier '{reason}' failed "
            f"(error={report.error!r}, ops_lost={report.ops_lost}, "
            f"conversation={conversation_id}, request={request_id}). "
            f"Request stopped to avoid silent data loss."
        )
        super().__init__(message)

        # The generic streaming boundary understands exceptions carrying
        # ``error_info``. Classify this infrastructure failure here, at its
        # source, so the client never mislabels it as a prompt/settings error.
        from matrx_ai.providers.errors import RetryableError

        self.error_info = RetryableError(
            error_type="persistence_commit_failed",
            message=message,
            is_retryable=False,
            user_message=(
                "The request stopped because some conversation records could not "
                "be saved safely. This is an internal data-saving error, not a "
                "problem with your prompt or settings. Please try again shortly."
            ),
            details={
                "barrier": reason,
                "operations_lost": report.ops_lost,
                "conversation_id": conversation_id,
                "request_id": request_id,
                "tables": dict(report.by_table),
            },
        )


# Bounded waits — the fast path never blocks, but the accountability check and
# the degrade/panic drain are bounded so a stuck DB surfaces as a loud failure
# instead of an indefinite hang (the exact failure mode of the 2026-05-23 incident).
_COMMIT_GRACE_SECONDS: float = 30.0  # how long check_pending waits on an overdue commit
_DRAIN_TIMEOUT_SECONDS: float = 30.0  # how long a sync/panic drain waits per in-flight commit

# A fired background commit must release its pool connection at a KNOWN bound,
# even when the DB is wedged (lock wait, saturated write queue, black-holed
# socket). Without this, orphaned overdue commits accumulate and exhaust the
# connection pool → service-wide hang (the 2026-05-23 class, at the service
# level). On expiry the commit's ops are captured to system_write_failure on a
# fresh connection, so the deadline bounds the connection hold without losing data.
_COMMIT_HARD_DEADLINE_SECONDS: float = 60.0

# Process-wide cap on fired-but-unfinished background commits. Beyond this we
# apply BACKPRESSURE: refuse to fire (blow up the request) rather than pile up
# commits and starve the pool. "Data first": stop the request loudly rather than
# wedge the whole service.
#
# Headroom math: each stalled commit can transiently need TWO pool connections
# (the flush's own, plus a fresh one for record_failures on the hard-deadline
# path). The asyncpg pool default is pool_max=30 (matrx_orm config). So the cap
# must satisfy 2*cap + (foreground reads) < pool_max. 8 → ≤16 for stalled
# commits, leaving ≥14 for everything else. Keep it well under pool_max/2.
_MAX_INFLIGHT_COMMITS: int = 8
_inflight_commits: int = 0  # process-wide count of fired-but-unfinished bg commits

# How long a barrier WAITS for a free commit slot before declaring the DB stuck.
#
# Saturation of the cap is NOT by itself evidence of a sick DB. One workflow
# super-step legitimately runs N parallel agent invocations (a Masterwork fans
# one auditor per Rulebook section per drafted variant — 25 concurrent agent
# runs is a normal shape), and each is its own Coordinator firing its own
# per-turn commit. Those commits are millisecond-scale; the cap is a POOL-
# CONNECTION budget, not a health signal. Failing a request the instant a 9th
# HEALTHY commit wants to fire is a timing coincidence dressed up as a
# durability incident (production run 6266cb1b-f7f9-44f7-a951-15da231de9ef: 22
# of 25 auditor invocations committed fine in the same second the other 3 were
# refused with "DB not draining").
#
# So the barrier WAITS for a slot — that is what backpressure means — and only
# fails when the wait expires, which is the honest "commits are not draining"
# condition. Nothing is ever committed unconfirmed and the accountability
# barrier (check_pending) is untouched; the wait is bounded, so a genuinely
# wedged DB still stops the request loudly.
_COMMIT_SLOT_WAIT_SECONDS: float = 30.0
_COMMIT_SLOT_POLL_SECONDS: float = 0.01


def _try_reserve_commit_slot() -> bool:
    """Reserve one process-wide background-commit slot, or return False.

    Sync (no await) so check + increment is atomic w.r.t. other coroutines —
    two waiters can never both claim the last free slot. The reservation is
    released by ``_release_commit_slot`` (the commit never fired) or by
    ``_on_commit_done`` (the commit finished)."""
    global _inflight_commits
    if _inflight_commits >= _MAX_INFLIGHT_COMMITS:
        return False
    _inflight_commits += 1
    return True


def _release_commit_slot() -> None:
    """Give back a reserved slot that never became a fired commit."""
    global _inflight_commits
    _inflight_commits = max(0, _inflight_commits - 1)


@dataclass(slots=True)
class _PendingCommit:
    """A fired-but-not-yet-verified background commit (one turn's flush)."""

    task: asyncio.Task[Any]
    reason: str
    fired_at: float
    ops: int


class Coordinator:
    """WriteCoordinator-shaped façade over ``matrx_orm.Session``.

    One Coordinator per request. The lane finalizer fires
    :meth:`flush` on every exit path (stream_end / error / cancelled).
    The coordinator wraps a single matrx-orm Session that does the
    actual coalesce / DAG / transactional commit / fallback work.
    """

    __slots__ = (
        "_session",
        "_phase",
        "_report",
        "_lock",
        "_database",
        "_request_id",
        "_user_id",
        "_conversation_id",
        "_dropped_ops_count",
        "_pending_commits",
        "_slot_reserved",
        "_late_one_shot_tail",
        "_late_boundary_captured",
    )

    def __init__(
        self,
        *,
        database: str | None = None,
        request_id: str | None = None,
        user_id: str | None = None,
        conversation_id: str | None = None,
        late_write_only: bool = False,
    ) -> None:
        # Lazy import keeps matrx_ai.persistence importable when matrx-orm
        # isn't present (e.g. minimal install).
        from matrx_orm.session.managed import _coordinator_session
        from matrx_orm.session.session import _session_stack

        self._session: Any = _coordinator_session(database=database)
        # A coordinator first discovered after its RequestLane began draining
        # has no future finalizer.  Start it terminal so every queued operation
        # takes the existing fresh-Session one-shot path instead of entering an
        # OPEN Session that nothing can ever flush.
        self._phase: CoordinatorPhase = (
            CoordinatorPhase.FLUSHED if late_write_only else CoordinatorPhase.OPEN
        )
        self._report: FlushReport | None = None
        self._lock = asyncio.Lock()
        self._database = database
        self._request_id = request_id
        self._user_id = user_id
        self._conversation_id = conversation_id
        self._late_boundary_captured = False
        # Tracks queue-call drops (no model_cls available, etc.) that bypass
        # the Session entirely. Surfaces in FlushReport.ops_lost.
        self._dropped_ops_count = 0

        # Fire-and-forget commits in flight. commit_async() fires a turn's flush
        # as a background task (own connection) and records it here; the next
        # turn's check_pending() verifies it landed. See the persistence
        # contract in CLAUDE.md (fire-and-forget + accountability).
        self._pending_commits: list[_PendingCommit] = []
        # Late writes can carry FK ordering just like the main Session (for
        # example message INSERT -> tool_call.message_id UPDATE).  One-shot
        # Sessions must therefore execute in queue order rather than racing as
        # unrelated detached tasks.
        self._late_one_shot_tail: asyncio.Task[Any] | None = None

        # True while this Coordinator holds a background-commit slot reserved by
        # ``acquire_commit_slot`` at a barrier and not yet consumed by
        # ``commit_async``.
        self._slot_reserved = False

        # Push the wrapped Session onto matrx-orm's _session_stack so that
        # managed Model writes (``await CxConversation.create(...)``) reach
        # the SAME Session as queue_helpers. Before this push, queue_helpers
        # and direct Model.create() were two parallel paths that didn't
        # share a destination — direct Model.create would auto-elevate
        # per-call instead of batching.
        #
        # We never reset the token: the Coordinator is bound to the request
        # task's lifetime. When the task ends, the ContextVar Context is
        # discarded and the push is reclaimed automatically. After flush,
        # the Session's phase becomes FLUSHED; managed.py's wrapper walks
        # the stack and skips non-OPEN Sessions, so post-flush writes
        # correctly auto-elevate.
        current_stack = _session_stack.get()
        _session_stack.set(current_stack + (self._session,))

    # ---------------------- properties / introspection -------------------

    @property
    def phase(self) -> CoordinatorPhase:
        return self._phase

    @property
    def ops_count(self) -> int:
        return self._session.ops_count

    @property
    def report(self) -> FlushReport | None:
        return self._report

    def set_correlation(
        self,
        *,
        request_id: str | None = None,
        user_id: str | None = None,
        conversation_id: str | None = None,
    ) -> None:
        if request_id is not None:
            self._request_id = request_id
        if user_id is not None:
            self._user_id = user_id
        if conversation_id is not None:
            self._conversation_id = conversation_id

    # ---------------------- queue ---------------------------------------

    def queue(
        self,
        table: str,
        payload: dict[str, Any],
        *,
        op_type: OpType = "insert",
        primary_key: tuple[str, str] | None = None,
        depends_on: Sequence[tuple[str, str]] = (),
    ) -> str:
        """Translate (table, payload) → SessionOp on the wrapped Session.

        ``depends_on`` is accepted for back-compat and ignored — Session
        derives dependencies from each Model's declared FK fields.
        """
        sanitization = sanitize_postgres_text(payload)
        if sanitization.replacements:
            payload = sanitization.value
            vcprint(
                f"[Coordinator] Backstop replaced {sanitization.replacements} "
                f"PostgreSQL-invalid NUL byte(s) on {op_type} {table}; paths="
                f"{list(sanitization.paths)}.",
                color="red",
            )
            self._capture_text_sanitization(
                table=table,
                op_type=op_type,
                replacements=sanitization.replacements,
                paths=sanitization.paths,
            )

        if primary_key is None:
            pk_value = payload.get("id")
            if pk_value is None:
                self._dropped_ops_count += 1
                self._capture_lost_op(
                    table, payload, op_type, None, reason="no_primary_key"
                )
                return ""
            primary_key = ("id", str(pk_value))

        # A write that arrives once the request's terminal flush has begun or
        # completed (FLUSHING / FLUSHED) is a legitimate LATE write — typically a
        # fire-and-forget tool completion (``log_completed`` / ``log_error``)
        # whose detached_task ran after the lane finalizer sealed the request, or
        # after a delegation suspend already finalized the turn. It MUST NOT be
        # stranded in a rolled OPEN session that nothing will ever flush again,
        # nor silently dropped mid-flush. Fire a durable one-shot on its own
        # fresh Session — the row's INSERT is already committed by the terminal
        # drain, so a late UPDATE matches it. (See _finalize/seal in queue_helpers.)
        if self._phase in (CoordinatorPhase.FLUSHED, CoordinatorPhase.FLUSHING):
            return self._fire_one_shot(table, payload, op_type, primary_key)

        if self._phase is not CoordinatorPhase.OPEN:
            # ERRORED — a commit barrier already failed; the request is stopping
            # and the DB may be wedged. We deliberately do NOT fire a live
            # one-shot write onto a possibly-wedged DB — but we MUST NOT lose the
            # data either. Capture the op to system_write_failure (its own fresh
            # connection, the designated sink) so replay recovers it. Still
            # accounted in _dropped_ops_count so the next check_pending() barrier
            # blows up. (Was previously a silent drop relying only on the
            # watchdog — the gap that lost research_web's completion write.)
            self._dropped_ops_count += 1
            self._capture_lost_op(
                table,
                payload,
                op_type,
                primary_key,
                reason=f"queue_in_phase_{self._phase.value}",
            )
            return ""

        try:
            model_cls = get_model(table)
        except KeyError as exc:
            self._dropped_ops_count += 1
            self._capture_lost_op(
                table, payload, op_type, primary_key,
                reason="unregistered_table", exc=exc,
            )
            return ""

        pk_field, pk_value = primary_key
        try:
            if op_type == "insert":
                merged_payload = dict(payload)
                merged_payload.setdefault(pk_field, pk_value)
                return self._session.defer_insert(
                    model_cls,
                    merged_payload,
                    pk_value=pk_value,
                )
            if op_type == "update":
                return self._session.defer_update(
                    model_cls,
                    pk_value,
                    dict(payload),
                )
            if op_type == "delete":
                return self._session.defer_delete(model_cls, pk_value)
        except Exception as exc:
            self._dropped_ops_count += 1
            self._capture_lost_op(
                table, payload, op_type, primary_key,
                reason="session_defer_failed", exc=exc,
            )
            return ""

        self._dropped_ops_count += 1
        self._capture_lost_op(
            table, payload, op_type, primary_key, reason="unknown_op_type"
        )
        return ""

    def _capture_text_sanitization(
        self,
        *,
        table: str,
        op_type: str,
        replacements: int,
        paths: tuple[str, ...],
    ) -> None:
        request_id = self._request_id
        user_id = self._user_id
        conversation_id = self._conversation_id
        database = self._database

        async def _runner() -> None:
            from matrx_orm.session.fallback import record_error

            await record_error(
                ValueError("PostgreSQL-invalid NUL bytes were replaced before persistence"),
                kind="persistence_payload_sanitized",
                request_id=request_id,
                user_id=user_id,
                conversation_id=conversation_id,
                error_type="PostgresTextSanitization",
                error_text=(
                    f"replaced {replacements} PostgreSQL-invalid NUL byte(s) "
                    f"before {op_type} on {table}"
                ),
                context={
                    "table": table,
                    "op_type": op_type,
                    "replacement_count": replacements,
                    "paths": list(paths),
                    "layer": "coordinator_backstop",
                },
                database=database,
            )

        try:
            from matrx_utils import detached_task

            detached_task(_runner(), name="capture_coordinator_payload_sanitized")
        except RuntimeError:
            logger.error(
                "persistence_payload_sanitized_capture_no_loop table=%s op_type=%s",
                table,
                op_type,
            )

    # ---------------------- late-write auto-elevate ----------------------

    def _fire_one_shot(
        self,
        table: str,
        payload: dict[str, Any],
        op_type: OpType,
        primary_key: tuple[str, str],
    ) -> str:
        """Open a fresh Session-of-one for a late write that arrived after
        the parent Session already flushed."""
        try:
            model_cls = get_model(table)
        except KeyError as exc:
            # A late write is the LAST chance this row has — a console line is
            # not a capture. Route it through the same durable sink every other
            # drop uses so the payload survives and is queryable, instead of
            # vanishing with only a stdout message nobody reads.
            self._dropped_ops_count += 1
            self._capture_lost_op(
                table,
                payload,
                op_type,
                primary_key,
                reason="one_shot_unregistered_table",
                exc=exc,
            )
            return ""

        pk_field, pk_value = primary_key
        request_id = self._request_id
        user_id = self._user_id
        conversation_id = self._conversation_id
        database = self._database

        predecessor = self._late_one_shot_tail

        async def _runner() -> None:
            from matrx_orm.session.managed import _coordinator_session

            if predecessor is not None:
                try:
                    await predecessor
                except Exception:
                    # Each predecessor captures its own durable failure. Keep
                    # draining later operations so one bad write cannot strand
                    # the rest of the late-write lane.
                    pass
            try:
                async with _coordinator_session(database=database) as s:
                    if op_type == "insert":
                        merged = dict(payload)
                        merged.setdefault(pk_field, pk_value)
                        s.defer_insert(model_cls, merged, pk_value=pk_value)
                    elif op_type == "update":
                        s.defer_update(model_cls, pk_value, dict(payload))
                    elif op_type == "delete":
                        s.defer_delete(model_cls, pk_value)
                    else:
                        logger.error(
                            "one_shot_unknown_op_type",
                            extra={"table": table, "op_type": op_type},
                        )
                        return
                vcprint(
                    f"[Coordinator] late one-shot {op_type} on {table} "
                    f"({pk_value[:8] if isinstance(pk_value, str) else pk_value}…) "
                    f"completed",
                    color="green",
                )
            except Exception as exc:
                vcprint(
                    f"[Coordinator] late one-shot {op_type} on {table} "
                    f"FAILED outside Session: {type(exc).__name__}: {exc}. "
                    f"Capturing to system_write_failure for replay.",
                    color="red",
                )
                logger.exception(
                    "one_shot_failed",
                    extra={
                        "table": table,
                        "op_type": op_type,
                        "request_id": request_id,
                        "user_id": user_id,
                        "conversation_id": conversation_id,
                    },
                )
                try:
                    from matrx_connect.streaming.error_capture import capture_error

                    await capture_error(
                        exc,
                        kind="late_persistence_write_failed",
                        route="matrx_ai.persistence.coordinator.one_shot",
                        error_type=type(exc).__name__,
                        request_id=request_id,
                        user_id=user_id,
                        conversation_id=conversation_id,
                        context={"table": table, "op_type": op_type},
                    )
                except Exception:
                    # The replay sink below remains authoritative for the row;
                    # capture must never prevent it from being preserved.
                    pass
                # A late write that one-shotted and then FAILED must NOT vanish
                # (the exact silent loss that left research_web's cx_tool_call
                # stuck 'running' until the 600s watchdog). Capture the op to
                # system_write_failure on a fresh connection so replay recovers
                # it. record_failures never raises.
                try:
                    from matrx_orm.session.fallback import record_failures
                    from matrx_orm.session.op import (
                        make_delete,
                        make_insert,
                        make_update,
                    )

                    if op_type == "insert":
                        _merged = dict(payload)
                        _merged.setdefault(pk_field, pk_value)
                        _op = make_insert(model_cls, _merged, pk_value=pk_value)
                    elif op_type == "update":
                        _op = make_update(model_cls, pk_value, dict(payload))
                    else:
                        _op = make_delete(model_cls, pk_value)
                    await record_failures(
                        [_op],
                        exc,
                        request_id=request_id,
                        user_id=user_id,
                        conversation_id=conversation_id,
                        database=database,
                    )
                    _scream_lost_write(
                        table, op_type, primary_key, "one_shot_failed",
                        request_id, conversation_id,
                    )
                except Exception as cap_exc:  # noqa: BLE001 — last resort
                    logger.error(
                        "one_shot_capture_failed table=%s op_type=%s err=%s",
                        table, op_type, cap_exc,
                    )

        from uuid import uuid4

        op_id = str(uuid4())

        # Use detached_task so the one-shot doesn't inherit the parent's
        # _active_connection (Phase F). matrx-utils is a required dependency;
        # never fall back to an unowned task that inherits the transaction.
        try:
            from matrx_utils import detached_task

            self._late_one_shot_tail = detached_task(
                _runner(), name=f"coord_one_shot_{table}"
            )
        except RuntimeError:
            # No running loop — we cannot schedule the async one-shot OR an
            # async capture. This is process teardown; scream with the exact op.
            _scream_lost_write(
                table, op_type, primary_key, "late_write_no_event_loop",
                self._request_id, self._conversation_id,
            )
        return op_id

    def _capture_lost_op(
        self,
        table: str,
        payload: dict[str, Any],
        op_type: OpType,
        primary_key: tuple[str, str] | None,
        *,
        reason: str,
        exc: BaseException | None = None,
    ) -> None:
        """Durably capture a write the Coordinator could NOT queue, so it is
        replayable from ``system_write_failure`` and never vanishes.

        ``queue()`` is synchronous and ``record_failures()`` is async on its own
        fresh connection, so the capture is scheduled detached (same pattern as
        ``_fire_one_shot``). A clean ``insert``/``update``/``delete`` with a known
        pk is reconstructed into a real ``SessionOp`` (replayable byte-for-byte);
        anything malformed (no pk, unregistered table, unknown op) lands in
        ``system_error`` instead so the loss is STILL durable, never silent.
        """
        _scream_lost_write(
            table, op_type, primary_key, reason, self._request_id, self._conversation_id
        )

        request_id = self._request_id
        user_id = self._user_id
        conversation_id = self._conversation_id
        database = self._database
        capture_exc = exc or RuntimeError(f"coordinator drop: {reason}")

        pk = primary_key
        if pk is None:
            _pid = payload.get("id")
            pk = ("id", str(_pid)) if _pid is not None else None

        async def _runner() -> None:
            from matrx_orm.session.fallback import record_error, record_failures

            try:
                if pk is not None and op_type in ("insert", "update", "delete"):
                    from matrx_orm.session.op import (
                        make_delete,
                        make_insert,
                        make_update,
                    )

                    model_cls = get_model(table)
                    pk_field, pk_value = pk
                    if op_type == "insert":
                        merged = dict(payload)
                        merged.setdefault(pk_field, pk_value)
                        op = make_insert(model_cls, merged, pk_value=pk_value)
                    elif op_type == "update":
                        op = make_update(model_cls, pk_value, dict(payload))
                    else:
                        op = make_delete(model_cls, pk_value)
                    await record_failures(
                        [op],
                        capture_exc,
                        request_id=request_id,
                        user_id=user_id,
                        conversation_id=conversation_id,
                        database=database,
                    )
                    return
                # Malformed op (no pk / unknown op_type) — not cleanly replayable.
                # Capture as a NON-write error so it is still durable + queryable.
                await record_error(
                    capture_exc,
                    kind="coordinator_drop",
                    request_id=request_id,
                    user_id=user_id,
                    conversation_id=conversation_id,
                    error_type="coordinator_drop_malformed",
                    error_text=f"dropped {op_type} on {table} (reason={reason}); not replayable",
                    payload=payload,
                    context={"table": table, "reason": reason, "op_type": op_type},
                    database=database,
                )
            except Exception as cap_exc:  # noqa: BLE001 — capture must never raise
                try:
                    await record_error(
                        capture_exc,
                        kind="coordinator_drop",
                        request_id=request_id,
                        user_id=user_id,
                        conversation_id=conversation_id,
                        error_type="coordinator_drop_uncaptured",
                        error_text=(
                            f"could not capture dropped {op_type} on {table} "
                            f"(reason={reason}): {type(cap_exc).__name__}: {cap_exc}"
                        ),
                        payload=payload,
                        context={
                            "table": table,
                            "reason": reason,
                            # WITHOUT these the record is unactionable: an
                            # operator reading an uncaptured drop must know WHICH
                            # row and WHICH operation to replay by hand.
                            # (2026-08-15: 51 uncaptured drops landed carrying
                            # only table+reason, so the rows they belonged to
                            # could not be named from the record at all.)
                            "op_type": op_type,
                            "primary_key": list(pk) if pk else None,
                        },
                        database=database,
                    )
                except Exception as final_exc:  # noqa: BLE001
                    logger.error(
                        "coordinator_drop_capture_failed table=%s reason=%s err=%s",
                        table, reason, final_exc,
                    )

        try:
            from matrx_utils import detached_task

            detached_task(_runner(), name=f"coord_capture_lost_{table}")
        except RuntimeError:
            logger.error(
                "coordinator_drop_no_loop table=%s reason=%s", table, reason
            )

    # ---------------------- flush ---------------------------------------

    async def flush(
        self,
        *,
        reason: str = "stream_end",
        error_payload: dict[str, Any] | None = None,
    ) -> FlushReport:
        """Delegate to Session.flush(); translate the Session FlushReport
        into the matrx-ai FlushReport shape that lane finalizers /
        observers depend on.

        Idempotent: a second call returns the cached report. The Session's
        own idempotency protects the underlying flush.
        """
        async with self._lock:
            if self._phase in (CoordinatorPhase.FLUSHED, CoordinatorPhase.ERRORED):
                assert self._report is not None
                return self._report

            self._phase = CoordinatorPhase.FLUSHING
            ops_queued_before = self._session.ops_count

            if ops_queued_before == 0 and self._dropped_ops_count == 0:
                empty_report = FlushReport(
                    reason=reason,  # type: ignore[arg-type]
                    ops_queued=0,
                    started_at=datetime.now(UTC),
                    finished_at=datetime.now(UTC),
                )
                self._report = empty_report
                self._phase = CoordinatorPhase.FLUSHED
                return empty_report

            session_report = await self._session.flush(reason=reason)

            translated = FlushReport(
                reason=reason,  # type: ignore[arg-type]
                ops_queued=session_report.ops_queued,
                ops_after_coalesce=session_report.ops_after_coalesce,
                tiers=session_report.tiers,
                ops_written=session_report.ops_written,
                ops_lost=session_report.ops_lost + self._dropped_ops_count,
                started_at=session_report.started_at,
                finished_at=session_report.finished_at,
                error=session_report.error,
                by_table=dict(session_report.by_table),
                tier_summary=list(session_report.tier_summary),
            )
            self._report = translated

            if session_report.error is None:
                self._phase = CoordinatorPhase.FLUSHED
                vcprint(
                    f"[Coordinator] flush({reason}) wrote "
                    f"{translated.ops_written} op(s) across {translated.tiers} "
                    f"tier(s) (coalesced from {translated.ops_queued} queued)",
                    color="green",
                )
            else:
                self._phase = CoordinatorPhase.ERRORED
                vcprint(
                    f"[Coordinator] flush({reason}) ERRORED: "
                    f"{session_report.error}. {translated.ops_lost} op(s) lost "
                    f"(see system_write_failure or scream log).",
                    color="red",
                )
            return translated

    # ════════════ fire-and-forget + accountability (the hot path) ════════

    async def acquire_commit_slot(
        self, *, wait_seconds: float = _COMMIT_SLOT_WAIT_SECONDS
    ) -> bool:
        """Wait (bounded) for a free process-wide background-commit slot so the
        next :meth:`commit_async` can fire.

        This is the REAL backpressure: under legitimate fan-out (N parallel
        agent runs in one workflow super-step, each its own Coordinator) the
        process-wide budget is momentarily full while perfectly healthy
        millisecond-scale commits drain. Waiting a few milliseconds is the
        correct response; failing the request is not.

        It does NOT weaken the durability contract in any way: nothing is
        committed unconfirmed, no barrier is skipped, the cap is unchanged, and
        the wait is bounded — if it expires, ``commit_async`` raises
        :class:`PersistenceBarrierError` exactly as before, now meaning what it
        says ("still not draining after N seconds"). Returns True when a slot is
        held. Call it at a barrier, immediately before ``commit_async``."""
        if self._slot_reserved:
            return True
        if self._phase in (CoordinatorPhase.FLUSHED, CoordinatorPhase.ERRORED):
            return False
        if self._session.ops_count == 0:
            return False  # nothing to commit — never hold a slot idle
        deadline = time.monotonic() + wait_seconds
        waited_from: float | None = None
        while True:
            if _try_reserve_commit_slot():
                self._slot_reserved = True
                if waited_from is not None:
                    logger.info(
                        "[Coordinator] waited %.0fms for a background-commit "
                        "slot (fan-out backpressure, cap %d) — request=%s",
                        (time.monotonic() - waited_from) * 1000,
                        _MAX_INFLIGHT_COMMITS,
                        self._request_id,
                    )
                return True
            if time.monotonic() >= deadline:
                # Genuinely not draining. Leave it to commit_async to raise the
                # barrier error (one failure path, one report shape).
                return False
            if waited_from is None:
                waited_from = time.monotonic()
            await asyncio.sleep(_COMMIT_SLOT_POLL_SECONDS)

    def commit_async(self, *, reason: str = "turn_commit") -> None:
        """FIRE this turn's accumulated writes as a background commit and roll a
        fresh Session — NON-BLOCKING. The flush runs on its own DB connection
        (clean context) so it overlaps the next model call instead of delaying
        it. Verify it landed at the next barrier via :meth:`check_pending`.

        A queue-time drop is a lost write → blow up immediately (never fire past
        a drop). An empty turn is a no-op. This is the hot-path commit; the only
        deliberately blocking commits are :meth:`finalize` (final / pre-suspend /
        fork-join). See the persistence contract in CLAUDE.md.

        Sync (no ``await``) so it is atomic w.r.t. other coroutines — the roll +
        spawn + append happen without an interleaving point.
        """
        # Consume any slot reserved by ``acquire_commit_slot`` at this barrier.
        # Every path that does NOT end in a fired commit gives it back.
        holding_slot = self._slot_reserved
        self._slot_reserved = False

        def _give_back() -> None:
            if holding_slot:
                _release_commit_slot()

        if self._phase in (CoordinatorPhase.FLUSHED, CoordinatorPhase.ERRORED):
            _give_back()
            return
        if self._dropped_ops_count > 0:
            _give_back()
            report = FlushReport(
                reason=reason,  # type: ignore[arg-type]
                ops_lost=self._dropped_ops_count,
                started_at=datetime.now(UTC),
                finished_at=datetime.now(UTC),
                error=f"{self._dropped_ops_count} op(s) dropped at queue time",
            )
            self._phase = CoordinatorPhase.ERRORED
            self._report = report
            raise PersistenceBarrierError(
                reason=reason,
                report=report,
                conversation_id=self._conversation_id,
                request_id=self._request_id,
            )
        if self._session.ops_count == 0:
            _give_back()
            return  # nothing to commit this turn

        # BACKPRESSURE: a slot must be held before firing. The barrier normally
        # already WAITED for one (``acquire_commit_slot``); reaching this branch
        # without a reservation means the wait expired (or a caller skipped it)
        # AND the process-wide budget is still full — i.e. commits genuinely are
        # not draining. Then we stop this request loudly rather than pile up and
        # starve the connection pool. The current cache stays in the Session and
        # is secured by the degrade-drain in the except handler.
        # (Data first; see CLAUDE.md.)
        if not holding_slot and not _try_reserve_commit_slot():
            report = FlushReport(
                reason=reason,  # type: ignore[arg-type]
                ops_lost=self._session.ops_count,
                started_at=datetime.now(UTC),
                finished_at=datetime.now(UTC),
                error=f"backpressure: {_inflight_commits} bg commits in flight "
                f"(cap {_MAX_INFLIGHT_COMMITS}) still unfinished after waiting "
                f"{_COMMIT_SLOT_WAIT_SECONDS:.0f}s — DB not draining",
            )
            self._phase = CoordinatorPhase.ERRORED
            self._report = report
            raise PersistenceBarrierError(
                reason=reason,
                report=report,
                conversation_id=self._conversation_id,
                request_id=self._request_id,
            )

        old_session = self._session
        ops = old_session.ops_count
        self._roll_session()  # swap to a fresh OPEN Session synchronously
        task = self._spawn_commit(old_session, reason)
        self._pending_commits.append(
            _PendingCommit(task=task, reason=reason, fired_at=time.monotonic(), ops=ops)
        )

    def _spawn_commit(self, session: Any, reason: str) -> asyncio.Task[Any]:
        cid, rid, database = self._conversation_id, self._request_id, self._database

        async def _runner() -> Any:
            try:
                # HARD DEADLINE on the background commit so it releases its pool
                # connection at a known bound even if the DB is wedged. Without
                # this an orphaned overdue commit holds a connection ~indefinitely
                # → pool exhaustion → service-wide hang.
                rep = await asyncio.wait_for(
                    session.flush(reason=reason),
                    timeout=_COMMIT_HARD_DEADLINE_SECONDS,
                )
            except TimeoutError:
                # Blew the deadline → wait_for cancelled the flush (its transaction
                # rolled back + released the connection). CancelledError bypassed
                # Session.flush's record_failures, so capture the ops HERE on a
                # FRESH connection — never lose them — then surface a barrier fail.
                try:
                    from matrx_orm.session.fallback import record_failures

                    ops = list(getattr(session, "_ops", []) or [])
                    if ops:
                        await record_failures(
                            ops,
                            TimeoutError(
                                f"commit hard-deadline {_COMMIT_HARD_DEADLINE_SECONDS:.0f}s"
                            ),
                            session_id=getattr(session, "id", ""),
                            database=database,
                        )
                except Exception as cap_exc:  # noqa: BLE001 — last resort
                    logger.error("hard_deadline_capture_failed: %s", cap_exc)
                raise PersistenceBarrierError(
                    reason=f"{reason}_hard_deadline",
                    report=FlushReport(
                        reason=reason,  # type: ignore[arg-type]
                        error=f"commit hard-deadline {_COMMIT_HARD_DEADLINE_SECONDS:.0f}s exceeded",
                    ),
                    conversation_id=cid,
                    request_id=rid,
                )
            if rep.error is not None:
                # Session.flush already captured the ops to system_write_failure;
                # raise so the next check_pending() degrades + blows up.
                raise PersistenceBarrierError(
                    reason=reason,
                    report=FlushReport(
                        reason=reason,  # type: ignore[arg-type]
                        ops_queued=rep.ops_queued,
                        ops_written=rep.ops_written,
                        ops_lost=rep.ops_lost,
                        error=rep.error,
                        started_at=rep.started_at,
                        finished_at=rep.finished_at,
                    ),
                    conversation_id=cid,
                    request_id=rid,
                )
            return rep

        # detached_task spawns in a CLEAN context so the bg flush gets its OWN
        # pool connection and never inherits an active transaction connection
        # (the asyncpg "another operation in progress" bug class).
        try:
            from matrx_utils import detached_task

            task = detached_task(_runner(), name=f"coord_commit_{reason}")
        except RuntimeError as exc:
            raise PersistenceBarrierError(
                reason=reason,
                report=FlushReport(reason=reason, error=str(exc)),
                conversation_id=self._conversation_id,
                request_id=self._request_id,
            ) from exc
        # The process-wide backpressure slot for this commit was RESERVED by the
        # caller (commit_async) before we got here — reserving up front is what
        # makes a waiting barrier safe (a waiter that saw a free slot cannot be
        # beaten to it). It is released in _on_commit_done.
        # Always observe the outcome — even if this commit becomes an orphan
        # (overdue → check_pending already blew up and stopped awaiting it). The
        # callback retrieves the exception so it's never an unobserved "Task
        # exception was never retrieved", decrements the in-flight count, and logs.
        task.add_done_callback(self._on_commit_done)
        return task

    @staticmethod
    def _on_commit_done(task: asyncio.Task[Any]) -> None:
        # Release the slot this commit held. Floor-clamped: a dropped/late
        # callback (loop teardown) must never let the process-wide counter drift
        # up into a permanent false-backpressure wedge.
        _release_commit_slot()
        if task.cancelled():
            return
        exc = task.exception()
        if exc is not None:
            vcprint(
                f"[Coordinator] background commit finished FAILED (ops already "
                f"captured to system_write_failure via the Session fallback): "
                f"{type(exc).__name__}: {exc}",
                color="red",
            )

    async def check_pending(self, *, grace_seconds: float = _COMMIT_GRACE_SECONDS) -> None:
        """ACCOUNTABILITY: confirm prior fired commits landed. Called at each
        barrier. A failed commit, or one still unfinished after ``grace_seconds``
        (it should already be done — it had a whole model call to finish), RAISES
        :class:`PersistenceBarrierError`. Bounded — never hangs."""
        if not self._pending_commits:
            return
        # Snapshot the pending list under the lock (no await → atomic), then
        # await OUTSIDE the lock so a stuck commit (up to grace_seconds) can't
        # block a concurrent drain / the cancel path.
        async with self._lock:
            pending, self._pending_commits = self._pending_commits, []
        err: PersistenceBarrierError | None = None
        for pc in pending:
            try:
                await asyncio.wait_for(asyncio.shield(pc.task), timeout=grace_seconds)
            except TimeoutError:
                # Overdue → blow up loudly (bounded at grace_seconds; no
                # indefinite hang). Do NOT cancel the orphan: a CancelledError
                # would bypass Session.flush's record_failures and LOSE the data.
                # Leave it running — it self-bounds via its hard deadline and
                # captures to system_write_failure; _on_commit_done observes it.
                err = err or PersistenceBarrierError(
                    reason=f"{pc.reason}_overdue",
                    report=FlushReport(
                        reason=pc.reason,
                        ops_lost=pc.ops,  # type: ignore[arg-type]
                        error=f"commit overdue >{grace_seconds:.0f}s (DB stuck?)",
                    ),
                    conversation_id=self._conversation_id,
                    request_id=self._request_id,
                )
            except PersistenceBarrierError as e:
                err = err or e
            except Exception as e:  # noqa: BLE001
                err = err or PersistenceBarrierError(
                    reason=pc.reason,
                    report=FlushReport(
                        reason=pc.reason,
                        ops_lost=pc.ops,  # type: ignore[arg-type]
                        error=f"{type(e).__name__}: {e}",
                    ),
                    conversation_id=self._conversation_id,
                    request_id=self._request_id,
                )
        if err is not None:
            await self._apply_verdict(err.report, errored=True)
            vcprint(
                f"[Coordinator] ACCOUNTABILITY CHECK FAILED: {err}",
                color="red",
            )
            raise err

    async def _apply_verdict(self, report: FlushReport, *, errored: bool) -> None:
        """Record the persistence verdict atomically and MONOTONICALLY. ERRORED
        is sticky — a racing success drain (e.g. cancel-path finalize vs lane
        drain) can never overwrite a failure verdict, so the STOP-EVERYTHING
        signal always survives.

        LOAD-BEARING INVARIANT: this critical section must contain NO ``await``
        (between acquiring the lock and returning). ``commit_async`` sets
        ``_phase = ERRORED`` synchronously without the lock on its drop /
        backpressure paths; that is only torn-state-safe because the locked
        block here is atomic w.r.t. other coroutines on a single event loop.
        Keep both properties (no await here; commit_async stays sync) or add a
        real lock to commit_async."""
        async with self._lock:
            if self._phase is CoordinatorPhase.ERRORED:
                return
            self._report = report
            if errored:
                self._phase = CoordinatorPhase.ERRORED

    # ════════════ synchronous commit points (deliberate blocks) ══════════

    async def finalize(self, *, reason: str = "commit") -> FlushReport:
        """SYNCHRONOUS commit point — flush the current cache AND drain every
        in-flight commit, then RAISE on any failure. Use ONLY at the deliberate
        blocking points: the final commit at request end, the pre-suspend commit
        before a client-delegated tool, and sub-agent fork/join. The hot path
        uses :meth:`commit_async` + :meth:`check_pending` instead.
        """
        if self._phase is CoordinatorPhase.ERRORED and self._report is not None:
            raise PersistenceBarrierError(
                reason=reason,
                report=self._report,
                conversation_id=self._conversation_id,
                request_id=self._request_id,
            )
        # _flush_current_and_drain locks only its synchronous snapshot internally.
        report, failures = await self._flush_current_and_drain(
            reason=reason,
            timeout=_DRAIN_TIMEOUT_SECONDS,
        )
        await self._apply_verdict(report, errored=bool(failures))
        if failures:
            vcprint(
                f"[Coordinator] COMMIT BARRIER FAILED ({reason}): {report.error}. "
                f"STOPPING (conversation={self._conversation_id}, "
                f"request={self._request_id}). See system_write_failure.",
                color="red",
            )
            raise PersistenceBarrierError(
                reason=reason,
                report=report,
                conversation_id=self._conversation_id,
                request_id=self._request_id,
            )
        return report

    async def seal(self) -> None:
        """TERMINAL SEAL — call exactly once AFTER the lane's final drain.

        ``finalize`` / ``drain_and_confirm`` keep the coordinator OPEN (they roll
        a fresh empty Session each time) so multi-turn runs can keep writing. But
        once the request lane has drained for the LAST time, that fresh OPEN
        Session is a trap: any fire-and-forget write that lands in it afterwards
        (a server tool's detached ``log_completed`` that finished after a
        delegation suspend; any late telemetry write) will NEVER be flushed
        again, and is silently lost — the exact cause of cx_tool_call rows stuck
        at ``status='running'`` despite the tool succeeding.

        Sealing flips the phase to FLUSHED so every subsequent ``queue()`` fires a
        durable one-shot on its own Session instead of stranding. Any op that
        landed in the window between the final drain and this seal is flushed here
        first. NON-BLOCKING in the common case (no residual ops). Never downgrades
        an ERRORED verdict (the STOP-EVERYTHING signal must survive).
        """
        async with self._lock:
            if self._phase is CoordinatorPhase.ERRORED:
                return
            residual = self._session
            had_ops = residual.ops_count > 0
            # Seal FIRST: with phase=FLUSHED, any write arriving DURING the
            # residual flush below one-shots on its own Session and cannot race
            # this flush.
            self._phase = CoordinatorPhase.FLUSHED

        if had_ops:
            try:
                await residual.flush(reason="seal")
            except Exception as exc:  # noqa: BLE001 — best-effort terminal flush
                vcprint(
                    f"[Coordinator] seal() residual flush failed: "
                    f"{type(exc).__name__}: {exc}. Subsequent late writes one-shot.",
                    color="red",
                )

    async def drain_and_confirm(self, *, reason: str = "degrade") -> list[str]:
        """DEGRADE to synchronous — DATA FIRST, never raises. On ANY anomaly the
        caller invokes this BEFORE error-handling/unwinding: it flushes the cache
        and awaits every in-flight commit, capturing failures (already recorded
        to system_write_failure by the Session fallback). Returns failure
        descriptions for the caller to surface. See CLAUDE.md."""
        # _flush_current_and_drain locks only its synchronous snapshot internally.
        report, failures = await self._flush_current_and_drain(
            reason=reason,
            timeout=_DRAIN_TIMEOUT_SECONDS,
        )
        await self._apply_verdict(report, errored=bool(failures))
        if failures:
            vcprint(
                f"[Coordinator] DEGRADE drain({reason}) had {len(failures)} "
                f"failure(s): {report.error}. See system_write_failure.",
                color="red",
            )
        return failures

    async def _flush_current_and_drain(
        self,
        *,
        reason: str,
        timeout: float,
    ) -> tuple[FlushReport, list[str]]:
        """Await all in-flight commits FIRST (so prior-turn INSERTs land), THEN
        flush the current Session (so any current-turn UPDATE sees the prior
        INSERT it depends on). Returns (report, failures); does not raise —
        Session.flush captures its own failures to system_write_failure;
        bg-commit failures are collected.

        The lock is held ONLY for the synchronous snapshot + roll, never across
        the awaits — so a long drain (a stuck commit, up to ``timeout``) can't
        block a concurrent check_pending / drain / the cancel path."""
        # A slot reserved for a commit that never fired (an anomaly between the
        # barrier's acquire and its commit_async) must not leak into a permanent
        # false-backpressure wedge. Both blocking paths — finalize and the
        # degrade drain — funnel through here.
        if self._slot_reserved:
            self._slot_reserved = False
            _release_commit_slot()
        failures: list[str] = []
        report = FlushReport(reason=reason, started_at=datetime.now(UTC))  # type: ignore[arg-type]

        # Snapshot under the lock (no await → atomic): take the pending commits
        # and the current Session, and roll a fresh one so new writes go
        # elsewhere while we flush the captured one. A concurrent drain that runs
        # second sees empty pending + a fresh empty Session → a clean no-op (no
        # double-drain, no double-flush).
        async with self._lock:
            pending, self._pending_commits = self._pending_commits, []
            if self._session.ops_count > 0:
                current_session: Any | None = self._session
                self._roll_session()
            else:
                current_session = None
            dropped = self._dropped_ops_count
            self._dropped_ops_count = 0  # accounted below — never double-count

        # Await OUTSIDE the lock. 1) Drain in-flight commits FIRST — a current
        # UPDATE must never flush ahead of the prior-turn INSERT it targets.
        for pc in pending:
            try:
                await asyncio.wait_for(asyncio.shield(pc.task), timeout=timeout)
            except TimeoutError:
                # Overdue → report (bounded at timeout). Do NOT cancel: a
                # CancelledError bypasses Session.flush's record_failures and
                # loses the data. The orphan self-bounds via its hard deadline and
                # captures to system_write_failure; _on_commit_done observes it.
                failures.append(f"{pc.reason}:overdue>{timeout:.0f}s")
                report.ops_lost += pc.ops
            except PersistenceBarrierError as e:
                failures.append(f"{pc.reason}:{e.report.error}")
                report.ops_lost += pc.ops
            except Exception as e:  # noqa: BLE001
                failures.append(f"{pc.reason}:{type(e).__name__}:{e}")
                report.ops_lost += pc.ops

        # 2) Flush the captured current cache.
        if current_session is not None:
            srep = await current_session.flush(reason=reason)
            report.ops_queued = srep.ops_queued
            report.ops_after_coalesce = srep.ops_after_coalesce
            report.tiers = srep.tiers
            report.ops_written = srep.ops_written
            report.by_table = dict(srep.by_table)
            report.tier_summary = list(srep.tier_summary)
            if srep.error is not None:
                failures.append(f"current:{srep.error}")
                report.ops_lost += srep.ops_lost

        if dropped:
            failures.append(f"dropped_ops:{dropped}")
            report.ops_lost += dropped

        report.finished_at = datetime.now(UTC)
        report.error = "; ".join(failures) if failures else None
        return report, failures

    def _roll_session(self) -> None:
        """Swap the just-flushed Session for a fresh OPEN one, keeping the
        Coordinator OPEN. Replaces the entry on matrx-orm's ``_session_stack``
        in place so managed-Model writes and queue helpers both reach the new
        Session and the stack never grows unbounded across turns."""
        from matrx_orm.session.managed import _coordinator_session
        from matrx_orm.session.session import _session_stack

        old = self._session
        new = _coordinator_session(database=self._database)
        self._session = new
        stack = _session_stack.get()
        if any(s is old for s in stack):
            _session_stack.set(tuple(new if s is old else s for s in stack))
        else:
            # Defensive: the coordinator's session is normally on the stack
            # (pushed at __init__); never lose the new one if it isn't.
            _session_stack.set(stack + (new,))


# ---------------------------------------------------------------------------
# Back-compat alias. ``WriteCoordinator`` was the May 2026 public name.
# Anything that still imports it gets the new implementation transparently.
# Schedule for deletion in the next PR after observation.
# ---------------------------------------------------------------------------
WriteCoordinator = Coordinator
