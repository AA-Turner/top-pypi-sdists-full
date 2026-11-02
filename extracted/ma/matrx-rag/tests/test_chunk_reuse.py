"""Phase A — Knowledge Graph chunk-level reuse.

Verifies the upsert_chunks SHA-keyed reuse path:

* On first ingest, every chunk is INSERTED.
* On re-ingest with one changed chunk, exactly one row is INSERTED,
  one row is DELETED, the rest are REUSED (their chunk_id stays the
  same, their embedding row is not re-written).
* The reuse count + delete count match expectations.

``upsert_chunks`` (packages/matrx-rag/matrx_rag/ingestion.py) writes through
real matrx-orm primitives — ``KgChunks.delete_where`` /
``.bulk_insert_ignore`` / ``.bulk_update_by_pk``, ``matrx_orm.transaction()``
+ ``.advisory_xact_lock()``, and per-embedding-table
``Model.bulk_insert_ignore`` — no raw asyncpg pool/conn. The fakes below
simulate that ORM surface in memory. No live DB, no network.
"""

from __future__ import annotations

import contextlib
import hashlib
from typing import Any

import pytest

# ---------------------------------------------------------------------------
# Fake ORM surface — minimal in-memory substitute for KgChunks / the
# embedding-table models, matching exactly the methods upsert_chunks calls.
# ---------------------------------------------------------------------------


class _FakeKgChunksDb:
    """In-memory rag.kg_chunks + embeddings substitute.

    Schema represented per row:
        {id, source_kind, source_id, field_id, chunker_version,
         content_text, content_sha256, chunk_index, parent_chunk_id,
         metadata, page_numbers, page_spans, source_hash, ...}
    """

    def __init__(self) -> None:
        self.chunks: dict[str, dict[str, Any]] = {}  # by id
        self.embeddings: dict[str, dict[str, Any]] = {}  # by chunk_id
        self.delete_log: list[list[str]] = []
        self.insert_log: list[list[str]] = []
        self.update_log: list[list[str]] = []
        self.update_cast_log: list[dict[str, str]] = []
        # Rows per embedding bulk_insert_ignore call, in order — the
        # durable-write tests assert batching shape from this.
        self.embedding_insert_log: list[int] = []


class _FakeKgChunksModel:
    """Simulates the ``KgChunks`` ORM surface ``upsert_chunks`` calls:
    ``delete_where`` / ``bulk_insert_ignore`` / ``bulk_update_by_pk``."""

    def __init__(self, db: _FakeKgChunksDb) -> None:
        self._db = db

    def filter(self, **filters: Any):
        """``filter(source_kind=, source_id=, chunker_version=, content_sha256__isnull=False)
        .values(...)`` — the source snapshot ``_existing_chunks_by_sha`` reads."""
        db = self._db

        def _match(row: dict[str, Any]) -> bool:
            for key, want in filters.items():
                if key == "content_sha256__isnull":
                    if (row.get("content_sha256") is None) != bool(want):
                        return False
                elif row.get(key) != want:
                    return False
            return True

        class _QB:
            async def values(self, *fields: str) -> list[dict[str, Any]]:
                return [
                    {f: row.get(f) for f in fields}
                    for row in db.chunks.values()
                    if _match(row)
                ]

        return _QB()

    async def delete_where(self, **filters: Any) -> int:
        if "id__in" in filters:
            ids = list(filters["id__in"])
            removed = [cid for cid in ids if cid in self._db.chunks]
        else:
            sk = filters["source_kind"]
            sid = filters["source_id"]
            field_isnull = filters.get("field_id__isnull", False)
            fid = filters.get("field_id")
            removed = [
                cid
                for cid, row in self._db.chunks.items()
                if row["source_kind"] == sk
                and row["source_id"] == sid
                and (
                    (field_isnull and row.get("field_id") is None)
                    or (not field_isnull and row.get("field_id") == fid)
                )
            ]
        for cid in removed:
            del self._db.chunks[cid]
            self._db.embeddings.pop(cid, None)
        self._db.delete_log.append(removed)
        return len(removed)

    async def bulk_insert_ignore(
        self,
        objects_data: list[dict[str, Any]],
        *,
        on_conflict: Any = None,
        returning: bool | str = False,
        connection: Any = None,
    ) -> int | list[dict[str, Any]] | list[Any]:
        # Enforce the unique index (source_kind, source_id, content_sha256,
        # chunker_version) — DO NOTHING on conflict, mirroring the real index.
        landed: list[str] = []
        for row in objects_data:
            conflict = any(
                r["source_kind"] == row["source_kind"]
                and r["source_id"] == row["source_id"]
                and r.get("content_sha256") == row.get("content_sha256")
                and r["chunker_version"] == row["chunker_version"]
                for r in self._db.chunks.values()
            )
            if conflict:
                continue
            cid = row["id"]
            self._db.chunks[cid] = dict(row)
            landed.append(cid)
        self._db.insert_log.append(landed)
        if returning == "id":
            return landed
        if returning is True:
            return [dict(self._db.chunks[cid]) for cid in landed]
        return len(landed)

    async def bulk_update_by_pk(
        self,
        objects_data: list[dict[str, Any]],
        *,
        pk_field: str = "id",
        casts: dict[str, str] | None = None,
        set_expressions: dict[str, Any] | None = None,
        connection: Any = None,
    ) -> int:
        self._db.update_cast_log.append(dict(casts or {}))
        updated: list[str] = []
        for row in objects_data:
            cid = row[pk_field]
            if cid in self._db.chunks:
                r = self._db.chunks[cid]
                for k, v in row.items():
                    if k == pk_field:
                        continue
                    r[k] = v
                updated.append(cid)
        self._db.update_log.append(updated)
        return len(updated)


