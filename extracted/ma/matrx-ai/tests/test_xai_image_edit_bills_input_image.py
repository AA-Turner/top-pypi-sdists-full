"""An xAI image edit bills the INPUT image too (provider: docs.x.ai image guide).

Before this guard, an edit recorded only the output image, so the catalog cost
read $0.02 where xAI charged $0.022 (ai.pricing.provider_catalog_drift).
"""

import pytest

from matrx_ai.config import usage_config
from matrx_ai.config.usage_config import ModelPricing, TokenUsage, _tiers_from_pricing_field
from matrx_ai.providers.xai.xai_image_api import XAIImageGeneration

MODEL = "grok-imagine-image"
TIER = {
    "max_tokens": None,
    "input_price": 0,
    "usage_basis": "image_output",
    "output_price": 0.02,
    "component_prices": {"service.input_image": 2000},
    "cached_input_price": 0,
}


def test_request_counts_every_input_image():
    gen = XAIImageGeneration()
    assert gen._request_billing_components({"image_url": "x"}) == {"service.input_image": 1}
    assert gen._request_billing_components({"image_urls": ["a", "b"]}) == {"service.input_image": 2}
    assert gen._request_billing_components({"prompt": "p"}) == {}


def test_edit_costs_output_plus_input_image(monkeypatch):
    lookup = {MODEL: ModelPricing(model_name=MODEL, api="xai", tiers=_tiers_from_pricing_field([TIER]))}
    monkeypatch.setattr(usage_config, "_pricing_lookup_cache", lookup)
    components = XAIImageGeneration()._request_billing_components({"image_url": "x"})
    usage = TokenUsage(
        input_tokens=0,
        output_tokens=1_000_000,
        matrx_model_name=MODEL,
        api="xai",
        billing_components=components,
    )
    assert usage.calculate_cost(lookup) == pytest.approx(0.022)
