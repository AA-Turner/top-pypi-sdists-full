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
from matrx_orm.session.fallback import (
    DIRECT_WRITE_PRESERVED_MARKER,
    DISK_SPILL_RECOVERED_MARKER,
    IMMUTABLE_WRITE_PRESERVED_MARKER,
)

from matrx_ai.persistence import replay

_TRIGGER_REFUSAL = (
    f"{DISK_SPILL_RECOVERED_MARKER}: asyncpg.exceptions.RaiseError: "
    "ensure_personal_organization: user e4687a9c-acf7-469f-aa12-860eb4d948d0 "
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

    driver = asyncpg.exceptions.RaiseError("ensure_personal_organization: user x does not exist")
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
        monkeypatch.setattr(replay, "_row_to_op", lambda r: r)
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
