"""Unit tests for the B1 control-rule vocabulary — on_unmapped, const,
send_when_unset, processor/processor_config — plus load-time quarantine of bad
rule rows. Pure fixtures, no DB."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_ai.catalog.controls import (
    CompiledControlsMap,
    UnmappedValueError,
    compile_controls,
)
from matrx_ai.catalog.manager import QUARANTINED_ROWS, AiCatalogManager
from matrx_ai.catalog.models import CatalogSetting, ControlRule
from matrx_ai.catalog.processors import (
    UnknownProcessorError,
    get_processor,
    has_processor,
    register_processor,
)

EFFORT_ORDER = ["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"]


def _compiled(rules: dict[str, dict], value_orders: dict[str, list] | None = None) -> CompiledControlsMap:
    return CompiledControlsMap(
        rules={k: ControlRule.model_validate(v) for k, v in rules.items()},
        value_orders=value_orders or {},
    )


# ── rule parsing / validation ────────────────────────────────────────────────
class TestRuleValidation:
    def test_new_field_defaults(self):
        rule = ControlRule.model_validate({})
        assert rule.on_unmapped == "nearest"  # conversion is the default (2026-08-17)
        assert rule.send_when_unset is False
        assert rule.const is None
        assert rule.processor is None
        assert rule.processor_config == {}

    def test_unknown_field_still_forbidden(self):
        with pytest.raises(ValidationError):
            ControlRule.model_validate({"on_unmaped": "drop"})

    def test_bad_on_unmapped_value_rejected(self):
        with pytest.raises(ValidationError):
            ControlRule.model_validate({"on_unmapped": "passthrough"})

    @pytest.mark.parametrize(
        "conflict",
        [
            {"value_map": {"low": "low"}},
            {"const": "x"},
        ],
    )
    def test_processor_exclusive_with_scalar_transforms(self, conflict):
        with pytest.raises(ValidationError, match="exclusive"):
            ControlRule.model_validate({"processor": "anthropic_thinking", **conflict})

    def test_processor_composes_with_clamp(self):
        # ai_038: clamp is a range CONSTRAINT, not a value rewrite — it composes
        # with a processor (applied to the canonical value before the processor
        # runs), so DB rules can carry e.g. anthropic temperature max 1.0.
        rule = ControlRule.model_validate(
            {"processor": "anthropic_thinking", "clamp": {"min": 0, "max": 1}}
        )
        assert rule.clamp is not None and rule.clamp.max == 1

    def test_clamp_applies_before_processor(self):
        # anthropic temperature 1.8 must reach the provider as 1.0 (Anthropic's
        # max), clamped BEFORE the exclusion processor places the key, with a
        # loud 'clamped' Adjustment.
        compiled = _compiled(
            {
                "temperature": {
                    "processor": "anthropic_temp_topp_exclusion",
                    "processor_config": {"consumes": ["top_p", "top_k"], "order": 200},
                    "clamp": {"min": 0, "max": 1},
                }
            }
        )
        out, adjustments = compiled.outbound({"temperature": 1.8})
        assert out["temperature"] == 1
        assert any(a.action == "clamped" and a.key == "temperature" for a in adjustments)
        # In-range values pass through untouched, no adjustment.
        out2, adj2 = compiled.outbound({"temperature": 0.7})
        assert out2["temperature"] == 0.7
        assert not [a for a in adj2 if a.action == "clamped"]

    def test_processor_config_requires_processor(self):
        with pytest.raises(ValidationError, match="processor_config requires processor"):
            ControlRule.model_validate({"processor_config": {"mode": "legacy"}})

    def test_const_exclusive_with_value_map_and_clamp(self):
        with pytest.raises(ValidationError, match="const is exclusive"):
            ControlRule.model_validate({"const": "parsed", "value_map": {"a": "b"}})
        with pytest.raises(ValidationError, match="const is exclusive"):
            ControlRule.model_validate({"const": 5, "clamp": {"max": 10}})

    def test_processor_with_provider_key_default_allowed(self):
        # Only value_map/clamp/const conflict; the rest are ignored by the engine.
        rule = ControlRule.model_validate(
            {"processor": "anthropic_thinking", "processor_config": {"mode": "budget"}}
        )
        assert rule.processor == "anthropic_thinking"


# ── on_unmapped ──────────────────────────────────────────────────────────────
class TestOnUnmapped:
    def test_drop_is_default(self):
        compiled = _compiled({"reasoning_effort": {"value_map": {"low": "low"}}})
        out, adj = compiled.outbound({"reasoning_effort": "xhigh"})
        assert out == {}
        assert len(adj) == 1
        assert adj[0].action == "dropped"
        assert adj[0].canonical_value == "xhigh"

    def test_error_raises_loudly(self):
        compiled = _compiled(
            {"reasoning_effort": {"value_map": {"low": "low"}, "on_unmapped": "error"}}
        )
        with pytest.raises(UnmappedValueError, match="reasoning_effort"):
            compiled.outbound({"reasoning_effort": "xhigh"})

    def test_nearest_snaps_to_closest_mapped_position(self):
        # Order: auto none minimal low medium high xhigh max. "xhigh" (idx 6)
        # with only {"high": "H"} mapped -> nearest mapped is "high" (idx 5).
        compiled = _compiled(
            {
                "reasoning_effort": {
                    "value_map": {"high": "H", "low": "L"},
                    "on_unmapped": "nearest",
                }
            },
            value_orders={"reasoning_effort": EFFORT_ORDER},
        )
        out, adj = compiled.outbound({"reasoning_effort": "xhigh"})
        assert out == {"reasoning_effort": "H"}
        assert len(adj) == 1
        assert adj[0].action == "mapped"
        assert adj[0].canonical_value == "xhigh"
        assert adj[0].sent_value == "H"

    def test_nearest_tie_breaks_toward_later_position(self):
        # "medium" (idx 4) between mapped "low" (idx 3) and "high" (idx 5):
        # equidistant -> the LATER position wins (never silently weaken).
        compiled = _compiled(
            {
                "reasoning_effort": {
                    "value_map": {"low": "L", "high": "H"},
                    "on_unmapped": "nearest",
                }
            },
            value_orders={"reasoning_effort": EFFORT_ORDER},
        )
        out, _ = compiled.outbound({"reasoning_effort": "medium"})
        assert out == {"reasoning_effort": "H"}

    def test_nearest_can_resolve_to_null_mapping_and_omit(self):
        # The nearest mapped value may map to null — that IS its translation.
        compiled = _compiled(
            {
                "reasoning_effort": {
                    "value_map": {"auto": None},
                    "on_unmapped": "nearest",
                }
            },
            value_orders={"reasoning_effort": EFFORT_ORDER},
        )
        out, adj = compiled.outbound({"reasoning_effort": "none"})
        assert out == {}
        assert adj[0].action == "omitted"

    def test_nearest_without_value_order_falls_back_to_drop(self):
        compiled = _compiled(
            {"reasoning_effort": {"value_map": {"low": "low"}, "on_unmapped": "nearest"}}
        )
        out, adj = compiled.outbound({"reasoning_effort": "xhigh"})
        assert out == {}
        assert adj[0].action == "dropped"
        assert "no nearest" in adj[0].reason

    def test_nearest_value_not_in_order_falls_back_to_drop(self):
        compiled = _compiled(
            {"reasoning_effort": {"value_map": {"low": "low"}, "on_unmapped": "nearest"}},
            value_orders={"reasoning_effort": EFFORT_ORDER},
        )
        out, adj = compiled.outbound({"reasoning_effort": "ultra"})
        assert out == {}
        assert adj[0].action == "dropped"

    def test_compile_controls_populates_value_orders_from_settings(self):
        settings = {
            "reasoning_effort": CatalogSetting(
                key="reasoning_effort", value_type="enum", canonical_values=EFFORT_ORDER
            ),
            "temperature": CatalogSetting(key="temperature", value_type="number"),
        }
        compiled = compile_controls(
            {
                "reasoning_effort": ControlRule.model_validate(
                    {"value_map": {"high": "high"}, "on_unmapped": "nearest"}
                ),
                "temperature": ControlRule.model_validate({"clamp": {"max": 1}}),
            },
            {},
            settings=settings,
        )
        assert compiled.value_orders == {"reasoning_effort": EFFORT_ORDER}
        out, _ = compiled.outbound({"reasoning_effort": "xhigh"})
        assert out == {"reasoning_effort": "high"}


# ── const ────────────────────────────────────────────────────────────────────
class TestConst:
    def test_const_sent_when_key_unset_silently(self):
        compiled = _compiled({"reasoning_format": {"const": "parsed"}})
        out, adj = compiled.outbound({})
        assert out == {"reasoning_format": "parsed"}
        assert adj == []

    def test_const_wins_over_incoming_value_with_adjustment(self):
        compiled = _compiled({"reasoning_format": {"const": "parsed"}})
        out, adj = compiled.outbound({"reasoning_format": "raw"})
        assert out == {"reasoning_format": "parsed"}
        assert len(adj) == 1
        assert adj[0].action == "const"
        assert adj[0].canonical_value == "raw"
        assert adj[0].sent_value == "parsed"

    def test_const_equal_incoming_is_silent(self):
        compiled = _compiled({"reasoning_format": {"const": "parsed"}})
        out, adj = compiled.outbound({"reasoning_format": "parsed"})
        assert out == {"reasoning_format": "parsed"}
        assert adj == []

    def test_const_respects_provider_key_rename(self):
        compiled = _compiled({"reasoning_format": {"const": "parsed", "provider_key": "rf.mode"}})
        out, _ = compiled.outbound({})
        assert out == {"rf": {"mode": "parsed"}}

    def test_const_beats_supported_false(self):
        # Precedence is const > supported:false (the locked order).
        compiled = _compiled({"reasoning_format": {"const": "parsed", "supported": False}})
        out, _ = compiled.outbound({"reasoning_format": "raw"})
        assert out == {"reasoning_format": "parsed"}


# ── default / send_when_unset ────────────────────────────────────────────────
class TestSendWhenUnset:
    def test_default_alone_keeps_legacy_semantics(self):
        # Backward compat with seeded rows: default fills when unset...
        compiled = _compiled({"reasoning_effort": {"default": "medium"}})
        out, _ = compiled.outbound({})
        assert out == {"reasoning_effort": "medium"}
        # ...and never overrides a set value.
        out, _ = compiled.outbound({"reasoning_effort": "high"})
        assert out == {"reasoning_effort": "high"}

    def test_default_alone_does_not_backfill_after_elimination(self):
        # A set value eliminated by a null mapping stays eliminated.
        compiled = _compiled(
            {"reasoning_effort": {"value_map": {"auto": None}, "default": "medium"}}
        )
        out, _ = compiled.outbound({"reasoning_effort": "auto"})
        assert out == {}

    def test_send_when_unset_backfills_after_null_omit(self):
        compiled = _compiled(
            {
                "reasoning_effort": {
                    "value_map": {"auto": None, "high": "high"},
                    "default": "medium",
                    "send_when_unset": True,
                }
            }
        )
        out, _ = compiled.outbound({"reasoning_effort": "auto"})
        assert out == {"reasoning_effort": "medium"}

    def test_send_when_unset_backfills_after_unmapped_drop(self):
        compiled = _compiled(
            {
                "reasoning_effort": {
                    "value_map": {"high": "high"},
                    "default": "high",
                    "send_when_unset": True,
                }
            }
        )
        out, _ = compiled.outbound({"reasoning_effort": "ultra"})
        assert out == {"reasoning_effort": "high"}

    def test_send_when_unset_fills_when_unset_too(self):
        compiled = _compiled(
            {"reasoning_effort": {"default": "medium", "send_when_unset": True}}
        )
        out, _ = compiled.outbound({})
        assert out == {"reasoning_effort": "medium"}

    def test_send_when_unset_never_overrides_a_sent_value(self):
        compiled = _compiled(
            {
                "reasoning_effort": {
                    "value_map": {"high": "high"},
                    "default": "medium",
                    "send_when_unset": True,
                }
            }
        )
        out, _ = compiled.outbound({"reasoning_effort": "high"})
        assert out == {"reasoning_effort": "high"}

    def test_supported_false_still_suppresses_default(self):
        compiled = _compiled(
            {"reasoning_effort": {"default": "medium", "send_when_unset": True, "supported": False}}
        )
        out, _ = compiled.outbound({})
        assert out == {}


# ── processor engine mechanics ───────────────────────────────────────────────
class TestProcessorEngine:
    def test_unknown_processor_raises_loud(self):
        with pytest.raises(UnknownProcessorError, match="definitely_not_registered"):
            get_processor("definitely_not_registered")

    def test_register_and_dispatch(self):
        name = "test_vocab_dispatch"
        if not has_processor(name):

            @register_processor(name)
            def _fn(canonical, params, ctx):
                params["marker"] = ctx.config.get("value", "hit")
                return params

        compiled = _compiled(
            {"seed": {"processor": name, "processor_config": {"value": "from-config"}}}
        )
        out, _ = compiled.outbound({"seed": 42})
        assert out == {"marker": "from-config"}  # seed consumed by its processor rule

    def test_duplicate_registration_rejected(self):
        name = "test_vocab_dup"

        @register_processor(name)
        def _a(canonical, params, ctx):
            return params

        with pytest.raises(ValueError, match="already registered"):

            @register_processor(name)
            def _b(canonical, params, ctx):
                return params

    def test_processors_run_after_scalar_rules_in_order(self):
        if not has_processor("test_vocab_first"):

            @register_processor("test_vocab_first")
            def _first(canonical, params, ctx):
                params["trace"] = params.get("trace", []) + ["first"]
                # Scalar output already assembled when pass 2 runs.
                assert params.get("max_tokens") == 100
                return params

        if not has_processor("test_vocab_second"):

            @register_processor("test_vocab_second")
            def _second(canonical, params, ctx):
                params["trace"] = params.get("trace", []) + ["second"]
                return params

        compiled = _compiled(
            {
                "max_output_tokens": {"provider_key": "max_tokens"},
                # "z_key" would run last alphabetically; order=1 forces it FIRST.
                "z_key": {"processor": "test_vocab_first", "processor_config": {"order": 1}},
                "a_key": {"processor": "test_vocab_second", "processor_config": {"order": 2}},
            }
        )
        out, _ = compiled.outbound({"max_output_tokens": 100})
        assert out["trace"] == ["first", "second"]

    def test_consumes_skips_scalar_pass_silently(self):
        if not has_processor("test_vocab_consumer"):

            @register_processor("test_vocab_consumer")
            def _consumer(canonical, params, ctx):
                params["combined"] = f"{canonical.get('temperature')}/{canonical.get('top_p')}"
                return params

        compiled = _compiled(
            {
                "temperature": {
                    "processor": "test_vocab_consumer",
                    "processor_config": {"consumes": ["top_p"]},
                }
            }
        )
        out, adj = compiled.outbound({"temperature": 0.7, "top_p": 0.9})
        assert out == {"combined": "0.7/0.9"}
        assert adj == []  # consumed keys are skipped silently, not "dropped"

    def test_metadata_keys_never_reach_the_wire(self):
        compiled = _compiled({})
        out, adj = compiled.outbound({"_reasoning_effort_derived": True, "seed": 7})
        assert out == {"seed": 7}
        assert adj == []

    def test_processor_adjustments_are_recorded(self):
        if not has_processor("test_vocab_adjuster"):

            @register_processor("test_vocab_adjuster")
            def _adjuster(canonical, params, ctx):
                from matrx_ai.catalog.models import Adjustment

                ctx.adjustments.append(
                    Adjustment(
                        key=ctx.key, action="dropped", canonical_value=1, reason="test"
                    )
                )
                return params

        compiled = _compiled({"seed": {"processor": "test_vocab_adjuster"}})
        _, adj = compiled.outbound({"seed": 1})
        assert [a.action for a in adj] == ["dropped"]


# ── load-time quarantine (extra="forbid" + processor-name gate) ──────────────
SETTINGS = [
    {
        "key": "reasoning_effort",
        "value_type": "enum",
        "canonical_values": EFFORT_ORDER,
    },
    {"key": "temperature", "value_type": "number", "canonical_min": 0, "canonical_max": 2},
]


def _rows(api_params: dict, offering_params: dict | None = None) -> dict:
    return {
        "endpoints": [
            {
                "id": "ep-1",
                "vendor": "openai",
                "internal_name": "openai_direct",
                "display_name": "OpenAI",
            }
        ],
        "apis": [
            {
                "id": "api-1",
                "name": "openai_chat",
                "display_name": "OpenAI Chat",
                "translator_key": "openai_chat",
                "rules": {"params": api_params, "constraints": []},
            }
        ],
        "offerings": [
            {
                "id": "off-1",
                "model_id": "model-1",
                "endpoint_id": "ep-1",
                "api_id": "api-1",
                "provider_model_id": "gpt-5.2",
                "override": {"params": offering_params or {}, "constraints": []},
            }
        ],
        "settings": SETTINGS,
    }


class TestQuarantine:
    def test_unknown_rule_field_quarantines_api_not_crash(self):
        manager = AiCatalogManager()
        manager.load_from_rows(
            **_rows({"reasoning_effort": {"value_map": {"low": "low"}, "typo_field": 1}})
        )
        kinds = {(r.kind, r.name) for r in QUARANTINED_ROWS}
        assert ("api", "openai_chat") in kinds
        # The api is quarantined -> its offering is unavailable, catalog still serves.
        assert manager.api("api-1") is None
        assert manager.offerings_for("model-1") == []

    def test_unknown_processor_name_quarantines(self):
        manager = AiCatalogManager()
        manager.load_from_rows(
            **_rows({"reasoning_effort": {"processor": "no_such_processor"}})
        )
        assert any(
            r.kind == "api" and "no_such_processor" in " ".join(r.errors)
            for r in QUARANTINED_ROWS
        )
        assert manager.api("api-1") is None

    def test_invalid_processor_combo_in_offering_override_quarantines_offering(self):
        manager = AiCatalogManager()
        manager.load_from_rows(
            **_rows(
                {"reasoning_effort": {"value_map": {"low": "low"}}},
                {
                    "reasoning_effort": {
                        "processor": "anthropic_thinking",
                        "clamp": {"min": 0},
                    }
                },
            )
        )
        assert any(r.kind == "offering" for r in QUARANTINED_ROWS)
        assert manager.offerings_for("model-1") == []

    def test_valid_new_vocabulary_loads_clean(self):
        manager = AiCatalogManager()
        manager.load_from_rows(
            **_rows(
                {
                    "reasoning_effort": {
                        "value_map": {v: v for v in ["low", "medium", "high"]},
                        "on_unmapped": "nearest",
                        "default": "medium",
                        "send_when_unset": True,
                    },
                    "temperature": {
                        "processor": "anthropic_temp_topp_exclusion",
                        "processor_config": {"consumes": ["top_p", "top_k"], "order": 200},
                    },
                }
            )
        )
        assert QUARANTINED_ROWS == []
        compiled = manager.compiled_controls("api-1", "off-1")
        # value_orders flowed from ai.setting.canonical_values into the compiled map.
        assert compiled.value_orders["reasoning_effort"] == EFFORT_ORDER
        out, _ = compiled.outbound({"reasoning_effort": "xhigh"})
        assert out["reasoning_effort"] == "high"  # nearest mapped in canonical order
