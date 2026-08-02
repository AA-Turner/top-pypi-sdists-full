# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Test 9 (P0): Object Store IOPS and Throughput Limits.

Find the concurrency level where object store throttling causes task
failures or stall detection false positives.  Spawns N actors that each
perform a burst of small object store operations against the same prefix.

Runs on **local Ray** — no k8s cluster required.  GCS credentials come
from the CI runner's environment (gcloud auth).
"""

from __future__ import annotations

import logging
import statistics
import time
from typing import Any

import pytest
import ray
import ray.exceptions

from stress_tests.stress_results import (
    log_result,
    make_result,
    percentile,
    scale_params,
)

_LOG = logging.getLogger(__name__)

OPS_PER_ACTOR = 200
OBJECT_SIZE_BYTES = 1024  # 1 KB


@ray.remote(num_cpus=0.02, memory=128 * 1024**2)
class IOPSStressActor:
    """Burst small-object reads and writes against an object store prefix."""

    def burst_io(
        self, store_prefix: str, num_ops: int, actor_idx: int
    ) -> dict[str, Any]:
        import pyarrow.fs as pafs

        fs, path = pafs.FileSystem.from_uri(store_prefix)
        write_times: list[float] = []
        read_times: list[float] = []
        errors = 0
        error_details: list[str] = []
        payload = b"x" * OBJECT_SIZE_BYTES

        for i in range(num_ops):
            # All actors write under the same prefix so they contend on the
            # same storage partition.  Object stores (S3, GCS) distribute load
            # by key prefix — separate sub-dirs would spread requests across
            # partitions and bypass the per-prefix throttling this test targets.
            #
            # S3:  3,500 PUT / 5,500 GET per prefix/s (automatic partitioning).
            # GCS: ~1,000 writes/s initial, auto-scales by key-name range.
            #
            # Refs:
            #   https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html
            #   https://docs.cloud.google.com/storage/docs/request-rate
            key = f"{path}/stress_{actor_idx}_{i}.bin"
            try:
                t0 = time.monotonic()
                with fs.open_output_stream(key) as f:
                    f.write(payload)
                write_times.append(time.monotonic() - t0)

                t0 = time.monotonic()
                with fs.open_input_stream(key) as f:
                    f.read()
                read_times.append(time.monotonic() - t0)
            except Exception as exc:
                errors += 1
                if len(error_details) < 10:  # cap stored error details
                    error_details.append(f"{type(exc).__name__}: {exc}")

        def _safe_median(vals: list[float]) -> float:
            return statistics.median(vals) if vals else 0.0

        return {
            "write_p50": _safe_median(write_times),
            "write_p99": percentile(write_times, 99),
            "read_p50": _safe_median(read_times),
            "read_p99": percentile(read_times, 99),
            "write_times": write_times,
            "read_times": read_times,
            "errors": errors,
            "error_details": error_details,
            "total_ops": num_ops * 2,
        }


def _run_object_store_iops(num_actors: int, store_prefix: str) -> dict[str, Any]:
    """Run a single scale-point of the IOPS stress test."""
    actors = [IOPSStressActor.remote() for _ in range(num_actors)]

    t0 = time.monotonic()
    futures = [
        a.burst_io.remote(store_prefix, OPS_PER_ACTOR, idx)
        for idx, a in enumerate(actors)
    ]

    # Generous timeout: each actor does OPS_PER_ACTOR ops, allow 30s per op worst case.
    timeout = max(600.0, OPS_PER_ACTOR * 30)
    try:
        results = ray.get(futures, timeout=timeout)
    except ray.exceptions.GetTimeoutError:
        _LOG.error("Timed out waiting for IOPS actors at scale=%d", num_actors)
        results = []

    elapsed = time.monotonic() - t0

    # Aggregate across all actors.
    all_write_times: list[float] = []
    all_read_times: list[float] = []
    total_errors = 0
    all_error_details: list[str] = []

    for r in results:
        all_write_times.extend(r["write_times"])
        all_read_times.extend(r["read_times"])
        total_errors += r["errors"]
        all_error_details.extend(r["error_details"])

    all_latencies = all_write_times + all_read_times
    total_ops = len(all_latencies)

    result = make_result(
        scale=num_actors,
        latencies=all_latencies,
        error_count=total_errors,
        elapsed_s=elapsed,
        metadata={
            "ops_per_actor": OPS_PER_ACTOR,
            "object_size_bytes": OBJECT_SIZE_BYTES,
            "total_ops": total_ops,
            "aggregate_ops_per_sec": total_ops / elapsed if elapsed > 0 else 0.0,
            "write_p50": statistics.median(all_write_times) if all_write_times else 0.0,
            "write_p99": percentile(all_write_times, 99),
            "read_p50": statistics.median(all_read_times) if all_read_times else 0.0,
            "read_p99": percentile(all_read_times, 99),
            "error_count_by_actor": [r["errors"] for r in results],
            "error_samples": all_error_details[:20],
        },
    )
    log_result(result)

    # Cleanup actors.
    for a in actors:
        ray.kill(a)

    return {
        "result": result,
        "total_ops": total_ops,
        "total_errors": total_errors,
        "elapsed_s": elapsed,
    }


@pytest.mark.limit
@pytest.mark.gcp_only
@pytest.mark.parametrize(
    "num_actors",
    # Explore variants (>=200) are disabled: actor startup hangs
    # indefinitely on CI, blocking all subsequent tests.
    scale_params([50, 100], id_prefix="actors", explore_threshold=200),
)
def test_object_store_iops(
    local_ray: None, num_actors: int, tmp_dataset_uri: str
) -> None:
    """Object store IOPS at increasing concurrency.

    Reports the concurrency where error rate > 1% or p99 > 10s.
    """
    store_prefix = tmp_dataset_uri.rstrip("/") + "/iops_stress"

    info = _run_object_store_iops(num_actors, store_prefix)

    result = info["result"]

    _LOG.info(
        "scale=%d total_ops=%d errors=%d (%.2f%%) p99=%.3fs "
        "aggregate_ops/s=%.0f elapsed=%.1fs",
        num_actors,
        info["total_ops"],
        info["total_errors"],
        result.error_rate * 100,
        result.p99_latency_s,
        result.metadata.get("aggregate_ops_per_sec", 0),
        info["elapsed_s"],
    )

    # The test reports findings rather than failing hard — the goal is
    # to discover the breaking point, not enforce a fixed threshold.
    if result.error_rate > 0.01:
        _LOG.warning(
            "ERROR RATE >1%%: %.2f%% at scale=%d",
            result.error_rate * 100,
            num_actors,
        )
    if result.p99_latency_s > 10.0:
        _LOG.warning(
            "P99 >10s: %.1fs at scale=%d",
            result.p99_latency_s,
            num_actors,
        )
