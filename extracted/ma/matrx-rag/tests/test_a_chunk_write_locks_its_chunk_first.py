"""A chunk's entity write takes the chunk first, the order a re-ingest's cascade takes (40P01).

Live 2026-10-30..11-06: 38 deadlocks on rag.kg_edges, rag.kg_chunk_entities and rag.kg_chunks.
A re-ingest deletes a chunk and cascades into its mentions and edges; NER deleted those rows,
then wrote new ones whose foreign key needs the chunk. Opposite orders, so Postgres killed one.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_rag import ner


class _Query:
    def __init__(self, log: list[str], name: str) -> None:
        self.log = log
        self.name = name
        self.lock: str | None = None

    def select_for_update(self, *, mode: str) -> _Query:
        self.lock = mode
        return self

    async def values(self, *_fields: str) -> list[dict[str, Any]]:
        self.log.append(f"read {self.name}" + (f" FOR {self.lock}" if self.lock else ""))
        return [{"entity_id": "e-1"}] if self.name == "KgChunkEntities" else []


def _model(log: list[str], name: str) -> type:
    class Model:
        @classmethod
        def filter(cls, **_: Any) -> _Query:
            return _Query(log, name)

        @classmethod
        async def delete_where(cls, **_: Any) -> int:
            log.append(f"delete {name}")
            return 1

    return Model


async def test_the_chunk_is_locked_before_anything_under_it(monkeypatch: pytest.MonkeyPatch) -> None:
    log: list[str] = []
    monkeypatch.setattr(ner, "get_db_model", lambda name: _model(log, name))

    previous = await ner._replace_chunk_writes("c-1")

    assert log[0] == "read KgChunks FOR KEY SHARE"
    assert "delete KgChunkEntities" in log
    assert "delete KgEdges" in log
    assert previous == {"e-1"}
