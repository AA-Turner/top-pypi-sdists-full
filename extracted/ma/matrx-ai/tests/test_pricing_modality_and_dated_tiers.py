"""Pricing tiers: per-modality prices, effective-dated prices, and both web-search key shapes.

* ``modality_prices`` ({"audio": {"input_price": 3, "output_price": 12}}) is the same price as
  ``component_prices`` {"input.audio": 3, "output.audio": 12} — folded at parse.
* Gemini chat usage carries its modality split as ADVISORY components
  (``modality.input.audio``): priced at the modality rate when the tier has one, otherwise the
  tokens stay at the base rate exactly as before (a missing override is never an unknown cost).
* ``effective_from`` (ISO date/datetime, UTC): per ``max_tokens`` threshold the tier with the
  latest ``effective_from`` at or before the request time wins; undated tiers behave as today.
* ``component_prices`` nested ({"service": {"web_search": 14000}}) and dotted
  ({"service.web_search": 14000}) are the same price for cost AND for the validator.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from matrx_ai.config.usage_config import (
    ModelPricing,
    PricingShapeError,
    TokenUsage,
    _tiers_from_pricing_field,
    gemini_modality_counts,
    validate_model_pricing,
)
from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

MODEL = "gemini-test"


def _lookup(pricing: list[dict]) -> dict[str, ModelPricing]:
    return {MODEL: ModelPricing(model_name=MODEL, api="google", tiers=_tiers_from_pricing_field(pricing))}


def _usage(input_tokens: int, output_tokens: int, cached: int = 0, components: dict | None = None) -> TokenUsage:
    return TokenUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cached_input_tokens=cached,
        matrx_model_name=MODEL,
        api="google",
        billing_components=components or {},
    )


# ── per-modality prices ─────────────────────────────────────────────────────────────────────


def test_modality_prices_fold_into_component_prices():
    [tier] = _tiers_from_pricing_field(
        [
            {
                "max_tokens": None,
                "input_price": 0.75,
                "output_price": 4.5,
                "cached_input_price": 0.075,
                "modality_prices": {
                    "audio": {"input_price": 3, "output_price": 12, "cached_input_price": 0.3},
                    "image": {"input_price": 1},
                    "video": {"input_price": 1},
                },
            }
        ]
    )
    assert tier.component_prices == {
        "input.audio": 3.0,
        "output.audio": 12.0,
        "cached_input.audio": 0.3,
        "input.image": 1.0,
        "input.video": 1.0,
    }


def test_the_same_price_written_twice_differently_is_refused():
    with pytest.raises(PricingShapeError, match="input.audio twice"):
        _tiers_from_pricing_field(
            [
                {
                    "input_price": 1,
                    "output_price": 1,
                    "component_prices": {"input.audio": 3},
                    "modality_prices": {"audio": {"input_price": 4}},
                }
            ]
        )
    with pytest.raises(PricingShapeError, match="not a price field"):
        _tiers_from_pricing_field([{"input_price": 1, "modality_prices": {"audio": {"price": 4}}}])


def test_gemini_sdk_usage_becomes_advisory_modality_counts():
    sdk_usage = SimpleNamespace(
        prompt_token_count=1_000,
        cached_content_token_count=200,
        candidates_token_count=300,
        thoughts_token_count=50,
        prompt_tokens_details=[
            SimpleNamespace(modality=SimpleNamespace(value="AUDIO"), token_count=600),
            SimpleNamespace(modality=SimpleNamespace(value="TEXT"), token_count=400),
        ],
        cache_tokens_details=[SimpleNamespace(modality="MediaModality.AUDIO", token_count=200)],
        candidates_tokens_details=[SimpleNamespace(modality="IMAGE", token_count=100)],
    )
    usage = TokenUsage.from_gemini(sdk_usage, matrx_model_name=MODEL)
    assert usage.billing_components == {
        "modality.input.audio": 400,
        "modality.cached_input.audio": 200,
        "modality.output.image": 100,
    }
    assert (usage.input_tokens, usage.cached_input_tokens, usage.output_tokens) == (800, 200, 350)


def test_unpriced_modality_stays_at_the_base_rate_never_unknown():
    usage = _usage(1_000_000, 0, components={"modality.input.audio": 600_000})
    cost = usage.calculate_cost(_lookup([{"input_price": 1.0, "output_price": 2.0, "cached_input_price": 0.1}]))
    assert cost == pytest.approx(1.0)
    assert "cost_reconciliation" not in usage.metadata


def test_priced_modality_bills_its_share_at_the_modality_rate():
    usage = _usage(
        1_000_000,
        1_000_000,
        cached=100_000,
        components={
            "modality.input.audio": 600_000,
            "modality.output.audio": 250_000,
            "modality.cached_input.audio": 100_000,
        },
    )
    pricing = [
        {
            "input_price": 0.75,
            "output_price": 4.5,
            "cached_input_price": 0.075,
            "modality_prices": {"audio": {"input_price": 3, "output_price": 12, "cached_input_price": 0.3}},
        }
    ]
    cost = usage.calculate_cost(_lookup(pricing))
    expected = (
        0.4 * 0.75 + 0.6 * 3  # input: 400k text + 600k audio
        + 0.75 * 4.5 + 0.25 * 12  # output: 750k text + 250k audio
        + 0.1 * 0.3  # cached audio
    )
    assert cost == pytest.approx(expected)


def test_an_exact_modality_component_still_refuses_without_a_price():
    """Live's exact components keep their rule: unpriced audio is an unknown cost, not text-rate."""
    usage = _usage(1_000, 0, components={"input.audio": 600})
    assert usage.calculate_cost(_lookup([{"input_price": 1.0, "output_price": 2.0}])) is None
    assert usage.metadata["cost_reconciliation"] == "unknown_component_price"


