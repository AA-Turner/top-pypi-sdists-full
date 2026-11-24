"""prompt_cache_prefix_drift, the sibling of ``test_a_stubbed_history_text_stays_stubbed.py``.

Before: the last fit pass (``input_fit.cut_largest_text_to_fit``, automated calls over an enforced
host budget) cut the rebuilt wire of every round from scratch, choosing its cut length from that
round's excess. A text cut on round 2 came back whole on round 3 (or cut to another length), so
every earlier turn's bytes moved and the whole cached prefix was written again.

After: every text a wire cut shortened is cut to the same length on every later send of the
conversation, before anything is measured; a deeper cut later starts from the kept head and equals
the same cut of the original. The real ``_fit_wire``, ``_cut_text_to_fit`` and the cut pass run;
only the measurement is a character count.
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

CONVERSATION = "9e4a2d71-0b3c-4f55-8a19-6c7d8e9f0a1b"
BUDGET_CHARS = 60_000
EXPORT = "".join(f"Shipment {n:05d}: dock 4, pallets 12, signed. " for n in range(1200))  # ~50k chars


def _canonical(newest: str) -> list[UnifiedMessage]:
    return [
        UnifiedMessage(role=Role.USER, content=[TextContent(text="Reconcile last month's shipments, please.")]),
        UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Reading the export.")]),
        UnifiedMessage(role=Role.USER, content=[TextContent(text=EXPORT)]),
        UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Checking the carrier log.")]),
        UnifiedMessage(role=Role.USER, content=[TextContent(text=newest)]),
    ]


def _round(ledger: list[UnifiedMessage], iteration: int) -> list[str]:
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

    async def ensure_fits(config, **_):
        found = await limits(config)
        over = [lim for lim in found if lim["estimated_tokens"] > lim["limit_tokens"]]
        if not over:
            return {"fits": True, "limits": found}
        # Every earlier pass frees nothing here: only the cut can make it fit.
        return {"fits": False, "before": over, "passes": [{"pass": "forced_trim", "freed_chars": 0}]}

    monkeypatch.setattr(input_fit, "_limits", limits)
    monkeypatch.setattr(input_fit, "ensure_fits", ensure_fits)
    for memo in (send_boundary._WIRE_TEXT_CUTS, send_boundary._WIRE_TEXT_STUBS, send_boundary._REPLAYED_CONTEXT_DROPPED):
        memo.clear()
    yield
    for memo in (send_boundary._WIRE_TEXT_CUTS, send_boundary._WIRE_TEXT_STUBS, send_boundary._REPLAYED_CONTEXT_DROPPED):
        memo.clear()


def test_two_rounds_send_a_byte_identical_prefix_after_a_cut(budget) -> None:
    round_2 = _round(_canonical("Carrier log row. " * 900), 2)  # ~65k: over, the export is cut
    assert "[Cut to fit this call:" in round_2[2], "the setup did not make the pass cut the export"

    # Round 3: the newest item (never part of the cached prefix) is small, so the wire would fit
    # with the export whole — the earlier turns must still send the bytes round 2 cached.
    round_3 = _round(_canonical("Carrier log: 3 rows."), 3)
    stable = len(round_2) - 1
    assert round_3[:stable] == round_2[:stable], "an earlier message was rewritten between rounds of one loop"


def test_a_deeper_cut_equals_the_same_cut_of_the_original() -> None:
    head = EXPORT[:30_000]
    once = head + input_fit.TEXT_CUT_MARKER.format(kept=30_000, total=len(EXPORT))
    assert input_fit.text_cut_key(once) == input_fit.text_cut_key(EXPORT)
    assert input_fit._cut_parts(once) == (head, len(EXPORT))


def test_a_conversation_that_never_went_over_keeps_every_text(budget) -> None:
    wire = _round(_canonical("Carrier log: 3 rows."), 1)
    assert "[Cut to fit this call:" not in "".join(wire)
