"""THE PLATFORM REASONING DEFAULT — owner ruling, 2026-10-24.

"When you don't provide a thinking level ... it is supposed to default to our
platform default, which is low. When we're given a thinking level, we use it.
If we are told explicitly that the thinking level is to be set to auto ... then
we send that to the provider if the provider offers that. In every other
instance, we hard set it to low."

Per provider dialect, on the WIRE (config -> canonicalize -> outbound):
  unset          -> low
  explicit level -> that level
  explicit auto  -> the provider's own auto only where it natively offers one
                    (Gemini dynamic thinking, Together omission, a value_map
                    "auto" word), else low.

Regression this pins: ai_041 (8fe4182ff49, 2026-07-11) made "auto" == UNSET
and the B1/C5 translation layer made "NOT SET SENDS NOTHING", so every agent
without a stored level ran at the PROVIDER's default (Gemini 3: high, OpenAI:
medium) — 58k thinking tokens for a 7k answer on one Smart Add job.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog.canonicalize import canonical_settings_from_config
from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.families import SettingFamilies
from matrx_ai.catalog.models import CatalogSetting, ControlRule

_ANTHROPIC_BUDGET = {
    "reasoning_effort": {
        "processor": "anthropic_thinking",
        "processor_config": {"mode": "budget", "order": 100,
                             "consumes": ["thinking_budget", "thinking_level"]},
        "ui_values": ["auto", "none", "low", "medium", "high"],
    },
    "max_output_tokens": {"provider_key": "max_tokens"},
}
_ANTHROPIC_ADAPTIVE = {
    "reasoning_effort": {
        "processor": "anthropic_thinking",
        "processor_config": {"mode": "adaptive", "order": 100,
                             "consumes": ["thinking_budget", "thinking_level"]},
    },
    "max_output_tokens": {"provider_key": "max_tokens"},
}
_GEMINI_3 = {
    "reasoning_effort": {
        "processor": "google_thinking",
        "provider_key": "thinking_config",
        "processor_config": {"mode": "gemini_3", "family": "flash", "order": 100,
                             "consumes": ["thinking_budget", "thinking_level"]},
        "ui_values": ["auto", "none", "minimal", "low", "medium", "high"],
    },
}
_GEMINI_25 = {
    "reasoning_effort": {
        "processor": "google_thinking",
        "processor_config": {"mode": "legacy", "order": 100,
                             "consumes": ["thinking_budget", "thinking_level"]},
    },
}
_OPENAI = {
    "reasoning_effort": {
        "provider_key": "reasoning.effort",
        "value_map": {"auto": None, "none": "none", "minimal": "low", "low": "low",
                      "medium": "medium", "high": "high", "xhigh": "xhigh", "max": "xhigh"},
    },
}
_XAI = {"reasoning_effort": {"ui_values": ["auto", "low", "medium", "high", "xhigh"]}}
_TOGETHER = {
    "reasoning_effort": {
        "processor": "together_reasoning",
        "processor_config": {"order": 100},
        "ui_values": ["auto", "none", "high", "xhigh"],
    },
}
_NON_REASONING = {"reasoning_effort": {"supported": False}, "temperature": {}}


def _controls(rules: dict[str, dict[str, Any]], *, setting_default: Any = None) -> CompiledControlsMap:
    families = None
    if setting_default is not None:
        families = SettingFamilies.from_settings(
            {"reasoning_effort": CatalogSetting(key="reasoning_effort", value_type="enum",
                                                default_value=setting_default, family="reasoning")}
        )
    return CompiledControlsMap(
        rules={k: ControlRule.model_validate(v) for k, v in rules.items()}, families=families
    )


def _wire(rules: dict[str, dict[str, Any]], **config: Any) -> dict[str, Any]:
    canonical = canonical_settings_from_config(SimpleNamespace(**config))
    params, _ = _controls(rules).outbound(canonical)
    return params


# ── unset -> low, every dialect ──────────────────────────────────────────────
def test_unset_openai_sends_low():
    assert _wire(_OPENAI)["reasoning"] == {"effort": "low"}


def test_unset_xai_sends_low():
    assert _wire(_XAI)["reasoning_effort"] == "low"


def test_unset_gemini_3_sends_low_level():
    assert _wire(_GEMINI_3)["thinking_config"]["thinking_level"] == "low"


def test_unset_gemini_25_sends_low_budget():
    assert _wire(_GEMINI_25)["thinking_config"]["thinking_budget"] == 1024


def test_unset_anthropic_budget_sends_low_budget():
    assert _wire(_ANTHROPIC_BUDGET)["thinking"] == {"type": "enabled", "budget_tokens": 1024}


def test_unset_anthropic_adaptive_sends_low_effort():
    assert _wire(_ANTHROPIC_ADAPTIVE)["output_config"] == {"effort": "low"}


def test_unset_together_without_low_sends_its_lowest_offered_level():
    # Together's declared choices have no "low": the default is the nearest
    # level it OFFERS (never the provider's own unset depth, never "none").
    assert _wire(_TOGETHER) == {"reasoning_effort": "high"}


def test_together_offering_low_never_sends_high_for_unset_or_low():
    # DeepSeek-V4-Flash on Together lists "low"; the processor used to map every
    # effort short of xhigh to "high".
    rules = {"reasoning_effort": {**_TOGETHER["reasoning_effort"],
                                  "ui_values": ["auto", "none", "low", "high", "xhigh"]}}
    assert _wire(rules) == {"reasoning_effort": "low"}
    assert _wire(rules, reasoning_effort="low") == {"reasoning_effort": "low"}
    assert _wire(rules, reasoning_effort="xhigh") == {"reasoning_effort": "max"}


def test_an_on_off_only_listing_keeps_its_own_unset():
    rules = {"reasoning_effort": {"ui_values": ["auto", "none"]}}
    assert _wire(rules) == {}


def test_value_map_without_low_gets_its_nearest_level():
    rules = {"reasoning_effort": {"value_map": {"none": "off", "medium": "medium", "high": "high"}}}
    assert _wire(rules) == {"reasoning_effort": "medium"}


def test_accepts_without_low_gets_its_nearest_level_quietly():
    params, adjustments = _controls(
        {"reasoning_effort": {"accepts": ["high", "max"]}}
    ).outbound({})
    assert params == {"reasoning_effort": "high"}
    assert adjustments == []


def test_unset_together_offering_low_sends_low():
    rules = {"reasoning_effort": {**_TOGETHER["reasoning_effort"],
                                  "ui_values": ["auto", "none", "low", "high"],
                                  "processor_config": {"order": 100, "effort_map": {"low": "low"}}}}
    assert _wire(rules) == {"reasoning_effort": "low"}


def test_non_reasoning_model_gets_nothing():
    assert _wire(_NON_REASONING, temperature=0.3) == {"temperature": 0.3}


# ── explicit level passes through ────────────────────────────────────────────
@pytest.mark.parametrize("level", ["medium", "high"])
def test_explicit_level_openai(level):
    assert _wire(_OPENAI, reasoning_effort=level)["reasoning"] == {"effort": level}


def test_explicit_level_gemini_3():
    assert _wire(_GEMINI_3, reasoning_effort="high")["thinking_config"]["thinking_level"] == "high"


def test_explicit_none_is_off_not_low():
    assert _wire(_ANTHROPIC_BUDGET, reasoning_effort="none").get("thinking") is None


def test_explicit_budget_is_a_level():
    assert _wire(_ANTHROPIC_BUDGET, thinking_budget=8192)["thinking"]["budget_tokens"] == 8192


# ── explicit auto ────────────────────────────────────────────────────────────
def test_auto_gemini_3_is_native_auto():
    # Gemini offers dynamic thinking: the level is left to the model.
    assert "thinking_level" not in _wire(_GEMINI_3, reasoning_effort="auto").get("thinking_config", {})


def test_auto_gemini_25_is_native_auto():
    assert "thinking_budget" not in _wire(_GEMINI_25, reasoning_effort="auto").get("thinking_config", {})


def test_auto_openai_has_no_auto_so_low():
    assert _wire(_OPENAI, reasoning_effort="auto")["reasoning"] == {"effort": "low"}


def test_auto_anthropic_budget_has_no_auto_so_low():
    assert _wire(_ANTHROPIC_BUDGET, reasoning_effort="auto")["thinking"]["budget_tokens"] == 1024


def test_auto_with_a_provider_word_sends_it():
    rules = {"reasoning_effort": {"value_map": {"auto": "auto", "low": "low"}}}
    assert _wire(rules, reasoning_effort="auto") == {"reasoning_effort": "auto"}


def test_auto_raw_in_a_session_dict_is_decided_the_same_way():
    # Session seams hand outbound a raw dict (no canonicalize pass).
    params, _ = _controls(_OPENAI).outbound({"reasoning_effort": "auto"})
    assert params["reasoning"] == {"effort": "low"}


# ── the default is DATA (ai.setting.default_value) ───────────────────────────
def test_setting_default_value_is_the_platform_default():
    params, _ = _controls(_OPENAI, setting_default="medium").outbound({})
    assert params["reasoning"] == {"effort": "medium"}


def test_a_cell_default_deeper_than_low_never_wins_unset():
    rules = {"reasoning_effort": {**_OPENAI["reasoning_effort"], "default": "medium"}}
    assert _wire(rules)["reasoning"] == {"effort": "low"}


def test_a_cell_default_auto_never_arises_implicitly():
    rules = {"reasoning_effort": {**_OPENAI["reasoning_effort"], "default": "auto"}}
    assert _wire(rules)["reasoning"] == {"effort": "low"}


def test_a_listing_that_does_not_offer_low_keeps_its_own_default():
    # A "-max" listing's choices are ["xhigh","max"]; its declared default rides.
    rules = {"reasoning_effort": {"ui_values": ["xhigh", "max"], "default": "xhigh"}}
    assert _wire(rules) == {"reasoning_effort": "xhigh"}


def test_a_shallower_cell_default_stays():
    rules = {"thinking_level": {"value_map": {"minimal": "MINIMAL", "low": "LOW"}, "default": "MINIMAL"}}
    assert _wire(rules) == {"thinking_level": "MINIMAL"}


def test_the_default_never_defeats_a_set_temperature_on_anthropic():
    # Thinking forces Anthropic's temperature to 1; a person's 0.25 wins over
    # the platform default (a translation never defeats an explicit setting).
    rules = {**_ANTHROPIC_BUDGET,
             "temperature": {"processor": "anthropic_temp_topp_exclusion",
                             "processor_config": {"order": 200, "consumes": ["top_p", "top_k"]}}}
    params = _wire(rules, temperature=0.25)
    assert "thinking" not in params
    assert params["temperature"] == 0.25


# ── a FORCED tool call never rides manual thinking (Anthropic 400s) ──────────
# Docs: manual (budget) extended thinking supports tool_choice auto/none only;
# the orchestrator's required-member intervention forces one mid-loop.
def _seam(rules: dict[str, dict[str, Any]], **config: Any) -> dict[str, Any]:
    from matrx_ai.providers.outbound_params import resolve_outbound_params

    return resolve_outbound_params(SimpleNamespace(model="guard-model", **config), _controls(rules))


def test_forced_tool_unset_level_sends_no_budget_thinking():
    assert "thinking" not in _seam(_ANTHROPIC_BUDGET, tool_choice="required")


def test_forced_tool_explicit_level_drops_thinking_for_that_turn_and_records_it():
    from matrx_ai.catalog import translation_defaults as D

    params, adjustments = _controls(_ANTHROPIC_BUDGET).outbound(
        {"reasoning_effort": "high", D.FORCED_TOOL_CHOICE_KEY: True}
    )
    assert "thinking" not in params
    assert any(a.key == "reasoning_effort" and a.action == "dropped" for a in adjustments)
    assert "thinking" not in _seam(_ANTHROPIC_BUDGET, tool_choice="required", reasoning_effort="high")


def test_forced_tool_on_adaptive_keeps_the_default():
    # Adaptive thinking accepts a forced tool call: nothing changes there.
    assert _seam(_ANTHROPIC_ADAPTIVE, tool_choice="required")["output_config"] == {"effort": "low"}


def test_unforced_tool_choice_keeps_budget_thinking():
    assert _seam(_ANTHROPIC_BUDGET, tool_choice="auto")["thinking"]["budget_tokens"] == 1024


# ── a person's "auto" on a target whose accepts lacks "auto" (gemini-flash-latest)
# Live cell 2026-10-24: accepts [none, low, medium, high], ui_values with auto.
# "auto" used to be converted to the nearest accepted ("none"), then through the
# Gemini map to "minimal", then reconciled to "low" under a red banner.
_GEMINI_FLASH_LATEST = {
    "reasoning_effort": {
        "processor": "google_thinking",
        "accepts": ["none", "low", "medium", "high"],
        "ui_values": ["auto", "none", "low", "medium", "high"],
        "provider_key": "thinking_config.thinking_budget",
        "off": {"send": 0},
        "processor_config": {"mode": "gemini_3", "family": "flash", "order": 100,
                             "consumes": ["thinking_budget", "thinking_level"],
                             "default_include_thoughts": True},
    },
    "thinking_budget": {"supported": False},
    "thinking_level": {"accepts": ["low", "medium", "high"],
                       "value_map": {"low": "low", "medium": "medium", "high": "high"},
                       "provider_key": "thinking_config.thinking_level"},
}


def test_auto_on_gemini_flash_latest_is_native_and_quiet():
    controls = _controls(_GEMINI_FLASH_LATEST).model_copy(
        update={"value_orders": {"reasoning_effort": ["auto", "none", "minimal", "low",
                                                      "medium", "high", "xhigh", "max"]}}
    )
    params, adjustments = controls.outbound({"reasoning_effort": "auto"})
    assert "thinking_level" not in params["thinking_config"]
    assert adjustments == []
    unset, _ = controls.outbound({})
    assert unset["thinking_config"]["thinking_level"] == "low"
