"""P1a: the ``live_date`` block's text, extracted from ``send_boundary._announce_live_date`` into
``prompt_block_producers.produce_live_date``, is byte-identical to the injector it came from.

The golden (``golden/live_date.json``) was written through ``_announce_live_date`` BEFORE extraction,
over the clock cases that matter: zone known / unknown, pinned date equal / stale / absent, AM / PM,
midnight UTC. Regenerate only for a change meant to move bytes: ``PROMPT_BLOCKS_REGEN_GOLDEN=1``.
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.send_boundary import LIVE_DATE_SLOT, _announce_live_date
from matrx_ai.instructions.core import SystemInstruction

GOLDEN = Path(__file__).with_name("golden") / "live_date.json"
MOMENTS = {
    "monday_am": datetime(2026, 9, 28, 9, 5, tzinfo=UTC),
    "utc_2am": datetime(2026, 10, 3, 2, 0, tzinfo=UTC),
    "friday_pm_la": datetime(2026, 10, 3, 4, 54, tzinfo=UTC),
    "midnight": datetime(2026, 11, 13, 0, 0, tzinfo=UTC),
}
ZONES = {"none": None, "la": ZoneInfo("America/Los_Angeles"), "tokyo": ZoneInfo("Asia/Tokyo")}
PINS = {"same": "today", "stale": "2026-09-22", "absent": None}
CASES = [(m, z, p) for m in MOMENTS for z in ZONES for p in PINS]
#: The day the golden was written. With no pinned anchor, ``SystemInstruction`` pins the real UTC
#: today, so the "absent" cases are frozen to this day — otherwise the golden goes red at midnight.
GOLDEN_WRITTEN = datetime(2026, 11, 13, 12, 0, tzinfo=UTC)


class _FrozenDatetime(datetime):
    @classmethod
    def now(cls, tz=None):  # type: ignore[override]
        return GOLDEN_WRITTEN if tz is None else GOLDEN_WRITTEN.astimezone(tz)


@pytest.fixture(autouse=True)
def _freeze_the_pinned_today(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_ai.instructions.core as core

    monkeypatch.setattr(core, "datetime", _FrozenDatetime)


def _text(moment_key: str, zone_key: str, pin_key: str) -> str:
    moment = MOMENTS[moment_key]
    pin = PINS[pin_key]
    anchor = moment.strftime("%Y-%m-%d") if pin == "today" else pin
    si = SystemInstruction(base_instruction="X", include_date=True, date_anchor=anchor)
    config = UnifiedConfig(
        model="m",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]
        ),
    )
    config.system_instruction = si
    _announce_live_date(config, now=moment, zone=ZONES[zone_key])
    return config.messages.turn_context_blocks()[LIVE_DATE_SLOT]


@pytest.mark.parametrize(("moment", "zone", "pin"), CASES)
def test_live_date_text_matches_the_golden(moment: str, zone: str, pin: str) -> None:
    key = f"{moment}/{zone}/{pin}"
    text = _text(moment, zone, pin)
    if os.environ.get("PROMPT_BLOCKS_REGEN_GOLDEN") == "1":
        golden = json.loads(GOLDEN.read_text()) if GOLDEN.exists() else {}
        golden[key] = text
        GOLDEN.write_text(
            json.dumps(dict(sorted(golden.items())), indent=1, ensure_ascii=False) + "\n"
        )
        return
    assert text == json.loads(GOLDEN.read_text())[key], key
