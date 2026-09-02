from decimal import Decimal

import pytest

from agentic_devtools.ai_providers.tier_selector import (
    EXCLUDED_MODELS,
    TIER_LADDER,
    ModelSelection,
    NoSelection,
    select_model_for_dispatch,
)


def _entry(model_id: str, cost: str) -> dict[str, object]:
    output_tokens = int(Decimal(cost) * 1_000_000)
    return {
        "modelId": model_id,
        "surfaces": {
            "copilot": {"modelId": model_id},
            "vscode": {"displayName": model_id},
            "docs": {"displayName": model_id},
        },
        "inputRatePerM": 1,
        "outputRatePerM": 1,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 0,
        "assumedOutputTokens": output_tokens,
        "modelledSessionCost": cost,
        "priceCategory": "standard",
        "provenance": "fixture",
        "costDataAsOf": "2026-08-24T00:00:00+00:00",
    }


def test_select_model_for_dispatch_filters_availability_exclusions_and_rotates() -> None:
    assert sum(len(models) for models in TIER_LADDER.values()) == 7
    assert len(EXCLUDED_MODELS) == 3
    models = {model: _entry(model, "0.10") for tier in TIER_LADDER.values() for model in tier}
    availability = {model: "available" for model in models}
    selection = select_model_for_dispatch(models, availability, ordinal=3)
    assert isinstance(selection, ModelSelection)
    assert selection.model_id == "gpt-5.6-luna"
    assert selection.remaining_attempts == 0


def test_select_model_for_dispatch_reports_budget_exhaustion() -> None:
    model = TIER_LADDER["tier-1"][0]
    models = {model: _entry(model, "0.10")}
    result = select_model_for_dispatch(
        models,
        {model: "available"},
        budget_ceiling=Decimal("0.09"),
    )
    assert isinstance(result, NoSelection)
    assert result.reason == "budget_exhausted"


def test_select_model_for_dispatch_handles_invalid_inputs_and_status_shapes() -> None:
    model = TIER_LADDER["tier-1"][0]
    entry = _entry(model, "0.10")
    assert isinstance(select_model_for_dispatch({}, {model: "available"}), NoSelection)
    with pytest.raises(ValueError):
        select_model_for_dispatch([], {})  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        select_model_for_dispatch({model: entry}, {model: "available"}, ordinal=4)
    with pytest.raises(ValueError):
        select_model_for_dispatch({model: entry}, {model: "available"}, attempted_models=model)
    with pytest.raises(ValueError):
        select_model_for_dispatch(
            {model: entry},
            {model: "available"},
            attempted_models=[],
            attempted_model_ids=[],
        )
    selection = select_model_for_dispatch(
        {model: entry},
        {model: {"status": "available"}},
        next_dispatch_ordinal=3,
        attempted_model_ids=["unknown-model"],
    )
    assert isinstance(selection, ModelSelection)
    attempted_selection = select_model_for_dispatch(
        {model: entry, "gpt-5.6-luna": _entry("gpt-5.6-luna", "0.20")},
        {model: "available", "gpt-5.6-luna": "available"},
        attempted_models=[model],
        ordinal=2,
    )
    assert isinstance(attempted_selection, ModelSelection)
    with pytest.raises(ValueError):
        select_model_for_dispatch(
            {model: entry},
            {model: "available"},
            next_dispatch_ordinal=3,
            attempted_models=[],
            attempted_model_ids=[],
        )


def test_select_model_for_dispatch_fails_closed_for_bad_candidates_and_budget() -> None:
    model = TIER_LADDER["tier-1"][0]
    entry = _entry(model, "0.10")
    bad_entry = dict(entry)
    bad_entry["modelledSessionCost"] = "bad"
    assert isinstance(select_model_for_dispatch({model: bad_entry}, {model: "available"}), NoSelection)
    bad_currency = dict(entry)
    bad_currency["currency"] = ""
    assert isinstance(select_model_for_dispatch({model: bad_currency}, {model: "available"}), NoSelection)
    assert isinstance(
        select_model_for_dispatch(
            {model: entry},
            {model: "available"},
            committed_cost=-1,
        ),
        NoSelection,
    )
    assert isinstance(
        select_model_for_dispatch(
            {model: entry},
            {model: "available"},
            budget_ceiling=-1,
        ),
        NoSelection,
    )
    assert isinstance(select_model_for_dispatch({model: entry}, {model: "rejected"}), NoSelection)
    assert isinstance(select_model_for_dispatch({model: []}, {model: "available"}), NoSelection)
    assert isinstance(
        select_model_for_dispatch(
            {
                model: entry,
                "gpt-5.6-luna": {
                    **entry,
                    "modelId": "gpt-5.6-luna",
                    "surfaces": {
                        "copilot": {"modelId": "gpt-5.6-luna"},
                        "vscode": {"displayName": "gpt-5.6-luna"},
                        "docs": {"displayName": "gpt-5.6-luna"},
                    },
                    "currency": "EUR",
                },
            },
            {model: "available", "gpt-5.6-luna": "available"},
        ),
        NoSelection,
    )


