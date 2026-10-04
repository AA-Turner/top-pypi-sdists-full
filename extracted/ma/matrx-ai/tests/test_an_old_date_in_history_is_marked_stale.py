"""A date the assistant said in an earlier turn reaches the model marked STALE.

THE STATE BEFORE THIS TEST (measured live, Lane BC, 2026-10-03 04:01Z,
request f5e25a24-6982-4062-853f-0f8b5ecf00b8 on test@test.com's staff thread
6dbe2fa6). Asked "what's today's date?" on Friday, October 2 (PT), the Chief
answered "Monday, September 28, 2026." Its instructions that turn were live —
"Right now it is 9:01 PM on Friday, October 2" and "Today is Saturday, October
3" — but the history held its own answer to the same question on 09-28,
"Today's Monday, September 28, 2026.", unmarked, and the model copied it.

WHAT MUST HOLD. On a permanent thread every earlier assistant text that states a
date, weekday or clock time is prefixed ``[STALE — said at <its own time> …]``;
current-turn text and undated earlier text are untouched; the pass is
idempotent and byte-stable.
"""

from __future__ import annotations

from matrx_ai.config import TextContent, UnifiedMessage
from matrx_ai.config.perishable_state import STALE_MARKER, mark_perishable_state

OLD_ANSWER = "Today's Monday, September 28, 2026."


def _say(role: str, text: str, at: str | None = None) -> UnifiedMessage:
    return UnifiedMessage(role=role, timestamp=at, content=[TextContent(text=text)])


def _thread() -> list[UnifiedMessage]:
    return [
        _say("user", "what's today's date?", "2026-09-28T22:59:00+00:00"),
        _say("assistant", OLD_ANSWER, "2026-09-28T22:59:15+00:00"),
        _say("user", "what's my home directory?", "2026-09-29T10:00:00+00:00"),
        _say("assistant", "/home/agent", "2026-09-29T10:00:09+00:00"),
        _say("user", "what's today's date? just the day and date.", "2026-10-03T04:01:03+00:00"),
    ]


def _text(message: UnifiedMessage) -> str:
    return message.content[0].text


def test_the_old_date_answer_is_marked_with_when_it_was_said() -> None:
    messages = _thread()
    report = mark_perishable_state(messages)

    marked = _text(messages[1])
    assert marked.startswith(STALE_MARKER), marked
    assert "said at 2026-09-28 22:59 UTC" in marked
    assert marked.endswith(OLD_ANSWER)
    assert report.dated_statements_marked == 1


def test_undated_text_and_the_current_turn_are_untouched() -> None:
    messages = _thread()
    mark_perishable_state(messages)
    assert _text(messages[3]) == "/home/agent"
    assert _text(messages[4]) == "what's today's date? just the day and date."
    assert _text(messages[0]) == "what's today's date?"  # the person's words are never marked


def test_a_dated_answer_in_the_current_turn_is_this_turns_truth() -> None:
    messages = _thread() + [_say("assistant", "Friday, October 2.", "2026-10-03T04:01:15+00:00")]
    mark_perishable_state(messages)
    assert _text(messages[5]) == "Friday, October 2."


def test_idempotent_and_byte_stable() -> None:
    first = _thread()
    mark_perishable_state(first)
    once = _text(first[1])
    mark_perishable_state(first)
    assert _text(first[1]) == once

    second = _thread()
    mark_perishable_state(second)
    assert _text(second[1]) == once, "the stamp must come from the message, never from now"
