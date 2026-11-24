"""ONE CANCELED RECALL LANE NEVER FAILS THE SEARCH (2026-11-14).

``rag.recall_vector`` was canceled by the database (SQLSTATE 57014, a cold HNSW walk past the
driver's command timeout) and, because ``search()`` gathers the vector, lexical and entity lanes
with one ``asyncio.gather``, the whole search failed although the other two lanes had answered.
A canceled lane now drops out of the fusion and ``SearchResponse.recall_lane_errors`` names it;
the ORM door still files the cancel as a ``db_statement_canceled`` system error. A search where
EVERY lane was canceled still raises — nothing answered, that is a failure.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from matrx_orm.exceptions import QueryTimeoutError

from matrx_rag import search

_USER = "11111111-1111-4111-8111-111111111111"


def _timeout() -> QueryTimeoutError:
    return QueryTimeoutError(operation="call_function:rag.recall_vector", timeout=30.0)


def _stub(monkeypatch, *, vector, lexical, entity) -> None:
    async def fake_embed(model, texts, *, organization_id):
        return [[0.1, 0.2] for _ in texts]

    monkeypatch.setattr(search, "_embed_query_cached", fake_embed)
    monkeypatch.setattr(search, "spec_for", lambda model: SimpleNamespace(table="rag.embeddings_x"))
    monkeypatch.setattr(search, "_recall_vector_door", vector)
    monkeypatch.setattr(search, "_recall_lexical_door", lexical)
    monkeypatch.setattr(search, "_recall_entity_door", entity)


async def _search():
    return await search.search(
        "quarterly plan",
        user_id=_USER,
        embedding_models=["m"],
        rerank=False,
        record_audit=False,
        include_entity_map=False,
        readable=search.ReadableDocuments(user_id=_USER, processed_document_ids=()),
    )


async def test_a_canceled_vector_lane_degrades_the_search_and_says_so(monkeypatch):
    async def vector(*_a, **_kw):
        raise _timeout()

    async def lexical(*_a, **_kw):
        return []

    async def entity(*_a, **_kw):
        return [], [], []

    _stub(monkeypatch, vector=vector, lexical=lexical, entity=entity)
    response = await _search()
    assert set(response.recall_lane_errors) == {"vector"}
    assert "timed out" in response.recall_lane_errors["vector"]
    assert response.vector_candidates == 0
    # A lane that never answered might have found something: never "definitively nothing".
    assert response.relevance_verdict == search.RELEVANCE_VERDICT_UNSCORED


async def test_every_lane_answering_reports_no_lane_errors(monkeypatch):
    async def vector(*_a, **_kw):
        return []

    async def lexical(*_a, **_kw):
        return []

    async def entity(*_a, **_kw):
        return [], [], []

    _stub(monkeypatch, vector=vector, lexical=lexical, entity=entity)
    response = await _search()
    assert response.recall_lane_errors == {}
    assert response.relevance_verdict == search.RELEVANCE_VERDICT_NONE


async def test_every_lane_canceled_still_fails(monkeypatch):
    async def canceled(*_a, **_kw):
        raise _timeout()

    _stub(monkeypatch, vector=canceled, lexical=canceled, entity=canceled)
    with pytest.raises(QueryTimeoutError):
        await _search()


async def test_a_lane_error_that_is_not_a_cancel_still_fails_the_search(monkeypatch):
    async def broken(*_a, **_kw):
        raise RuntimeError("rag.recall_vector: not a rag embedding table")

    async def lexical(*_a, **_kw):
        return []

    async def entity(*_a, **_kw):
        return [], [], []

    _stub(monkeypatch, vector=broken, lexical=lexical, entity=entity)
    with pytest.raises(RuntimeError, match="not a rag embedding table"):
        await _search()
