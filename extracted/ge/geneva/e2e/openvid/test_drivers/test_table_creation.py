# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Test basic table creation and video loading for OpenVid pipeline.

This is a minimal test to verify the e2e scaffolding works.
"""

import logging

_LOG = logging.getLogger(__name__)


def test_openvid_table_creation(
    openvid_table: tuple,
    num_videos: int,
) -> None:
    """
    Test that the OpenVid table is created correctly.

    This test:
    1. Uses shared OpenVid table fixture
    2. Validates table schema and row count
    3. Checks that required CSV columns exist (video, caption, frame, fps, seconds)
    """
    conn, tbl, table_name = openvid_table

    _LOG.info(f"Testing table: {table_name}")
    _LOG.info(f"Table schema: {tbl.schema}")
    _LOG.info(f"Table row count: {len(tbl)}")

    # Validate schema - check for expected columns from HF Lance dataset
    schema = tbl.schema
    expected_columns = ["video_path", "video", "caption", "frame", "fps", "seconds"]

    for col in expected_columns:
        assert col in schema.names, f"{col} column not found in schema"

    # Validate data — use to_pandas() for an authoritative row count
    # (len(tbl) can be inflated on object stores after add_columns).
    # The openvid_table fixture is session-scoped and other tests (MV refresh,
    # blob tests) may add rows before this test runs, so we check >= rather
    # than strict equality.
    df = tbl.to_pandas()
    actual_rows = len(df)
    _LOG.info(f"len(tbl)={len(tbl)}, len(df)={actual_rows}")
    assert actual_rows >= num_videos, (
        f"Expected at least {num_videos} rows, got {actual_rows}"
    )
    _LOG.info(f"Sample data:\n{df.head()}")

    # Check required columns have data
    assert df["video_path"].notna().all(), "video_path column has null values"
    assert df["video"].notna().all(), "video column has null values"
    assert df["caption"].notna().all(), "caption column has null values"

    # Check numeric columns
    assert df["frame"].notna().all(), "frame column has null values"
    assert df["fps"].notna().all(), "fps column has null values"
    assert df["seconds"].notna().all(), "seconds column has null values"

    _LOG.info("Table creation test passed!")
