"""A model NAME may never decide how a customer is billed.

`resolve_usage_basis` and `TokenUsage.calculate_cost` used to fall back to
`model_name.startswith(key)` over the pricing-lookup dict, taking the FIRST
prefix hit in insertion order. On the live catalog that is not a fallback, it is
a billing lottery — these collisions are real, taken from ai.model_definition:

    gpt-5-nano          ($0.40/M out)  ->  gpt-5   ($10.00/M out)   25x overcharge
    gpt-4o-mini         ($0.60/M out)  ->  gpt-4o  ($10.00/M out)   16x overcharge
    google/veo-3.0-fast ($0.80/s)      ->  veo-3.0 ($1.60/s)         2x overcharge

The pricing fact is `ai.offering.pricing`, keyed exactly. A miss must SCREAM and
record no cost, never guess: a wrong cost recorded silently is discovered by a
customer; a missing cost recorded loudly is discovered by us.
"""

from __future__ import annotations

import pytest

from matrx_ai.config import usage_config as uc
from matrx_ai.config.usage_config import (
    ModelPricing,
    PricingTier,
    ProviderCharge,
    TokenUsage,
    provider_charge_from_usage,
)


@pytest.mark.asyncio
async def test_orphan_model_failure_creates_structured_system_error(monkeypatch) -> None:
    captured: list[tuple[BaseException, dict[str, object]]] = []

    async def record_error(error: BaseException, **kwargs: object) -> None:
        captured.append((error, kwargs))

    monkeypatch.setattr(uc, "has_ext", None, raising=False)
    from matrx_ai import _ext

    monkeypatch.setattr(_ext, "has_ext", lambda name: name == "record_error")
    monkeypatch.setattr(_ext, "get_ext", lambda name: record_error)

    await uc._capture_orphan_models(["model-a (id-a)", "model-b (id-b)"])

    assert len(captured) == 1
    error, fields = captured[0]
    assert isinstance(error, uc.CatalogOrphanModelsError)
    assert fields["kind"] == "ai_catalog_orphan_models"
    assert fields["route"] == "matrx_ai.config.usage_config.warm_pricing_lookup"
    assert fields["payload"] == {
        "orphan_models": ["model-a (id-a)", "model-b (id-b)"],
        "orphan_count": 2,
    }


def _tier(input_price: float, output_price: float, usage_basis: str | None = None) -> PricingTier:
    return PricingTier(
        max_tokens=None,
        input_price=input_price,
        output_price=output_price,
        cached_input_price=0.0,
        usage_basis=usage_basis,
    )


@pytest.fixture
def colliding_lookup(monkeypatch: pytest.MonkeyPatch) -> dict[str, ModelPricing]:
    """`gpt-5` is inserted FIRST so a prefix scan would hit it before `gpt-5-nano`."""
    lookup = {
        "gpt-5": ModelPricing(model_name="gpt-5", api="openai", tiers=[_tier(1.25, 10.00)]),
        "gpt-5-nano": ModelPricing(model_name="gpt-5-nano", api="openai", tiers=[_tier(0.05, 0.40)]),
        "gpt-4o": ModelPricing(model_name="gpt-4o", api="openai", tiers=[_tier(2.50, 10.00)]),
        "gpt-4o-mini": ModelPricing(
            model_name="gpt-4o-mini", api="openai", tiers=[_tier(0.15, 0.60)]
        ),
        "veo-3.0": ModelPricing(
            model_name="veo-3.0", api="google", tiers=[_tier(0.0, 1.60, "video_second_output")]
        ),
        "veo-3.0-fast": ModelPricing(
            model_name="veo-3.0-fast", api="google", tiers=[_tier(0.0, 0.80, "video_second_output")]
        ),
    }
    monkeypatch.setattr(uc, "_get_db_pricing_lookup", lambda: lookup)
    monkeypatch.setattr(uc, "is_pricing_lookup_warm", lambda: True)
    return lookup


@pytest.mark.parametrize(
    ("model_name", "expected_output_price"),
    [
        ("gpt-5-nano", 0.40),
        ("gpt-5", 10.00),
        ("gpt-4o-mini", 0.60),
        ("gpt-4o", 10.00),
    ],
)
def test_exact_name_wins_over_a_shorter_prefix(
    colliding_lookup: dict[str, ModelPricing], model_name: str, expected_output_price: float
) -> None:
    usage = TokenUsage(input_tokens=0, output_tokens=1_000_000)
    usage.matrx_model_name = model_name
    usage.api = "openai"
    cost = usage.calculate_cost()
    assert cost is not None, f"{model_name} must resolve its own pricing row"
    assert cost == pytest.approx(expected_output_price), (
        f"{model_name} billed at {cost} — a prefix row leaked into the lookup"
    )


def test_unknown_model_records_no_cost_instead_of_guessing(
    colliding_lookup: dict[str, ModelPricing],
) -> None:
    """`gpt-5-nano-2026-01-01` prefix-matches `gpt-5` (25x). It must bill NOTHING."""
    usage = TokenUsage(input_tokens=0, output_tokens=1_000_000)
    usage.matrx_model_name = "gpt-5-nano-2026-01-01"
    usage.api = "openai"
    assert usage.calculate_cost() is None


def test_provider_reported_charge_never_replaces_canonical_catalog_cost(
    colliding_lookup: dict[str, ModelPricing],
) -> None:
    usage = TokenUsage(
        input_tokens=0,
        output_tokens=1_000_000,
        matrx_model_name="gpt-5-nano",
        api="openai",
        provider_charge=ProviderCharge(
            amount_usd=0.37,
            raw_amount=3_700_000_000,
            raw_unit="usd_tick_1e-10",
            field_path="usage.cost_in_usd_ticks",
        ),
    )
    assert usage.calculate_cost() == pytest.approx(0.40)
    assert usage.provider_charge.authoritative_usd == pytest.approx(0.37)
    assert usage.calculate_catalog_cost() == pytest.approx(0.40)


