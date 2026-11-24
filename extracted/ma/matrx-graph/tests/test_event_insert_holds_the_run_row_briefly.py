"""The workflow.run row lock an event insert takes covers TWO statements and nothing else.

Live 2026-10-29..11-02 (7 system_error rows, ``55P03 lock_not_available`` on workflow.run): the
single-event path held the run row idle-in-transaction for 10 s — its ``create()`` hopped to the
thread pool to encode the row, read the whole row back and decoded it, all after the seq bump —
so every sibling writer of that run was canceled at the 5 s ``lock_timeout``. And a canceled
collision was never re-run, so the event was simply lost.
"""

from __future__ import annotations

import importlib
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_orm import LockContentionError

from matrx_graph.db.event_store import EventStore

RUN = "00000000-0000-0000-0000-0000000000a1"
ORG = "00000000-0000-0000-0000-0000000000b2"


class _World:
    def __init__(self, *, refuse_first_bumps: int = 0) -> None:
        self.in_tx = False
        self.log: list[tuple[str, bool]] = []
        self.seq = 0
        self.refuse = refuse_first_bumps
        self.inserted: list[dict[str, Any]] = []

    @asynccontextmanager
    async def transaction(self, *_a: Any, **_k: Any):
        self.in_tx = True
        try:
            yield
        finally:
            self.in_tx = False

    async def update_run(self, _filters: dict[str, Any], **kwargs: Any) -> Any:
        self.log.append(("bump", self.in_tx))
        if self.refuse:
            self.refuse -= 1
            raise LockContentionError(original_error=RuntimeError("canceling statement due to lock timeout"), in_transaction=True)
        n = kwargs["event_seq"].value
        self.seq += int(n)
        return SimpleNamespace(updated_rows=[{"id": RUN, "event_seq": self.seq, "organization_id": ORG}])

    def model(self, name: str) -> Any:
        world = self

        class _M:
            @staticmethod
            def get_database_name() -> str:
                return "test_db"

            @staticmethod
            async def bulk_create(rows: list[dict[str, Any]], *, returning: list[str] | None = None, **_k: Any):
                world.log.append(("insert", world.in_tx))
                assert returning == ["id"], "the event rows must never be read back"
                world.inserted.extend(rows)
                return [{"id": i} for i, _ in enumerate(rows)]

            @staticmethod
            async def create(**_k: Any) -> Any:
                world.log.append(("create", world.in_tx))
                raise AssertionError("create() reads the whole row back inside the run-row lock")

        return _M


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch):
    def make(**kw: Any) -> _World:
        w = _World(**kw)
        monkeypatch.setattr("matrx_orm.transaction", w.transaction)
        monkeypatch.setattr("matrx_graph.db.run_store.update_run", w.update_run)
        monkeypatch.setattr("matrx_graph.db._registry.get_model", w.model)

        async def intern(_run: str, payload: dict[str, Any]) -> dict[str, Any]:
            w.log.append(("intern", w.in_tx))
            return payload

        def redact(payload: dict[str, Any]) -> dict[str, Any]:
            w.log.append(("redact", w.in_tx))
            return payload

        monkeypatch.setattr("matrx_graph.checkpoint.value_store.intern_event_payload", intern)
        monkeypatch.setattr(importlib.import_module("matrx_graph.failure"), "client_safe_error_payload", redact)

        async def policy(_db: str) -> Any:
            return SimpleNamespace(max_retries=3, backoff_seconds=lambda _a: 0.0)

        monkeypatch.setattr("matrx_orm.core.write_retry.resolve_policy", policy)
        return w

    return make


@pytest.mark.asyncio
async def test_single_event_does_only_the_bump_and_one_insert_under_the_run_lock(world) -> None:
    w = world()
    seq = await EventStore().insert_event(RUN, event_type="node_started", payload={"a": 1}, node_id="n1")
    assert seq == 1
    under_lock = [what for what, locked in w.log if locked]
    assert under_lock == ["bump", "insert"], w.log
    assert w.inserted[0]["seq"] == 1 and str(w.inserted[0]["organization_id"]) == ORG


@pytest.mark.asyncio
async def test_batch_does_only_the_bump_and_one_insert_under_the_run_lock(world) -> None:
    w = world()
    seqs = await EventStore().insert_events(
        RUN, [{"event_type": "a", "payload": {}}, {"event_type": "b", "payload": {}, "error_message": "x"}]
    )
    assert seqs == [1, 2]
    assert [what for what, locked in w.log if locked] == ["bump", "insert"], w.log


@pytest.mark.asyncio
async def test_a_canceled_lock_collision_is_rerun_whole_not_lost(world) -> None:
    w = world(refuse_first_bumps=2)
    seq = await EventStore().insert_event(RUN, event_type="node_started", payload={})
    assert seq == 1
    assert [what for what, _ in w.log].count("bump") == 3
    assert len(w.inserted) == 1
