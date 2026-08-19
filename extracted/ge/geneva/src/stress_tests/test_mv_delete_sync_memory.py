# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Driver-memory and commit-count profile of the v2 MV delete-sync path.

When an MV refresh syncs source deletions, the driver materializes the full
set of valid source row ids (``_get_valid_source_row_ids_at_version``) plus
the MV's current ``__source_row_id`` set, then issues one DELETE commit per
``MAX_DELETE_BATCH_SIZE`` stale rows (``_delete_rows_not_in_source_version``).
Driver memory therefore scales with source row count and each refresh that
syncs D deletions produces ceil(D / MAX_DELETE_BATCH_SIZE) commits on the MV.

The scale points call the two pipeline functions directly on the driver (no
Ray) under ``tracemalloc``; correctness of the valid-id set, delete count, and
per-batch commit count is asserted hard, while memory growth across scales is
soft (warn when bytes/row exceeds 2x linear of the smallest point). A small
end-to-end test drives the same path through a real ``refresh()`` so the
direct-call measurement cannot drift from what refresh actually executes.
"""

from __future__ import annotations

import logging
import math
import resource
import sys
import time
import tracemalloc
from typing import TYPE_CHECKING, cast

import pyarrow as pa
import pytest

import geneva
from geneva.query import MATVIEW_META_QUERY, GenevaQuery
from geneva.runners.ray.pipeline import (
    MAX_DELETE_BATCH_SIZE,
    _delete_rows_not_in_source_version,
    _get_valid_source_row_ids_at_version,
)
from stress_tests.stress_results import log_result, make_result, scale_params

if TYPE_CHECKING:
    from pathlib import Path

    from geneva.db import Connection
    from geneva.table import Table

_LOG = logging.getLogger(__name__)

pytestmark = pytest.mark.limit

_SRID_OPTS = {"new_table_enable_stable_row_ids": "true"}
_ADD_CHUNK_ROWS = 500_000

# Row-count sweep; the 20M point is exploratory.
_SCALES = [1_000_000, 5_000_000, 20_000_000]
_EXPLORE_THRESHOLD = 20_000_000

# Soft cross-scale bound: bytes/row may not exceed 2x the smallest point.
_MAX_BYTES_PER_ROW_RATIO = 2.0

# bytes/row per completed scale point, for the cross-scale soft check.
# Scale points run sequentially in ascending order within one module run.
_BYTES_PER_ROW: dict[int, float] = {}


def _ru_maxrss_bytes() -> int:
    """Return the process peak RSS in bytes (ru_maxrss is KiB on Linux)."""
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return peak if sys.platform == "darwin" else peak * 1024


def _build_int_source(db: Connection, name: str, num_rows: int) -> Table:
    """Create an SRID source with ids 0..num_rows-1 via chunked appends."""
    first = min(_ADD_CHUNK_ROWS, num_rows)
    tbl = db.create_table(
        name,
        pa.table({"id": pa.array(range(first), type=pa.int64())}),
        storage_options=_SRID_OPTS,
    )
    start = first
    while start < num_rows:
        n = min(_ADD_CHUNK_ROWS, num_rows - start)
        tbl.add(pa.table({"id": pa.array(range(start, start + n), type=pa.int64())}))
        start += n
    return tbl


def _identity_mv(db: Connection, src: Table, name: str) -> Table:
    # geneva's query builders lose the GenevaQueryBuilder type through
    # search()/select(); create_materialized_view exists at runtime.
    query = src.search(None).select(["id"])
    return query.create_materialized_view(db, name)  # pyright: ignore[reportAttributeAccessIssue]


def _sorted_ids(tbl: Table) -> list[int]:
    tbl.checkout_latest()
    return sorted(cast("list[int]", tbl.to_arrow()["id"].to_pylist()))


def _mv_query(mv: Table) -> GenevaQuery:
    """Parse the MV's source query from its ``geneva::view::query`` metadata."""
    metadata = mv.schema.metadata or {}
    return GenevaQuery.model_validate_json(
        metadata[MATVIEW_META_QUERY.encode()].decode()
    )


