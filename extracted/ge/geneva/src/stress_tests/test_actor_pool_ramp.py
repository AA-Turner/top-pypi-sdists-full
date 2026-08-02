# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Test 2: Actor Ramp-up at Scale.

Verify that actor scheduling time scales roughly linearly and doesn't
regress.  Creates N actors directly, pings all in parallel, and measures
the wall-clock time until every actor is alive.

This directly measures Ray's actor scheduling overhead — the bottleneck
that can trip Geneva's stall detector before all workers are ready.

Runs on **local Ray** — no k8s cluster required.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import pytest
import ray

from stress_tests.bench_worker import BenchWorker
from stress_tests.stress_results import log_result, make_result, scale_params

_LOG = logging.getLogger(__name__)

TIMEOUT_S = 300.0


def _run_actor_ramp(num_actors: int) -> dict[str, Any]:
    """Create N actors, ping all, measure time-to-all-alive."""
    # Phase 1: Create all actors (async — returns handles immediately).
    t_create = time.monotonic()
    actors = [BenchWorker.remote() for _ in range(num_actors)]
    create_elapsed = time.monotonic() - t_create
    _LOG.info("Created %d actor handles in %.3fs", num_actors, create_elapsed)

    # Phase 2: Ping all actors in parallel — forces Ray to schedule them.
    t_ping = time.monotonic()
    ping_futures = [a.run.remote(0, busy_ms=0) for a in actors]

    # Collect results, tracking when each actor responds.
    latencies: list[float] = []
    errors = 0
    try:
        results = ray.get(ping_futures, timeout=TIMEOUT_S)
        ping_elapsed = time.monotonic() - t_ping
        # Each actor reports its task_start relative to our ping time.
        latencies.extend(r["task_start"] - t_ping for r in results)
    except ray.exceptions.GetTimeoutError:
        ping_elapsed = time.monotonic() - t_ping
        _LOG.error("Timed out waiting for actors at scale=%d", num_actors)
        errors = num_actors
    except Exception as exc:
        ping_elapsed = time.monotonic() - t_ping
        _LOG.error("Actor ramp failed at scale=%d: %s", num_actors, exc)
        errors = num_actors

    elapsed = time.monotonic() - t_create

    result = make_result(
        scale=num_actors,
        latencies=latencies,
        error_count=errors,
        elapsed_s=elapsed,
        metadata={
            "create_handles_s": create_elapsed,
            "ping_elapsed_s": ping_elapsed,
            "actors_responded": len(latencies),
        },
    )
    log_result(result)

    # Cleanup
    for a in actors:
        ray.kill(a)

    return {
        "result": result,
        "actors_responded": len(latencies),
        "create_handles_s": create_elapsed,
        "ping_elapsed_s": ping_elapsed,
    }


@pytest.mark.limit
@pytest.mark.parametrize(
    "num_actors",
    # Explore variants (>=400) are disabled: actor startup at high
    # scale exceeds the 5-min timeout on CI, blocking subsequent tests.
    scale_params([100, 200], explore_threshold=400),
)
def test_actor_pool_ramp_scale(local_ray: None, num_actors: int) -> None:
    """Actor scheduling reaches all N actors at increasing scale."""
    info = _run_actor_ramp(num_actors)

    result = info["result"]
    _LOG.info(
        "scale=%d actors_responded=%d create=%.3fs ping=%.3fs "
        "p50=%.3fs p90=%.3fs p99=%.3fs",
        num_actors,
        info["actors_responded"],
        info["create_handles_s"],
        info["ping_elapsed_s"],
        result.p50_latency_s,
        result.p90_latency_s,
        result.p99_latency_s,
    )

    assert info["actors_responded"] == num_actors, (
        f"Only {info['actors_responded']}/{num_actors} actors responded to ping"
    )
    assert result.error_count == 0, (
        f"{result.error_count} actors failed at scale={num_actors}"
    )
