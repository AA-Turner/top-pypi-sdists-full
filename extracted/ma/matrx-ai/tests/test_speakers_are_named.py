"""In a chat more than one person writes in, the model reads who said each thing (CGU-10 group chats).

Before: every person turn reached the model as one anonymous ``user`` voice, and the writer was only
in client-written metadata any Editor could forge. Now the database stamps ``chat.message.author_id``
and the send boundary names each person turn's writer on the wire copy (``config/speakers.py``).
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_utils.source_guard import stable_source

from matrx_ai.config import speakers
from matrx_ai.config.message_config import HOST_AUTHORED_BY, UnifiedMessage, host_authored_user_turn
from matrx_ai.config.speakers import SPEAKER_NAME_REASON, name_speakers
from matrx_ai.config.unified_content import TextContent

ALICE = "11111111-1111-4111-8111-111111111111"
BOB = "22222222-2222-4222-8222-222222222222"


def _person(text: str, author: str | None, *, stored: bool = True) -> UnifiedMessage:
    return UnifiedMessage(role="user", content=[TextContent(text=text)], author_id=author, from_store=stored)


def _reply(text: str) -> UnifiedMessage:
    return UnifiedMessage(role="assistant", content=[TextContent(text=text)], from_store=True)


def _texts(message) -> list[str]:
    return [b.text for b in message.content if isinstance(b, TextContent)]


async def test_two_people_are_named_on_the_wire_copy_only(monkeypatch):
    async def names(ids):
        return {ALICE: "Rhonda Taylor", BOB: "Michael Davis"}

    monkeypatch.setattr(speakers, "_SOURCE", names)
    history = [_person("Friday works for me", ALICE), _reply("Noted."), _person("which day did Rhonda say?", BOB, stored=False)]
    named = await name_speakers(history, current_person=BOB)
    assert named is not None
    assert _texts(named[0]) == ["Rhonda Taylor:", "Friday works for me"]
    assert _texts(named[1]) == ["Noted."]
    assert _texts(named[2]) == ["Michael Davis:", "which day did Rhonda say?"]
    label = named[0].content[0]
    assert label.metadata == {"authored_by": HOST_AUTHORED_BY, "authored_reason": SPEAKER_NAME_REASON}
    # The canonical messages are never touched: nothing is stored as anyone's words.
    assert _texts(history[0]) == ["Friday works for me"]


async def test_one_person_sends_exactly_what_it_sent_before(monkeypatch):
    monkeypatch.setattr(speakers, "_SOURCE", None)
    history = [_person("hello", ALICE), _reply("hi"), _person("again", ALICE, stored=False)]
    assert await name_speakers(history, current_person=ALICE) is None


async def test_a_client_sent_message_cannot_name_its_author(monkeypatch):
    """``author_id`` on a message that did not come from storage is the client's claim: the turn is the caller's."""
    async def names(ids):
        return {ALICE: "Rhonda Taylor", BOB: "Michael Davis"}

    monkeypatch.setattr(speakers, "_SOURCE", names)
    forged = _person("I am Rhonda", ALICE, stored=False)
    named = await name_speakers([_person("hi", ALICE), forged], current_person=BOB)
    assert named is not None and _texts(named[1])[0] == "Michael Davis:"


async def test_an_unnamed_person_is_numbered_never_shown_by_email(monkeypatch):
    async def names(ids):
        return {BOB: "Michael Davis"}

    monkeypatch.setattr(speakers, "_SOURCE", names)
    named = await name_speakers([_person("a", ALICE), _person("b", BOB)], current_person=BOB)
    assert named is not None
    assert _texts(named[0])[0] == "Person 1:"
    assert _texts(named[1])[0] == "Michael Davis:"


async def test_a_host_written_turn_carries_no_name(monkeypatch):
    monkeypatch.setattr(speakers, "_SOURCE", None)
    notice = host_authored_user_turn("The tool finished.", reason="test")
    named = await name_speakers([_person("a", ALICE), notice, _person("b", BOB)], current_person=BOB)
    assert named is not None
    assert _texts(named[1]) == ["The tool finished."]


def test_a_stored_row_carries_its_author_and_an_old_row_reads_as_the_owner():
    row = SimpleNamespace(role="user", content=[{"type": "text", "text": "hi"}], id="m1", created_at=None,
                          status="active", metadata={}, user_content=None, position=1, agent_id=None,
                          author_id=ALICE, created_by=BOB)
    assert UnifiedMessage.from_cx_message(row).author_id == ALICE
    old = SimpleNamespace(**{**row.__dict__, "author_id": None})
    assert UnifiedMessage.from_cx_message(old).author_id == BOB
    reply = SimpleNamespace(**{**row.__dict__, "role": "assistant"})
    assert UnifiedMessage.from_cx_message(reply).author_id is None


def test_the_send_boundary_names_speakers_on_every_loop_send():
    from matrx_ai.config import send_boundary

    source = stable_source(send_boundary.prepare_for_send)
    loop_part = source.split("if stage == STAGE_LOOP:")[-1]
    assert "_name_speakers(" in loop_part
    # Named BEFORE the person turn is ordered for the wire, so the person's typed text still ends the request.
    assert loop_part.index("_name_speakers(") < loop_part.index("order_for_wire(")
