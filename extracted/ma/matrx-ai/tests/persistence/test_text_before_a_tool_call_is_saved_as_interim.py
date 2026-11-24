"""FORCING TEST — the text a model writes before it calls a tool is saved as INTERIM.

"Add a services section to the Home draft." written right before a tool call is a note between
steps, not the answer. The ONE chat.message write funnel marks such a text part ``interim: true``
(``matrx_ai.processing.blocks.interim_text``), the ``message_blocks`` event carries the same flag, and
every client draws it as a progress note. The rule, in one place:

* a text part a tool call follows IN THE SAME MESSAGE is interim;
* text a reply ends on before it parks on the person (``ask_person`` and its kin) is what the person
  reads to answer — never interim, even with another call between;
* a reply with no tool call, a user row, and a row saved before this existed carry no flag.

The flag is display data: it is never sent to a provider and never changes the text.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest

_ORG = "66666666-6666-4666-8666-666666666666"
_USER = "11111111-1111-4111-8111-111111111111"
_NOTE = "Add a services section to the Home draft."


def _text(text: str, **extra) -> dict:
    return {"type": "text", "text": text, **extra}


def _call(name: str = "apply_surface_write") -> dict:
    return {"type": "tool_call", "call_id": f"call_{uuid.uuid4().hex[:8]}", "name": name, "arguments": {}}


# --------------------------------------------------------------------------- the rule


# The cases are shared with the chat's live reading (tool-cards ``interimProse``): one file, both guards.
_CASES = json.loads((Path(__file__).parent / "interim_text_cases.json").read_text())["cases"]


@pytest.mark.parametrize(("content", "expected"), [(c["content"], c["expected"]) for c in _CASES], ids=[c["name"] for c in _CASES])
def test_the_rule(content: list[dict], expected: list[bool]) -> None:
    from matrx_ai.processing.blocks.interim_text import interim_flags

    flags = interim_flags(content)
    assert [flags[i] for i, p in enumerate(content) if p["type"] == "text"] == expected


def test_marking_sets_the_flag_only_where_true_and_drops_a_stale_one() -> None:
    from matrx_ai.processing.blocks.interim_text import mark_interim_text

    content = [_text(_NOTE), _call(), _text("Done.", interim=True)]
    marked = mark_interim_text(content)
    assert marked[0]["interim"] is True
    assert "interim" not in marked[2], "the flag is derived: text no call follows loses a stale one"
    assert "interim" not in content[0], "the caller's content is never mutated"
    assert marked[0]["text"] == _NOTE


def test_content_with_nothing_to_mark_is_returned_as_is() -> None:
    from matrx_ai.processing.blocks.interim_text import mark_interim_text

    plain = [_text("Here is the answer.")]
    assert mark_interim_text(plain) is plain
    already = [_text(_NOTE, interim=True), _call()]
    assert mark_interim_text(already) is already
    assert mark_interim_text("not a list") == "not a list"


# --------------------------------------------------------------------------- the save funnel


class _MessageMeta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "message"
    db_schema = "chat"


class _PackageMessage:
    _meta = _MessageMeta()


@pytest.fixture(params=[True, False], ids=["blocks-on", "blocks-off"])
def funnel(monkeypatch, request):
    from matrx_orm.session.coalesce import coalesce_ops

    from matrx_ai.persistence import queue_helpers
    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.registry import override_table
    from matrx_ai.processing.blocks import saved_blocks

    monkeypatch.setattr(
        queue_helpers,
        "_resolve_app_context",
        lambda: SimpleNamespace(organization_id=_ORG, request_id=str(uuid.uuid4()), user_id=_USER, conversation_id=None),
    )
    saved_blocks.configure_blocks_save(lambda: request.param)
    coord = Coordinator(request_id=str(uuid.uuid4()))
    token = queue_helpers._coordinator_cv.set(coord)
    stand_in = override_table("chat.message", _PackageMessage)
    stand_in.__enter__()

    def rows() -> dict[str, dict]:
        return {op.pk_value: (op.payload or {}) for op in coalesce_ops(list(coord._session._ops))}

    try:
        yield rows
    finally:
        stand_in.__exit__(None, None, None)
        queue_helpers._coordinator_cv.reset(token)
        coord._session._ops.clear()
        saved_blocks.configure_blocks_save(None)


def _texts(payload: dict) -> list[dict]:
    return [p for p in payload["content"] if p.get("type") == "text"]


def test_a_reply_that_calls_a_tool_lands_with_its_note_marked(funnel) -> None:
    """The main writer's shape: the row is reserved, then filled by a role-less UPDATE."""
    from matrx_ai.persistence.queue_helpers import queue_message_create, queue_message_update

    conv, reply = str(uuid.uuid4()), str(uuid.uuid4())
    queue_message_create(id=reply, conversation_id=conv, role="assistant", status="pending", content=[])
    queue_message_update(reply, status="active", content=[_text(_NOTE), _call()])
    (note,) = _texts(funnel()[reply])
    assert note.get("interim") is True
    assert note["text"] == _NOTE


