"""Gemini Live bills audio/image/video tokens at their own rates; text is the base rate.

``live_usage`` turns Live's per-modality token details into ``billing_components`` so
``ai.offering.pricing[].component_prices`` (input.audio $3, output.audio $12 per 1M on
gemini-3.8-live) applies to the audio subset and the text rate ($0.75 / $4.50) to the rest.
"""

from matrx_ai.config.usage_config import ModelPricing, PricingTier
from matrx_ai.providers.google.live_history import live_modality_components, live_usage


def test_modality_details_become_components_either_spelling():
    snake = {
        "prompt_token_count": 1000,
        "response_token_count": 500,
        "prompt_tokens_details": [{"modality": "AUDIO", "token_count": 800}, {"modality": "TEXT", "token_count": 200}],
        "response_tokens_details": [{"modality": "AUDIO", "token_count": 450}, {"modality": "TEXT", "token_count": 50}],
    }
    camel = {
        "promptTokenCount": 1000,
        "promptTokensDetails": [{"modality": "AUDIO", "tokenCount": 800}],
        "responseTokensDetails": [{"modality": "AUDIO", "tokenCount": 450}],
    }
    expected = {"input.audio": 800, "output.audio": 450}
    assert live_modality_components(snake) == expected
    assert live_modality_components(camel) == expected


def test_cached_audio_comes_off_uncached_audio():
    usage = {
        "prompt_tokens_details": [{"modality": "AUDIO", "token_count": 800}],
        "cache_tokens_details": [{"modality": "AUDIO", "token_count": 300}],
    }
    assert live_modality_components(usage) == {"input.audio": 500, "cached_input.audio": 300}


def test_a_live_turn_prices_audio_at_audio_rates():
    usage = live_usage(
        {
            "prompt_token_count": 1_000_000,
            "response_token_count": 1_000_000,
            "prompt_tokens_details": [{"modality": "AUDIO", "token_count": 600_000}, {"modality": "TEXT", "token_count": 400_000}],
            "response_tokens_details": [{"modality": "AUDIO", "token_count": 1_000_000}],
        },
        model="gemini-3.1-flash-live-preview",
        provider_model="gemini-3.8-live",
    )
    pricing = ModelPricing(
        model_name="gemini-3.1-flash-live-preview",
        api="google",
        tiers=[
            PricingTier(
                max_tokens=None,
                input_price=0.75,
                output_price=4.5,
                cached_input_price=0.0,
                component_prices={"input.audio": 3.0, "input.image": 1.0, "input.video": 1.0, "output.audio": 12.0},
            )
        ],
    )
    cost = usage.calculate_cost({"gemini-3.1-flash-live-preview": pricing})
    # input: 0.4M text * 0.75 + 0.6M audio * 3; output: 1M audio * 12
    assert abs(cost - (0.3 + 1.8 + 12.0)) < 1e-9