def test_non_final_provider_charge_is_evidence_not_authoritative(
    colliding_lookup: dict[str, ModelPricing],
) -> None:
    usage = TokenUsage(
        input_tokens=0,
        output_tokens=1_000_000,
        matrx_model_name="gpt-5-nano",
        provider_charge=ProviderCharge(
            amount_usd=0.01,
            raw_amount=1,
            raw_unit="estimate",
            field_path="usage.estimate",
            is_final=False,
        ),
    )
    assert usage.calculate_cost() == pytest.approx(0.40)


def test_distinct_provider_charges_accumulate_without_catalog_fallback() -> None:
    first = TokenUsage(
        input_tokens=1,
        output_tokens=1,
        provider_charge=ProviderCharge(0.10, 1, "tick", "first"),
    )
    second = TokenUsage(
        input_tokens=1,
        output_tokens=1,
        provider_charge=ProviderCharge(0.20, 2, "tick", "second"),
    )
    combined = first + second
    assert combined.provider_charge is not None
    assert combined.provider_charge.authoritative_usd == pytest.approx(0.30)


@pytest.mark.parametrize(
    ("raw_usage", "expected", "field_path"),
    [
        ({"cost": 0.08123}, 0.08123, "usage.cost"),
        ({"total_cost": "0.42"}, 0.42, "usage.total_cost"),
        ({"cost_usd": 1.25}, 1.25, "usage.cost_usd"),
        ({"total_cost_usd": 2}, 2.0, "usage.total_cost_usd"),
    ],
)
def test_explicit_provider_usd_charge_is_recovered_from_usage(
    raw_usage: dict[str, object], expected: float, field_path: str
) -> None:
    charge = provider_charge_from_usage(raw_usage)

    assert charge is not None
    assert charge.authoritative_usd == pytest.approx(expected)
    assert charge.field_path == field_path


def test_token_usage_automatically_promotes_explicit_provider_charge() -> None:
    usage = TokenUsage(
        input_tokens=100,
        output_tokens=20,
        matrx_model_name="gateway/model",
        api="openrouter",
        raw_usage={"cost": 0.009, "prompt_tokens": 100, "completion_tokens": 20},
    )

    assert usage.provider_charge is not None
    assert usage.provider_charge.authoritative_usd == pytest.approx(0.009)
    assert usage.calculate_cost({}) is None


@pytest.mark.parametrize(
    "raw_usage",
    [
        {"prompt_tokens": 100, "completion_tokens": 20},
        {"cost": True},
        {"cost": "not-money"},
        {"cost": 0.01, "currency": "EUR"},
    ],
)
def test_non_usd_or_non_monetary_usage_is_not_authoritative(
    raw_usage: dict[str, object],
) -> None:
    charge = provider_charge_from_usage(raw_usage)

    assert charge is None or charge.authoritative_usd is None


def test_aggregate_separates_catalog_total_from_provider_charge_evidence(
    colliding_lookup: dict[str, ModelPricing],
) -> None:
    known = TokenUsage(
        input_tokens=0,
        output_tokens=1_000_000,
        matrx_model_name="gpt-5-nano",
        api="gateway",
        raw_usage={"cost": 0.37},
    )
    unknown = TokenUsage(
        input_tokens=20,
        output_tokens=2,
        matrx_model_name="unknown",
        api="anthropic",
    )

    aggregate = TokenUsage.aggregate_by_model([known, unknown])

    assert aggregate.total.total_cost is None
    assert aggregate.total.known_cost_subtotal == pytest.approx(0.40)
    assert aggregate.total.provider_reported_requests == 1
    assert aggregate.total.catalog_priced_requests == 1
    assert aggregate.total.unknown_cost_requests == 1


def test_model_summary_is_unknown_if_any_call_for_model_is_unpriced(
    colliding_lookup: dict[str, ModelPricing],
) -> None:
    known = TokenUsage(
        input_tokens=0,
        output_tokens=1_000_000,
        matrx_model_name="gpt-5-nano",
        api="openai",
    )
    unknown = TokenUsage(
        input_tokens=0,
        output_tokens=1,
        matrx_model_name="gpt-5-nano",
        api="openai",
        metadata={"cost_reconciliation": "unknown_missing_provider_usage"},
    )

    known_then_unknown = TokenUsage.aggregate_by_model([known, unknown])
    unknown_then_known = TokenUsage.aggregate_by_model([unknown, known])

    assert known_then_unknown.by_model["gpt-5-nano"].cost is None
    assert unknown_then_known.by_model["gpt-5-nano"].cost is None
    assert known_then_unknown.total.known_cost_subtotal == pytest.approx(0.40)


def test_resolve_usage_basis_never_prefix_matches(
    colliding_lookup: dict[str, ModelPricing],
) -> None:
    """veo-3.0-fast has its own basis; an unknown veo variant must not inherit one."""
    assert uc.resolve_usage_basis("veo-3.0-fast", "google") == (True, "video_second_output")
    assert uc.resolve_usage_basis("veo-3.0-turbo-preview", "google") == (False, None)


def test_no_startswith_in_the_pricing_resolution_path() -> None:
    """Structural guard: the prefix fallback must never come back."""
    import inspect

    for fn in (uc.resolve_usage_basis, TokenUsage.calculate_cost):
        src = inspect.getsource(fn)
        assert "startswith" not in src, (
            f"{fn.__qualname__} reintroduced a name-prefix match into billing"
        )
