"""Phase 2c — HyDE-blended RRF tests.

Direct unit tests for the two new pieces (no DB):

* ``hyde_passage(query)`` returns the injected LLM's output or "" on
  failure (silent fallback so search degrades gracefully).
* ``_rrf_fuse(..., ranking_weights={...})`` weights HyDE rankings at the
  configured fraction so a candidate that ONLY appears in the HyDE
  ranking can't out-rank a candidate that appears highly in the raw
  query ranking.

The integration path (embed → vector_recall → _rrf_fuse) is exercised
indirectly via the weight contract: as long as _rrf_fuse honors the
weight, the search wiring (which only adds a ``#hyde`` key) is
self-evidently correct.
"""

from __future__ import annotations

import asyncio


def test_rrf_fuse_default_weights_match_unweighted():
    """Calling _rrf_fuse without ranking_weights matches the pre-weight
    behavior. Guards backward compatibility for any caller that hasn't
    opted into weighting."""
    from matrx_rag.search import _rrf_fuse

    rankings = {"m#v0": ["a", "b", "c"], "m#v1": ["c", "a", "d"]}
    lexical = ["b", "d", "a"]

    out_default = _rrf_fuse(rankings, lexical)
    out_explicit_ones = _rrf_fuse(
        rankings,
        lexical,
        ranking_weights={k: 1.0 for k in rankings},
        lexical_weight=1.0,
    )
    assert out_default == out_explicit_ones


def test_rrf_fuse_hyde_weight_demotes_hyde_only_candidates():
    """A candidate that appears ONLY in a HyDE ranking (weight 0.3) is
    demoted relative to a candidate that appears highly in the raw
    query ranking (weight 1.0)."""
    from matrx_rag.search import _rrf_fuse

    # raw-query vector ranking puts "real" at rank 5 (low contribution
    # at RRF_K=60 → 1/65 ≈ 0.0154).
    real_ranking = ["x1", "x2", "x3", "x4", "real"]
    # HyDE ranking puts "fake" at rank 1 (top contribution at full
    # weight would be 1/61 ≈ 0.0164; at 0.3 weight → 0.00492).
    hyde_ranking = ["fake", "y2", "y3"]

    weights = {"m#v0": 1.0, "m#v1#hyde": 0.3}
    fused = _rrf_fuse(
        {"m#v0": real_ranking, "m#v1#hyde": hyde_ranking},
        lexical_ranking=[],
        ranking_weights=weights,
    )
    fused_map = dict(fused)
    assert fused_map["real"] > fused_map["fake"], (
        "real query rank-5 should out-score HyDE rank-1 at the 0.3 weight: "
        f"real={fused_map['real']:.6f} fake={fused_map['fake']:.6f}"
    )


def test_rrf_fuse_hyde_weight_boosts_when_seen_by_both():
    """When the same candidate appears in BOTH the raw and HyDE rankings,
    HyDE contributes its share — so the fused score is strictly greater
    than the raw-only score (HyDE acts as a tiebreaker / amplifier)."""
    from matrx_rag.search import _rrf_fuse

    raw_only = _rrf_fuse(
        {"m#v0": ["a", "b", "c"]},
        lexical_ranking=[],
    )
    with_hyde = _rrf_fuse(
        {"m#v0": ["a", "b", "c"], "m#v1#hyde": ["b", "a", "c"]},
        lexical_ranking=[],
        ranking_weights={"m#v0": 1.0, "m#v1#hyde": 0.3},
    )
    raw_map = dict(raw_only)
    hyde_map = dict(with_hyde)
    for cid in ("a", "b", "c"):
        assert hyde_map[cid] > raw_map[cid], (
            f"HyDE-blended score for {cid} should exceed raw-only: "
            f"raw={raw_map[cid]:.6f} blended={hyde_map[cid]:.6f}"
        )


def test_hyde_weight_is_a_code_constant(monkeypatch):
    """The HyDE blend weight is a CODE constant, tuned via code push — not an
    env var. The ``RAG_HYDE_RRF_WEIGHT`` env override was deliberately removed
    from the prod path (silent-env-var eradication); ``_hyde_rrf_weight()`` must
    return ``HYDE_RRF_WEIGHT_DEFAULT`` regardless of the environment so a stray
    env var can never silently re-tune retrieval."""
    from matrx_rag import search

    assert search._hyde_rrf_weight() == search.HYDE_RRF_WEIGHT_DEFAULT

    monkeypatch.setenv("RAG_HYDE_RRF_WEIGHT", "0.5")
    assert search._hyde_rrf_weight() == search.HYDE_RRF_WEIGHT_DEFAULT

    monkeypatch.delenv("RAG_HYDE_RRF_WEIGHT", raising=False)
    assert search._hyde_rrf_weight() == search.HYDE_RRF_WEIGHT_DEFAULT


def test_hyde_passage_uses_injected_runner():
    """hyde_passage routes through the injected RagAgentRunner — the ONLY path
    (there is no raw-provider fallback) — and returns its stripped text."""
    import matrx_rag
    from matrx_rag.llm import hyde_passage

    captured: dict[str, object] = {}

    class _StubRunner:
        async def hyde(self, query, *, timeout=None):
            captured["query"] = query
            captured["timeout"] = timeout
            return "  A short hypothetical answer.  "

    matrx_rag._ext._reset_for_tests()
    matrx_rag.configure(rag_agent_runner=_StubRunner())

    out = asyncio.run(hyde_passage("what is X?"))
    assert out == "A short hypothetical answer."
    assert captured["query"] == "what is X?"


def test_hyde_passage_returns_empty_on_failure():
    """On runner failure, hyde_passage returns "" so the search silently falls
    back to raw-query embedding (no user-visible error)."""
    import matrx_rag
    from matrx_rag.llm import hyde_passage

    class _ExplodingRunner:
        async def hyde(self, query, *, timeout=None):
            raise RuntimeError("simulated agent outage")

    matrx_rag._ext._reset_for_tests()
    matrx_rag.configure(rag_agent_runner=_ExplodingRunner())

    out = asyncio.run(hyde_passage("any query"))
    assert out == ""


def test_hyde_passage_skips_empty_query():
    """An empty query short-circuits to "" BEFORE the runner requirement — no
    runner needed, no agent call wasted."""
    import matrx_rag
    from matrx_rag.llm import hyde_passage

    class _ShouldNotBeCalled:
        async def hyde(self, query, *, timeout=None):
            raise AssertionError("runner was called for empty query")

    matrx_rag._ext._reset_for_tests()
    matrx_rag.configure(rag_agent_runner=_ShouldNotBeCalled())

    assert asyncio.run(hyde_passage("")) == ""
    assert asyncio.run(hyde_passage("   ")) == ""
