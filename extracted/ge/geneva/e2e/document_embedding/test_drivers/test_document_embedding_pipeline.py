# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
End-to-end pipeline test for document embeddings.

Runs all backfills in sequence:
1. pdf_bytes (download PDF)
2. pages (extract text)
3. chunks (split text)
4. chunk_embeddings (SentenceTransformer embeddings)
"""

import logging

import pytest

_LOG = logging.getLogger(__name__)

DERIVED_COLUMNS = ["pdf_bytes", "pages", "chunks", "chunk_embeddings"]
EMBEDDING_DIM = 384


def _run_pipeline(tbl, conn, cluster_name: str, manifest_name: str, batch_size: int) -> None:
    with conn.context(cluster=cluster_name, manifest=manifest_name):
        for col in DERIVED_COLUMNS:
            _LOG.info("Backfilling column %s", col)
            tbl.backfill(col, batch_size=batch_size)


def test_document_embedding_pipeline(
    document_table,
    standard_cluster,
    batch_size,
    manifest_name,
) -> None:
    conn, tbl, table_name = document_table

    _LOG.info(
        "Starting document embedding pipeline on table %s (rows=%s)",
        table_name,
        len(tbl),
    )

    _run_pipeline(tbl, conn, standard_cluster, manifest_name, batch_size)

    df = tbl.to_pandas()
    assert len(df) > 0, "Table should have data after pipeline"

    # Validate intermediate columns
    assert df["pdf_bytes"].notna().any(), "Expected downloaded PDF bytes"
    assert df["pages"].notna().any(), "Expected page text extraction"
    assert df["chunks"].notna().any(), "Expected text chunks"

    # Validate embeddings
    non_null_embeddings = df["chunk_embeddings"].dropna()
    if len(non_null_embeddings) == 0:
        pytest.fail("No embeddings produced; check UDF and data availability")

    first_embedding = non_null_embeddings.iloc[0]
    assert len(first_embedding) > 0, "Embedding list should have at least one chunk"
    first_vector = first_embedding[0]
    assert len(first_vector) == EMBEDDING_DIM, (
        f"Expected embedding dim {EMBEDDING_DIM}, got {len(first_vector)}"
    )

    _LOG.info("✓ Document embedding pipeline completed successfully")
