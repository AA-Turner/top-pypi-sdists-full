# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Compare the flat and hierarchical checkpoint store layouts on real
cloud storage.

This test runs as part of the standard integration matrix on the cloud
selected by ``--csp`` (default ``gcp``; the AWS CI job runs it against
S3). It populates the same set of synthetic checkpoint keys twice — once
through ``FlatLanceCheckpointStore`` and once through
``HierarchicalLanceCheckpointStore`` — and times listing, scoped
listing, and point membership on both. The results are logged and
attached as a JSON artifact so reviewers can compare layouts inline on
the PR.

The default scale (``2_000`` checkpoints across ``5`` backfill
identities) keeps CI wall time bounded while still exercising the flat
store's full-LIST-then-filter cost on scoped queries against the
hierarchical store's narrowed ``bf=`` scan. Bump ``GENEVA_S3_PERF_N`` for
deeper local runs.
"""

from __future__ import annotations

import json
import logging
import os
import random
import tempfile
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

import pyarrow as pa
import pytest

from geneva.checkpoint import (
    FlatLanceCheckpointStore,
    HierarchicalLanceCheckpointStore,
)
from geneva.checkpoint_utils import hash_string

_LOG = logging.getLogger(__name__)


# ----------------------------------------------------------------- knobs


def _env_int(name: str, default: int) -> int:
    return int(os.environ.get(name, str(default)))


# CI-friendly defaults. Override locally for deeper sweeps:
#   GENEVA_S3_PERF_N           total checkpoints across all identities
#   GENEVA_S3_PERF_IDENTITIES  number of distinct backfill identities
#   GENEVA_S3_PERF_WORKERS     populate-time thread pool size
#   GENEVA_S3_PERF_SAMPLE      point-lookup latency samples
_N = _env_int("GENEVA_S3_PERF_N", 2_000)
_NUM_IDENTITIES = _env_int("GENEVA_S3_PERF_IDENTITIES", 5)
_WORKERS = _env_int("GENEVA_S3_PERF_WORKERS", 16)
_SAMPLE = _env_int("GENEVA_S3_PERF_SAMPLE", 200)

# Where to drop the JSON summary artifact. Defaults to system tempdir so the
# CI workflow can pick it up via ``actions/upload-artifact`` if desired.
_RESULTS_DIR = os.environ.get("GENEVA_S3_PERF_RESULTS_DIR", tempfile.gettempdir())


# ----------------------------------------------------------------- keys


def _identity_prefix(seed: int) -> str:
    """A flat-key checkpoint prefix for a single synthetic backfill.

    ``where``/``uri``/``srcfiles`` are deterministic md5 hex segments so
    the hierarchical path resolver can recover the table-hash and
    identity-hash components.
    """
    return (
        f"udf-perfu{seed}_ver-1_col-c"
        f"_where-{hash_string(f'where-{seed}')}"
        f"_uri-{hash_string(f'uri-{seed}')}"
        f"_srcfiles-{hash_string(f'srcfiles-{seed}')}"
    )


def _full_key(identity: str, frag_id: int, range_start: int | None = None) -> str:
    if range_start is None:
        return f"{identity}_frag-{frag_id}"
    return f"{identity}_frag-{frag_id}_range-{range_start}-{range_start + 100}"


def _build_keys(num_identities: int, total: int) -> list[tuple[str, str]]:
    """Return ``(identity_prefix, full_key)`` pairs, mixing fragment and
    range checkpoints to match a real backfill's shape.
    """
    out: list[tuple[str, str]] = []
    per_identity = total // num_identities
    for i in range(num_identities):
        identity = _identity_prefix(i)
        half = per_identity // 2
        out.extend((identity, _full_key(identity, f)) for f in range(half))
        out.extend(
            (identity, _full_key(identity, r // 10, (r % 10) * 100))
            for r in range(per_identity - half)
        )
    return out


# --------------------------------------------------------------- measurements


@dataclass
class _OpResult:
    label: str
    op: str
    elapsed_s: float
    items: int

    def as_dict(self) -> dict:
        return {
            "label": self.label,
            "op": self.op,
            "elapsed_s": self.elapsed_s,
            "items": self.items,
        }


def _populate(
    store: FlatLanceCheckpointStore,
    keys: list[tuple[str, str]],
    label: str,
) -> _OpResult:
    """Write *keys* into *store* using a thread pool. Returns timing."""
    batch = pa.RecordBatch.from_pydict({"x": [0]})

    def _write(item: tuple[str, str]) -> None:
        _, key = item
        store[key] = batch

    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=_WORKERS) as pool:
        futures = [pool.submit(_write, k) for k in keys]
        log_every = max(1, len(keys) // 10)
        for done, fut in enumerate(as_completed(futures), start=1):
            fut.result()
            if done % log_every == 0:
                _LOG.info("[%s] populated %d/%d", label, done, len(keys))
    elapsed = time.perf_counter() - t0
    _LOG.info("[%s] populate finished: %.2fs (%d keys)", label, elapsed, len(keys))
    return _OpResult(label=label, op="populate", elapsed_s=elapsed, items=len(keys))


def _time_cold_list(store: FlatLanceCheckpointStore, label: str) -> _OpResult:
    t0 = time.perf_counter()
    listed = sum(1 for _ in store.list_keys())
    elapsed = time.perf_counter() - t0
    _LOG.info("[%s] cold list_keys: %.2fs, %d keys returned", label, elapsed, listed)
    return _OpResult(label=label, op="list_full", elapsed_s=elapsed, items=listed)


def _time_scoped_list(
    store: FlatLanceCheckpointStore, prefix: str, label: str
) -> _OpResult:
    t0 = time.perf_counter()
    listed = sum(1 for _ in store.list_keys(prefix=prefix))
    elapsed = time.perf_counter() - t0
    _LOG.info(
        "[%s] scoped list_keys (1 identity): %.2fs, %d keys returned",
        label,
        elapsed,
        listed,
    )
    return _OpResult(label=label, op="list_scoped", elapsed_s=elapsed, items=listed)


def _time_contains(
    store: FlatLanceCheckpointStore,
    keys: list[tuple[str, str]],
    label: str,
) -> _OpResult:
    rng = random.Random(0xC0FFEE)
    samples = [rng.choice(keys)[1] for _ in range(min(_SAMPLE, len(keys)))]
    t0 = time.perf_counter()
    for key in samples:
        assert key in store, f"expected {key!r} to be present in {label} store"
    elapsed = time.perf_counter() - t0
    _LOG.info(
        "[%s] __contains__ over %d samples: %.2fs total (%.4fs/op)",
        label,
        len(samples),
        elapsed,
        elapsed / max(1, len(samples)),
    )
    return _OpResult(label=label, op="contains", elapsed_s=elapsed, items=len(samples))


# Intentionally no ``_time_delete_prefix`` helper: delete is a maintenance
# path (not the backfill hot path) and its semantics are covered by unit tests
# in ``src/tests/test_checkpoint.py``.


# ------------------------------------------------------------------- test


@pytest.mark.timeout(1200)
def test_checkpoint_store_layout_perf(
    geneva_test_bucket: str,
    slug: str | None,
    csp: str,
) -> None:
    """Time the same workload through ``FlatLanceCheckpointStore`` and
    ``HierarchicalLanceCheckpointStore`` against the integration bucket.
    Runs on whichever CSP the integ suite is pointed at.

    The test passes as long as both layouts complete the workload
    without errors and the hierarchical store's full-list time is not
    catastrophically worse than the flat store's (we expect the
    hierarchical store to be at worst comparable on small workloads and
    meaningfully better at scale). Per-op timings are logged at INFO and
    saved as a JSON artifact under
    ``$TMPDIR/checkpoint_store_layout_perf-<slug>.json``.
    """
    if csp == "azure":
        pytest.skip(
            "Disabled on azure: workload runs past the SAS token lifetime and "
            "writes start failing 401. Re-enable once credential refresh "
            "covers long-running checkpoint perf workloads (GEN-545)."
        )

    run_id = uuid.uuid4().hex[:8]
    isolation = f"{slug}-{run_id}" if slug else run_id

    flat_root = f"{geneva_test_bucket}/ckp-perf/flat-{isolation}"
    hierarchical_root = f"{geneva_test_bucket}/ckp-perf/hierarchical-{isolation}"
    keys = _build_keys(_NUM_IDENTITIES, _N)
    sample_identity = _identity_prefix(0)

    _LOG.info(
        "checkpoint perf: bucket=%s N=%d identities=%d workers=%d sample=%d",
        geneva_test_bucket,
        len(keys),
        _NUM_IDENTITIES,
        _WORKERS,
        _SAMPLE,
    )

    results: list[_OpResult] = []

    # -- flat -------------------------------------------------------------
    flat = FlatLanceCheckpointStore(flat_root)
    results.append(_populate(flat, keys, "flat"))
    results.append(_time_cold_list(flat, "flat"))
    results.append(_time_scoped_list(flat, sample_identity, "flat"))
    results.append(_time_contains(flat, keys, "flat"))

    # -- hierarchical -----------------------------------------------------
    hierarchical = HierarchicalLanceCheckpointStore(hierarchical_root)
    results.append(_populate(hierarchical, keys, "hierarchical"))
    results.append(_time_cold_list(hierarchical, "hierarchical"))
    results.append(_time_scoped_list(hierarchical, sample_identity, "hierarchical"))
    results.append(_time_contains(hierarchical, keys, "hierarchical"))

    # -- correctness sanity ---------------------------------------------
    flat_full = next(r for r in results if r.label == "flat" and r.op == "list_full")
    hierarchical_full = next(
        r for r in results if r.label == "hierarchical" and r.op == "list_full"
    )
    assert flat_full.items == len(keys), (
        f"flat list_keys returned {flat_full.items}, expected {len(keys)}"
    )
    assert hierarchical_full.items == len(keys), (
        f"hierarchical list_keys returned {hierarchical_full.items}, "
        f"expected {len(keys)}"
    )
    expected_scoped = len(keys) // _NUM_IDENTITIES
    flat_scoped = next(
        r for r in results if r.label == "flat" and r.op == "list_scoped"
    )
    hierarchical_scoped = next(
        r for r in results if r.label == "hierarchical" and r.op == "list_scoped"
    )
    assert flat_scoped.items == expected_scoped
    assert hierarchical_scoped.items == expected_scoped

    # -- summary table --------------------------------------------------
    _LOG.info("\n--- Checkpoint store layout comparison (N=%d) ---", len(keys))
    _LOG.info("%-13s  %-12s  %12s  %10s", "layout", "op", "elapsed_s", "items")
    for r in results:
        _LOG.info("%-13s  %-12s  %12.3f  %10d", r.label, r.op, r.elapsed_s, r.items)

    summary_path = os.path.join(
        _RESULTS_DIR, f"checkpoint_store_layout_perf-{isolation}.json"
    )
    with open(summary_path, "w") as f:
        json.dump(
            {
                "bucket": geneva_test_bucket,
                "n": len(keys),
                "num_identities": _NUM_IDENTITIES,
                "workers": _WORKERS,
                "results": [r.as_dict() for r in results],
            },
            f,
            indent=2,
        )
    _LOG.info("wrote summary: %s", summary_path)

    # -- soft regression guard -----------------------------------------
    # The hierarchical store should not be more than 3× slower than the
    # flat store on any operation. At N=10k we expect hierarchical to win
    # on scoped list operations and break roughly even on populate / cold
    # full LIST / point contains. The guard catches accidental regressions
    # — e.g. hierarchical doing an extra round-trip or falling back to a
    # full scan.
    for op in ("list_full", "list_scoped", "contains"):
        flat_r = next(r for r in results if r.label == "flat" and r.op == op)
        hierarchical_r = next(
            r for r in results if r.label == "hierarchical" and r.op == op
        )
        # Only enforce when both took a measurable amount of time;
        # otherwise tiny absolute differences dominate the ratio.
        if flat_r.elapsed_s < 0.1:
            continue
        assert hierarchical_r.elapsed_s <= flat_r.elapsed_s * 3, (
            f"hierarchical {op} took {hierarchical_r.elapsed_s:.2f}s "
            f"vs flat {flat_r.elapsed_s:.2f}s (>3× regression)"
        )