class _FakeEmbeddingModel:
    """Simulates one ``embeddings_*`` table's ORM surface — the write side
    (``bulk_insert_ignore``) and the read side (``filter().values()``) used
    by ``_unembedded_chunk_ids`` / ``_source_has_embedding_gap``."""

    def __init__(self, db: _FakeKgChunksDb) -> None:
        self._db = db

    async def bulk_insert_ignore(
        self,
        objects_data: list[dict[str, Any]],
        *,
        on_conflict: Any = None,
        returning: bool | str = False,
        connection: Any = None,
    ) -> int | list[dict[str, Any]]:
        n = 0
        for row in objects_data:
            cid = row["chunk_id"]
            self._db.embeddings[cid] = dict(row)
            n += 1
        self._db.embedding_insert_log.append(n)
        if returning is True:
            return [dict(self._db.embeddings[row["chunk_id"]]) for row in objects_data]
        return n

    def filter(self, **kwargs: Any):
        ids = set(kwargs.get("chunk_id__in") or [])
        db = self._db

        class _QB:
            async def values(self, *fields: str):
                return [{"chunk_id": cid} for cid in db.embeddings if cid in ids]

        return _QB()


_EMBEDDING_MODEL_NAMES = (
    "EmbeddingsOai3Small1536",
    "EmbeddingsVoyageCode31024",
    "EmbeddingsVoyage4Large1024",
)


@contextlib.asynccontextmanager
async def _noop_transaction(*_a: Any, **_kw: Any):
    yield None



# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _wire_fake_db(monkeypatch, db: _FakeKgChunksDb) -> None:
    """Patch matrx_rag.ingestion's ORM entry points to the in-memory fake.

    ``locked_transaction()`` becomes a no-op — single-
    threaded tests never yield control between the conflict-check and the
    insert inside ``_FakeKgChunksModel.bulk_insert_ignore`` (no ``await`` in
    between), so the fake's uniqueness check is race-safe under
    ``asyncio.gather`` without needing a real lock (see
    test_chunk_conflict.py).
    """
    import matrx_rag.ingestion as ingestion_mod

    kg_chunks = _FakeKgChunksModel(db)
    embedding_models = {name: _FakeEmbeddingModel(db) for name in _EMBEDDING_MODEL_NAMES}

    def _fake_get_db_model(name: str, schema: str | None = None):
        if name == "KgChunks":
            return kg_chunks
        if name in embedding_models:
            return embedding_models[name]
        raise AssertionError(f"fake_db_pool: unexpected get_db_model({name!r})")

    monkeypatch.setattr(ingestion_mod, "get_db_model", _fake_get_db_model)
    # ``locked_transaction(key, …)`` (matrx_orm) opens the chunk transaction holding the advisory lock.
    monkeypatch.setattr(ingestion_mod, "locked_transaction", _noop_transaction)


