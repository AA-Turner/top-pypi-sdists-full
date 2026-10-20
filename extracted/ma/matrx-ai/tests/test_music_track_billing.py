"""A music model (Lyria) is priced per generated track while the Gemini API reports tokens.

Before migration 1494 the Lyria offerings carried the unknown basis ``per_song`` and a call recorded a token-only cost
of about $0.00001 for a track that costs $0.04-$0.08. These tests lock the contract: tier ``audio_unit_output`` bills
one unit per generated track, and every other basis (a TTS model returning audio) is left exactly as reported.
"""

from __future__ import annotations

import pytest

from matrx_ai.config import usage_config as uc
from matrx_ai.config.usage_config import ModelPricing, PricingTier, TokenUsage, apply_track_billing


@pytest.fixture
def warm_pricing():
    saved, warned = uc._pricing_lookup_cache, set(uc._billing_warned)
    uc._billing_warned.clear()
    uc._pricing_lookup_cache = {
        "lyria-3.5": ModelPricing("lyria-3.5", "google_chat", [PricingTier(None, input_price=0, output_price=0.08, cached_input_price=0, usage_basis="audio_unit_output")]),
        "gemini-tts": ModelPricing("gemini-tts", "google_chat", [PricingTier(None, input_price=0.5, output_price=10, cached_input_price=0.05, usage_basis=None)]),
    }
    yield
    uc._pricing_lookup_cache = saved
    uc._billing_warned.clear()
    uc._billing_warned.update(warned)


def _usage(model: str) -> TokenUsage:
    return TokenUsage(input_tokens=27, output_tokens=1920, matrx_model_name=model, provider_model_name=model, api="google_chat")


def test_a_track_is_billed_per_track_not_per_token(warm_pricing):
    u = _usage("lyria-3.5")
    assert apply_track_billing(u, tracks=1, matrx_model_name="lyria-3.5", api="google_chat") is True
    assert u.calculate_cost() == pytest.approx(0.08)
    assert u.metadata["billed_tracks"] == 1
    assert u.metadata["provider_reported_tokens"] == {"input_tokens": 27, "output_tokens": 1920, "cached_input_tokens": 0}


def test_two_tracks_cost_two_units(warm_pricing):
    u = _usage("lyria-3.5")
    apply_track_billing(u, tracks=2, matrx_model_name="lyria-3.5", api="google_chat")
    assert u.calculate_cost() == pytest.approx(0.16)


def test_a_token_priced_model_that_returns_audio_is_left_alone(warm_pricing):
    u = _usage("gemini-tts")
    before = (u.input_tokens, u.output_tokens)
    assert apply_track_billing(u, tracks=1, matrx_model_name="gemini-tts", api="google_chat") is False
    assert (u.input_tokens, u.output_tokens) == before and "billed_tracks" not in u.metadata


def test_no_track_no_charge_change(warm_pricing):
    u = _usage("lyria-3.5")
    assert apply_track_billing(u, tracks=0, matrx_model_name="lyria-3.5", api="google_chat") is False
    assert apply_track_billing(None, tracks=1, matrx_model_name="lyria-3.5", api="google_chat") is False
