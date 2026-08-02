# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Basic sanity checks for the document embedding table setup.
"""

import logging

_LOG = logging.getLogger(__name__)

EXPECTED_COLUMNS = [
    "file_name",
    "uploaded_pdf_path",
    "pdf_bytes",
    "pages",
    "chunks",
    "chunk_embeddings",
]


def test_document_table_schema(document_table, num_docs):
    conn, tbl, table_name = document_table

    _LOG.info("Testing table %s with schema %s", table_name, tbl.schema.names)

    for col in EXPECTED_COLUMNS:
        assert col in tbl.schema.names, f"Missing expected column {col}"

    assert len(tbl) > 0, "Table should contain rows"
    assert len(tbl) <= num_docs, "Table should not exceed requested sample size"

    sample = tbl.to_pandas().head()
    _LOG.info("Sample rows:\n%s", sample)
