"""processor_config.thinking_always_on — Opus 5.5 / Fable 5.1 / Mythos 5.x.

These models reject thinking.type="disabled". Every "off" signal must convert to
the NEAREST accepted equivalent (adaptive, lowest effort, display omitted) with a
server-logged ``mapped`` Adjustment — never omit the block (that runs the model's
deeper DEFAULT effort) and never send "disabled" (400).
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.catalog.models import Adjustment
from matrx_ai.catalog.processors import ProcessorContext, anthropic_thinking

BASE: dict[str, Any] = {
    "mode": "adaptive",
    "order": 100,
    "consumes": [
        "thinking_budget",
        "thinking_level",
        "include_thoughts",
        "reasoning_summary",
        "clear_thinking",
    ],
    "default_max_tokens": 128000,
}
ALWAYS_ON = {**BASE, "thinking_always_on": True}
ALWAYS_ON_CEILING = {**ALWAYS_ON, "effort_ceiling": "high"}


def run(
    canonical: dict[str, Any], config: dict[str, Any]
) -> tuple[dict[str, Any], list[Adjustment]]:
    adjustments: list[Adjustment] = []
    ctx = ProcessorContext(key="reasoning_effort", config=config, adjustments=adjustments)
    return anthropic_thinking(dict(canonical), {}, ctx), adjustments


OFF_SIGNALS = [
    ({"reasoning_effort": "none"}, "reasoning_effort"),
    ({"include_thoughts": False}, "include_thoughts"),
    ({"thinking_budget": 0}, "thinking_budget"),
]


class TestAlwaysOn:
    @pytest.mark.parametrize("canonical,key", OFF_SIGNALS)
    def test_off_converts_to_lowest_effort_hidden(
        self, canonical: dict[str, Any], key: str
    ) -> None:
        params, adjustments = run(canonical, ALWAYS_ON)
        assert params["thinking"] == {"type": "adaptive", "display": "omitted"}
        assert params["output_config"]["effort"] == "low"
        assert params["max_tokens"] == 128000
        assert len(adjustments) == 1
        adj = adjustments[0]
        assert adj.key == key and adj.action == "mapped"
        assert "cannot be disabled" in adj.reason

    def test_never_sends_disabled(self) -> None:
        for canonical, _ in OFF_SIGNALS:
            params, _ = run(canonical, ALWAYS_ON)
            assert params["thinking"].get("type") != "disabled"

    def test_hidden_but_deep_keeps_requested_effort(self) -> None:
        params, adjustments = run(
            {"reasoning_effort": "high", "include_thoughts": False}, ALWAYS_ON
        )
        assert params["output_config"]["effort"] == "high"
        assert params["thinking"]["display"] == "omitted"
        assert adjustments[0].key == "include_thoughts"

    def test_floor_still_respects_effort_ceiling(self) -> None:
        params, adjustments = run(
            {"reasoning_effort": "max", "include_thoughts": False}, ALWAYS_ON_CEILING
        )
        assert params["output_config"]["effort"] == "high"
        assert [a.action for a in adjustments] == ["effort_ceiling", "mapped"]

    def test_unset_still_defers_to_provider_default(self) -> None:
        params, adjustments = run({}, ALWAYS_ON)
        assert "thinking" not in params and "output_config" not in params
        assert adjustments == []

    def test_normal_effort_unchanged(self) -> None:
        params, adjustments = run({"reasoning_effort": "medium"}, ALWAYS_ON)
        assert params["thinking"] == {"type": "adaptive", "display": "summarized"}
        assert params["output_config"]["effort"] == "medium"
        assert adjustments == []


class TestWithoutFlagBehaviourIsUnchanged:
    @pytest.mark.parametrize("canonical,_key", OFF_SIGNALS)
    def test_off_still_omits_block(self, canonical: dict[str, Any], _key: str) -> None:
        params, adjustments = run(canonical, BASE)
        assert "thinking" not in params and "output_config" not in params
        assert adjustments == []
