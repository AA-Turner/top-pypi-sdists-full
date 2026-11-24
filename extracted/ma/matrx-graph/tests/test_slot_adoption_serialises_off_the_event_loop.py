"""Adopting a run's live outputs never serialises them on the event loop (2026-11-17).

Live: ``wf_slot_adoption`` froze the server's loop for 1,129 ms inside ``json.dumps`` (``_bounded_dumps``)
while turning a run's step results into ``last_live_output`` slot rows; no request was served meanwhile.
Resolving and serialising every step's result is pure CPU, so it runs in a worker thread.
"""

from __future__ import annotations

import asyncio
import threading
from typing import Any
from uuid import uuid4

import pytest

from matrx_graph.db import _registry
from matrx_graph.db import node_data_slot_store as slots_mod


class _Query:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def filter(self, **_kw: Any) -> _Query:
        return self

    def order_by(self, *_a: Any) -> _Query:
        return self

    async def values(self, *_a: Any) -> list[dict[str, Any]]:
        return self._rows


class _OutcomeModel:
    rows: list[dict[str, Any]] = []

    @classmethod
    def filter(cls, **_kw: Any) -> _Query:
        return _Query(cls.rows)


def test_slot_rows_are_serialised_off_the_loop_thread(monkeypatch: pytest.MonkeyPatch) -> None:
    _OutcomeModel.rows = [
        {"node_id": "n1", "output": {"items": list(range(50))}, "emissions": {}, "output_kind": None},
        {"node_id": "n2", "output": {"text": "hello"}, "emissions": {}, "output_kind": None},
    ]
    monkeypatch.setitem(_registry._models, "WfNodeOutcome", _OutcomeModel)
    monkeypatch.setitem(_registry._models, "WfNodeDataSlot", object())

    dump_threads: list[int] = []
    real_dumps = slots_mod._bounded_dumps

    def recording_dumps(value: Any, *, field: str) -> str:
        dump_threads.append(threading.get_ident())
        return real_dumps(value, field=field)

    monkeypatch.setattr(slots_mod, "_bounded_dumps", recording_dumps)

    import matrx_orm.operations.create as create_ops

    async def fake_bulk_upsert(_model: Any, rows: list[dict[str, Any]], *_a: Any, **_kw: Any) -> list[dict[str, Any]]:
        return [{"id": i} for i, _ in enumerate(rows)]

    monkeypatch.setattr(create_ops, "bulk_upsert", fake_bulk_upsert)

    async def run() -> tuple[int, int]:
        landed = await slots_mod.NodeDataSlotStore().adopt_live_outputs(
            run_id=str(uuid4()), definition_id=str(uuid4()), user_id=str(uuid4())
        )
        return landed, threading.get_ident()

    landed, loop_thread = asyncio.run(run())
    assert landed == 2
    assert dump_threads, "no slot row was serialised"
    assert loop_thread not in dump_threads, "slot rows were serialised on the event loop thread"
