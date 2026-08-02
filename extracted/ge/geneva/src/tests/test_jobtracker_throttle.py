# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for the JobTracker duration-aware save throttle (GEN-566).

These are pure in-process tests — no Ray runtime required. They cover the
duration-aware interval schedule (interval grows proportionally with runtime),
config defaults / construction kwargs, the actor's use of the schedule, and the
invariant that forced/terminal saves bypass the throttle.
"""

import asyncio
import time
from typing import Any

import pytest

from geneva.runners.ray.jobtracker import (
    JobTrackerConfig,
    _JobTracker,
    compute_update_interval,
    job_tracker_throttle_kwargs,
)
from geneva.table import TableReference

_TABLE_REF = TableReference(table_id=["t"], version=None, db_uri=None)


def test_job_tracker_config_defaults() -> None:
    """Defaults: start at 10s, interval ~= runtime/60, cap at 5 min."""
    c = JobTrackerConfig()
    assert c.min_update_interval_secs == 10.0
    assert c.max_update_interval_secs == 300.0
    assert c.update_interval_ramp == 60.0
    assert JobTrackerConfig.name() == "geneva_job_tracker"


@pytest.mark.parametrize(
    ("elapsed", "expected"),
    [
        (0.0, 10.0),  # job start -> initial interval
        (300.0, 10.0),  # 5 min in: 300/60=5 -> still clamped to min
        (1200.0, 20.0),  # 20 min in: 1200/60
        (1800.0, 30.0),  # 30 min in: 1800/60
        (6000.0, 100.0),  # ~1.7h in: 6000/60
        (18000.0, 300.0),  # 5h in: 18000/60=300 -> the cap
        (100000.0, 300.0),  # long job -> capped
    ],
)
def test_compute_update_interval_grows_proportionally(
    elapsed: float, expected: float
) -> None:
    """Interval ~= elapsed/ramp, clamped to [min, max]."""
    assert (
        compute_update_interval(elapsed, min_secs=10.0, max_secs=300.0, ramp=60.0)
        == expected
    )


def test_compute_update_interval_flat_when_ramp_disabled() -> None:
    """ramp <= 0 holds a flat min interval (no ramp)."""
    for elapsed in (0.0, 60.0, 100_000.0):
        assert (
            compute_update_interval(elapsed, min_secs=15.0, max_secs=300.0, ramp=0.0)
            == 15.0
        )


def test_compute_update_interval_clamps_to_min() -> None:
    """Negative/zero elapsed never drops below the initial interval."""
    assert (
        compute_update_interval(-5.0, min_secs=10.0, max_secs=300.0, ramp=60.0) == 10.0
    )


def test_job_tracker_throttle_kwargs_from_config() -> None:
    """Construction kwargs come straight from config; override sets the floor."""
    c = JobTrackerConfig()
    assert job_tracker_throttle_kwargs(config=c) == {
        "min_update_interval_secs": 10.0,
        "max_update_interval_secs": 300.0,
        "update_interval_ramp": 60.0,
    }

    overridden = job_tracker_throttle_kwargs(override_min_interval_secs=30.0, config=c)
    assert overridden["min_update_interval_secs"] == 30.0
    assert overridden["max_update_interval_secs"] == 300.0  # ceiling preserved

    # An override above the ceiling raises the ceiling so it never sits below min.
    high = job_tracker_throttle_kwargs(
        override_min_interval_secs=600.0,
        config=JobTrackerConfig(max_update_interval_secs=300.0),
    )
    assert high["min_update_interval_secs"] == 600.0
    assert high["max_update_interval_secs"] == 600.0


def test_actor_interval_grows_with_runtime() -> None:
    """The actor throttles using the duration-aware schedule from job start."""
    tracker = _JobTracker(
        job_id="j",
        table_ref=_TABLE_REF,
        min_update_interval_secs=10.0,
        max_update_interval_secs=300.0,
        update_interval_ramp=60.0,
    )
    now = time.time()
    tracker._job_start_time = now
    assert tracker._current_update_interval(now) == 10.0
    assert tracker._current_update_interval(now + 1200) == 20.0
    assert tracker._current_update_interval(now + 18000) == 300.0  # capped


class _CountingTracker(_JobTracker):
    """In-process JobTracker that counts save attempts instead of writing."""

    def _arm(self) -> None:
        self.saves = 0

    async def _save_metrics(self, _metrics: dict[str, dict]) -> None:  # type: ignore[override]
        self.saves += 1


async def _run_and_drain(tracker: _CountingTracker, coro: Any) -> None:
    """Run an actor op and wait for any background save it scheduled."""
    await coro
    task = tracker._save_task
    if task is not None:
        await asyncio.wait_for(task, timeout=2.0)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("interval", "expect_intermediate_save"),
    [(0.0, True), (1000.0, False)],
)
async def test_throttle_suppresses_intermediate_and_forced_bypasses(
    interval: float, expect_intermediate_save: bool
) -> None:
    """A flat interval throttles intermediate saves; forced ones always bypass.

    With interval=0 every update flushes; with a large interval intermediate
    (non-forced) updates are suppressed. A terminal ``mark_done`` always saves.
    (``ramp=0`` holds the interval flat so the schedule doesn't move underneath
    the assertions.)
    """
    tracker = _CountingTracker(
        job_id="j",
        table_ref=_TABLE_REF,
        min_update_interval_secs=interval,
        max_update_interval_secs=max(interval, 1.0),
        update_interval_ramp=0.0,
    )
    tracker._arm()

    # First update always flushes (last_updated starts at -inf).
    await _run_and_drain(tracker, tracker.set_total("m", 100))
    base = tracker.saves
    assert base >= 1

    # A non-forced intermediate update is gated by the configured interval.
    await _run_and_drain(tracker, tracker.set("m", 50))
    intermediate = tracker.saves - base
    assert (intermediate > 0) is expect_intermediate_save

    # A terminal/forced save bypasses the throttle in all cases.
    saves_before_done = tracker.saves
    await _run_and_drain(tracker, tracker.mark_done("m"))
    assert tracker.saves > saves_before_done


@pytest.mark.asyncio
async def test_save_pressure_counters_distinguish_throttled_and_forced() -> None:
    """get_save_stats() separates throttle-driven saves from forced ones."""
    tracker = _CountingTracker(
        job_id="j",
        table_ref=_TABLE_REF,
        min_update_interval_secs=1000.0,
        max_update_interval_secs=1000.0,
        update_interval_ramp=0.0,
    )
    tracker._arm()

    # First update flushes via the throttled path.
    await _run_and_drain(tracker, tracker.set_total("m", 2))
    # Completing the metric forces a save that bypasses the throttle.
    await _run_and_drain(tracker, tracker.increment("m", 2))

    stats = tracker.get_save_stats()
    assert stats["throttled_saves"] == 1
    assert stats["forced_saves"] == 1
    # Saves are no-ops here (no DB), so no real writes were counted.
    assert stats["save_writes"] == 0
    assert stats["min_update_interval_secs"] == 1000.0
