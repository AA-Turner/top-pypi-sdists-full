"""Regression tests for sampling-param (temperature / top_p / top_k) gating.

The platform's contract: a translator MUST DROP any sampling param a model's
api_class cannot accept, rather than sending it and letting the provider 400.

Two provider families enforce this:

* OpenAI Responses API — the reasoning api_classes (gpt-5.x:
  ``openai_reasoning_minimal`` / ``openai_reasoning`` /
  ``openai_reasoning_xhigh``) reject ``temperature`` and ``top_p`` with
  ``400 Unsupported parameter: 'temperature' is not supported with this model``.
  Only ``openai_standard`` accepts them.
* Anthropic — when an extended/adaptive ``thinking`` block is present the API
  rejects ``temperature != 1`` and any ``top_k``, and only accepts ``top_p`` in
  [0.95, 1].

These tests lock both gates so the "send it and let the API reject" regression
(which broke gpt-5.5 in production) cannot come back.
"""

from __future__ import annotations

from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator


def _config(**kwargs) -> UnifiedConfig:
    base = {
        "model": "test-model",
        "messages": [UnifiedMessage(role="user", content=[TextContent(text="hi")])],
    }
    base.update(kwargs)
    return UnifiedConfig(**base)


# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------


def _openai_profile(family: str):
    """Profile carrying the REAL rule snapshot for the family (golden fixture)."""
    from matrx_ai.testing.profile_factory import make_profile

    from test_chat_param_golden import load_golden

    payload = load_golden(family)
    return make_profile(
        model_name="test-model",
        wire_format=payload["wire_format"],
        rules=payload["rules"],
        value_orders=payload["value_orders"],
    )


def test_openai_standard_keeps_temperature_and_top_p():
    cfg = _config(temperature=0.25, top_p=0.9)
    req = OpenAITranslator().to_openai(cfg, _openai_profile("openai_standard"))
    assert req["temperature"] == 0.25
    assert req["top_p"] == 0.9


def test_openai_reasoning_drops_temperature_and_top_p():
    for family in (
        "openai_reasoning_minimal",
        "openai_reasoning",
        "openai_reasoning_xhigh",
    ):
        cfg = _config(temperature=0.25, top_p=0.9)
        req = OpenAITranslator().to_openai(cfg, _openai_profile(family))
        assert "temperature" not in req, f"{family} must drop temperature"
        assert "top_p" not in req, f"{family} must drop top_p"


# ---------------------------------------------------------------------------
# Anthropic
# ---------------------------------------------------------------------------


def _anthropic_profile():
    from matrx_ai.testing.profile_factory import make_profile

    from test_chat_param_golden import load_golden

    payload = load_golden("anthropic_standard")
    return make_profile(
        model_name="test-model",
        wire_format=payload["wire_format"],
        rules=payload["rules"],
        value_orders=payload["value_orders"],
    )


def test_anthropic_no_thinking_keeps_temperature():
    cfg = _config(temperature=0.25)
    req = AnthropicTranslator().to_anthropic(cfg, _anthropic_profile())
    assert "thinking" not in req
    assert req["temperature"] == 0.25


def test_anthropic_thinking_drops_incompatible_sampling_params():
    cfg = _config(temperature=0.25, top_k=40, top_p=0.5, reasoning_effort="high")
    req = AnthropicTranslator().to_anthropic(cfg, _anthropic_profile())
    assert "thinking" in req, "high reasoning_effort should enable a thinking block"
    assert "temperature" not in req
    assert "top_k" not in req
    assert "top_p" not in req


def test_anthropic_thinking_keeps_temperature_1():
    cfg = _config(temperature=1, reasoning_effort="high")
    req = AnthropicTranslator().to_anthropic(cfg, _anthropic_profile())
    assert "thinking" in req
    assert req["temperature"] == 1


def test_anthropic_thinking_keeps_in_range_top_p():
    # top_p only (no temperature, so the mutual-exclusion guard leaves it).
    cfg = _config(top_p=0.97, reasoning_effort="high")
    req = AnthropicTranslator().to_anthropic(cfg, _anthropic_profile())
    assert "thinking" in req
    assert req["top_p"] == 0.97
