"""Block producers extracted from their injectors (prompt blocks / static seal P1a, PLAN §5.1).

A producer returns a block's TEXT and nothing else; where the text goes stays with today's
orchestration, which calls the producer in today's order. Each producer is named by its entry in
``matrx_ai.config.platform_parts.BLOCKS`` (``producer=``). Extraction is byte-identical, proven by
``tests/prompt_blocks/test_the_replay_set_is_byte_identical.py``.

Never-fail: a producer raises exactly where the code it came from raised, and its caller keeps the
same guard it had (``send_boundary._run_step`` announces and skips a failed step). A producer never
adds a failure path to a request.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


def produce_conversation_instructions(config: Any) -> str | None:
    """Block ``conversation_instructions``: the person's own instructions for this conversation.

    ``None`` when unset or blank (the block is absent)."""
    text = getattr(config, "conversation_instructions", None)
    if not isinstance(text, str) or not text.strip():
        return None
    return text


def produce_agent_modes(config: Any) -> str | None:
    """Block ``agent_modes``: the agent's modes, the conversation's current mode and its instructions.

    ``None`` when the agent has no modes (the block is absent). Text shape: ``config/agent_modes.py``."""
    from matrx_ai.config.agent_modes import render_block

    return render_block(
        getattr(config, "agent_modes", None),
        getattr(config, "agent_mode", None),
        getattr(config, "agent_mode_person_set", None),
    )


def produce_live_date(moment: datetime, *, zone: Any, pinned: str | None) -> str:
    """Block ``live_date``: the live instant, in the person's zone when known (``moment`` is UTC).

    Moved verbatim from ``send_boundary._announce_live_date``, which keeps the gate (a date-less
    prompt or no per-turn channel gets nothing) and the placement (slot ``live_date``)."""
    today = moment.strftime("%Y-%m-%d")
    # ALWAYS, not only when the pinned day is stale (Lane BC, 2026-10-03): a pin
    # that equals today IN UTC is still the wrong day for half the world for part
    # of every day — at 02:00Z it is yesterday evening in Los Angeles — so the
    # live instant travels on every turn and the person's own clock wins.
    began = (
        f'The "Current date: {pinned}" line in your instructions is the day this '
        f"conversation BEGAN, not today; never state it as the current date. "
        if pinned and pinned != today
        else ""
    )
    # 🚨 NO "Today is <UTC date>" HEADLINE (Lane BC, 2026-10-03 04:54Z): at 9:54 PM
    # Friday in Los Angeles the block opened "Today is Saturday, October 3" and the
    # Chief said Saturday, although its profile said Friday. The UTC date is named
    # only as the UTC reading of the instant, and the person's own date wins.
    if zone is not None:
        # The person's zone is known: ONE clock, theirs. No UTC time is shown, so none can compete.
        local = moment.astimezone(zone)
        hour = local.hour % 12 or 12
        return (
            f"The person's local time right now is {hour}:{local.minute:02d} {'AM' if local.hour < 12 else 'PM'} "
            f"on {local:%A}, {local:%B} {local.day}, {local.year} ({getattr(zone, 'key', str(zone))}). "
            f"That is the only clock to state to them; state exactly this date, day and time. {began}"
            f"Never state a date or time remembered from earlier in this conversation as the current one."
        )
    return (
        f"The current moment is {moment:%Y-%m-%dT%H:%MZ} (UTC). In UTC that falls on "
        f"{moment:%A}, {moment:%B} {moment.day}, {moment.year}, but the date and day "
        f"depend on the time zone. When your instructions give the person's own local "
        f"time, state THAT date, day and time to them, never the UTC ones. {began}"
        f"Never state a date or time remembered from earlier in this conversation as "
        f"the current one."
    )


__all__ = ["produce_conversation_instructions", "produce_live_date"]
