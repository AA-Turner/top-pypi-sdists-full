"""Regression tests: an Anthropic call that used hosted web search must PRICE.

The incident (2026-08-18 → 2026-08-19): seven ``chat.request`` rows recorded
``cost = NULL``. All were ``claude-opus-5`` runs of the "Race Frontier Floor"
agent with ``settings.internal_web_search = true``. Anthropic returned
``server_tool_use.web_search_requests``, ``from_anthropic`` recorded the
``service.web_search`` billing component, and the offering's pricing tier
carried ``component_prices = {}`` — so ``calculate_cost_breakdown`` refused the
whole calculation (``cost_reconciliation = "unknown_component_price"``) rather
than record a token-only underestimate. Ordinary Anthropic calls the same day
priced fine, because they emit no billing component at all.

Two fixes are locked in here:
  1. With the component price present ($10 per 1,000 searches → 10_000/1M), the
     call prices — service fee INCLUDED.
  2. ``validate_model_pricing`` now flags a web-search-capable model whose
     pricing lacks that component price, BEFORE the spend.

Plus the cache-write defect the same fixture exposed: the Anthropic duration
split (``cache_creation.ephemeral_*``) was 6,624 tokens while the authoritative
``cache_creation_input_tokens`` was 42,709 — trusting the split dropped 36,085
billable cache-write tokens.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.usage_config import (
    ModelPricing,
    PricingTier,
    TokenUsage,
    validate_model_pricing,
)

# Verbatim ``chat.request.raw_usage`` of row 3d501a92-24eb-42b8-9815-6dfa595d9780
# (2026-08-19 23:17, anthropic, claude-opus-5, finish_reason "stop", cost NULL).
ROW_3D501A92_RAW_USAGE: dict = {
    "input_tokens": 8,
    "service_tier": "standard",
    "inference_geo": "global",
    "output_tokens": 12595,
    "cache_creation": {
        "ephemeral_1h_input_tokens": 0,
        "ephemeral_5m_input_tokens": 6624,
    },
    "server_tool_use": {"web_fetch_requests": 0, "web_search_requests": 5},
    "cache_read_input_tokens": 61981,
    "cache_creation_input_tokens": 42709,
}

# Verbatim ``ai.offering.pricing[0]`` for claude-opus-5 (offering
# 1a2730e8-4ee7-4557-82d0-f1869db86332) as recorded in that row's
# ``metadata.pricing_snapshot`` — component_prices was EMPTY.
_OPUS_5_TIER_FIELDS = dict(
    max_tokens=None,
    input_price=5.0,
    output_price=25.0,
    cached_input_price=0.5,
    cache_write_5m_price=6.25,
    cache_write_1h_price=10.0,
)


def _pricing(component_prices: dict[str, float]) -> dict[str, ModelPricing]:
    return {
        "claude-opus-5": ModelPricing(
            model_name="claude-opus-5",
            api="anthropic",
            tiers=[PricingTier(component_prices=component_prices, **_OPUS_5_TIER_FIELDS)],
        )
    }


def _usage() -> TokenUsage:
    return TokenUsage.from_anthropic(
        ROW_3D501A92_RAW_USAGE, matrx_model_name="claude-opus-5"
    )


def test_recorded_usage_carries_the_web_search_component():
    usage = _usage()
    assert usage.billing_components == {"service.web_search": 5}
    # web_fetch is free on the Claude API — it must NOT become a billing component.
    assert "service.web_fetch" not in usage.billing_components


def test_unpriced_web_search_component_records_null_not_zero():
    """The bug as it happened: no component price → cost NULL, loudly labelled."""
    usage = _usage()
    assert usage.calculate_cost(_pricing({})) is None
    assert usage.metadata["cost_reconciliation"] == "unknown_component_price"


def test_recorded_usage_prices_once_the_component_is_priced():
    """The fix: $10 per 1,000 searches is stored per MILLION units (10_000)."""
    usage = _usage()
    breakdown = usage.calculate_cost_breakdown(
        _pricing({"service.web_search": 10_000.0})
    )
    assert breakdown is not None

    assert breakdown.input_cost == pytest.approx(8 / 1e6 * 5.0)
    assert breakdown.output_cost == pytest.approx(12_595 / 1e6 * 25.0)
    assert breakdown.cached_input_cost == pytest.approx(61_981 / 1e6 * 0.5)
    # 5 searches × $10/1,000 = $0.05
    assert breakdown.component_costs["service.web_search"] == pytest.approx(0.05)
    # The authoritative cache_creation_input_tokens wins over the short split.
    assert breakdown.cache_write_5m_tokens == 42_709
    assert breakdown.cache_write_1h_tokens == 0
    assert breakdown.cache_write_5m_cost == pytest.approx(42_709 / 1e6 * 6.25)

    assert breakdown.total_cost == pytest.approx(0.66283675)
    assert "cost_reconciliation" not in usage.metadata


def test_short_cache_write_duration_split_does_not_drop_billable_tokens():
    """A merged usage record can carry a duration split smaller than its total."""
    usage = _usage()
    breakdown = usage.calculate_cost_breakdown(
        _pricing({"service.web_search": 10_000.0})
    )
    assert breakdown is not None
    # 6,624 was the split; 42,709 is the recorded total — the 36,085-token
    # remainder is billed at the 5m default TTL rate, never silently discarded.
    assert breakdown.cache_write_5m_tokens - 6_624 == 36_085


def test_honest_duration_split_is_left_alone():
    """When the split agrees with the total, nothing is re-attributed."""
    raw = {
        "input_tokens": 10,
        "output_tokens": 100,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 30_000,
        "cache_creation": {
            "ephemeral_5m_input_tokens": 20_000,
            "ephemeral_1h_input_tokens": 10_000,
        },
    }
    usage = TokenUsage.from_anthropic(raw, matrx_model_name="claude-opus-5")
    breakdown = usage.calculate_cost_breakdown(_pricing({}))
    assert breakdown is not None
    assert breakdown.cache_write_5m_tokens == 20_000
    assert breakdown.cache_write_1h_tokens == 10_000


# --------------------------------------------------------------------------- #
# The guard: catch the missing price BEFORE money is spent
# --------------------------------------------------------------------------- #


def _caps(name: str, features: list[str]):
    from types import SimpleNamespace

    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

    return resolve_model_capabilities(
        SimpleNamespace(
            name=name,
            capabilities={
                "input": ["text", "image"],
                "output": ["text"],
                "features": features,
                "interaction": "turn",
            },
        )
    )


_WEB_SEARCH_FEATURES = ["function_calling", "thinking", "vision", "web_search"]


def test_validator_flags_web_search_model_without_a_service_price():
    issues = validate_model_pricing(
        "claude-opus-5",
        "anthropic_chat",
        _caps("claude-opus-5", _WEB_SEARCH_FEATURES),
        [dict(_OPUS_5_TIER_FIELDS)],  # exactly what shipped: no component_prices
        token_billed=True,
    )
    assert any(i.code == "missing_service_price" and i.severity == "error" for i in issues)


def test_validator_accepts_the_priced_tier():
    issues = validate_model_pricing(
        "claude-opus-5",
        "anthropic_chat",
        _caps("claude-opus-5", _WEB_SEARCH_FEATURES),
        [dict(_OPUS_5_TIER_FIELDS, component_prices={"service.web_search": 10_000})],
        token_billed=True,
    )
    assert not [i for i in issues if i.code == "missing_service_price"]


def test_validator_ignores_a_model_that_cannot_web_search():
    issues = validate_model_pricing(
        "claude-3-opus-20240229",
        "anthropic_chat",
        _caps("claude-3-opus-20240229", ["json_mode", "structured_output"]),
        [dict(_OPUS_5_TIER_FIELDS)],
        token_billed=True,
    )
    assert not [i for i in issues if i.code == "missing_service_price"]
