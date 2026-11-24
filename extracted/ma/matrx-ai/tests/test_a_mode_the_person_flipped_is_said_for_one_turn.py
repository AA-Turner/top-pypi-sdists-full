"""A mode the person FLIPPED is said to the agent, as data, for that one turn (D17).

"Set" = the mode at this turn differs from the mode the agent last knew (``agent_mode_known``, kept in the
conversation's metadata). Opening a chat already in a mode means nothing; the agent's own switch never produces
the line; the line is gone on the next turn.

Fails when: the line is missing on the turn the person flipped; it survives into the next turn; the agent's own
switch produces it; a chat that simply opens in a mode gets it.
"""

from __future__ import annotations

import pytest

from matrx_ai.config import UnifiedConfig
from matrx_ai.config.agent_modes import running_modes_for, settle_turn_mode
from matrx_ai.config.prompt_block_producers import produce_agent_modes

MODES = [
    {"key": "discovery", "name": "Discovery", "description": "learn first", "instructions": "Ask first."},
    {"key": "answer", "name": "Answer", "description": "answer now", "instructions": "Answer now."},
]
LINE = "by hand this turn"


@pytest.fixture
def recorded(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    monkeypatch.setattr(
        "matrx_ai.config.agent_modes.remember_known_mode", lambda cid, key: rows.append((str(cid), str(key)))
    )
    return rows


def _config(mode: str | None, known: str | None) -> UnifiedConfig:
    config = UnifiedConfig(model="m", messages=[])
    config.agent_modes = [dict(m) for m in MODES]
    config.agent_mode = mode
    config.agent_mode_known = known
    return config


def _block(config: UnifiedConfig, request_id: str) -> str:
    settle_turn_mode(config, request_id=request_id, conversation_id="c1")
    return produce_agent_modes(config) or ""


def test_the_turn_the_person_flipped_says_so_on_every_call(recorded) -> None:
    config = _config("discovery", known="answer")
    first = _block(config, "r1")
    said = "The person switched the mode to Discovery by hand this turn (it was Answer)."
    assert said in first
    # An ADDITIONAL line: the current mode and its instructions are always there too.
    assert "Current mode: Discovery." in first and "Ask first." in first
    assert said in _block(config, "r1"), "every call of that turn"
    assert recorded == [("c1", "discovery")]


def test_the_next_turn_has_no_line(recorded) -> None:
    config = _config("discovery", known="answer")
    _block(config, "r1")
    nxt = _block(config, "r2")
    assert LINE not in nxt
    assert "Current mode: Discovery." in nxt and "Ask first." in nxt, "the block itself never goes away"


def test_the_agents_own_switch_never_produces_it(recorded) -> None:
    config = _config("discovery", known="discovery")
    assert LINE not in _block(config, "r1")
    running_modes_for(config).switch("answer")
    assert LINE not in _block(config, "r1"), "the rest of the turn"
    assert LINE not in _block(config, "r2"), "the next turn"


def test_a_chat_that_simply_opens_in_a_mode_says_nothing(recorded) -> None:
    assert LINE not in _block(_config("discovery", known=None), "r1"), "nothing known yet"
    assert LINE not in _block(_config("discovery", known="discovery"), "r1"), "same mode as known"
