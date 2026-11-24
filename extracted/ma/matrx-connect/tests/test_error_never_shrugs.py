"""An error's ``user_message`` holds only a sentence someone wrote for a person.

Every client prefers ``user_message`` over ``message`` (it is the field named "what the
person reads"). Two failures, one in each direction:

- 2026-09-12: ``user_message`` defaulted to an apology and SHADOWED the honest sentence a
  Masterwork upload wrote in ``message`` ("...isn't a kind of file we can read yet. Paste
  the text instead."). Closed at the callers: a refusal whose ``message`` is a person
  sentence passes the same sentence as ``user_message``.
- 2026-11-19 (Matrx Study): ``send_error`` built ``user_message=user_message or message``,
  so every ``fatal_error(message=...)`` without a person sentence handed exception text and
  Mandate refusal codes to people as if written for them.

So: no ``user_message`` (or a blank one) → the one generic person line, never ``message``.

How to prove these can fail: restore ``user_message=user_message or message`` in
``emitters/stream_emitter.py`` → the emitter test fails with the exception text as the
person's sentence; restore the old validator (blank → ``message``) in ``context/events.py``
→ the two payload tests fail the same way. Proven red 2026-11-19.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_connect.context.events import GENERIC_ERROR_MESSAGE, ErrorPayload
from matrx_connect.emitters.stream_emitter import StreamEmitter

RAW = "KeyError: 'rulebook_id'"
REAL_SENTENCE = (
    "“contract-review-checklist.txt” isn't a kind of file we can read yet. "
    "Paste the text instead."
)


def test_raw_message_never_becomes_the_persons_sentence() -> None:
    payload = ErrorPayload(error_type="boom", message=RAW)
    assert payload.user_message == GENERIC_ERROR_MESSAGE


def test_a_blank_user_message_is_the_generic_line_not_the_raw_message() -> None:
    payload = ErrorPayload(error_type="boom", message=RAW, user_message="   ")
    assert payload.user_message == GENERIC_ERROR_MESSAGE


def test_a_sentence_written_for_a_person_is_what_the_person_reads() -> None:
    payload = ErrorPayload(
        error_type="masterwork_source_unsupported", message=REAL_SENTENCE, user_message=REAL_SENTENCE
    )
    assert payload.user_message == REAL_SENTENCE


def test_an_explicit_user_message_still_wins() -> None:
    payload = ErrorPayload(
        error_type="boom",
        message=RAW,
        user_message="We lost track of that Rulebook. Open it again and retry.",
    )
    assert payload.user_message.startswith("We lost track")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("said", "reads"),
    [(None, GENERIC_ERROR_MESSAGE), ("", GENERIC_ERROR_MESSAGE), (REAL_SENTENCE, REAL_SENTENCE)],
)
async def test_the_emitter_sends_only_a_person_sentence(said: str | None, reads: str) -> None:
    emitter = StreamEmitter(heartbeat_interval=600)
    sent: list[Any] = []

    async def _capture(event: Any) -> None:
        sent.append(event)

    emitter._emit_event = _capture  # type: ignore[method-assign]
    await emitter.send_error("boom", RAW, said)
    data = sent[-1].data
    data = data.model_dump() if hasattr(data, "model_dump") else data
    assert data["message"] == RAW
    assert data["user_message"] == reads
