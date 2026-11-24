"""Every embedding writer sends its rows in ascending chunk_id (2026-11-04).

Two writers embedding overlapping chunks each sent a multi-row ``INSERT … ON
CONFLICT`` in their own order and Postgres broke the cycle with 40P01 on
rag.embeddings_voyage_4_large_1024 after five retries. One shared lock order
makes that cycle impossible.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_rag import ingestion


async def test_write_embedding_rows_sends_every_batch_in_ascending_chunk_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sent: list[list[str]] = []

    class _Emb:
        @classmethod
        async def bulk_insert_ignore(cls, rows: list[dict[str, Any]], **_: Any) -> None:
            sent.append([r["chunk_id"] for r in rows])

    monkeypatch.setattr(ingestion, "orm_model_name_for_table", lambda _t: "Emb")
    monkeypatch.setattr(ingestion, "get_db_model", lambda _name: _Emb)
    ids = ["c-9", "c-1", "c-7", "c-3", "c-5"]
    written = await ingestion._write_embedding_rows(
        "embeddings_x", [(i, "o", "u", "[1]") for i in ids], batch_size=2
    )
    assert written == 5
    flat = [i for batch in sent for i in batch]
    assert flat == sorted(ids)
    assert all(batch == sorted(batch) for batch in sent)
