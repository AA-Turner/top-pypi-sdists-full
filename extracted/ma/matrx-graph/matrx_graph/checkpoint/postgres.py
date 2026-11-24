from __future__ import annotations

import asyncio
import json
import logging
import inspect
from functools import wraps
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import Any

from matrx_graph.failure import Cause, client_safe_error_payload, persistence_cause_for_exception
from matrx_graph.checkpoint.protocol import (
    Checkpoint,
    NextInvocation,
    NodeOutcome,
    PendingBinding,
    ReadScopeFactory,
    latest_settled_keys,
    read_scope,
    read_scope_factory_for,
)
from matrx_graph.checkpoint.values import (
    InternMemo,
    checkpoint_columns,
    outcome_input_row,
    run_pure_off_loop,
    referenced_hashes,
    resolve_values,
)
from matrx_graph.db._registry import get_model
from matrx_graph.errors import CheckpointWriteFailedError
from matrx_graph.knobs import CheckpointWritePolicy, checkpoint_write_policy
from matrx_graph.types.send import Send

logger = logging.getLogger(__name__)

# The checkpoint write is the ONE write in this package that is provably safe to
# re-issue after an ambiguous timeout: the row is keyed by a caller-chosen
# checkpoint id, so a second attempt either inserts it or proves the first one
# landed (``_checkpoint_landed``). That is why matrx-orm's own write path refuses
# to retry these classes and the decision is made HERE, where the idempotency
# key is known — never as a general ORM policy.
_RETRYABLE_WRITE_TYPE_NAMES = frozenset(
    {
        "QueryTimeoutError",
        "PoolAcquireTimeoutError",
        "LockContentionError",
        "WriteQueueTimeoutError",
        "WriteQueueFullError",
        "ConnectionDoesNotExistError",
        "InterfaceError",
    }
)


async def _organization_for_run(run_id: str) -> str:
    """workflow.checkpoint / workflow.node_outcome carry organization_id NOT
    NULL but have no independent org source of their own — they are CHILDREN
    of workflow.run (which the router stamped with the verified request's
    organization at run-creation time; see matrx_graph/db/run_store.py).
    Carry it, never default it. Raises loudly if the parent run cannot be
    found or itself carries none — a checkpoint/outcome for a run with no
    resolvable organization must never land.

    A run's organization is fixed at creation and never changes, so a found
    answer is remembered for the process: this lookup ran before EVERY
    checkpoint, outcome and by-reference event value (a full ``SELECT *`` of
    the run row each time — 2026-10-27: ~95k reads, the per-super-step
    overhead of a 15-step run was ~70 ms). A miss is never remembered. The
    memory's size is the ``workflow.run_org_cache_size`` knob."""
    key = str(run_id)
    known = _RUN_ORGANIZATION.get(key)
    if known is not None:
        return known
    wf_run = get_model("WfRun")
    row = await wf_run.get_or_none(id=run_id)
    org = getattr(row, "organization_id", None) if row is not None else None
    if not org:
        raise ValueError(
            f"run {run_id!r} has no resolvable organization_id — refusing to "
            "write a checkpoint/outcome row with no organization"
        )
    from matrx_graph.knobs import run_org_cache_size

    limit = await run_org_cache_size()
    if limit > 0:  # 0 = the knob is unreadable or set to remember nothing
        while len(_RUN_ORGANIZATION) >= limit:
            _RUN_ORGANIZATION.pop(next(iter(_RUN_ORGANIZATION)))
        _RUN_ORGANIZATION[key] = str(org)
    return str(org)


# run_id -> organization_id (immutable per run); insertion-ordered, oldest evicted first.
_RUN_ORGANIZATION: dict[str, str] = {}

# run_id -> the run's status read by its latest checkpoint save, taken once by the
# scheduler's next boundary poll (PostgresCheckpointer.pop_run_status). Bounded:
# a run that ends without polling again leaves one entry, evicted oldest first.
_RUN_STATUS_AT_SAVE: dict[str, str] = {}
_RUN_STATUS_AT_SAVE_MAX = 1024  # protocol-constant: memory bound on an in-process status cache (evicted when full), not an admin behavior


def _remember_run_status(run_id: str, result: Any) -> None:
    rows = getattr(result, "updated_rows", None) or []
    status = rows[0].get("status") if rows and isinstance(rows[0], dict) else None
    key = str(run_id)
    _RUN_STATUS_AT_SAVE.pop(key, None)
    if status is None:
        return
    while len(_RUN_STATUS_AT_SAVE) >= _RUN_STATUS_AT_SAVE_MAX:
        _RUN_STATUS_AT_SAVE.pop(next(iter(_RUN_STATUS_AT_SAVE)))
    _RUN_STATUS_AT_SAVE[key] = str(status)


def _is_retryable_write_failure(exc: BaseException) -> bool:
    """Whether re-issuing the keyed INSERT is worth an attempt.

    Matched on the exception's CLASS (its whole MRO), never on its message: the
    ORM renders the statement's args into that message, and the args are the
    run's data. See ``matrx_graph.failure`` for the failure this rule came from.
    """
    return any(klass.__name__ in _RETRYABLE_WRITE_TYPE_NAMES for klass in type(exc).__mro__)


def _payload_bytes(*values: Any) -> int:
    """Serialized size of what the checkpoint is about to store.

    Measured, not estimated — it goes into the person-facing failure sentence and
    into the over-size alarm, and a wrong number there would send the next agent
    hunting the wrong thing.
    """
    total = 0
    for value in values:
        try:
            total += len(json.dumps(value, default=str).encode())
        except Exception:  # noqa: BLE001 — sizing must never break the write
            continue
    return total

_CHECKPOINT_COLUMNS = (
    "id",
    "run_id",
    "thread_id",
    "parent_checkpoint_id",
    "step",
    "channel_values",
    "pending_bindings",
    "next_invocations",
    "interrupt_payload",
    "metadata",
    "created_at",
)

_OUTCOME_COLUMNS = (
    "run_id",
    "step",
    "node_id",
    "attempt",
    "dispatch_id",
    "item_index",
    "output",
    "channel_writes",
    "sends",
    "emissions",
    "duration_ms",
    "error",
    "source",
    "completed_at",
    "output_kind",
    "output_kind_ok",
    "output_kind_errors",
)

# Versioned kind-verdict refs (Content-IR Wave 1, lane W1-G). Each column is
# written/read ONLY when the generated ORM model actually declares it —
# capability-gated per column, so each activates itself the moment
# `python db/generate.py` regenerates db/models/workflow.py, no code change
# needed. Status 2026-07-15: BOTH DDLs are live (A3 DB lane — wf_018
# output_kind_version, wf_021 output_kind_degraded) but the generated model
# carries neither yet, so both writes stay gated OFF pending the regen (owned
# by the DB lane). Until then the values are computed and carried on
# NodeOutcome/events in memory but not persisted, and this module screams
# once per process per missing column.
_VERSIONED_KIND_COLUMNS = ("output_kind_version", "output_kind_degraded")

