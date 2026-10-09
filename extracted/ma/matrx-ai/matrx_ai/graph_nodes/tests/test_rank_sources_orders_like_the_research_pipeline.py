"""``ai.search.rank_sources`` orders results with the research pipeline's own score.

Gap (b) of the 2026-10-07 Deep Research comparison: the workflow scraped search
results in raw engine order; the code path reads best-first by the pre-read score
(rank prominence x breadth x authority). Both now call ONE algorithm
(``matrx_ai.search_ranking``)."""

from __future__ import annotations

import pytest

from matrx_ai.graph_nodes import register_with_graph
from matrx_ai.graph_nodes.search_action import (
    RankSourcesInput,
    ai_search_rank_sources,
    rank_sources,
)
from matrx_ai.graph_nodes.tests.test_node_handlers_execute import _ctx
from matrx_ai.search_ranking import KeywordRanking, compute_pre_read_score

register_with_graph()


def test_authority_lifts_a_lower_ranked_trusted_source() -> None:
    results = [
        {"url": "https://spam.example/a", "rank": 1},
        {"url": "https://www.nih.gov/b", "rank": 3},
    ]
    ranked = rank_sources(results, {"nih.gov": 95, "spam.example": 5}, None)
    assert [r["url"] for r in ranked] == ["https://www.nih.gov/b", "https://spam.example/a"]
    expected = compute_pre_read_score([KeywordRanking("", 1.0, 3)], 1.0, 95).pre_read_score
    assert ranked[0]["pre_read_score"] == pytest.approx(expected, abs=1e-3)


def test_breadth_across_queries_beats_a_single_hit_and_dedupes() -> None:
    results = [
        {"url": "https://one.example/x", "rank": 2, "query": "k1"},
        {"url": "https://broad.example/y", "rank": 4, "query": "k1"},
        {"url": "https://broad.example/y", "rank": 4, "query": "k2"},
        {"url": "https://broad.example/y", "rank": 4, "query": "k3"},
    ]
    ranked = rank_sources(results, {}, None)
    assert [r["url"] for r in ranked] == ["https://broad.example/y", "https://one.example/x"]


@pytest.mark.asyncio
async def test_node_keeps_the_best_n_and_lists_their_urls() -> None:
    res = await ai_search_rank_sources(
        _ctx(),
        RankSourcesInput(results=[{"url": f"https://e{i}.com", "rank": i} for i in range(1, 6)], limit=2),
    )
    assert res.result.urls == ["https://e1.com", "https://e2.com"]
