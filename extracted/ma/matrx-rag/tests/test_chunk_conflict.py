"""B.0 — concurrent re-ingest must never raise 23505.

Regression guard for FOUND_DEFECTS 2026-06-02 / matrx-feedback 695983de:
the unique index ``kg_chunks_content_sha_idx`` on
``(source_kind, source_id, content_sha256, chunker_version)`` raised a
duplicate-key error (23505) when two re-ingest runs for the same source
+ same content interleaved. The fix is a transaction-scoped advisory
lock keyed on the source PLUS ``INSERT ... ON CONFLICT DO NOTHING``, so
the class of failure is structurally gone — the second run either waits
for the first (lock) or silently no-ops the duplicate insert (conflict).

This test fires two concurrent ``upsert_chunks`` calls for the SAME source
and SAME content and asserts:

  * neither call raises,
  * exactly one chunk row survives per distinct ``content_sha256``,
  * no embedding orphan (every embedding points at a surviving chunk).

It reuses the in-memory fake pool from ``test_chunk_reuse`` — the fake
enforces the unique constraint with DO-NOTHING semantics, mirroring the
real index, so the no-exception + one-row guarantee is exercised without
a live DB.
"""

from __future__ import annotations

import asyncio
import hashlib
from typing import Any

import pytest

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


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@pytest.fixture
def shared_db(monkeypatch):
    db = _FakeKgChunksDb()
    _wire_fake_db(monkeypatch, db)
    return db


@pytest.fixture
def stub_embedding_spec(monkeypatch):
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class _Spec:
        name: str = "openai:text-embedding-3-small"
        dim: int = 4
        table: str = "rag.embeddings_oai_3_small_1536"
        batch_size: int = 96

    import matrx_rag.ingestion as ingestion_mod

    monkeypatch.setattr(ingestion_mod, "spec_for", lambda model: _Spec())


@pytest.mark.asyncio
async def test_concurrent_reingest_same_content_no_conflict(
    shared_db, stub_embedding_spec
):
    """Two simultaneous first-ingests for the same source + identical
    content. The unique constraint is enforced; the second run's inserts
    conflict-skip rather than raise. Exactly one row per content_sha256."""
    from matrx_rag.ingestion import upsert_chunks

    def _build_call():
        # Each "run" sees an empty existing_by_sha (it queried before the
        # other committed — the classic interleave). Identical content,
        # distinct chunk_ids (each run minted its own UUIDs).
        chunks = [_make_chunk(f"shared paragraph {i}", i) for i in range(5)]
        shas = [_sha(c.content_text) for c in chunks]
        embeddings = [[0.1, 0.2, 0.3, 0.4]] * 5
        return chunks, shas, embeddings

    chunks_a, shas_a, emb_a = _build_call()
    chunks_b, shas_b, emb_b = _build_call()
    resolved = _make_resolved(source_id="race-src")

    # Both runs observed an empty DB before either committed.
    results = await asyncio.gather(
        upsert_chunks(
            resolved=resolved,
            chunks=chunks_a,
            embedding_model="openai:text-embedding-3-small",
            embeddings=emb_a,
            new_shas=shas_a,
            existing_by_sha={},
        ),
        upsert_chunks(
            resolved=resolved,
            chunks=chunks_b,
            embedding_model="openai:text-embedding-3-small",
            embeddings=emb_b,
            new_shas=shas_b,
            existing_by_sha={},
        ),
        return_exceptions=True,
    )

    # No call raised.
    for r in results:
        assert not isinstance(r, Exception), f"upsert_chunks raised: {r!r}"

    # Exactly one row per distinct content_sha256.
    shas_in_db = [row["content_sha256"] for row in shared_db.chunks.values()]
    assert len(shas_in_db) == len(set(shas_in_db)), (
        f"duplicate content_sha256 rows survived: {shas_in_db}"
    )
    assert set(shas_in_db) == set(shas_a) == set(shas_b)
    assert len(shared_db.chunks) == 5

    # The combined inserted count across both runs equals the rows that
    # actually landed — conflicts were skipped, not double-counted.
    total_inserted = sum(r["chunks_inserted"] for r in results)
    assert total_inserted == 5

    # No embedding orphans — every embedding points at a surviving chunk.
    for chunk_id in shared_db.embeddings:
        assert chunk_id in shared_db.chunks, (
            f"orphan embedding for missing chunk {chunk_id}"
        )


@pytest.mark.asyncio
async def test_second_run_after_first_committed_reuses_not_duplicates(
    shared_db, stub_embedding_spec
):
    """Sequential re-ingest: first run lands 3 rows; the second run sees
    them via existing_by_sha and reuses — zero new inserts, zero
    conflicts, zero duplicates."""
    from matrx_rag.ingestion import upsert_chunks

    chunks = [_make_chunk(f"doc line {i}", i) for i in range(3)]
    shas = [_sha(c.content_text) for c in chunks]
    resolved = _make_resolved(source_id="seq-src")

    await upsert_chunks(
        resolved=resolved,
        chunks=chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=[[0.0, 0.0, 0.0, 0.0]] * 3,
        new_shas=shas,
        existing_by_sha={},
    )
    assert len(shared_db.chunks) == 3

    existing_by_sha = {
        row["content_sha256"]: row["id"] for row in shared_db.chunks.values()
    }
    second_chunks = [_make_chunk(f"doc line {i}", i) for i in range(3)]
    second_shas = [_sha(c.content_text) for c in second_chunks]

    result = await upsert_chunks(
        resolved=resolved,
        chunks=second_chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=[None, None, None],
        new_shas=second_shas,
        existing_by_sha=existing_by_sha,
    )

    assert result["chunks_inserted"] == 0
    assert result["chunks_reused"] == 3
    assert len(shared_db.chunks) == 3