# The INPUT half of a node occurrence (contract C-30, migration wf_031).
# Capability-gated by the SAME mechanism as the versioned kind columns above,
# and for the same reason: matrx-graph must keep working against a host whose
# generated model predates the DDL. Unlike those columns this one is silent
# when absent — a package running standalone against an older schema is a
# supported deployment, not a defect to scream about every process.
_INPUT_ENVELOPE_COLUMNS = ("input", "input_kind")
_input_envelope_capability: tuple[str, ...] | None = None


def _available_input_envelope_columns() -> tuple[str, ...]:
    global _input_envelope_capability
    if _input_envelope_capability is None:
        fields = getattr(get_model("WfNodeOutcome"), "_fields", None) or {}
        _input_envelope_capability = tuple(c for c in _INPUT_ENVELOPE_COLUMNS if c in fields)
        if len(_input_envelope_capability) != len(_INPUT_ENVELOPE_COLUMNS):
            logger.info(
                "workflow.node_outcome has no input-envelope column(s) %s — per-step "
                "INPUT capture (C-30) is off for this deployment; outputs are "
                "unaffected. Apply wf_031 and regenerate models to activate it.",
                ", ".join(c for c in _INPUT_ENVELOPE_COLUMNS if c not in fields),
            )
    return _input_envelope_capability


_versioned_kind_capability: tuple[str, ...] | None = None


def _available_versioned_kind_columns() -> tuple[str, ...]:
    """Capability check: which versioned kind-verdict columns the generated
    workflow.node_outcome model carries. Cached per process; loud (once) about
    every missing column."""
    global _versioned_kind_capability
    if _versioned_kind_capability is None:
        fields = getattr(get_model("WfNodeOutcome"), "_fields", None) or {}
        _versioned_kind_capability = tuple(c for c in _VERSIONED_KIND_COLUMNS if c in fields)
        missing = [c for c in _VERSIONED_KIND_COLUMNS if c not in fields]
        if missing:
            logger.error(
                "TODO HANDSHAKE (DB-owner lane, project A3 version-reference "
                "DDL): the generated workflow.node_outcome model is missing "
                "column(s) %s — kind verdict version/degraded-reason are "
                "computed and emitted on events but NOT persisted for them. "
                "Both DDLs are live (wf_018 output_kind_version, wf_021 "
                "output_kind_degraded); regenerate db/models via "
                "`python db/generate.py` and each write activates itself "
                "(capability-gated, no code change needed).",
                ", ".join(missing),
            )
    return _versioned_kind_capability


def _outcome_columns() -> tuple[str, ...]:
    return (
        *_OUTCOME_COLUMNS,
        *_available_versioned_kind_columns(),
        *_available_input_envelope_columns(),
    )


def _read_scope(instance: Any, unit: str, run_id: str | None, checkpoint_id: str | None):
    return read_scope(read_scope_factory_for(instance), unit, run_id, checkpoint_id)


