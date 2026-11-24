"""A date the assistant said in an earlier turn reaches the model marked STALE.

THE STATE BEFORE THIS TEST (measured live, Lane BC, 2026-10-03 04:01Z,
request f5e25a24-6982-4062-853f-0f8b5ecf00b8 on test@test.com's staff thread
6dbe2fa6). Asked "what's today's date?" on Friday, October 2 (PT), the Chief
answered "Monday, September 28, 2026." Its instructions that turn were live —
"Right now it is 9:01 PM on Friday, October 2" and "Today is Saturday, October
3" — but the history held its own answer to the same question on 09-28,
"Today's Monday, September 28, 2026.", unmarked, and the model copied it.

WHAT MUST HOLD. On a permanent thread every earlier assistant text that states a
date, weekday or clock time is noted ``[STALE — the reply to this message was said
at <its own time> …]`` — as a leading block on the PERSON's message it answered,
never in the assistant's own words (2026-11-06: the model echoed a marker placed
there; see test_the_model_never_sees_a_stale_note_in_its_own_voice.py). Current-turn
text and undated earlier text are untouched; the pass is idempotent and byte-stable.
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

    note = _text(messages[0])
    assert note.startswith(STALE_MARKER), note
    assert "said in an earlier turn" in note and "UTC" not in note
    assert messages[0].content[1].text == "what's today's date?"  # the person's words, unchanged, after the note
    assert _text(messages[1]) == OLD_ANSWER  # the assistant's own words are never marked
    assert report.dated_statements_marked == 1


def test_undated_text_and_the_current_turn_are_untouched() -> None:
    messages = _thread()
    mark_perishable_state(messages)
    assert _text(messages[3]) == "/home/agent"
    assert _text(messages[4]) == "what's today's date? just the day and date."
    assert messages[0].content[-1].text == "what's today's date?"  # the person's words are never changed
    assert len(messages[2].content) == 1  # an undated answer adds no note


def test_a_dated_answer_in_the_current_turn_is_this_turns_truth() -> None:
    messages = _thread() + [_say("assistant", "Friday, October 2.", "2026-10-03T04:01:15+00:00")]
    mark_perishable_state(messages)
    assert _text(messages[5]) == "Friday, October 2."


def test_idempotent_and_byte_stable() -> None:
    first = _thread()
    mark_perishable_state(first)
    once = [b.text for b in first[0].content]
    mark_perishable_state(first)
    assert [b.text for b in first[0].content] == once

    second = _thread()
    mark_perishable_state(second)
    assert [b.text for b in second[0].content] == once, "the stamp must come from the message, never from now"
