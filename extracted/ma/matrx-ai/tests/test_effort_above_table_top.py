"""An effort above an effort->number table's top lands on the TOP entry, never on
the unknown-effort default (FIXV1 item 6, live 2026-10-04: gemini-2.5-flash
reasoning_effort "max" sent thinking_budget 1,024)."""

from __future__ import annotations

from matrx_ai.catalog import translation_defaults as D
from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule
from matrx_ai.catalog.processors import effort_lookup

CONSUMES = ["thinking_budget", "thinking_level", "include_thoughts", "reasoning_summary"]


def _wire(processor: str, config: dict, effort: str) -> dict:
    rule = ControlRule.model_validate(
        {"processor": processor, "processor_config": {"consumes": CONSUMES, **config}}
    )
    params, _ = CompiledControlsMap(rules={"reasoning_effort": rule}).outbound({"reasoning_effort": effort})
    return params


def test_gemini_25_max_effort_gets_the_top_budget_not_the_unknown_one() -> None:
    wire = _wire("google_thinking", {"mode": "legacy"}, "max")
    assert wire["thinking_config"]["thinking_budget"] == D.GOOGLE_LEGACY_EFFORT_TO_BUDGET["xhigh"]


def test_every_table_maps_max_to_its_top() -> None:
    for table in (D.GOOGLE_LEGACY_EFFORT_TO_BUDGET, D.ANTHROPIC_EFFORT_TO_BUDGET, *D.GOOGLE_3_EFFORT_TO_LEVEL.values()):
        assert effort_lookup(table, "max") == table["xhigh"], table


def test_an_off_scale_value_still_gets_the_unknown_default() -> None:
    assert effort_lookup({"low": 1, "high": 2}, "banana", 7) == 7
    assert effort_lookup({"low": 1, "high": 2}, "medium", 7) == 7  # inside the range: not this rule


# ── NET lane (live 2026-10-04): a thinking budget is bounded by the model's
# BUDGET ceiling, never by its OUTPUT maximum (da318b6f: 2.5 Pro's 100,000 was
# clamped to its 64,000 output max; Google's 2.5 Pro range is 128..32768). ──


def _legacy_wire(config: dict, canonical: dict, output_maximum: int | None) -> dict:
    rule = ControlRule.model_validate(
        {"processor": "google_thinking", "processor_config": {"consumes": CONSUMES, "mode": "legacy", **config}}
    )
    controls = CompiledControlsMap(rules={"reasoning_effort": rule})
    if output_maximum is not None:
        controls = controls.with_output_maximum(output_maximum)
    params, _ = controls.outbound(canonical)
    return params


def test_budget_is_clamped_by_the_declared_budget_ceiling_not_the_output_max() -> None:
    wire = _legacy_wire({"max_thinking_budget": 32768}, {"thinking_budget": 100000}, output_maximum=64000)
    assert wire["thinking_config"]["thinking_budget"] == 32768


def test_the_output_maximum_never_becomes_the_budget() -> None:
    wire = _legacy_wire({}, {"thinking_budget": 100000}, output_maximum=64000)
    assert wire["thinking_config"]["thinking_budget"] != 64000
    assert wire["thinking_config"]["thinking_budget"] == D.GOOGLE_THINKING_BUDGET_FIELD_MAX


def test_max_effort_reaches_the_declared_top_budget() -> None:
    wire = _legacy_wire({"max_thinking_budget": 32768}, {"reasoning_effort": "max"}, output_maximum=64000)
    assert wire["thinking_config"]["thinking_budget"] == 32768


# ── BURN lane (live 2026-10-04, record ae16d0f2): a budget BELOW the model's
# floor clamps UP to the floor — Google: "The thinking budget 50 is invalid. Please
# choose a value between 128 and 32768" (2.5 Pro; ai.google.dev/gemini-api/docs/thinking).


def test_budget_below_the_declared_floor_clamps_up_to_the_floor() -> None:
    config = {"max_thinking_budget": 32768, "min_thinking_budget": 128}
    wire = _legacy_wire(config, {"thinking_budget": 50}, output_maximum=None)
    assert wire["thinking_config"]["thinking_budget"] == 128


def test_low_effort_below_the_floor_clamps_up_to_the_floor() -> None:
    config = {"max_thinking_budget": 32768, "min_thinking_budget": 128}
    for effort in ("minimal", "low"):
        wire = _legacy_wire(config, {"reasoning_effort": effort}, output_maximum=None)
        assert wire["thinking_config"]["thinking_budget"] >= 128, effort


def test_budget_inside_the_range_is_untouched_by_the_floor() -> None:
    config = {"max_thinking_budget": 32768, "min_thinking_budget": 128}
    wire = _legacy_wire(config, {"thinking_budget": 4000}, output_maximum=None)
    assert wire["thinking_config"]["thinking_budget"] == 4000
