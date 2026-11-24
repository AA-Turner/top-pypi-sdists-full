"""The embed STAGE's vector write fits the database's statement budget (2026-11-16 23:59Z).

One 73-row ``INSERT INTO rag.embeddings_voyage_4_large_1024`` ran exactly 10.0 s (IO/DataFileRead,
no blocker: every row is an HNSW insert reading index pages from disk), hit the pool's 10 s
``command_timeout`` and dead-lettered a kept Source. ``ingestion._write_embedding_rows`` was fixed
the day before; this stage had its own copy of the write and was not. Small statements, and the
driver waits for the server's own ceiling.
"""

from __future__ import annotations

import asyncio

from matrx_orm import SERVER_CEILING

from matrx_rag import stages
from matrx_rag.ingestion import EMBED_WRITE_BATCH_SIZE


class _Aw:
    def __init__(self, rows):
        self._rows = rows

    def __await__(self):
        async def go():
            return self._rows

        return go().__await__()


class _Q:
    def __init__(self, rows):
        self._rows = rows

    def order_by(self, *_a):
        return self

    def values(self, *_a):
        return _Aw(self._rows)


def test_the_stage_writes_small_statements_that_wait_for_the_server_ceiling(monkeypatch):
    ids = [f"00000000-0000-0000-0000-{i:012d}" for i in range(EMBED_WRITE_BATCH_SIZE * 2 + 23)]
    candidates = [{"id": i, "content_text": "t", "metadata": {}} for i in ids]
    calls: list[tuple[int, object]] = []

    class KgChunks:
        @staticmethod
        async def count(**_k):
            return len(ids)

        @staticmethod
        def filter(**k):
            if "processed_document_id" in k:
                return _Q(candidates)
            return _Q([{"id": i} for i in ids])  # every chunk still exists

    class Emb:
        @staticmethod
        def filter(**_k):
            return _Q([])

        @staticmethod
        async def bulk_upsert(rows, **kw):
            calls.append((len(rows), kw.get("statement_timeout")))

    async def load_doc(_id):
        return {"organization_id": "o", "created_by": "u"}

    async def eff(_o, _u):
        return "o"

    async def fake_embed(_m, texts, **_k):
        return [[0.1] for _ in texts]

    class Spec:
        table = "embeddings_voyage_4_large_1024"
        batch_size = 1000  # one provider batch holds every chunk: only the write split matters

    monkeypatch.setattr(stages, "_load_doc", load_doc)
    monkeypatch.setattr("matrx_rag.ingestion.resolve_effective_org", eff)
    monkeypatch.setattr(stages, "get_db_model", lambda _n: KgChunks)
    monkeypatch.setattr(stages, "_embedding_model_for_table", lambda _t: Emb)
    monkeypatch.setattr(stages, "spec_for", lambda _m: Spec)
    monkeypatch.setattr(stages, "embed", fake_embed)

    async def progress(_e):
        return None

    res = asyncio.run(
        stages.run_embed(
            processed_document_id="d", on_progress=progress, embedding_model="voyage:voyage-4-large"
        )
    )
    assert res.chunks_embedded == len(ids)
    assert len(calls) > 1, "one statement for every vector is the defect"
    assert all(n <= EMBED_WRITE_BATCH_SIZE for n, _ in calls)
    assert sum(n for n, _ in calls) == len(ids)
    assert all(t is SERVER_CEILING for _, t in calls)
