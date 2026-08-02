# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""End-to-end tests for the image dedup pipeline using batch UDTFs.

Two-stage pipeline:
  1. EdgeDetection UDTF — partitioned pairwise hamming comparison
  2. DedupClustering UDTF — global union-find connected components
"""

from __future__ import annotations

import logging

import pytest

from geneva.udtfs import dedupe_clustering_udtf, edge_detection_udtf

_LOG = logging.getLogger(__name__)

MAX_PAIRS_PER_CLUSTER_TO_CHECK = 100


def _get_threshold(num_images: int) -> int:
    """Get hamming distance threshold based on dataset size.

    CIFAR-10 images are quite diverse. With fewer images, we need a higher
    threshold to find similar pairs. With more images (10k+), we're more
    likely to find truly similar images at a stricter threshold.
    """
    if num_images >= 10000:
        return 4
    return 20


def _hamming_distance(a: list[int], b: list[int]) -> int:
    """Compute hamming distance between two pHash byte arrays."""
    dist = 0
    for x, y in zip(a, b, strict=True):
        dist += bin(x ^ y).count("1")
    return dist


# ---------------------------------------------------------------------------
# Tests — full pipeline with pHash UDF + centroid partitioning
# ---------------------------------------------------------------------------


def test_full_pipeline_with_phash_udf(
    image_source_table: tuple,
    standard_cluster: str,
    manifest_name: str,
) -> None:
    """Full pipeline from raw CIFAR-10 images: pHash UDF → partition → UDTFs."""
    from conftest import (
        create_ivf_flat_index,
        make_compute_phash,
    )

    conn, tbl, table_name = image_source_table

    with conn.context(cluster=standard_cluster, manifest=manifest_name):
        # Step 0: Compute pHash via UDF
        tbl.add_columns({"phash": make_compute_phash()})
        tbl.backfill("phash")

    # Verify phash column is populated
    arrow_tbl = tbl.to_arrow()
    total_rows = arrow_tbl.num_rows
    phash_col = arrow_tbl.column("phash")
    non_null = sum(1 for v in phash_col if v.as_py() is not None)
    assert non_null == total_rows, (
        f"Expected {total_rows} non-null phashes, got {non_null}"
    )

    # Determine threshold based on dataset size
    threshold = _get_threshold(total_rows)
    _LOG.info("Using hamming threshold=%d for %d images", threshold, total_rows)

    # Step 0b: Build IVF_FLAT index (partition_by_indexed_column reads it at refresh)
    k = max(8, total_rows // 1000)
    create_ivf_flat_index(tbl, "phash", k=k)

    with conn.context(cluster=standard_cluster, manifest=manifest_name):
        # Steps 1-3: Edge detection UDTF (uses _rowid for efficient take)
        query = tbl.search(None).select(["_rowid", "phash"])
        edge_view = conn.create_udtf_view(
            f"{table_name}_edges",
            query,
            edge_detection_udtf(
                input_columns=["_rowid", "phash"],
                partition_by_indexed_column="phash",
                threshold=threshold,
            ),
        )
        edge_view.refresh()

    # Log any edge detection errors before proceeding
    edge_errors = edge_view.get_errors()
    for err in edge_errors:
        _LOG.error(
            "Edge UDTF error: %s: %s\n%s",
            err.error_type,
            err.error_message,
            err.error_trace,
        )

    with conn.context(cluster=standard_cluster, manifest=manifest_name):
        # Steps 4-5: Clustering UDTF
        cluster_query = edge_view.search(None).select(["row_id_a", "row_id_b"])
        cluster_view = conn.create_udtf_view(
            f"{table_name}_clusters",
            cluster_query,
            dedupe_clustering_udtf(
                input_columns=["row_id_a", "row_id_b"],
                partition_by="partition_id",
            ),
        )
        cluster_view.refresh()

    # Log any clustering errors
    cluster_errors = cluster_view.get_errors()
    for err in cluster_errors:
        _LOG.error(
            "Cluster UDTF error: %s: %s\n%s",
            err.error_type,
            err.error_message,
            err.error_trace,
        )

    result = cluster_view.to_arrow()
    edge_result = edge_view.to_arrow()
    _LOG.info(
        "Pipeline stats: %d images → %d edges → %d clusters"
        " (%d edge errors, %d cluster errors)",
        total_rows,
        edge_result.num_rows,
        result.num_rows,
        len(edge_errors),
        len(cluster_errors),
    )

    # If no edges found, check whether it was due to UDTF errors
    if edge_result.num_rows == 0 and len(edge_errors) > 0:
        pytest.fail(
            f"Edge detection produced 0 edges but had {len(edge_errors)} "
            f"errors across {k} requested partitions. "
            f"First error: {edge_errors[0].error_type}: "
            f"{edge_errors[0].error_message}"
        )

    # Require actual clusters to be produced
    assert result.num_rows > 0, (
        f"Expected at least one cluster from {total_rows} CIFAR-10 images, "
        f"but got 0 clusters ({edge_result.num_rows} edges, "
        f"{len(edge_errors)} edge errors, {len(cluster_errors)} cluster errors)"
    )

    # Verify cluster validity properties (one row per cluster)
    rep_row_ids = result.column("representative_row_id").to_pylist()
    dup_row_ids_col = result.column("duplicate_row_ids").to_pylist()
    num_clusters = len(rep_row_ids)

    # Verify each cluster's representative is smaller than all duplicates
    total_matched_images = 0
    for rep, dups in zip(rep_row_ids, dup_row_ids_col, strict=True):
        assert all(rep < d for d in dups), (
            f"Representative {rep} is not smaller than all duplicates {dups}"
        )
        assert rep not in dups, f"Representative {rep} should not be in duplicates"
        total_matched_images += 1 + len(dups)  # rep + duplicates

    _LOG.info(
        "Cluster validity OK: %d clusters containing %d matched images",
        num_clusters,
        total_matched_images,
    )

    # Verify that EDGES are within threshold (not all cluster pairs)
    # Union-find creates transitive clusters: if A-B similar and B-C similar,
    # then A,B,C are in same cluster even if A-C distance > threshold
    _LOG.info("Verifying edge pHash similarity...")
    edge_dict = edge_result.to_pydict()
    num_edges = len(edge_dict["row_id_a"])

    # Sample edges if too many
    edges_to_check = min(num_edges, MAX_PAIRS_PER_CLUSTER_TO_CHECK)

    # Collect unique row_ids from edges to check
    row_ids_needed: set[int] = set()
    for i in range(edges_to_check):
        row_ids_needed.add(edge_dict["row_id_a"][i])
        row_ids_needed.add(edge_dict["row_id_b"][i])

    # Fetch pHashes and build mapping
    edge_data = tbl.take_row_ids(list(row_ids_needed)).with_row_id().to_arrow()
    rowid_to_phash = {
        rid: phash
        for rid, phash in zip(
            edge_data.column("_rowid").to_pylist(),
            edge_data.column("phash").to_pylist(),
            strict=True,
        )
    }

    # Verify each edge
    for i in range(edges_to_check):
        rid_a = edge_dict["row_id_a"][i]
        rid_b = edge_dict["row_id_b"][i]
        dist = _hamming_distance(rowid_to_phash[rid_a], rowid_to_phash[rid_b])
        assert dist <= threshold, (
            f"Edge ({rid_a}, {rid_b}) has hamming distance {dist} > threshold {threshold}"
        )

    _LOG.info(
        "Edge verification passed: %d edges verified out of %d total",
        edges_to_check,
        num_edges,
    )
