# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Implementation of MV blob tests.

These tests run in the frame_extractor UDF environment (Ray 2.54.0)
and are invoked via subprocess from test_mv_blobs.py.
"""

import logging
import os

import pytest

import geneva

_LOG = logging.getLogger(__name__)


@pytest.fixture
def mv_blob_table() -> tuple:
    """Create a connection and table for blob MV tests."""
    bucket_path = os.environ.get("GENEVA_TEST_BUCKET")
    table_name = os.environ.get("GENEVA_TABLE_NAME")

    if not bucket_path or not table_name:
        pytest.skip("GENEVA_TEST_BUCKET and GENEVA_TABLE_NAME must be set")

    conn = geneva.connect(bucket_path)
    tbl = conn.open_table(table_name)

    _LOG.info(f"Opened table: {table_name}, rows: {tbl.count_rows()}")
    return conn, tbl, table_name


def test_mv_with_frame_blob_column(mv_blob_table, request) -> None:
    """Test creating MV with blob-producing UDF (ExtractFirstFrame)."""
    conn, source_tbl, table_name = mv_blob_table

    from geneva.udfs.video.frame_extractor import ExtractFirstFrame

    _LOG.info(f"Creating blob MV from source table '{table_name}'")

    mv_name = f"{table_name}_blob_mv"
    mv = (
        source_tbl.search(None)
        .select({
            "video": "video",
            "first_frame": ExtractFirstFrame(),
        })
        .create_materialized_view(conn, mv_name)
    )

    _LOG.info(f"MV created: {mv_name}, schema: {mv.schema.names}")

    # Verify blob column exists
    assert "first_frame" in mv.schema.names

    # Check blob metadata on the field
    frame_field = mv.schema.field("first_frame")
    assert frame_field.metadata is not None
    assert frame_field.metadata.get(b"lance-encoding:blob") == b"true"

    _LOG.info("Blob MV created with correct metadata")


def test_mv_blob_metadata_propagates(mv_blob_table, request) -> None:
    """Test that blob field metadata survives MV refresh (PR #437 fix)."""
    conn, source_tbl, table_name = mv_blob_table

    from geneva.udfs.video.frame_extractor import ExtractFirstFrame

    cluster_name = os.environ.get("GENEVA_CLUSTER_NAME")
    if not cluster_name:
        pytest.skip("GENEVA_CLUSTER_NAME must be set")

    mv_name = f"{table_name}_blob_meta_mv"
    mv = (
        source_tbl.search(None)
        .limit(5)  # Small subset for faster testing
        .select({
            "video": "video",
            "first_frame": ExtractFirstFrame(),
        })
        .create_materialized_view(conn, mv_name)
    )

    # Check metadata before refresh
    frame_field_before = mv.schema.field("first_frame")
    _LOG.info(f"Metadata before refresh: {frame_field_before.metadata}")
    assert frame_field_before.metadata.get(b"lance-encoding:blob") == b"true"

    # Refresh requires a cluster context to run the backfill
    _LOG.info("Refreshing blob MV...")
    with conn.context(cluster=cluster_name, manifest="frame-extractor-v1"):
        mv.refresh()

    # Re-open table to get fresh schema
    mv = conn.open_table(mv_name)

    # Check metadata after refresh
    frame_field_after = mv.schema.field("first_frame")
    _LOG.info(f"Metadata after refresh: {frame_field_after.metadata}")

    # This was the bug fixed in PR #437 - metadata should be preserved
    assert frame_field_after.metadata is not None
    assert frame_field_after.metadata.get(b"lance-encoding:blob") == b"true"

    _LOG.info("Blob metadata correctly propagated through refresh")


def test_mv_take_blobs_after_refresh(mv_blob_table, request) -> None:
    """Test that take_blobs() works on MV after refresh."""
    conn, source_tbl, table_name = mv_blob_table

    from geneva.udfs.video.frame_extractor import ExtractFirstFrame

    cluster_name = os.environ.get("GENEVA_CLUSTER_NAME")
    if not cluster_name:
        pytest.skip("GENEVA_CLUSTER_NAME must be set")

    mv_name = f"{table_name}_blob_take_mv"
    mv = (
        source_tbl.search(None)
        .limit(3)  # Small subset for testing
        .select({
            "video": "video",
            "first_frame": ExtractFirstFrame(),
        })
        .create_materialized_view(conn, mv_name)
    )

    # Refresh requires a cluster context to run the backfill
    _LOG.info("Refreshing blob MV...")
    with conn.context(cluster=cluster_name, manifest="frame-extractor-v1"):
        mv.refresh()

    # Assertions below don't need a cluster context
    row_count = mv.count_rows()
    _LOG.info(f"MV has {row_count} rows after refresh")

    if row_count == 0:
        pytest.skip("No rows in MV after refresh")

    # Take blobs from the MV
    indices = list(range(min(row_count, 3)))
    _LOG.info(f"Taking blobs at indices: {indices}")

    blob_files = mv.take_blobs(indices=indices, column="first_frame")
    _LOG.info(f"Retrieved {len(blob_files)} blob files")

    # Verify blobs are valid PNG data
    for i, blob in enumerate(blob_files):
        if blob is not None:
            data = blob.read()
            _LOG.info(f"Blob {i}: {len(data)} bytes")
            # PNG files start with specific magic bytes
            assert data[:4] == b"\x89PNG", f"Blob {i} is not a valid PNG"
        else:
            _LOG.warning(f"Blob {i} is None (extraction may have failed)")

    _LOG.info("take_blobs() works correctly on MV after refresh")
