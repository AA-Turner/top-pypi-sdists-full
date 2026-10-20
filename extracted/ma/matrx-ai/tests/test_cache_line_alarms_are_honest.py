"""The cache-line alarm is honest: one clock, one alarm per conversation, a row the queue can group.

Adversarial review I6 (2026-10-18): 309 ``frozen_prompt_differs_from_row`` captures in 72 h
and none was a real cache break. 297 came from ONE conversation in 48 minutes; the rest
diverged at the date digit. Cause: turn one rendered "Current date" from a naive host-local
``datetime.now()`` while later turns pin the conversation's UTC ``created_at`` date, so on any
non-UTC host the two disagree. The rows also left ``conversation_id`` null (payload only).

Each test failed on origin/main before the fix and passes after it.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from matrx_ai.instructions.core import SystemInstruction

CONV = "e67fa745-0000-4000-8000-000000000001"


class _LocalBehindUTC(datetime):
    """A host 7 h behind UTC, at 02:02 UTC on 10-18 (local 19:02 on 10-17)."""

    @classmethod
    def now(cls, tz=None):  # type: ignore[override]
        utc = datetime(2026, 10, 18, 2, 2, tzinfo=UTC)
        if tz is None:
            return datetime(2026, 10, 17, 19, 2)
        return utc.astimezone(tz)


def test_turn_one_renders_the_utc_date(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_ai.instructions.core as core

    monkeypatch.setattr(core, "datetime", _LocalBehindUTC)
    si = SystemInstruction(base_instruction="You help.")
    assert si.effective_date() == "2026-10-18", (
        "turn one used the host-local date; later turns pin the UTC created_at date"
    )


@pytest.mark.parametrize(
    "created",
    [
        datetime(2026, 10, 17, 19, 2, tzinfo=timezone(timedelta(hours=-7))),
        "2026-10-17T19:02:00-07:00",
        "2026-10-18T02:02:00Z",
        datetime(2026, 10, 18, 2, 2, tzinfo=UTC),
    ],
)
def test_later_turns_pin_the_same_utc_date(created: object) -> None:
    from matrx_ai.config.send_boundary import _pin_system_date

    si = SystemInstruction(base_instruction="You help.")
    _pin_system_date(SimpleNamespace(system_instruction=si), SimpleNamespace(created_at=created))
    assert si.date_anchor == "2026-10-18"


def test_one_alarm_per_conversation_with_the_conversation_on_the_row() -> None:
    from matrx_ai import _ext
    from matrx_ai.providers import cache_guard

    rows: list[dict] = []

    async def record_error(exc: BaseException, **fields: object) -> None:
        rows.append(fields)

    saved = dict(_ext._registry)
    _ext._registry["record_error"] = record_error

    async def run() -> None:
        for i in range(5):
            cache_guard.scream_cache_line_violation(
                kind="frozen_prompt_differs_from_row",
                conversation_id=CONV,
                request_id=None,
                prev_text="Current date: 2026-10-17\nYou help.",
                new_text=f"Current date: 2026-10-18\nYou help. {i}",
                where="test",
            )
        # A different conversation still alarms.
        cache_guard.scream_cache_line_violation(
            kind="frozen_prompt_differs_from_row",
            conversation_id="e67fa745-0000-4000-8000-000000000002",
            request_id=None,
            prev_text="a",
            new_text="b",
            where="test",
        )
        await asyncio.sleep(0.05)

    try:
        asyncio.run(run())
    finally:
        _ext._registry.clear()
        _ext._registry.update(saved)
    assert len(rows) == 2, f"expected one row per conversation, got {len(rows)}"
    assert rows[0].get("conversation_id") == CONV, "the row must carry conversation_id itself"
