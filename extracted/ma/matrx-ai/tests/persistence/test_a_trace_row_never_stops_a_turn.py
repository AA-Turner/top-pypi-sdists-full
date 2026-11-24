"""A telemetry row the database refuses costs that row, never the person's turn.

2026-11-06 09:54-10:03Z: a ``chat.tool_trace`` event the CHECK did not list was refused at the turn's commit, and the
next barrier stopped the request ("Request stopped to avoid silent data loss") though every message of the turn had
landed. The row is still filed to ``system_write_failure``; only the barrier's verdict changes. A refused row of any
other table keeps stopping the request (test_one_refused_row_never_drops_the_rest_of_the_turn).
"""

from __future__ import annotations

import contextlib
from collections.abc import Sequence

import asyncpg
import pytest

from matrx_ai.persistence import coordinator as coordinator_module
from matrx_ai.persistence.coordinator import Coordinator, PersistenceBarrierError
from matrx_ai.persistence.registry import register_table

_REAL_TELEMETRY_TABLES = coordinator_module._TELEMETRY_TABLES
_TRACE_ID = "7c6cceb8-3748-4372-9410-8a0f3226fdec"
_MESSAGE_ID = "6c2e8f3b-1d4a-4b7c-9e0f-2a3b4c5d6e7f"


def _model(schema: str, table: str) -> type:
    meta = type("Meta", (), {"primary_keys": ["id"], "foreign_keys": {}, "table_name": table, "db_schema": schema})

    class Model:
        _meta = meta()

        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    register_table(f"{schema}.{table}", Model)
    return Model


_model("public", "cx_fake_trace_turn_trace")
_model("public", "cx_fake_trace_turn_message")


@contextlib.asynccontextmanager
async def _fake_transaction(*args, **kwargs):
    yield


@pytest.fixture(autouse=True)
def _patch_transaction(monkeypatch):
    import matrx_orm.core.transaction as txn_mod

    monkeypatch.setattr(txn_mod, "transaction", _fake_transaction)
    # A stand-in never owns a real chat table (test_registry_isolation): it takes the telemetry slot here.
    monkeypatch.setattr(coordinator_module, "_TELEMETRY_TABLES", frozenset({"public.cx_fake_trace_turn_trace"}))


@pytest.fixture
def database(monkeypatch):
    """execute_tiers that refuses the row whose id is in ``refused`` (CHECK, 23514) and writes the rest."""
    written: list[str] = []
    refused = {_TRACE_ID}

    async def fake_execute_tiers(tiers: Sequence[Sequence]) -> int:
        ops = [op for tier in tiers for op in tier]
        if any(str(op.pk_value) in refused for op in ops):
            raise asyncpg.exceptions.CheckViolationError("violates check constraint cx_tool_trace_event_check")
        written.extend(str(op.pk_value) for op in ops)
        return len(ops)

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", fake_execute_tiers)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", fake_execute_tiers)
    return written, refused


def _turn(coordinator: Coordinator) -> None:
    coordinator.queue("public.cx_fake_trace_turn_trace", {"id": _TRACE_ID, "event": "NOT_IN_THE_CHECK"})
    coordinator.queue("public.cx_fake_trace_turn_message", {"id": _MESSAGE_ID})


def test_the_trace_table_is_telemetry() -> None:
    assert _REAL_TELEMETRY_TABLES == frozenset({"chat.tool_trace"})


async def test_a_refused_trace_row_passes_the_next_barrier_and_is_filed(database, capture_sink) -> None:
    written, _ = database
    coordinator = Coordinator(conversation_id="c", request_id="r")
    _turn(coordinator)
    coordinator.commit_async(reason="turn_1_commit")

    await coordinator.check_pending()
    await coordinator.finalize(reason="turn_2_delegate_precommit")

    assert written == [_MESSAGE_ID]
    failures, _ = capture_sink
    assert [op.table for failure in failures for op in failure["ops"]] == ["public.cx_fake_trace_turn_trace"]


async def test_a_refused_trace_row_passes_a_synchronous_commit(database, capture_sink) -> None:
    written, _ = database
    coordinator = Coordinator(conversation_id="c", request_id="r")
    _turn(coordinator)

    await coordinator.finalize(reason="final")

    assert written == [_MESSAGE_ID]


async def test_any_other_refused_row_still_stops_the_request(database, capture_sink) -> None:
    _, refused = database
    refused.add(_MESSAGE_ID)
    coordinator = Coordinator(conversation_id="c", request_id="r")
    _turn(coordinator)
    coordinator.commit_async(reason="turn_1_commit")

    with pytest.raises(PersistenceBarrierError) as barrier:
        await coordinator.finalize(reason="turn_2_delegate_precommit")
    assert barrier.value.report.ops_lost == 2
