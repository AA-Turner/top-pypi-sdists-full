# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Test sentence transformer embeddings on image_id text.

This test generates embeddings from the image_id field (e.g., "Abyssinian_1.jpg").
It demonstrates text embedding generation from existing string fields.
"""

import pytest
import logging

_LOG = logging.getLogger(__name__)

# Well-known manifest name (uploaded via upload_manifests.py)
MANIFEST_NAME = "sentence-transformers-udfs-v1"

pytestmark = pytest.mark.order(-1) # happen after all others

def test_image_id_embeddings(
    oxford_pets_table: tuple,
    standard_cluster: str,  # CPU cluster is fine for sentence transformers
    batch_size: int,
) -> None:
    """
    Test embedding generation from image_id text using sentence transformers.

    This test generates embeddings from the image_id field (e.g., "Abyssinian_1.jpg").
    It demonstrates text embedding on existing string columns.

    Note: Uses the shared oxford_pets_table with the image_id_embedding column.
    """
    conn, tbl, _ = oxford_pets_table
    num_images = len(tbl)

    _LOG.info(f"Using shared table with {num_images} rows for embedding test")

    embedding_col = "image_id_embedding"

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
    arrow_table = tbl.to_arrow()

    _LOG.info(f"Completed backfill for {len(arrow_table)} rows")

    # Assertions
    embeddings = arrow_table.column(embedding_col)
    assert embeddings.length() == num_images

    # Check first non-null embedding
    first_vector = embeddings[0].as_py()
    assert isinstance(first_vector, list), (
        f"Embedding should be a list, got {type(first_vector)}"
    )
    assert all(isinstance(value, float) for value in first_vector), (
        "All embedding values should be floats"
    )

    # all-MiniLM-L6-v2 produces 384-dimensional embeddings
    assert len(first_vector) == 384, (
        f"Expected 384-dimensional embeddings, got {len(first_vector)}"
    )

    # Verify all embeddings have correct dimension
    for i, vec in enumerate(embeddings):
        vec_py = vec.as_py()
        if vec_py is not None:
            assert len(vec_py) == 384, (
                f"Row {i}: Expected 384 dimensions, got {len(vec_py)}"
            )

    _LOG.info("Embedding test passed!")
    _LOG.info(f"Sample embedding (first 5 dims): {first_vector[:5]}")
