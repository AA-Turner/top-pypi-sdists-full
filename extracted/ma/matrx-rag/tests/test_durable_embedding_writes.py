"""Durable embedding persistence (2026-06-10 redesign).

The contract under test:

* ``upsert_chunks(embeddings=None)`` (deferred mode) commits chunk rows and
  writes NO embedding rows — the caller persists-as-it-embeds afterward.
* Legacy mode (vectors supplied) writes embeddings AFTER the chunk
  transaction, in idempotent sub-batches of ``EMBED_WRITE_BATCH_SIZE`` —
  never one giant statement, never a custom command_timeout.
* ``_embed_and_persist_batched`` interleaves: one provider batch → one
  committed write, so a crash loses at most one batch of paid work.
* ``_unembedded_chunk_ids`` (the self-heal probe) finds chunk rows whose
  embedding row is missing, so a crash between the chunk commit and the
  embedding writes is repaired by the next ingest instead of leaving the
  chunk invisible to vector recall forever.

Uses the in-memory fakes from test_chunk_reuse. No live DB, no network.
"""

from __future__ import annotations

import hashlib
import uuid
from typing import Any

import pytest

try:
    from test_chunk_reuse import (  # type: ignore[import-not-found]
        _make_chunk,
        fake_db_pool,
        stub_embedding_spec,
    )
except ImportError:  # pragma: no cover - import-path resilience
    from tests.test_chunk_reuse import (  # type: ignore[import-not-found]
        _make_chunk,
        fake_db_pool,
        stub_embedding_spec,
    )


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _vec(i: int) -> list[float]:
    return [float(i), 0.0, 0.0, 1.0]


# ---------------------------------------------------------------------------
# Deferred mode
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_deferred_mode_writes_chunks_but_no_embeddings(fake_db_pool, stub_embedding_spec):
    from matrx_rag.ingestion import upsert_chunks

    chunks = [_make_chunk(f"deferred chunk {i}", i) for i in range(4)]
    new_shas = [_sha(c.content_text) for c in chunks]

    from matrx_rag.sources import ResolvedSource

    resolved = ResolvedSource(
        source_kind="note",
        source_id="n-defer",
        field_id=None,
        organization_id=str(uuid.uuid4()),
        owner_id=str(uuid.uuid4()),
        text="x",
        mime_type="text/plain",
        language=None,
        source_hash="h1",
        metadata={},
    )

    result = await upsert_chunks(
        resolved=resolved,
        chunks=chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=None,  # deferred
        new_shas=new_shas,
        existing_by_sha={},
    )

    assert len(fake_db_pool.chunks) == 4
    assert fake_db_pool.embeddings == {}  # nothing written
    assert sorted(result["inserted_chunk_ids"]) == sorted(c.chunk_id for c in chunks)


@pytest.mark.asyncio
async def test_deferred_mode_skips_vector_validation(fake_db_pool, stub_embedding_spec):
    """embeddings=None must not trip the 'inserted chunk needs a vector' check."""
    from matrx_rag.ingestion import upsert_chunks
    from matrx_rag.sources import ResolvedSource

    chunks = [_make_chunk("only one", 0)]
    resolved = ResolvedSource(
        source_kind="note",
        source_id="n-defer2",
        field_id=None,
        organization_id=str(uuid.uuid4()),
        owner_id=str(uuid.uuid4()),
        text="x",
        mime_type="text/plain",
        language=None,
        source_hash="h1",
        metadata={},
    )
    result = await upsert_chunks(
        resolved=resolved,
        chunks=chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=None,
        new_shas=[_sha(chunks[0].content_text)],
        existing_by_sha={},
    )
    assert result["chunks_inserted"] == 1


# ---------------------------------------------------------------------------
# Batched writer
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_write_embedding_rows_batches(fake_db_pool):
    """450 payloads with batch_size=200 → exactly 3 bulk_insert_ignore calls
    (200/200/50) — one per idempotent sub-batch, via the fake
    EmbeddingsOai3Small1536 model's bulk_insert_ignore (fake_db_pool wires
    matrx_rag.ingestion.get_db_model to it)."""
    from matrx_rag.ingestion import _write_embedding_rows

    payloads = [(str(uuid.uuid4()), None, str(uuid.uuid4()), "[1,2,3,4]") for _ in range(450)]
    written = await _write_embedding_rows(
        "rag.embeddings_oai_3_small_1536", payloads, batch_size=200
    )
    assert written == 450
    assert fake_db_pool.embedding_insert_log == [200, 200, 50]
    assert len(fake_db_pool.embeddings) == 450


@pytest.mark.asyncio
async def test_legacy_mode_writes_embeddings_in_batches(
    fake_db_pool, stub_embedding_spec, monkeypatch
):
    """Legacy callers (vectors supplied) get post-commit batched writes."""
    import matrx_rag.ingestion as ingestion_mod
    from matrx_rag.ingestion import upsert_chunks
    from matrx_rag.sources import ResolvedSource

    # Shrink the batch size so 5 chunks → 3 statements (2/2/1).
    monkeypatch.setattr(ingestion_mod, "EMBED_WRITE_BATCH_SIZE", 2)

    chunks = [_make_chunk(f"legacy chunk {i}", i) for i in range(5)]
    resolved = ResolvedSource(
        source_kind="note",
        source_id="n-legacy",
        field_id=None,
        organization_id=str(uuid.uuid4()),
        owner_id=str(uuid.uuid4()),
        text="x",
        mime_type="text/plain",
        language=None,
        source_hash="h1",
        metadata={},
    )
    result = await upsert_chunks(
        resolved=resolved,
        chunks=chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=[_vec(i) for i in range(5)],
        new_shas=[_sha(c.content_text) for c in chunks],
        existing_by_sha={},
    )
    assert result["chunks_inserted"] == 5
    assert len(fake_db_pool.embeddings) == 5  # every vector landed
    # Batched post-commit writes: 5 rows with batch_size=2 → 3 statements.
    assert fake_db_pool.embedding_insert_log == [2, 2, 1]


