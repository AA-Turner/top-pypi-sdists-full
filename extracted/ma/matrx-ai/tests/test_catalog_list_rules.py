"""K6 amendment (FIXV1, CONTRACTS v5) — LIST-valued settings: ``max_items`` and
``drop_items_matching``.

Live failures this pins (V1 verifier, 2026-10-04): Groq qwen3.8-27b with 10 stop
sequences ("maximum number of items is 4", conversation fdf78037…) and Claude Haiku
4.5 with a whitespace-only stop sequence ("each stop sequence must contain
non-whitespace", 555d5547…) both returned NO answer. With the cell carrying the
provider's limit, the wire never carries the refused shape. Pure units — no DB.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule
from matrx_ai.providers.outbound_params import resolve_outbound_params

STOPS = [f"END-{i}" for i in range(10)]


def _outbound(rule: dict, stops: list[str]) -> tuple[dict, list]:
    controls = CompiledControlsMap(rules={"stop_sequences": ControlRule.model_validate(rule)})
    return controls.outbound({"stop_sequences": stops})


def test_groq_cell_caps_stop_sequences_at_four() -> None:
    wire, adjustments = _outbound({"provider_key": "stop", "max_items": 4}, STOPS)
    assert wire["stop"] == STOPS[:4]
    (adj,) = [a for a in adjustments if a.key == "stop_sequences"]
    assert adj.action == "clamped" and adj.expected is True


def test_anthropic_cell_removes_whitespace_only_items() -> None:
    rule = {"provider_key": "stop_sequences", "drop_items_matching": r"\s*"}
    wire, _ = _outbound(rule, ["   ", "END", ""])
    assert wire["stop_sequences"] == ["END"]


def test_a_list_emptied_by_the_rule_is_omitted_not_sent_empty() -> None:
    rule = {"provider_key": "stop_sequences", "drop_items_matching": r"\s*"}
    wire, adjustments = _outbound(rule, ["   "])
    assert "stop_sequences" not in wire
    assert [a.action for a in adjustments if a.key == "stop_sequences"] == ["omitted"]


def test_a_list_within_the_limit_is_untouched_and_unannounced() -> None:
    wire, adjustments = _outbound({"provider_key": "stop", "max_items": 4}, STOPS[:3])
    assert wire["stop"] == STOPS[:3]
    assert not [a for a in adjustments if a.key == "stop_sequences"]


def test_a_rule_without_the_fields_passes_every_item_through() -> None:
    wire, _ = _outbound({"provider_key": "stop"}, STOPS)
    assert wire["stop"] == STOPS


def test_the_full_seam_applies_the_cap() -> None:
    controls = CompiledControlsMap(
        rules={"stop_sequences": ControlRule.model_validate({"provider_key": "stop", "max_items": 4})}
    )
    wire = resolve_outbound_params(SimpleNamespace(stop_sequences=STOPS), controls)
    assert wire["stop"] == STOPS[:4]


@pytest.mark.parametrize("bad", [{"max_items": 0}, {"drop_items_matching": "("}])
def test_invalid_list_constraints_fail_loudly(bad: dict) -> None:
    with pytest.raises(ValueError):
        ControlRule.model_validate(bad)
