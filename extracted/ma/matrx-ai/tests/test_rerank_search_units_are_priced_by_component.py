"""A Cohere rerank bills per SEARCH UNIT: ``billing_components={"search_units": n}`` priced by
``component_prices["search_units"]`` (per MILLION units, like every component: $2 / 1,000 searches = 2000.0), with
``input_price`` 0 so the units riding in ``input_tokens`` are never billed twice. No rate priced = cost None
(unpriced, never $0)."""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.config.usage_config import ModelPricing, TokenUsage, _tiers_from_pricing_field
from matrx_ai.providers.cohere.rerank import COHERE_RERANK_API, rerank_usage

MODEL = "rerank-test-model"


def _lookup(pricing: list[dict]) -> dict[str, ModelPricing]:
    return {MODEL: ModelPricing(model_name=MODEL, api=COHERE_RERANK_API, tiers=_tiers_from_pricing_field(pricing))}


def _usage(units: int) -> TokenUsage:
    response = SimpleNamespace(id="r", meta=SimpleNamespace(billed_units=SimpleNamespace(search_units=units)))
    return rerank_usage(response, model=MODEL, documents=["a"])


def test_search_units_bill_by_component_price_once():
    lookup = _lookup([{"max_tokens": None, "input_price": 0, "output_price": 0, "component_prices": {"search_units": 2000.0}}])
    assert _usage(3).calculate_cost(lookup) == 3 * 2000.0 / 1_000_000  # $0.006, units not billed again as tokens


def test_a_rerank_with_no_search_unit_price_is_unpriced_never_free():
    lookup = _lookup([{"max_tokens": None, "input_price": 0, "output_price": 0}])
    assert _usage(3).calculate_cost(lookup) is None


def test_the_budget_guard_quotes_a_priced_rerank_at_its_search_unit_price_never_zero(monkeypatch):
    """The guard's hold for a rerank (``quote_units``) reads the same ``component_prices["search_units"]`` the settle
    bills, not ``input_price`` (0 on this shape): a priced rerank holds real money, an unpriced one holds None."""
    from matrx_ai.providers import guardrail_gate

    route = SimpleNamespace(vendor="cohere", model_name=MODEL, endpoint_id="cohere-rerank", base_url="", offering_metadata={})
    priced = _lookup([{"max_tokens": None, "input_price": 0, "output_price": 0, "component_prices": {"search_units": 2500.0}}])
    monkeypatch.setattr("matrx_ai.config.usage_config._get_db_pricing_lookup", lambda: priced)
    quote = guardrail_gate.quote_units(route, 3)
    assert quote is not None and quote.input_usd() == 3 * 2500.0 / 1_000_000.0

    monkeypatch.setattr("matrx_ai.config.usage_config._get_db_pricing_lookup", lambda: {})
    assert guardrail_gate.quote_units(route, 3) is None


# --- the live catalog row (2026-11-18) --------------------------------------------------------------------------------
# ai.offering 5ef16b13-0fbb-42a3-a106-afde43738372 (model rerank-v4.0-pro, endpoint vendor cohere, api cohere_rerank),
# its ``pricing`` column exactly as read from the live database after
# db/migrations/20261119240000_onboard_cohere_rerank_v4_pro.sql. $2.50 per 1,000 searches.
LIVE_MODEL = "rerank-v4.0-pro"
LIVE_OFFERING_ID = "5ef16b13-0fbb-42a3-a106-afde43738372"
LIVE_PRICING = [{"max_tokens": None, "input_price": 0, "output_price": 0, "component_prices": {"search_units": 2500}}]
USD_PER_SEARCH = 0.0025


def _live_lookup() -> dict[str, ModelPricing]:
    """The pricing lookup as ``warm_pricing_lookup`` indexes that one offering: by offering id, by model name (its only
    offering) and by the provider's wire id under the endpoint vendor."""
    from matrx_ai.config.usage_config import _wire_key

    pricing = ModelPricing(model_name=LIVE_MODEL, api="cohere", tiers=_tiers_from_pricing_field(LIVE_PRICING))
    return {LIVE_OFFERING_ID: pricing, LIVE_MODEL: pricing, _wire_key("cohere", LIVE_MODEL): pricing}


def test_one_rerank_on_the_live_catalog_row_is_quoted_and_settled_at_the_same_real_figure(monkeypatch):
    """The guard's pricing path on the REAL route the reranker dispatches (``rerank_route``) and the live row's shape:
    one search holds $0.0025 before it is sent and settles at $0.0025, never the unpriced stand-in and never $0."""
    from matrx_ai.providers import guardrail_gate
    from matrx_ai.providers.cohere.rerank import rerank_route, rerank_search_units_at_most

    lookup = _live_lookup()
    monkeypatch.setattr("matrx_ai.config.usage_config._get_db_pricing_lookup", lambda: lookup)
    documents = ["a short passage about a slow kitchen drain"] * 20
    units = rerank_search_units_at_most(documents)
    assert units == 1

    quote = guardrail_gate.quote_units(rerank_route(LIVE_MODEL), units)
    assert quote is not None, "the run budget could not price a rerank: it would hold the unpriced stand-in"
    assert quote.worst_usd() == USD_PER_SEARCH

    response = SimpleNamespace(id="r", meta=SimpleNamespace(billed_units=SimpleNamespace(search_units=1)))
    settled = rerank_usage(response, model=LIVE_MODEL, documents=documents).calculate_cost(lookup)
    assert settled == USD_PER_SEARCH == quote.worst_usd()


def test_the_rerank_wire_and_model_kind_are_known_to_the_catalog():
    """The live ``ai.api`` row's translator_key compiles (an unknown one quarantines the offering, which unprices it),
    and the live model row's ``interaction`` is in the vocabulary and is refused as a chat model."""
    from matrx_ai.catalog.manager import WIRE_FORMATS
    from matrx_ai.catalog.routes import client_attr_for_wire_format
    from matrx_ai.providers.capability_vocabulary import normalize_capabilities
    from matrx_ai.providers.model_channel_gate import ModelNotForChatError

    assert COHERE_RERANK_API in WIRE_FORMATS
    assert client_attr_for_wire_format(COHERE_RERANK_API) == "rerank"
    live_capabilities = {"input": ["text"], "output": [], "features": [], "interaction": "rerank", "multilingual": True}
    checked = normalize_capabilities(live_capabilities, label=LIVE_MODEL)
    assert not checked.rejections and not checked.corrections
    refusal = ModelNotForChatError(model_name=LIVE_MODEL, channel="rerank", wire_format=COHERE_RERANK_API)
    assert "reranking model" in refusal.user_message
