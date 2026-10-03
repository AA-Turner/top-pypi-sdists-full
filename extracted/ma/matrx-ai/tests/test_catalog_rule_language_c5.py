"""Settings-translation item C5 — the K6 rule language ACTS.

Each field is proven twice: it changes the outcome when a rule carries it, and
a rule that does not carry it behaves exactly as before (the wire snapshot over
the whole clone catalog is the second, catalog-wide half of that proof).
Pure units — no DB.
"""

from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from matrx_ai.catalog import translation_defaults as D
from matrx_ai.catalog.canonicalize import canonical_settings_from_config
from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule
from matrx_ai.providers.outbound_params import resolve_outbound_params

EFFORT_ORDER = ["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"]
THINKING_CONSUMES = [
    "thinking_budget",
    "thinking_level",
    "include_thoughts",
    "reasoning_summary",
    "clear_thinking",
]


def _map(rules: dict[str, dict], **extra) -> CompiledControlsMap:
    return CompiledControlsMap(
        rules={k: ControlRule.model_validate(v) for k, v in rules.items()},
        value_orders={"reasoning_effort": EFFORT_ORDER, "thinking_level": EFFORT_ORDER},
        **extra,
    )


def _wire(controls: CompiledControlsMap, **config) -> dict:
    return resolve_outbound_params(SimpleNamespace(**config), controls)


def _adj(adjustments, key):
    return [a for a in adjustments if a.key == key]


IDENTITY_EFFORT = {v: v for v in ("none", "minimal", "low", "medium", "high", "xhigh")}


# ── the owner's example (GROUND-TRUTH, 2026-10-02 06:16) ─────────────────────
# "5,000 tokens to 11,000 tokens for thinking tokens converts to 'Medium' for
#  gpt 5 and for llama 3, drop it, and for claude, make it xyz."

GPT5_CLASS = {
    "reasoning_effort": {
        "provider_key": "reasoning.effort",
        "value_map": {"auto": None, **IDENTITY_EFFORT},
        "from_number": [
            {"lte": 0, "to": "none"},
            {"lte": 4999, "to": "low"},
            {"lte": 11000, "to": "medium"},
            {"lte": None, "to": "high"},
        ],
    },
    "thinking_budget": {"supported": False},
}
LLAMA_3 = {
    "reasoning_effort": {"drop": True, "why": "Llama 3 has no reasoning"},
    "thinking_budget": {"drop": True, "why": "Llama 3 has no reasoning"},
}
CLAUDE_BUDGET = {
    "reasoning_effort": {
        "processor": "anthropic_thinking",
        "processor_config": {"mode": "budget", "consumes": THINKING_CONSUMES},
    }
}


class TestOwnerExample:
    @pytest.mark.parametrize("budget", [5000, 11000])
    def test_gpt5_class_target_converts_through_its_from_number(self, budget):
        assert _wire(_map(GPT5_CLASS), thinking_budget=budget) == {"reasoning": {"effort": "medium"}}

    def test_gpt5_without_from_number_keeps_todays_tiers(self):
        rules = {**GPT5_CLASS, "reasoning_effort": {**GPT5_CLASS["reasoning_effort"]}}
        del rules["reasoning_effort"]["from_number"]
        controls = _map(rules)
        assert _wire(controls, thinking_budget=5000) == {"reasoning": {"effort": "medium"}}
        assert _wire(controls, thinking_budget=11000) == {"reasoning": {"effort": "high"}}

    @pytest.mark.parametrize("budget", [5000, 11000])
    def test_no_thinking_target_is_a_declared_drop(self, budget):
        controls = _map(LLAMA_3)
        canonical = canonical_settings_from_config(SimpleNamespace(thinking_budget=budget))
        params, adjustments = controls.outbound(canonical)
        assert params == {}
        for key in ("reasoning_effort", "thinking_budget"):
            [adj] = _adj(adjustments, key)
            assert adj.action == "dropped"
            assert adj.expected is True
            assert adj.provenance == "declared"
            assert "Llama 3 has no reasoning" in adj.reason

    @pytest.mark.parametrize("budget", [5000, 11000])
    def test_claude_budget_target_gets_a_budget(self, budget):
        assert _wire(_map(CLAUDE_BUDGET), thinking_budget=budget) == {
            "thinking": {"type": "enabled", "budget_tokens": budget},
            "max_tokens": D.ANTHROPIC_DEFAULT_MAX_TOKENS,
        }


# ── off ──────────────────────────────────────────────────────────────────────
OPENAI_NONE_LESS = {  # the gpt-5 generation: no "none" tier
    "provider_key": "reasoning.effort",
    "value_map": {"auto": None, "minimal": "minimal", "low": "low", "medium": "medium", "high": "high"},
    "ui_values": ["auto", "minimal", "low", "medium", "high"],
}


