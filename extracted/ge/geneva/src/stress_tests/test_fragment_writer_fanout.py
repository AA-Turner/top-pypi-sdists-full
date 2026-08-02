# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Test 3: Fragment Writer Actor Count Stress.

Find the actor count where writer creation fails, OOMs, or hits the
10k Ray actor cap.  Creates N Queue + N FakeWriter actor pairs and
pumps checkpoint-sized messages through each.

Runs on **local Ray** — no k8s cluster required.  Pure Ray actor/queue test.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import pytest
import ray
import ray.exceptions
import ray.util.queue

from stress_tests.stress_results import log_result, make_result, scale_params

_LOG = logging.getLogger(__name__)

CHECKPOINTS_PER_FRAGMENT = 5


@ray.remote(num_cpus=0, memory=128 * 1024**2)
class FakeWriter:
    """Drain a queue until a seal signal (negative offset) arrives."""

    def write(self, queue: ray.util.queue.Queue) -> dict[str, Any]:
        t0 = time.monotonic()
        batches_received = 0
        while True:
            msg = queue.get()
            if msg[0] < 0:  # seal signal
                break
            batches_received += 1
        return {
            "elapsed_s": time.monotonic() - t0,
            "batches_received": batches_received,
        }


def _run_fragment_writer_fanout(num_fragments: int) -> dict[str, Any]:
    """Run a single scale-point of the writer fanout test."""
    # Phase 1: Create all queue + writer actor pairs.
    t_create_start = time.monotonic()
    queues: list[ray.util.queue.Queue] = []
    writers: list[Any] = []
    for _ in range(num_fragments):
        q = ray.util.queue.Queue(actor_options={"num_cpus": 0, "memory": 64 * 1024**2})
        queues.append(q)
        writers.append(FakeWriter.remote())
    creation_time = time.monotonic() - t_create_start
    _LOG.info("Created %d queue+writer pairs in %.1fs", num_fragments, creation_time)

    total_actors = num_fragments * 2  # queue actors + writer actors
    _LOG.info("Total actor count: %d", total_actors)

    # Phase 2: Start all writers draining their queues.
    write_futures = [w.write.remote(q) for w, q in zip(writers, queues, strict=True)]

    # Phase 3: Pump checkpoint messages.
    t_pump_start = time.monotonic()
    for q in queues:
        for offset in range(CHECKPOINTS_PER_FRAGMENT):
            q.put((offset, f"ckpt_{offset}"))
        q.put((-1, "seal"))  # seal signal
    pump_time = time.monotonic() - t_pump_start
    total_msgs = num_fragments * (CHECKPOINTS_PER_FRAGMENT + 1)
    _LOG.info("Pumped %d messages in %.1fs", total_msgs, pump_time)

    # Phase 4: Collect results.
    t_collect_start = time.monotonic()
    errors = 0
    latencies: list[float] = []
    try:
        results = ray.get(write_futures, timeout=600.0)
        for r in results:
            latencies.append(r["elapsed_s"])
            if r["batches_received"] != CHECKPOINTS_PER_FRAGMENT:
                errors += 1
    except ray.exceptions.GetTimeoutError:
        _LOG.error("Timed out waiting for writers at scale=%d", num_fragments)
        errors += num_fragments
    collect_time = time.monotonic() - t_collect_start

    elapsed = time.monotonic() - t_create_start
    result = make_result(
        scale=num_fragments,
        latencies=latencies,
        error_count=errors,
        elapsed_s=elapsed,
        metadata={
            "checkpoints_per_fragment": CHECKPOINTS_PER_FRAGMENT,
            "total_actors": total_actors,
            "creation_time_s": creation_time,
            "pump_time_s": pump_time,
            "collect_time_s": collect_time,
        },
    )
    log_result(result)
    return {
        "result": result,
        "total_actors": total_actors,
        "completed": len(latencies),
    }


@pytest.mark.limit
@pytest.mark.parametrize(
    "num_fragments",
    # Explore variants (>=200) are skipped: the queue.put() pump loop has
    # no timeout and deadlocks when actors OOM, causing the CI job to hang
    # for hours.  Keep regression baseline at 100 fragments.
    scale_params([100], id_prefix="fragments", explore_threshold=200),
)
def test_fragment_writer_fanout(local_ray: None, num_fragments: int) -> None:
    """Writer actor creation and message passing at increasing scale."""
    info = _run_fragment_writer_fanout(num_fragments)

    result = info["result"]
    assert info["completed"] == num_fragments, (
        f"Only {info['completed']}/{num_fragments} writers completed"
    )
    assert result.error_count == 0, (
        f"{result.error_count} writers received wrong checkpoint count"
    )
    assert info["total_actors"] < 10_000, (
        f"Total actor count {info['total_actors']} exceeds 10,000"
    )
