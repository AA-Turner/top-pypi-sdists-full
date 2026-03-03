"""Tests for chronos dev startup profiling helpers."""

from __future__ import annotations

import pytest

from plato.cli.chronos.dev.profiling import StartupProfiler


def _now_factory(values: list[float]):
    it = iter(values)
    return lambda: next(it)


def test_start_stop_accumulates():
    profiler = StartupProfiler(now=_now_factory([10.0, 12.0, 20.0, 21.5]))

    profiler.start("step.a")
    elapsed_a = profiler.stop("step.a")
    profiler.start("step.a")
    elapsed_b = profiler.stop("step.a")

    assert elapsed_a == pytest.approx(2.0)
    assert elapsed_b == pytest.approx(1.5)
    assert profiler.durations()["step.a"] == pytest.approx(3.5)


def test_time_context_and_sorting():
    profiler = StartupProfiler(now=_now_factory([1.0, 4.5, 5.0, 5.7]))

    with profiler.time("slow"):
        pass
    with profiler.time("fast"):
        pass

    rows = profiler.sorted_durations()
    assert rows[0][0] == "slow"
    assert rows[0][1] == pytest.approx(3.5)
    assert rows[1][0] == "fast"
    assert rows[1][1] == pytest.approx(0.7)

    filtered = profiler.sorted_durations(exclude={"slow"})
    assert filtered == [("fast", pytest.approx(0.7))]


@pytest.mark.anyio
async def test_async_time_context():
    profiler = StartupProfiler(now=_now_factory([100.0, 100.25]))

    async with profiler.atime("async.step"):
        pass

    assert profiler.durations()["async.step"] == pytest.approx(0.25)
