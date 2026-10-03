"""The date an agent states is always the live one — even on a thread that began days ago.

THE INCIDENT (Lane AZ2, 2026-09-28 22:59Z): test@test.com's permanent staff
thread ``6dbe2fa6`` was asked the time on Monday, September 28 and answered
"Saturday, September 26". The door had handed the Chief the correct instant
("4:09 PM on Monday, September 28, 2026" in its profile), but the system prefix
also said ``Current date: 2026-09-22``: ``_pin_system_date`` pins the date to
the conversation's ``created_at`` so the cached prefix is byte-stable, which is
right for one day and a lie on every day after. The thread's own history said
the 26th. Two stale dates against one live one, and the model picked a stale one.

Guards:
1. On every turn the resolve stage puts the live instant in the per-turn
   context channel; when the pinned date is not today it also names the pinned
   line as the day the conversation began. The cached prefix is untouched.
2. The per-turn context channel survives the loop step, so the live date (and
   every other per-turn block) reaches every provider call of the turn, not
   only the first.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from types import SimpleNamespace

from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.send_boundary import (
    LIVE_DATE_SLOT,
    STAGE_RESOLVE,
    _announce_live_date,
    prepare_for_send,
)
from matrx_ai.config.unified_config import UnifiedConfig, UnifiedResponse
from matrx_ai.config.unified_content import TextContent
from matrx_ai.orchestrator.requests import AIMatrixRequest

MONDAY_28 = datetime(2026, 9, 28, 22, 59, tzinfo=UTC)


def _staff_config(anchor: str | None) -> UnifiedConfig:
    config = UnifiedConfig(
        model="claude-sonnet-5",
        system_instruction="You are the person's Chief of Staff.",
        messages=MessageList([]),
    )
    if anchor:
        config.system_instruction.date_anchor = anchor
    config.messages.extend(
        [
            UnifiedMessage(
                role=Role.ASSISTANT,
                content=[TextContent(text="It's 12:38 AM PDT, Saturday, September 26, in LA.")],
            ),
            UnifiedMessage(role=Role.USER, content=[TextContent(text="what's today's date?")]),
        ]
    )
    return config


def _live_date_block(config: UnifiedConfig) -> str:
    return config.messages._turn_context_blocks.get(LIVE_DATE_SLOT, "")


def test_a_thread_that_began_days_ago_is_told_today() -> None:
    config = _staff_config("2026-09-22")
    prefix_before = str(config.system_instruction)

    _announce_live_date(config, now=MONDAY_28)

    block = _live_date_block(config)
    assert "Today is Monday, September 28, 2026" in block, block
    assert "2026-09-22" in block and "BEGAN" in block
    # The cached prefix is byte-identical: the fix costs no cache.
    assert str(config.system_instruction) == prefix_before
    # And the channel actually renders it for the provider.
    assert "Today is Monday, September 28, 2026" in (config.messages.render_turn_context() or "")


def test_a_thread_pinned_to_today_in_utc_is_still_told_the_live_instant() -> None:
    """Lane BC: at 02:00Z on Oct 3 the pin says 10-03 but Los Angeles is on Oct 2.

    Skipping the block when the pin equals the UTC date left the person's local
    date to chance for part of every day. The live instant travels every turn.
    """
    config = _staff_config("2026-10-03")
    _announce_live_date(config, now=datetime(2026, 10, 3, 2, 0, tzinfo=UTC))
    block = _live_date_block(config)
    assert "Today is Saturday, October 3, 2026 — 2026-10-03T02:00Z in UTC" in block, block
    assert "BEGAN" not in block
    assert "person's own local time" in block
    assert "remembered from earlier" in block


def test_the_resolve_stage_announces_the_live_date() -> None:
    """Wired into THE send boundary, not just defined beside it."""
    config = _staff_config(None)
    row = SimpleNamespace(created_at="2026-09-22T05:49:28+00:00", last_request_status=None)

    asyncio.run(
        prepare_for_send(
            config,
            stage=STAGE_RESOLVE,
            conversation_row=row,
            policy=TrimPolicy(),
        )
    )

    assert config.system_instruction.date_anchor == "2026-09-22"
    today = datetime.now(UTC)
    assert f"{today:%B} {today.day}, {today.year}" in _live_date_block(config)


def test_the_live_date_reaches_every_call_of_the_turn() -> None:
    config = _staff_config("2026-09-22")
    _announce_live_date(config, now=MONDAY_28)
    request = AIMatrixRequest(conversation_id="6dbe2fa6", config=config, request_id="r-1")

    after_tool_round = AIMatrixRequest.add_response(
        request,
        UnifiedResponse(
            messages=[UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="…")])]
        ),
    )

    assert "Today is Monday, September 28, 2026" in _live_date_block(after_tool_round.config), (
        "the per-turn context channel was dropped by the loop step — the second provider "
        "call of the turn no longer knows what day it is"
    )
