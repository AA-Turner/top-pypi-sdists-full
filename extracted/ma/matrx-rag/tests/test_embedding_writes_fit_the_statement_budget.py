"""Embedding writes fit inside the database's statement budget (2026-11-16).

Three 200-row INSERTs into rag.embeddings_voyage_4_large_1024 ran past the pool's
10 s command_timeout (IO/DataFileRead, no blocker: every row is an HNSW insert reading
index pages from disk) and dead-lettered a kept Source. Each write is now a small
statement that the driver lets run to the server's own ceiling.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_orm import SERVER_CEILING

from matrx_rag import ingestion


async def test_default_embedding_write_is_small_and_waits_for_the_server_ceiling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[int, Any]] = []

    class _Emb:
        @classmethod
        async def bulk_insert_ignore(cls, rows: list[dict[str, Any]], **kw: Any) -> None:
            calls.append((len(rows), kw.get("statement_timeout")))

    monkeypatch.setattr(ingestion, "orm_model_name_for_table", lambda _t: "Emb")
    monkeypatch.setattr(ingestion, "get_db_model", lambda _name: _Emb)
    payloads = [(f"c-{i:04d}", "o", "u", "[1]") for i in range(200)]
    written = await ingestion._write_embedding_rows("embeddings_x", payloads)

    assert written == 200
    assert len(calls) > 1, "200 vectors must never ride one statement"
    assert all(n <= 50 for n, _ in calls)
    assert all(t is SERVER_CEILING for _, t in calls)
