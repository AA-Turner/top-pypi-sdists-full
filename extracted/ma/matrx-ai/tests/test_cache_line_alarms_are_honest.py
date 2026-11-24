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


def test_a_legacy_row_keeps_the_date_its_stored_prompt_names() -> None:
    """system_error 2026-11-02 (108 rows, first divergence at the date digit): a row stored
    before the one-UTC-clock rule names a host-local date one day off its UTC created_at.
    The pin must keep the stored date, so the frozen prompt renders byte for byte and the
    cache-line alarm stays quiet."""
    from matrx_ai.config.send_boundary import _enforce_frozen_prompt, _pin_system_date

    turn_one = SystemInstruction(base_instruction="You help.", date_anchor="2026-08-15")
    stored = str(turn_one)
    assert "2026-08-15" in stored
    si = SystemInstruction(base_instruction="You help.")
    config = SimpleNamespace(system_instruction=si, system_prompt_frozen=True)
    row = SimpleNamespace(
        created_at=datetime(2026, 8, 16, 17, 13, tzinfo=UTC), system_instruction=stored
    )
    _pin_system_date(config, row)
    assert si.date_anchor == "2026-08-15"
    config.resolved_system_instruction = str(si)

    from matrx_ai.providers import cache_guard

    screams: list[str] = []
    original = cache_guard.scream_cache_line_violation
    cache_guard.scream_cache_line_violation = lambda **kw: screams.append(kw["kind"])  # type: ignore[assignment]
    try:
        _enforce_frozen_prompt(config, row, conversation_id=CONV)
    finally:
        cache_guard.scream_cache_line_violation = original  # type: ignore[assignment]
    assert screams == [], "a legacy row's own date is not a cache-line violation"


def test_a_frozen_row_stored_without_a_date_reloads_without_one() -> None:
    """system_error 2026-10-31..11-03 (first divergence 0-1, +77 chars): turn one stored a
    prompt with no date block; the reload rebuilt it with include_date=True, so every later
    turn put a date in front of the cached prefix and screamed. The stored text is what turn
    one sent — the reload must render it byte for byte."""
    from matrx_ai.config.send_boundary import _enforce_frozen_prompt, _pin_system_date

    turn_one = SystemInstruction(base_instruction="You are a research analyst.", include_date=False)
    stored = str(turn_one)
    reloaded = SystemInstruction.from_value(stored)
    config = SimpleNamespace(system_instruction=reloaded, system_prompt_frozen=True)
    row = SimpleNamespace(
        created_at=datetime(2026, 11, 3, 0, 48, tzinfo=UTC), system_instruction=stored
    )
    _pin_system_date(config, row)
    config.resolved_system_instruction = str(reloaded)
    assert config.resolved_system_instruction == stored

    from matrx_ai.providers import cache_guard

    screams: list[str] = []
    original = cache_guard.scream_cache_line_violation
    cache_guard.scream_cache_line_violation = lambda **kw: screams.append(kw["kind"])  # type: ignore[assignment]
    try:
        _enforce_frozen_prompt(config, row, conversation_id=CONV)
    finally:
        cache_guard.scream_cache_line_violation = original  # type: ignore[assignment]
    assert screams == []


def test_an_unfrozen_conversation_still_gets_its_date() -> None:
    from matrx_ai.config.send_boundary import _pin_system_date

    si = SystemInstruction(base_instruction="You help.")
    config = SimpleNamespace(system_instruction=si, system_prompt_frozen=False)
    _pin_system_date(
        config,
        SimpleNamespace(created_at=datetime(2026, 11, 3, tzinfo=UTC), system_instruction="You help."),
    )
    assert si.include_date and si.date_anchor == "2026-11-03"