def test_advisory_counts_add_across_calls():
    total = _usage(10, 0, components={"modality.input.audio": 4}) + _usage(10, 0, components={"modality.input.audio": 6})
    assert total.billing_components == {"modality.input.audio": 10}


def test_live_and_chat_read_the_same_modality_split():
    from matrx_ai.providers.google.live_history import live_modality_components

    live = {
        "promptTokensDetails": [{"modality": "AUDIO", "tokenCount": 800}],
        "responseTokensDetails": [{"modality": "AUDIO", "tokenCount": 450}],
    }
    assert live_modality_components(live) == gemini_modality_counts(live) == {"input.audio": 800, "output.audio": 450}


# ── effective-dated tiers ─────────────────────────────────────────────────────────────────


ARGON = [
    {"max_tokens": None, "input_price": 2, "output_price": 10, "cached_input_price": 0.1},
    {"max_tokens": None, "input_price": 4, "output_price": 20, "cached_input_price": 0.2, "effective_from": "2026-12-01"},
]


def test_the_latest_started_tier_wins_per_threshold():
    pricing = _lookup(ARGON)[MODEL]
    before = datetime(2026, 11, 30, 23, 59, 59, tzinfo=UTC)
    after = datetime(2026, 12, 1, 0, 0, 0, tzinfo=UTC)
    assert pricing.get_tier(0, before).input_price == 2.0
    assert pricing.get_tier(0, after).input_price == 4.0
    assert [t.input_price for t in pricing.upcoming_tiers(before)] == [4.0]
    assert pricing.upcoming_tiers(after) == []


def test_cost_uses_the_price_in_effect_at_request_time():
    usage = _usage(1_000_000, 1_000_000)
    lookup = _lookup(ARGON)
    assert usage.calculate_cost(lookup, datetime(2026, 11, 1, tzinfo=UTC)) == pytest.approx(12.0)
    assert usage.calculate_cost(lookup, datetime(2026, 12, 2, tzinfo=UTC)) == pytest.approx(24.0)
    # The snapshot the request row keeps is JSON-safe.
    json.dumps(usage.metadata["pricing_snapshot"])
    assert usage.metadata["pricing_snapshot"]["effective_from"] == "2026-12-01T00:00:00+00:00"


def test_each_context_threshold_switches_on_its_own_date():
    pro = [
        {"max_tokens": 200_000, "input_price": 2, "output_price": 12},
        {"max_tokens": None, "input_price": 4, "output_price": 18},
        {"max_tokens": 200_000, "input_price": 3, "output_price": 15, "effective_from": "2027-01-01T00:00:00Z"},
    ]
    pricing = _lookup(pro)[MODEL]
    jan = datetime(2027, 1, 2, tzinfo=UTC)
    assert pricing.get_tier(100_000, jan).input_price == 3.0
    assert pricing.get_tier(500_000, jan).input_price == 4.0  # the long-context tier did not change
    assert pricing.get_tier(100_000, datetime(2026, 6, 1, tzinfo=UTC)).input_price == 2.0