def test_an_ordinary_answer_and_a_user_row_carry_no_flag(funnel) -> None:
    from matrx_ai.persistence.queue_helpers import queue_message_create

    conv, answer, asked = str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())
    queue_message_create(id=answer, conversation_id=conv, role="assistant", content=[_text("Here is the answer.")])
    # A user row is never marked, whatever it holds.
    queue_message_create(id=asked, conversation_id=conv, role="user", content=[_text(_NOTE), _call()])
    rows = funnel()
    assert all("interim" not in p for p in _texts(rows[answer]))
    assert all("interim" not in p for p in _texts(rows[asked]))


def test_the_stream_hears_the_flag_with_the_saved_part() -> None:
    from matrx_ai.processing.blocks.interim_text import mark_interim_text
    from matrx_ai.processing.blocks.saved_blocks import annotate_content, message_blocks_payload

    content = annotate_content(mark_interim_text([_text(_NOTE), _call(), _text("Done.")]))
    payload = message_blocks_payload(str(uuid.uuid4()), content)
    assert payload is not None
    note, done = payload.parts
    assert (note.text, note.interim) == (_NOTE, True)
    assert (done.text, done.interim) == ("Done.", False)
    wire = payload.model_dump(mode="json", exclude_defaults=True)
    assert wire["parts"][0]["interim"] is True
    assert "interim" not in wire["parts"][1], "an ordinary part's wire shape is what it was before the flag"


# --------------------------------------------------------------------------- the stored shape and the model


def test_the_stored_part_model_accepts_the_flag() -> None:
    from matrx_ai.db.message_parts import TextPart

    assert TextPart.model_validate({"type": "text", "text": _NOTE, "interim": True}).interim is True
    assert TextPart.model_validate({"type": "text", "text": _NOTE}).interim is None
    assert "interim" not in TextPart(text=_NOTE).model_dump(exclude_none=True)


@pytest.mark.parametrize("provider", ["anthropic", "openai", "google"])
def test_the_flag_never_reaches_a_provider_and_never_changes_the_text(provider: str) -> None:
    """A stored note is replayed to the model exactly as a row saved before the flag existed."""
    from matrx_ai.config.unified_content import reconstruct_content

    flagged = reconstruct_content({"type": "text", "text": _NOTE, "interim": True})
    plain = reconstruct_content({"type": "text", "text": _NOTE})
    assert flagged.text == plain.text == _NOTE
    sent = {
        "anthropic": lambda c: c.to_anthropic(),
        "openai": lambda c: c.to_openai(role="assistant"),
        "google": lambda c: c.to_google(),
    }[provider]
    assert sent(flagged) == sent(plain)
    assert "interim" not in repr(sent(flagged))


def test_a_malformed_tool_name_never_fails_the_rule() -> None:
    from matrx_ai.processing.blocks.interim_text import interim_flags

    assert interim_flags([_text(_NOTE), {"type": "tool_call", "name": ["not", "a", "name"]}]) == [True, False]