class TestOff:
    def test_without_off_none_follows_todays_nearest(self):
        params, adjustments = _map({"reasoning_effort": OPENAI_NONE_LESS}).outbound(
            {"reasoning_effort": "none"}
        )
        # exactly as before C5: the nearest-mapped metric decides (computed)
        assert params == {"reasoning": {"effort": "minimal"}}
        assert adjustments[0].provenance == "computed"

    def test_off_floor_sends_the_lowest_accepted(self):
        rule = {**OPENAI_NONE_LESS, "off": {"floor": True}}
        params, adjustments = _map({"reasoning_effort": rule}).outbound({"reasoning_effort": "none"})
        assert params == {"reasoning": {"effort": "minimal"}}
        [adj] = _adj(adjustments, "reasoning_effort")
        assert (adj.action, adj.sent_value, adj.provenance) == ("mapped", "minimal", "declared")

    def test_off_send_sends_the_declared_value(self):
        rule = {**OPENAI_NONE_LESS, "off": {"send": "low"}}
        params, _ = _map({"reasoning_effort": rule}).outbound({"reasoning_effort": "none"})
        assert params == {"reasoning": {"effort": "low"}}

    def test_off_omit_equals_unset_including_the_default(self):
        rule = {**OPENAI_NONE_LESS, "default": "low", "off": {"omit": True, "why": "no off switch"}}
        controls = _map({"reasoning_effort": rule})
        off_params, adjustments = controls.outbound({"reasoning_effort": "none"})
        unset_params, _ = controls.outbound({})
        assert off_params == unset_params == {"reasoning": {"effort": "low"}}
        [adj] = _adj(adjustments, "reasoning_effort")
        assert adj.action == "omitted" and adj.expected is True and "no off switch" in adj.reason

    def test_off_acts_on_include_thoughts_false(self):
        rule = {"off": {"send": "never"}, "provider_key": "reasoning.summary"}
        params, _ = _map({"include_thoughts": rule}).outbound({"include_thoughts": False})
        assert params == {"reasoning": {"summary": "never"}}
        params, _ = _map({"include_thoughts": rule}).outbound({"include_thoughts": True})
        assert params == {"reasoning": {"summary": True}}

    def test_off_acts_on_disable_reasoning(self):
        rule = {**OPENAI_NONE_LESS, "off": {"floor": True}}
        assert _wire(_map({"reasoning_effort": rule}), disable_reasoning=True) == {
            "reasoning": {"effort": "minimal"}
        }

    def test_off_on_a_processor_rule_runs_before_the_processor(self):
        rule = {
            "processor": "together_reasoning",
            "processor_config": {"consumes": THINKING_CONSUMES},
        }
        without = _map({"reasoning_effort": rule}).outbound({"reasoning_effort": "none"})[0]
        assert without == {"reasoning": {"enabled": False}}  # today's native off
        omitted = _map(
            {"reasoning_effort": {**rule, "off": {"omit": True, "why": "treat as unset"}}}
        ).outbound({"reasoning_effort": "none"})[0]
        assert omitted == {"reasoning_effort": "high"}  # == wire(unset)


# ── from_number / to_number ──────────────────────────────────────────────────
class TestNumberScale:
    def test_from_number_on_a_scalar_rule(self):
        rule = {
            "provider_key": "effort",
            "from_number": [{"lte": 1000, "to": "low"}, {"lte": None, "to": "high"}],
        }
        controls = _map({"thinking_budget": rule})
        assert controls.outbound({"thinking_budget": 500})[0] == {"effort": "low"}
        assert controls.outbound({"thinking_budget": 5000})[0] == {"effort": "high"}

    def test_from_number_null_target_is_a_silent_declared_drop(self):
        rule = {"from_number": [{"lte": 1000, "to": None}, {"lte": None, "to": "high"}]}
        params, adjustments = _map({"thinking_budget": rule}).outbound({"thinking_budget": 500})
        assert params == {}
        [adj] = adjustments
        assert adj.action == "dropped" and adj.expected is True

    def test_bridge_honours_a_from_number_drop(self):
        rules = {
            "reasoning_effort": {
                "value_map": IDENTITY_EFFORT,
                "from_number": [{"lte": 4096, "to": None}, {"lte": None, "to": "high"}],
            },
            "thinking_budget": {"supported": False},
        }
        assert _wire(_map(rules), thinking_budget=2000) == {}
        assert _wire(_map(rules), thinking_budget=9000) == {"reasoning_effort": "high"}

    def test_to_number_converts_a_scale_to_a_number(self):
        rule = {"provider_key": "thinking.budget_tokens", "to_number": {"low": 1024, "high": 16000}}
        controls = _map({"reasoning_effort": rule})
        assert controls.outbound({"reasoning_effort": "high"})[0] == {
            "thinking": {"budget_tokens": 16000}
        }
        # a value the table lacks takes the nearest entry (computed)
        params, adjustments = controls.outbound({"reasoning_effort": "medium"})
        assert params in ({"thinking": {"budget_tokens": 1024}}, {"thinking": {"budget_tokens": 16000}})
        assert adjustments[0].provenance == "computed"

    def test_explicit_effort_is_never_overridden_by_the_budget(self):
        assert _wire(_map(GPT5_CLASS), reasoning_effort="low", thinking_budget=11000) == {
            "reasoning": {"effort": "low"}
        }

    def test_raw_canonical_is_never_bridged(self):
        # Only canonicalize's _convert request bridges; a raw dict is taken as given.
        params, _ = _map(GPT5_CLASS).outbound({"thinking_budget": 5000})
        assert params == {}


