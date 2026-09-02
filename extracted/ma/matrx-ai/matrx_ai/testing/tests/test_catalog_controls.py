"""Pure-unit tests for matrx_ai.catalog.controls — no DB, fixture rules only."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_ai.catalog.controls import (
    CompiledControlsMap,
    compile_controls,
    expand_dotted,
    flatten_dotted,
    merge_rule_dicts,
)
from matrx_ai.catalog.models import ControlRule


def _compiled(rules: dict[str, dict]) -> CompiledControlsMap:
    return CompiledControlsMap(rules={k: ControlRule.model_validate(v) for k, v in rules.items()})


# ── rule parsing ─────────────────────────────────────────────────────────────
class TestRuleParsing:
    def test_unknown_field_forbidden(self):
        with pytest.raises(ValidationError):
            ControlRule.model_validate({"provider_key": "x", "typo_field": True})

    def test_unknown_clamp_field_forbidden(self):
        with pytest.raises(ValidationError):
            ControlRule.model_validate({"clamp": {"min": 0, "maximum": 1}})

    def test_defaults(self):
        rule = ControlRule.model_validate({})
        assert rule.supported is True
        assert rule.provider_key is None
        assert rule.value_map is None
        assert rule.clamp is None
        assert rule.default is None


# ── merge: implicit passthrough <- service <- offering, per FIELD ────────────
class TestMerge:
    def test_offering_wins_per_field_keeps_service_fields(self):
        merged = merge_rule_dicts(
            {"provider_key": "reasoning.effort", "value_map": {"xhigh": "high"}},
            {"clamp": {"min": 0, "max": 1}},
        )
        assert merged.provider_key == "reasoning.effort"  # from service
        assert merged.value_map == {"xhigh": "high"}  # from service
        assert merged.clamp is not None and merged.clamp.max == 1  # from offering

    def test_offering_replaces_field_wholesale(self):
        merged = merge_rule_dicts(
            {"value_map": {"xhigh": "high", "high": "high"}},
            {"value_map": {"xhigh": "xhigh"}},
        )
        assert merged.value_map == {"xhigh": "xhigh"}

    def test_compile_unions_keys(self):
        compiled = compile_controls(
            {"temperature": ControlRule.model_validate({"clamp": {"max": 1}})},
            {"reasoning_effort": ControlRule.model_validate({"supported": False})},
        )
        assert set(compiled.rules) == {"temperature", "reasoning_effort"}


# ── outbound worked cases ────────────────────────────────────────────────────
class TestOutbound:
    def test_openai_xhigh_passthrough_vs_clamp_down(self):
        # gpt-5.2+ family: xhigh is in-contract — no adjustment.
        xhigh_family = _compiled(
            {
                "reasoning_effort": {
                    "provider_key": "reasoning.effort",
                    "value_map": {"xhigh": "xhigh", "high": "high", "auto": None},
                }
            }
        )
        out, adj = xhigh_family.outbound({"reasoning_effort": "xhigh"})
        assert out == {"reasoning": {"effort": "xhigh"}}
        assert adj == []

        # gpt-5.1 family: xhigh snaps down to high — voiced as an adjustment.
        older_family = _compiled(
            {
                "reasoning_effort": {
                    "provider_key": "reasoning.effort",
                    "value_map": {"xhigh": "high", "high": "high"},
                }
            }
        )
        out, adj = older_family.outbound({"reasoning_effort": "xhigh"})
        assert out == {"reasoning": {"effort": "high"}}
        assert len(adj) == 1
        assert adj[0].action == "mapped"
        assert adj[0].canonical_value == "xhigh"
        assert adj[0].sent_value == "high"

    def test_supported_false_drops_key(self):
        compiled = _compiled({"temperature": {"supported": False}})
        out, adj = compiled.outbound({"temperature": 0.7, "top_p": 0.9})
        assert out == {"top_p": 0.9}
        assert len(adj) == 1
        assert adj[0].action == "dropped"
        assert adj[0].key == "temperature"

    def test_temperature_clamp(self):
        compiled = _compiled({"temperature": {"clamp": {"min": 0, "max": 1}}})
        out, adj = compiled.outbound({"temperature": 1.7})
        assert out == {"temperature": 1.0}
        assert len(adj) == 1
        assert adj[0].action == "clamped"
        assert adj[0].sent_value == 1.0

        out, adj = compiled.outbound({"temperature": 0.5})
        assert out == {"temperature": 0.5}
        assert adj == []

    def test_clamp_preserves_int(self):
        compiled = _compiled({"max_output_tokens": {"clamp": {"max": 4096}}})
        out, _ = compiled.outbound({"max_output_tokens": 100_000})
        assert out == {"max_output_tokens": 4096}
        assert isinstance(out["max_output_tokens"], int)

    def test_clamp_skips_non_numeric(self):
        compiled = _compiled({"temperature": {"clamp": {"min": 0, "max": 1}}})
        out, adj = compiled.outbound({"temperature": "hot"})
        assert out == {"temperature": "hot"}
        assert adj == []

    def test_google_dotted_provider_key(self):
        compiled = _compiled(
            {
                "reasoning_effort": {
                    "provider_key": "thinking_config.thinking_level",
                    "value_map": {"none": "minimal", "low": "low", "high": "high"},
                },
                "reasoning_summary": {
                    "provider_key": "thinking_config.include_thoughts",
                    "value_map": {"detailed": True, "never": False},
                },
            }
        )
        out, _ = compiled.outbound({"reasoning_effort": "high", "reasoning_summary": "detailed"})
        assert out == {"thinking_config": {"thinking_level": "high", "include_thoughts": True}}

    def test_value_map_null_omits(self):
        compiled = _compiled({"reasoning_effort": {"value_map": {"auto": None, "low": "low"}}})
        out, adj = compiled.outbound({"reasoning_effort": "auto"})
        assert out == {}
        assert len(adj) == 1
        assert adj[0].action == "omitted"

    def test_value_map_missing_key_drops_by_default(self):
        # on_unmapped is EXPLICIT "drop" here — the default is "nearest" (THE
        # EQUIVALENCE LAW, 2026-08-17). A declared drop is still honoured:
        # a value with no map entry is dropped LOUDLY, never sent as-is.
        compiled = _compiled({"reasoning_effort": {"value_map": {"low": "low"}}})
        out, adj = compiled.outbound({"reasoning_effort": "medium"})
        assert out == {}
        assert len(adj) == 1
        assert adj[0].action == "dropped"
        assert adj[0].canonical_value == "medium"

    def test_default_applied_when_unset(self):
        compiled = _compiled({"reasoning_format": {"default": "parsed"}})
        out, adj = compiled.outbound({"temperature": 0.7})
        assert out == {"temperature": 0.7, "reasoning_format": "parsed"}
        assert adj == []

    def test_default_not_applied_when_set(self):
        compiled = _compiled({"reasoning_format": {"default": "parsed"}})
        out, _ = compiled.outbound({"reasoning_format": "raw"})
        assert out == {"reasoning_format": "raw"}

    def test_default_not_applied_when_unsupported(self):
        compiled = _compiled({"reasoning_format": {"default": "parsed", "supported": False}})
        out, _ = compiled.outbound({})
        assert out == {}

    def test_all_none_config_produces_exactly_defaults(self):
        compiled = _compiled(
            {
                "reasoning_effort": {
                    "provider_key": "reasoning.effort",
                    "value_map": {"low": "low"},
                },
                "reasoning_format": {"default": "parsed"},
                "temperature": {"clamp": {"min": 0, "max": 1}, "default": 1},
            }
        )
        out, adj = compiled.outbound({})
        assert out == {"reasoning_format": "parsed", "temperature": 1}
        assert adj == []

    def test_explicit_none_value_treated_as_unset(self):
        compiled = _compiled({"temperature": {"default": 1}})
        out, _ = compiled.outbound({"temperature": None})
        assert out == {"temperature": 1}

    def test_passthrough_for_unruled_keys(self):
        compiled = _compiled({})
        out, adj = compiled.outbound({"seed": 42, "top_k": 5})
        assert out == {"seed": 42, "top_k": 5}
        assert adj == []


# ── inbound (best-effort inverse) ────────────────────────────────────────────
class TestInbound:
    def test_reversed_rename(self):
        compiled = _compiled({"reasoning_effort": {"provider_key": "reasoning.effort"}})
        assert compiled.inbound({"reasoning": {"effort": "high"}}) == {"reasoning_effort": "high"}

    def test_reversed_value_map_prefers_identity(self):
        compiled = _compiled(
            {
                "reasoning_effort": {
                    "provider_key": "reasoning.effort",
                    "value_map": {"xhigh": "high", "high": "high", "low": "low"},
                }
            }
        )
        # "high" could invert to xhigh or high — identity pair wins.
        assert compiled.inbound({"reasoning": {"effort": "high"}}) == {"reasoning_effort": "high"}
        assert compiled.inbound({"reasoning": {"effort": "low"}}) == {"reasoning_effort": "low"}

    def test_reversed_value_map_non_identity(self):
        compiled = _compiled(
            {
                "reasoning_effort": {
                    "provider_key": "thinking_config.thinking_level",
                    "value_map": {"none": "minimal"},
                }
            }
        )
        assert compiled.inbound({"thinking_config": {"thinking_level": "minimal"}}) == {
            "reasoning_effort": "none"
        }

    def test_unknown_flat_keys_pass_through(self):
        compiled = _compiled({"reasoning_effort": {"provider_key": "reasoning.effort"}})
        assert compiled.inbound({"temperature": 0.7}) == {"temperature": 0.7}

    def test_roundtrip(self):
        compiled = _compiled(
            {
                "reasoning_effort": {
                    "provider_key": "reasoning.effort",
                    "value_map": {"xhigh": "xhigh", "high": "high"},
                },
                "max_output_tokens": {"provider_key": "max_completion_tokens"},
            }
        )
        canonical = {"reasoning_effort": "xhigh", "max_output_tokens": 1000}
        out, _ = compiled.outbound(canonical)
        assert compiled.inbound(out) == canonical


# ── dotted helpers ───────────────────────────────────────────────────────────
class TestDottedHelpers:
    def test_expand_and_flatten_are_inverse(self):
        target: dict = {}
        expand_dotted(target, "a.b.c", 1)
        expand_dotted(target, "a.b.d", 2)
        expand_dotted(target, "e", 3)
        assert target == {"a": {"b": {"c": 1, "d": 2}}, "e": 3}
        assert flatten_dotted(target) == {"a.b.c": 1, "a.b.d": 2, "e": 3}


# ── the vocabulary gate: a processor's RESOLVED level vs the offering ────────
#
# Regression for the 2026-08-17 FastFire outage. gemini-3.7-flash declares
# ui_values [auto, none, low, medium, high] — no "minimal" — while 38 live
# agents stored reasoning_effort="minimal". The google_thinking FLASH family
# map translates minimal -> "minimal" (true of 3.5-flash, false of 3.7), and
# Google 400'd every call: "Thinking level MINIMAL is not supported for this
# model." The gate compares the map's OUTPUT to the offering's declaration.
_EFFORT_ORDER = ["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"]


def _compiled_ordered(rules: dict[str, dict]) -> CompiledControlsMap:
    return CompiledControlsMap(
        rules={k: ControlRule.model_validate(v) for k, v in rules.items()},
        value_orders={"reasoning_effort": list(_EFFORT_ORDER)},
    )


def _flash_rule(ui_values: list[str]) -> dict[str, dict]:
    return {
        "reasoning_effort": {
            "processor": "google_thinking",
            "processor_config": {"mode": "gemini_3", "family": "flash"},
            "ui_values": ui_values,
        }
    }


class TestVocabularyGate:
    def test_unsupported_resolved_level_is_reconciled_not_sent(self):
        compiled = _compiled_ordered(_flash_rule(["auto", "none", "low", "medium", "high"]))
        out, adj = compiled.outbound({"reasoning_effort": "minimal"})
        assert out["thinking_config"]["thinking_level"] == "low"
        assert [a.action for a in adj] == ["unsupported_value"]
        assert (adj[0].canonical_value, adj[0].sent_value) == ("minimal", "low")

    def test_same_map_same_family_but_a_model_that_supports_it_is_untouched(self):
        # The ONLY difference from the case above is the offering's declaration
        # — which is exactly the per-model fact the family map cannot carry.
        compiled = _compiled_ordered(
            _flash_rule(["auto", "none", "minimal", "low", "medium", "high"])
        )
        out, adj = compiled.outbound({"reasoning_effort": "minimal"})
        assert out["thinking_config"]["thinking_level"] == "minimal"
        assert adj == []

    def test_never_reconciles_an_intensity_onto_none(self):
        # A model whose floor is "high" must serve "minimal" with high, never
        # by silently disabling thinking.
        compiled = _compiled_ordered(_flash_rule(["auto", "none", "high"]))
        out, _ = compiled.outbound({"reasoning_effort": "minimal"})
        assert out["thinking_config"]["thinking_level"] == "high"

    def test_no_reconcilable_neighbour_drops_rather_than_sends(self):
        compiled = _compiled_ordered(_flash_rule(["auto", "none"]))
        out, adj = compiled.outbound({"reasoning_effort": "minimal"})
        assert out["thinking_config"] == {}
        assert adj[0].action == "unsupported_value"
        assert adj[0].sent_value is None

    def test_rule_without_ui_values_is_unaffected(self):
        compiled = _compiled_ordered(
            {
                "reasoning_effort": {
                    "processor": "google_thinking",
                    "processor_config": {"mode": "gemini_3", "family": "flash"},
                }
            }
        )
        out, adj = compiled.outbound({"reasoning_effort": "minimal"})
        assert out["thinking_config"]["thinking_level"] == "minimal"
        assert adj == []

    def test_authored_family_downgrades_are_not_overridden(self):
        # gemini-3-pro maps medium -> low BY DESIGN. "low" is supported, so the
        # gate must leave that authored decision alone (never escalate to high).
        compiled = _compiled_ordered(
            {
                "reasoning_effort": {
                    "processor": "google_thinking",
                    "processor_config": {"mode": "gemini_3", "family": "pro"},
                    "ui_values": ["auto", "none", "low", "high"],
                }
            }
        )
        out, adj = compiled.outbound({"reasoning_effort": "medium"})
        assert out["thinking_config"]["thinking_level"] == "low"
        assert adj == []
