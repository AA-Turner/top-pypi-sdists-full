"""A polling park's wake must resume the park it was written FOR.

``re_execute`` re-runs the same node at the same step on every wake, so every park writes a new
interrupt checkpoint with an EQUAL step. The worker hands ``schedule_sleep_wake`` no checkpoint
pointer; the old fallback ordered interrupt checkpoints by step alone and picked the PREVIOUS park,
whose resume the run then refused as stale — the wake was spent and the run slept forever (live
2026-10-25, knowledge buckets ``batch.wait_for_units``). Red before: the wake targets ``old``.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from matrx_graph.nodes.flow.sleep import RE_EXECUTE_ON_WAKE, SLEEP_MARKER
from matrx_graph.workers import sleep_wake

OLD = "a104ef5c-ef00-4b54-a6eb-9a1571b726a2"
NEW = "efd60710-f90f-41da-8105-d2a8071f6700"
RUN = "f30299d0-0897-4a18-aa2b-4336fc5ec4bd"


class _Rows:
    """Two interrupt checkpoints at the same step; the store returns them in insertion order."""

    def __init__(self) -> None:
        self.rows = [
            {"id": OLD, "step": 4, "created_at": datetime(2026, 10, 25, 11, 39, tzinfo=UTC)},
            {"id": NEW, "step": 4, "created_at": datetime(2026, 10, 25, 11, 40, tzinfo=UTC)},
        ]
        self.order: tuple[str, ...] = ()

    def filter(self, **_: Any) -> _Rows:
        return self

    def exclude(self, **_: Any) -> _Rows:
        return self

    def order_by(self, *fields: str) -> _Rows:
        self.order = fields
        return self

    def limit(self, _: int) -> _Rows:
        return self

    async def values(self, *_: str) -> list[dict[str, Any]]:
        rows = list(self.rows)
        for f in reversed(self.order):  # stable multi-key sort, like ORDER BY a, b
            rows.sort(key=lambda r: r[f.lstrip("-")], reverse=f.startswith("-"))
        return [{"id": r["id"]} for r in rows]


@pytest.fixture
def enqueued(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    import matrx_graph.db._registry as registry
    import matrx_graph.workers.queue as queue

    rows = _Rows()
    monkeypatch.setattr(registry, "get_model", lambda name: rows)
    got: list[dict[str, Any]] = []

    async def fake_enqueue(**kw: Any) -> str:
        got.append(kw)
        return "job-1"

    monkeypatch.setattr(queue, "enqueue", fake_enqueue)
    return got


def _interrupt(checkpoint_id: str | None) -> dict[str, Any]:
    marker = {"node_id": "wait", "wake_at": (datetime.now(UTC) + timedelta(minutes=2)).isoformat(), RE_EXECUTE_ON_WAKE: True}
    out: dict[str, Any] = {"node_id": "wait", "payload": {SLEEP_MARKER: marker}}
    if checkpoint_id:
        out["checkpoint_id"] = checkpoint_id
    return out


async def test_the_wake_resumes_the_checkpoint_the_interrupt_names(enqueued: list[dict[str, Any]]) -> None:
    await sleep_wake.schedule_sleep_wake(RUN, _interrupt(NEW))
    assert enqueued[0]["checkpoint_id"] == NEW


async def test_without_a_named_checkpoint_the_newest_equal_step_park_wins(enqueued: list[dict[str, Any]]) -> None:
    await sleep_wake.schedule_sleep_wake(RUN, _interrupt(None))
    assert enqueued[0]["checkpoint_id"] == NEW


async def test_the_callers_pointer_still_wins(enqueued: list[dict[str, Any]]) -> None:
    await sleep_wake.schedule_sleep_wake(RUN, _interrupt(NEW), last_checkpoint_id=OLD)
    assert enqueued[0]["checkpoint_id"] == OLD
