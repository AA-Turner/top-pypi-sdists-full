from decimal import Decimal

from agentic_devtools.ai_providers.tier_selector import _Candidate, _candidate_values


def test_candidate_values_handles_empty_tiers_and_marginal_escalation() -> None:
    first = _Candidate("first", "tier-1", Decimal("10"), "USD", Decimal("0"))
    next_model = _Candidate("next", "tier-2", Decimal("1"), "USD", Decimal("1"))
    assert _candidate_values([], 0, 1) == (Decimal("0"), [])
    assert _candidate_values([first], 0, 0) == (Decimal("0"), [])
    assert _candidate_values([next_model], 0, 1)[1][0].model_id == "next"
    assert _candidate_values([first], 0, 1)[1][0].model_id == "first"
    assert _candidate_values([first], 1, 1) == (Decimal("0"), [])
    assert _candidate_values([first, next_model], 0, 1)[1][0].model_id == "next"


def test_candidate_values_tie_breaks_by_cost_and_model_id() -> None:
    candidates = [
        _Candidate("z-model", "tier-1", Decimal("1"), "USD", Decimal("1")),
        _Candidate("a-model", "tier-1", Decimal("1"), "USD", Decimal("1")),
    ]
    assert _candidate_values(candidates, 0, 1)[1][0].model_id == "a-model"
