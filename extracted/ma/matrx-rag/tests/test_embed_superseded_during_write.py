"""A chunk superseded AFTER the live re-check but BEFORE the vector write must be dropped and
counted (not fail the stage on the kg_chunks FK); an FK failure with every chunk still present
must still raise (system_error class content_processing_stage_failed, 2026-11-18)."""

from __future__ import annotations

import asyncio

import pytest
from matrx_orm.exceptions import IntegrityError

from matrx_rag import stages

GONE = "00000000-0000-0000-0000-000000000001"
KEPT = "00000000-0000-0000-0000-000000000002"


class _Aw:
    def __init__(self, rows):
        self._rows = rows

    def order_by(self, *_a):
        return self

    def values(self, *_a):
        return self

    def __await__(self):
        async def go():
            return self._rows
        return go().__await__()


def _run(monkeypatch, *, live_after_failure):
    candidates = [{"id": GONE, "content_text": "a", "metadata": {}},
                  {"id": KEPT, "content_text": "b", "metadata": {}}]
    written: list[list[dict]] = []
    state = {"rechecks": 0}

    class KgChunks:
        @staticmethod
        async def count(**_k):
            return 2

        @staticmethod
        def filter(**k):
            if "processed_document_id" in k:
                return _Aw(candidates)
            state["rechecks"] += 1
            if state["rechecks"] == 1:  # first re-check: both still exist
                return _Aw([{"id": GONE}, {"id": KEPT}])
            return _Aw([{"id": i} for i in live_after_failure])

    class Emb:
        @staticmethod
        def filter(**_k):
            return _Aw([])

        @staticmethod
        async def bulk_upsert(rows, **_k):
            if any(r["chunk_id"] == GONE for r in rows):
                raise IntegrityError(model=None, constraint="foreign_key", original_error=None)
            written.append(rows)

    async def load_doc(_id):
        return {"organization_id": "o", "created_by": "u"}

    async def eff(_o, _u):
        return "o"

    async def fake_embed(_m, texts, **_k):
        return [[0.1] for _ in texts]

    class Spec:
        table = "embeddings_voyage_4_large_1024"

    async def progress(_e):
        return None

    monkeypatch.setattr(stages, "_load_doc", load_doc)
    monkeypatch.setattr("matrx_rag.ingestion.resolve_effective_org", eff)
    monkeypatch.setattr(stages, "get_db_model", lambda _n: KgChunks)
    monkeypatch.setattr(stages, "_embedding_model_for_table", lambda _t: Emb)
    monkeypatch.setattr(stages, "spec_for", lambda _m: Spec)
    monkeypatch.setattr(stages, "embed", fake_embed)
    res = asyncio.run(stages.run_embed(processed_document_id="d", on_progress=progress,
                                       embedding_model="voyage:voyage-4-large"))
    return res, written


def test_chunk_superseded_between_recheck_and_write_is_dropped_and_counted(monkeypatch):
    res, written = _run(monkeypatch, live_after_failure=[KEPT])
    assert res.chunks_embedded == 1 and res.chunks_skipped_gone == 1
    assert [r["chunk_id"] for r in written[0]] == [KEPT]


def test_fk_failure_with_every_chunk_present_still_fails_loudly(monkeypatch):
    with pytest.raises(IntegrityError):
        _run(monkeypatch, live_after_failure=[GONE, KEPT])
