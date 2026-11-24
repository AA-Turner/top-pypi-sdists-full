"""`knowledge_search` hands the model a bounded view, live and on resend.

Benchmark P6 (2026-11-02, conversations 34756283 / a4f1287f): twenty calls at limit=3
stored 10k-43k chars each. The passages were ~4.5k; the rest was per-hit indexing
metadata (4-5k per image hit), the entity_map (~9k) and full section JSON (~10k), and
the model was handed most of it — live through the metadata block, and on every resend
(a DB-rebuilt conversation) as the raw stored JSON. Model calls grew from ~32k to ~72k
input tokens; one run hit the 399k guard.

The contract now: each hit is a ranked window around the query's words (ids + title),
sections are one line per item, the whole view fits ``output_budget_chars``, the caps
are knobs (``agents.knowledge_search``), and the stored output stays complete.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

import pytest

from matrx_ai.config.tools_config import ToolResultContent
from matrx_ai.tools.implementations import rag
from matrx_ai.tools.implementations.rag import (
    OUTPUT_BUDGET_CHARS,
    knowledge_search,
    model_view,
    snippet_window,
)
from matrx_ai.tools.result_gate import block_text_chars


@dataclass
class _Hit:
    chunk_id: str
    source_kind: str = "cld_file"
    source_id: str = "7aa2cc68-5b6f-4d64-bd84-8831f5e8bd6f"
    content_text: str = ""
    score: float = 0.9
    vector_rank: int | None = 1
    lexical_rank: int | None = 1
    rerank_score: float | None = 0.9
    metadata: dict[str, Any] = field(default_factory=dict)
    entities: list[str] = field(default_factory=list)
    entity_rank: int | None = 1
    processed_document_id: str | None = "d-1"
    primary_page_id: str | None = "p-1"
    page_numbers: list[int] = field(default_factory=lambda: [1])
    derivation_kind: str = "initial_extract"


@dataclass
class _Entity:
    entity_id: str
    name: str
    kind: str = "concept"
    mention_count: int = 3
    artifact_count: int = 2
    source_kind_counts: dict[str, int] = field(default_factory=lambda: {"cld_file": 2})
    top_chunk_id: str = "c"
    importance: float = 0.5
    is_concept: bool = True
    linked: list[Any] = field(default_factory=list)


@dataclass
class _Resp:
    query: str = "q"
    hits: list[Any] = field(default_factory=list)
    total_candidates: int = 3
    embedding_model: str = "voyage-4-large"
    reranker_model: str | None = "rerank-2.5"
    latency_ms: int = 900
    matched_entities: list[str] = field(default_factory=list)
    entity_map: list[Any] = field(default_factory=list)
    relevance_verdict: str = "relevant"
    relevance_floor: float | None = 0.3
    below_floor_dropped: int = 0


class _Ctx:
    user_id = "00000000-0000-4000-8000-0000000fffa3"
    organization_id = "80ad3283-ea87-4e83-9cee-7b2f2404472c"
    call_id = "call_p6"


def _p6_shape() -> _Resp:
    """The measured P6 shape: 3 hits, heavy image-indexing metadata, a big entity_map."""
    image_meta = {
        "ner": {"engine": "gliner", "version": "gliner2-large@0.3"},
        "role": "leaf",
        "title": "Fir Analytics account notes",
        "image": {"keywords": [f"keyword-{i}" for i in range(120)], "caption": "c" * 1500},
        "row_metadata": {"notes": "n" * 1500},
    }
    filler = "Quarterly review of shipping volumes and staffing. " * 60
    body = filler[:3000] + " Fir Analytics renewal is due in March; the owner is Dana. " + filler[:2000]
    hits = [
        _Hit(chunk_id=f"chunk-{i}", content_text=body, metadata=image_meta, entities=["Fir"] * 10)
        for i in range(3)
    ]
    entity_map = [_Entity(entity_id=f"e-{i}", name=f"Entity {i} " + "x" * 120) for i in range(40)]
    return _Resp(hits=hits, entity_map=entity_map)


@pytest.fixture
def inject(monkeypatch):
    def _install(resp: Any) -> None:
        import matrx_ai._ext as ext

        async def _fake(query: str, **_kw: Any):
            resp.query = query
            return resp

        monkeypatch.setattr(ext, "get_ext", lambda name: _fake if name == "rag_search" else None)
        monkeypatch.setattr(ext, "has_ext", lambda name: False)

    return _install


@pytest.fixture(autouse=True)
def _no_resolver():
    rag.set_knowledge_search_caps_resolver(None)
    yield
    rag.set_knowledge_search_caps_resolver(None)


def test_the_window_holds_the_query_words_buried_deep_in_the_chunk():
    filler = "Quarterly review of shipping volumes and staffing. " * 60
    text = filler[:3000] + " Fir Analytics renewal is due in March. " + filler[:2000]
    win = snippet_window(text, "Fir Analytics renewal", 700)
    assert "Fir Analytics renewal is due in March" in win
    assert len(win) <= 702
    assert win.startswith("…") and win.endswith("…")
    # Short text is returned whole; no query words → the head.
    assert snippet_window("short passage", "x", 700) == "short passage"
    assert snippet_window(text, "zzz", 700).startswith("Quarterly review")


async def test_live_p6_result_is_held_to_the_budget_and_stored_output_stays_complete(inject):
    inject(_p6_shape())
    res = await knowledge_search({"query": "Fir Analytics renewal", "limit": 3}, _Ctx())
    assert res.success
    stored = len(json.dumps(res.output, default=str))
    model = block_text_chars(res.provider_content)
    assert stored > 30_000  # what P6 stored (and used to hand the model most of)
    assert model <= OUTPUT_BUDGET_CHARS + 1_000
    passages = [b for b in res.provider_content if getattr(b, "type", "") == "search_result"]
    assert len(passages) == 3
    assert all("Fir Analytics renewal is due in March" in b.texts[0] for b in passages)
    meta = json.loads(res.provider_content[-1].text)
    assert "entity_map" not in meta
    assert all("metadata" not in h and "entities" not in h for h in meta["hits"])
    assert "knowledge_open" in meta["output_budget"]["read_more"]
    # Stored output keeps everything the UI shows.
    assert res.output["entity_map"] and res.output["hits"][0]["metadata"]
    assert "Fir Analytics renewal" in res.output["hits"][0]["snippet"]
    assert res.output["model_view_caps"] == {
        "snippet_window_chars": rag.SNIPPET_WINDOW_CHARS,
        "output_budget_chars": OUTPUT_BUDGET_CHARS,
    }


async def test_the_caps_are_knobs_read_per_organization(inject):
    seen: list[str | None] = []

    async def _resolver(org: str | None) -> dict[str, int]:
        seen.append(org)
        return {"snippet_window_chars": 200, "output_budget_chars": 1_500}

    rag.set_knowledge_search_caps_resolver(_resolver)
    inject(_p6_shape())
    res = await knowledge_search({"query": "Fir Analytics renewal", "limit": 3}, _Ctx())
    assert seen == [_Ctx.organization_id]
    assert res.output["model_view_caps"] == {"snippet_window_chars": 200, "output_budget_chars": 1_500}
    passages = [b for b in res.provider_content if getattr(b, "type", "") == "search_result"]
    assert all(len(b.texts[0]) <= 202 for b in passages)
    meta = json.loads(res.provider_content[-1].text)
    assert meta["output_budget"]["budget_chars"] == 1_500


async def test_a_failing_knob_read_keeps_the_mirrored_caps(inject):
    async def _broken(org: str | None) -> dict[str, int]:
        raise RuntimeError("knob not registered")

    rag.set_knowledge_search_caps_resolver(_broken)
    inject(_p6_shape())
    res = await knowledge_search({"query": "Fir Analytics renewal", "limit": 3}, _Ctx())
    assert res.success
    assert res.output["model_view_caps"]["output_budget_chars"] == OUTPUT_BUDGET_CHARS


async def test_resend_of_the_stored_output_is_the_same_bounded_view_on_every_provider(inject):
    inject(_p6_shape())
    res = await knowledge_search({"query": "Fir Analytics renewal", "limit": 3}, _Ctx())
    stored = json.loads(json.dumps(res.output, default=str))  # what the DB hands back
    trc = ToolResultContent(tool_use_id="toolu_1", call_id="call_1", name="knowledge_search", content=stored)

    openai_out = trc.to_openai()["output"]
    chat_out = trc.to_openai_chat()["content"]
    google_out = json.dumps(trc.to_google()["functionResponse"]["response"])
    anthropic = trc.to_anthropic()["content"]
    anthropic_chars = sum(len(c.get("text") or "") for b in anthropic for c in b.get("content") or [])
    for size in (len(openai_out), len(chat_out), len(google_out), anthropic_chars):
        assert size <= OUTPUT_BUDGET_CHARS + 1_000, size
    assert "entity_map" not in openai_out and "gliner" not in openai_out
    assert "Fir Analytics renewal is due in March" in openai_out
    # Anthropic stays citable on resend.
    assert sum(1 for b in anthropic if b.get("source", "").startswith("matrx://file/")) == 3


def test_a_budget_smaller_than_the_result_drops_section_lines_then_lowest_hits():
    output = {
        "query": "fir",
        "hits": [
            {"chunk_id": f"c{i}", "source_id": "s", "snippet": "fir " * 300, "metadata": {"title": f"T{i}"}}
            for i in range(6)
        ],
        "sections": [
            {"section": "chats", "count": 30, "items": [{"entity": "conversation", "id": f"x{i}", "title": "chat " * 10} for i in range(30)]}
        ],
    }
    view = model_view(output, window_chars=500, budget_chars=2_500)
    assert len(json.dumps(view)) <= 2_500 + 200
    assert [h["chunk_id"] for h in view["hits"]] == [f"c{i}" for i in range(len(view["hits"]))]
    assert view["output_budget"]["section_lines_dropped"] > 0
    assert view["output_budget"]["hits_dropped"] > 0
    assert output["hits"][0]["snippet"] == "fir " * 300  # input untouched


def test_trimming_sections_keeps_every_section_and_its_best_item():
    """Platform Librarian sweeps agents_workflows / records — the LAST sections. A cut
    from the end of the list would remove them first; the cut takes from the fullest."""
    sections = [
        {"section": name, "count": 25, "items": [{"entity": "x", "id": f"{name}-{i}", "title": "t " * 20} for i in range(25)]}
        for name in ("chats", "projects_tasks", "agents_workflows", "records")
    ]
    output = {"query": "q", "hits": [{"chunk_id": "c0", "source_id": "s", "snippet": "q " * 100}], "sections": sections}
    view = model_view(output, window_chars=500, budget_chars=3_000)
    text = view["sections_text"]
    for name in ("chats", "projects_tasks", "agents_workflows", "records"):
        assert f"{name}-0 " in text, name
    assert view["output_budget"]["section_lines_dropped"] > 0
    assert len(view["hits"]) == 1
