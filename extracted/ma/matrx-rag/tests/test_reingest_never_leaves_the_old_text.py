"""A re-ingest never leaves the previous text searchable beside the new.

Live 2026-10-10 (found 2026-10-11): note 0a441c86… carried TWO live
``initial_extract`` chunks at chunk_index 0 — the 33-char old text and the
134-char new text, written 2 s apart. Two ingests of one source (a save burst)
both read ``existing_by_sha`` BEFORE the advisory lock; the second deleted only
the rows in its own (stale) snapshot and kept the first run's chunk alive.
``upsert_chunks`` now re-reads the source's rows under the lock and deletes
every row it does not keep.

Fail-before: on the pre-fix ingestion.py the old chunk survives (2 rows).
"""

from __future__ import annotations

import hashlib

import pytest

try:
    from test_chunk_reuse import _FakeKgChunksDb, _make_chunk, _make_resolved, _wire_fake_db  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    from tests.test_chunk_reuse import _FakeKgChunksDb, _make_chunk, _make_resolved, _wire_fake_db  # type: ignore[import-not-found]


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@pytest.fixture
def db(monkeypatch):
    from dataclasses import dataclass

    import matrx_rag.ingestion as ingestion_mod

    fake = _FakeKgChunksDb()
    _wire_fake_db(monkeypatch, fake)

    @dataclass(frozen=True)
    class _Spec:
        name: str = "openai:text-embedding-3-small"
        dim: int = 4
        table: str = "rag.embeddings_oai_3_small_1536"
        batch_size: int = 96

    monkeypatch.setattr(ingestion_mod, "spec_for", lambda model: _Spec())

    return fake


async def _ingest(text: str, snapshot: dict[str, str]) -> dict:
    from matrx_rag.ingestion import upsert_chunks

    chunk = _make_chunk(text, 0)
    return await upsert_chunks(
        resolved=_make_resolved(source_id="note-save-burst"),
        chunks=[chunk],
        embedding_model="openai:text-embedding-3-small",
        embeddings=None,
        new_shas=[_sha(chunk.content_text)],
        existing_by_sha=snapshot,
    )


@pytest.mark.asyncio
async def test_second_ingest_with_a_stale_snapshot_removes_the_first_runs_chunk(db):
    # Both runs read the source BEFORE either committed: an empty snapshot each.
    await _ingest("Meeting notes: draft", {})
    await _ingest("Meeting notes: agenda, owners, decisions and the follow-up dates", {})

    texts = sorted(row["content_text"] for row in db.chunks.values())
    assert texts == ["Meeting notes: agenda, owners, decisions and the follow-up dates"], (
        f"the old text is still searchable beside the new: {texts}"
    )


@pytest.mark.asyncio
async def test_unchanged_content_is_still_reused_not_rewritten(db):
    await _ingest("Quarterly plan", {})
    first_id = next(iter(db.chunks))
    result = await _ingest("Quarterly plan", {})  # stale empty snapshot again
    assert list(db.chunks) == [first_id]
    assert result["chunks_reused"] == 1 and result["chunks_deleted"] == 0
