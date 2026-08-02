# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Basic sanity checks for the Whisper transcription table setup.
"""

import logging

_LOG = logging.getLogger(__name__)

EXPECTED_COLUMNS = [
    "clip_id",
    "source",
    "chunk_id",
    "start_sec",
    "end_sec",
    "samples",
    "text",
    "embedding",
]


def test_audio_table_schema(chunk_table, row_limit):
    conn, tbl, table_name = chunk_table

    _LOG.info("Testing table %s with schema %s", table_name, tbl.schema.names)

    for col in EXPECTED_COLUMNS:
        assert col in tbl.schema.names, f"Missing expected column {col}"

    assert len(tbl) > 0, "Table should contain rows"

    sample = tbl.to_pandas().head()
    _LOG.info("Sample rows:\n%s", sample)
