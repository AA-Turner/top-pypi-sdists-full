# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Stress guardrail for applier-side allocator trimming.

``SimpleApplier`` has a best-effort cleanup hook that runs Python GC, asks
PyArrow to release unused memory, and calls Linux ``malloc_trim(0)`` every N
completed batches. This test validates that the quick fix is load-bearing for
the target allocator-retention failure mode.

The workload deliberately runs with ``concurrency=1`` and
``intra_applier_concurrency=1`` so the Ray actor uses ``SimpleApplier``.
Each batch samples the worker RSS at batch start, performs a transient
heap allocation, releases it, and returns the sampled RSS. A disabled
control run uses ``GENEVA_APPLIER_MEMORY_TRIM_INTERVAL=0``; the enabled
run leaves the env var unset and relies on the production default.

This is Linux/glibc-specific because it depends on ``/proc/self/statm`` and
``malloc_trim(0)`` behavior. Other platforms skip the test.
"""

from __future__ import annotations

import ctypes
import logging
import os
import shutil
import sys
import tempfile
import time
import uuid
from typing import TYPE_CHECKING, Any, cast

import lance
import pyarrow as pa
import pytest
import ray

import geneva
from geneva import udf
from geneva.apply.memory import APPLIER_MEMORY_TRIM_INTERVAL_ENV
from stress_tests.stress_results import log_result, make_result

if TYPE_CHECKING:
    from pathlib import Path

    from geneva.transformer import UDF

_LOG = logging.getLogger(__name__)

_NUM_BATCHES = 33
_HEAP_BYTES_PER_BATCH = 96 * 1024 * 1024
_HEAP_CHUNK_BYTES = 64 * 1024
_DISABLED_MIN_GROWTH_BYTES = 48 * 1024 * 1024
_MIN_REDUCTION_BYTES = 32 * 1024 * 1024
_MAX_ENABLED_GROWTH_RATIO = 0.70
_DEFAULT_TRIM_INTERVAL = 8

pytestmark = pytest.mark.skipif(
    not sys.platform.startswith("linux"),
    reason="GENEVA applier memory trim stress test requires Linux",
)


def _make_rss_probe_udf() -> UDF:
    """Build a by-value UDF so Ray workers need no stress-test module import."""
    heap_chunk_bytes = _HEAP_CHUNK_BYTES
    libc_configured = False

    def page_size() -> int:
        return int(os.sysconf("SC_PAGE_SIZE"))

    def rss_bytes_from_proc() -> int:
        # /proc/self/statm reports process memory counters in pages; the second
        # field is resident set size, so multiplying by page size gives RSS bytes.
        with open("/proc/self/statm", encoding="utf-8") as f:  # noqa: S108
            fields = f.read().split()
        return int(fields[1]) * page_size()

    def configure_libc_for_retention_harness() -> None:
        """Make the disabled-control run retain freed heap pages."""
        nonlocal libc_configured
        if libc_configured:
            return

        libc = ctypes.CDLL("libc.so.6")
        mallopt = libc.mallopt
        mallopt.argtypes = [ctypes.c_int, ctypes.c_int]
        mallopt.restype = ctypes.c_int
        # glibc may automatically trim the top heap on free. Raising
        # M_TRIM_THRESHOLD makes the control run deterministic while still
        # allowing Geneva's explicit malloc_trim(0) call to release pages.
        mallopt(-1, 1024 * 1024 * 1024)  # M_TRIM_THRESHOLD
        libc_configured = True

    def touch_heap_bytes(total_bytes: int) -> None:
        local_page_size = page_size()
        chunks: list[bytearray] = []
        remaining = total_bytes
        while remaining > 0:
            chunk_size = min(heap_chunk_bytes, remaining)
            chunk = bytearray(chunk_size)
            for offset in range(0, chunk_size, local_page_size):
                chunk[offset] = 1
            chunk[-1] = 1
            chunks.append(chunk)
            remaining -= chunk_size
        del chunks

    @udf(data_type=pa.uint64(), checkpoint_size=1)
    def rss_probe(row_id: pa.Array, payload_bytes: pa.Array) -> pa.Array:  # noqa: ARG001
        configure_libc_for_retention_harness()
        rss_before = rss_bytes_from_proc()
        requested_bytes = int(payload_bytes[0].as_py())
        touch_heap_bytes(requested_bytes)
        return pa.array([rss_before] * len(payload_bytes), type=pa.uint64())

    return cast("UDF", rss_probe)


def _build_input_table(uri: str) -> None:
    tbl = pa.Table.from_pydict(
        {
            "row_id": list(range(_NUM_BATCHES)),
            "payload_bytes": [_HEAP_BYTES_PER_BATCH] * _NUM_BATCHES,
        }
    )
    lance.write_dataset(tbl, uri, max_rows_per_file=_NUM_BATCHES)


def _run_backfill_case(
    work_dir: str,
    trim_interval: str | None,
) -> dict[str, Any]:
    if trim_interval is None:
        os.environ.pop(APPLIER_MEMORY_TRIM_INTERVAL_ENV, None)
    else:
        os.environ[APPLIER_MEMORY_TRIM_INTERVAL_ENV] = trim_interval

    os.makedirs(work_dir, exist_ok=True)
    ray_temp_dir = tempfile.mkdtemp(prefix="gva-ray-")
    ray.init(
        num_cpus=2,
        include_dashboard=False,
        ignore_reinit_error=True,
        _temp_dir=ray_temp_dir,
    )
    try:
        input_uri = os.path.join(work_dir, "input")
        _build_input_table(input_uri)
        db = geneva.connect(work_dir)
        src = lance.dataset(input_uri).to_table()
        table_name = f"rss-{uuid.uuid4().hex[:8]}"
        tbl = db.create_table(table_name, src)
        tbl.add_columns({"rss_before": _make_rss_probe_udf()})

        t0 = time.monotonic()
        result = tbl.backfill(
            "rss_before",
            concurrency=1,
            intra_applier_concurrency=1,
            max_checkpoint_size=1,
            commit_granularity=1,
            _admission_check=False,
        )
        elapsed_s = time.monotonic() - t0
        if result.status != "DONE":
            raise AssertionError(f"unexpected backfill status: {result.status}")

        arrow_tbl = tbl.to_arrow().sort_by("row_id")
        samples: list[int] = []
        for value in arrow_tbl["rss_before"].to_pylist():
            if value is None:
                raise AssertionError("RSS probe returned a null sample")
            samples.append(int(value))
        if len(samples) != _NUM_BATCHES:
            raise AssertionError(
                f"expected {_NUM_BATCHES} RSS samples, got {len(samples)}"
            )
        return {
            "samples": samples,
            "initial_rss_bytes": samples[0],
            "final_rss_bytes": samples[-1],
            "max_rss_bytes": max(samples),
            "growth_bytes": samples[-1] - samples[0],
            "elapsed_s": elapsed_s,
            "trim_interval": trim_interval,
        }
    finally:
        ray.shutdown()
        shutil.rmtree(ray_temp_dir, ignore_errors=True)
        time.sleep(2)


def _require_linux_malloc_trim() -> None:
    if not sys.platform.startswith("linux"):
        pytest.skip("GENEVA applier memory trim stress test requires Linux")
    if not os.path.exists("/proc/self/statm"):
        pytest.skip("GENEVA applier memory trim stress test requires /proc/self/statm")
    try:
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim.argtypes = [ctypes.c_int]
        libc.mallopt.argtypes = [ctypes.c_int, ctypes.c_int]
    except Exception as exc:
        pytest.skip(f"GENEVA applier memory trim stress test requires glibc: {exc}")


@pytest.mark.stress_explore
@pytest.mark.timeout(600)
def test_simple_applier_memory_trim_bounds_worker_rss(tmp_path: Path) -> None:
    """Default memory trimming should reduce retained worker RSS.

    The 33rd batch samples RSS immediately after the fourth default trim point
    (8, 16, 24, 32 completed batches). With trimming disabled, the same final
    sample should still reflect retained heap pages from the prior batches.
    """
    _require_linux_malloc_trim()

    disabled = _run_backfill_case(str(tmp_path / "trim-0"), trim_interval="0")
    enabled = _run_backfill_case(str(tmp_path / "enabled"), trim_interval=None)

    disabled_growth = int(disabled["growth_bytes"])
    enabled_growth = int(enabled["growth_bytes"])
    reduction = disabled_growth - enabled_growth
    result = make_result(
        scale=_NUM_BATCHES,
        latencies=[float(disabled["elapsed_s"]), float(enabled["elapsed_s"])],
        error_count=0,
        elapsed_s=float(disabled["elapsed_s"]) + float(enabled["elapsed_s"]),
        metadata={
            "heap_bytes_per_batch": _HEAP_BYTES_PER_BATCH,
            "trim_interval": _DEFAULT_TRIM_INTERVAL,
            "disabled_initial_mib": disabled["initial_rss_bytes"] >> 20,
            "disabled_final_mib": disabled["final_rss_bytes"] >> 20,
            "enabled_initial_mib": enabled["initial_rss_bytes"] >> 20,
            "enabled_final_mib": enabled["final_rss_bytes"] >> 20,
            "disabled_growth_mib": disabled_growth >> 20,
            "enabled_growth_mib": enabled_growth >> 20,
            "reduction_mib": reduction >> 20,
        },
    )
    log_result(result)
    _LOG.info(
        "applier memory trim samples: disabled=%s enabled=%s",
        [value >> 20 for value in disabled["samples"]],
        [value >> 20 for value in enabled["samples"]],
    )

    assert disabled_growth >= _DISABLED_MIN_GROWTH_BYTES, (
        "disabled control did not retain enough RSS to validate the guardrail: "
        f"growth={disabled_growth >> 20}MiB "
        f"threshold={_DISABLED_MIN_GROWTH_BYTES >> 20}MiB"
    )
    assert reduction >= _MIN_REDUCTION_BYTES, (
        "default trim did not materially reduce retained RSS: "
        f"disabled_growth={disabled_growth >> 20}MiB "
        f"enabled_growth={enabled_growth >> 20}MiB "
        f"reduction={reduction >> 20}MiB"
    )
    assert enabled_growth <= int(disabled_growth * _MAX_ENABLED_GROWTH_RATIO), (
        "default trim left too much retained RSS relative to disabled control: "
        f"disabled_growth={disabled_growth >> 20}MiB "
        f"enabled_growth={enabled_growth >> 20}MiB "
        f"max_ratio={_MAX_ENABLED_GROWTH_RATIO}"
    )
