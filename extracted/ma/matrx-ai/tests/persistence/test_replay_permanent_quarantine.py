"""A permanently refused write is quarantined on sight, never re-attempted.

SUT: :func:`matrx_ai.persistence.replay.replay_pending` in auto mode
(``max_attempts`` set) and the two classifiers it leans on.

Live evidence (2026-09-12): eight ``chat.message`` rows whose ``created_by``
named a user that does not exist were spilled to disk, drained back with the
``DiskSpillRecovered`` marker (RECOVERABLE) plus ``capture_actor_missing=``,
and then attempted five times each — the ``_stamp_org_default`` trigger raised
``P0001`` on every attempt and every attempt landed its own
``persistence_replay_failed`` system_error row.

Breaks these tests name:
* the permanent-signature list loses the trigger / constraint / drift classes
  (or the deleted-actor stamp) — a refused row burns the attempt budget again;
* a recoverable marker is allowed to outrank the wrapped permanent error;
* a permanent row is attempted anyway (``execute_tiers`` reached);
* the quarantine stops pinning ``retry_count`` at the cap, so the auto loop and
  the watchdog pick the row up again next minute;
* a live permanent refusal during execute is treated as a transient (bumped,
  not quarantined), or its capture kind drifts from ``persistence_replay_quarantined``;
* a human's explicit retry (``max_attempts=None``) is refused — that path must
  still attempt, because a person asked.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest
from matrx_orm.exceptions import QueryTimeoutError
from matrx_orm.session.fallback import (
    DIRECT_WRITE_PRESERVED_MARKER,
    DISK_SPILL_RECOVERED_MARKER,
    IMMUTABLE_WRITE_PRESERVED_MARKER,
)

from matrx_ai.persistence import replay

_TRIGGER_REFUSAL = (
    f"{DISK_SPILL_RECOVERED_MARKER}: asyncpg.exceptions.RaiseError: "
    "stamp_actor: user e4687a9c-acf7-469f-aa12-860eb4d948d0 "
    "does not exist [SQLSTATE P0001] "
    "[capture_actor_missing=e4687a9c-acf7-469f-aa12-860eb4d948d0]"
)


def _row(row_id: str, error_text: str, *, retry_count: int = 0) -> dict[str, Any]:
    return {
        "id": row_id,
        "op_id": f"op-{row_id}",
        "request_id": "request-1",
        "table_target": "chat.message",
        "op_type": "insert",
        "primary_key": {"id": f"msg-{row_id}"},
        "payload": {"id": f"msg-{row_id}", "role": "user", "content": []},
        "depends_on": [],
        "error_text": error_text,
        "retry_count": retry_count,
        "failed_at": datetime.now(UTC),
        "user_id": None,
        "conversation_id": None,
        "organization_id": "org-1",
        "created_by": None,
    }


# ── the classifier ───────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "error_text",
    [
        _TRIGGER_REFUSAL,
        f"{DIRECT_WRITE_PRESERVED_MARKER}: asyncpg.exceptions.CheckViolationError: "
        "new row violates check constraint [SQLSTATE 23514]",
        "asyncpg.exceptions.NotNullViolationError: null value in column [SQLSTATE 23502]",
        "asyncpg.exceptions.UndefinedColumnError: column x does not exist [SQLSTATE 42703]",
        "asyncpg.exceptions.InvalidTextRepresentationError: invalid uuid [SQLSTATE 22P02]",
        f"{DISK_SPILL_RECOVERED_MARKER}: timeout [capture_actor_missing=abc]",
    ],
)
def test_permanent_signatures_are_recognised(error_text: str) -> None:
    assert replay.is_permanent_failure_text(error_text)


@pytest.mark.parametrize(
    "error_text",
    [
        f"{DISK_SPILL_RECOVERED_MARKER}: asyncpg.exceptions.ForeignKeyViolationError: "
        "insert violates foreign key [SQLSTATE 23503]",
        "InterfaceError: cannot perform operation: another operation is in progress",
        f"{DIRECT_WRITE_PRESERVED_MARKER}: asyncpg.exceptions.QueryCanceledError: "
        "canceling statement due to statement timeout [SQLSTATE 57014]",
        "commit hard-deadline exceeded",
        None,
        "",
    ],
)
def test_environmental_failures_stay_recoverable(error_text: str | None) -> None:
    assert not replay.is_permanent_failure_text(error_text)


# Hole found by the adversarial review of ae470c61b: when the app has already
# stamped organization_id, the org trigger no-ops and the same phantom user dies
# on chat.message's FK to auth.users instead — a ForeignKeyViolationError, which
# the recoverable list matches. A missing USER is never a race.
_ACTOR_FK = (
    f"{DISK_SPILL_RECOVERED_MARKER}: asyncpg.exceptions.ForeignKeyViolationError: "
    'insert or update on table "message" violates foreign key constraint '
    '"message_created_by_fkey" [SQLSTATE 23503] constraint=message_created_by_fkey '
    "table=message detail=Key (created_by)=(e4687a9c-acf7-469f-aa12-860eb4d948d0) "
    'is not present in table "users".'
)
_PARENT_FK = (
    "asyncpg.exceptions.ForeignKeyViolationError: insert or update on table "
    '"tool_call" violates foreign key constraint "cx_tool_call_conversation_id_fkey" '
    "[SQLSTATE 23503] constraint=cx_tool_call_conversation_id_fkey table=tool_call "
    'detail=Key (conversation_id)=(abc) is not present in table "conversation".'
)


def test_fk_to_a_missing_user_is_permanent_but_a_missing_parent_row_is_a_race() -> None:
    assert replay.is_actor_fk_violation_text(_ACTOR_FK)
    assert replay.is_permanent_failure_text(_ACTOR_FK)
    assert not replay.is_actor_fk_violation_text(_PARENT_FK)
    assert not replay.is_permanent_failure_text(_PARENT_FK)
    # The constraint name alone is enough when Postgres's detail is absent.
    assert replay.is_permanent_failure_text(
        "ForeignKeyViolationError: violates foreign key constraint "
        "[SQLSTATE 23503] constraint=conversation_user_id_fkey"
    )
    # And the actor signatures never fire on a non-FK error.
    assert not replay.is_actor_fk_violation_text('a note that says is not present in table "users"')


def _trigger_refusal_exception() -> RuntimeError:
    """The real shape: an ORM QueryError wrapping the asyncpg driver error."""
    import asyncpg.exceptions

    driver = asyncpg.exceptions.RaiseError("stamp_actor: user x does not exist")
    wrapped = RuntimeError("bulk_insert failed")
    wrapped.__cause__ = driver
    return wrapped


def test_live_exception_classifier_reads_the_driver_cause_chain() -> None:
    assert replay.is_permanent_failure_exception(_trigger_refusal_exception())
    assert not replay.is_permanent_failure_exception(RuntimeError("connection reset"))
    import asyncpg.exceptions

    fk = asyncpg.exceptions.ForeignKeyViolationError("insert violates foreign key")
    assert not replay.is_permanent_failure_exception(fk)


# ── replay_pending in auto mode ──────────────────────────────────────────────


class _Harness:
    """Wires replay_pending to in-memory doubles and records every side effect."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch, rows: list[dict[str, Any]]) -> None:
        self.rows = rows
        self.executed: list[Any] = []
        self.captured: list[dict[str, Any]] = []
        self.attempts: list[dict[str, Any]] = []
        self.recovered: list[list[str]] = []

        async def fetch(**kwargs: Any) -> list[dict[str, Any]]:
            return list(self.rows)

        async def execute(tiers: Any) -> None:
            self.executed.append(tiers)

        async def capture(exc: Exception, **kwargs: Any) -> None:
            self.captured.append({"exc": exc, **kwargs})

        async def record(rows_: Any, *, max_attempts: int | None, permanent: bool = False) -> int:
            self.attempts.append(
                {
                    "ids": [r["id"] for r in rows_],
                    "max_attempts": max_attempts,
                    "permanent": permanent,
                }
            )
            return len(rows_) if permanent else 0

        async def mark(ids: Any, recovery_op_id: str) -> None:
            self.recovered.append(list(ids))

        async def upgrade(rows_: Any) -> list[dict[str, Any]]:
            return [dict(r) for r in rows_]

        async def not_satisfied(op: Any) -> bool:
            return False

        class _Txn:
            async def __aenter__(self) -> None:
                return None

            async def __aexit__(self, *a: Any) -> None:
                return None

        import matrx_orm
        import matrx_orm.core.config as orm_config

        import matrx_ai.persistence.queue_helpers as queue_helpers

        monkeypatch.setattr(replay, "_fetch_pending", fetch)
        monkeypatch.setattr(replay, "execute_tiers", execute)
        monkeypatch.setattr(replay, "_capture_replay_failure", capture)
        monkeypatch.setattr(replay, "_record_failed_attempt", record)
        monkeypatch.setattr(replay, "_mark_recovered", mark)
        monkeypatch.setattr(replay, "_upgrade_legacy_chat_payloads", upgrade)
        monkeypatch.setattr(replay, "_op_already_satisfied", not_satisfied)
        monkeypatch.setattr(replay, "_row_to_op", _op)

        async def no_peer(rows_: Any) -> bool:
            return False

        monkeypatch.setattr(replay, "_rows_recovered_by_peer", no_peer)
        monkeypatch.setattr(replay, "coalesce_ops", lambda ops: ops)
        monkeypatch.setattr(replay, "tier_ops", lambda ops: ops)
        monkeypatch.setattr(matrx_orm, "transaction", lambda *a, **k: _Txn())
        monkeypatch.setattr(orm_config, "get_all_database_project_names", lambda: ["test"])
        monkeypatch.setattr(queue_helpers, "_ensure_cx_registered", lambda: None)


