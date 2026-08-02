# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# Reproduces a thundering read herd against the GCS auth token metadata server from Ray
# workers.
#
# Runs on **local Ray** — no k8s cluster required.  GCS credentials come from
# the CI runner's environment (gcloud auth).

from __future__ import annotations

import logging
import time
from typing import Any

import pyarrow as pa
import pytest
import ray
from yarl import URL

_LOG = logging.getLogger(__name__)

KEYSET_SIZE: int = 500  # unique checkpoint files to cycle over
KEY_PREFIX: str = "stampede-test/ckpts"  # subdir under root


def _ensure_keyset(store: Any, n: int) -> list[str]:
    """Create n tiny checkpoint files if missing; return their keys."""
    keys: list[str] = []
    batch = pa.record_batch({"a": [1]})  # type: ignore[arg-type]
    for i in range(n):
        key = f"{i:06d}"
        keys.append(key)
        # avoid double-touch: try get and write only if absent
        try:
            if key not in store:
                store[key] = batch
        except Exception:
            # Some stores (or perms) might not allow contains; fall back to best effort
            try:
                store[key] = batch
            except Exception as e:
                raise RuntimeError(
                    f"Failed to prepare checkpoint key {key}: {e}"
                ) from e
    return keys


@ray.remote(num_cpus=0.1, memory=256 * 1024**2, max_restarts=1, max_task_retries=3)
class StoreReader:
    """One actor = one process = one FlatLanceCheckpointStore. Single-threaded, many
    sequential reads."""

    def __init__(self, root: str, mode: str) -> None:
        self.mode = mode
        from geneva.checkpoint import FlatLanceCheckpointStore

        # Only session-based FlatLanceCheckpointStore is tested. The
        # ``checkpointer`` parameter was previously parametrized over
        # "session" and "file", but FlatLanceCheckpointStore does not accept a
        # mode argument — both variants ran identical code.
        self.store = FlatLanceCheckpointStore(root)

    def run(self, keys: list[str], ops: int) -> int:
        ok = 0
        if self.mode == "getitem":
            for i in range(ops):
                _ = self.store[keys[i % len(keys)]]
                ok += 1
            _LOG.info(
                "reader %s completed %d getitem ops",
                ray.get_runtime_context().get_actor_id(),
                ok,
            )
            return ok

        # "contains" mode
        for i in range(ops):
            _ = keys[i % len(keys)] in self.store
            ok += 1
        _LOG.info(
            "reader %s completed %d contains ops",
            ray.get_runtime_context().get_actor_id(),
            ok,
        )
        return ok


_explore_marks = [
    pytest.mark.stress_explore,
    pytest.mark.xfail(strict=False, reason="explore: probing for scale limits"),
]


@pytest.mark.limit
@pytest.mark.gcp_only
@pytest.mark.parametrize("mode", ["getitem"])
@pytest.mark.parametrize(
    ("scale", "ops_per_actor"),
    [
        pytest.param(10, 500, id="10x500"),
        pytest.param(20, 500, id="20x500", marks=_explore_marks),
        pytest.param(40, 500, id="40x500", marks=_explore_marks),
    ],
)
def test_lance_checkpoint_single_store_many_reads_per_file(
    local_ray: None,
    geneva_test_bucket: str,
    mode: str,
    scale: int,
    ops_per_actor: int,
) -> None:
    """
    Simulates the real workload: each actor builds ONE
    FlatLanceCheckpointStore and performs many sequential checkpoint
    reads. This exercises connection/cred caching and avoids the "one
    store per call" anti-pattern.

    Env knobs:
      mode           # testing different ops in checkpointstore (getitem|contains)
      scale          # number of actors (processes)
      ops_per_actor  # sequential reads per actor
    """
    ckp_root = str(URL(geneva_test_bucket) / "stampede-test" / KEY_PREFIX)

    if not ckp_root.startswith("gs://"):
        pytest.skip(
            "Set GENEVA_LANCE_CKPT_ROOT=gs://<bucket>/<prefix> to run this test."
        )

    _LOG.info(
        "starting single-store-many-reads: mode=%s actors=%d ops/actor=%d",
        mode,
        scale,
        ops_per_actor,
    )

    # Prepare a small keyset once (on driver) so each actor cycles through the
    # same store/files
    from geneva.checkpoint import FlatLanceCheckpointStore

    prep_store = FlatLanceCheckpointStore(ckp_root)
    keys = _ensure_keyset(prep_store, KEYSET_SIZE)
    keys_ref = ray.put(keys)  # broadcast to actors efficiently
    _LOG.info(f"keys {keys}")

    # Spin up actors (each with its own single store)
    readers = [
        StoreReader.options(num_cpus=0.25).remote(ckp_root, mode) for _ in range(scale)
    ]

    # Run sequential reads in each actor
    refs = [r.run.remote(keys_ref, ops_per_actor) for r in readers]  # type: ignore[attr-defined]

    failures = 0
    successes = 0
    # Actors run in parallel, so timeout scales with per-actor ops, not
    # total ops. In CI, local Ray workers may spend noticeable time creating
    # their runtime package/venv before the first object-store read, so keep a
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
            _LOG.warning("actor run failed: %r", e)

    _LOG.info(
        "stampede single-store-many-reads: actors=%d ops/actor=%d"
        " keyset=%d mode=%s successes=%d failures=%d root=%s",
        scale,
        ops_per_actor,
        KEYSET_SIZE,
        mode,
        successes,
        failures,
        ckp_root,
    )
    assert failures == 0, f"Expected all to complete; saw {failures} failures"
