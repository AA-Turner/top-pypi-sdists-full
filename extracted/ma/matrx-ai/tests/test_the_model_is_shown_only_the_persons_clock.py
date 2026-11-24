"""One clock reaches the model: the person's. Never a UTC time beside it.

2026-11-06, admin@admin.com's staff thread 3af9e95c: the Chief answered the time in UTC on some turns and
Pacific on others. Every earlier-turn note carried a ``... UTC`` stamp and the per-turn live-date block stated
the UTC instant, so the model had many UTC times and one local one. Red before: the notes contained "UTC" and the
live-date block named the UTC instant even when the host knew the person's zone.
"""

from __future__ import annotations

from datetime import UTC, datetime

from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.perishable_state import mark_perishable_state
from matrx_ai.config.send_boundary import LIVE_DATE_SLOT, _announce_live_date
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent


def _config() -> UnifiedConfig:
    config = UnifiedConfig(
        model="claude-sonnet-5", system_instruction="Chief of Staff.", messages=MessageList([])
    )
    config.messages.extend([UnifiedMessage(role=Role.USER, content=[TextContent(text="what's the date?")])])
    return config


def test_live_date_block_is_in_the_persons_zone_with_no_utc_time() -> None:
    from zoneinfo import ZoneInfo

    config = _config()
    _announce_live_date(
        config, now=datetime(2026, 11, 6, 21, 24, tzinfo=UTC), zone=ZoneInfo("America/Los_Angeles")
    )
    block = config.messages._turn_context_blocks[LIVE_DATE_SLOT]
    assert "1:24 PM on Friday, November 6, 2026 (America/Los_Angeles)" in block, block
    assert "UTC" not in block and "21:24" not in block, block


def test_live_date_block_reads_the_zone_the_host_carried(monkeypatch) -> None:
    from types import SimpleNamespace

    import matrx_ai.context.app_context as app_context

    monkeypatch.setattr(
        app_context, "try_get_app_context", lambda: SimpleNamespace(metadata={"person_timezone": "America/New_York"})
    )
    config = _config()
    _announce_live_date(config, now=datetime(2026, 11, 6, 21, 24, tzinfo=UTC))
    block = config.messages._turn_context_blocks[LIVE_DATE_SLOT]
    assert "4:24 PM on Friday, November 6, 2026 (America/New_York)" in block, block


def test_stale_notes_carry_no_utc_stamp() -> None:
    at = datetime(2026, 11, 6, 21, 8, tzinfo=UTC).isoformat()
    messages = [
        UnifiedMessage(role=Role.USER, timestamp=at, content=[TextContent(text="time?")]),
        UnifiedMessage(role=Role.ASSISTANT, timestamp=at, content=[TextContent(text="It's 1:08 PM on Friday.")]),
        UnifiedMessage(role=Role.USER, timestamp=at, content=[TextContent(text="again?")]),
    ]
    mark_perishable_state(messages)
    assert "UTC" not in messages[0].content[0].text, messages[0].content[0].text