def test_select_model_for_dispatch_handles_invalid_prior_and_fitting_budget() -> None:
    model = TIER_LADDER["tier-1"][0]
    entry = _entry(model, "0.10")
    assert isinstance(
        select_model_for_dispatch(
            {model: entry},
            {model: "available"},
            model_overrides={model: "invalid"},
        ),
        NoSelection,
    )
    selection = select_model_for_dispatch(
        {model: entry},
        {model: "available"},
        budget_ceiling=Decimal("0.10"),
    )
    assert isinstance(selection, ModelSelection)
    assert selection.expected_cost == Decimal("0.10")
    two_models = {
        model: _entry(model, "0.20"),
        "gpt-5.6-luna": _entry("gpt-5.6-luna", "0.10"),
    }
    fitting = select_model_for_dispatch(
        two_models,
        {model: "available", "gpt-5.6-luna": "available"},
        model_overrides={model: 1, "gpt-5.6-luna": 0},
        budget_ceiling=Decimal("0.15"),
    )
    assert isinstance(fitting, ModelSelection)
    assert fitting.model_id == "gpt-5.6-luna"


def test_select_model_for_dispatch_budget_fallback_considers_all_first_step_candidates() -> None:
    expensive = TIER_LADDER["tier-1"][0]
    cheap = TIER_LADDER["tier-1"][1]
    models = {
        expensive: _entry(expensive, "0.20"),
        cheap: _entry(cheap, "0.10"),
        TIER_LADDER["tier-2"][0]: _entry(TIER_LADDER["tier-2"][0], "1.00"),
    }
    availability = {model_id: "available" for model_id in models}
    result = select_model_for_dispatch(
        models,
        availability,
        budget_ceiling=Decimal("0.15"),
        model_overrides={
            expensive: Decimal("0.95"),
            cheap: Decimal("0.10"),
            TIER_LADDER["tier-2"][0]: Decimal("1.00"),
        },
    )
    assert isinstance(result, ModelSelection)
    assert result.model_id == cheap


def test_select_model_for_dispatch_budget_fallback_uses_recursive_decision_not_tier_sort() -> None:
    """Tier-2 wins when its marginal expected cost is lower than a fitting tier-1 model."""
    expensive = TIER_LADDER["tier-1"][0]
    cheap_tier1 = TIER_LADDER["tier-1"][1]
    tier2 = TIER_LADDER["tier-2"][0]
    # cheap_tier1: cost=0.13, prior=0.05 → high expected cost due to low success probability
    # tier2:       cost=0.11, prior=0.98 → low expected cost due to near-certain success
    models = {
        expensive: _entry(expensive, "0.20"),
        cheap_tier1: _entry(cheap_tier1, "0.13"),
        tier2: _entry(tier2, "0.11"),
    }
    availability = {model_id: "available" for model_id in models}
    result = select_model_for_dispatch(
        models,
        availability,
        budget_ceiling=Decimal("0.14"),
        model_overrides={
            expensive: Decimal("0.50"),
            cheap_tier1: Decimal("0.05"),
            tier2: Decimal("0.98"),
        },
    )
    assert isinstance(result, ModelSelection)
    # The recursive decision tree should select tier2 (expected cost ≈ 0.11)
    # over cheap_tier1 (expected cost ≈ 0.23), not the tier-first sort winner.
    assert result.model_id == tier2


def test_select_model_for_dispatch_budget_fallback_preserves_original_ranking() -> None:
    over_budget = TIER_LADDER["tier-1"][0]
    fitting_tier1 = TIER_LADDER["tier-1"][1]
    fitting_tier2 = TIER_LADDER["tier-2"][0]
    tier3 = TIER_LADDER["tier-3"][0]
    models = {
        over_budget: _entry(over_budget, "0.20"),
        fitting_tier1: _entry(fitting_tier1, "0.05"),
        fitting_tier2: _entry(fitting_tier2, "0.10"),
        tier3: _entry(tier3, "0.30"),
    }
    availability = {model_id: "available" for model_id in models}
    result = select_model_for_dispatch(
        models,
        availability,
        budget_ceiling=Decimal("0.15"),
        model_overrides={
            over_budget: Decimal("1.00"),
            fitting_tier1: Decimal("0.00"),
            fitting_tier2: Decimal("0.00"),
            tier3: Decimal("1.00"),
        },
    )
    assert isinstance(result, ModelSelection)
    assert result.model_id == fitting_tier1
    expected_cost = Decimal("0.05") + (Decimal("1.00") - Decimal("0.00")) * Decimal("0.20")
    assert result.expected_cost == expected_cost
    assert result.branch_value == expected_cost