@pytest.mark.parametrize(
    "num_rows",
    scale_params(_SCALES, id_prefix="rows", explore_threshold=_EXPLORE_THRESHOLD),
)
def test_mv_delete_sync_driver_memory(tmp_path: Path, num_rows: int) -> None:
    """Delete sync of 25% of the source, called directly on the driver.

    Hard assertions cover the valid-id set size, the deleted-row count, the MV
    row count afterwards, and one DELETE commit per MAX_DELETE_BATCH_SIZE
    stale rows (counted via the MV dataset version delta). Peak driver memory
    is recorded and only soft-checked across scales.
    """
    db = geneva.connect(str(tmp_path))
    src = _build_int_source(db, f"src_{num_rows}", num_rows)
    # MV creation writes only __source_row_id/__is_set placeholders, so the
    # MV tracks all N source rows without computing any projection data.
    mv = _identity_mv(db, src, f"mv_{num_rows}")

    src.delete("id % 4 = 0")
    num_deleted_source = (num_rows + 3) // 4
    expected_valid = num_rows - num_deleted_source

    query = _mv_query(mv)
    src_ref = src.get_reference()
    src_version = src.version

    rss_before = _ru_maxrss_bytes()
    tracemalloc.start()

    t0 = time.monotonic()
    valid_ids = _get_valid_source_row_ids_at_version(src_ref, src_version, query)
    t_valid_ids = time.monotonic() - t0

    mv_version_before = mv.to_lance().version
    t0 = time.monotonic()
    deleted = _delete_rows_not_in_source_version(
        mv, valid_ids, batch_size=MAX_DELETE_BATCH_SIZE
    )
    t_delete = time.monotonic() - t0

    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    rss_after = _ru_maxrss_bytes()

    # Each DELETE batch is one commit on the MV; nothing else writes to it.
    delete_batches = mv.to_lance().version - mv_version_before
    expected_batches = math.ceil(deleted / MAX_DELETE_BATCH_SIZE)

    assert len(valid_ids) == expected_valid, (
        f"valid-id set has {len(valid_ids)} ids, expected {expected_valid}"
    )
    assert deleted == num_deleted_source, (
        f"delete sync removed {deleted} rows, expected {num_deleted_source}"
    )
    assert mv.count_rows() == expected_valid, (
        f"MV has {mv.count_rows()} rows after delete sync, expected {expected_valid}"
    )
    assert delete_batches == expected_batches, (
        f"delete sync used {delete_batches} DELETE commits, "
        f"expected ceil({deleted}/{MAX_DELETE_BATCH_SIZE}) = {expected_batches}"
    )

    bytes_per_row = peak_bytes / num_rows
    _BYTES_PER_ROW[num_rows] = bytes_per_row

    result = make_result(
        scale=num_rows,
        latencies=[t_valid_ids, t_delete],
        error_count=0,
        elapsed_s=t_valid_ids + t_delete,
        metadata={
            "peak_tracemalloc_bytes": peak_bytes,
            "bytes_per_row": bytes_per_row,
            "rss_before_bytes": rss_before,
            "rss_after_bytes": rss_after,
            "valid_ids_s": t_valid_ids,
            "delete_s": t_delete,
            "deleted_rows": deleted,
            "delete_batches": delete_batches,
        },
    )
    log_result(result)
    _LOG.info(
        "delete sync at %d rows: peak=%.1f MiB (%.1f bytes/row), "
        "valid_ids=%.1fs delete=%.1fs batches=%d",
        num_rows,
        peak_bytes / (1024 * 1024),
        bytes_per_row,
        t_valid_ids,
        t_delete,
        delete_batches,
    )

    smallest = min(_BYTES_PER_ROW)
    if num_rows != smallest:
        baseline = _BYTES_PER_ROW[smallest]
        if bytes_per_row > baseline * _MAX_BYTES_PER_ROW_RATIO:
            _LOG.warning(
                "SUPERLINEAR DRIVER MEMORY: %.1f bytes/row at %d rows vs "
                "%.1f bytes/row at %d rows (> %.1fx linear)",
                bytes_per_row,
                num_rows,
                baseline,
                smallest,
                _MAX_BYTES_PER_ROW_RATIO,
            )


def test_mv_delete_sync_through_refresh(tmp_path: Path, local_ray) -> None:
    """End-to-end wiring: a real refresh runs the same batched delete sync.

    Deleting 30k of 100k source rows must leave the MV equal to the Arrow
    oracle, and the refresh must have issued at least ceil(30k/10k) = 3
    DELETE commits on the MV (visible as a version delta of at least 3).
    """
    num_rows = 100_000
    num_deleted = 30_000

    db = geneva.connect(str(tmp_path))
    src = _build_int_source(db, "src_e2e", num_rows)
    mv = _identity_mv(db, src, "mv_e2e")

    # Populate, then sync a delete-only source change.
    mv.refresh(_admission_check=False)
    src.delete(f"id < {num_deleted}")

    mv_version_before = mv.to_lance().version
    t0 = time.monotonic()
    mv.refresh(_admission_check=False)
    refresh_s = time.monotonic() - t0
    version_delta = mv.to_lance().version - mv_version_before

    expected_batches = math.ceil(num_deleted / MAX_DELETE_BATCH_SIZE)

    got_ids = _sorted_ids(mv)
    expected_ids = _sorted_ids(src)
    assert got_ids == expected_ids, (
        f"MV diverged from source after delete-sync refresh: "
        f"{len(got_ids)} rows vs oracle {len(expected_ids)} rows"
    )
    # The refresh commits each DELETE batch separately, so its version delta
    # is at least the expected batch count.
    assert version_delta >= expected_batches, (
        f"refresh advanced the MV by {version_delta} versions, expected at "
        f"least {expected_batches} DELETE commits for {num_deleted} deletions"
    )

    result = make_result(
        scale=num_rows,
        latencies=[refresh_s],
        error_count=0,
        elapsed_s=refresh_s,
        metadata={
            "deleted_rows": num_deleted,
            "mv_version_delta": version_delta,
            "expected_delete_batches": expected_batches,
        },
    )
    log_result(result)
