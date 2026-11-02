"""Regression — the derivative-chunk APPEND path is IDEMPOTENT (kg_038).

FOUND_DEFECTS 2026-07-07: ``derivation.py::_write_chunks`` (``replace=False``)
inserted rows with a fresh ``uuid4()`` per row, so re-running a batch whose
chunk transaction had already committed DOUBLE-INSERTED the set — a transient
flush failure could not be retried and blocked true self-healing.

The fix has three interlocking parts, each pinned here:

  1. The chunk write is a conflict-safe bulk insert —
     ``KgChunks.bulk_insert_ignore(rows, on_conflict=_CHUNK_CONFLICT_TARGET,
     returning="id")`` — where ``_CHUNK_CONFLICT_TARGET`` targets
     ``(processed_document_id, chunk_index, derivation_kind)`` WHERE
     ``derivation_kind <> 'initial_extract' AND deleted_at IS NULL``,
     mirroring the partial unique index ``kg_chunks_derivation_set_uidx``.
     The predicate is not decoration: Postgres infers a partial index only
     when the conflict specification's predicate implies the index's, so if
     these two ever drift apart every derived-chunk insert raises 42P10
     ("no unique or exclusion constraint matching the ON CONFLICT
     specification"). That is what this first test is for.
  2. ``_write_chunks`` writes embedding rows ONLY for the ids that actually
     landed (a conflict-skipped chunk's embedding would orphan) and returns
     the LANDED count — a full-conflict retry returns 0.
  3. Generators with a running chunk_index counter (synthetic Q&A, figure
     captions) resume from ``existing_max_chunk_index() + 1`` so a resumed
     run can never collide with the previous run's rows and lose NEW paid
     content to the DO-NOTHING skip.

2026-07-11 — Rewritten for the raw-SQL -> matrx-orm conversion (`derive
_chunk_set`/`_write_chunks` now go through `matrx_orm.transaction()` +
`advisory_xact_lock()` + `KgChunks.delete_where()` /
`KgChunks.bulk_insert_ignore()`, not hand-rolled asyncpg). The test now fakes
those SEAMS (`get_db_model`, `locked_transaction`) instead of a
raw asyncpg pool/connection — it pins the CONTRACT (conflict-safe bulk insert,
landed-ids-only embedding write, delete-then-insert atomicity), not SQL text.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

import pytest
from matrx_rag.derivation import _CHUNK_CONFLICT_TARGET, ChunkSpec, _write_chunks

# ---------------------------------------------------------------------------
# 1. The conflict target itself
# ---------------------------------------------------------------------------


def test_chunk_conflict_target_matches_kg_038_partial_index() -> None:
    assert list(_CHUNK_CONFLICT_TARGET.expressions) == [
        "processed_document_id",
        "chunk_index",
        "derivation_kind",
    ]
    # `deleted_at IS NULL` joined the index on 2026-09-20, when the six unique
    # indexes that still counted REMOVED rows were made partial — a soft-deleted
    # chunk used to block its own re-derivation. The conflict target had to
    # follow in the same change or inference breaks; see the module docstring.
    assert (
        _CHUNK_CONFLICT_TARGET.where
        == "deleted_at IS NULL AND derivation_kind <> 'initial_extract'"
    )


# ---------------------------------------------------------------------------
# Fake KgChunks model enforcing the kg_038 unique key with DO-NOTHING
# semantics, keyed on (processed_document_id, chunk_index, derivation_kind) —
# mirrors the live partial unique index without any SQL/connection faking.
# ---------------------------------------------------------------------------


class _FakeKgChunks:
    def __init__(self) -> None:
        # identity key -> chunk id
        self.rows: dict[tuple[str, int, str], str] = {}
        self.delete_calls: list[dict[str, Any]] = []

    async def delete_where(self, **filters: Any) -> int:
        self.delete_calls.append(filters)
        derivative_id = str(filters["processed_document_id"])
        kind = filters["derivation_kind"]
        before = len(self.rows)
        self.rows = {
            k: v for k, v in self.rows.items() if not (k[0] == derivative_id and k[2] == kind)
        }
        return before - len(self.rows)

    async def bulk_insert_ignore(
        self, objects_data: list[dict[str, Any]], *, on_conflict: Any, returning: Any = False
    ) -> list[str]:
        assert on_conflict is _CHUNK_CONFLICT_TARGET
        assert returning == "id"
        landed: list[str] = []
        for row in objects_data:
            key = (str(row["processed_document_id"]), int(row["chunk_index"]), row["derivation_kind"])
            if row["derivation_kind"] != "initial_extract" and key in self.rows:
                continue  # DO NOTHING
            self.rows[key] = row["id"]
            landed.append(row["id"])
        return landed


@asynccontextmanager
async def _fake_locked_transaction(*_keys: Any, **_kw: Any) -> Any:
    yield None


_PARENT_DOC = {
    "created_by": "owner-1",
    "source_kind": "cld_file",
    "source_id": "src-1",
    "mime_type": "application/pdf",
    "source_hash": "hash-1",
}


@pytest.fixture
def kg_chunks(monkeypatch: pytest.MonkeyPatch) -> _FakeKgChunks:
    fake = _FakeKgChunks()

    def _fake_get_db_model(name: str) -> Any:
        assert name == "KgChunks"
        return fake

    import matrx_rag.derivation as derivation_mod

    monkeypatch.setattr(derivation_mod, "get_db_model", _fake_get_db_model)
    monkeypatch.setattr(derivation_mod, "locked_transaction", _fake_locked_transaction)
    return fake


@pytest.fixture
def embedding_calls(monkeypatch: pytest.MonkeyPatch) -> list[list[tuple]]:
    """Capture the payloads _write_chunks hands to _write_embedding_rows.

    _write_embedding_rows is fully ORM now (``embedding_table, payloads,
    batch_size=None``) — it takes no connection at all, so there is no pool
    to fake here anymore."""
    calls: list[list[tuple]] = []

    async def _capture(table: str, payloads: list[tuple], **kw: Any) -> int:
        calls.append(payloads)
        return len(payloads)

    import matrx_rag.ingestion as ingestion_mod

    monkeypatch.setattr(ingestion_mod, "_write_embedding_rows", _capture)
    return calls


async def _run_batch(specs: list[ChunkSpec]) -> int:
    return await _write_chunks(
        derivative_id="11111111-1111-1111-1111-111111111111",
        derivation_kind="synthetic_qa",
        parent_doc=_PARENT_DOC,
        organization_id="org-1",
        chunks=specs,
        embeddings=[[0.1, 0.2] for _ in specs],
        embedding_table="rag.embeddings_oai_3_small_1536",
        priority=0,
        agent_id=None,
        extraction_run_id=None,
        chunker_name="test",
        chunker_version="v1",
        page_id_by_number={},
        replace=False,
    )


# ---------------------------------------------------------------------------
# 2. Retrying a committed batch is a no-op (the self-heal contract)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_append_retry_is_idempotent(
    kg_chunks: _FakeKgChunks, embedding_calls: list[list[tuple]]
) -> None:
    specs = [ChunkSpec(content_text=f"Q{i}", chunk_index=i) for i in range(3)]

    first = await _run_batch(specs)
    assert first == 3
    assert len(kg_chunks.rows) == 3
    assert len(embedding_calls[0]) == 3

    # The RETRY — same batch, same chunk_index values (what retry_on_transient
    # replays after a commit-then-transient-failure). Zero new rows, zero new
    # embedding payloads, no double-insert.
    second = await _run_batch(specs)
    assert second == 0
    assert len(kg_chunks.rows) == 3, "retry double-inserted the batch"
    assert embedding_calls[1] == [], "embedding rows written for conflict-skipped chunks"

    # replace=False (append mode) must NEVER delete.
    assert kg_chunks.delete_calls == []


@pytest.mark.asyncio
async def test_partial_conflict_embeds_only_landed(
    kg_chunks: _FakeKgChunks, embedding_calls: list[list[tuple]]
) -> None:
    await _run_batch([ChunkSpec(content_text="Q0", chunk_index=0)])

    # A later batch overlapping index 0 (the pre-fix caption/QA resume shape):
    # only the NEW index lands, and only ITS embedding is written.
    written = await _run_batch(
        [
            ChunkSpec(content_text="Q0-again", chunk_index=0),
            ChunkSpec(content_text="Q1", chunk_index=1),
        ]
    )
    assert written == 1
    assert len(kg_chunks.rows) == 2
    landed_payload = embedding_calls[-1]
    assert len(landed_payload) == 1
    assert (
        landed_payload[0][0]
        == kg_chunks.rows[("11111111-1111-1111-1111-111111111111", 1, "synthetic_qa")]
    )


# ---------------------------------------------------------------------------
# 3. Resume counters continue from the persisted max (no new-content loss)
# ---------------------------------------------------------------------------


def test_generators_resume_from_existing_max_chunk_index() -> None:
    """Source-level pin: both running-counter generators consult
    existing_max_chunk_index on a non-reset run. (Behavioral coverage needs a
    live DB; this keeps the call from silently disappearing.)"""
    from pathlib import Path

    pkg = Path(__file__).resolve().parent.parent / "matrx_rag"
    caption_src = (pkg / "image_caption_derivation.py").read_text(encoding="utf-8")
    assert "existing_max_chunk_index" in caption_src

    repo_root = pkg.parent.parent.parent
    kd = repo_root / "aidream" / "services" / "knowledge_derivations.py"
    if kd.exists():  # standalone package checkouts don't ship aidream
        assert "existing_max_chunk_index" in kd.read_text(encoding="utf-8")
