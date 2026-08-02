# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Test video embeddings UDF for OpenVid videos.
"""

import logging

import pytest

_LOG = logging.getLogger(__name__)

TARGET_COL = "video_embedding_vjepa2"

def test_video_embedding_column_added(openvid_table):
    """Test that video_embedding column was added to the table."""
    conn, tbl, table_name = openvid_table

    # Verify video_embedding_vjpea2 column exists
    assert TARGET_COL in tbl.schema.names, (
        f"Expected '{TARGET_COL}' column in schema, got: {tbl.schema.names}"
    )

    _LOG.info(f"✓ {TARGET_COL} column exists in table schema")


def test_video_embedding_backfill(
    openvid_table,
    ray_254_gpu_cluster,
    batch_size,
    skip_gpu,
):
    """Test backfilling video_embedding_vjepa2 column with CLIP embeddings."""
    if skip_gpu:
        pytest.skip("Skipping GPU test (--skip-gpu flag set)")

    conn, tbl, table_name = openvid_table
    cluster_name = "e2e-openvid-ray-254-gpu-cluster"

    # Use small checkpoint size for GPU processing
    gpu_checkpoint_size = min(batch_size, 5)  # Limit to 5 for GPU memory
    _LOG.info(
        f"Starting {TARGET_COL} backfill with GPU (checkpoint_size={gpu_checkpoint_size})"
    )

    # Run backfill with GPU cluster and manifest
    with conn.context(cluster=cluster_name, manifest="video-embeddings-v1"):
        result = tbl.backfill(
            TARGET_COL,
            checkpoint_size=gpu_checkpoint_size,
        )

    _LOG.info(f"Backfill completed: {result}")

    # Verify results
    df = tbl.to_pandas()
    assert len(df) > 0, "Table should have data"
    assert TARGET_COL in df.columns, f"{TARGET_COL} column should exist"

    # Check embedding dimensions (2D tensor)
    non_null_embeddings = df[TARGET_COL].dropna()
    if len(non_null_embeddings) > 0:
        first_embedding = non_null_embeddings.iloc[0]
        _LOG.info(
            f"Embedding tensor shape: "
            f"[{len(first_embedding)}, {len(first_embedding[0])}]"
        )

        # Verify 2D structure (accepts both lists and numpy arrays)
        import numpy as np

        # Convert to numpy for uniform handling
        if not isinstance(first_embedding, np.ndarray):
            first_embedding = np.array(first_embedding)

        assert len(first_embedding) > 0, "Should have at least one token"
        assert len(first_embedding[0]) == 1024, (
            f"Each embedding should be 1024-dim for V-JEPA2 ViT-L, "
            f"got {len(first_embedding[0])}"
        )

        # Log some statistics
        _LOG.info(f"Embeddings generated: {len(non_null_embeddings)}/{len(df)}")
        _LOG.info(f"Tokens per video: ~{len(first_embedding)}")

    _LOG.info(f"✓ {TARGET_COL} backfill completed successfully")


@pytest.mark.skip(reason="Will vet this later")
def test_video_similarity_search(
    openvid_table,
    ray_254_gpu_cluster,
    skip_gpu,
):
    """Test similarity search using video embeddings with mean pooling."""
    if skip_gpu:
        pytest.skip("Skipping GPU test (--skip-gpu flag set)")

    import numpy as np

    conn, tbl, table_name = openvid_table

    # Check if embeddings are populated
    df = tbl.to_pandas()
    if TARGET_COL not in df.columns or df[TARGET_COL].isna().all():
        pytest.skip(f"{TARGET_COL} column not populated - run test_video_embedding_backfill first")

    # Get first non-null embedding as query
    non_null = df[df[TARGET_COL].notna()]
    if len(non_null) == 0:
        pytest.skip("No video embeddings found")

    # Aggregate 2D tensor to 1D for search (mean pooling)
    query_tensor = np.array(non_null[TARGET_COL].iloc[0])  # Shape: [num_tokens, 1024]
    query_embedding = query_tensor.mean(axis=0)  # Shape: [1024]
    query_embedding = query_embedding / np.linalg.norm(query_embedding)  # L2 normalize

    _LOG.info(f"Using embedding from: {non_null['video'].iloc[0] if 'video' in non_null.columns else 'unknown'}")
    _LOG.info(f"Query tensor shape: {query_tensor.shape}, aggregated to: {query_embedding.shape}")

    # Perform similarity search with aggregated embedding
    results = tbl.search(query_embedding.tolist()).limit(5).to_pandas()

    _LOG.info(f"Found {len(results)} similar videos")
    if len(results) > 0 and "video" in results.columns:
        _LOG.info("\nTop 5 similar videos (mean-pooled search):")
        for idx, row in results.iterrows():
            video = row.get("video", "unknown")
            caption = row.get("caption", "N/A")
            _LOG.info(f"  {idx+1}. {video}: {caption[:80]}...")

    assert len(results) > 0, "Should find at least one similar video"
    _LOG.info(f"✓ Similarity search completed successfully")
