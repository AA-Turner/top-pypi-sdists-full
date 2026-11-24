"""prompt_cache_prefix_drift (feedback 3634bafb, 2026-11-15): "the send boundary rewrote N block(s)
it could not place on the wire".

Before: ``_fit_wire`` dropped the earlier turns' replayed page blocks only on the round that went
over the host budget. Round 1 of a long chat fit WITH them, round 2 (grown by tool results)
dropped them, so every earlier person turn's bytes changed mid-loop and the whole cached prefix
was re-billed — again on every later request of the same conversation (seen 2026-11-12 on two
requests 80 s apart, the same 15 turns each time).

After: once a conversation's wire had to lose them, every later send of that conversation drops
them before anything is measured, so two rounds send a byte-identical prefix.
"""

from __future__ import annotations

import asyncio
from copy import copy

import pytest

from matrx_ai.config import input_fit, send_boundary
from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.send_boundary import STAGE_LOOP, SendPrep, _fit_wire
from matrx_ai.config.typed_text_last import REPLAYED_TURN_KEY
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent

CONVERSATION = "7d3f7f0e-4c11-4f5e-9a3a-2b6f0c1d9e11"
PAGE = "<page>" + ("Warehouse dock schedule, week 46. " * 140) + "</page>"


def _user(text: str, *, replayed: bool = False) -> UnifiedMessage:
    message = UnifiedMessage(role=Role.USER, content=[TextContent(text=text)])
    if replayed:
        message.metadata = {REPLAYED_TURN_KEY: True}
    return message


def _history(tool_rounds: int) -> list[UnifiedMessage]:
    messages = [
        _user(PAGE, replayed=True),
        _user("Which trailers arrive Monday?"),
        UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Three: TR-40917, TR-40922, TR-41003.")]),
        _user(PAGE, replayed=True),
        _user("And Tuesday?"),
    ]
    for n in range(tool_rounds):
        messages.append(UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text=f"Checking the yard log ({n}).")]))
        messages.append(_user("Yard log row " * 400))
    return messages


def _wire_prep(tool_rounds: int) -> SendPrep:
    config = UnifiedConfig(model="claude-haiku-5-5", messages=MessageList(_messages=_history(tool_rounds)))
    prep = SendPrep(stage=STAGE_LOOP)
    wire = copy(config)
    wire.messages = MessageList(_messages=list(config.messages))
    prep.wire_config = wire
    return prep


def _wire_bytes(prep: SendPrep) -> list[str]:
    return [
        f"{m.role}:" + "".join(getattr(c, "text", "") for c in m.content)
        for m in prep.wire_config.messages
    ]


BUDGET_CHARS = 40_000


@pytest.fixture
def budget(monkeypatch):
    """A host budget measured in characters: what is on the wire, against one enforced limit."""

    async def limits(config):
        chars = sum(len(getattr(c, "text", "")) for m in config.messages for c in m.content)
        return [{"limit": "host_input_budget", "enforced": True, "limit_tokens": BUDGET_CHARS, "estimated_tokens": chars}]

    def over(found):
        return [lim for lim in found if lim["estimated_tokens"] > lim["limit_tokens"]]

    async def ensure_fits(config, **_):
        found = await limits(config)
        if not over(found):
            return {"fits": True, "limits": found}
        # The forced trim tiers free nothing here: only the replayed blocks can make it fit.
        return {"fits": False, "before": over(found), "passes": [{"pass": "forced_trim", "freed_chars": 0}]}

    monkeypatch.setattr(input_fit, "_limits", limits)
    monkeypatch.setattr(input_fit, "_over", over)
    monkeypatch.setattr(input_fit, "_enforced", lambda found: found)
    monkeypatch.setattr(input_fit, "ensure_fits", ensure_fits)
    send_boundary._REPLAYED_CONTEXT_DROPPED.clear()
    yield
    send_boundary._REPLAYED_CONTEXT_DROPPED.clear()


def _fit(prep: SendPrep, iteration: int) -> SendPrep:
    asyncio.run(_fit_wire(prep, None, policy=None, stage=STAGE_LOOP, conversation_id=CONVERSATION, iteration=iteration))
    return prep


def test_the_round_that_goes_over_drops_the_replayed_blocks(budget) -> None:
    prep = _fit(_wire_prep(tool_rounds=6), 1)
    assert not any(m.metadata.get(REPLAYED_TURN_KEY) for m in prep.wire_config.messages)
    assert prep.fit["fits"] is True


def test_two_rounds_after_a_drop_send_a_byte_identical_prefix(budget) -> None:
    # An earlier request of this conversation had to drop the replayed blocks.
    _fit(_wire_prep(tool_rounds=6), 1)

    # The next request: round 1 would fit WITH them; round 2, grown by a tool result, would not.
    round_1 = _fit(_wire_prep(tool_rounds=1), 1)
    round_2 = _fit(_wire_prep(tool_rounds=6), 2)

    first, second = _wire_bytes(round_1), _wire_bytes(round_2)
    assert second[: len(first)] == first, "an earlier message was rewritten between rounds of one loop"
    assert not any(m.metadata.get(REPLAYED_TURN_KEY) for m in round_1.wire_config.messages)
    assert round_1.fit["passes"][0] == {
        "pass": "drop_replayed_turn_context", "on": "wire", "messages_dropped": 2,
        "sticky": True, "unplaced_blocks": 2, "rewritten_blocks": [],
    }


def test_a_conversation_that_never_went_over_keeps_its_replayed_blocks(budget) -> None:
    prep = _fit(_wire_prep(tool_rounds=1), 1)
    assert sum(1 for m in prep.wire_config.messages if m.metadata.get(REPLAYED_TURN_KEY)) == 2