@pytest.mark.asyncio
async def test_permanent_at_capture_is_quarantined_without_an_attempt(monkeypatch) -> None:
    rows = [_row("a", _TRIGGER_REFUSAL), _row("b", _TRIGGER_REFUSAL)]
    h = _Harness(monkeypatch, rows)

    report = await replay.replay_pending(
        dry_run=False,
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert h.executed == [], "a permanently refused row must never be re-sent"
    assert h.recovered == []
    assert h.attempts == [
        {"ids": ["a", "b"], "max_attempts": replay.AUTO_REPLAY_MAX_ATTEMPTS, "permanent": True}
    ]
    assert report.quarantined_count == 2
    assert report.still_failed_count == 2
    assert report.recovered_count == 0
    assert report.by_request == {"request-1": "quarantined (permanent at capture)"}
    assert [c["kind"] for c in h.captured] == ["persistence_replay_quarantined"]
    assert h.captured[0]["phase"] == "classify"
    assert [r["id"] for r in h.captured[0]["rows"]] == ["a", "b"]


@pytest.mark.asyncio
@pytest.mark.parametrize("dry_run", [True, False])
async def test_immutable_replay_conflict_is_reported_and_never_replayed(
    monkeypatch: pytest.MonkeyPatch, dry_run: bool
) -> None:
    """PK existence with different text must be a conflict, not recovery."""
    h = _Harness(monkeypatch, [_row("a", f"{IMMUTABLE_WRITE_PRESERVED_MARKER}: timeout")])

    async def conflicting(_: Any, *, verify_exact: bool = False) -> bool:
        if verify_exact:
            raise RuntimeError("immutable replay conflict: existing row differs")
        return False

    monkeypatch.setattr(replay, "_op_already_satisfied", conflicting)
    report = await replay.replay_pending(
        dry_run=dry_run, retry_errors=None, max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS
    )
    assert h.executed == []
    assert report.conflict_count == 1
    assert report.by_request["request-1"] == (
        "would-quarantine (immutable conflict)" if dry_run else "quarantined (immutable conflict)"
    )
    if dry_run:
        assert h.attempts == []
    else:
        assert h.attempts == [{"ids": ["a"], "max_attempts": 5, "permanent": True}]


@pytest.mark.asyncio
@pytest.mark.parametrize("outcome", ["exact", "different"])
async def test_concurrent_unique_immutable_replay_has_one_truthful_terminal_receipt(
    monkeypatch: pytest.MonkeyPatch, outcome: str
) -> None:
    """A post-insert unique race recovers exact rows and quarantines differing rows once."""
    h = _Harness(monkeypatch, [_row("a", f"{IMMUTABLE_WRITE_PRESERVED_MARKER}: timeout")])
    checks = 0

    async def state(_: Any, *, verify_exact: bool = False) -> bool:
        nonlocal checks
        checks += 1
        if checks == 1:
            return False  # pre-insert probe: absent
        if outcome == "different":
            raise replay.ImmutableReplayConflictError("immutable replay conflict: text")
        return True  # post-unique probe: another writer landed the exact row

    class UniqueViolationError(RuntimeError):
        pass

    async def collide(_: Any) -> None:
        raise UniqueViolationError("duplicate key [SQLSTATE 23505]")

    monkeypatch.setattr(replay, "_op_already_satisfied", state)
    monkeypatch.setattr(replay, "execute_tiers", collide)
    report = await replay.replay_pending(
        dry_run=False, retry_errors=None, max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS
    )
    assert len(h.executed) == 0  # replaced with collision seam, never overwrites
    if outcome == "exact":
        assert h.recovered == [["a"]]
        assert h.attempts == []
        assert report.recovered_count == 1
        assert report.quarantined_count == 0
    else:
        assert h.recovered == []
        assert h.attempts == [{"ids": ["a"], "max_attempts": 5, "permanent": True}]
        assert report.recovered_count == 0
        assert report.quarantined_count == 1
        assert report.by_request["request-1"].startswith("quarantined (permanent)")


@pytest.mark.asyncio
async def test_a_human_retry_still_attempts_a_permanent_row(monkeypatch) -> None:
    """``max_attempts=None`` is the admin per-row Replay: a person asked."""
    h = _Harness(monkeypatch, [_row("a", _TRIGGER_REFUSAL)])

    report = await replay.replay_pending(dry_run=False, retry_errors=None, max_attempts=None)

    assert len(h.executed) == 1
    assert report.recovered_count == 1
    assert h.captured == []


@pytest.mark.asyncio
async def test_dry_run_reports_would_recover_without_quarantining(monkeypatch) -> None:
    h = _Harness(monkeypatch, [_row("a", _TRIGGER_REFUSAL)])

    report = await replay.replay_pending(
        dry_run=True,
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert h.attempts == []
    assert h.captured == []
    assert report.by_request == {"request-1": "would-recover"}


@pytest.mark.asyncio
async def test_environmental_row_is_still_attempted(monkeypatch) -> None:
    """The control: a genuine outage spill is replayed and recovered."""
    h = _Harness(
        monkeypatch,
        [_row("a", f"{DISK_SPILL_RECOVERED_MARKER}: ConnectionRefusedError: db down")],
    )

    report = await replay.replay_pending(
        dry_run=False,
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert len(h.executed) == 1
    assert h.recovered == [["a"]]
    assert report.recovered_count == 1
    assert report.quarantined_count == 0


@pytest.mark.asyncio
async def test_permanent_refusal_during_execute_is_quarantined_on_that_attempt(
    monkeypatch,
) -> None:
    """The row looked environmental at capture; the live attempt proves otherwise."""
    h = _Harness(
        monkeypatch,
        [_row("a", f"{DISK_SPILL_RECOVERED_MARKER}: ConnectionRefusedError: db down")],
    )

    async def refuse(tiers: Any) -> None:
        raise _trigger_refusal_exception()

    monkeypatch.setattr(replay, "execute_tiers", refuse)

    report = await replay.replay_pending(
        dry_run=False,
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert h.attempts == [
        {"ids": ["a"], "max_attempts": replay.AUTO_REPLAY_MAX_ATTEMPTS, "permanent": True}
    ]
    assert report.quarantined_count == 1
    assert report.by_request["request-1"].startswith("quarantined (permanent)")
    assert [c["kind"] for c in h.captured] == ["persistence_replay_quarantined"]
    assert h.captured[0]["phase"] == "execute"


@pytest.mark.asyncio
async def test_transient_refusal_during_execute_burns_one_attempt_only(monkeypatch) -> None:
    """The control for the branch above: a transient error is bumped, not quarantined."""
    h = _Harness(
        monkeypatch,
        [_row("a", f"{DISK_SPILL_RECOVERED_MARKER}: ConnectionRefusedError: db down")],
    )

    async def flake(tiers: Any) -> None:
        raise ConnectionResetError("pooler dropped the connection")

    monkeypatch.setattr(replay, "execute_tiers", flake)

    report = await replay.replay_pending(
        dry_run=False,
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert h.attempts == [
        {"ids": ["a"], "max_attempts": replay.AUTO_REPLAY_MAX_ATTEMPTS, "permanent": False}
    ]
    assert report.quarantined_count == 0
    assert [c["kind"] for c in h.captured] == ["persistence_replay_failed"]


@pytest.mark.asyncio
async def test_replay_failure_capture_never_serializes_bound_arguments(monkeypatch) -> None:
    """A replay retry cannot copy a snapshot prompt into system_error diagnostics."""
    captured: dict[str, Any] = {}

    async def capture_error(exc: Exception, **kwargs: Any) -> None:
        captured["text"] = str(exc)
        captured.update(kwargs)

    import matrx_connect.streaming.error_capture as error_capture

    monkeypatch.setattr(error_capture, "capture_error", capture_error)
    private = "PRIVATE_SENTINEL"
    await replay._capture_replay_failure(
        QueryTimeoutError(
            operation="execute_query",
            query="INSERT INTO chat.request_snapshot (request_payload) VALUES ($1)",
            args=[private],
        ),
        request_id="request-1",
        rows=[_row("snapshot", "QueryTimeoutError: lock timeout")],
        phase="execute",
    )

    assert private not in str(captured)
    assert "Args:" not in str(captured)
    assert captured["error_type"] == "QueryTimeoutError"
    assert captured["text"] == "QueryTimeoutError: replay execution failed"


# ── the accounting itself ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_record_failed_attempt_permanent_pins_retry_count_at_the_cap(monkeypatch) -> None:
    updates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    bumps: list[list[str]] = []

    class _Qb:
        def __init__(self, ids: list[str]) -> None:
            self.ids = ids

        async def update(self, **fields: Any) -> int:
            bumps.append(self.ids)
            return len(self.ids)

    class _Swf:
        @staticmethod
        def filter(**kw: Any) -> _Qb:
            return _Qb(list(kw["id__in"]))

        @staticmethod
        async def update_where(where: dict[str, Any], **fields: Any) -> int:
            updates.append((where, fields))
            return len(where["id__in"])

    monkeypatch.setattr(replay, "_swf_model", lambda: _Swf)

    # Fresh rows (retry_count 0, seconds old) would ordinarily just be bumped.
    rows = [_row("a", _TRIGGER_REFUSAL), _row("b", _TRIGGER_REFUSAL)]
    gave_up = await replay._record_failed_attempt(rows, max_attempts=5, permanent=True)

    assert gave_up == 2
    assert bumps == []
    assert updates == [({"id__in": ["a", "b"]}, {"retry_count": 5})]

    # Control: the same rows without the flag are bumped, not quarantined.
    updates.clear()
    gave_up = await replay._record_failed_attempt(rows, max_attempts=5, permanent=False)
    assert gave_up == 0
    assert bumps == [["a", "b"]]
    assert updates == []


# ── a unique collision with a landed write settles, never quarantines ────────
#
# Live evidence (2026-11-10, request dd82cc0c): a turn's chat.message insert
# "timed out" but landed; three replay sweeps (one per server task) raced the
# preserved group (the failed-turn message INSERT + its chat.user_request
# UPDATE). One recovered it; the other two hit 23505, exact-verified EVERY op —
# an UPDATE is never "satisfied" and the message's ``position`` -1 (append
# sentinel) differed from the trigger's 49 — and quarantined a write that was
# safely in the table.


def _op(row: dict[str, Any]) -> Any:
    from types import SimpleNamespace

    pk = next(iter(row["primary_key"].values()))
    return SimpleNamespace(
        table=row["table_target"], pk_value=pk, op_type=row["op_type"], row_id=row["id"]
    )


def _collision_group() -> list[dict[str, Any]]:
    insert = _row("msg", "builtins.RuntimeError: coordinator drop: queue_in_phase_errored")
    update = _row("ur", "builtins.RuntimeError: coordinator drop: queue_in_phase_errored")
    update.update(
        table_target="chat.user_request",
        op_type="update",
        primary_key={"id": "request-1"},
        payload={"status": "failed"},
    )
    return [insert, update]


class _UniqueViolationError(RuntimeError):
    sqlstate = "23505"


@pytest.mark.asyncio
async def test_unique_collision_with_a_landed_insert_recovers_and_reapplies_updates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = _Harness(monkeypatch, _collision_group())
    monkeypatch.setattr(replay, "_row_to_op", _op)
    landed = {"msg": False}

    async def state(op: Any, *, verify_exact: bool = False) -> bool:
        if op.op_type != "insert":
            return False
        if verify_exact:
            # The pre-fix comparator: append sentinel -1 vs trigger-assigned 49.
            raise replay.ImmutableReplayConflictError("immutable replay conflict: ['position']")
        return landed[op.row_id]

    calls: list[list[str]] = []

    async def execute(tiers: Any) -> None:
        calls.append([op.row_id for op in tiers])
        if len(calls) == 1:
            landed["msg"] = True  # a peer sweep landed the message first
            raise _UniqueViolationError("duplicate key value [SQLSTATE 23505]")

    async def not_peer(rows: Any) -> bool:
        return False

    monkeypatch.setattr(replay, "_op_already_satisfied", state)
    monkeypatch.setattr(replay, "execute_tiers", execute)
    monkeypatch.setattr(replay, "_rows_recovered_by_peer", not_peer)

    report = await replay.replay_pending(
        dry_run=False,
        retry_errors=None,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert h.captured == [], "a landed write is not an incident"
    assert h.attempts == [], "a landed write must never be quarantined"
    assert calls == [["msg", "ur"], ["ur"]], "only the UPDATE is re-applied"
    assert h.recovered == [["msg", "ur"]]
    assert report.recovered_count == 2
    assert report.quarantined_count == 0


@pytest.mark.asyncio
async def test_unique_collision_after_a_peer_recovered_the_group_writes_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = _Harness(monkeypatch, _collision_group())
    monkeypatch.setattr(replay, "_row_to_op", _op)
    calls: list[Any] = []

    async def execute(tiers: Any) -> None:
        calls.append(tiers)
        raise _UniqueViolationError("duplicate key value [SQLSTATE 23505]")

    async def peer(rows: Any) -> bool:
        return True

    monkeypatch.setattr(replay, "execute_tiers", execute)
    monkeypatch.setattr(replay, "_rows_recovered_by_peer", peer)

    report = await replay.replay_pending(
        dry_run=False,
        retry_errors=None,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert len(calls) == 1, "no second write once a peer settled the group"
    assert h.captured == [] and h.attempts == []
    assert h.recovered == [], "the peer's recovery receipt is kept, not overwritten"
    assert report.by_request["request-1"] == "recovered (by a concurrent replay)"


def test_append_position_sentinel_is_satisfied_by_the_assigned_position() -> None:
    from matrx_orm import immutable_row_differences

    import matrx_ai.db.message_positions  # noqa: F401 — declares the sentinel

    landed = {"id": "m", "position": 49, "content": "x"}
    intent = {"id": "m", "position": -1, "content": "x"}
    assert immutable_row_differences(landed, intent, table="chat.message") == {}
    # A real difference is still a conflict; an explicit position is still exact.
    assert immutable_row_differences(landed, {**intent, "content": "y"}, table="chat.message")
    assert immutable_row_differences(landed, {**intent, "position": 7}, table="chat.message")
    # Undeclared tables compare exactly.
    assert immutable_row_differences(landed, intent, table="chat.other") == {"position": {"expected": -1, "actual": 49}}


class _LockNotAvailable(Exception):
    sqlstate = "55P03"


@pytest.mark.asyncio
async def test_lock_contention_on_replay_is_a_peer_not_a_filed_failure(monkeypatch) -> None:
    """Two sweeps reach one group together; the loser's lock timeout is counted, never filed.

    2026-11-10: failure row c24828b1 drew two persistence_replay_failed rows (00:17:06, 00:17:07) from two
    sweeps waiting on the row a third sweep landed at 00:17:07.68.
    """
    h = _Harness(monkeypatch, [_row("a", f"{DISK_SPILL_RECOVERED_MARKER}: QueryTimeoutError")])

    async def contended(tiers: Any) -> None:
        raise _LockNotAvailable("canceling statement due to lock timeout")

    monkeypatch.setattr(replay, "execute_tiers", contended)

    report = await replay.replay_pending(
        dry_run=False,
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert h.captured == [], "a lock wait lost to a concurrent writer files no system_error"
    assert h.attempts == [
        {"ids": ["a"], "max_attempts": replay.AUTO_REPLAY_MAX_ATTEMPTS, "permanent": False}
    ], "the attempt still counts, so a row that never lands still reaches the quarantine"
    assert report.quarantined_count == 0


@pytest.mark.asyncio
async def test_lock_contention_after_a_peer_landed_the_group_is_recovered(monkeypatch) -> None:
    h = _Harness(monkeypatch, [_row("a", f"{DISK_SPILL_RECOVERED_MARKER}: QueryTimeoutError")])

    async def contended(tiers: Any) -> None:
        raise _LockNotAvailable("canceling statement due to lock timeout")

    async def peer(rows: Any) -> bool:
        return True

    monkeypatch.setattr(replay, "execute_tiers", contended)
    monkeypatch.setattr(replay, "_rows_recovered_by_peer", peer)

    report = await replay.replay_pending(
        dry_run=False, retry_errors=None, max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS
    )

    assert h.captured == [] and h.attempts == []
    assert report.by_request["request-1"] == "recovered (by a concurrent replay)"


@pytest.mark.asyncio
async def test_lock_contention_that_exhausts_the_budget_is_quarantined_once(monkeypatch) -> None:
    h = _Harness(monkeypatch, [_row("a", f"{DISK_SPILL_RECOVERED_MARKER}: QueryTimeoutError")])

    async def contended(tiers: Any) -> None:
        raise _LockNotAvailable("canceling statement due to lock timeout")

    async def exhausted(rows_: Any, *, max_attempts: int | None, permanent: bool = False) -> int:
        return len(rows_)

    monkeypatch.setattr(replay, "execute_tiers", contended)
    monkeypatch.setattr(replay, "_record_failed_attempt", exhausted)

    report = await replay.replay_pending(
        dry_run=False, retry_errors=None, max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS
    )

    assert [c["kind"] for c in h.captured] == ["persistence_replay_quarantined"]
    assert report.quarantined_count == 1


@pytest.mark.asyncio
async def test_a_write_that_keeps_failing_files_one_system_error_not_one_per_attempt(monkeypatch) -> None:
    """Live 2026-11-14: one orphan chat.tool_call insert (FK to a conversation that never landed) was retried
    five times and each sweep filed its own persistence_replay_failed row. The first attempt files; the
    sweeps that follow (retry_count 1..4) stay silent while still counting their attempt."""
    fk = "asyncpg.exceptions.ForeignKeyViolationError: tool_call violates cx_tool_call_conversation_id_fkey [SQLSTATE 23503]"
    filed = 0
    for retry_count in range(replay.AUTO_REPLAY_MAX_ATTEMPTS):
        h = _Harness(monkeypatch, [_row("a", f"{DISK_SPILL_RECOVERED_MARKER}: {fk}", retry_count=retry_count)])

        async def orphan(tiers: Any) -> None:
            raise RuntimeError("ForeignKeyViolationError: replay execution failed [SQLSTATE 23503]")

        monkeypatch.setattr(replay, "execute_tiers", orphan)
        await replay.replay_pending(
            dry_run=False,
            retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
            max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
        )
        assert len(h.attempts) == 1  # every attempt is still counted
        filed += len(h.captured)
    assert filed == 1