# ---------------------------------------------------------------------------
# Persist-as-you-embed
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_embed_and_persist_interleaves(fake_db_pool, monkeypatch):
    """One provider batch → one committed write, in order; a provider failure
    on batch N leaves batches 1..N-1 durably written."""
    import matrx_rag.ingestion as ingestion_mod

    events: list[str] = []

    class _Spec:
        name = "stub"
        dim = 4
        table = "rag.embeddings_oai_3_small_1536"
        batch_size = 2

    monkeypatch.setattr(ingestion_mod, "spec_for", lambda model: _Spec())

    calls = {"n": 0}

    async def _fake_embed(model, texts, **kwargs):
        calls["n"] += 1
        events.append(f"embed:{len(texts)}")
        if calls["n"] == 3:
            raise RuntimeError("provider down")
        return [_vec(i) for i in range(len(texts))]

    monkeypatch.setattr(ingestion_mod, "embed", _fake_embed)

    # Wrap the real _write_embedding_rows (already routed to the fake
    # embedding model by the fake_db_pool fixture) to record a "write" event
    # per call — one call per provider batch, per _embed_and_persist_batched.
    real_write_embedding_rows = ingestion_mod._write_embedding_rows

    async def _tracking_write_embedding_rows(*args, **kwargs):
        events.append("write")
        return await real_write_embedding_rows(*args, **kwargs)

    monkeypatch.setattr(ingestion_mod, "_write_embedding_rows", _tracking_write_embedding_rows)

    items = [(str(uuid.uuid4()), f"text {i}") for i in range(6)]
    with pytest.raises(RuntimeError, match="provider down"):
        await ingestion_mod._embed_and_persist_batched(
            embedding_model="stub",
            organization_id=None,
            owner_id=str(uuid.uuid4()),
            items=items,
        )

    # Two full embed→write cycles committed before the third embed failed.
    assert events == ["embed:2", "write", "embed:2", "write", "embed:2"]
    assert len(fake_db_pool.embeddings) == 4  # paid work persisted, not rolled back


# ---------------------------------------------------------------------------
# Self-heal probe
# ---------------------------------------------------------------------------


@pytest.fixture
def fake_embedding_model():
    """Inject a fake EmbeddingsOai3Small1536 model via the db_models override."""
    from matrx_rag import _ext

    class _FakeEmbModel:
        rows: list[dict[str, Any]] = []

        class _QB:
            def __init__(self, ids):
                self._ids = set(ids)

            async def values(self, *fields):
                return [
                    {"chunk_id": r["chunk_id"]}
                    for r in _FakeEmbModel.rows
                    if r["chunk_id"] in self._ids
                ]

        @classmethod
        def filter(cls, **kwargs):
            return cls._QB(kwargs.get("chunk_id__in") or [])

    _ext._reset_for_tests()
    _ext.configure(db_models={"EmbeddingsOai3Small1536": _FakeEmbModel})
    yield _FakeEmbModel
    _ext._reset_for_tests()


@pytest.mark.asyncio
async def test_unembedded_chunk_ids_finds_the_gap(fake_embedding_model):
    from matrx_rag.ingestion import _unembedded_chunk_ids

    have = str(uuid.uuid4())
    missing = str(uuid.uuid4())
    fake_embedding_model.rows = [{"chunk_id": have}]

    gap = await _unembedded_chunk_ids("rag.embeddings_oai_3_small_1536", [have, missing])
    assert gap == {missing}


@pytest.mark.asyncio
async def test_unembedded_chunk_ids_unknown_table_skips(fake_embedding_model):
    from matrx_rag.ingestion import _unembedded_chunk_ids

    gap = await _unembedded_chunk_ids("rag.embeddings_custom_999", [str(uuid.uuid4())])
    assert gap == set()  # unknown spec → self-heal silently skipped


@pytest.mark.asyncio
async def test_unembedded_chunk_ids_empty_input(fake_embedding_model):
    from matrx_rag.ingestion import _unembedded_chunk_ids

    assert await _unembedded_chunk_ids("rag.embeddings_oai_3_small_1536", []) == set()


@pytest.mark.asyncio
async def test_source_gap_probe_blocks_skip_until_healed(fake_embedding_model):
    """The skipped_unchanged early-exit guard: a source whose chunks lack
    embedding rows reports a gap; once rows exist the gap clears."""
    from matrx_rag import _ext
    from matrx_rag.ingestion import _source_has_embedding_gap

    c1, c2 = str(uuid.uuid4()), str(uuid.uuid4())

    class _FakeKgChunks:
        class _QB:
            async def values(self, *fields):
                return [{"id": c1}, {"id": c2}]

        @classmethod
        def filter(cls, **kwargs):
            assert kwargs.get("field_id__isnull") is True  # None → IS NULL branch
            return cls._QB()

    _ext.configure(db_models={"KgChunks": _FakeKgChunks})

    # One embedding missing → gap.
    fake_embedding_model.rows = [{"chunk_id": c1}]
    assert await _source_has_embedding_gap("rag.embeddings_oai_3_small_1536", "note", "n1", None)

    # Both present → no gap, skip allowed.
    fake_embedding_model.rows = [{"chunk_id": c1}, {"chunk_id": c2}]
    assert not await _source_has_embedding_gap(
        "rag.embeddings_oai_3_small_1536", "note", "n1", None
    )