def _scoped_read[**P, T](method: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
    signature = inspect.signature(method)

    @wraps(method)
    async def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        bound = signature.bind(*args, **kwargs)
        async with _read_scope(
            args[0], method.__name__, bound.arguments.get("run_id"), bound.arguments.get("checkpoint_id")
        ):
            return await method(*args, **kwargs)

    return wrapped


class PostgresCheckpointer:
    """Durable Checkpointer backed by the workflow.checkpoint + workflow.node_outcome tables.

    Uses the host-injected matrx-orm models (``configure_db`` /
    ``matrx_graph.db.db_requirements``). Resolution happens at call time, so
    importing this module never requires a configured registry; calling a
    method before ``configure_db()`` raises ``DBNotConfiguredError`` loudly.

    The Checkpointer protocol maps to two tables:
        - Checkpoint      → workflow.checkpoint
        - NodeOutcome     → workflow.node_outcome (UNIQUE on
          (run_id, step, node_id, dispatch_id, item_index, attempt))

    Run-level metadata (status, user, organization, conversation) lives in
    workflow.run and is owned by the router, not the Checkpointer. The Checkpointer
    never writes workflow.run; it only updates workflow.run.last_checkpoint_id after
    save_checkpoint so the router can efficiently find the latest.
    """

    def __init__(self, *, read_scope: ReadScopeFactory | None = None) -> None:
        self._read_scope_factory = read_scope

    async def save_checkpoint(
        self,
        checkpoint: Checkpoint,
        *,
        _outcomes: list[_PreparedOutcome] | None = None,
        _earlier: Sequence[tuple[Checkpoint, Sequence[_PreparedOutcome]]] = (),
    ) -> None:
        # ``_earlier`` (``save_checkpoint_chain``): the checkpoints of a chain of pure steps
        # before this one, each with its outcomes — every row lands in THIS save's transaction.
        # ``_outcomes`` (``save_checkpoint_with_outcomes``): outcome rows that land in the
        # checkpoint's own transaction.
        # The status an EARLIER save read is stale from here on: only a write that lands in
        # THIS save may hand the next boundary a status. A save that ends without one (a
        # timed-out attempt that had committed, a failure) leaves none, so the boundary reads.
        _RUN_STATUS_AT_SAVE.pop(str(checkpoint.run_id), None)
        # Serialization guard (audit P2-2): channel_values are JSON-coerced
        # at write time by the channel layer, but interrupt_payload and
        # pending_bindings' payload fragments arrive raw from node code — a
        # datetime/Decimal/set in either used to raise bare TypeError HERE.
        # The ORM's JSONBField coerces non-JSON leaves on the fly (isoformat /
        # str / repr), so the write stays durable either way; this pre-check
        # keeps the loud warning so the smell is never silent.
        def _warn_if_non_json(value: object, what: str) -> None:
            try:
                json.dumps(value)
            except TypeError:
                logger.warning(
                    "checkpoint %s for run %s: %s contained non-JSON values "
                    "— coerced by the ORM JSONB serializer",
                    checkpoint.checkpoint_id[:8],
                    checkpoint.run_id[:8],
                    what,
                )

        policy = await checkpoint_write_policy()
        from matrx_graph.knobs import interning_grain

        grain = await interning_grain()
        # MKT-111: every value over THE ONE GRAIN goes BY REFERENCE, stored once per run
        # — when this deployment has the value store (a host that has not
        # generated the model writes everything inline, as before).
        # One memo for every row this save writes (a chain of pure steps names the same settled
        # outputs in each of its checkpoints): each value is walked and hashed once (InternMemo).
        # Its committed hashes: a value an earlier save of the run (or this process's outcome rows) already
        # stored is a reference with no walk (values.InternMemo, the process's interned-value cache).
        memo = InternMemo(_stored_value_hashes.get(checkpoint.run_id) or frozenset())

        def _columns_and_size() -> tuple[dict[str, Any], dict[str, Any], int]:
            # Pure: interning, the JSON checks and the size walk every value — off the
            # event loop for a large checkpoint (run_pure_off_loop, PF-WF).
            cols, vals = checkpoint_columns(
                checkpoint, grain if _value_store_available() else 0, memo
            )
            _warn_if_non_json(cols["channel_values"], "channel_values")
            _warn_if_non_json(cols["pending_bindings"], "pending_bindings")
            if checkpoint.interrupt_payload is not None:
                _warn_if_non_json(checkpoint.interrupt_payload, "interrupt_payload")
            size = _payload_bytes(cols["channel_values"], cols["pending_bindings"], cols["next_invocations"])
            return cols, vals, size

        columns, values, payload_bytes = await run_pure_off_loop(
            _columns_and_size,
            values=(checkpoint.channel_values, checkpoint.next_invocations, checkpoint.pending_bindings),
        )
        earlier: list[tuple[Checkpoint, dict[str, Any], dict[str, Any], Sequence[_PreparedOutcome]]] = []
        for earlier_cp, earlier_outcomes in _earlier:

            def _earlier_columns(cp: Checkpoint = earlier_cp) -> tuple[dict[str, Any], dict[str, Any], int]:
                cols, vals = checkpoint_columns(cp, grain if _value_store_available() else 0, memo)
                _warn_if_non_json(cols["channel_values"], "channel_values")
                _warn_if_non_json(cols["pending_bindings"], "pending_bindings")
                return cols, vals, _payload_bytes(cols["channel_values"], cols["pending_bindings"], cols["next_invocations"])

            cols, vals, size = await run_pure_off_loop(
                _earlier_columns,
                values=(earlier_cp.channel_values, earlier_cp.next_invocations, earlier_cp.pending_bindings),
            )
            if size >= policy.warn_bytes:
                # SHOW WHAT YOU HIDE, for every checkpoint of a chain (not only its last).
                logger.error(
                    "checkpoint %s for run %s step %s is %s bytes — over the "
                    "workflow.checkpoint_write.warn_bytes knob (%s); %d scheduled invocation(s) inline",
                    earlier_cp.checkpoint_id[:8],
                    earlier_cp.run_id[:8],
                    earlier_cp.step,
                    f"{size:,}",
                    f"{policy.warn_bytes:,}",
                    len(cols["next_invocations"]),
                )
            earlier.append((earlier_cp, cols, vals, earlier_outcomes))
        next_invocations = columns["next_invocations"]
        if payload_bytes >= policy.warn_bytes:
            # SHOW WHAT YOU HIDE: a fan-out that stores every item's full input
            # inline in next_invocations is what made run 053e8b72's step-3
            # checkpoint 1.1 MB. Name the size and the nodes so the next step
            # (payloads by reference) has evidence, not anecdote.
            logger.error(
                "checkpoint %s for run %s step %s is %s bytes — over the "
                "workflow.checkpoint_write.warn_bytes knob (%s). %d scheduled "
                "invocation(s) carry their inputs INLINE: %s. A row this size "
                "is one database hiccup away from failing the run; move large "
                "fan-out payloads to storage and keep a reference.",
                checkpoint.checkpoint_id[:8],
                checkpoint.run_id[:8],
                checkpoint.step,
                f"{payload_bytes:,}",
                f"{policy.warn_bytes:,}",
                len(next_invocations),
                ", ".join(
                    sorted({str(ni.get("node_id") or "?") for ni in next_invocations})[:10]
                ),
            )

        attempts = 0
        while True:
            try:
                await self._write_checkpoint_once(
                    checkpoint,
                    columns=columns,
                    values=values,
                    policy=policy,
                    outcomes=_outcomes or (),
                    earlier=earlier,
                )
                if attempts:
                    logger.warning(
                        "[checkpoint-retry] HEALED on attempt %d — run %s step %s saved.",
                        attempts + 1,
                        checkpoint.run_id[:8],
                        checkpoint.step,
                    )
                return
            except BaseException as exc:  # noqa: BLE001 — classified immediately below
                if not _is_retryable_write_failure(exc):
                    raise
                # The write is idempotent BY ID, so ambiguity is decidable: if
                # the row is there, the attempt asyncpg gave up on had already
                # committed. Asked on EVERY failure, including the first — a
                # command_timeout means the client stopped waiting, not that
                # Postgres stopped working, so a blind re-issue is exactly the
                # duplicate-key hazard matrx-orm's write path refuses to take.
                # One indexed read on a failure path is nothing.
                if await self._checkpoint_landed(checkpoint):
                    logger.warning(
                        "[checkpoint-retry] run %s step %s: the timed-out attempt had "
                        "already committed — row %s is present, continuing.",
                        checkpoint.run_id[:8],
                        checkpoint.step,
                        checkpoint.checkpoint_id[:8],
                    )
                    return
                if attempts >= policy.max_retries:
                    raise CheckpointWriteFailedError(
                        run_id=checkpoint.run_id,
                        checkpoint_id=checkpoint.checkpoint_id,
                        step=checkpoint.step,
                        payload_bytes=payload_bytes,
                        attempts=attempts + 1,
                        original_error=exc,
                    ) from exc
                backoff = policy.backoff_seconds(attempts)
                logger.warning(
                    "[checkpoint-retry] attempt %d/%d failed to save run %s step %s "
                    "(%s: %s) — %s bytes, re-issuing in %.3fs. The INSERT is keyed by "
                    "checkpoint id, so a re-issue is exactly-once.",
                    attempts + 1,
                    1 + policy.max_retries,
                    checkpoint.run_id[:8],
                    checkpoint.step,
                    type(exc).__name__,
                    str(exc)[:200],
                    f"{payload_bytes:,}",
                    backoff,
                )
                await asyncio.sleep(backoff)
                attempts += 1

    async def _write_checkpoint_once(
        self,
        checkpoint: Checkpoint,
        *,
        columns: dict[str, Any],
        values: dict[str, Any],
        policy: CheckpointWritePolicy,
        outcomes: Sequence[_PreparedOutcome] = (),
        earlier: Sequence[tuple[Checkpoint, dict[str, Any], dict[str, Any], Sequence[_PreparedOutcome]]] = (),
    ) -> None:

        if earlier:
            # A chain of pure steps (``save_checkpoint_chain``): every row of every step in one
            # transaction, in step order; the run row is pointed once, at the last checkpoint.
            all_outcomes = [o for *_rest, outs in earlier for o in outs] + list(outcomes)
            merged_values: dict[str, Any] = {}
            for _cp, _cols, vals, _outs in earlier:
                merged_values.update(vals)
            merged_values.update(values)
            await self._write_rows(
                [(cp, cols) for cp, cols, _vals, _outs in earlier] + [(checkpoint, columns)],
                values=merged_values,
                policy=policy,
                outcomes=all_outcomes,
            )
            return
        await self._write_rows([(checkpoint, columns)], values=values, policy=policy, outcomes=outcomes)

    async def _write_rows(
        self,
        checkpoints: Sequence[tuple[Checkpoint, dict[str, Any]]],
        *,
        values: dict[str, Any],
        policy: CheckpointWritePolicy,
        outcomes: Sequence[_PreparedOutcome] = (),
    ) -> None:
        from matrx_orm import transaction

        checkpoint = checkpoints[-1][0]
        wf_checkpoint = get_model("WfCheckpoint")
        # workflow.checkpoint.organization_id is NOT NULL. A checkpoint is a
        # CHILD of its run — carry the parent's organization; see
        # _organization_for_run().
        organization_id = await _organization_for_run(checkpoint.run_id)
        stored = _stored_value_hashes.setdefault(checkpoint.run_id, set())
        outcome_values: dict[str, Any] = {}
        for prepared in outcomes:
            outcome_values.update(prepared.fresh)
        # A value an outcome of this same transaction stores (a step's output is the next
        # step's scheduled input) is written once, by the outcome's write.
        fresh = {h: v for h, v in values.items() if h not in stored and h not in outcome_values}
        written: list[str] = []
        async with transaction():
            # The outcomes' new values and the checkpoint's land in ONE insert, and the outcome
            # rows in one upsert per column shape (L-SPEED 6c part 2): a save was a statement per
            # outcome plus two value inserts, each a pooled round trip on the step's path.
            if outcome_values or fresh:
                from matrx_graph.checkpoint import value_store

                written = list(
                    await value_store.store_run_values(
                        checkpoint.run_id,
                        {**outcome_values, **fresh},
                        organization_id=organization_id,
                        remember=False,
                    )
                    or ()
                )
            await _write_outcomes_together(outcomes)

            def _checkpoint_row(row_checkpoint: Checkpoint, columns: dict[str, Any]) -> dict[str, Any]:
                return {
                    "id": row_checkpoint.checkpoint_id,
                    "run_id": row_checkpoint.run_id,
                    "organization_id": organization_id,
                    "thread_id": row_checkpoint.thread_id,
                    "parent_checkpoint_id": row_checkpoint.parent_checkpoint_id,
                    "step": row_checkpoint.step,
                    "channel_values": columns["channel_values"],
                    "pending_bindings": columns["pending_bindings"],
                    "next_invocations": columns["next_invocations"],
                    "interrupt_payload": columns["interrupt_payload"],
                    # Hole H4: the kind-subscription matcher's state rides the
                    # existing metadata column (absent key = nothing to carry).
                    "metadata": (
                        {"subscription_state": row_checkpoint.subscription_state}
                        if row_checkpoint.subscription_state
                        else {}
                    ),
                    "created_at": row_checkpoint.created_at,
                }

            if len(checkpoints) > 1:
                # A CHAIN's checkpoints land in ONE statement (L-SPEED round 6a, item 3b), not one INSERT
                # each. Ids are fresh; a retried chain re-sends the same ids, so a row already there is
                # skipped (the chain is idempotent by its last id, ``_checkpoint_landed``).
                await wf_checkpoint.bulk_insert_ignore(
                    [_checkpoint_row(cp_, cols_) for cp_, cols_ in checkpoints],
                    on_conflict=["id"],
                    statement_timeout=policy.statement_timeout_seconds,
                )
            else:
                # Only the id comes back: create() would read the whole row back over
                # the wire, decode it, and keep it in the ORM's process cache.
                for row_checkpoint, columns in checkpoints:
                    await wf_checkpoint.insert_returning(
                        _checkpoint_row(row_checkpoint, columns),
                        returning=["id"],
                        statement_timeout=policy.statement_timeout_seconds,
                    )
            # Only the id and the status come back — never the whole run row
            # (run_store.RUN_UPDATE_RETURNS). The status is read by this same
            # statement, under its row lock, so the scheduler's pause/cancel poll at
            # the boundary that follows needs no read of its own (pop_run_status).
            # ``steps_executed`` rides the same statement: the run's live progress lands with its
            # checkpoint, so the host's event writer no longer writes the run row a second time
            # for it (in its own transaction, contending for this row's lock).
            pointed = await (
                get_model("WfRun")
                .filter(id=checkpoint.run_id)
                .returning("id", "status")
                .update(last_checkpoint_id=checkpoint.checkpoint_id, steps_executed=checkpoint.step + 1)
            )
        _remember_run_status(checkpoint.run_id, pointed)
        if written:
            from matrx_graph.checkpoint import value_store

            # Remembered only now, COMMITTED (the record_outcome rule).
            value_store.remember_stored_values(checkpoint.run_id, written)
        stored.update(fresh)
        if len(_stored_value_hashes) > _STORED_HASH_RUNS:
            _stored_value_hashes.pop(next(iter(_stored_value_hashes)))

    def pop_run_status(self, run_id: str) -> str | None:
        """The run's status as the last checkpoint save of ``run_id`` read it — once.

        ``None`` when no save in this process read it (or it was already taken); the
        caller then reads the status itself."""
        return _RUN_STATUS_AT_SAVE.pop(str(run_id), None)

    async def _checkpoint_landed(self, checkpoint: Checkpoint) -> bool:
        """Whether the row is already there — the idempotency proof for a retry.

        Also (re)points ``workflow.run.last_checkpoint_id``, which is itself
        idempotent: the failed attempt may have committed the INSERT and lost the
        UPDATE, or the whole transaction may have rolled back.
        """
        try:
            rows = await get_model("WfCheckpoint").filter(id=checkpoint.checkpoint_id).values("id")
            if not rows:
                return False
            # Only the id comes back — never the whole run row (run_store.RUN_UPDATE_RETURNS).
            await (
                get_model("WfRun")
                .filter(id=checkpoint.run_id)
                .returning("id")
                .update(last_checkpoint_id=checkpoint.checkpoint_id)
            )
            return True
        except Exception:  # noqa: BLE001 — the probe must never mask the write failure
            logger.warning(
                "checkpoint %s: could not verify whether the timed-out write landed; "
                "treating it as not written.",
                checkpoint.checkpoint_id[:8],
                exc_info=True,
            )
            return False

    @_scoped_read
    async def load_checkpoint(self, checkpoint_id: str) -> Checkpoint | None:
        rows = await get_model("WfCheckpoint").filter(id=checkpoint_id).values(*_CHECKPOINT_COLUMNS)
        if not rows:
            return None
        return (await _rows_to_checkpoints(rows))[0]

    @_scoped_read
    async def latest_checkpoint(self, run_id: str) -> Checkpoint | None:
        rows = await (
            get_model("WfCheckpoint")
            .filter(run_id=run_id)
            .order_by("-step", "-created_at")
            .limit(1)
            .values(*_CHECKPOINT_COLUMNS)
        )
        if not rows:
            return None
        return (await _rows_to_checkpoints(rows))[0]

    @_scoped_read
    async def list_checkpoints(self, run_id: str) -> list[Checkpoint]:
        rows = await (
            get_model("WfCheckpoint")
            .filter(run_id=run_id)
            .order_by("step", "created_at")
            .values(*_CHECKPOINT_COLUMNS)
        )
        return await _rows_to_checkpoints(rows)

    async def list_checkpoint_summaries(
        self,
        run_id: str,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], bool]:
        """Page checkpoint metadata without loading durable channel state.

        External control surfaces need lineage/frontier summaries, not the
        potentially very large ``channel_values`` and ``pending_bindings``
        blobs. The query is bounded in Postgres and fetches one sentinel row
        so callers can expose ``has_more`` without a separate count query.
        """
        if limit < 1:
            raise ValueError("limit must be at least 1")
        if offset < 0:
            raise ValueError("offset must be non-negative")
        async with _read_scope(self, "list_checkpoint_summaries", run_id, None):
            rows = await (
                get_model("WfCheckpoint")
                .filter(run_id=run_id)
                .order_by("-step", "-created_at")
                .limit(limit + 1)
                .offset(offset)
                .values(
                    "id",
                    "parent_checkpoint_id",
                    "step",
                    "next_invocations",
                    "interrupt_payload",
                )
            )
        shown = rows[:limit]
        return (
            [
                {
                    "checkpoint_id": str(row["id"]),
                    "parent_checkpoint_id": (
                        str(row["parent_checkpoint_id"]) if row["parent_checkpoint_id"] else None
                    ),
                    "step": row["step"],
                    "scheduled_node_ids": [
                        str(invocation.get("node_id") or "")
                        for invocation in (_coerce_json(row["next_invocations"]) or [])[:100]
                    ],
                    "interrupt_payload": _coerce_json(row["interrupt_payload"]),
                }
                for row in shown
            ],
            len(rows) > limit,
        )

    async def record_outcome(self, outcome: NodeOutcome) -> None:
        """Land one outcome row; a lock collision Postgres broke is re-run whole, never raised on the
        first refusal.

        The row is an upsert keyed by the outcome's correlation key, so re-running it is safe. A
        declared host context sends every write inside its own ``transaction()``, where matrx-orm
        never re-runs a canceled statement itself — so before 2026-11-01 the first ``55P03`` here
        escaped into the step and parked a whole 5,000-item drain on one item's write (run
        188426a6). The re-run uses matrx-orm's ONE transient-retry primitive on the database's own
        ``orm.write_retry`` knobs, and costs nothing until a write is refused."""
        try:
            await self._record_outcome_once(outcome)
        except Exception as exc:
            if persistence_cause_for_exception(exc) != Cause.DATABASE_BUSY:
                raise
            # Imported only on a lock refusal: no other path touches it.
            from matrx_orm import LockContentionError, retry_on_transient

            if not isinstance(exc, LockContentionError):
                raise
            await retry_on_transient(
                lambda: self._record_outcome_once(outcome),
                retry_on=(LockContentionError,),
                label=f"workflow outcome {outcome.run_id[:8]} {outcome.node_id}#{outcome.item_index}",
                policy_db=_outcome_database(),
            )

    async def _record_outcome_once(self, outcome: NodeOutcome) -> None:
        prepared = await _prepare_outcome(outcome)
        if not prepared.fresh:
            await prepared.write(prepared.row)
            return
        from matrx_graph.checkpoint import value_store

        try:
            async with _outcome_transaction():
                written = await value_store.store_run_values(
                    outcome.run_id, prepared.fresh, organization_id=prepared.organization_id, remember=False
                )
                await prepared.write(prepared.row)
            # Remembered only now, COMMITTED: a concurrent sibling (fan-out) with the same value
            # must write it itself until then, never a reference to an uncommitted value.
            value_store.remember_stored_values(outcome.run_id, written)
            return
        except Exception:  # noqa: BLE001 — the outcome must still land
            # The transaction rolled back: nothing was remembered, so write the row whole.
            logger.exception(
                "[wf:%s] outcome value store write FAILED (node=%s) — outcome stored INLINE",
                outcome.run_id[:8],
                outcome.node_id,
            )
        await prepared.write(prepared.inline_row())

    async def save_checkpoint_with_outcomes(
        self, checkpoint: Checkpoint, outcomes: list[NodeOutcome]
    ) -> None:
        """Save ``checkpoint`` and land ``outcomes`` in the SAME transaction.

        One BEGIN / COMMIT for a whole super-step of pure steps instead of one per
        outcome plus one for the checkpoint (each transaction is three round trips
        before its first row: 2026-10-29, a pure step cost ~9 round trips, ~63 ms).
        The outcomes and the checkpoint commit together or not at all, so a reader
        never sees a checkpoint whose step's outcomes are missing. Raises like
        ``save_checkpoint``; the caller then writes each outcome on its own."""
        # One memo for the outcomes saved together: a step's output is the next step's input,
        # so each is walked and hashed once per save (InternMemo, the outcome limit).
        memo = InternMemo()
        prepared = [await _prepare_outcome(o, memo) for o in outcomes]
        await self.save_checkpoint(checkpoint, _outcomes=prepared)

    async def save_checkpoint_chain(self, items: list[tuple[Checkpoint, list[NodeOutcome]]]) -> None:
        """Save a CHAIN of pure steps' checkpoints, each with its outcomes, in ONE transaction.

        One row per step, exactly as one save per step would write them (Re-run from, Fork from,
        the timeline and step mode keep every checkpoint), but one BEGIN / COMMIT and one run
        pointer update for the chain: a pure step paid ~8 round trips for its own save
        (PF-WF 2026-11-02, 88 ms of a 110 ms step). Raises like ``save_checkpoint``; retried as
        a unit (idempotent by the LAST checkpoint's id, which lands only with all of them)."""
        if not items:
            return
        memo = InternMemo()  # the chain's outcomes: each output hashed once (save_checkpoint_with_outcomes)
        prepared = [(cp, [await _prepare_outcome(o, memo) for o in outs]) for cp, outs in items]
        last_cp, last_outcomes = prepared[-1]
        await self.save_checkpoint(last_cp, _outcomes=last_outcomes, _earlier=prepared[:-1])

    @_scoped_read
    async def step_history(self, run_id: str) -> tuple[set[str], dict[str, dict[str, str]]]:
        """Succeeded and failed steps of ``run_id`` across every leg, from ``workflow.node_outcome``
        (``step_history_from_outcomes``) — read by the run-end result check on a resumed run."""
        from matrx_graph.checkpoint.protocol import step_history_from_outcomes

        rows = await get_model("WfNodeOutcome").filter(run_id=run_id).values("node_id", "error")
        return step_history_from_outcomes(
            [(str(r["node_id"]), _coerce_json(r["error"])) for r in rows]
        )

    async def settled_outputs(
        self, run_id: str, node_ids: set[str], up_to_step: int | None = None
    ) -> dict[str, Any]:
        """``{step id: output}`` of each of ``node_ids``' latest successful outcome in ``run_id`` at or
        before ``up_to_step``, across every leg, from ``workflow.node_outcome``
        (``latest_settled_keys``). Two reads: the keys, then the chosen rows' outputs; outputs kept in
        the run's value store come back whole. Only a resumed leg's completion calls it, for the
        steps that leg did not run."""
        if not node_ids:
            return {}
        async with _read_scope(self, "settled_outputs", run_id, None):
            filters: dict[str, Any] = {"run_id": run_id, "node_id__in": sorted(node_ids)}
            if up_to_step is not None:
                filters["step__lte"] = up_to_step
            rows = await (
                get_model("WfNodeOutcome")
                .filter(**filters)
                .values("id", "node_id", "step", "dispatch_id", "item_index", "attempt", "error")
            )
            row_ids: dict[tuple[str, tuple[int, str, int, int]], Any] = {}
            outcomes = []
            for r in rows:
                key = (int(r["step"]), str(r["dispatch_id"] or ""), int(r["item_index"] or 0), int(r["attempt"]))
                row_ids[(str(r["node_id"]), key)] = r["id"]
                outcomes.append((str(r["node_id"]), key, _coerce_json(r["error"])))
            chosen = [row_ids[(nid, key)] for nid, key in latest_settled_keys(outcomes, node_ids, up_to_step).items()]
            if not chosen:
                return {}
            rows = list(await get_model("WfNodeOutcome").filter(id__in=chosen).values("node_id", "output"))
            # Decoding and walking every chosen output for references runs off the loop when they are
            # large (event_loop_stall cdbb1070: 1.14 s here on a resume), like the checkpoint rows.
            decoded = await run_pure_off_loop(_decode_settled_outputs, rows)
            out: dict[str, Any] = {}
            for node_id, output, has_refs in decoded:
                if has_refs:
                    from matrx_graph.checkpoint.value_store import resolve_run_values

                    output = await resolve_run_values(run_id, output)
                out[node_id] = output
            return out

    @_scoped_read
    async def item_outcomes(
        self, run_id: str, node_id: str, dispatch_id: str, *, step: int | None = None
    ) -> dict[int, str]:
        """``{item_index: outcome}`` of ``node_id``'s items in ``dispatch_id`` — at ``step`` only when
        given (one pass of a dispatch a cycle runs again) — one read (``item_outcomes_from_rows``):
        a resumed leg's item counts (matrx_graph/says.py)."""
        from matrx_graph.checkpoint.protocol import item_outcomes_from_rows

        filters: dict[str, Any] = {"run_id": run_id, "node_id": node_id, "dispatch_id": dispatch_id}
        if step is not None:
            filters["step"] = step
        rows = await (
            get_model("WfNodeOutcome")
            .filter(**filters)
            .values("item_index", "error", "source")
        )
        return item_outcomes_from_rows([
            (int(r["item_index"] or 0), _coerce_json(r["error"]), r["source"]) for r in rows
        ])

    @_scoped_read
    async def outcome_keys(self, run_id: str, dispatch_prefix: str) -> list[tuple[int, str, str, int, int]]:
        """``(step, node_id, dispatch_id, item_index, attempt)`` of ``run_id``'s outcomes whose dispatch id
        starts with ``dispatch_prefix`` — one read: an inline child's recorded steps (``nodes/subgraph/inline.py``)."""
        rows = await (
            get_model("WfNodeOutcome")
            .filter(run_id=run_id, dispatch_id__startswith=dispatch_prefix)
            .values("step", "node_id", "dispatch_id", "item_index", "attempt")
        )
        return [
            (int(r["step"]), str(r["node_id"]), str(r["dispatch_id"] or ""), int(r["item_index"] or 0), int(r["attempt"]))
            for r in rows
        ]

    @_scoped_read
    async def get_outcome(
        self,
        run_id: str,
        step: int,
        node_id: str,
        attempt: int,
        dispatch_id: str = "",
        item_index: int = 0,
    ) -> NodeOutcome | None:
        rows = await (
            get_model("WfNodeOutcome")
            .filter(
                run_id=run_id,
                step=step,
                node_id=node_id,
                attempt=attempt,
                dispatch_id=dispatch_id,
                item_index=item_index,
            )
            .values(*_outcome_columns())
        )
        if not rows:
            return None
        outcome = _row_to_outcome(rows[0])
        # Inputs (MKT-170) and output (MKT-171) go to the run's value store by reference; rows written
        # before that hold them inline and pass through untouched. NodeOutcome is frozen: copy, don't assign.
        from matrx_graph.checkpoint.value_store import resolve_run_values

        resolved: dict[str, Any] = {}
        if outcome.inputs is not None and referenced_hashes(outcome.inputs):
            resolved["inputs"] = await resolve_run_values(run_id, outcome.inputs)
        if referenced_hashes(outcome.output):
            resolved["output"] = await resolve_run_values(run_id, outcome.output)
        if resolved:
            outcome = outcome.model_copy(update=resolved)
        return outcome


