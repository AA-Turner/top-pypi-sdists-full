# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
End-to-end pipeline test for Whisper transcription + embeddings.

Validates chunk-level output table created by the pipeline.
"""

import logging

import pytest

_LOG = logging.getLogger(__name__)

EMBEDDING_DIM = 1024


def test_whisper_transcription_pipeline(
    chunk_table,
) -> None:
    conn, tbl, table_name = chunk_table

    _LOG.info(
        "Validating Whisper chunk table %s (rows=%s)",
        table_name,
        len(tbl),
    )

    df = tbl.to_pandas()
    assert len(df) > 0, "Table should have data after pipeline"

    # With 5-second chunks on LibriSpeech clips (5-15s each), the UDTF
    # should produce more chunk rows than source rows (1:N expansion).
    _LOG.info("Chunk table has %d rows (source had 256 rows)", len(df))
    assert len(df) > 256, (
        f"Expected 1:N expansion to produce more than 256 chunk rows, got {len(df)}"
    )

    # Validate chunk metadata + embeddings
    assert df["clip_id"].notna().any(), "Expected clip_id values"
    assert df["source"].notna().any(), "Expected source values"
    assert df["text"].notna().any(), "Expected transcript text"

    non_null_embeddings = df["embedding"].dropna()
    if len(non_null_embeddings) == 0:
        pytest.fail("No embeddings produced; check embedding UDF")

    first_vector = non_null_embeddings.iloc[0]
    assert len(first_vector) == EMBEDDING_DIM, (
        f"Expected embedding dim {EMBEDDING_DIM}, got {len(first_vector)}"
    )

    # Only build an IVF_PQ index when there are enough vectors to
    # meaningfully populate the default 256 KMeans clusters; otherwise
    # brute-force search is fine and avoids noisy empty-cluster warnings.
    if len(non_null_embeddings) >= 256 * 10:
        tbl.create_index(
            metric="cosine",
            vector_column_name="embedding",
            num_sub_vectors=64,
        )

    query_vec = first_vector
    results = tbl.search(query_vec, vector_column_name="embedding").limit(5).to_list()
    assert results, "Expected cosine similarity search results"

    _LOG.info("✓ Whisper transcription pipeline completed successfully")
