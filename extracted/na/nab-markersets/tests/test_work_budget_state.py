"""Bounded marker operations keep their work state within each thread."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest

from nab_markersets import _markersets as engine

_THREAD_TIMEOUT_SECONDS = 10.0


def test_a_fresh_thread_can_compare_without_a_work_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(engine._work_meter, "remaining", 7, raising=False)

    def compare() -> tuple[bool, int | None]:
        """Exercise unmetered operations in a fresh worker thread."""
        engine.charge_work(1)
        equivalent = engine.equivalent_within_rows(
            engine.TRUE, engine.TRUE, engine.TRUE, 1
        )
        return equivalent, engine._work_meter.remaining

    with ThreadPoolExecutor(max_workers=1) as pool:
        assert pool.submit(compare).result(timeout=_THREAD_TIMEOUT_SECONDS) == (
            True,
            None,
        )

    assert engine._work_meter.remaining == 7


def test_two_threads_debit_only_their_own_work_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(engine._work_meter, "remaining", 777, raising=False)
    ready = Barrier(2, timeout=_THREAD_TIMEOUT_SECONDS)

    def spend(budget_and_charge: tuple[int, int]) -> tuple[int | None, int | None]:
        """Synchronize active workers before debiting their own budgets."""
        budget, units = budget_and_charge
        initial = engine._work_meter.remaining
        engine._work_meter.remaining = budget
        ready.wait()
        engine.charge_work(units)
        return initial, engine._work_meter.remaining

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(spend, [(17, 3), (29, 5)]))

    assert results == [(None, 14), (None, 24)]
    assert engine._work_meter.remaining == 777
