"""A large source's chunk INSERT is split into bounded statements.

Live 2026-11-02..13 (ops.system_error 57014 on rag.kg_chunks, auto_ingest): a
1,400-page note was written as ONE multi-row ``INSERT INTO rag.kg_chunks``.
Every row runs five row triggers and feeds two GIN indexes over its text, so
the statement ran past the 10 s statement timeout and the note never became
searchable. Every kg_chunks writer now sends its rows through
``chunk_row_write_batches``: at most ``CHUNK_WRITE_BATCH_ROWS`` rows and
``CHUNK_WRITE_BATCH_BYTES`` of text per statement, parents before children.
"""

from __future__ import annotations

import hashlib
import uuid

import pytest

from matrx_rag.chunking import (
    CHUNK_WRITE_BATCH_BYTES,
    CHUNK_WRITE_BATCH_ROWS,
    chunk_row_write_batches,
)

try:
    from test_chunk_reuse import (  # type: ignore[import-not-found]
        _FakeKgChunksDb,
        _make_chunk,
        _make_resolved,
        _wire_fake_db,
    )
except ImportError:  # pragma: no cover - import-path resilience
    from tests.test_chunk_reuse import (  # type: ignore[import-not-found]
        _FakeKgChunksDb,
        _make_chunk,
        _make_resolved,
        _wire_fake_db,
    )


@pytest.fixture
def db(monkeypatch):
    fake = _FakeKgChunksDb()
    _wire_fake_db(monkeypatch, fake)

    from dataclasses import dataclass

    @dataclass(frozen=True)
    class _Spec:
        name: str = "openai:text-embedding-3-small"
        dim: int = 4
        table: str = "rag.embeddings_oai_3_small_1536"
        batch_size: int = 96

    import matrx_rag.ingestion as ingestion_mod

    monkeypatch.setattr(ingestion_mod, "spec_for", lambda model: _Spec())
    return fake


@pytest.mark.asyncio
async def test_a_large_note_lands_in_bounded_insert_statements(db) -> None:
    from matrx_rag.ingestion import upsert_chunks

    # ~1.2 MB of text over 400 chunks — the shape of the live note.
    chunks = [_make_chunk(f"section {i} " + ("x" * 3000), i) for i in range(400)]
    shas = [hashlib.sha256(c.content_text.encode()).hexdigest() for c in chunks]

    result = await upsert_chunks(
        resolved=_make_resolved(source_id="big-note"),
        chunks=chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=[[0.1, 0.2, 0.3, 0.4]] * len(chunks),
        new_shas=shas,
        existing_by_sha={},
    )

    assert result["chunks_inserted"] == 400
    assert len(db.chunks) == 400
    assert len(db.insert_log) > 1, "one INSERT carried the whole note"
    for landed in db.insert_log:
        assert len(landed) <= CHUNK_WRITE_BATCH_ROWS
        text_bytes = sum(len(db.chunks[cid]["content_text"].encode()) for cid in landed)
        assert text_bytes <= CHUNK_WRITE_BATCH_BYTES


def test_parents_land_no_later_than_their_children() -> None:
    parent = {"id": str(uuid.uuid4()), "parent_chunk_id": None, "content_text": "p" * 10}
    children = [
        {"id": str(uuid.uuid4()), "parent_chunk_id": parent["id"], "content_text": "c"}
        for _ in range(5)
    ]
    grandchild = {
        "id": str(uuid.uuid4()),
        "parent_chunk_id": children[0]["id"],
        "content_text": "g",
    }
    outside = {"id": str(uuid.uuid4()), "parent_chunk_id": str(uuid.uuid4()), "content_text": "o"}
    # Children first, the way a careless caller might send them.
    rows = [grandchild, *children, outside, parent]

    batches = chunk_row_write_batches(rows, max_rows=2)
    position = {r["id"]: i for i, batch in enumerate(batches) for r in batch}

    assert sorted(position) == sorted(r["id"] for r in rows)
    for row in rows:
        p = row["parent_chunk_id"]
        if p in position:
            assert position[p] <= position[row["id"]]
    assert all(len(b) <= 2 for b in batches)


def test_one_oversized_row_gets_its_own_batch() -> None:
    rows = [
        {"id": "a", "parent_chunk_id": None, "content_text": "a" * 10},
        {"id": "b", "parent_chunk_id": None, "content_text": "b" * 500},
        {"id": "c", "parent_chunk_id": None, "content_text": "c" * 10},
    ]
    batches = chunk_row_write_batches(rows, max_bytes=100)
    assert [[r["id"] for r in b] for b in batches] == [["a"], ["b"], ["c"]]
