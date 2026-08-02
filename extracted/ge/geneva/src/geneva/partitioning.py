# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Utilities for assigning partition IDs to table rows via vector indexes."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, cast

import pyarrow as pa

if TYPE_CHECKING:
    from geneva.table import Table

_LOG = logging.getLogger(__name__)

# Lance type_url that identifies a vector index (IVF_FLAT, IVF_PQ, etc.).
# Used to filter out non-vector indices (e.g. BITMAP) on the same column.
_VECTOR_INDEX_TYPE_URLS = (
    "/lance.index.pb.VectorIndexDetails",
    "/lance.table.VectorIndexDetails",
)


# Target number of rows per partition.  Keeps per-partition pairwise
# comparison cost bounded at ~O(target^2) regardless of dataset size.
# See internal_docs/designs/image_dedup_pipeline.md "Choosing k".
DEFAULT_TARGET_PARTITION_SIZE = 50_000

# Minimum number of partitions to create (avoids degenerate single-partition).
_MIN_PARTITIONS = 2


def create_ivf_flat_index(
    tbl: Table,
    column: str,
    k: int | None = None,
    *,
    metric: str = "hamming",
    target_partition_size: int = DEFAULT_TARGET_PARTITION_SIZE,
) -> str:
    """Create an IVF_FLAT index on *column* and return the index name.

    Separated from partition assignment so callers can create the index
    independently (e.g., for direct VectorIndexReader usage).

    Parameters
    ----------
    tbl:
        The Geneva table to index.  Must already contain *column*.
    column:
        The vector column to build the IVF_FLAT index on.
    k:
        Requested number of partitions (``num_partitions`` for the index).
        If *None*, automatically chosen as ``n / target_partition_size``
        (clamped to at least 2).
    metric:
        Distance metric passed to ``create_index``.  Defaults to ``"hamming"``.
    target_partition_size:
        Target rows per partition, used when *k* is ``None``.  Defaults to
        50,000 (see ``internal_docs/designs/image_dedup_pipeline.md``).

    Returns
    -------
    str
        The name of the created index (as reported by ``describe_indices``).

    Note
    ----
    Lance's IVF k-means needs sufficient data per partition (typically ~256
    samples) to converge well.  If *k* is too large relative to the number of
    rows, some partitions may end up empty.
    """
    from geneva.query import open_read_dataset

    lance_ds = open_read_dataset(tbl)

    if k is None:
        n = lance_ds.count_rows()
        k = max(_MIN_PARTITIONS, n // target_partition_size)
        _LOG.info(
            "Auto-selected k=%d for %d rows (target_partition_size=%d)",
            k,
            n,
            target_partition_size,
        )

    lance_ds.create_index(
        column,
        index_type="IVF_FLAT",
        num_partitions=k,
        metric=metric,
        replace=True,
    )

    # Advance the LanceDB Table to the version that includes the index so
    # that callers (e.g. _build_index_partition_work_items) can see it via
    # tbl.to_lance() without re-opening at the latest version.
    tbl.checkout_latest()

    # TODO: describe_indices should not require filtering by type_url;
    # this is a workaround for a current limitation in the API.
    idx_info = next(
        idx
        for idx in lance_ds.describe_indices()
        if column in idx.field_names and idx.type_url in _VECTOR_INDEX_TYPE_URLS
    )
    return idx_info.name


def assign_partitions_from_index(
    tbl: Table,
    column: str,
) -> None:
    """Add a ``partition_id`` column whose values come directly from an
    existing IVF_FLAT index's partition assignments.

    The index must already exist on *column* — use
    [`create_ivf_flat_index`][create_ivf_flat_index] to create one first.

    This runs entirely on the driver — no Ray cluster or UDF backfill needed.

    Parameters
    ----------
    tbl:
        The Geneva table to partition.
    column:
        The vector column that has an IVF_FLAT index.
    """
    import lance
    from lance.dataset import VectorIndexReader

    from geneva.query import open_read_dataset

    # Re-open the dataset to pick up the index.
    lance_ds = lance.dataset(
        open_read_dataset(tbl).uri, storage_options=tbl._storage_options
    )
    # TODO: describe_indices should not require filtering by type_url;
    # this is a workaround for a current limitation in the API.
    idx_info = next(
        idx
        for idx in lance_ds.describe_indices()
        if column in idx.field_names and idx.type_url in _VECTOR_INDEX_TYPE_URLS
    )
    index_name = idx_info.name
    reader = VectorIndexReader(lance_ds, index_name)

    rowid_to_pid: dict[int, int] = {}
    for pid in range(reader.num_partitions()):
        part = reader.read_partition(pid)
        rowids = cast("list[int]", part.column("_rowid").to_pylist())
        for rid in rowids:
            rowid_to_pid[rid] = pid

    _LOG.info(
        "IVF_FLAT index %s: %d rows assigned to %d partitions",
        index_name,
        len(rowid_to_pid),
        len(set(rowid_to_pid.values())),
    )

    # Add partition_id column by looking up each row's _rowid in the map.
    #
    # We use lance.batch_udf (not a Geneva UDF) because this is a trivial
    # dict lookup that runs in-process on the driver — no need to spin up a
    # Ray cluster.  Key properties of lance.batch_udf + add_columns:
    #
    #  - Eager, not lazy: add_columns() iterates every batch, calls the
    #    function, and writes the new column to disk immediately.  There is
    #    no separate "backfill" step.
    #  - Static result: the written column values are plain data on disk.
    #    If rows are added later they will have NULL for partition_id.
    #    If the index is rebuilt the existing values become stale.
    #  - Bypasses Geneva versioning: writes directly to the lance dataset,
    #    so we must call tbl.checkout_latest() afterwards for Geneva to see
    #    the new column.
    #
    # This is appropriate here because the pipeline is a linear one-shot
    # flow (index → partition → UDTFs) with no incremental updates.
    @lance.batch_udf(output_schema=pa.schema([pa.field("partition_id", pa.int32())]))
    def _assign(batch: pa.RecordBatch) -> pa.RecordBatch:
        rids = cast("list[int]", batch.column("_rowid").to_pylist())
        empty_count = 0
        pids = []
        for rid in rids:
            pid = rowid_to_pid.get(rid)
            if pid is None:
                empty_count += 1
                pid = 0
            pids.append(pid)
        if empty_count:
            _LOG.warning(
                "%d rows in batch had no index partition assignment, "
                "defaulted to partition 0",
                empty_count,
            )
        return pa.RecordBatch.from_pydict(
            {"partition_id": pa.array(pids, type=pa.int32())}
        )

    # Re-open the dataset to pick up the index changes, add the column,
    # then refresh Geneva's Table reference to the latest version.
    lance_ds = lance.dataset(lance_ds.uri, storage_options=tbl._storage_options)
    lance_ds.add_columns(_assign, read_columns=["_rowid"])
    tbl.checkout_latest()
