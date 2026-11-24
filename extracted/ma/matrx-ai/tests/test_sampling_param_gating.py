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

import pytest

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


@pytest.mark.parametrize(
    "settings",
    [
        {"temperature": 0.25},
        {"temperature": 1, "reasoning_effort": "high"},
        {"top_p": 0.97, "reasoning_effort": "high"},
        {"temperature": 0.25, "top_k": 40, "top_p": 0.5, "reasoning_effort": "high"},
    ],
    ids=["temperature", "temperature_1_thinking", "top_p_thinking", "all_with_thinking"],
)
def test_anthropic_never_sends_a_sampling_parameter(settings):
    # API 2026-10-21 (anthropic>=2.0) refuses temperature/top_p/top_k on EVERY model; the
    # catalog marks them supported:false, so none reaches the request, top-level or extra_body.
    req = AnthropicTranslator().to_anthropic(_config(**settings), _anthropic_profile())
    assert "extra_body" not in req, "no sampling knob is sent — no empty container on the wire"
    for key in ("temperature", "top_k", "top_p"):
        assert key not in req
    if settings.get("reasoning_effort") == "high":
        assert "thinking" in req, "high reasoning_effort still enables a thinking block"
