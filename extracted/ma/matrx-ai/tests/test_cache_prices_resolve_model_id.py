"""model_cache_prices prices a model referenced by catalog ID, not only by name.

Live defect (2026-10-24): the request config carries the model_definition ID, the pricing
lookup is keyed by offering id and model NAME, so every send recorded read_price=null and the
payback gate fell back to its legacy floor. An unknown ref must still come back unpriced.
"""

from __future__ import annotations

import matrx_ai.config.usage_config as usage_config
from matrx_ai.catalog.manager import ai_catalog_manager
from matrx_ai.config.send_boundary import model_cache_prices
from matrx_ai.config.usage_config import ModelPricing, PricingTier

MODEL_ID = "00000000-0000-4000-8000-000000000001"
NAME = "claude-test-model"

PRICING = ModelPricing(
    model_name=NAME,
    api="anthropic",
    tiers=[
        PricingTier(
            max_tokens=None,
            input_price=4.0,
            output_price=20.0,
            cached_input_price=0.2,
            cache_hit_price=0.2,
            cache_write_5m_price=5.0,
            cache_write_1h_price=8.0,
        )
    ],
)


def _install(monkeypatch) -> None:
    monkeypatch.setattr(usage_config, "_get_db_pricing_lookup", lambda: {NAME: PRICING})
    monkeypatch.setattr(
        ai_catalog_manager, "resolve_model_ref", lambda ref: MODEL_ID if ref in (MODEL_ID, NAME) else ref
    )
    monkeypatch.setattr(
        ai_catalog_manager,
        "model_state",
        lambda mid: {"id": MODEL_ID, "name": NAME} if mid == MODEL_ID else {},
    )


def test_model_id_is_priced(monkeypatch) -> None:
    _install(monkeypatch)
    result = model_cache_prices(MODEL_ID)
    assert result is not None
    prices, ttl = result
    assert prices is not None
    assert (prices.read_price, prices.write_price, prices.input_price) == (0.2, 5.0, 4.0)
    assert ttl == 300


def test_model_name_still_priced(monkeypatch) -> None:
    _install(monkeypatch)
    prices, _ = model_cache_prices(NAME)
    assert prices is not None and prices.read_price == 0.2


def test_unknown_ref_stays_unpriced(monkeypatch) -> None:
    _install(monkeypatch)
    assert model_cache_prices("11111111-1111-4111-8111-111111111111") is None
