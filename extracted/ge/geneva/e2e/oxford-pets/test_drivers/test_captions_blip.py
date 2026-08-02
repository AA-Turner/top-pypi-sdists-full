# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Test BLIP caption generation.

This test uses the BLIP model for GPU-accelerated image captioning.
"""

import logging

import pytest

_LOG = logging.getLogger(__name__)

# Well-known manifest name (uploaded via upload_manifests.py)
MANIFEST_NAME = "blip-udfs-v1"


def test_oxford_pets_captions_gpu(
    oxford_pets_table: tuple,
    gpu_cluster: str,
    batch_size: int,
    skip_gpu: bool,
) -> None:
    """
    Test GPU-accelerated caption generation using BLIP.

    This test generates image captions and validates that
    they are non-empty strings.

    Note: Uses the shared oxford_pets_table and adds caption column to it.
    """
    if skip_gpu:
        pytest.skip("GPU tests skipped (--skip-gpu)")

    conn, tbl, _ = oxford_pets_table
    num_images = len(tbl)

    _LOG.info(f"Using shared table with {num_images} rows for caption test")

    # Column name (using default from columns.py)
    caption_col = "caption"

    # Use conn.context() with cluster and manifest
    # Column already added by upload_manifests.py
    with conn.context(cluster=gpu_cluster, manifest=MANIFEST_NAME):
        _LOG.info(f"Backfilling {caption_col}")
        tbl.backfill(
            caption_col,
            batch_size=batch_size,
            commit_granularity=2,
        )

    # Validate results
    tbl.checkout_latest()
    df = tbl.to_pandas()

    _LOG.info(f"Completed backfill for {len(df)} rows")

    # Assertions
    assert caption_col in df.columns, f"{caption_col} column not found"
    assert df[caption_col].notna().all(), "All rows should have captions"
    assert len(df) == num_images, f"Expected {num_images} rows"

    # Check that captions are non-empty strings
    filled_captions = df[caption_col]
    for caption in filled_captions:
        assert isinstance(caption, str), (
            f"Caption should be string, got {type(caption)}"
        )
        assert len(caption) > 0, "Caption should be non-empty"

    _LOG.info("Caption test passed!")
    _LOG.info(f"Sample captions: {filled_captions.head(3).tolist()}")
