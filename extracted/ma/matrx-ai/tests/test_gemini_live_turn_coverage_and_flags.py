"""Gemini Live's newest turn coverage reaches the wire; the long_decode flag is catalog data;
a multi-call Gemini answer (segmented TTS, long-decode hops) bills every call like one call.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from google.genai import types

from matrx_ai.catalog.models import ControlRule
from matrx_ai.providers.capability_vocabulary import FEATURE_KEYS, normalize_capabilities
from matrx_ai.providers.google.specialized import GoogleLiveOptions, build_live_config
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities
from matrx_ai.testing.profile_factory import make_profile

AUDIO_AND_VIDEO = "TURN_INCLUDES_AUDIO_ACTIVITY_AND_ALL_VIDEO"


def _live_profile():
    return make_profile(
        model_name="gemini-3.8-live",
        wire_format="google_live",
        capabilities={"input": ["audio", "video"], "output": ["audio"], "features": ["live_api"], "interaction": "realtime"},
        rules={
            "turn_coverage": ControlRule.model_validate({}),
            "response_modalities": ControlRule.model_validate({}),
        },
    )


@pytest.mark.parametrize("value", ["TURN_INCLUDES_ONLY_ACTIVITY", "TURN_INCLUDES_ALL_INPUT", AUDIO_AND_VIDEO])
def test_every_turn_coverage_value_reaches_the_live_config(value):
    config = build_live_config(_live_profile(), GoogleLiveOptions(turn_coverage=value))
    assert config.realtime_input_config.turn_coverage == types.TurnCoverage(value)


def test_an_unknown_turn_coverage_is_refused():
    with pytest.raises(ValueError):
        GoogleLiveOptions(turn_coverage="TURN_INCLUDES_EVERYTHING")


def test_long_decode_is_a_canonical_feature_that_resolves_to_a_flag():
    assert "long_decode" in FEATURE_KEYS
    normalized = normalize_capabilities({"input": ["text"], "output": ["text"], "features": ["long_decode"], "interaction": "turn"})
    assert not normalized.rejections
    on = resolve_model_capabilities(SimpleNamespace(name="argon", capabilities=normalized.value))
    off = resolve_model_capabilities(
        SimpleNamespace(name="flash", capabilities={"input": ["text"], "output": ["text"], "features": [], "interaction": "turn"})
    )
    assert on.supports_long_decode is True
    assert off.supports_long_decode is False


def test_multi_call_usage_bills_cached_and_thinking_like_a_single_call():
    """Until 2026-10-16 the multi-call sum billed cached tokens at the full input rate and
    dropped thinking tokens."""

    def call(prompt, cached, out, thoughts):
        return SimpleNamespace(
            prompt_token_count=prompt,
            cached_content_token_count=cached,
            candidates_token_count=out,
            thoughts_token_count=thoughts,
        )

    usage = GoogleTranslator.summed_gemini_usage(
        [call(1_000, 0, 100, 10), call(1_000, 800, 200, 20)],
        matrx_model_name="gemini-test",
        provider_model_name="gemini-test-001",
        response_id="r2",
    )
    assert (usage.input_tokens, usage.cached_input_tokens, usage.output_tokens) == (1_200, 800, 330)
    assert usage.metadata["segmented_provider_calls"] == 2
    assert (usage.provider_model_name, usage.response_id) == ("gemini-test-001", "r2")
