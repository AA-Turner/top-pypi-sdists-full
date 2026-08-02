# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# Reproduces a thundering write herd against the GCS auth token metadata server from
# Ray workers.  Complements the read-path stampede in test_metadata_stampede.py.
#
# In production, many CheckpointingApplier actors write disjoint checkpoint keys
# concurrently.  When UDF processing is fast or many actors start at once (job
# startup), the resulting burst of PUTs stresses connection reuse and auth/metadata
# token refresh on the object store — the same class of stampede the read test
# exercises, but on the write side.
#
# Runs on **local Ray** — no k8s cluster required.  GCS credentials come from
# the CI runner's environment (gcloud auth).

from __future__ import annotations

import logging
import time

import pyarrow as pa
import pytest
import ray
from yarl import URL

_LOG = logging.getLogger(__name__)

KEY_PREFIX: str = "stampede-test/ckpts-write"


@ray.remote(num_cpus=0.1, memory=256 * 1024**2, max_restarts=1, max_task_retries=3)
class StoreWriter:
    """
    One actor = one process = one FlatLanceCheckpointStore.
    Writes a *disjoint* shard of keys so no two writers collide,
    mirroring how CheckpointingApplier actors each own their own
    fragment's checkpoint keyspace.
    """

    def __init__(self, root: str) -> None:
        from geneva.checkpoint import FlatLanceCheckpointStore

        # Only session-based FlatLanceCheckpointStore is tested. The
        # ``checkpointer`` parameter was previously parametrized over
        # "session" and "file", but FlatLanceCheckpointStore does not accept a
        # mode argument — both variants ran identical code.
        self.store = FlatLanceCheckpointStore(root)

    def run(self, start: int, count: int) -> int:
        ok = 0
        for i in range(count):
            key = f"{start + i:08d}"
            batch = pa.record_batch({"a": [start + i]})  # type: ignore[arg-type]
            self.store[key] = batch
            ok += 1
        _LOG.info(
            "writer %s wrote %d keys (start=%d, count=%d)",
            ray.get_runtime_context().get_actor_id(),
            ok,
            start,
            count,
        )
        return ok


def _shard_ranges(total: int, parts: int) -> list[tuple[int, int]]:
    """Split ``total`` as evenly as possible across ``parts``.

    Returns a list of ``(start, count)`` tuples whose counts sum to ``total``.
    """
    base = total // parts
    rem = total % parts
    ranges: list[tuple[int, int]] = []
    acc = 0
    for i in range(parts):
        count = base + (1 if i < rem else 0)
        ranges.append((acc, count))
        acc += count
    return ranges


_explore_marks = [
    pytest.mark.stress_explore,
    pytest.mark.xfail(strict=False, reason="explore: probing for write scale limits"),
]


@pytest.mark.limit
@pytest.mark.gcp_only
@pytest.mark.parametrize(
    ("scale", "ops_per_actor"),
    [
        pytest.param(10, 500, id="10x500"),
        pytest.param(20, 500, id="20x500", marks=_explore_marks),
        pytest.param(40, 500, id="40x500", marks=_explore_marks),
    ],
)
def test_lance_checkpoint_write_stampede(
    local_ray: None,
    geneva_test_bucket: str,
    scale: int,
    ops_per_actor: int,
) -> None:
    """
    WRITE-path stampede: N actors, each with its own FlatLanceCheckpointStore,
    writing disjoint checkpoint keys as fast as possible.

    Exercises connection reuse, auth/metadata token refresh churn, and
    object PUT throughput under concurrent pressure — the write-side
    complement to test_lance_checkpoint_single_store_many_reads_per_file.
    """
    ckp_root = str(URL(geneva_test_bucket) / KEY_PREFIX)

    if not ckp_root.startswith("gs://"):
        pytest.skip("Requires GCS-backed geneva_test_bucket")

    keys_total = scale * ops_per_actor

    _LOG.info(
        "starting write stampede: actors=%d ops/actor=%d total_keys=%d",
        scale,
        ops_per_actor,
        keys_total,
    )

    writers = [
        StoreWriter.options(num_cpus=0.25).remote(ckp_root) for _ in range(scale)
    ]

    ranges = _shard_ranges(keys_total, scale)

    refs = [
        w.run.remote(start, count)  # type: ignore[attr-defined]
        for w, (start, count) in zip(writers, ranges, strict=False)
    ]

    failures = 0
    successes = 0
    # Actors run in parallel, so timeout scales with per-actor ops, not
    # total ops. In CI, local Ray workers may spend noticeable time creating
    # their runtime package/venv before the first object-store write, so keep a
    # larger startup buffer than the regular unit-test suites. The per-op
    # budget still needs to cover retry_lance backoff under transient GCS
    # contention.
    total_timeout = max(600.0, ops_per_actor * 0.4 + 120.0)
    deadline = time.monotonic() + total_timeout

    for ref in refs:
        remaining = max(1.0, deadline - time.monotonic())
        try:
            successes += ray.get(ref, timeout=remaining)  # type: ignore[operator]
        except Exception as e:  # noqa: PERF203
            failures += 1
            _LOG.warning("writer actor failed: %r", e)

    _LOG.info(
        "write stampede summary: actors=%d ops/actor=%d "
        "total_keys=%d successes=%d failures=%d root=%s",
        scale,
        ops_per_actor,
        keys_total,
        successes,
        failures,
        ckp_root,
    )

    assert failures == 0, f"Expected all to complete; saw {failures} failures"
