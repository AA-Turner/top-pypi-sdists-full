"""🚨 A STALE NOTE IS NEVER WRITTEN IN THE ASSISTANT'S OWN VOICE — the model copies its own turns.

THE STATE BEFORE THIS TEST (live, 2026-11-06 21:24 UTC, admin@admin.com's staff thread 3af9e95c, request
e486a36e). Asked "what time is it for me?" for the eighth time, the Chief answered
``[STALE — said at 2026-11-06 21:24 UTC, in an earlier turn. …]\\nIt's 1:24 PM on Friday …`` and that text was
stored as its reply. The send boundary had prefixed every earlier "It's 1:XX PM …" answer with the marker, so
every answer the model could see of its own opened with it, and it continued the pattern — stamping the time it
read in its instructions. No code wrote the marker onto the new reply: the marker runs only on messages before
the person's latest one, and the stamp is the turn's own clock.

WHAT MUST HOLD. After the boundary's pass no assistant message carries the marker, while the note that the
dated answer is old still reaches the model — on the person's message that answer replied to.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from matrx_ai.config import TextContent, UnifiedMessage
from matrx_ai.config.perishable_state import STALE_MARKER, mark_perishable_state


def _say(role: str, text: str, at: datetime) -> UnifiedMessage:
    return UnifiedMessage(role=role, timestamp=at.isoformat(), content=[TextContent(text=text)])


def _live_thread() -> list[UnifiedMessage]:
    start = datetime(2026, 11, 6, 21, 8, tzinfo=UTC)
    messages: list[UnifiedMessage] = []
    for i in range(7):
        at = start + timedelta(minutes=i)
        messages.append(_say("user", f"Probe {7730 + i} what time is it for me?", at))
        messages.append(
            _say(
                "assistant",
                f"It's 1:{8 + i:02d} PM on Friday, November 6, 2026, in Pacific time. "
                "I'm still assuming Pacific, so tell me your city if you're somewhere else.",
                at + timedelta(seconds=5),
            )
        )
    messages.append(_say("user", "Probe 7736 what time is it for me?", start + timedelta(minutes=16)))
    return messages


def _texts(message: UnifiedMessage) -> list[str]:
    return [b.text for b in message.content if isinstance(b, TextContent)]


def test_no_assistant_turn_opens_with_a_marker_the_model_could_continue() -> None:
    messages = _live_thread()
    report = mark_perishable_state(messages)

    own_voice = [t for m in messages if m.role == "assistant" for t in _texts(m) if STALE_MARKER in t]
    assert own_voice == [], f"the model would see its own answers open with a STALE note and copy it: {own_voice[0]!r}"
    assert report.dated_statements_marked == 7


def test_the_note_still_reaches_the_model_on_the_question_each_old_answer_replied_to() -> None:
    messages = _live_thread()
    mark_perishable_state(messages)

    for question, answer in zip(messages[0:-1:2], messages[1:-1:2], strict=True):
        note, words = _texts(question)
        assert note.startswith(STALE_MARKER) and "said in an earlier turn" in note, note
        assert words.startswith("Probe ")
        assert _texts(answer)[0].startswith("It's 1:")
    assert _texts(messages[-1]) == ["Probe 7736 what time is it for me?"]  # this turn's question is untouched
