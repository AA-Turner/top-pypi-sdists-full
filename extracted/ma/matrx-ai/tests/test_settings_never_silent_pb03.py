"""PB-03 (real test, core-chain): one kitchen-sink settings block on three providers.

Guard for defect 6 (a key the rules mark unsupported reached the Gemini wire with no
record) and the engine half of defect 7 (nothing a setting does is silent).

Fixture: ``tests/fixtures/pb03_offering_rules.json`` — the compiled cells
(``ai.offering_rules_compiled``, 2026-10-17) of the three PB-03 offerings
(claude-haiku-5-5, gpt-5-nano, gemini-flash-lite-latest), every key the kitchen sink
sends plus every processor rule.

Two invariants, per offering, through the real seam (gate + ``outbound``):

* I1 — a key whose own cell says ``supported: false`` / ``drop`` and that no processor
  carries never appears as a top-level wire key.
* I2 — every key the caller set is ACCOUNTED: it reached the wire unchanged at its
  rule's provider key, or an Adjustment names it (dropped / clamped / mapped …).
  Before the fix, the keys a processor consumes (Gemini ``thinking_budget``,
  ``include_thoughts``, ``reasoning_effort``) became ``thinking_config`` with no
  Adjustment at all — read off the rules, an "unsupported key on the wire".
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from matrx_ai.catalog import translation_defaults as D
from matrx_ai.catalog.controls import CompiledControlsMap, flatten_dotted
from matrx_ai.catalog.models import ControlRule
from matrx_ai.catalog.wire_meaning import meaning_paths
from matrx_ai.providers.outbound_params import drop_foreign_canonical_keys

FIXTURE = Path(__file__).parent / "fixtures" / "pb03_offering_rules.json"

KITCHEN_SINK: dict[str, Any] = {
    "temperature": 0.3,
    "top_p": 0.9,
    "top_k": 40,
    "seed": 4471,
    "frequency_penalty": 0.2,
    "presence_penalty": 0.1,
    "stop_sequences": ["ZZ-HALT"],
    "parallel_tool_calls": False,
    "verbosity": "low",
    "store": True,
    "reasoning_effort": "high",
    "thinking_budget": 2048,
    "thinking_level": "low",
    "include_thoughts": True,
    "clear_thinking": True,
    "max_output_tokens": 400000,
    "tool_choice": "auto",
    "internal_web_search": True,
    "internal_url_context": True,
}


def _offerings() -> dict[str, dict[str, Any]]:
    return json.loads(FIXTURE.read_text())


def _controls(rules: dict[str, Any]) -> CompiledControlsMap:
    return CompiledControlsMap(
        rules={k: ControlRule.model_validate(v) for k, v in rules.items()}
    ).with_output_maximum(65536)


def run_kitchen_sink(controls: CompiledControlsMap) -> tuple[dict[str, Any], list[Any]]:
    canonical = dict(KITCHEN_SINK)
    gate: list[Any] = []
    drop_foreign_canonical_keys(canonical, controls, adjustments=gate)
    params, adjustments = controls.outbound(canonical)
    return params, gate + adjustments


def violations(controls: CompiledControlsMap) -> list[str]:
    params, adjustments = run_kitchen_sink(controls)
    flat = flatten_dotted(params)
    owned, _unsupported, _declared = controls._surface()
    named = {a.key for a in adjustments} | {
        a.converted_from for a in adjustments if a.converted_from
    }
    problems: list[str] = []
    for key, value in KITCHEN_SINK.items():
        rule = controls.rules.get(key)
        unsupported = rule is not None and (rule.supported is False or rule.drop)
        if unsupported and key not in owned:
            wire_key = rule.provider_key or key
            if key in params or wire_key in params:
                problems.append(f"I1 {key}: marked unsupported but on the wire as {wire_key}")
        if unsupported:
            # I3 — by MEANING (PB-03 U3): unsupported means absent in EVERY shape; a
            # value folded into thinking_config / reasoning / generation_config still counts.
            for path in meaning_paths(params, key):
                problems.append(f"I3 {key}: marked unsupported but its meaning is on the wire at {path}")
        if key in named:
            continue
        if D.is_unset_posture(value):
            continue  # C3c ruling: "auto" MEANS not set — absent, never an adjustment
        wire_key = (rule.provider_key if rule is not None else None) or key
        if flat.get(wire_key) == value:
            continue
        problems.append(f"I2 {key}={value!r}: not on the wire as sent and no Adjustment names it")
    return problems


@pytest.mark.parametrize("offering", sorted(_offerings()))
def test_kitchen_sink_every_setting_accounted(offering: str) -> None:
    controls = _controls(_offerings()[offering]["rules"])
    assert violations(controls) == []


def test_gemini_thinking_keys_are_translated_not_raw() -> None:
    controls = _controls(_offerings()["google_gemini_flash_lite_latest"]["rules"])
    params, adjustments = run_kitchen_sink(controls)
    # The reasoning request rides in Gemini's own shape — never as raw top-level keys.
    assert "thinking_budget" not in params and "include_thoughts" not in params
    assert "thinking_config" in params
    by_key = {a.key: a for a in adjustments}
    # The offering resolves to gemini-3.5-flash-lite: Gemini 3 mode takes thinking_level, so the
    # raw budget is dropped WITH a record and the effort rides as the level (L4d, 2026-10-18).
    assert params["thinking_config"].get("thinking_level"), params["thinking_config"]
    assert "thinking_budget" not in params["thinking_config"]
    assert by_key["thinking_budget"].action in {"dropped", "mapped"}
    assert by_key["reasoning_effort"].action in {"mapped", "dropped", "overridden"}
    assert "include_thoughts" in by_key


def test_guard_can_fail() -> None:
    """A processor that writes a raw unsupported key onto the wire is caught (I1)."""
    rules = {
        "thinking_budget": ControlRule.model_validate({"supported": False}),
        "temperature": ControlRule.model_validate({}),
    }
    leaky = CompiledControlsMap(rules=rules)
    # Simulate the class: an unsupported key smuggled through as raw passthrough.
    original = leaky.outbound

    def smuggle(canonical: dict[str, Any], **kw: Any):
        out, adj = original(canonical, **kw)
        out["thinking_budget"] = canonical.get("thinking_budget")
        return out, [a for a in adj if a.key != "thinking_budget"]

    object.__setattr__(leaky, "outbound", smuggle)
    assert any(p.startswith("I1 thinking_budget") for p in violations(leaky))


def test_budget_beats_effort_and_the_run_says_so() -> None:
    """Budget-taking targets (Gemini legacy, Anthropic budget mode): the explicit number is
    the more specific instruction; the effort is recorded as overridden. Effort-native
    targets keep their tier and name the foreign number as lost."""
    for name, data in _offerings().items():
        controls = _controls(data["rules"])
        _params, adjustments = run_kitchen_sink(controls)
        by_key = {a.key: a for a in adjustments}
        if controls._takes_raw_thinking_budget():
            over = [a for a in adjustments if a.key == "reasoning_effort" and a.action == "overridden"]
            assert over, f"{name}: reasoning_effort lost silently"
            assert "thinking_budget 2048" in over[0].reason
            assert over[0].canonical_value == "high"
        else:
            assert "thinking_budget" in by_key, f"{name}: thinking_budget lost silently"


def test_effort_alone_is_not_overridden() -> None:
    controls = _controls(_offerings()["google_gemini_flash_lite_latest"]["rules"])
    _params, adjustments = controls.outbound({"reasoning_effort": "high"})
    assert not [a for a in adjustments if a.action == "overridden"]


def test_meaning_finder_sees_nested_shapes() -> None:
    """The I3 detector itself can fail: it finds a value folded into any nested shape."""
    assert meaning_paths({"thinking_config": {"thinking_budget": 1}}, "thinking_budget")
    assert meaning_paths({"thinking": {"budget_tokens": 1}}, "thinking_budget")
    assert meaning_paths({"reasoning": {"effort": "low"}}, "reasoning_effort")
    assert not meaning_paths({"max_tokens": 5}, "thinking_budget")