def test_select_model_for_dispatch_budget_fallback_does_not_skip_next_tier() -> None:
    tier1 = TIER_LADDER["tier-1"][0]
    tier2 = TIER_LADDER["tier-2"][0]
    tier3 = TIER_LADDER["tier-3"][0]
    models = {
        tier1: _entry(tier1, "0.20"),
        tier2: _entry(tier2, "0.15"),
        tier3: _entry(tier3, "0.05"),
    }
    availability = {model_id: "available" for model_id in models}
    result = select_model_for_dispatch(
        models,
        availability,
        budget_ceiling=Decimal("0.15"),
        model_overrides={
            tier1: Decimal("1.00"),
            tier2: Decimal("0.00"),
            tier3: Decimal("1.00"),
        },
    )
    assert isinstance(result, ModelSelection)
    assert result.model_id == tier2
    # tier2 remains the only legal affordable first step because tier-3 cannot be
    # chosen directly while tier-2 is still eligible. Its branch value includes
    # the forced fallback to tier-3 after a tier-2 failure: 0.15 + 1.0 * 0.05.
    assert result.expected_cost == Decimal("0.20")


def test_select_model_for_dispatch_budget_exhausted_when_fitting_candidates_below_start_tier() -> None:
    """NoSelection('budget_exhausted') when all fitting candidates are below the start tier."""
    tier1 = TIER_LADDER["tier-1"][0]
    tier2 = TIER_LADDER["tier-2"][0]
    tier3 = TIER_LADDER["tier-3"][0]
    # tier2 was already attempted → start_index advances to tier-2.
    # tier3 (only candidate at/above start_index) is over budget.
    # tier1 fits budget but is below start_index, so _candidate_values([tier1], 1, ...) → [].
    models = {
        tier1: _entry(tier1, "0.05"),
        tier3: _entry(tier3, "0.50"),
    }
    availability = {tier1: "available", tier3: "available"}
    result = select_model_for_dispatch(
        models,
        availability,
        attempted_models=[tier2],
        budget_ceiling=Decimal("0.10"),
    )
    assert isinstance(result, NoSelection)
    assert result.reason == "budget_exhausted"


def test_select_model_for_dispatch_handles_currency_and_mapping_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import agentic_devtools.ai_providers.tier_selector as module

    model = TIER_LADDER["tier-1"][0]
    entry = _entry(model, "0.10")
    monkeypatch.setattr(module, "resolve_model_cost", lambda model_id, models: Decimal("0.10"))
    bad_currency = dict(entry)
    bad_currency["currency"] = ""
    assert isinstance(select_model_for_dispatch({model: bad_currency}, {model: "available"}), NoSelection)

    class BrokenMapping(dict[str, object]):
        def get(self, key: object, default: object = None) -> object:
            raise TypeError("broken mapping")

    assert isinstance(select_model_for_dispatch({model: entry}, BrokenMapping()), NoSelection)
    assert isinstance(
        select_model_for_dispatch(
            {model: entry},
            {model: "available"},
            budget_ceiling=Decimal("1"),
            budget_currency="EUR",
        ),
        NoSelection,
    )
    assert isinstance(
        select_model_for_dispatch(
            {model: entry},
            {model: "available"},
            budget_currency="",
        ),
        NoSelection,
    )


def test_select_model_for_dispatch_derives_highest_attempted_tier_from_set() -> None:
    tier1_model = TIER_LADDER["tier-1"][0]
    tier2_model = TIER_LADDER["tier-2"][0]
    tier3_model = TIER_LADDER["tier-3"][0]
    models = {
        tier1_model: _entry(tier1_model, "0.05"),
        tier2_model: _entry(tier2_model, "0.20"),
        tier3_model: _entry(tier3_model, "0.50"),
    }
    availability = {m: "available" for m in models}
    # When a tier-2 model was attempted last but a tier-1 model was also attempted,
    # the start_index must be derived from the *highest* tier in the set (tier-2).
    # With input ordering reversed (tier-1 last), broken code would pick tier-1 start.
    result = select_model_for_dispatch(
        models,
        availability,
        attempted_models=[tier2_model, tier1_model],
        ordinal=3,
    )
    assert isinstance(result, ModelSelection)
    assert result.tier == "tier-3"


def test_select_model_for_dispatch_returns_no_selection_when_no_candidate_at_or_above_start_tier() -> None:
    tier1_model = TIER_LADDER["tier-1"][0]
    tier2_model = TIER_LADDER["tier-2"][0]
    models = {tier1_model: _entry(tier1_model, "0.05")}
    availability = {tier1_model: "available"}
    # Tier-2 model was attempted; only tier-1 candidates remain.
    # _candidate_values returns empty sequence → must produce NoSelection, not IndexError.
    result = select_model_for_dispatch(
        models,
        availability,
        attempted_models=[tier2_model],
        ordinal=2,
    )
    assert isinstance(result, NoSelection)
    assert result.reason == "no_eligible_model"
