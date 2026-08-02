# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Test incremental and async backfill functionality.

These tests verify that backfills can be run incrementally and asynchronously.
"""

import logging
import time

import pytest

_LOG = logging.getLogger(__name__)

# Well-known manifest name (uploaded via upload_manifests.py)
MANIFEST_NAME = "simple-udfs-v1"


def test_oxford_pets_incremental_backfill(
    oxford_pets_table: tuple,
    standard_cluster: str,
    batch_size: int,
) -> None:
    """
    Test incremental backfill with num_frags parameter.

    This verifies that backfill can be run multiple times on subsets
    of fragments and will resume from where it left off.
    """
    conn, tbl, _ = oxford_pets_table
    num_images = len(tbl)

    _LOG.info(f"Using shared table with {num_images} rows for incremental backfill test")

    # Use file_size column (already added by upload_manifests.py)
    test_column = "file_size"

    # Use conn.context() with cluster and manifest
    with conn.context(cluster=standard_cluster, manifest=MANIFEST_NAME):

        # First backfill - process only 2 fragments
        _LOG.info("Backfill 1: Processing first 2 fragments")
        tbl.backfill(test_column, batch_size=batch_size, num_frags=2)
        tbl.checkout_latest()
        df = tbl.to_pandas()
        filled_rows_1 = df[test_column].notna().sum()
        _LOG.info(f"After backfill 1: {filled_rows_1} rows filled")

        # Second backfill - process 2 more fragments, first 2 already done.
        _LOG.info("Backfill 2: Processing next 2 fragments")
        tbl.backfill(test_column, batch_size=batch_size, num_frags=4)
        tbl.checkout_latest()
        df = tbl.to_pandas()
        filled_rows_2 = df[test_column].notna().sum()
        _LOG.info(f"After backfill 2: {filled_rows_2} rows filled")

        # Third backfill - complete the rest
        _LOG.info("Backfill 3: Processing remaining fragments")
        tbl.backfill(test_column, batch_size=batch_size)
        tbl.checkout_latest()
        df = tbl.to_pandas()
        filled_rows_3 = df[test_column].notna().sum()
        _LOG.info(f"After backfill 3: {filled_rows_3} rows filled")

    # Assertions
    assert filled_rows_1 > 0, "First backfill should fill some rows"
    # if there are only 2 or fewer fragments, filled_rows_2 will be num_images
    assert filled_rows_2 == num_images or filled_rows_2 > filled_rows_1, (
        "Second backfill should fill more rows"
    )
    assert filled_rows_3 == num_images, (
        f"Final backfill should fill all {num_images} rows"
    )
    assert df[test_column].notna().all(), (
        "All rows should be filled after complete backfill"
    )

    _LOG.info("Incremental backfill test passed!")


def test_oxford_pets_async_backfill(
    oxford_pets_table: tuple,
    standard_cluster: str,
    batch_size: int,
) -> None:
    """
    Test asynchronous backfill with progress monitoring.

    This verifies that backfill_async returns a future that can be
    monitored and that intermediate commits are visible.
    """
    conn, tbl, _ = oxford_pets_table
    num_images = len(tbl)

    _LOG.info(f"Using shared table with {num_images} rows for async backfill test")

    # Use dimensions column (already added by upload_manifests.py)
    # Using dimensions instead of file_size to avoid conflict with incremental test
    test_column = "dimensions"

    # Use conn.context() with cluster and manifest
    with conn.context(cluster=standard_cluster, manifest=MANIFEST_NAME):

        _LOG.info("Starting async backfill")
        fut = tbl.backfill_async(
            test_column, batch_size=batch_size, commit_granularity=2
        )

        # Monitor progress
        iterations = 0
        while not fut.done():
            time.sleep(2)
            tbl.checkout_latest()
            try:
                df = tbl.to_pandas()
                done_rows = df[test_column].notna().sum()
                _LOG.info(
                    f"Async backfill in progress: {done_rows}/{num_images} rows, "
                    f"version {tbl.version}"
                )
            except Exception as e:
                _LOG.warning(f"Could not check progress: {e}")
            iterations += 1

            # Safety timeout
            if iterations > 100:
                pytest.fail("Async backfill timed out after 200 seconds")

        _LOG.info("Async backfill completed")

        # Verify final state
        tbl.checkout_latest()
        df = tbl.to_pandas()

    # Assertions
    assert df[test_column].notna().all(), "All rows should be filled"
    assert len(df) == num_images, f"Expected {num_images} rows"

    _LOG.info("Async backfill test passed!")