@pytest.fixture
def fake_db_pool(monkeypatch):
    db = _FakeKgChunksDb()
    _wire_fake_db(monkeypatch, db)
    return db


@pytest.fixture
def stub_embedding_spec(monkeypatch):
    """Pin spec_for to a stable table name + dim so the inserts compose."""
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class _Spec:
        name: str = "openai:text-embedding-3-small"
        dim: int = 4
        table: str = "rag.embeddings_oai_3_small_1536"
        batch_size: int = 96

    import matrx_rag.ingestion as ingestion_mod
    monkeypatch.setattr(ingestion_mod, "spec_for", lambda model: _Spec())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _make_chunk(text: str, idx: int) -> Any:
    import uuid

    from matrx_rag.chunking import Chunk

    return Chunk(
        chunk_id=str(uuid.uuid4()),
        content_text=text,
        chunk_index=idx,
        chunk_kind="text",
        token_count=len(text.split()),
        parent_chunk_id=None,
        language=None,
        metadata={},
    )


def _make_resolved(source_id: str = "src-1") -> Any:
    from matrx_rag.sources import ResolvedSource

    return ResolvedSource(
        source_kind="note",
        source_id=source_id,
        field_id=None,
        organization_id="11111111-1111-1111-1111-111111111111",
        owner_id="22222222-2222-2222-2222-222222222222",
        text="full text",
        source_hash="hash-1",
        mime_type="text/plain",
        language=None,
        metadata={},
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_first_ingest_inserts_every_chunk(fake_db_pool, stub_embedding_spec):
    """Fresh source — no existing chunks. All 5 chunks INSERTED."""
    from matrx_rag.ingestion import upsert_chunks

    chunks = [_make_chunk(f"chunk text number {i}", i) for i in range(5)]
    new_shas = [_sha(c.content_text) for c in chunks]
    embeddings = [[0.1, 0.2, 0.3, 0.4]] * 5
    resolved = _make_resolved()

    result = await upsert_chunks(
        resolved=resolved,
        chunks=chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=embeddings,
        new_shas=new_shas,
        existing_by_sha={},
    )

    assert result["chunks_written"] == 5
    assert result["chunks_inserted"] == 5
    assert result["chunks_reused"] == 0
    assert result["chunks_deleted"] == 0
    assert len(fake_db_pool.chunks) == 5
    assert len(fake_db_pool.embeddings) == 5


@pytest.mark.asyncio
async def test_reingest_with_one_changed_chunk_reuses_the_rest(
    fake_db_pool, stub_embedding_spec
):
    """Re-ingest with chunk #3 changed:
    * chunks 1, 2, 4, 5 are REUSED (their existing chunk_ids stay)
    * chunk #3 (new SHA) is INSERTED with a new id
    * the OLD chunk #3 is DELETED
    """
    from matrx_rag.ingestion import upsert_chunks

    # First pass — seed five chunks.
    original_chunks = [_make_chunk(f"chunk text number {i}", i) for i in range(5)]
    original_shas = [_sha(c.content_text) for c in original_chunks]
    embeddings = [[0.1, 0.2, 0.3, 0.4]] * 5
    resolved = _make_resolved()

    await upsert_chunks(
        resolved=resolved,
        chunks=original_chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=embeddings,
        new_shas=original_shas,
        existing_by_sha={},
    )
    assert len(fake_db_pool.chunks) == 5
    seeded_ids = set(fake_db_pool.chunks.keys())

    # Second pass — modify chunk #3, keep the rest byte-identical.
    second_chunks = [_make_chunk(f"chunk text number {i}", i) for i in range(5)]
    second_chunks[3] = _make_chunk("DIFFERENT TEXT FOR CHUNK 3", 3)
    # Re-text the unchanged chunks so their SHAs match the first pass.
    for i in (0, 1, 2, 4):
        second_chunks[i] = _make_chunk(f"chunk text number {i}", i)
    second_shas = [_sha(c.content_text) for c in second_chunks]

    # Existing map from the seeded DB.
    existing_by_sha = {
        row["content_sha256"]: row["id"]
        for row in fake_db_pool.chunks.values()
    }
    assert len(existing_by_sha) == 5

    second_embeddings: list[list[float] | None] = [None] * 5
    second_embeddings[3] = [0.9, 0.9, 0.9, 0.9]  # only the new chunk has an embedding

    result = await upsert_chunks(
        resolved=resolved,
        chunks=second_chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=second_embeddings,
        new_shas=second_shas,
        existing_by_sha=existing_by_sha,
    )

    assert result["chunks_written"] == 5
    assert result["chunks_inserted"] == 1  # only chunk #3
    assert result["chunks_reused"] == 4
    assert result["chunks_deleted"] == 1  # the old chunk #3
    assert fake_db_pool.update_cast_log[-1]["chunk_index"] == "integer"

    # The reused chunk_ids are still in the DB
    remaining_seeded = seeded_ids & set(fake_db_pool.chunks.keys())
    assert len(remaining_seeded) == 4

    # The new chunk got inserted (new id not in seeded set)
    new_ids = set(fake_db_pool.chunks.keys()) - seeded_ids
    assert len(new_ids) == 1

    # Only one new embedding row was written
    seeded_embedding_count = sum(
        1 for cid in seeded_ids if cid in fake_db_pool.embeddings
    )
    new_embedding_count = sum(
        1 for cid in new_ids if cid in fake_db_pool.embeddings
    )
    assert new_embedding_count == 1
    assert seeded_embedding_count == 4  # original embeddings untouched


@pytest.mark.asyncio
async def test_legacy_path_without_sha_args_falls_back_to_wipe(
    fake_db_pool, stub_embedding_spec
):
    """When the caller doesn't pass new_shas/existing_by_sha, behave
    exactly as before — wipe and replace. Image / PDF callers depend on this.
    """
    from matrx_rag.ingestion import upsert_chunks

    # Seed three rows.
    initial = [_make_chunk(f"alpha {i}", i) for i in range(3)]
    initial_shas = [_sha(c.content_text) for c in initial]
    await upsert_chunks(
        resolved=_make_resolved(),
        chunks=initial,
        embedding_model="openai:text-embedding-3-small",
        embeddings=[[0.0, 0.0, 0.0, 0.0]] * 3,
        new_shas=initial_shas,
        existing_by_sha={},
    )
    assert len(fake_db_pool.chunks) == 3

    # Legacy call — no SHAs supplied. Should wipe + re-insert.
    new_chunks = [_make_chunk(f"beta {i}", i) for i in range(2)]
    result = await upsert_chunks(
        resolved=_make_resolved(),
        chunks=new_chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=[[1.0, 1.0, 1.0, 1.0]] * 2,
    )
    # Total rows are now exactly the 2 new ones.
    assert len(fake_db_pool.chunks) == 2
    assert result["chunks_written"] == 2
    assert result["chunks_inserted"] == 2
    assert result["chunks_reused"] == 0
    assert result["chunks_deleted"] == 3  # the seeded ones got wiped


@pytest.mark.asyncio
async def test_three_word_edit_to_a_ten_chunk_note_reuses_nine(
    fake_db_pool, stub_embedding_spec
):
    """The plan's headline acceptance test — 10-chunk note, edit 3
    words (one chunk), assert 9 reused + 1 new + 1 deleted."""
    from matrx_rag.ingestion import upsert_chunks

    original = [_make_chunk(f"paragraph number {i}, plenty of words", i) for i in range(10)]
    original_shas = [_sha(c.content_text) for c in original]
    await upsert_chunks(
        resolved=_make_resolved(),
        chunks=original,
        embedding_model="openai:text-embedding-3-small",
        embeddings=[[0.0, 0.0, 0.0, 0.0]] * 10,
        new_shas=original_shas,
        existing_by_sha={},
    )

    # Edit paragraph #5: "plenty of words" → "many small terms"
    second = [
        _make_chunk("paragraph number 5, many small terms", 5)
        if i == 5
        else _make_chunk(f"paragraph number {i}, plenty of words", i)
        for i in range(10)
    ]
    second_shas = [_sha(c.content_text) for c in second]
    existing_by_sha = {
        row["content_sha256"]: row["id"] for row in fake_db_pool.chunks.values()
    }

    embeddings: list[list[float] | None] = [None] * 10
    embeddings[5] = [0.7, 0.7, 0.7, 0.7]

    result = await upsert_chunks(
        resolved=_make_resolved(),
        chunks=second,
        embedding_model="openai:text-embedding-3-small",
        embeddings=embeddings,
        new_shas=second_shas,
        existing_by_sha=existing_by_sha,
    )

    assert result["chunks_reused"] == 9
    assert result["chunks_inserted"] == 1
    assert result["chunks_deleted"] == 1
    assert result["chunks_written"] == 10


@pytest.mark.asyncio
async def test_a_reused_chunk_that_vanished_under_the_lock_is_embedded_not_refused(
    fake_db_pool, stub_embedding_spec, monkeypatch
):
    """Race (final review 2026-10-15): the caller snapshot said chunk B is REUSED
    (no vector sent); a concurrent run removed B's row before this write took the
    lock, so the under-lock re-split must INSERT it. Fail-before: ValueError
    "being INSERTED but its embedding vector is None". Now its vector is fetched
    through ``embed`` after the commit and every embedding row carries one."""
    import matrx_rag.ingestion as ingestion_mod
    from matrx_rag.ingestion import upsert_chunks

    resolved = _make_resolved()
    seed = [_make_chunk(f"seeded paragraph {i}", i) for i in range(3)]
    await upsert_chunks(
        resolved=resolved,
        chunks=seed,
        embedding_model="openai:text-embedding-3-small",
        embeddings=[[0.1, 0.2, 0.3, 0.4]] * 3,
        new_shas=[_sha(c.content_text) for c in seed],
        existing_by_sha={},
    )
    snapshot = {row["content_sha256"]: row["id"] for row in fake_db_pool.chunks.values()}
    vanished_sha = _sha("seeded paragraph 1")
    vanished_id = snapshot[vanished_sha]

    @contextlib.asynccontextmanager
    async def _concurrent_delete_then_lock(*_a: Any, **_kw: Any):
        # Another writer deleted the row while this one waited for the lock.
        fake_db_pool.chunks.pop(vanished_id, None)
        fake_db_pool.embeddings.pop(vanished_id, None)
        yield None

    monkeypatch.setattr(ingestion_mod, "locked_transaction", _concurrent_delete_then_lock)

    async def _fresh_snapshot(*_a: Any, **_kw: Any) -> dict[str, str]:
        return {row["content_sha256"]: row["id"] for row in fake_db_pool.chunks.values()}

    monkeypatch.setattr(ingestion_mod, "_existing_chunks_by_sha", _fresh_snapshot)
    embedded: list[list[str]] = []

    async def _fake_embed(model: str, texts: list[str], **_kw: Any) -> list[list[float]]:
        embedded.append(list(texts))
        return [[0.7, 0.7, 0.7, 0.7] for _ in texts]

    monkeypatch.setattr(ingestion_mod, "embed", _fake_embed)

    second = [_make_chunk(f"seeded paragraph {i}", i) for i in range(3)] + [_make_chunk("a brand new paragraph", 3)]
    vectors: list[list[float] | None] = [None, None, None, [0.9, 0.9, 0.9, 0.9]]
    result = await upsert_chunks(
        resolved=resolved,
        chunks=second,
        embedding_model="openai:text-embedding-3-small",
        embeddings=vectors,
        new_shas=[_sha(c.content_text) for c in second],
        existing_by_sha=dict(snapshot),
    )

    assert result["chunks_inserted"] == 2  # the vanished chunk + the new one
    assert embedded == [[ingestion_mod._embed_text_for(second[1])]]  # only the gap is paid
    new_b = second[1].chunk_id
    assert new_b in fake_db_pool.chunks
    assert fake_db_pool.embeddings[new_b] is not None
    assert all(cid in fake_db_pool.embeddings for cid in fake_db_pool.chunks), "a chunk row lacks its vector"
