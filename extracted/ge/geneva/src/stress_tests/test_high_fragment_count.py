# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Test 8 (P0): High Fragment Count Scaling.

Find the fragment count where planning, commit, and metadata operations
become unacceptable (>60s per operation).  Measures key read operations
against a Lance dataset with increasing fragment counts.

**Prebaked dataset** — To avoid spending CI minutes creating fragments
on every run, the test uses a stable, shared dataset at a well-known
path (``STRESS_PREBAKED_FRAGMENT_URI``).  The dataset is built locally
on the first run, uploaded to the target store, and reused thereafter.
Each sweep point is tagged (e.g. ``fragments-1000``) so the test can
open it with ``lance.dataset(uri, version="fragments-1000")``.
"""

from __future__ import annotations

import logging
import os
import tempfile
import time
import tracemalloc
from typing import Any

import lance
import pyarrow as pa
import pytest

from stress_tests.stress_results import StressResult, log_result, scale_params

_LOG = logging.getLogger(__name__)

# Default fragment count sweep.  Override with STRESS_MAX_FRAGMENTS.
# CI sets this per suite: regression=10000, explore=150000.
_MAX_FRAGMENTS = int(os.environ.get("STRESS_MAX_FRAGMENTS", "150000"))
DEFAULT_FRAGMENT_SWEEP = [1000, 5000, 10000, 50000, 150000]
ROWS_PER_FRAGMENT = 10

# All sweep points pass quickly (<1s even at 150K), so run them all
# as regression.
_FRAG_EXPLORE_THRESHOLD = 200000

# Stable path for a prebaked fragment dataset shared across CI runs.
# Set in CI to avoid recreating fragments on every run.  When unset, the
# test falls back to creating under tmp_dataset_uri (per-run, ephemeral).
_PREBAKED_FRAGMENT_URI = os.environ.get("STRESS_PREBAKED_FRAGMENT_URI", "")


def fragment_sweep() -> list[int]:
    """Return the fragment count sweep capped by STRESS_MAX_FRAGMENTS."""
    return [n for n in DEFAULT_FRAGMENT_SWEEP if n <= _MAX_FRAGMENTS]


def _fragment_params() -> list[Any]:
    """Build pytest params for fragment sweep with explore markers."""
    return scale_params(
        fragment_sweep(),
        id_prefix="fragments",
        explore_threshold=_FRAG_EXPLORE_THRESHOLD,
    )


def _make_fragment_data(frag_idx: int, rows_per_frag: int) -> pa.Table:
    return pa.table(
        {
            "id": pa.array(range(rows_per_frag)),
            "val": pa.array([f"row_{frag_idx}_{j}" for j in range(rows_per_frag)]),
        }
    )


def _tag_name(fragment_count: int) -> str:
    return f"fragments-{fragment_count}"


def create_dataset_with_fragment_sweep(
    uri: str, sweep: list[int], rows_per_frag: int
) -> None:
    """Create a Lance dataset with commits and tags at each sweep point.

    Uses ``LanceFragment.create()`` to write fragment data files without
    committing, then batch-commits at each sweep point via
    ``LanceOperation.Append``.  This reduces 150K individual commits to
    ``len(sweep)`` commits, yielding a massive speedup.

    Each sweep point is tagged (e.g. ``fragments-1000``) so callers can
    open the dataset with ``lance.dataset(uri, version="fragments-1000")``.
    """
    prev = 0

    for target in sorted(sweep):
        count = target - prev
        if count <= 0:
            continue

        if prev == 0:
            # Bootstrap: create dataset with first fragment
            lance.write_dataset(_make_fragment_data(0, rows_per_frag), uri)
            frags = []
            for i in range(1, count):
                fm = lance.LanceFragment.create(
                    uri, _make_fragment_data(i, rows_per_frag)
                )
                frags.append(fm)
                if (i + 1) % 5000 == 0:
                    _LOG.info(
                        "Prepared %d / %d fragment files",
                        i + 1,
                        target,
                    )
            if frags:
                op = lance.LanceOperation.Append(frags)
                ds = lance.LanceDataset.commit(uri, op, read_version=1)
            else:
                ds = lance.dataset(uri)
        else:
            frags = []
            for i in range(count):
                fm = lance.LanceFragment.create(
                    uri,
                    _make_fragment_data(prev + i, rows_per_frag),
                )
                frags.append(fm)
                if (i + 1) % 5000 == 0:
                    _LOG.info(
                        "Prepared %d / %d fragment files (batch %d→%d)",
                        i + 1,
                        count,
                        prev,
                        target,
                    )
            ds_cur = lance.dataset(uri)
            op = lance.LanceOperation.Append(frags)
            ds = lance.LanceDataset.commit(uri, op, read_version=ds_cur.version)

        tag = _tag_name(target)
        ds.tags.create(tag, ds.version)
        _LOG.info(
            "Committed %d fragments → version %d, tag %s",
            target,
            ds.version,
            tag,
        )
        prev = target


def _measure_get_fragments(ds: lance.LanceDataset) -> dict[str, Any]:
    """Time ``get_fragments()`` and return timing + count."""
    t0 = time.monotonic()
    frags = list(ds.get_fragments())
    elapsed = time.monotonic() - t0
    return {"elapsed_s": elapsed, "fragment_count": len(frags)}


def _measure_plan_read(ds: lance.LanceDataset) -> dict[str, Any]:
    """Time a scan/plan operation that touches fragment metadata."""
    t0 = time.monotonic()
    # count_rows() forces a full scan plan across all fragments.
    row_count = ds.count_rows()
    elapsed = time.monotonic() - t0
    return {"elapsed_s": elapsed, "row_count": row_count}


def _measure_memory(ds: lance.LanceDataset) -> dict[str, Any]:
    """Measure peak memory during fragment enumeration."""
    tracemalloc.start()
    _ = list(ds.get_fragments())
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"peak_memory_bytes": peak, "peak_memory_mib": peak / (1024 * 1024)}


def _run_high_fragment_count(
    fragment_count: int,
    uri: str,
) -> dict[str, Any]:
    """Run all measurements for a given fragment count."""
    tag = _tag_name(fragment_count)
    ds = lance.dataset(uri, version=tag)

    _LOG.info("Measuring get_fragments() at tag %s...", tag)
    frag_result = _measure_get_fragments(ds)
    _LOG.info(
        "get_fragments: %.3fs (%d fragments)",
        frag_result["elapsed_s"],
        frag_result["fragment_count"],
    )

    _LOG.info("Measuring plan/scan (count_rows)...")
    plan_result = _measure_plan_read(ds)
    _LOG.info(
        "count_rows: %.3fs (%d rows)",
        plan_result["elapsed_s"],
        plan_result["row_count"],
    )

    _LOG.info("Measuring memory during fragment enumeration...")
    mem_result = _measure_memory(ds)
    _LOG.info("peak memory: %.1f MiB", mem_result["peak_memory_mib"])

    # The "latency" for the stress result is the worst-case operation time.
    op_times = [
        frag_result["elapsed_s"],
        plan_result["elapsed_s"],
    ]
    worst_op_time = max(op_times)

    result = StressResult(
        scale=fragment_count,
        throughput=0.0,
        p50_latency_s=sorted(op_times)[len(op_times) // 2],
        p90_latency_s=worst_op_time,
        p99_latency_s=worst_op_time,
        max_latency_s=worst_op_time,
        error_count=0,
        error_rate=0.0,
        elapsed_s=sum(op_times),
        metadata={
            "get_fragments_s": frag_result["elapsed_s"],
            "count_rows_s": plan_result["elapsed_s"],
            "peak_memory_mib": mem_result["peak_memory_mib"],
            "row_count": plan_result["row_count"],
        },
    )
    log_result(result)

    return {
        "result": result,
        "get_fragments_s": frag_result["elapsed_s"],
        "count_rows_s": plan_result["elapsed_s"],
        "peak_memory_mib": mem_result["peak_memory_mib"],
    }


def _upload_dataset(local_uri: str, remote_uri: str) -> None:
    """Sync a local Lance dataset directory to a remote store via gcloud rsync."""
    import subprocess

    _LOG.info("Uploading local dataset %s → %s", local_uri, remote_uri)
    t0 = time.monotonic()
    # Stream rsync output and log progress every 5000 files instead of
    # printing 150K+ individual file lines.
    proc = subprocess.Popen(
        ["gcloud", "storage", "rsync", "-r", local_uri, remote_uri],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    lines = 0
    assert proc.stdout is not None
    for _ in proc.stdout:
        lines += 1
        if lines % 5000 == 0:
            _LOG.info("Uploaded %d files...", lines)
    proc.wait()
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, "gcloud")
    _LOG.info(
        "Upload completed: %d files in %.1fs",
        lines,
        time.monotonic() - t0,
    )


@pytest.fixture(scope="module")
def prebaked_fragment_dataset(tmp_dataset_uri: str) -> str:
    """Module-scoped fixture: prebaked fragment dataset on cloud storage.

    Uses a stable, shared path (``STRESS_PREBAKED_FRAGMENT_URI``) so the
    dataset persists across CI runs.  If the dataset doesn't exist or is too
    small, it is built **locally** and then copied to the store in bulk.

    Uses ``LanceFragment.create()`` + batch ``Append`` commits at each
    sweep point instead of N individual appends — this reduces 150K commits
    to ~5 and cuts build time from hours to minutes.

    Each sweep point is tagged (e.g. ``fragments-1000``) so tests open
    it with ``lance.dataset(uri, version="fragments-1000")``.

    Returns the dataset URI.
    """
    sweep = fragment_sweep()
    max_frags = max(sweep) if sweep else 10000

    uri = _PREBAKED_FRAGMENT_URI or (tmp_dataset_uri.rstrip("/") + "/frag_stress")

    # Check if existing dataset already has the required tags.
    try:
        ds = lance.dataset(uri)
        existing_tags = set(ds.tags.list())
        needed_tags = {_tag_name(n) for n in sweep}
        if needed_tags <= existing_tags:
            _LOG.info(
                "Prebaked dataset at %s has all required tags — reusing",
                uri,
            )
            return uri
    except (FileNotFoundError, ValueError):
        pass

    # Build locally (fast) then bulk-copy to the store.
    _LOG.info("Building prebaked dataset locally for %d fragments", max_frags)
    tmpdir = tempfile.mkdtemp(prefix="stress_fragments_")
    local_uri = os.path.join(tmpdir, "test.lance")

    t0 = time.monotonic()
    create_dataset_with_fragment_sweep(local_uri, sweep, ROWS_PER_FRAGMENT)
    _LOG.info(
        "Local build took %.1fs for %d fragments (%d commits)",
        time.monotonic() - t0,
        max_frags,
        len(sweep),
    )

    _upload_dataset(local_uri, uri)
    return uri


@pytest.mark.limit
@pytest.mark.parametrize("fragment_count", _fragment_params())
def test_high_fragment_count(
    fragment_count: int, prebaked_fragment_dataset: str
) -> None:
    """Fragment count scaling on cloud storage.

    Uses a prebaked Lance dataset for realistic manifest I/O timing.
    The dataset is created once and shared across CI runs.
    """
    info = _run_high_fragment_count(fragment_count, prebaked_fragment_dataset)

    # Report which operations exceed thresholds.
    threshold_s = 60.0
    for op_name in ("get_fragments_s", "count_rows_s"):
        op_time = info[op_name]
        if op_time > threshold_s:
            _LOG.warning(
                "THRESHOLD EXCEEDED: %s took %.1fs (>%.0fs) at %d fragments",
                op_name,
                op_time,
                threshold_s,
                fragment_count,
            )

    _LOG.info(
        "fragment_count=%d get_fragments=%.1fs count_rows=%.1fs peak_memory=%.1fMiB",
        fragment_count,
        info["get_fragments_s"],
        info["count_rows_s"],
        info["peak_memory_mib"],
    )
