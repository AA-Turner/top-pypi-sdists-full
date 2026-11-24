"""run_embed must skip (visibly) a chunk deleted between chunking and the vector write,
not fail the whole stage on the kg_chunks FK (system_error ebf2c4b6, 2026-11-14+)."""

from __future__ import annotations

import asyncio

from matrx_rag import stages


class _Q:
    def __init__(self, rows):
        self._rows = rows

    def order_by(self, *_a):
        return self

    def values(self, *_a):
        async def go():
            return self._rows
        return go().__await__() if False else _Aw(self._rows)


class _Aw:
    def __init__(self, rows):
        self._rows = rows

    def __await__(self):
        async def go():
            return self._rows
        return go().__await__()


def test_deleted_chunk_is_skipped_and_reported(monkeypatch):
    gone, kept = "00000000-0000-0000-0000-000000000001", "00000000-0000-0000-0000-000000000002"
    candidates = [{"id": gone, "content_text": "a", "metadata": {}},
                  {"id": kept, "content_text": "b", "metadata": {}}]
    written: list[list[dict]] = []

    class KgChunks:
        @staticmethod
        async def count(**_k):
            return 2

        @staticmethod
        def filter(**k):
            if "processed_document_id" in k:
                return _Q(candidates)
            return _Q([{"id": kept}])  # the live re-check: only `kept` still exists

    class Emb:
        @staticmethod
        def filter(**_k):
            return _Q([])

        @staticmethod
        async def bulk_upsert(rows, **_k):
            if any(r["chunk_id"] == gone for r in rows):
                raise AssertionError("FK would refuse a deleted chunk")
            written.append(rows)

    async def load_doc(_id):
        return {"organization_id": "o", "created_by": "u"}

    async def eff(_o, _u):
        return "o"

    async def fake_embed(_m, texts, **_k):
        return [[0.1] for _ in texts]

    class Spec:
        table = "embeddings_voyage_4_large_1024"

    monkeypatch.setattr(stages, "_load_doc", load_doc)
    monkeypatch.setattr("matrx_rag.ingestion.resolve_effective_org", eff)
    monkeypatch.setattr(stages, "get_db_model", lambda _n: KgChunks)
    monkeypatch.setattr(stages, "_embedding_model_for_table", lambda _t: Emb)
    monkeypatch.setattr(stages, "spec_for", lambda _m: Spec)
    monkeypatch.setattr(stages, "embed", fake_embed)

    events = []

    async def progress(e):
        events.append(e)

    res = asyncio.run(stages.run_embed(processed_document_id="d", on_progress=progress,
                                       embedding_model="voyage:voyage-4-large"))
    assert res.chunks_embedded == 1 and res.chunks_skipped_gone == 1
    assert [r["chunk_id"] for r in written[0]] == [kept]
    assert any((e.extra or {}).get("skipped_chunks_gone") == 1 for e in events)
