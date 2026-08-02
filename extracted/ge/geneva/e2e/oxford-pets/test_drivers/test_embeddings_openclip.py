# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Test OpenCLIP embedding generation.

This test uses the OpenCLIP model to generate 512-dimensional embeddings.
"""

import logging

import pytest

_LOG = logging.getLogger(__name__)

# Well-known manifest name (uploaded via upload_manifests.py)
MANIFEST_NAME = "openclip-udfs-v1"


def test_oxford_pets_embeddings(
    oxford_pets_table: tuple,
    standard_cluster: str,
    batch_size: int,
    skip_gpu: bool,
) -> None:
    """
    Test vector embedding generation using OpenCLIP.

    This test generates 512-dimensional embeddings and validates
    the output shape and values.

    Note: Uses the shared oxford_pets_table and adds embedding column to it.
    """
    if skip_gpu:
        pytest.skip("GPU tests skipped (--skip-gpu)")

    conn, tbl, _ = oxford_pets_table
    num_images = len(tbl)

    _LOG.info(f"Using shared table with {num_images} rows for embedding test")

    # Column name (using default from columns.py)
    embedding_col = "embedding"

    # Use conn.context() with cluster and manifest
    # Column already added by upload_manifests.py
    with conn.context(cluster=standard_cluster, manifest=MANIFEST_NAME):
        _LOG.info(f"Backfilling {embedding_col}")
        tbl.backfill(
            embedding_col,
            batch_size=batch_size,
            commit_granularity=2,
        )

    # Validate results
    tbl.checkout_latest()
    df = tbl.to_pandas()

    _LOG.info(f"Completed backfill for {len(df)} rows")

    # Assertions
    assert embedding_col in df.columns, f"{embedding_col} column not found"
    assert df[embedding_col].notna().all(), "All rows should have embeddings"
    assert len(df) == num_images, f"Expected {num_images} rows"

    # Check embedding dimensions
    first_embedding = df.loc[0, embedding_col]
    assert len(first_embedding) == 512, (
        f"Expected 512-dim embedding, got {len(first_embedding)}"
    )

    _LOG.info("Embedding test passed!")