# ── processors read their tables from the rule ───────────────────────────────
class TestProcessorTablesAreRuleData:
    def test_anthropic_budget_effort_table_from_to_number(self):
        rule = {**CLAUDE_BUDGET["reasoning_effort"], "to_number": {"high": 20000}}
        params = _wire(_map({"reasoning_effort": rule}), reasoning_effort="high")
        assert params["thinking"] == {"type": "enabled", "budget_tokens": 20000}
        default = _wire(_map(CLAUDE_BUDGET), reasoning_effort="high")
        assert default["thinking"]["budget_tokens"] == D.ANTHROPIC_EFFORT_TO_BUDGET["high"]

    def test_anthropic_adaptive_budget_tiers_from_from_number(self):
        base = {
            "processor": "anthropic_thinking",
            "processor_config": {"mode": "adaptive", "consumes": THINKING_CONSUMES},
        }
        default = _wire(_map({"reasoning_effort": base}), thinking_budget=5000)
        assert default["output_config"] == {"effort": "medium"}
        custom = {**base, "from_number": [{"lte": 4000, "to": "low"}, {"lte": None, "to": "max"}]}
        params = _wire(_map({"reasoning_effort": custom}), thinking_budget=5000)
        assert params["output_config"] == {"effort": "max"}

    def test_gemini3_budget_levels_from_from_number(self):
        base = {
            "processor": "google_thinking",
            "processor_config": {"mode": "gemini_3", "family": "flash", "consumes": THINKING_CONSUMES},
        }
        assert _wire(_map({"reasoning_effort": base}), thinking_budget=3000) == {
            "thinking_config": {"thinking_level": "medium"}
        }
        custom = {**base, "from_number": [{"lte": None, "to": "high"}]}
        assert _wire(_map({"reasoning_effort": custom}), thinking_budget=3000) == {
            "thinking_config": {"thinking_level": "high"}
        }

    def test_together_effort_map_from_processor_config(self):
        rule = {
            "processor": "together_reasoning",
            "processor_config": {"effort_map": {"medium": "medium"}, "default_effort": "low"},
        }
        controls = _map({"reasoning_effort": rule})
        assert controls.outbound({"reasoning_effort": "medium"})[0] == {"reasoning_effort": "medium"}
        assert controls.outbound({"reasoning_effort": "xhigh"})[0] == {"reasoning_effort": "low"}

    def test_media_aspect_table_from_processor_config(self):
        rule = {
            "processor": "media_dims",
            "processor_config": {"mode": "size", "aspect_table": {"16:9": [1920, 1080]}},
        }
        assert _map({"aspect_ratio": rule}).outbound({"aspect_ratio": "16:9"})[0] == {
            "size": "1920x1080"
        }
        default = {"processor": "media_dims", "processor_config": {"mode": "size"}}
        assert _map({"aspect_ratio": default}).outbound({"aspect_ratio": "16:9"})[0] == {
            "size": "1536x1024"
        }


