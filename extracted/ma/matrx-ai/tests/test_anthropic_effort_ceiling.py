"""ai_047 — the ENGINE-side effort ceiling on Anthropic adaptive thinking.

The offering's ui_values gates xhigh/max in the UI only; a raw API caller can
send reasoning_effort="xhigh"/"max" straight at a BASE listing. The second,
independent gate is processor_config["effort_ceiling"] on the anthropic_thinking
processor (mode=adaptive): anything above the ceiling clamps DOWN to it with a
loud "effort_ceiling" Adjustment. The premium "-max" listings carry no ceiling.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.catalog.models import Adjustment
from matrx_ai.catalog.processors import ProcessorContext, anthropic_thinking

BASE_CONFIG: dict[str, Any] = {
    "mode": "adaptive",
    "order": 100,
    "consumes": [
        "thinking_budget",
        "thinking_level",
        "include_thoughts",
        "reasoning_summary",
        "clear_thinking",
    ],
    "default_max_tokens": 32768,
    "effort_ceiling": "high",
}

MAX_CONFIG: dict[str, Any] = {k: v for k, v in BASE_CONFIG.items() if k != "effort_ceiling"}


def run(effort: str | None, config: dict[str, Any]) -> tuple[dict[str, Any], list[Adjustment]]:
    canonical: dict[str, Any] = {}
    if effort is not None:
        canonical["reasoning_effort"] = effort
    adjustments: list[Adjustment] = []
    ctx = ProcessorContext(key="reasoning_effort", config=config, adjustments=adjustments)
    params = anthropic_thinking(canonical, {}, ctx)
    return params, adjustments


class TestBaseOfferingCeiling:
    @pytest.mark.parametrize("requested", ["xhigh", "max"])
    def test_above_ceiling_clamps_with_loud_adjustment(self, requested: str) -> None:
        params, adjustments = run(requested, BASE_CONFIG)
        assert params["output_config"]["effort"] == "high"
        assert params["thinking"] == {"type": "adaptive", "display": "summarized"}
        assert len(adjustments) == 1
        adj = adjustments[0]
        assert adj.key == "reasoning_effort"
        assert adj.action == "effort_ceiling"
        assert adj.canonical_value == requested
        assert adj.sent_value == "high"
        assert "premium" in adj.reason

    @pytest.mark.parametrize("requested", ["low", "medium", "high"])
    def test_at_or_below_ceiling_passes_through(self, requested: str) -> None:
        params, adjustments = run(requested, BASE_CONFIG)
        assert params["output_config"]["effort"] == requested
        assert adjustments == []

    def test_none_stays_explicit_off(self) -> None:
        params, adjustments = run("none", BASE_CONFIG)
        assert "thinking" not in params
        assert "output_config" not in params
        assert adjustments == []

    def test_auto_stays_unset(self) -> None:
        # HOUSE SEMANTICS (ai_041): "auto" == unset — no thinking key, no clamp.
        params, adjustments = run("auto", BASE_CONFIG)
        assert "thinking" not in params
        assert "output_config" not in params
        assert adjustments == []

    def test_unset_effort_untouched(self) -> None:
        params, adjustments = run(None, BASE_CONFIG)
        assert "thinking" not in params
        assert adjustments == []

    def test_budget_derived_tiers_never_exceed_ceiling(self) -> None:
        # Priority-2 budget ranges top out at "high" — the ceiling is a no-op
        # there, but must not disturb them either.
        adjustments: list[Adjustment] = []
        ctx = ProcessorContext(
            key="reasoning_effort", config=BASE_CONFIG, adjustments=adjustments
        )
        params = anthropic_thinking({"thinking_budget": 30000}, {}, ctx)
        assert params["output_config"]["effort"] == "high"
        assert adjustments == []


class TestMaxOfferingNoCeiling:
    @pytest.mark.parametrize("requested", ["xhigh", "max"])
    def test_deep_tiers_pass_natively(self, requested: str) -> None:
        params, adjustments = run(requested, MAX_CONFIG)
        assert params["output_config"]["effort"] == requested
        assert adjustments == []


class TestInvalidCeilingScreams:
    def test_invalid_ceiling_value_raises(self) -> None:
        bad = {**BASE_CONFIG, "effort_ceiling": "extreme"}
        with pytest.raises(ValueError, match="effort_ceiling"):
            run("xhigh", bad)
