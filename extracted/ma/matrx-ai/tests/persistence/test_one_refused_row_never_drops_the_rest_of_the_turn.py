"""One row the database refuses never drops the writes queued after it.

2026-11-04 02:39Z / 02:41Z (live, two confidential chat turns): the sealed-content
CHECK refused the turn's final ``chat.user_request`` UPDATE. The final commit barrier
failed — correctly: the request stopped. But the Coordinator then went ERRORED and
every write queued AFTER the failure (the turn's ``chat.message`` INSERT, the
request's terminal UPDATE) was dropped to ``system_write_failure``; a confidential
capture is redacted, so replay refused it and the messages were lost.

The database had ANSWERED (it refused one row); it was not wedged. So an ERRORED
verdict made of database refusals keeps stopping the request, while each later
write lands on its own one-shot. An ERRORED verdict of any other kind (a timeout,
an unreachable database) still captures for replay, as before.
"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import Sequence

import asyncpg
import pytest

from matrx_ai.persistence.coordinator import (
    Coordinator,
    CoordinatorPhase,
    PersistenceBarrierError,
    _is_database_refusal,
)
from matrx_ai.persistence.registry import register_table

_REFUSED_ID = "5b1d7e2a-0c3f-4a6b-8d9e-1f2a3b4c5d6e"
_LATER_ID = "6c2e8f3b-1d4a-4b7c-9e0f-2a3b4c5d6e7f"


class _MetaRequest:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "cx_fake_refusal_request"
    db_schema = "public"


class _MetaMessage:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "cx_fake_refusal_message"
    db_schema = "public"


class _FakeRequest:
    _meta = _MetaRequest()

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class _FakeMessage:
    _meta = _MetaMessage()

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


register_table("public.cx_fake_refusal_request", _FakeRequest)
register_table("public.cx_fake_refusal_message", _FakeMessage)


@contextlib.asynccontextmanager
async def _fake_transaction(*args, **kwargs):
    yield


@pytest.fixture(autouse=True)
def _patch_transaction(monkeypatch):
    import matrx_orm.core.transaction as txn_mod

    monkeypatch.setattr(txn_mod, "transaction", _fake_transaction)


@pytest.fixture
def refusing_database(monkeypatch):
    """execute_tiers that refuses the sealed row (CHECK, 23514) and writes the rest."""
    written: list[str] = []

    async def fake_execute_tiers(tiers: Sequence[Sequence]) -> int:
        ops = [op for tier in tiers for op in tier]
        if any(str(op.pk_value) == _REFUSED_ID for op in ops):
            raise asyncpg.exceptions.CheckViolationError(
                "confidential conversation: metadata.notes may not be stored on the server"
            )
        written.extend(str(op.pk_value) for op in ops)
        return len(ops)

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", fake_execute_tiers)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", fake_execute_tiers)
    return written


@pytest.mark.asyncio
async def test_a_write_queued_after_a_refused_row_still_lands(capture_sink, refusing_database):
    failures, _errors = capture_sink
    coord = Coordinator(request_id="req-refusal", conversation_id="conv-refusal")
    coord.queue(
        "public.cx_fake_refusal_request",
        {"status": "completed"},
        op_type="update",
        primary_key=("id", _REFUSED_ID),
    )

    with pytest.raises(PersistenceBarrierError):
        await coord.finalize(reason="request_final_commit")
    assert coord.phase is CoordinatorPhase.ERRORED, "the request still stops"

    op_id = coord.queue(
        "public.cx_fake_refusal_message",
        {"id": _LATER_ID, "role": "assistant", "position": 3},
    )
    assert op_id, "a write after a refusal must be scheduled, not dropped"
    await coord.seal()

    assert _LATER_ID in refusing_database, "the later message landed in its table"
    captured_ids = {str(op.pk_value) for f in failures for op in f["ops"]}
    assert _REFUSED_ID in captured_ids, "the refused row is still preserved for a human"
    assert _LATER_ID not in captured_ids, "the landed message is not filed as lost"
    assert coord.phase is CoordinatorPhase.ERRORED, "the verdict stays sticky"


@pytest.mark.asyncio
async def test_an_errored_coordinator_that_is_not_a_refusal_still_captures(capture_sink, refusing_database):
    failures, _errors = capture_sink
    coord = Coordinator(request_id="req-wedged", conversation_id="conv-wedged")
    coord._phase = CoordinatorPhase.ERRORED  # e.g. a hard-deadline: the database did not answer

    assert coord.queue("public.cx_fake_refusal_message", {"id": _LATER_ID}) == ""
    await coord.seal()
    for _ in range(20):  # the capture runs on a detached task
        await asyncio.sleep(0)

    assert _LATER_ID not in refusing_database
    assert {str(op.pk_value) for f in failures for op in f["ops"]} == {_LATER_ID}


def test_refusal_is_read_from_the_sqlstate_never_the_words():
    assert _is_database_refusal(asyncpg.exceptions.CheckViolationError("x"))
    assert _is_database_refusal(asyncpg.exceptions.InFailedSQLTransactionError("x"))
    assert not _is_database_refusal(asyncpg.exceptions.QueryCanceledError("statement timeout"))
    assert not _is_database_refusal(asyncpg.exceptions.ConnectionDoesNotExistError("gone"))
    assert not _is_database_refusal(TimeoutError("commit hard-deadline"))
    assert not _is_database_refusal(None)
