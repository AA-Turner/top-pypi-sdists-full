"""Structural keys (tool_choice) now honour the api/offering control rule.

Before: the rule was UI-only; a stored "required" reached the Anthropic
translator's hardcoded switch and became {"type": "any"} — a 400 on Opus 5.5 /
Fable 5.1. Now resolve_structural_setting applies the rule through the same
CompiledControlsMap.outbound pass as every scalar key.
"""

from __future__ import annotations

from unittest.mock import patch

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule
from matrx_ai.providers import outbound_params
from matrx_ai.providers.outbound_params import resolve_structural_setting

NO_FORCED_TOOLS = CompiledControlsMap(
    rules={
        "tool_choice": ControlRule(
            supported=True,
            value_map={"auto": "auto", "none": "none"},
            on_unmapped="drop",
            ui_values=["auto", "none"],
        )
    },
    value_orders={"tool_choice": ["auto", "required", "none"]},
)


def test_forced_tool_use_is_dropped_loudly() -> None:
    with patch.object(outbound_params, "warn_client_about_dropped_settings") as warn:
        assert (
            resolve_structural_setting("required", "tool_choice", NO_FORCED_TOOLS, model="m")
            is None
        )
    (adjs,), _ = warn.call_args
    assert (
        adjs[0].key == "tool_choice" and adjs[0].action == "dropped" and adjs[0].expected is False
    )


def test_allowed_values_pass_through_silently() -> None:
    with patch.object(outbound_params, "warn_client_about_dropped_settings") as warn:
        assert resolve_structural_setting("auto", "tool_choice", NO_FORCED_TOOLS) == "auto"
        assert resolve_structural_setting("none", "tool_choice", NO_FORCED_TOOLS) == "none"
    warn.assert_not_called()


def test_no_rule_means_unchanged_behaviour() -> None:
    empty = CompiledControlsMap()
    for v in ("auto", "required", "none", None):
        assert resolve_structural_setting(v, "tool_choice", empty) == v


def test_unsupported_rule_drops() -> None:
    off = CompiledControlsMap(rules={"tool_choice": ControlRule(supported=False)})
    assert resolve_structural_setting("required", "tool_choice", off) is None


def test_explicit_map_converts() -> None:
    relax = CompiledControlsMap(
        rules={
            "tool_choice": ControlRule(
                value_map={"auto": "auto", "required": "auto", "none": "none"}
            )
        }
    )
    assert resolve_structural_setting("required", "tool_choice", relax) == "auto"


def test_one_rule_copy_fires_no_other_rule() -> None:
    noisy = CompiledControlsMap(
        rules={
            "tool_choice": ControlRule(
                value_map={"auto": "auto", "none": "none"}, on_unmapped="drop"
            ),
            "temperature": ControlRule(const=0.2),
        }
    )
    assert resolve_structural_setting("auto", "tool_choice", noisy) == "auto"
