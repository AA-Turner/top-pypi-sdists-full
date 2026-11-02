"""A newer save replacing chunks before this run's embeddings land is not a failed run (audit
2026-09-26: 54 note ingest runs recorded as errors — embedding FK violation, chunk not present)."""

from __future__ import annotations

from typing import Any

import pytest

from matrx_rag import ingestion
from matrx_orm.exceptions import IntegrityError


def _chunk_fk_violation() -> Exception:
    """What the driver raises: SQLSTATE 23503 naming the chunk_id foreign key."""
    import asyncpg

    err = asyncpg.exceptions.ForeignKeyViolationError("any words")
    err.constraint_name = "kg_embeddings_chunk_id_fkey"
    return err


async def test_embeddings_of_chunks_a_newer_save_replaced_are_dropped_not_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    writes: list[list[str]] = []

    class _Emb:
        @classmethod
        async def bulk_insert_ignore(cls, rows: list[dict[str, Any]], **_: Any) -> None:
            ids = [r["chunk_id"] for r in rows]
            if "gone" in ids:
                raise IntegrityError(constraint="foreign_key", original_error=_chunk_fk_violation())
            writes.append(ids)

    class _Q:
        async def values(self, *_: str) -> list[dict[str, Any]]:
            return [{"id": "live"}]

    class _Chunks:
        @classmethod
        def filter(cls, **_: Any) -> _Q:
            return _Q()

    monkeypatch.setattr(ingestion, "orm_model_name_for_table", lambda _t: "Emb")
    monkeypatch.setattr(ingestion, "get_db_model", lambda name: _Chunks if name == "KgChunks" else _Emb)
    written = await ingestion._write_embedding_rows(
        "embeddings_x", [("live", "o", "u", "[1]"), ("gone", "o", "u", "[2]")]
    )
    assert written == 1 and writes == [["live"]]
