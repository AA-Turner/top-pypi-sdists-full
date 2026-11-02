"""A failure event never hides the reason behind an apology.

THE INCIDENT (2026-09-12, real). A Masterwork file upload failed with a real,
actionable sentence — *"'contract-review-checklist.txt' isn't a document type
we can read into pages yet. Paste the text instead."* — written by the server
into `ErrorPayload.message`. The person saw **"Sorry. An error occurred."**

Nothing swallowed it: `user_message` defaulted to that apology, and every
client prefers `user_message` (correctly — it is the field named "what the
person reads"), so the default SHADOWED the honest sentence on every surface in
the platform at once. The remedy — paste the text — never reached the one
person who could act on it.

## How to prove these can fail

Revert `_never_shrug` in `matrx_connect/context/events.py` (or restore
`user_message=user_message or "Sorry. An error occurred."` in
`emitters/stream_emitter.py`) → both of the first two tests fail with the
apology as the rendered sentence. Proven red 2026-09-12.
"""

from __future__ import annotations

from matrx_connect.context.events import GENERIC_ERROR_MESSAGE, ErrorPayload

REAL_SENTENCE = (
    "“contract-review-checklist.txt” isn't a kind of file we can read yet. "
    "Paste the text instead."
)


def test_the_servers_sentence_is_what_the_person_reads() -> None:
    payload = ErrorPayload(error_type="masterwork_source_unsupported", message=REAL_SENTENCE)
    assert payload.user_message == REAL_SENTENCE


def test_a_blank_user_message_does_not_become_the_apology() -> None:
    payload = ErrorPayload(
        error_type="masterwork_source_unsupported",
        message=REAL_SENTENCE,
        user_message="   ",
    )
    assert payload.user_message == REAL_SENTENCE


def test_an_explicit_user_message_still_wins() -> None:
    payload = ErrorPayload(
        error_type="boom",
        message="KeyError: 'rulebook_id'",
        user_message="We lost track of that Rulebook. Open it again and retry.",
    )
    assert payload.user_message.startswith("We lost track")


def test_the_apology_survives_only_when_the_server_said_nothing() -> None:
    payload = ErrorPayload(error_type="boom", message="")
    assert payload.user_message == GENERIC_ERROR_MESSAGE
