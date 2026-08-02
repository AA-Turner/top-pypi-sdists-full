# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Shared UDTF factories and schemas for the image-dedupe pipeline.

Two-stage pipeline:
  1. EdgeDetection UDTF — partitioned pairwise hamming comparison
  2. DedupClustering UDTF — per-partition union-find connected components
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pyarrow as pa

import geneva

if TYPE_CHECKING:
    from collections.abc import Iterator

    from geneva.query import GenevaQueryBuilder
    from geneva.transformer import UDTF

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

EDGE_SCHEMA = pa.schema(
    [
        pa.field("row_id_a", pa.uint64()),
        pa.field("row_id_b", pa.uint64()),
        pa.field("partition_id", pa.int32()),
    ]
)

DEDUP_OUTPUT_SCHEMA = pa.schema(
    [
        pa.field("representative_row_id", pa.uint64()),
        pa.field("duplicate_row_ids", pa.list_(pa.uint64())),
    ]
)

# ---------------------------------------------------------------------------
# UDTF factories — defined inside functions so cloudpickle embeds them
# rather than referencing this module by name.
# ---------------------------------------------------------------------------


def edge_detection_udtf(
    input_columns: list[str],
    partition_by_indexed_column: str,
    threshold: int = 4,
) -> UDTF:
    """Create an EdgeDetection UDTF (all-pairs hamming within a partition).

    Performs pairwise hamming-distance comparison across all rows within
    each partition, emitting edges for pairs whose distance is at or
    below *threshold*.  Each edge includes the IVF ``partition_id`` so
    that downstream UDTFs (e.g. DedupClustering) can use it as a
    ``partition_by`` key for parallel execution.

    The ``_partition_id`` column is injected automatically by the
    framework when using ``partition_by_indexed_column``
    (see ``_IndexPartitionSource`` in ``table.py``).

    Parameters
    ----------
    input_columns : list[str]
        Source columns to read. Must contain ``_rowid`` and the hash column
        (e.g. ``["_rowid", "phash"]``).
    partition_by_indexed_column : str
        Column name that has an existing IVF vector index to partition by.
    threshold : int, optional
        Maximum hamming distance to consider two hashes as similar.
        Default is 4.
    """

    def _hamming_distance(a: list[int], b: list[int]) -> int:
        dist = 0
        for x, y in zip(a, b, strict=True):
            dist += bin(x ^ y).count("1")
        return dist

    @geneva.udtf(  # type: ignore[operator]
        output_schema=EDGE_SCHEMA,
        input_columns=input_columns,
        partition_by_indexed_column=partition_by_indexed_column,
        on_error=geneva.skip_on_error(),
    )
    class EdgeDetection:
        def __init__(self, thresh: int = 4) -> None:
            self.threshold = thresh

        def __call__(self, source: GenevaQueryBuilder) -> Iterator[pa.RecordBatch]:
            data = source.to_arrow()
            if data.num_rows == 0:
                return
            row_ids = cast("list[int]", data.column("_rowid").to_pylist())
            phashes = cast("list[list[int]]", data.column("phash").to_pylist())
            # _partition_id is injected by the framework when using
            # partition_by_indexed_column (see _IndexPartitionSource).
            partition_id = cast("int", data.column("_partition_id")[0].as_py())

            edges_a: list[int] = []
            edges_b: list[int] = []

            n = len(row_ids)
            for i in range(n):
                for j in range(i + 1, n):
                    rid_a, rid_b = row_ids[i], row_ids[j]
                    if rid_a > rid_b:
                        rid_a, rid_b = rid_b, rid_a
                    if _hamming_distance(phashes[i], phashes[j]) <= self.threshold:
                        edges_a.append(rid_a)
                        edges_b.append(rid_b)

            if edges_a:
                yield pa.RecordBatch.from_pydict(
                    {
                        "row_id_a": edges_a,
                        "row_id_b": edges_b,
                        "partition_id": pa.array(
                            [partition_id] * len(edges_a), type=pa.int32()
                        ),
                    },
                    schema=EDGE_SCHEMA,
                )

    return EdgeDetection(thresh=threshold)  # type: ignore[call-arg]


def dedupe_clustering_udtf(
    input_columns: list[str],
    partition_by: str | None = None,
) -> UDTF:
    """Create a DedupClustering UDTF (union-find connected components).

    Reads edge pairs and clusters them via union-find, emitting one row
    per cluster with the representative row_id and list of all duplicate row_ids.

    Parameters
    ----------
    input_columns : list[str]
        Source columns containing the edge pair row IDs
        (e.g. ``["row_id_a", "row_id_b"]``).
    partition_by : str | None, optional
        Column in the edge view to partition by for parallel execution.
        Set to ``"partition_id"`` when the upstream EdgeDetection UDTF
        emits partition IDs, enabling parallel union-find per IVF
        partition.  Defaults to ``None`` (single-worker clustering).
    """

    @geneva.udtf(  # type: ignore[operator]
        output_schema=DEDUP_OUTPUT_SCHEMA,
        input_columns=input_columns,
        partition_by=partition_by,
        on_error=geneva.skip_on_error(),
    )
    class DedupClustering:
        def __call__(self, source: GenevaQueryBuilder) -> Iterator[pa.RecordBatch]:
            data = source.to_arrow()
            ids_a = cast("list[int]", data.column("row_id_a").to_pylist())
            ids_b = cast("list[int]", data.column("row_id_b").to_pylist())

            parent: dict[int, int] = {}

            def find(x: int) -> int:
                while parent.get(x, x) != x:
                    parent[x] = parent.get(parent[x], parent[x])  # type: ignore[assignment]
                    x = parent[x]
                return x

            def union(a: int, b: int) -> None:
                ra, rb = find(a), find(b)
                if ra != rb:
                    if ra > rb:
                        ra, rb = rb, ra
                    parent[rb] = ra

            for a, b in zip(ids_a, ids_b, strict=True):
                if a not in parent:
                    parent[a] = a
                if b not in parent:
                    parent[b] = b
                union(a, b)

            # Group nodes by their root (cluster representative)
            clusters: dict[int, list[int]] = {}
            for node in parent:
                root = find(node)
                clusters.setdefault(root, []).append(node)

            rep_row_ids: list[int] = []
            dup_row_ids: list[list[int]] = []

            for rep in sorted(clusters.keys()):
                # Duplicates exclude the representative itself
                duplicates = sorted(m for m in clusters[rep] if m != rep)
                if duplicates:  # Only emit clusters with actual duplicates
                    rep_row_ids.append(rep)
                    dup_row_ids.append(duplicates)

            if rep_row_ids:
                yield pa.RecordBatch.from_pydict(
                    {
                        "representative_row_id": rep_row_ids,
                        "duplicate_row_ids": dup_row_ids,
                    },
                    schema=DEDUP_OUTPUT_SCHEMA,
                )

    return DedupClustering()  # type: ignore[call-arg]
