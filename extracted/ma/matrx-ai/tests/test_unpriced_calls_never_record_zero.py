"""An unpriced model call must never count as $0 (incident 2026-10-15).

One ai.offering row (gemini-4-argon) stored ``component_prices`` nested —
``{"service": {"web_search": 14000}}`` instead of ``{"service.web_search": 14000}``.
``float(dict)`` threw inside ``warm_pricing_lookup``, the whole price table failed to load,
every model call after the next restart had no price, and the spend guards accrued
``float(None or 0.0)`` = $0. The per-account weekly cap, the per-run cost limit and the spend
alarms saw nothing.

These tests pin the three halves of the fix:
* the parser reads every shape the catalog holds (nested component prices included);
* one malformed row unprices ONE offering, loudly — never the whole table;
* an unpriced call accrues a conservative estimate and reaches the unpriced hook (the alarm).
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config import usage_config as uc
from matrx_ai.config.usage_config import ModelPricing, PricingTier, TokenUsage

LIVE_BAD_ROW = [
    {
        "max_tokens": None,
        "input_price": 2,
        "output_price": 10,
        "component_prices": {"service": {"web_search": 14000}},
        "cached_input_price": 0.1,
    }
]


def test_nested_component_prices_parse_to_dotted_keys() -> None:
    tiers = uc._tiers_from_pricing_field(LIVE_BAD_ROW)

    assert len(tiers) == 1
    assert tiers[0].component_prices == {"service.web_search": 14000.0}
    assert tiers[0].input_price == 2.0
    assert tiers[0].output_price == 10.0


def test_flat_and_string_prices_still_parse() -> None:
    tiers = uc._tiers_from_pricing_field(
        '[{"max_tokens": 200000, "input_price": "1.25", "output_price": 10,'
        ' "cached_input_price": null, "component_prices": {"service.google_search": 14000.0}}]'
    )
    assert tiers[0].max_tokens == 200000
    assert tiers[0].input_price == 1.25
    assert tiers[0].cached_input_price == 0.0
    assert tiers[0].component_prices == {"service.google_search": 14000.0}


def test_empty_pricing_is_unpriced_never_a_zero_tier() -> None:
    assert uc._tiers_from_pricing_field(None) == []
    assert uc._tiers_from_pricing_field([]) == []
    assert uc._tiers_from_pricing_field({}) == []


def test_a_non_price_is_a_named_shape_error() -> None:
    with pytest.raises(uc.PricingShapeError, match=r"pricing\[0\]\.input_price"):
        uc._tiers_from_pricing_field([{"input_price": {"usd": 2}, "output_price": 10}])


@pytest.mark.asyncio
async def test_one_bad_offering_never_unprices_the_whole_table(monkeypatch) -> None:
    from matrx_ai.catalog import host_catalog
    from matrx_ai.catalog import manager as catalog_manager_module
    from matrx_ai.db.ai_models import ai_model_manager as model_manager_module

    models = [
        SimpleNamespace(id="m-good", name="good-model", is_deprecated=False, retired_at=None),
        SimpleNamespace(id="m-bad", name="bad-model", is_deprecated=False, retired_at=None),
    ]
    offerings = {
        "m-good": [SimpleNamespace(id="o-good", endpoint_id="e", provider_model_id="good-model", pricing=[{"input_price": 1, "output_price": 4}])],
        "m-bad": [SimpleNamespace(id="o-bad", endpoint_id="e", provider_model_id="bad-model", pricing=[{"input_price": [1], "output_price": 4}])],
    }

    class _Models:
        async def load_all_models(self):
            return models

    class _Catalog:
        async def ensure_loaded(self):
            return None

        def offerings_for(self, model_id):
            return offerings[model_id]

        def parked_offerings_for(self, model_id):
            return []

        def endpoint(self, endpoint_id):
            return SimpleNamespace(vendor="test")

    captured: list[tuple[str, str]] = []
    monkeypatch.setattr(uc, "_capture_pricing_problem", lambda kind, message, payload: captured.append((kind, message)))
    monkeypatch.setattr(host_catalog, "get_model_catalog", lambda: None)
    monkeypatch.setattr(model_manager_module, "ai_model_manager_instance", _Models())
    monkeypatch.setattr(catalog_manager_module, "ai_catalog_manager", _Catalog())
    monkeypatch.setattr(uc, "_pricing_lookup_cache", None)
    monkeypatch.setattr(uc, "_pricing_invalid_offerings", {})
    monkeypatch.setattr(uc, "_pricing_warm_error", "")

    lookup = await uc.warm_pricing_lookup()

    assert "good-model" in lookup and "o-good" in lookup
    assert "bad-model" not in lookup
    health = uc.pricing_warm_health()
    assert health["warm"] is True
    assert health["ok"] is False
    assert list(health["invalid_offerings"]) == ["bad-model (offering o-bad)"]
    assert [kind for kind, _ in captured] == ["pricing_shape_invalid"]


@pytest.mark.asyncio
async def test_a_failed_warm_is_captured_and_reported_not_ready(monkeypatch) -> None:
    from matrx_ai.catalog import host_catalog
    from matrx_ai.db.ai_models import ai_model_manager as model_manager_module

    class _Broken:
        async def load_all_models(self):
            raise RuntimeError("catalog unreachable")

    captured: list[str] = []
    monkeypatch.setattr(uc, "_capture_pricing_problem", lambda kind, message, payload: captured.append(kind))
    monkeypatch.setattr(host_catalog, "get_model_catalog", lambda: None)
    monkeypatch.setattr(model_manager_module, "ai_model_manager_instance", _Broken())
    monkeypatch.setattr(uc, "_pricing_lookup_cache", None)
    monkeypatch.setattr(uc, "_pricing_warm_error", "")

    assert await uc.warm_pricing_lookup() == {}
    assert captured == ["pricing_lookup_warm_failed"]
    health = uc.pricing_warm_health()
    assert health["ok"] is False and health["warm"] is False
    assert "catalog unreachable" in health["last_error"]


def test_conservative_estimate_uses_the_highest_price_or_the_fallback(monkeypatch) -> None:
    usage = TokenUsage(input_tokens=1_000_000, output_tokens=1_000_000, matrx_model_name="x")

    monkeypatch.setattr(uc, "_pricing_lookup_cache", {})
    assert uc.conservative_unpriced_cost(usage) == pytest.approx(
        uc.UNPRICED_FALLBACK_INPUT_PER_M + uc.UNPRICED_FALLBACK_OUTPUT_PER_M
    )

    cheap = PricingTier(max_tokens=None, input_price=0.1, output_price=0.4, cached_input_price=0.01)
    dear = PricingTier(max_tokens=None, input_price=5.0, output_price=25.0, cached_input_price=0.5)
    monkeypatch.setattr(
        uc,
        "_pricing_lookup_cache",
        {"a": ModelPricing("a", "x", [cheap]), "b": ModelPricing("b", "x", [dear])},
    )
    assert uc.conservative_unpriced_cost(usage) == pytest.approx(30.0)


@pytest.mark.asyncio
async def test_an_unpriced_call_accrues_an_estimate_and_alarms_never_zero(monkeypatch) -> None:
    """THE incident path: price table empty, a tracked account makes a call."""
    from matrx_ai.context import app_context
    from matrx_ai.providers import guardrail_gate

    ctx = SimpleNamespace(user_id="u-test", request_id="r-1", conversation_id="c-1")
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: ctx)
    monkeypatch.setattr(uc, "_pricing_lookup_cache", {})  # warm but empty: every call unpriced

    accrued: list[float] = []
    unpriced: list[tuple[str, float]] = []
    monkeypatch.setattr(guardrail_gate, "_accrue", None)
    monkeypatch.setattr(guardrail_gate, "_every_call_usage", None)
    monkeypatch.setattr(guardrail_gate, "_every_call_tracked", lambda c: True)
    monkeypatch.setattr(guardrail_gate, "_every_call_accrue", lambda c, cost: accrued.append(cost))
    monkeypatch.setattr(
        guardrail_gate,
        "_every_call_unpriced",
        lambda c, usage, cost: unpriced.append((usage.matrx_model_name, cost)),
        raising=False,
    )

    usage = TokenUsage(input_tokens=40_000, output_tokens=1_000, matrx_model_name="openai/gpt-oss-20b", api="groq")
    await guardrail_gate.note_paid_result(SimpleNamespace(usage=usage))

    assert accrued and accrued[0] > 0, f"an unpriced call accrued {accrued} — the caps would see $0"
    assert unpriced == [("openai/gpt-oss-20b", accrued[0])]


@pytest.mark.asyncio
async def test_a_priced_call_accrues_its_real_cost(monkeypatch) -> None:
    from matrx_ai.context import app_context
    from matrx_ai.providers import guardrail_gate

    ctx = SimpleNamespace(user_id="u-test", request_id="r-1", conversation_id="c-1")
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: ctx)
    tier = PricingTier(max_tokens=None, input_price=0.075, output_price=0.3, cached_input_price=0.0)
    monkeypatch.setattr(uc, "_pricing_lookup_cache", {"openai/gpt-oss-20b": ModelPricing("openai/gpt-oss-20b", "groq", [tier])})

    accrued: list[float] = []
    unpriced: list[float] = []
    monkeypatch.setattr(guardrail_gate, "_accrue", None)
    monkeypatch.setattr(guardrail_gate, "_every_call_usage", None)
    monkeypatch.setattr(guardrail_gate, "_every_call_tracked", lambda c: True)
    monkeypatch.setattr(guardrail_gate, "_every_call_accrue", lambda c, cost: accrued.append(cost))
    monkeypatch.setattr(guardrail_gate, "_every_call_unpriced", lambda c, u, cost: unpriced.append(cost), raising=False)

    usage = TokenUsage(input_tokens=40_000, output_tokens=1_000, matrx_model_name="openai/gpt-oss-20b", api="groq")
    await guardrail_gate.note_paid_result(SimpleNamespace(usage=usage))

    assert accrued == [pytest.approx((40_000 * 0.075 + 1_000 * 0.3) / 1_000_000)]
    assert unpriced == []


@pytest.mark.asyncio
async def test_a_counters_only_usage_is_priced_by_the_dispatched_route(monkeypatch) -> None:
    """2026-10-16 (model_call_unpriced "unknown model", 17 alarms): a TypeSafe decision call returns
    ``usage={input_tokens, output_tokens}`` with no model name. The dispatcher knows the route, so the
    call is priced against it — never alarmed as an unknown model while being priced a step later."""
    from matrx_ai.context import app_context
    from matrx_ai.providers import guardrail_gate
    from matrx_ai.providers.typesafe.client import TypeSafeUsage

    ctx = SimpleNamespace(user_id="u-test", request_id="r-1", conversation_id="c-1")
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: ctx)
    tier = PricingTier(max_tokens=None, input_price=0.02, output_price=0.1, cached_input_price=0.0)
    monkeypatch.setattr(uc, "_pricing_lookup_cache", {"jev-1.13.0": ModelPricing("jev-1.13.0", "typesafe", [tier])})

    accrued: list[float] = []
    unpriced: list[str] = []
    monkeypatch.setattr(guardrail_gate, "_accrue", None)
    monkeypatch.setattr(guardrail_gate, "_every_call_usage", None)
    monkeypatch.setattr(guardrail_gate, "_every_call_tracked", lambda c: True)
    monkeypatch.setattr(guardrail_gate, "_every_call_accrue", lambda c, cost: accrued.append(cost))
    monkeypatch.setattr(
        guardrail_gate, "_every_call_unpriced",
        lambda c, u, cost: unpriced.append(str(getattr(u, "matrx_model_name", "") or "unknown model")), raising=False,
    )
    profile = SimpleNamespace(model_name="jev-1.13.0", provider_model_id="jev-1.13.0", vendor="typesafe",
                              offering_id="", resolution_route="pinned")
    result = SimpleNamespace(usage=TypeSafeUsage(input_tokens=1_987, output_tokens=362))

    await guardrail_gate.note_paid_result(result, profile=profile)
    assert unpriced == [], f"a routed decision call alarmed as unpriced: {unpriced}"
    assert accrued == [pytest.approx((1_987 * 0.02 + 362 * 0.1) / 1_000_000)]

    # Without the route the same usage is honestly unpriced (the fix is the route, not a silent 0).
    accrued.clear()
    await guardrail_gate.note_paid_result(result)
    assert unpriced == ["unknown model"] and accrued and accrued[0] > 0


def test_non_token_usage_is_never_priced_as_tokens(monkeypatch) -> None:
    """veo-3.1-lite stored 21,000,000 video units in output_tokens; at the top token rate that read
    $1,575 and refused every call (2026-10-18). Units price by their own unit or stay announced."""
    dear = PricingTier(max_tokens=None, input_price=20.0, output_price=75.0, cached_input_price=2.0)
    video = PricingTier(max_tokens=None, input_price=0.0, output_price=0.2, cached_input_price=0.0,
                        usage_basis="video_second_output")
    monkeypatch.setattr(
        uc, "_pricing_lookup_cache",
        {"a": ModelPricing("a", "x", [dear]), "veo": ModelPricing("veo", "x", [video])},
    )
    usage = TokenUsage(
        input_tokens=0, output_tokens=21_000_000, matrx_model_name="veo-new",
        metadata={"billing_kind": "synthetic:video_second_output"},
    )
    est = uc.estimate_unpriced_call(usage)
    assert est.kind == "units" and est.unit == "second" and est.units == pytest.approx(21.0)
    assert est.cost_usd == pytest.approx(4.2)
    assert uc.conservative_unpriced_cost(usage) < 10  # was 1,575

    # no unit price known anywhere: announced as unknown, never a token price
    monkeypatch.setattr(uc, "_pricing_lookup_cache", {"a": ModelPricing("a", "x", [dear])})
    est = uc.estimate_unpriced_call(usage)
    assert est.kind == "unknown_units" and est.cost_usd == 0.0

    # basis found from the model's own price tier when metadata is absent
    monkeypatch.setattr(
        uc, "_pricing_lookup_cache",
        {"veo-new": ModelPricing("veo-new", "x", [video]), "a": ModelPricing("a", "x", [dear])},
    )
    monkeypatch.setattr(uc, "is_pricing_lookup_warm", lambda: True)
    monkeypatch.setattr(uc, "_get_db_pricing_lookup", lambda: uc._pricing_lookup_cache)
    bare = TokenUsage(input_tokens=0, output_tokens=2_000_000, matrx_model_name="veo-new")
    assert uc.estimate_unpriced_call(bare).cost_usd == pytest.approx(0.4)

    # real tokens still price high
    real = TokenUsage(input_tokens=1_000_000, output_tokens=1_000_000, matrx_model_name="gpt-x")
    assert uc.estimate_unpriced_call(real).cost_usd == pytest.approx(95.0)
