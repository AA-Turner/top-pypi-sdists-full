# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Stress tests for framework-side UDTF memory usage.

These tests validate the memory-sensitive helper paths added for GEN-366:

- streaming UDTF batch consumption should keep peak memory bounded as the
  total number of output batches grows;
- chunked row-id fanout should keep extra peak memory bounded as the total
  number of row IDs grows.

Both tests run the measured code in a fresh subprocess so RSS readings are
not polluted by the parent pytest process.
"""

from __future__ import annotations

import multiprocessing as mp
import queue as queue_module
import resource
import sys
import tempfile
import time
from typing import Any

import pyarrow as pa
import pytest

from geneva import connect
from stress_tests.stress_results import log_result, make_result


def _max_rss_bytes() -> int:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return int(value)
    return int(value) * 1024


def _run_measurement_subprocess(
    target,  # noqa: ANN001
    *args: Any,
    timeout_s: float = 120.0,
) -> dict[str, Any]:
    ctx = mp.get_context("spawn")
    result_queue: Any = ctx.Queue()
    proc = ctx.Process(target=target, args=(result_queue, *args))
    proc.start()
    try:
        result = result_queue.get(timeout=timeout_s)
    except queue_module.Empty:
        if proc.is_alive():
            proc.terminate()
        proc.join(timeout=10)
        pytest.fail(f"subprocess did not complete within {timeout_s}s")
    finally:
        proc.join(timeout=5)
        if proc.is_alive():
            proc.terminate()
            proc.join(timeout=5)
    assert proc.exitcode == 0, f"child exited with code {proc.exitcode}"
    return result


def _streaming_rss_worker(
    queue: Any,
    num_batches: int,
    rows_per_batch: int,
    payload_size: int,
) -> None:
    from geneva.table import _make_udtf_batch_reader

    schema = pa.schema([pa.field("payload", pa.large_binary())])

    def _gen() -> Any:
        for idx in range(num_batches):
            payload = bytes([idx % 251]) * payload_size
            yield pa.RecordBatch.from_arrays(
                [
                    pa.array(
                        [payload] * rows_per_batch,
                        type=pa.large_binary(),
                    )
                ],
                schema=schema,
            )

    start = _max_rss_bytes()
    peak = start
    t0 = time.monotonic()
    reader, get_stats = _make_udtf_batch_reader(_gen(), schema)
    if reader is not None:
        for _batch in reader:
            peak = max(peak, _max_rss_bytes())
    rows, batches = get_stats()
    elapsed_s = time.monotonic() - t0
    queue.put(
        {
            "start_rss_bytes": start,
            "peak_rss_bytes": peak,
            "rows": rows,
            "batches": batches,
            "elapsed_s": elapsed_s,
        }
    )


def _chunked_row_id_rss_worker(
    queue: Any,
    total_row_ids: int,
    chunk_size: int,
) -> None:
    from geneva.table import _iter_row_id_chunks

    row_ids = pa.array(range(total_row_ids), type=pa.uint64())
    baseline = _max_rss_bytes()
    peak = baseline
    processed = 0
    max_chunk_len = 0
    t0 = time.monotonic()
    for row_id_chunk in _iter_row_id_chunks(row_ids, chunk_size):
        processed += len(row_id_chunk)
        max_chunk_len = max(max_chunk_len, len(row_id_chunk))
        peak = max(peak, _max_rss_bytes())
    elapsed_s = time.monotonic() - t0
    queue.put(
        {
            "baseline_rss_bytes": baseline,
            "peak_rss_bytes": peak,
            "delta_rss_bytes": peak - baseline,
            "processed": processed,
            "max_chunk_len": max_chunk_len,
            "elapsed_s": elapsed_s,
        }
    )


def _partition_distinct_rss_worker(queue: Any, db_uri: str, table_name: str) -> None:
    from geneva import connect
    from geneva.table import _sorted_distinct_partition_values

    db = connect(db_uri)
    tbl = db.open_table(table_name)
    baseline = _max_rss_bytes()
    t0 = time.monotonic()
    distinct_values = _sorted_distinct_partition_values(tbl, "group_id")
    elapsed_s = time.monotonic() - t0
    peak = _max_rss_bytes()
    queue.put(
        {
            "baseline_rss_bytes": baseline,
            "peak_rss_bytes": peak,
            "delta_rss_bytes": peak - baseline,
            "distinct_count": len(distinct_values),
            "elapsed_s": elapsed_s,
        }
    )


def _make_partition_distinct_table(
    tmp_dir: str,
    table_name: str,
    total_rows: int,
) -> None:
    db = connect(tmp_dir)
    group_ids = pa.array((idx % 3 for idx in range(total_rows)), type=pa.int64())
    payload = pa.array(range(total_rows), type=pa.int64())
    db.create_table(table_name, pa.table({"group_id": group_ids, "payload": payload}))


@pytest.mark.limit
@pytest.mark.slow
def test_udtf_streaming_batch_reader_peak_memory_is_bounded() -> None:
    """Peak RSS should not scale with the total number of emitted batches."""
    rows_per_batch = 512
    payload_size = 4096
    low = _run_measurement_subprocess(
        _streaming_rss_worker,
        16,
        rows_per_batch,
        payload_size,
    )
    high = _run_measurement_subprocess(
        _streaming_rss_worker,
        128,
        rows_per_batch,
        payload_size,
    )

    low_peak_mib = low["peak_rss_bytes"] / (1024 * 1024)
    high_peak_mib = high["peak_rss_bytes"] / (1024 * 1024)

    result = make_result(
        scale=high["batches"],
        latencies=[low["elapsed_s"], high["elapsed_s"]],
        error_count=0,
        elapsed_s=low["elapsed_s"] + high["elapsed_s"],
        metadata={
            "low_batches": low["batches"],
            "high_batches": high["batches"],
            "low_peak_mib": low_peak_mib,
            "high_peak_mib": high_peak_mib,
        },
    )
    log_result(result)

    assert low["rows"] == 16 * rows_per_batch
    assert high["rows"] == 128 * rows_per_batch
    assert high["batches"] == 128
    assert high_peak_mib <= low_peak_mib + 64, (
        f"Peak RSS grew too much with total output size: "
        f"low={low_peak_mib:.1f} MiB high={high_peak_mib:.1f} MiB"
    )


@pytest.mark.limit
@pytest.mark.slow
def test_udtf_chunked_row_id_fanout_peak_memory_is_bounded() -> None:
    """Extra peak RSS should stay bounded as total row-id volume grows."""
    chunk_size = 50_000
    low = _run_measurement_subprocess(
        _chunked_row_id_rss_worker,
        100_000,
        chunk_size,
    )
    high = _run_measurement_subprocess(
        _chunked_row_id_rss_worker,
        2_000_000,
        chunk_size,
    )

    low_delta_mib = low["delta_rss_bytes"] / (1024 * 1024)
    high_delta_mib = high["delta_rss_bytes"] / (1024 * 1024)

    result = make_result(
        scale=high["processed"],
        latencies=[low["elapsed_s"], high["elapsed_s"]],
        error_count=0,
        elapsed_s=low["elapsed_s"] + high["elapsed_s"],
        metadata={
            "chunk_size": chunk_size,
            "low_delta_mib": low_delta_mib,
            "high_delta_mib": high_delta_mib,
        },
    )
    log_result(result)

    assert low["processed"] == 100_000
    assert high["processed"] == 2_000_000
    assert high["max_chunk_len"] == chunk_size
    assert high_delta_mib <= low_delta_mib + 32, (
        f"Chunked row-id overhead grew too much: "
        f"low={low_delta_mib:.1f} MiB high={high_delta_mib:.1f} MiB"
    )


@pytest.mark.limit
@pytest.mark.slow
def test_udtf_partition_distinct_peak_memory_is_bounded() -> None:
    """`partition_by` distinct discovery should scale with cardinality, not rows."""
    with (
        tempfile.TemporaryDirectory() as low_dir,
        tempfile.TemporaryDirectory() as high_dir,
    ):
        _make_partition_distinct_table(low_dir, "low", 100_000)
        _make_partition_distinct_table(high_dir, "high", 2_000_000)

        low = _run_measurement_subprocess(
            _partition_distinct_rss_worker,
            low_dir,
            "low",
        )
        high = _run_measurement_subprocess(
            _partition_distinct_rss_worker,
            high_dir,
            "high",
        )

    low_delta_mib = low["delta_rss_bytes"] / (1024 * 1024)
    high_delta_mib = high["delta_rss_bytes"] / (1024 * 1024)

    result = make_result(
        scale=2_000_000,
        latencies=[low["elapsed_s"], high["elapsed_s"]],
        error_count=0,
        elapsed_s=low["elapsed_s"] + high["elapsed_s"],
        metadata={
            "low_distinct_count": low["distinct_count"],
            "high_distinct_count": high["distinct_count"],
            "low_delta_mib": low_delta_mib,
            "high_delta_mib": high_delta_mib,
        },
    )
    log_result(result)

    assert low["distinct_count"] == 3
    assert high["distinct_count"] == 3
    assert high_delta_mib <= low_delta_mib + 48, (
        f"partition distinct overhead grew too much: "
        f"low={low_delta_mib:.1f} MiB high={high_delta_mib:.1f} MiB"
    )
