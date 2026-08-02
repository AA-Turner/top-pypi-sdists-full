# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Test 1: JobTracker Mailbox Saturation.

Find the worker count where JobTracker round-trip latency exceeds
acceptable bounds.  The JobTracker is a Ray actor with max_concurrency=1,
so all calls are serialized.  This test floods it with batch_increment
calls from N concurrent actors and measures round-trip latency.

Two variants:

* ``test_jobtracker_saturation`` — pure mailbox throughput with
  ``enable_saves=False`` (DB isolated).  Measures the dict-update cost.
* ``test_jobtracker_save_path_does_not_block_mailbox`` — exercises the
  ``enable_saves=True`` path with slow/failing metric saves and verifies the
  mailbox stays responsive.  Regression for the wedge where an inline,
  awaited save (e.g. a cloud-auth retry storm) blocked the single-concurrency
  actor and stalled all progress/finalization.

Runs on **local Ray** — no k8s cluster required.  The JobTracker is a
pure in-process Ray actor; there is nothing cluster-specific about the
mailbox bottleneck being measured.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import pytest
import ray

from stress_tests.jobtracker_save_probe import InjectedSaveJobTracker
from stress_tests.stress_results import (
    StressResult,
    log_result,
    make_result,
    scale_params,
)

_LOG = logging.getLogger(__name__)

CALLS_PER_ACTOR = 50
METRICS_PAYLOAD: dict[str, int] = {
    "udf_processing_time": 100,
    "batch_checkpointing_time": 50,
    "read_io_time_ms": 200,
    "checkpoint_load_time_ms": 30,
    "read_task_total_time_ms": 400,
}

# Per-save injected latency for the save-path test (seconds).  Large enough
# that an inline (pre-fix) save would serialize into the mailbox and blow the
# wall-clock budget; backgrounded saves keep the flood far below it.
SLOW_SAVE_DELAY_S = 0.5

# Wall-clock budget for the flood to complete with slow/failing saves.  With
# backgrounded saves the flood finishes in seconds; a wedged mailbox (inline
# save) would exceed this and fail the test instead of hanging CI.
MAILBOX_RESPONSIVE_TIMEOUT_S = 120.0


@ray.remote(num_cpus=0, memory=128 * 1024**2)
class StressCallerActor:
    """Flood a JobTracker with batch_increment calls, measuring RTT."""

    def ping(self) -> bool:
        """No-op used to force actor initialization before measurement."""
        return True

    def flood_tracker(
        self, tracker_handle: Any, num_calls: int, payload: dict[str, int]
    ) -> list[float]:
        latencies: list[float] = []
        for _ in range(num_calls):
            t0 = time.monotonic()
            ray.get(tracker_handle.batch_increment.remote(payload))
            latencies.append(time.monotonic() - t0)
        return latencies