def test_undated_pricing_is_exactly_todays_behaviour():
    tiers = _tiers_from_pricing_field([{"max_tokens": 200_000, "input_price": 1}, {"max_tokens": None, "input_price": 2}])
    pricing = ModelPricing(model_name=MODEL, api="google", tiers=tiers)
    assert pricing.current_tiers() is pricing.tiers
    assert pricing.get_tier(300_000).input_price == 2.0
    assert asdict(tiers[0])["effective_from"] is None


def test_a_price_that_has_not_started_anywhere_prices_nothing():
    pricing = _lookup([{"input_price": 1, "effective_from": "2999-01-01"}])[MODEL]
    assert pricing.get_tier(0) is None
    assert _usage(10, 10).calculate_cost({MODEL: pricing}) is None


@pytest.mark.parametrize("bad", ["next month", "2026-13-01", 20261201, {"date": "2026-12-01"}])
def test_an_effective_from_that_is_not_a_date_is_refused(bad):
    with pytest.raises(PricingShapeError, match="effective_from"):
        _tiers_from_pricing_field([{"input_price": 1, "effective_from": bad}])


def test_basis_resolution_reads_the_tier_in_effect(monkeypatch):
    from matrx_ai.config import usage_config

    lookup = _lookup(
        [
            {"input_price": 1, "usage_basis": "character_input", "effective_from": "2000-01-01"},
            {"input_price": 9, "usage_basis": "minute", "effective_from": "2999-01-01"},
        ]
    )
    monkeypatch.setattr(usage_config, "_pricing_lookup_cache", lookup)
    assert usage_config.resolve_usage_basis(MODEL) == (True, "character_input")


# ── web-search fee: both stored shapes ────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "component_prices",
    [{"service": {"web_search": 14000}}, {"service.web_search": 14000}],
    ids=["nested", "dotted"],
)
def test_both_web_search_shapes_price_the_same(component_prices):
    usage = _usage(0, 0, components={"service.web_search": 3})
    pricing = [{"input_price": 1, "output_price": 1, "component_prices": component_prices}]
    assert usage.calculate_cost(_lookup(pricing)) == pytest.approx(3 * 14000 / 1_000_000)


@pytest.mark.parametrize(
    "component_prices",
    [{"service": {"web_search": 10000}}, {"service.web_search": 10000}],
    ids=["nested", "dotted"],
)
def test_the_validator_reads_both_web_search_shapes(component_prices):
    caps = resolve_model_capabilities(
        SimpleNamespace(
            name="claude-test",
            capabilities={"input": ["text"], "output": ["text"], "features": ["web_search"], "interaction": "turn"},
        )
    )
    tier = {"input_price": 3, "output_price": 15, "component_prices": component_prices}
    issues = validate_model_pricing("claude-test", "anthropic_chat", caps, [tier], token_billed=True)
    assert [i.code for i in issues] == []


def test_the_validator_names_a_broken_tier_shape():
    caps = resolve_model_capabilities(
        SimpleNamespace(name="m", capabilities={"input": ["text"], "output": ["text"], "features": [], "interaction": "turn"})
    )
    issues = validate_model_pricing(
        "m", "google_chat", caps, [{"input_price": 1, "effective_from": "soon"}], token_billed=True
    )
    assert [i.code for i in issues] == ["bad_tier_shape"]


def test_a_dated_tier_can_add_a_new_threshold_after_the_catch_all():
    pricing = _lookup(
        [
            {"max_tokens": None, "input_price": 2, "output_price": 10},
            {"max_tokens": 200_000, "input_price": 1, "output_price": 5, "effective_from": "2027-01-01"},
        ]
    )[MODEL]
    jan = datetime(2027, 1, 2, tzinfo=UTC)
    assert pricing.get_tier(100_000, jan).input_price == 1.0
    assert pricing.get_tier(300_000, jan).input_price == 2.0
    assert pricing.get_tier(100_000, datetime(2026, 12, 1, tzinfo=UTC)).input_price == 2.0


def test_the_validator_warns_when_cached_modality_has_no_price():
    caps = resolve_model_capabilities(
        SimpleNamespace(name="m", capabilities={"input": ["audio"], "output": ["text"], "features": [], "interaction": "turn"})
    )
    tier = {"input_price": 1, "output_price": 1, "modality_prices": {"audio": {"input_price": 3}}}
    issues = validate_model_pricing("m", "google_chat", caps, [tier], token_billed=True)
    assert [i.code for i in issues] == ["cached_modality_unpriced"]
