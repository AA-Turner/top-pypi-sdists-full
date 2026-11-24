"""``item_settled`` never raises and never builds a paced dispatch (review 2026-11-10, finding 7).

``_emit_item_settled`` says "Never raises", yet it looked the item's wave up OUTSIDE its try, through
``_pace_for`` — which also CREATES a ``PacedDispatch`` entry for an item whose entry is gone. A progress
event must be a pure read: a failing wave lookup costs only the event, and the scheduler's pace table is
the same after the event as before it.

Since lane A2f (2026-11-19) the event carries no wave at all (a per-page line rides the step's ``says``), so it
never reads the pace table: a broken table cannot cost the event.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from matrx_graph.executor.scheduler import Scheduler


def _result() -> Any:
    inv = SimpleNamespace(
        node_id="each_page", dispatch_id="d1", item_index=3, attempt=1, pace={"wave_size": "2"}, inputs={}, step=None
    )
    return SimpleNamespace(
        interrupt=None, replayed=False, held=False, error=None, failure=None, user_skipped=False,
        reused=False, output={"ok": 1}, settled_dump=None, invocation=inv,
    )  # fmt: skip


def _scheduler(**over: Any) -> Any:
    sent: list[Any] = []

    async def _emit(event: Any) -> None:
        sent.append(event)

    async def _says(*_a: Any, **_k: Any) -> None:
        return None

    async def _raise_says_flags() -> None:
        return None

    # ``_loop_step``: the step a tally's pass is (says F1); ``_raise_says_flags``: flags written after the event (F2).
    fake = SimpleNamespace(_paced={}, _emit=_emit, sent=sent, _item_tallies={}, _dispatch_expected={}, _says=_says,
                           _loop_step=None, _raise_says_flags=_raise_says_flags)
    fake._pace_for = lambda inv: Scheduler._pace_for(fake, inv)
    # The item count (``{done}`` ``{failed}`` ``{total}``) is the scheduler's own, read through its real methods.
    fake._item_tally = lambda inv: Scheduler._item_tally(fake, inv)
    fake._items_total = lambda inv: Scheduler._items_total(fake, inv)
    for key, value in over.items():
        setattr(fake, key, value)
    return fake


async def test_the_event_never_creates_a_paced_dispatch() -> None:
    fake = _scheduler()
    await Scheduler._emit_item_settled(fake, "run-1", 2, _result(), {})
    assert fake._paced == {}, "a progress event must not build a pace entry as a side effect"
    assert len(fake.sent) == 1 and not hasattr(fake.sent[0], "first_in_wave")
    assert (fake.sent[0].done, fake.sent[0].failed, fake.sent[0].total) == (1, 0, None)


async def test_a_broken_pace_table_never_costs_the_event() -> None:
    class _Broken(dict):
        def get(self, *_a: Any, **_k: Any) -> Any:
            raise RuntimeError("pace table unreadable")

    def _boom(_inv: Any) -> Any:
        raise RuntimeError("pace table unreadable")

    fake = _scheduler(_paced=_Broken(), _pace_for=_boom)
    await Scheduler._emit_item_settled(fake, "run-1", 2, _result(), {})  # must not raise
    assert len(fake.sent) == 1, "the event never reads the pace table, so a broken one cannot cost it"
