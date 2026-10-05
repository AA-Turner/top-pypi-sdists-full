"""Engine fixes for the V3 live failures the settings live fuzz found (2026-10-04).

Chair rulings: R-a — a translation never DEFEATS what the person explicitly set (an output
cap is honoured, a list is capped never emptied); R-b — an empty answer is a failure.
Each case below was a live failure (conversation ids in the V3 verifier report) and each
test fails on the pre-fix engine (proven by reverting the fix, 2026-10-04).
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule
from matrx_ai.providers.outbound_params import resolve_outbound_params

EFFORT_ORDER = ["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"]


def _wire(rules: dict[str, dict], **config) -> dict:
    controls = CompiledControlsMap(
        rules={k: ControlRule.model_validate(v) for k, v in rules.items()},
        value_orders={"reasoning_effort": EFFORT_ORDER},
    )
    return resolve_outbound_params(SimpleNamespace(**config), controls)


# Groq / Cerebras live: ``stop: [""]`` reached the wire, the model stopped at once and the
# person got no answer (1827d80f, a62373b6). The cell only caps the count.
GROQ_STOP = {"stop_sequences": {"provider_key": "stop", "max_items": 4}}


def test_a_blank_stop_never_reaches_any_wire():
    assert "stop" not in _wire(GROQ_STOP, stop_sequences=[""])
    assert "stop" not in _wire({"stop_sequences": {"provider_key": "stop"}}, stop_sequences=["  "])


def test_real_stops_survive_beside_a_blank_one():
    assert _wire(GROQ_STOP, stop_sequences=["", "END"])["stop"] == ["END"]


# Claude live: effort max + max_output_tokens 50 sent max_tokens 26624 (e7c78e54).
CLAUDE_BUDGET = {
    "reasoning_effort": {
        "processor": "anthropic_thinking",
        "processor_config": {"mode": "budget", "consumes": ["thinking_budget"]},
    },
    "max_output_tokens": {"provider_key": "max_tokens"},
}


def test_claude_explicit_cap_below_the_thinking_floor_is_honoured():
    wire = _wire(CLAUDE_BUDGET, reasoning_effort="max", max_output_tokens=50)
    assert wire["max_tokens"] == 50
    assert "thinking" not in wire


def test_claude_explicit_cap_shrinks_the_budget_and_leaves_room_to_answer():
    wire = _wire(CLAUDE_BUDGET, reasoning_effort="max", max_output_tokens=8000)
    assert wire["max_tokens"] == 8000
    assert 1024 <= wire["thinking"]["budget_tokens"] < 8000


# GPT-5 live: max_output_tokens 0/1 raised to 16 (the provider minimum) and the default /
# max effort spent all 16 thinking — "I used my whole output limit thinking" (1d46f3ea).
GPT5 = {
    "max_output_tokens": {"provider_key": "max_output_tokens", "clamp": {"min": 16}},
    "reasoning_effort": {
        "provider_key": "reasoning.effort",
        "off": {"send": "minimal"},
        "value_map": {"auto": None, "none": "minimal", "minimal": "minimal", "low": "low",
                      "medium": "medium", "high": "high", "xhigh": "high"},
    },
}


def test_tiny_output_cap_lowers_reasoning_so_an_answer_fits():
    for cap in (0, 1):
        wire = _wire(GPT5, max_output_tokens=cap)
        assert wire["max_output_tokens"] == 16
        assert wire["reasoning"]["effort"] == "minimal"
    wire = _wire(GPT5, max_output_tokens=1, reasoning_effort="high")
    assert wire["reasoning"]["effort"] == "minimal"


def test_a_roomy_cap_keeps_the_asked_effort():
    wire = _wire(GPT5, max_output_tokens=8000, reasoning_effort="high")
    assert wire["reasoning"]["effort"] == "high"


# Gemini 2.5 Flash live (FUZZ-2, 2026-10-04): cap 16 with dynamic thinking -> MAX_TOKENS, no
# text; thinking budget 0 -> "ok". The thinking budget yields to a tiny cap; a roomy cap keeps it.
GEMINI_FLASH = {
    "max_output_tokens": {"provider_key": "max_output_tokens", "clamp": {"min": 16}},
    "reasoning_effort": {
        "off": {"send": 0},
        "processor": "google_thinking",
        "supported": True,
        "provider_key": "thinking_config.thinking_budget",
        "processor_config": {
            "mode": "legacy",
            "consumes": ["thinking_budget", "thinking_level", "include_thoughts"],
            "max_thinking_budget": 24576,
        },
    },
}


def test_gemini_tiny_cap_turns_thinking_off_so_an_answer_fits():
    for cap in (0, 1, 16):
        wire = _wire(GEMINI_FLASH, max_output_tokens=cap, reasoning_effort="high")
        assert wire["max_output_tokens"] >= 16, wire
        assert wire["thinking_config"]["thinking_budget"] == 0, wire


def test_gemini_roomy_cap_keeps_the_asked_thinking():
    wire = _wire(GEMINI_FLASH, max_output_tokens=8000, reasoning_effort="high")
    assert wire["thinking_config"]["thinking_budget"] > 0, wire


# FUZZ-2 2026-10-04: thinking_level "none" was a request-validation 422. Convert, never refuse.
def test_thinking_level_off_the_gemini_scale_converts_onto_reasoning_effort():
    from matrx_ai.config.llm_params import LLMParams

    assert LLMParams.model_validate({"thinking_level": "none"}).reasoning_effort == "none"
    assert LLMParams.model_validate({"thinking_level": "max"}).reasoning_effort == "max"
    kept = LLMParams.model_validate({"thinking_level": "none", "reasoning_effort": "low"})
    assert kept.reasoning_effort == "low" and kept.thinking_level is None
    assert LLMParams.model_validate({"thinking_level": "auto"}).reasoning_effort is None
    assert LLMParams.model_validate({"thinking_level": "High"}).thinking_level == "high"