async def _prepare_outcome(outcome: NodeOutcome, memo: InternMemo | None = None) -> _PreparedOutcome:
    """The node_outcome row for ``outcome``, its new by-reference values, and its inline form.

    ``memo``: shared by the outcomes one save writes together (their ``fresh`` values are written
    together too, so a value hashed for an earlier outcome is not hashed again)."""
    # workflow.node_outcome.organization_id is NOT NULL. A node outcome
    # is a CHILD of its run — carry the parent's organization; see
    # _organization_for_run(). Deliberately NOT in update_fields below:
    # a conflict (re-run of the same dispatch/attempt) never reassigns
    # the row's organization.
    organization_id = await _organization_for_run(outcome.run_id)
    available = _available_versioned_kind_columns()
    extra_payload = {col: getattr(outcome, col) for col in available}
    extra_update = list(available)
    # C-30: the input envelope rides the SAME upsert as the output, because
    # both halves describe one occurrence at one correlation key. The
    # NodeOutcome field is `inputs` (plural — it is a mapping of arguments);
    # the column is `input` (singular — it is one envelope). Mapped here,
    # once, rather than renaming either side to match the other.
    # The large input/output values and the outcome row land in ONE transaction
    # (one BEGIN, one COMMIT) instead of a transaction per value batch plus one
    # for the row: the values are split off here and written beside the upsert.
    fresh: dict[str, Any] = {}
    inline_payload: dict[str, Any] = {}
    for col in _available_input_envelope_columns():
        value = outcome.inputs if col == "input" else outcome.input_kind
        if col == "input":
            inline_payload[col] = value
            value = await _split_outcome_value(outcome.run_id, value, "input", fresh, memo)
        extra_payload[col] = value
        extra_update.append(col)
    if outcome.metadata:
        # Only when there is something to say — an empty write must never
        # clobber metadata another writer put on the row.
        extra_payload["metadata"] = outcome.metadata
        extra_update.append("metadata")
    inline_payload["output"] = outcome.output
    output_value = await _split_outcome_value(outcome.run_id, outcome.output, "output", fresh, memo)
    row = {
            **extra_payload,
            "run_id": outcome.run_id,
            "organization_id": organization_id,
            "step": outcome.step,
            "node_id": outcome.node_id,
            "attempt": outcome.attempt,
            "dispatch_id": outcome.dispatch_id,
            "item_index": outcome.item_index,
            "output": output_value,
            "channel_writes": outcome.channel_writes,
            "sends": [s.model_dump(mode="json") for s in outcome.sends],
            "emissions": outcome.emissions,
            "duration_ms": outcome.duration_ms,
            # Client-rendered (Studio node inspector, checkpoint preview):
            # never a terminal banner, SQL, or bound args.
            "error": client_safe_error_payload(outcome.error),
            "source": outcome.source,
            "completed_at": outcome.completed_at,
            "output_kind": outcome.output_kind,
            "output_kind_ok": outcome.output_kind_ok,
            "output_kind_errors": outcome.output_kind_errors,
    }
    update_fields = [
        "output",
        "channel_writes",
        "sends",
        "emissions",
        "duration_ms",
        "error",
        "source",
        "completed_at",
        "output_kind",
        "output_kind_ok",
        "output_kind_errors",
        *extra_update,
    ]
    return _PreparedOutcome(
        run_id=outcome.run_id,
        organization_id=organization_id,
        row=row,
        update_fields=update_fields,
        fresh=fresh,
        inline_payload=inline_payload,
    )


