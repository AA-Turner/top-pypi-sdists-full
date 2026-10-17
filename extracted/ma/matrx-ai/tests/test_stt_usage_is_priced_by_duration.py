"""A transcription is priced by its audio duration, never alarmed as an unpriced 0-token call.

THE BREAK (2026-10-16, 25 occurrences): the spend gate asked the call's usage for a catalog cost; a
transcription's usage is an ``STTUsage`` (seconds, no token fields) with no ``calculate_catalog_cost``, so the
AttributeError read as "no price" and every Groq whisper call alarmed ``Model calls are unpriced ... 0 tokens``.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.usage_config import ModelPricing, PricingTier
from matrx_ai.processing.audio.stt import STTUsage
from matrx_ai.providers.unified_client import billable_usage, catalog_cost_or_none


def _lookup(basis: str, price: float) -> dict[str, ModelPricing]:
    tier = PricingTier(max_tokens=None, input_price=price, output_price=0.0, cached_input_price=0.0, usage_basis=basis)
    return {"offering-1": ModelPricing(model_name="whisper-large-v3-turbo", api="groq", tiers=[tier])}


def _usage(basis: str, seconds: float) -> STTUsage:
    return STTUsage(
        duration_seconds=seconds, billed_duration=seconds, model="whisper-large-v3-turbo",
        matrx_model_name="whisper-large-v3-turbo", api="groq", offering_id="offering-1", usage_basis=basis,
    )


@pytest.mark.asyncio
async def test_one_hour_of_groq_whisper_costs_the_hourly_list_price(monkeypatch: pytest.MonkeyPatch) -> None:
    lookup = _lookup("audio_hour_input", 0.04)

    async def _ensure() -> dict[str, ModelPricing]:
        return lookup

    monkeypatch.setattr("matrx_ai.config.usage_config.ensure_pricing_lookup", _ensure)
    cost = await catalog_cost_or_none(_usage("audio_hour_input", 3600.0))
    assert cost == pytest.approx(0.04)


def test_a_token_usage_is_left_alone() -> None:
    token_usage = _usage("audio_hour_input", 60.0).to_token_usage()
    assert billable_usage(token_usage) is token_usage