def _run_jobtracker_saturation(num_actors: int) -> StressResult:
    """Run a single scale-point of the JobTracker saturation test."""
    from geneva.runners.ray.jobtracker import job_tracker_options
    from geneva.table import TableReference

    # Create a lightweight TableReference (saves are disabled, so it won't be used).
    table_ref = TableReference(
        table_id=["stress", "jobtracker_test"],
        version=None,
        db_uri=None,
    )

    tracker = job_tracker_options().remote(
        job_id="stress-jobtracker-saturation",
        table_ref=table_ref,
        enable_saves=False,
    )

    actors = [StressCallerActor.remote() for _ in range(num_actors)]

    # Warmup: force all actors to initialize before starting the timer.
    _LOG.info("Warming up %d stress actors...", num_actors)
    warmup_t0 = time.monotonic()
    ray.get([a.ping.remote() for a in actors])
    _LOG.info(
        "Actor warmup completed in %.1fs for %d actors",
        time.monotonic() - warmup_t0,
        num_actors,
    )

    t0 = time.monotonic()
    futures = [
        a.flood_tracker.remote(tracker, CALLS_PER_ACTOR, METRICS_PAYLOAD)
        for a in actors
    ]
    all_latencies_per_actor: list[list[float]] = ray.get(futures)
    elapsed = time.monotonic() - t0

    # Flatten latencies across all actors.
    all_latencies: list[float] = []
    for actor_latencies in all_latencies_per_actor:
        all_latencies.extend(actor_latencies)

    error_count = 0
    total_expected = num_actors * CALLS_PER_ACTOR
    if len(all_latencies) < total_expected:
        error_count = total_expected - len(all_latencies)

    # Verify metric totals are correct (no lost updates).
    # Local Ray — no client proxy, so we can call the tracker directly.
    metrics: dict[str, dict[str, Any]] = ray.get(tracker.get_all.remote())
    expected_total = num_actors * CALLS_PER_ACTOR
    for key, value in METRICS_PAYLOAD.items():
        recorded = metrics.get(key, {}).get("n", 0)
        expected_n = expected_total * value
        if recorded != expected_n:
            _LOG.error(
                "Metric %s: expected %d, got %d (lost %d updates)",
                key,
                expected_n,
                recorded,
                expected_n - recorded,
            )
            error_count += abs(expected_n - recorded)

    result = make_result(
        scale=num_actors,
        latencies=all_latencies,
        error_count=error_count,
        elapsed_s=elapsed,
        metadata={
            "calls_per_actor": CALLS_PER_ACTOR,
            "metrics_per_call": len(METRICS_PAYLOAD),
            "total_calls": total_expected,
        },
    )
    log_result(result)

    # Cleanup
    ray.kill(tracker)
    for a in actors:
        ray.kill(a)

    return result


@pytest.mark.limit
@pytest.mark.parametrize(
    "num_actors",
    # Explore variants (>=200) are disabled: actor warmup hangs
    # indefinitely on CI, blocking all subsequent tests.
    scale_params([100], explore_threshold=200),
)
def test_jobtracker_saturation(local_ray: None, num_actors: int) -> None:
    """JobTracker mailbox round-trip latency at increasing concurrency."""
    result = _run_jobtracker_saturation(num_actors)

    assert result.error_count == 0, (
        f"Lost {result.error_count} updates at scale={num_actors}"
    )
    assert result.p99_latency_s < 30.0, (
        f"p99 latency {result.p99_latency_s:.1f}s exceeds 30s at scale={num_actors}"
    )


