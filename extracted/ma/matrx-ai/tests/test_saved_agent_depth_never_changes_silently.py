"""No saved agent's depth changes silently (Arman, 2026-11-09, ruling on C73).

Replays the 90 LIVE agent.definition_version rows that carry both thinking_budget and reasoning_effort
(fixtures/pb03_saved_agent_depth_rows.json, read-only snapshot) on the live rules of seven offerings
(fixtures/pb03_live_depth_rules.json) and compares the wire with what the PRE-C73 code sent for the
same rows (stored in the snapshot). Source first: a value set for THIS run beats a stored agent value.

ZERO exceptions: a saved row sends exactly what it sent before C73 (history versions and the current
definitions that store both a level and an effort). A named thinking_level beats a reasoning_effort tier
(``specific-beats-general``, the original U6 fix) only when both were sent together for ONE run.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog.canonicalize import canonical_settings_from_config
from matrx_ai.catalog.controls import compile_controls
from matrx_ai.catalog.models import CatalogSetting, ControlRule

FIXTURES = Path(__file__).parent / "fixtures"
RULES = json.loads((FIXTURES / "pb03_live_depth_rules.json").read_text())
SAVED = json.loads((FIXTURES / "pb03_saved_agent_depth_rows.json").read_text())
SETTINGS = {s["key"]: CatalogSetting.model_validate(s) for s in RULES["settings"]}
GEMINI_3 = {"gemini_3_flash", "gemini_3_pro"}


def _controls(name: str):
    o = RULES["offerings"][name]
    rules = lambda p: {k: ControlRule.model_validate(v) for k, v in p.items()}  # noqa: E731
    return compile_controls(rules(o["api_params"]), rules(o["override"]), SETTINGS)


def _wire(name: str, *, stored: dict[str, Any], run: dict[str, Any] | None = None) -> tuple[dict[str, Any], list[Any]]:
    """The wire for a config whose ``stored`` depth came from the agent and ``run`` was set for this run."""
    values = {**stored, **(run or {})}
    cfg = SimpleNamespace(
        reasoning_effort=values.get("reasoning_effort"),
        thinking_budget=values.get("thinking_budget"),
        thinking_level=values.get("thinking_level"),
        disable_reasoning=None,
        authored_settings=dict(stored),
    )
    params, adjustments = _controls(name).outbound(canonical_settings_from_config(cfg))
    return json.loads(json.dumps(params, default=str, sort_keys=True)), adjustments


def _row_settings(row: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in row.items() if k != "id" and v is not None}


@pytest.mark.parametrize("name", list(SAVED["pre_c73_wire"]))
@pytest.mark.parametrize(("rows", "wires"), [("rows", "pre_c73_wire"), ("current_rows", "pre_c73_wire_current")])
def test_every_saved_row_sends_exactly_what_it_sent_before_c73(name: str, rows: str, wires: str) -> None:
    """ZERO exceptions: history versions (90) and the current definitions that store both a level and an effort."""
    changed = [
        row["id"][:8]
        for row, before in zip(SAVED[rows], SAVED[wires][name], strict=True)
        if _wire(name, stored=_row_settings(row))[0] != before
    ]
    assert not changed, f"{name}: {len(changed)} saved rows changed depth: {changed[:5]}"


@pytest.mark.parametrize("name", sorted(GEMINI_3))
def test_a_stored_pair_records_the_old_winner_with_its_law(name: str) -> None:
    """Both stored on Gemini 3: effort still wins (as before C73) and the level loser is recorded and named."""
    _wire_out, adjustments = _wire(name, stored={"reasoning_effort": "high", "thinking_level": "low"})
    lost = [a for a in adjustments if a.key == "thinking_level" and a.action == "overridden"]
    assert len(lost) == 1 and lost[0].law == "effort-beats-level (gemini 3)" and lost[0].sent_value == "high"


@pytest.mark.parametrize("name", sorted(GEMINI_3))
def test_a_level_and_effort_sent_together_for_one_run_keeps_the_level_over_effort(name: str) -> None:
    wire, adjustments = _wire(name, stored={}, run={"reasoning_effort": "high", "thinking_level": "low"})
    alone, _ = _wire(name, stored={}, run={"thinking_level": "low"})
    assert wire == alone
    lost = [a for a in adjustments if a.key == "reasoning_effort" and a.action == "overridden"]
    assert len(lost) == 1 and lost[0].law == "specific-beats-general" and lost[0].sent_value == "low"


@pytest.mark.parametrize("name", list(SAVED["pre_c73_wire"]))
def test_a_per_run_effort_beats_a_stored_budget(name: str) -> None:
    stored = {"thinking_budget": 2048}
    run = {"reasoning_effort": "high"}
    wire, adjustments = _wire(name, stored=stored, run=run)
    alone, _ = _wire(name, stored={}, run=run)
    assert wire == alone, f"{name}: the person's per-run effort must decide the wire"
    lost = [a for a in adjustments if a.key == "thinking_budget" and a.action == "overridden"]
    assert len(lost) == 1 and lost[0].law == "this-run-beats-stored-agent"
    assert lost[0].sent_value == "high" and lost[0].faithful is False


@pytest.mark.parametrize("name", ["claude_adaptive", "gemini_legacy"])
def test_a_per_run_budget_beats_a_stored_effort(name: str) -> None:
    wire, adjustments = _wire(name, stored={"reasoning_effort": "high"}, run={"thinking_budget": 2048})
    alone, _ = _wire(name, stored={}, run={"thinking_budget": 2048})
    assert wire == alone
    lost = [a for a in adjustments if a.key == "reasoning_effort" and a.action == "overridden"]
    assert len(lost) == 1 and lost[0].law == "this-run-beats-stored-agent" and lost[0].sent_value == 2048


@pytest.mark.parametrize("name", ["claude_adaptive", "claude_adaptive_always_on", "gemini_3_flash"])
def test_a_stored_zero_budget_never_switches_thinking_off_over_an_effort(name: str) -> None:
    """Pre-C73, effort decided before budget on these processors: budget 0 beside an effort did nothing."""
    before, _ = _wire(name, stored={}, run={"reasoning_effort": "high"})
    wire, _ = _wire(name, stored={"thinking_budget": 0, "reasoning_effort": "high"})
    assert wire == before
    wire_run, _ = _wire(name, stored={"thinking_budget": 0}, run={"reasoning_effort": "high"})
    assert wire_run == before


def test_one_source_alone_runs_exactly_as_saved() -> None:
    wire, adjustments = _wire("claude_adaptive", stored={"reasoning_effort": "high", "thinking_budget": 2048})
    assert not [a for a in adjustments if a.law == "this-run-beats-stored-agent"]


def _wire_with_stored_switch(
    name: str, *, disable_reasoning: bool, run: dict[str, Any]
) -> tuple[dict[str, Any], list[Any]]:
    """A saved agent that stores only ``disable_reasoning`` (its effort is DERIVED from it), run with a
    depth value set for this run (canonicalize.py: the derived effort is marked stored, 2026-11-10)."""
    cfg = SimpleNamespace(
        reasoning_effort=None,
        thinking_budget=run.get("thinking_budget"),
        thinking_level=run.get("thinking_level"),
        disable_reasoning=disable_reasoning,
        authored_settings={"disable_reasoning": disable_reasoning},
    )
    params, adjustments = _controls(name).outbound(canonical_settings_from_config(cfg))
    return json.loads(json.dumps(params, default=str, sort_keys=True)), adjustments


@pytest.mark.parametrize("name", sorted(GEMINI_3))
def test_a_per_run_level_beats_a_stored_reasoning_switch_on_gemini_3(name: str) -> None:
    """Stored ``disable_reasoning=False`` derives effort "medium"; a level set for THIS run decides the wire."""
    run = {"thinking_level": "low"}
    wire, adjustments = _wire_with_stored_switch(name, disable_reasoning=False, run=run)
    alone, _ = _wire(name, stored={}, run=run)
    assert wire == alone, f"{name}: the per-run level must decide the wire over the stored switch"
    lost = [a for a in adjustments if a.key == "reasoning_effort" and a.action == "overridden"]
    assert len(lost) == 1 and lost[0].law == "this-run-beats-stored-agent"


@pytest.mark.parametrize("name", sorted(GEMINI_3))
def test_a_per_run_budget_beats_a_stored_reasoning_switch_on_gemini_3(name: str) -> None:
    run = {"thinking_budget": 2048}
    wire, adjustments = _wire_with_stored_switch(name, disable_reasoning=False, run=run)
    alone, _ = _wire(name, stored={}, run=run)
    assert wire == alone
    lost = [a for a in adjustments if a.key == "reasoning_effort" and a.action == "overridden"]
    assert len(lost) == 1 and lost[0].law == "this-run-beats-stored-agent"


@pytest.mark.parametrize("name", ["claude_budget", "claude_adaptive"])
def test_a_per_run_budget_beats_a_stored_reasoning_switch_on_anthropic(name: str) -> None:
    run = {"thinking_budget": 2048}
    wire, adjustments = _wire_with_stored_switch(name, disable_reasoning=False, run=run)
    alone, _ = _wire(name, stored={}, run=run)
    assert wire == alone, f"{name}: the per-run budget must decide the wire over the stored switch"
    lost = [a for a in adjustments if a.key == "reasoning_effort" and a.action == "overridden"]
    assert len(lost) == 1 and lost[0].law == "this-run-beats-stored-agent" and lost[0].sent_value == 2048

