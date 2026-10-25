"""Gemini 3 has no thinking OFF: "none" lands on the model's LOWEST level, never its default.

Live 2026-10-13: a person chose reasoning "none" on gemini-3.8-flash. The gemini_3
processor sent no level for "none", so the model's own default ran (more thinking,
not less). Three faults, each pinned here:

* off (effort "none", level "none", budget <= 0) now sends the lowest level, which
  the offering's vocabulary reconciles to the lowest THIS model takes;
* the cell ``default`` was backfilled BEFORE the off was read, so an off sent
  through a consumed key ran at the default — it now applies only when nothing
  was asked;
* an explicit ``thinking_level`` was ignored (the default replaced it).
"""

from __future__ import annotations

import pytest

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule

# The live gemini-3.8-flash reasoning_effort cell (offering cb1f1119), verbatim shape.
GEMINI_38_FLASH = {
    "default": "medium",
    "processor": "google_thinking",
    "supported": True,
    "ui_values": ["auto", "none", "low", "medium", "high"],
    "processor_config": {
        "mode": "gemini_3",
        "family": "flash",
        "consumes": ["thinking_budget", "thinking_level", "include_thoughts", "reasoning_summary", "clear_thinking"],
        "default_include_thoughts": True,
    },
}
ORDER = {"reasoning_effort": ["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"]}


def _level(canonical: dict) -> str | None:
    rule = ControlRule.model_validate(GEMINI_38_FLASH)
    params, _ = CompiledControlsMap(rules={"reasoning_effort": rule}, value_orders=ORDER).outbound(canonical)
    return params.get("thinking_config", {}).get("thinking_level")


@pytest.mark.parametrize(
    "canonical",
    [{"reasoning_effort": "none"}, {"thinking_budget": 0}, {"thinking_level": "none"}],
    ids=["effort-none", "budget-zero", "level-none"],
)
def test_off_sends_the_lowest_level(canonical: dict) -> None:
    assert _level(canonical) == "low"


def test_unsupported_minimal_reconciles_to_low() -> None:
    assert _level({"reasoning_effort": "minimal"}) == "low"


def test_unset_takes_the_platform_default_over_a_deeper_cell_default() -> None:
    # Owner ruling 2026-10-24: unset is the platform default ("low"); a cell's
    # deeper product default (medium) no longer decides an unset run.
    assert _level({}) == "low"


def test_auto_is_the_providers_own_auto() -> None:
    assert _level({"reasoning_effort": "auto"}) is None


def test_a_budget_is_translated_not_replaced_by_the_default() -> None:
    assert _level({"thinking_budget": 20000}) == "high"


@pytest.mark.parametrize("level", ["low", "medium", "high"])
def test_an_explicit_level_is_sent_as_chosen(level: str) -> None:
    assert _level({"thinking_level": level}) == level


def test_off_is_reported_never_silent() -> None:
    rule = ControlRule.model_validate(GEMINI_38_FLASH)
    _, adjustments = CompiledControlsMap(rules={"reasoning_effort": rule}, value_orders=ORDER).outbound(
        {"reasoning_effort": "none"}
    )
    assert [a.sent_value for a in adjustments] == ["low"]
    assert all(a.action != "dropped" for a in adjustments)
