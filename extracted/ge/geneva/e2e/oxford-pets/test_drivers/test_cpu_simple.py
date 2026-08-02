# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Test CPU-based simple UDFs (file_size, dimensions).

These tests use minimal dependencies and run on any worker.
"""

import logging

_LOG = logging.getLogger(__name__)

# Well-known manifest name (uploaded via upload_manifests.py)
MANIFEST_NAME = "simple-udfs-v1"


def test_oxford_pets_cpu_pipeline(
    oxford_pets_table: tuple,
    standard_cluster: str,
    batch_size: int,
) -> None:
    """
    Test CPU-based feature engineering pipeline.

    This test:
    1. Uses shared Oxford pets images table
    2. Runs file_size and dimensions UDFs
    3. Validates results
    """
    conn, tbl, _ = oxford_pets_table
    num_images = len(tbl)

    _LOG.info(f"Using shared table with {num_images} rows")
    _LOG.info(f"Initial schema: {tbl.schema}")

    # Use conn.context() with cluster and manifest
    # Columns already added by upload_manifests.py
    with conn.context(cluster=standard_cluster, manifest=MANIFEST_NAME):
        _LOG.info(f"Schema: {tbl.schema}")

        # Backfill file_size
        _LOG.info("Backfilling file_size column")
        tbl.backfill("file_size", batch_size=batch_size, commit_granularity=5)
        _LOG.info("file_size backfill complete")

        # Backfill dimensions
        _LOG.info("Backfilling dimensions column")
        tbl.backfill("dimensions", batch_size=batch_size, commit_granularity=5)
        _LOG.info("dimensions backfill complete")

    # Validate results
    tbl.checkout_latest()
    df = tbl.to_pandas()
    _LOG.info(f"Final table shape: {df.shape}")
    _LOG.info(f"Final schema: {tbl.schema}")

    # Assertions
    assert len(df) == num_images, f"Expected {num_images} rows, got {len(df)}"
    assert "file_size" in df.columns, "file_size column not found"
    assert "dimensions" in df.columns, "dimensions column not found"
    assert df["file_size"].notna().all(), "file_size has null values"
    assert df["dimensions"].notna().all(), "dimensions has null values"
    assert (df["file_size"] > 0).all(), "file_size should be positive"

    _LOG.info("CPU pipeline test passed!")
