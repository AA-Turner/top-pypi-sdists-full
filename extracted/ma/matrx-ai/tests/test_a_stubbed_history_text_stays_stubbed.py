"""prompt_cache_prefix_drift (system_error c3b2b223, 2026-11-17, chat 0fbc8c1f): "Wire prefix changed
between rounds of one provider loop: messages[0] (user) changed (143 -> 4,760 bytes); messages[16]
(user) changed (143 -> 5,061 bytes) ...".

Before: the wire is rebuilt from the canonical list on every round (the replayed page blocks and the
person's turns are fresh copies). Round 2 went over the host budget and the last-resort fit stubbed
earlier message texts on ITS wire only; round 3 fit without them, so those texts came back whole and
every earlier turn's bytes changed mid-loop — the whole cached prefix written again.

After: every history text a wire fit stubbed stays stubbed on every later send of the conversation,
before anything is measured, so two consecutive rounds send a byte-identical prefix. The real
``ensure_fits`` and ``_stub_history_to_fit`` run; only the limit measurement is a character count.
"""

from __future__ import annotations

import asyncio
from copy import copy, deepcopy

import pytest

from matrx_ai.config import input_fit, send_boundary
from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.send_boundary import STAGE_LOOP, SendPrep, _fit_wire
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent

CONVERSATION = "3c0b8f8e-5d2a-4b8e-9f61-1a2b3c4d5e6f"
BUDGET_CHARS = 30_000
OPENING = "Please set up our clinic: " + ("three locations, eleven providers, weekday hours. " * 150)


def _canonical(tool_rounds: int) -> list[UnifiedMessage]:
    messages = [
        UnifiedMessage(role=Role.USER, content=[TextContent(text=OPENING)]),
        UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Done: " + "location saved. " * 300)]),
        UnifiedMessage(role=Role.USER, content=[TextContent(text="Now the booking page, please.")]),
    ]
    for n in range(tool_rounds):
        messages.append(UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text=f"Working on step {n}.")]))
        messages.append(UnifiedMessage(role=Role.USER, content=[TextContent(text=f"Step {n} result row. " * 250)]))
    return messages


def _round(ledger: list[UnifiedMessage], iteration: int) -> list[str]:
    """One loop round: the wire is a fresh copy of the canonical list (as ``order_for_wire`` and the
    wire swaps build it), fitted by the real send-boundary step. Returns each wire message's bytes."""
    config = UnifiedConfig(model="claude-haiku-5-5", messages=MessageList(_messages=ledger))
    prep = SendPrep(stage=STAGE_LOOP)
    wire = copy(config)
    wire.messages = MessageList(_messages=deepcopy(list(config.messages)))
    prep.wire_config = wire
    asyncio.run(_fit_wire(prep, None, policy=None, stage=STAGE_LOOP, conversation_id=CONVERSATION, iteration=iteration))
    return [f"{m.role}:" + "".join(getattr(c, "text", "") for c in m.content) for m in prep.wire_config.messages]


@pytest.fixture
def budget(monkeypatch):
    async def limits(config):
        chars = sum(len(getattr(c, "text", "") or "") for m in config.messages for c in m.content)
        return [{"limit": "host_input_budget", "enforced": True, "limit_tokens": BUDGET_CHARS, "estimated_tokens": chars}]

    monkeypatch.setattr(input_fit, "_limits", limits)
    monkeypatch.setattr(send_boundary, "_forced_trim", lambda messages, policy: None)
    send_boundary._WIRE_TEXT_STUBS.clear()
    send_boundary._REPLAYED_CONTEXT_DROPPED.clear()
    yield
    send_boundary._WIRE_TEXT_STUBS.clear()
    send_boundary._REPLAYED_CONTEXT_DROPPED.clear()


def test_two_rounds_send_a_byte_identical_prefix_after_a_stub(budget) -> None:
    ledger = _canonical(tool_rounds=3)
    ledger[-1].content[0].text = "Big export row. " * 640  # round 2's newest result pushes it over
    round_2 = _round(ledger, 2)  # over the budget: earlier texts are stubbed on this wire only
    assert round_2[0] == f"{Role.USER}:{input_fit.STUB_TEXT}", "the setup did not make the fit stub history"
    assert ledger[0].content[0].text == OPENING, "a wire stub reached the canonical history"

    # Round 3: the newest item (never part of the cached prefix) is now small, so the wire would
    # fit WITHOUT the stubs — the earlier turns must still send the bytes round 2 cached.
    ledger[-1].content[0].text = "Big export row (summarised)."
    round_3 = _round(ledger, 3)
    assert round_3[0] == round_2[0]

    stable = len(round_2) - 1
    assert round_3[:stable] == round_2[:stable], "an earlier message was rewritten between rounds of one loop"


def test_the_newest_turn_is_never_restubbed(budget) -> None:
    ledger = _canonical(tool_rounds=6)
    _round(ledger, 2)
    # A new person turn repeating the opening words verbatim: her newest turn is never touched.
    ledger.append(UnifiedMessage(role=Role.USER, content=[TextContent(text=OPENING)]))
    wire = _round(ledger, 3)
    assert wire[-1] == f"{Role.USER}:{OPENING}"


def test_a_conversation_that_never_went_over_keeps_every_text(budget) -> None:
    ledger = _canonical(tool_rounds=1)
    wire = _round(ledger, 1)
    assert input_fit.STUB_TEXT not in "".join(wire)