#: The unique key of a ``workflow.node_outcome`` row (its upsert's conflict target).
_OUTCOME_KEY = ("run_id", "step", "node_id", "dispatch_id", "item_index", "attempt")


async def _write_outcomes_together(outcomes: Sequence[_PreparedOutcome]) -> None:
    """Land ``outcomes`` (inside the caller's transaction) in one upsert per column shape — the rows of
    one save share their columns, so that is one statement — with EXACTLY the single upsert's result.

    Review 6h (I3): the bulk statement used to write ``COALESCE(EXCLUDED.col, stored)`` for a column a
    row left empty, so a clean re-write at an existing key KEPT the stale ``error`` / ``output_kind_errors``
    the single upsert clears. Now every nullable column with no default that a row supplies as ``None``
    is written as NULL (``clear_when_empty``) — what the single upsert's ``EXCLUDED`` gives — and a column
    with a default is left out (its ``EXCLUDED`` is the default either way). A key that appears more than
    once lands one outcome at a time, in order, so the last write wins exactly as it does alone."""
    if not outcomes:
        return
    keys = [tuple(p.row.get(k) for k in _OUTCOME_KEY) for p in outcomes]
    if len(outcomes) == 1 or len(set(keys)) < len(keys):
        for prepared in outcomes:
            await prepared.write(prepared.row)
        return
    model = get_model("WfNodeOutcome")
    fields = getattr(model, "_fields", {}) or {}
    # A row's None in a column with a default means "leave it out" (the INSERT takes the default), as the
    # single upsert does, so rows group by the columns they supply: every statement's rows supply the same.
    shapes: dict[tuple[tuple[str, ...], tuple[str, ...]], list[_PreparedOutcome]] = {}
    for prepared in outcomes:
        supplied = tuple(sorted(k for k, v in prepared.row.items() if v is not None))
        shapes.setdefault((supplied, tuple(prepared.update_fields)), []).append(prepared)
    for (_columns, update_fields), group in shapes.items():
        await model.bulk_upsert(
            [{**p.row, "organization_id": p.organization_id} for p in group],
            on_conflict=list(_OUTCOME_KEY),
            returning=["id"],
            update_fields=list(update_fields),
            clear_when_empty=[f for f in update_fields if _empty_is_null(fields.get(f))],
        )