# ── accepts ──────────────────────────────────────────────────────────────────
class TestAccepts:
    def test_scalar_value_outside_accepts_takes_the_nearest(self):
        rule = {"value_map": IDENTITY_EFFORT, "accepts": ["low", "medium", "high"]}
        params, adjustments = _map({"reasoning_effort": rule}).outbound({"reasoning_effort": "xhigh"})
        assert params == {"reasoning_effort": "high"}
        [adj] = adjustments
        assert (adj.action, adj.provenance, adj.sent_value) == ("mapped", "computed", "high")

    def test_numeric_accepts(self):
        params, adjustments = _map({"count": {"accepts": [1, 2, 4]}}).outbound({"count": 3})
        assert params == {"count": 4}  # ties go up — never less than asked
        assert adjustments[0].provenance == "computed"

    def test_ui_values_without_accepts_enforce_nothing_new(self):
        rule = {"value_map": IDENTITY_EFFORT, "ui_values": ["low", "medium"]}
        params, adjustments = _map({"reasoning_effort": rule}).outbound({"reasoning_effort": "high"})
        assert params == {"reasoning_effort": "high"} and adjustments == []

    def test_accepts_on_a_processor_input(self):
        rule = {
            "processor": "anthropic_thinking",
            "processor_config": {"mode": "adaptive", "consumes": THINKING_CONSUMES},
            "accepts": ["low", "medium", "high"],
        }
        params, adjustments = _map({"reasoning_effort": rule}).outbound({"reasoning_effort": "max"})
        assert params["output_config"] == {"effort": "high"}
        assert any(a.action == "mapped" and a.provenance == "computed" for a in adjustments)

    def test_accepts_replaces_ui_values_in_the_gemini3_reconcile(self):
        rule = {
            "processor": "google_thinking",
            "processor_config": {"mode": "gemini_3", "family": "flash"},
            "ui_values": ["auto", "none", "minimal", "low", "medium", "high"],
            "accepts": ["auto", "none", "low", "high"],
        }
        params, _ = _map({"reasoning_effort": rule}).outbound({"reasoning_effort": "minimal"})
        assert params == {"thinking_config": {"thinking_level": "low"}}


# ── declared drop ────────────────────────────────────────────────────────────
class TestDeclaredDrop:
    def test_scalar_declared_drop_is_expected_and_silent(self):
        params, adjustments = _map({"seed": {"drop": True, "why": "no seed here"}}).outbound({"seed": 7})
        assert params == {}
        [adj] = adjustments
        assert adj.action == "dropped" and adj.expected is True and "no seed here" in adj.reason

    def test_processor_declared_drop_never_runs_and_drops_consumed_keys(self):
        rule = {
            "processor": "anthropic_thinking",
            "processor_config": {"mode": "budget", "consumes": ["thinking_budget"]},
            "drop": True,
            "why": "no reasoning",
        }
        params, adjustments = _map({"reasoning_effort": rule}).outbound(
            {"reasoning_effort": "high", "thinking_budget": 4000}
        )
        assert params == {}
        assert {a.key for a in adjustments} == {"reasoning_effort", "thinking_budget"}
        assert all(a.expected and a.action == "dropped" for a in adjustments)


# ── grep proof: processors.py carries no translation tables ──────────────────
def test_processors_module_holds_no_translation_table_literals():
    """Every map / threshold a processor translates with lives in
    translation_defaults (the declared defaults) or the rule. A dict literal
    with constant keys, or a constant list/tuple/set of 2+ values, in
    processors.py is a table that escaped — move it."""
    path = Path(__file__).resolve().parents[1] / "matrx_ai" / "catalog" / "processors.py"
    tree = ast.parse(path.read_text())
    exports = {
        id(stmt.value)
        for stmt in tree.body
        if isinstance(stmt, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "__all__" for t in stmt.targets)
    }
    # A wire SHAPE placed into the payload (``params["thinking"] = {...}``) is
    # not a table; a constant dict bound to a name or looked up is.
    placements = {
        id(stmt.value)
        for stmt in ast.walk(tree)
        if isinstance(stmt, ast.Assign) and all(isinstance(t, ast.Subscript) for t in stmt.targets)
    }
    offenders: list[str] = []
    for node in ast.walk(tree):
        if id(node) in exports or id(node) in placements:
            continue
        if isinstance(node, ast.Dict) and len(node.keys) >= 2:
            if all(isinstance(k, ast.Constant) for k in node.keys if k is not None) and all(
                isinstance(v, ast.Constant) for v in node.values
            ):
                offenders.append(f"dict literal at line {node.lineno}")
        elif isinstance(node, ast.List | ast.Tuple | ast.Set) and len(node.elts) >= 2:
            if all(isinstance(e, ast.Constant) for e in node.elts):
                values = [e.value for e in node.elts]
                if any(v is not None for v in values):
                    offenders.append(f"constant sequence {values!r} at line {node.lineno}")
        elif isinstance(node, ast.Compare):
            for comparator in [node.left, *node.comparators]:
                if (
                    isinstance(comparator, ast.Constant)
                    and isinstance(comparator.value, int | float)
                    and not isinstance(comparator.value, bool)
                    and comparator.value not in (0,)
                ):
                    offenders.append(f"numeric threshold {comparator.value} at line {node.lineno}")
    assert offenders == [], offenders
