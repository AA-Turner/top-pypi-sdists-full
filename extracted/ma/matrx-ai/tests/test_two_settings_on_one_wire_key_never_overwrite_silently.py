"""Two settings the caller set that decide ONE wire value: the specific one wins in any key order, the loser is recorded.

Live (PB-03 U6, Gemini copy, request snapshot 92b94b05): the copy set ``reasoning_effort: high`` and
``thinking_level: low``. On the LIVE google_chat rules both go through the ``google_thinking``
processor (``thinking_level`` itself is ``supported: false``); the effort used to win in either key
order and ``thinking_level`` was recorded as a plain drop. Law ``specific-beats-general`` (the one
``bridge_numbers`` declares) now decides on EVERY path: the named level wins, the effort is recorded
``overridden`` with the kept value in ``to``, announced (not faithful).

SUT: ``CompiledControlsMap.outbound`` on the LIVE rules (fixtures/pb03_live_depth_rules.json,
read from ai.api + ai.offering.override) for the processor path, and on scalar rules sharing one
provider_key for the scalar path.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import CatalogSetting, ControlRule

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "pb03_live_depth_rules.json").read_text())
SETTINGS = {s["key"]: CatalogSetting.model_validate(s) for s in FIXTURE["settings"]}
LAW = "specific-beats-general"
LEVELS = ["minimal", "low", "medium", "high"]

# Which depth key wins per live processor shape, and the law each loser carries. This is EXACTLY the
# order each processor had before C73 (effort beat budget on adaptive Claude and Gemini 3; budget beat
# effort on Gemini legacy and Claude budget mode) with one declared exception: Gemini 3's named level
# beats an effort tier (specific-beats-general). A key a processor does not carry is not judged.
KEY = {"level": "thinking_level", "budget": "thinking_budget", "effort": "reasoning_effort"}
VALUE = {"level": "low", "budget": 4096, "effort": "high"}
LABEL = {
    "gemini_3_flash": "gemini 3",
    "gemini_3_pro": "gemini 3",
    "gemini_legacy": "gemini legacy",
    "claude_adaptive": "adaptive",
    "claude_adaptive_always_on": "adaptive",
    "claude_budget": "budget mode",
}
GEMINI_3_ORDER = [("level", "effort"), ("level", "budget"), ("effort", "budget")]
ADAPTIVE_ORDER = [("effort", "budget"), ("effort", "level"), ("budget", "level")]
WINNERS = {  # (winner, loser) pairs per live offering
    "gemini_3_flash": GEMINI_3_ORDER,
    "gemini_3_pro": GEMINI_3_ORDER,
    "gemini_legacy": [("budget", "effort")],
    "claude_adaptive": ADAPTIVE_ORDER,
    "claude_adaptive_always_on": ADAPTIVE_ORDER,
    "claude_budget": [("budget", "effort")],
    "together": [],
}
RAW_BUDGET_LAW = "budget-beats-effort (raw-budget model)"  # bridge_numbers decides it before the processor runs


def _live(name: str) -> CompiledControlsMap:
    from matrx_ai.catalog.controls import compile_controls

    o = FIXTURE["offerings"][name]
    rules = lambda params: {k: ControlRule.model_validate(v) for k, v in params.items()}  # noqa: E731
    return compile_controls(rules(o["api_params"]), rules(o["override"]), SETTINGS)


def _cases():
    for name, pairs in WINNERS.items():
        for winner, loser in pairs:
            yield name, winner, loser


@pytest.mark.parametrize("flip", [False, True])
@pytest.mark.parametrize(("name", "winner", "loser"), list(_cases()))
def test_every_live_processor_keeps_its_order_and_names_the_law(name, winner, loser, flip) -> None:
    controls = _live(name)
    pair = [(KEY[winner], VALUE[winner]), (KEY[loser], VALUE[loser])]
    caller = dict(reversed(pair) if flip else pair)
    params, adjustments = controls.outbound(caller)
    solo, _ = controls.outbound({KEY[winner]: VALUE[winner]})
    assert params == solo, f"{name}: the wire must be what the winning key alone produces"
    lost = [a for a in adjustments if a.key == KEY[loser] and a.action == "overridden"]
    assert len(lost) == 1, f"{name}: {KEY[loser]} lost with no record: {[(a.key, a.action) for a in adjustments]}"
    if (winner, loser) == ("level", "effort"):
        accepted = {LAW}
    else:
        accepted = {f"{winner}-beats-{loser} ({LABEL[name]})"}
        if (winner, loser) == ("budget", "effort"):
            accepted.add(RAW_BUDGET_LAW)
    assert lost[0].law in accepted, (lost[0].law, accepted)
    assert lost[0].sent_value == VALUE[winner], "the kept value must be in `to`"
    assert lost[0].canonical_value == VALUE[loser]
    assert lost[0].faithful is False, "a lost value must be announced, not recorded quietly"


@pytest.mark.parametrize("name", list(WINNERS))
def test_a_lone_depth_key_records_no_override(name) -> None:
    for short in ("effort", "level", "budget"):
        _params, adjustments = _live(name).outbound({KEY[short]: VALUE[short]})
        assert [a for a in adjustments if a.action == "overridden"] == [], (name, short)


SHARED_KEY = "thinking_config.thinking_level"


def _scalar() -> CompiledControlsMap:
    rules = {
        "reasoning_effort": {"accepts": LEVELS, "provider_key": SHARED_KEY},
        "thinking_level": {"supported": True, "accepts": LEVELS, "provider_key": SHARED_KEY},
    }
    return CompiledControlsMap(rules={k: ControlRule.model_validate(v) for k, v in rules.items()})


@pytest.mark.parametrize("order", [("reasoning_effort", "thinking_level"), ("thinking_level", "reasoning_effort")])
def test_scalar_path_same_law_in_either_key_order(order) -> None:
    values = {"reasoning_effort": "high", "thinking_level": "low"}
    params, adjustments = _scalar().outbound({k: values[k] for k in order})
    assert params["thinking_config"]["thinking_level"] == "low"
    [lost] = [a for a in adjustments if a.action == "overridden"]
    assert (lost.key, lost.canonical_value, lost.sent_value, lost.law) == (
        "reasoning_effort", "high", "low", "specific-beats-general"
    )
    assert lost.faithful is False