def _empty_is_null(field: Any) -> bool:
    """True when the single upsert's ``EXCLUDED`` for a ``None`` in this column is NULL: nullable, no default."""
    return field is not None and bool(getattr(field, "nullable", False)) and getattr(field, "default", None) is None


@dataclass
class _PreparedOutcome:
    """One outcome ready to write: ``row`` carries references to ``fresh`` values (stored with it)."""

    run_id: str
    organization_id: str
    row: dict[str, Any]
    update_fields: list[str]
    fresh: dict[str, Any]
    inline_payload: dict[str, Any]

    def inline_row(self) -> dict[str, Any]:
        """The row with every value inline — the fallback when the value store write failed."""
        return {**self.row, **{k: v for k, v in self.inline_payload.items() if k in self.row}}

    async def write(self, values: dict[str, Any]) -> None:
        """Land ``values`` as the outcome row. The run's organization rides every write
        (workflow.node_outcome.organization_id is NOT NULL; a child of its run)."""
        await get_model("WfNodeOutcome").upsert(
            {**values, "organization_id": self.organization_id},
            on_conflict=["run_id", "step", "node_id", "dispatch_id", "item_index", "attempt"],
            # Only the id comes back (MKT-111): an outcome carries the step's
            # whole output and input, and RETURNING * read them back over the
            # wire, decoded them, and cached the row in the ORM.
            returning=["id"],
            update_fields=self.update_fields,
        )


