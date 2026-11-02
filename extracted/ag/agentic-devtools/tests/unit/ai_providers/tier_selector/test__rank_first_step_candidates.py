from decimal import Decimal

from agentic_devtools.ai_providers.tier_selector import _Candidate, _rank_first_step_candidates


def test_rank_first_step_candidates_returns_empty_when_no_attempts_left() -> None:
    candidate = _Candidate("a-model", "tier-1", Decimal("1"), "USD", Decimal("1"))
    assert _rank_first_step_candidates([candidate], 0, 0) == []


def test_rank_first_step_candidates_skips_candidates_below_start_tier() -> None:
    low = _Candidate("a-model", "tier-1", Decimal("1"), "USD", Decimal("1"))
    high = _Candidate("b-model", "tier-2", Decimal("2"), "USD", Decimal("1"))
    ranked = _rank_first_step_candidates([low, high], 1, 1)
    assert len(ranked) == 1
    assert ranked[0][1].model_id == "b-model"
