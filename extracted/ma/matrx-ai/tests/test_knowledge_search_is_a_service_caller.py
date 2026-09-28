"""knowledge_search is a caller of the one Knowledge search service — backward compatible.

Old fields map onto the query (data_store_id → within data_store, source_ids → within
source, scopes → within scope; rerank/mmr/multi-query/HyDE → the passage lane), the
Knowledge Hub fields pass through, the typed sections ride beside the old `hits`, and the
citations still come from the raw passage response.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from matrx_ai.tools.implementations.rag import knowledge_search


@dataclass
class _Hit:
    chunk_id: str = "chunk-1"
    source_kind: str = "cld_file"
    source_id: str = "f1"
    content_text: str = "the grant budget is 40k"
    score: float = 0.9
    processed_document_id: str | None = "d1"
    page_numbers: list[int] = field(default_factory=lambda: [3])


@dataclass
class _Resp:
    query: str = "grant"
    hits: list[Any] = field(default_factory=lambda: [_Hit()])
    total_candidates: int = 1
    relevance_verdict: str = "relevant"


class _Ctx:
    user_id = "00000000-0000-4000-8000-0000000fffa3"
    organization_id = "80ad3283-ea87-4e83-9cee-7b2f2404472c"
    conversation_id = "c0ffee00-0000-4000-8000-000000000001"
    call_id = "call_1"


@pytest.fixture
def service(monkeypatch):
    import matrx_ai._ext as ext

    seen: dict[str, Any] = {}

    async def _service(**kw):
        seen.update(kw)
        payload = {
            "sections": [
                {"type": "section", "section": "notes", "count": 1, "items": [{"entity": "note", "id": "n1", "title": "grant"}]},
                {"type": "section", "section": "segments", "count": 1, "items": []},
                {"type": "section", "section": "chats", "withheld": "Chats are private to their owner…", "items": []},
            ],
            "errors": [{"type": "section_error", "section": "sources", "message": "Item search is not available…"}],
            "chips": [],
        }
        return payload, _Resp()

    registry = {"knowledge_search_service": _service}
    monkeypatch.setattr(ext, "get_ext", lambda name: registry[name])
    monkeypatch.setattr(ext, "has_ext", lambda name: name in registry)
    return seen


async def test_old_fields_map_onto_the_one_query(service):
    res = await knowledge_search(
        {
            "query": "grant",
            "data_store_id": "ds1",
            "source_ids": ["f1"],
            "scope_ids": ["s1"],
            "rerank": False,
            "use_mmr": False,
            "multi_query": 3,
            "use_hyde": True,
            "limit": 7,
        },
        _Ctx(),
    )
    assert res.success, res.error
    q = service["query"]
    assert q["text"] == "grant" and q["limit"] == 7
    assert {"type": "scope", "id": "s1"} in q["within"]
    assert {"type": "data_store", "id": "ds1"} in q["within"]
    assert {"type": "source", "id": "f1"} in q["within"]
    opts = service["segment_options"]
    assert opts["rerank"] is False and opts["use_mmr"] is False
    assert opts["multi_query"] == 3 and opts["use_hyde"] is True
    assert service["conversation_id"] == _Ctx.conversation_id


async def test_hub_fields_pass_through_and_sections_ride_beside_the_cited_hits(service):
    res = await knowledge_search(
        {"query": "grant", "types": ["note", "processed_document"], "sort": "recent", "scope_ids": []}, _Ctx()
    )
    assert res.success
    assert service["query"]["types"] == ["note", "processed_document"]
    assert service["query"]["sort"] == "recent"
    out = res.output
    assert [h["chunk_id"] for h in out["hits"]] == ["chunk-1"]
    names = [s["section"] for s in out["sections"]]
    assert "segments" not in names and "notes" in names
    assert any(s.get("withheld") for s in out["sections"] if s["section"] == "chats")
    assert out["section_errors"][0]["section"] == "sources"
    # Citations still come from the raw passage response.
    assert res.provider_content


async def test_a_failed_passage_lane_is_a_failed_call(monkeypatch):
    import matrx_ai._ext as ext

    async def _service(**kw):
        return {"sections": [], "errors": [{"section": "segments", "message": "The passage search failed (X)"}]}, None

    registry = {"knowledge_search_service": _service}
    monkeypatch.setattr(ext, "get_ext", lambda name: registry[name])
    monkeypatch.setattr(ext, "has_ext", lambda name: name in registry)
    res = await knowledge_search({"query": "grant", "scope_ids": []}, _Ctx())
    assert res.success is False and "passage search failed" in res.error.message


async def test_the_model_sees_every_section_not_only_the_hits(service):
    res = await knowledge_search({"query": "grant", "scope_ids": []}, _Ctx())
    texts = [getattr(b, "text", "") for b in res.provider_content]
    rendering = next(t for t in texts if t.startswith("Every section of this search"))
    assert "Segments (1): the citable passages above" in rendering
    assert "- segment chunk-1" in rendering
    assert "Notes (1):" in rendering and "- note n1 — grant" in rendering
    assert "Chats: withheld — Chats are private" in rendering
    assert "Sources: could not be searched — Item search is not available" in rendering