async def _split_outcome_value(
    run_id: str, value: Any, column: str, fresh: dict[str, Any], memo: InternMemo | None = None
) -> Any:
    """The outcome's ``input`` or ``output`` with large values by reference (MKT-170/171).

    The values this run has not stored yet are added to ``fresh``; ``record_outcome``
    writes them in the same transaction as the row. Never raises: if splitting fails
    the value is stored whole (loud)."""
    if value is None or not _value_store_available():
        return value
    try:
        from matrx_graph.knobs import event_inline_value_max_bytes

        limit = await event_inline_value_max_bytes()
        if memo is None:
            memo = InternMemo()
        if memo.committed is None:
            memo.committed = _stored_value_hashes.get(run_id) or frozenset()
        out, values = await run_pure_off_loop(outcome_input_row, value, limit, memo, values=(value,))
        stored = _stored_value_hashes.get(run_id, set())
        fresh.update({h: v for h, v in values.items() if h not in stored})
        return out
    except Exception:  # noqa: BLE001 — the outcome must still land
        logger.exception("[wf:%s] outcome %s value split FAILED — stored INLINE", run_id[:8], column)
        return value


def _outcome_database() -> str:
    """The database ``workflow.node_outcome`` lives in — whose ``orm.write_retry`` knobs pace a re-run."""
    return get_model("WfNodeOutcome").get_database_name()


def _outcome_transaction() -> Any:
    """The transaction an outcome row and its new values share (a seam for tests)."""
    from matrx_orm import transaction

    return transaction()


def _decode_settled_outputs(rows: list[dict[str, Any]]) -> list[tuple[str, Any, bool]]:
    """``(step id, output, carries references)`` for each row with an output — pure."""
    out: list[tuple[str, Any, bool]] = []
    for r in rows:
        output = _coerce_json(r["output"])
        if output is not None:
            out.append((str(r["node_id"]), output, bool(referenced_hashes(output))))
    return out