def _run_jobtracker_save_path(num_actors: int, *, fail: bool) -> StressResult:
    """Flood a JobTracker with saves enabled and slow/failing writes injected.

    With backgrounded saves, the flood of batch_increment calls must complete
    within ``MAILBOX_RESPONSIVE_TIMEOUT_S`` regardless of how slow the saves
    are. A regression to inline, awaited saves would serialize ~one save delay
    per call into the mailbox and exceed the budget.
    """
    from geneva.table import TableReference

    table_ref = TableReference(
        table_id=["stress", "jobtracker_save"],
        version=None,
        db_uri=None,
    )

    tracker = InjectedSaveJobTracker.options(
        max_concurrency=1, num_cpus=0, memory=256 * 1024**2
    ).remote(
        job_id="stress-jobtracker-save-path",
        table_ref=table_ref,
        enable_saves=True,
        # Save on every update so the (slow/failing) save path is hammered:
        # a 0s initial interval with no ramp -> never throttled.
        min_update_interval_secs=0.0,
        max_update_interval_secs=0.0,
        update_interval_ramp=0.0,
    )
    ray.get(tracker.configure_injected_save.remote(SLOW_SAVE_DELAY_S, fail))

    actors = [StressCallerActor.remote() for _ in range(num_actors)]

    _LOG.info("Warming up %d stress actors...", num_actors)
    ray.get([a.ping.remote() for a in actors])

    t0 = time.monotonic()
    futures = [
        a.flood_tracker.remote(tracker, CALLS_PER_ACTOR, METRICS_PAYLOAD)
        for a in actors
    ]
    try:
        all_latencies_per_actor: list[list[float]] = ray.get(
            futures, timeout=MAILBOX_RESPONSIVE_TIMEOUT_S
        )
    except ray.exceptions.GetTimeoutError:
        ray.kill(tracker)
        for a in actors:
            ray.kill(a)
        pytest.fail(
            f"JobTracker mailbox wedged: flood of {num_actors} senders did not "
            f"complete within {MAILBOX_RESPONSIVE_TIMEOUT_S:.0f}s while saves "
            f"were {'failing' if fail else 'slow'} (save_delay="
            f"{SLOW_SAVE_DELAY_S}s). Saves are blocking the actor mailbox."
        )
    elapsed = time.monotonic() - t0

    all_latencies: list[float] = []
    for actor_latencies in all_latencies_per_actor:
        all_latencies.extend(actor_latencies)

    error_count = 0
    total_expected = num_actors * CALLS_PER_ACTOR
    if len(all_latencies) < total_expected:
        error_count = total_expected - len(all_latencies)

    # Saves are async, but metric counters update in-memory before scheduling a
    # save, so totals must always be exact regardless of save progress.
    metrics: dict[str, dict[str, Any]] = ray.get(tracker.get_all.remote())
    for key, value in METRICS_PAYLOAD.items():
        recorded = metrics.get(key, {}).get("n", 0)
        expected_n = total_expected * value
        if recorded != expected_n:
            _LOG.error(
                "Metric %s: expected %d, got %d (lost %d updates)",
                key,
                expected_n,
                recorded,
                expected_n - recorded,
            )
            error_count += abs(expected_n - recorded)

    save_attempts = ray.get(tracker.injected_save_attempts.remote())

    result = make_result(
        scale=num_actors,
        latencies=all_latencies,
        error_count=error_count,
        elapsed_s=elapsed,
        metadata={
            "save_mode": "failing" if fail else "slow",
            "save_delay_s": SLOW_SAVE_DELAY_S,
            "save_attempts": save_attempts,
            "total_calls": total_expected,
        },
    )
    log_result(result)

    ray.kill(tracker)
    for a in actors:
        ray.kill(a)

    return result


@pytest.mark.limit
@pytest.mark.parametrize("fail", [False, True], ids=["slow", "failing"])
@pytest.mark.parametrize(
    "num_actors",
    # Explore variants (>=200) disabled for the same reason as Test 1.
    scale_params([100], explore_threshold=200),
)
def test_jobtracker_save_path_does_not_block_mailbox(
    local_ray: None, num_actors: int, fail: bool
) -> None:
    """Slow/failing metric saves must not wedge the JobTracker mailbox.

    Regression for the wedge where ``_save_metrics`` was awaited inline on the
    ``max_concurrency=1`` actor, so a stalled system-DB write (e.g. Azure auth
    retry storm) blocked all progress increments and job finalization.
    """
    result = _run_jobtracker_save_path(num_actors, fail=fail)

    # No lost updates: in-memory counters are independent of save success.
    assert result.error_count == 0, (
        f"Lost {result.error_count} updates at scale={num_actors} (fail={fail})"
    )

    # The save path was actually exercised (enable_saves=True engaged).
    assert result.metadata["save_attempts"] >= 1, (
        "expected at least one save attempt with enable_saves=True"
    )

    # Backgrounded saves must not serialize into the mailbox. An inline save
    # would cost ~one save delay per call; require well under that.
    serialized_budget = num_actors * CALLS_PER_ACTOR * SLOW_SAVE_DELAY_S
    assert result.elapsed_s < serialized_budget * 0.2, (
        f"flood took {result.elapsed_s:.1f}s — saves appear to be blocking the "
        f"mailbox (serialized budget {serialized_budget:.0f}s, fail={fail})"
    )
    assert result.p99_latency_s < 30.0, (
        f"p99 latency {result.p99_latency_s:.1f}s exceeds 30s at "
        f"scale={num_actors} (fail={fail})"
    )
