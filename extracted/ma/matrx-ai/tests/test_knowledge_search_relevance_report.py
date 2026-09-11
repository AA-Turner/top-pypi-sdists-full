"""Guard: `knowledge_search` states what the relevance gate concluded.

The engine gates hits on a calibrated cross-encoder floor
(`matrx_rag.search.RELEVANCE_FLOOR`), so an empty `hits` list is frequently a
real answer — "the corpus has nothing for this query" — and not a malfunction.
An agent that cannot tell those apart re-issues the same call; `knowledge_compare`
did it 19 times in one turn on the live platform before the floor existed
(feedback 2985b3aa). `knowledge_search` is the hub tool of the family, so it
carries the same contract.

No DB and no RAG backend: the host injects `rag_search` through the
`matrx_ai.configure` seam, which is exactly the seam these tests drive.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from matrx_ai.tools.implementations.rag import knowledge_search


@dataclass
class _Resp:
    query: str = "q"
    hits: list[Any] = field(default_factory=list)
    total_candidates: int = 0
    embedding_model: str = "voyage-4-large"
    reranker_model: str | None = "rerank-v4.0-pro"
    latency_ms: int = 11
    matched_entities: list[str] = field(default_factory=list)
    entity_map: list[Any] = field(default_factory=list)
    relevance_verdict: str = "scored"
    relevance_floor: float | None = 0.45
    below_floor_dropped: int = 0


@dataclass
class _Hit:
    chunk_id: str = "c1"
    source_kind: str = "cld_file"
    source_id: str = "s1"
    content_text: str = "def parse_signal(raw): ..."
    score: float = 0.93
    vector_rank: int | None = 1
    lexical_rank: int | None = None
    rerank_score: float | None = 0.93
    metadata: dict[str, Any] = field(default_factory=dict)
    entities: list[str] = field(default_factory=list)
    entity_rank: int | None = None
    processed_document_id: str | None = None
    primary_page_id: str | None = None
    page_numbers: list[int] = field(default_factory=list)
    derivation_kind: str = "initial_extract"


class _Ctx:
    user_id = "a4955b5c-d524-4d72-a90e-0658d5d51148"
    organization_id = "80ad3283-ea87-4e83-9cee-7b2f2404472c"
    call_id = "guard"


@pytest.fixture
def inject(monkeypatch):
    """Install a fake rag_search through the real configure seam."""

    def _install(resp: Any) -> Any:
        import matrx_ai._ext as ext

        async def _fake(query: str, **_kwargs: Any):
            if hasattr(resp, "query"):
                resp.query = query
            return resp

        monkeypatch.setattr(ext, "get_ext", lambda name: _fake if name == "rag_search" else None)
        return resp

    return _install


async def test_no_relevant_matches_is_a_stated_answer(inject):
    inject(
        _Resp(
            hits=[],
            total_candidates=122,
            relevance_verdict="no_relevant_matches",
            below_floor_dropped=4,
        )
    )
    res = await knowledge_search({"query": "parse_signal"}, _Ctx())
    assert res.success is True
    out = res.output
    assert out["hits"] == []
    assert out["no_relevant_matches"] is True
    assert out["relevance_verdict"] == "no_relevant_matches"
    assert out["relevance_floor"] == 0.45
    assert out["below_floor_dropped"] == 4
    # The floor, the candidate count, and the stop-instruction are all stated.
    assert "0.45" in out["note"]
    assert "122" in out["note"]
    assert "Do NOT repeat this query" in out["note"]


async def test_relevant_hits_carry_the_verdict_without_a_scolding(inject):
    inject(_Resp(hits=[_Hit()], total_candidates=107, relevance_verdict="scored"))
    res = await knowledge_search({"query": "parse_signal"}, _Ctx())
    out = res.output
    assert len(out["hits"]) == 1
    assert out["relevance_verdict"] == "scored"
    assert "no_relevant_matches" not in out
    assert "note" not in out


async def test_unscored_hits_announce_that_no_floor_was_applied(inject):
    inject(
        _Resp(
            hits=[_Hit()],
            total_candidates=107,
            reranker_model=None,
            relevance_verdict="unscored",
            relevance_floor=None,
        )
    )
    res = await knowledge_search({"query": "parse_signal"}, _Ctx())
    out = res.output
    assert out["hits"]
    assert out["relevance_verdict"] == "unscored"
    assert out["relevance_floor"] is None
    assert "NOT relevance-scored" in out["note"]


async def test_empty_with_no_candidates_points_at_the_index(inject):
    """Recall found nothing at all — a different story from "nothing relevant"."""
    inject(_Resp(hits=[], total_candidates=0, relevance_verdict="no_relevant_matches"))
    res = await knowledge_search({"query": "zzz"}, _Ctx())
    assert res.output["no_relevant_matches"] is True
    assert "0.45" in res.output["note"]


async def test_engine_without_the_contract_degrades_to_unscored(inject):
    """An older/injected backend that lacks the fields must not crash the tool.

    The package is host-agnostic: a consumer can inject any `rag_search`. A
    missing verdict is "we did not judge", never a false all-clear.
    """

    @dataclass
    class _Bare:
        query: str = "q"
        hits: list[Any] = field(default_factory=list)
        total_candidates: int = 0
        embedding_model: str = "m"
        reranker_model: str | None = None
        latency_ms: int = 1

    inject(_Bare())
    res = await knowledge_search({"query": "q"}, _Ctx())
    assert res.success is True
    assert res.output["relevance_verdict"] == "unscored"
    assert res.output["relevance_floor"] is None