def _coerce_json(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        return json.loads(value)
    return value


_value_store_screamed = False


def _value_store_available() -> bool:
    """Whether the host registered ``WfCheckpointValue`` (workflow.checkpoint_value).

    Capability-gated like the input-envelope columns: a standalone install
    against an older schema keeps writing checkpoints inline — loud once. Asked
    on every save (a registry lookup), so a call before ``configure_db`` can
    never switch the capability off for the life of the process."""
    global _value_store_screamed
    try:
        get_model("WfCheckpointValue")
        return True
    except Exception:  # noqa: BLE001 — absent model = capability off
        if not _value_store_screamed:
            _value_store_screamed = True
            logger.error(
                "workflow.checkpoint_value is not registered (WfCheckpointValue) — "
                "checkpoints store every value INLINE, so a wide fan-in repeats its "
                "payloads per edge and per step (MKT-111). Apply matrx-graph migration "
                "0115 and regenerate models to activate by-reference values."
            )
        return False


#: Per process: which value hashes this process already stored for a run, so a
#: later checkpoint of the same run sends only its NEW values. Bounded to the
#: most recent runs; a forgotten run only costs a skipped duplicate insert.
_stored_value_hashes: dict[str, set[str]] = {}
_STORED_HASH_RUNS = 256


_VALUE_COLUMNS = ("channel_values", "pending_bindings", "next_invocations", "interrupt_payload")


def _decode_checkpoint_rows(rows: list[Any]) -> tuple[list[dict[str, Any]], dict[str, set[str]]]:
    """Decode each row's value columns and collect the value hashes they reference (pure CPU)."""
    decoded = []
    wanted: dict[str, set[str]] = {}
    for row in rows:
        row = dict(row)
        for col in _VALUE_COLUMNS:
            row[col] = _coerce_json(row[col])
            refs = referenced_hashes(row[col])
            if refs:
                wanted.setdefault(str(row["run_id"]), set()).update(refs)
        decoded.append(row)
    return decoded, wanted


def _finish_checkpoint_rows(decoded: list[dict[str, Any]], store: dict[str, Any] | None) -> list[Checkpoint]:
    """Resolve every by-reference value and build the Checkpoints (pure CPU)."""
    if store is not None:
        for row in decoded:
            for col in _VALUE_COLUMNS:
                row[col] = resolve_values(row[col], store)
    return [_row_to_checkpoint(r) for r in decoded]


async def _rows_to_checkpoints(rows: list[Any]) -> list[Checkpoint]:
    """Checkpoint rows → Checkpoints, every by-reference value resolved (MKT-111).

    Decoding, resolving and model-building walk every value of every checkpoint of the run (pure CPU):
    for a large checkpoint they run in a worker thread (``run_pure_off_loop``), never on the loop. Live 2026-11-07 (event_loop_stall 8fa91a5b): a resume's
    ``list_checkpoints`` held the workflow worker's loop 3 s inside ``resolve_values``.
    """
    rows = [dict(row) for row in rows]
    decoded, wanted = await run_pure_off_loop(_decode_checkpoint_rows, rows)
    store: dict[str, Any] | None = None
    if wanted:
        from matrx_graph.checkpoint.value_store import fetch_stored_values

        store = {}
        for run_id, hashes in wanted.items():
            pending = set(hashes)
            while pending:  # stored values may themselves reference others
                # This run's store, then the runs it called (a called workflow's answer stays there).
                found = await fetch_stored_values(run_id, pending)
                if not found:
                    break
                fresh: set[str] = set()
                for digest, value in found.items():
                    # Decoded by the jsonb codec; a long STRING value is a str here, never JSON text.
                    store[digest] = value
                    fresh |= referenced_hashes(value)
                pending = fresh - set(store)
    return await run_pure_off_loop(_finish_checkpoint_rows, decoded, store)


def _row_to_checkpoint(row: Any) -> Checkpoint:
    raw_next = _coerce_json(row["next_invocations"]) or []
    next_invs = [NextInvocation.model_validate(n) for n in raw_next]
    raw_bindings = _coerce_json(row["pending_bindings"]) or {}
    bindings = {
        node_id: PendingBinding.model_validate(binding) for node_id, binding in raw_bindings.items()
    }
    return Checkpoint(
        checkpoint_id=str(row["id"]),
        run_id=str(row["run_id"]),
        thread_id=str(row["thread_id"]),
        parent_checkpoint_id=str(row["parent_checkpoint_id"])
        if row["parent_checkpoint_id"]
        else None,
        step=row["step"],
        channel_values=_coerce_json(row["channel_values"]) or {},
        pending_bindings=bindings,
        next_invocations=next_invs,
        interrupt_payload=_coerce_json(row["interrupt_payload"]),
        subscription_state=(_coerce_json(row.get("metadata")) or {}).get("subscription_state") or {},
        created_at=row["created_at"],
    )


def _row_to_outcome(row: Any) -> NodeOutcome:
    raw_sends = _coerce_json(row["sends"]) or []
    raw_writes = _coerce_json(row["channel_writes"]) or []
    writes = [tuple(p) if isinstance(p, list) else p for p in raw_writes]
    # `source` is in 0008+ schemas; default to 'executor' for rows written
    # before the migration landed (with a non-null column default the row
    # should always carry it).
    source = row.get("source") or "executor"
    return NodeOutcome(
        run_id=str(row["run_id"]),
        step=row["step"],
        node_id=row["node_id"],
        attempt=row["attempt"],
        # Correlation identity + emissions are in 0023+ schemas; default for
        # rows fetched from a pre-migration table (dev/test bootstraps).
        dispatch_id=row.get("dispatch_id") or "",
        item_index=row.get("item_index") or 0,
        output=_coerce_json(row["output"]) or {},
        # C-30. `None` when the column is absent (older schema) or the row
        # predates capture — deliberately NOT coerced to {}, because "we never
        # recorded the inputs" and "the node was called with no arguments" are
        # different facts and a replay must not confuse them.
        inputs=_coerce_json(row.get("input")),
        input_kind=row.get("input_kind"),
        channel_writes=writes,
        sends=[Send.model_validate(s) for s in raw_sends],
        emissions=_coerce_json(row.get("emissions")) or {},
        duration_ms=row["duration_ms"],
        error=_coerce_json(row["error"]),
        source=source,
        completed_at=row["completed_at"],
        output_kind=row.get("output_kind"),
        output_kind_ok=row.get("output_kind_ok"),
        output_kind_errors=_coerce_json(row.get("output_kind_errors")),
        # Versioned kind-verdict refs — present only once the A3 DDL lands
        # (capability-gated columns; see _has_versioned_kind_columns).
        output_kind_version=row.get("output_kind_version"),
        output_kind_degraded=row.get("output_kind_degraded"),
    )
