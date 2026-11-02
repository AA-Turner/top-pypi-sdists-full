"""Guard: the relevance floor — retrieval never dresses up irrelevant chunks.

The defect this locks (feedback 2985b3aa): ``search()`` ranked candidates but
never asked whether the best one was actually ABOUT the query, so an
out-of-domain question came back with the top-k of whatever corpus the caller
could see, as a success. Live evidence, 2026-09-03: a Telegram/MEXC trading-bot
codebase query ("parse_signal") answered with NIST/CISA cybersecurity PDF
chunks; the calling agent re-issued the identical call 19 times in one turn
because every useless result looked exactly like a useful one.

These are pure-code tests over the gate helper plus the wiring invariants that
keep the gate reachable. The live before/after proof is in the feedback item.
"""

from __future__ import annotations

import inspect

from matrx_utils.source_guard import stable_source

from matrx_rag.search import (
    RELEVANCE_FLOOR,
    RELEVANCE_VERDICT_NONE,
    RELEVANCE_VERDICT_SCORED,
    RELEVANCE_VERDICT_UNSCORED,
    RERANK_CONFIDENCE_FLOOR,
    SearchResponse,
    _apply_relevance_floor,
    search,
)

# Real cross-encoder scores measured against the live corpus on 2026-09-09
# (rerank-v4.0-pro) — the numbers RELEVANCE_FLOOR was calibrated on.
LIVE_OUT_OF_DOMAIN = {
    # "parse_signal" (trading-bot code) vs the NIST/CISA library corpus
    "nist_a": 0.364416,
    "nist_b": 0.360804,
    "nist_c": 0.342990,
    "nist_d": 0.342990,
}
LIVE_OUT_OF_DOMAIN_FAR = {
    # "telegram_worker.py main loop message ingestion" vs the same corpus —
    # so weak the reranker itself reported low confidence, and the old code
    # returned these four anyway, in fused order.
    "nist_e": 0.016393,
    "nist_f": 0.016129,
    "nist_g": 0.015873,
    "nist_h": 0.015625,
}
LIVE_IN_DOMAIN = {
    # "parse_signal" vs the trading-bot case corpus (exclude_library)
    "code_a": 0.935958,
    "code_b": 0.933334,
    "code_c": 0.906562,
    "code_d": 0.900827,
}


class TestFloorCalibration:
    def test_floor_sits_between_the_live_bands(self):
        """The floor separates the measured out-of-domain and in-domain bands.

        If a future tune breaks this, it is silently re-enabling the defect
        (floor too low) or throwing away real answers (floor too high).
        """
        worst_in_domain = min(LIVE_IN_DOMAIN.values())
        best_out_of_domain = max(LIVE_OUT_OF_DOMAIN.values())
        assert best_out_of_domain < RELEVANCE_FLOOR < worst_in_domain

    def test_honesty_floor_is_stricter_than_the_ordering_floor(self):
        """RERANK_CONFIDENCE_FLOOR only chose an ORDER; it never gated output.

        The live out-of-domain NIST hits scored 0.34-0.36 — comfortably ABOVE
        0.25 — so the old "low confidence" branch never even fired for them.
        Anything the ordering floor distrusts must also fail the honesty floor.
        """
        assert RELEVANCE_FLOOR > RERANK_CONFIDENCE_FLOOR


class TestOutOfDomainIsHonestlyEmpty:
    def test_live_out_of_domain_scores_yield_no_hits(self):
        ordered = list(LIVE_OUT_OF_DOMAIN)
        kept, verdict, floor, dropped = _apply_relevance_floor(
            ordered, LIVE_OUT_OF_DOMAIN, floor=RELEVANCE_FLOOR, limit=4
        )
        assert kept == []
        assert verdict == RELEVANCE_VERDICT_NONE
        assert floor == RELEVANCE_FLOOR
        # The count of garbage hits the old code returned as a success.
        assert dropped == 4

    def test_reranker_low_confidence_case_is_also_empty(self):
        """The case the engine already DETECTED and still answered anyway."""
        ordered = list(LIVE_OUT_OF_DOMAIN_FAR)
        kept, verdict, _floor, dropped = _apply_relevance_floor(
            ordered, LIVE_OUT_OF_DOMAIN_FAR, floor=RELEVANCE_FLOOR, limit=4
        )
        assert kept == []
        assert verdict == RELEVANCE_VERDICT_NONE
        assert dropped == 4

    def test_verdict_is_not_an_error_state(self):
        """ "No relevant matches" is an ANSWER. It must never read as failure."""
        _kept, verdict, _floor, _dropped = _apply_relevance_floor(
            ["x"], {"x": 0.01}, floor=RELEVANCE_FLOOR, limit=4
        )
        assert verdict == RELEVANCE_VERDICT_NONE
        assert verdict != RELEVANCE_VERDICT_UNSCORED


