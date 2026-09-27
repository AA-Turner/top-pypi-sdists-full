"""`knowledge_search` bounds the metadata it rides beside its citable passages.

Production (2026-09-01, call_01a05def…): ``limit=50`` → 101,798 chars. Passages
were already budgeted (MAX_CITABLE_TEXT_CHARS); the trailing metadata block —
every hit's ``metadata``/``entities`` — was not, and because the result is a
typed block list the size gate never measured it (no ops event). The metadata
block is now capped (``cap_search_metadata``) lowest-ranked first, announced,
and the whole model-facing result stays under the soft cap.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

import pytest

from matrx_ai.tools.implementations.rag import knowledge_search
from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS
from matrx_ai.tools.result_gate import (
    _SINKS,
    ToolResultGateEvent,
    apply_size_gate,
    block_text_chars,
    register_tool_result_gate_sink,
)


@dataclass
class _Hit:
    chunk_id: str
    source_kind: str = "library_doc"
    source_id: str = "7aa2cc68-5b6f-4d64-bd84-8831f5e8bd6f"
    content_text: str = ""
    score: float = 0.016
    vector_rank: int | None = 1
    lexical_rank: int | None = None
    rerank_score: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    entities: list[str] = field(default_factory=list)
    entity_rank: int | None = None
    processed_document_id: str | None = None
    primary_page_id: str | None = None
    page_numbers: list[int] = field(default_factory=list)
    derivation_kind: str = "initial_extract"


@dataclass
class _Resp:
    query: str = "q"
    hits: list[Any] = field(default_factory=list)
    total_candidates: int = 50
    embedding_model: str = "voyage-4-large"
    reranker_model: str | None = None
    latency_ms: int = 9762
    matched_entities: list[str] = field(default_factory=list)
    entity_map: list[Any] = field(default_factory=list)
    relevance_verdict: str = "unscored"
    relevance_floor: float | None = None
    below_floor_dropped: int = 0


class _Ctx:
    user_id = "00000000-0000-4000-8000-0000000fffa3"
    organization_id = "80ad3283-ea87-4e83-9cee-7b2f2404472c"
    call_id = "call_01a05def8a1670d3ad8754cb"


def _prod_shape(n: int = 50) -> _Resp:
    meta = {
        "role": "child",
        "source": {
            "kind": "guideline",
            "title": "NIST SP 800-61 Revision 3 — Incident Response Recommendations",
            "version": "2025-04",
            "short_code": "NIST-SP-800-61r3",
            "source_url": "https://doi.org/10.6028/NIST.SP.800-61r3",
            "row_metadata": {"authority": "official", "notes": "n" * 1_200},
        },
        "parent_index": 8,
    }
    hits = [
        _Hit(chunk_id=f"chunk-{i:03d}", content_text=f"passage {i} " + "t" * 1_400, metadata=meta, vector_rank=i + 1)
        for i in range(n)
    ]
    return _Resp(hits=hits)


@pytest.fixture
def inject(monkeypatch):
    def _install(resp: Any) -> None:
        import matrx_ai._ext as ext

        async def _fake(query: str, **_kw: Any):
            resp.query = query
            return resp

        monkeypatch.setattr(ext, "get_ext", lambda name: _fake if name == "rag_search" else None)

    return _install


@pytest.fixture
def gate_events():
    events: list[ToolResultGateEvent] = []
    register_tool_result_gate_sink(events.append)
    yield events
    _SINKS.remove(events.append)


async def test_limit_50_result_stays_under_the_soft_cap_and_says_what_was_trimmed(inject, gate_events):
    inject(_prod_shape())
    res = await knowledge_search({"query": "pypi python codebase analysis", "limit": 50}, _Ctx())
    assert res.success
    blocks = res.provider_content
    assert blocks is not None
    assert block_text_chars(blocks) < TOOL_RESULT_SOFT_CAP_CHARS

    meta = json.loads(blocks[-1].text)
    trimmed = meta["metadata_trimmed"]
    assert trimmed["heavy_fields_removed"] > 0
    assert "smaller limit" in trimmed["note"]
    # Identity stays on every surviving hit.
    assert all("chunk_id" in h and "source_id" in h for h in meta["hits"])

    cd, truncated = apply_size_gate(
        res.to_tool_result_content(),
        output_self_capped=res.output_self_capped,
        tool_name="knowledge_search",
        tool_kind="native",
        conversation_id="c",
        user_id="u",
    )
    assert truncated is False
    assert gate_events == []  # no blocks_over_cap


async def test_lowest_ranked_hits_lose_metadata_first(inject):
    inject(_prod_shape(14))
    res = await knowledge_search({"query": "q", "limit": 14}, _Ctx())
    meta = json.loads(res.provider_content[-1].text)
    assert meta["metadata_trimmed"]["entries_dropped"] == 0
    assert "metadata" in meta["hits"][0]
    assert "metadata" not in meta["hits"][-1]
    assert len(meta["hits"]) == 14


async def test_small_result_metadata_is_untouched(inject):
    inject(_prod_shape(3))
    res = await knowledge_search({"query": "q", "limit": 3}, _Ctx())
    meta = json.loads(res.provider_content[-1].text)
    assert "metadata_trimmed" not in meta
    assert all("metadata" in h for h in meta["hits"])