class TestInDomainStillReturnsHits:
    def test_live_in_domain_scores_all_survive(self):
        ordered = list(LIVE_IN_DOMAIN)
        kept, verdict, floor, dropped = _apply_relevance_floor(
            ordered, LIVE_IN_DOMAIN, floor=RELEVANCE_FLOOR, limit=4
        )
        assert kept == ordered
        assert verdict == RELEVANCE_VERDICT_SCORED
        assert floor == RELEVANCE_FLOOR
        assert dropped == 0

    def test_order_is_preserved_not_resorted(self):
        """The gate FILTERS. Ranking decisions were already made upstream."""
        scores = {"a": 0.9, "b": 0.1, "c": 0.5, "d": 0.95}
        kept, _v, _f, _d = _apply_relevance_floor(
            ["a", "b", "c", "d"], scores, floor=RELEVANCE_FLOOR, limit=4
        )
        assert kept == ["a", "c", "d"]

    def test_mixed_band_keeps_only_the_relevant_half(self):
        scores = {**LIVE_IN_DOMAIN, **LIVE_OUT_OF_DOMAIN}
        ordered = list(LIVE_IN_DOMAIN) + list(LIVE_OUT_OF_DOMAIN)
        kept, verdict, _f, dropped = _apply_relevance_floor(
            ordered, scores, floor=RELEVANCE_FLOOR, limit=8
        )
        assert kept == list(LIVE_IN_DOMAIN)
        assert verdict == RELEVANCE_VERDICT_SCORED
        assert dropped == 4


class TestUnscoredNeverPretends:
    def test_no_cross_encoder_scores_is_a_stated_no_op(self):
        """No Cohere key / rerank=False / rerank errored.

        Relevance could not be judged, so the gate must NOT filter — and must
        NOT claim the survivors were vetted. "Nothing fails silently" cuts both
        ways: a gate that quietly skipped is as dishonest as one that lies.
        """
        ordered = ["a", "b", "c"]
        kept, verdict, floor, dropped = _apply_relevance_floor(
            ordered, {}, floor=RELEVANCE_FLOOR, limit=3
        )
        assert kept == ordered
        assert verdict == RELEVANCE_VERDICT_UNSCORED
        assert floor is None
        assert dropped == 0

    def test_zero_floor_returns_everything_and_still_reports_scored(self):
        """The knob's permissive end stays honest about what it did."""
        scores = dict(LIVE_OUT_OF_DOMAIN)
        kept, verdict, floor, _d = _apply_relevance_floor(list(scores), scores, floor=0.0, limit=4)
        assert kept == list(scores)
        assert verdict == RELEVANCE_VERDICT_SCORED
        assert floor == 0.0


class TestWiringInvariants:
    """The gate is only worth anything if it stays ON the output path."""

    def test_search_exposes_the_floor_as_a_per_call_knob(self):
        assert "relevance_floor" in inspect.signature(search).parameters

    def test_response_carries_the_verdict_contract(self):
        fields = SearchResponse.__dataclass_fields__
        for name in ("relevance_verdict", "relevance_floor", "below_floor_dropped"):
            assert name in fields, f"SearchResponse lost {name}"
        # Default must be the "we did not judge" state, never a false all-clear.
        assert fields["relevance_verdict"].default == RELEVANCE_VERDICT_UNSCORED

    def test_gate_runs_before_hits_are_built(self):
        """Order matters: filtering AFTER hydration would still emit the junk.

        Asserted structurally because the alternative — a full live search —
        cannot run in a no-DB unit suite, and a mocked pipeline would only test
        the mock.
        """
        src = stable_source(search)
        gate_at = src.index("_apply_relevance_floor(\n")
        hits_at = src.index("hits: list[SearchHit] = [_hit_for(")
        assert gate_at < hits_at
        # The fused preview (on_fused) is the one deliberate pre-gate emission: it is
        # superseded by the gated, reranked result the same search returns.

    def test_raw_cross_encoder_scores_survive_the_low_confidence_branch(self):
        """relevance_scores must NOT be cleared with rerank_scores.

        Clearing both is what made "we won't trust this ordering" mean "ship it
        anyway": the gate would see no scores and fall through to `unscored`.
        """
        src = stable_source(search)
        low_conf = src.index('rerank_status = "low_confidence"')
        window = src[low_conf - 600 : low_conf + 200]
        assert "rerank_scores = {}" in window
        assert "relevance_scores = {}" not in window


def test_the_fused_preview_is_offered_before_the_cross_encoder_runs():
    """on_fused hands a streaming caller the fused order BEFORE rerank (Knowledge Hub H1);
    after the rerank call it would be no earlier than the final answer."""
    src = stable_source(search)
    preview_at = src.index("await on_fused(")
    rerank_at = src.index("await reranker.rerank(")
    assert preview_at < rerank_at
