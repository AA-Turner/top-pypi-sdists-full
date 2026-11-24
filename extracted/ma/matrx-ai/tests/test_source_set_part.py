"""A turn's attachments as ONE ``source_set`` part (One Source contract, P0 §4 item 4).

The stored message must hold the set so read-back and edit-resend can show and resend
it; stored ``input_*`` parts stay readable beside it (one deserializer, no migration);
resolution is the host's, through the ``source_set_resolver`` seam, and an unbound
seam is LOUD — the turn refuses rather than answering without its attachments.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from pydantic import TypeAdapter, ValidationError

from matrx_ai import _ext
from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.structured_input_config import (
    SOURCE_SET_MEDIA_MARKER,
    NotesInputContent,
    SourceSetInputContent,
)
from matrx_ai.config.structured_input_resolver import resolve_structured_inputs
from matrx_ai.db.message_parts import UserInputPart, validate_message_content

NOTE_ID = "c208c61b-0cc2-4b78-a8f4-f19d29604795"
FILE_ID = "5b0c7a1e-2f61-4d3b-9a0e-3c8f1d2e4a77"
USER_ID = "87a6e699-3622-4869-8843-d0867456c0dd"
IMAGE_URL = "https://example.com/gate-3.png"


def _part(**source_set_extra) -> dict:
    return {
        "type": "source_set",
        "source_set": {
            "envelope": "source_set",
            "version": 1,
            "sources": [
                {
                    "envelope": "resource_ref",
                    "resource_type": "note",
                    "resource_id": NOTE_ID,
                    "label": "Gate plan",
                    "part": {"scope": "page", "page": 2},
                },
                {"envelope": "resource_ref", "resource_type": "file", "resource_id": FILE_ID},
            ],
            **source_set_extra,
        },
    }


@pytest.fixture
def signed_in(monkeypatch):
    from matrx_connect.context import app_context

    ctx = SimpleNamespace(user_id=USER_ID, metadata={})
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: ctx)
    return ctx


@pytest.fixture
def resolver(monkeypatch, signed_in):
    calls: list[tuple[dict, str | None]] = []

    async def resolve(source_set, *, user_id):
        calls.append((source_set, user_id))
        return {
            "text": "<source name=\"Gate plan\">north apron</source>",
            "media": [{"type": "media", "kind": "image", "url": IMAGE_URL}],
            "dropped": [],
        }

    monkeypatch.setitem(_ext._registry, _ext._SOURCE_SET_RESOLVER_KEY, resolve)
    return calls


# --- persistence round trip -------------------------------------------------


def test_a_source_set_part_round_trips_through_persistence():
    stored = validate_message_content([_part(topic="gates")])
    assert len(stored) == 1
    part = stored[0]
    assert part["type"] == "source_set"
    assert part["source_set"]["envelope"] == "source_set"
    assert part["source_set"]["topic"] == "gates"
    assert part["source_set"]["sources"][0]["part"] == {"scope": "page", "page": 2}
    assert part["source_set"]["sources"][0]["envelope"] == "resource_ref"

    # Read back through the ONE deserializer and stored again: identical.
    message = UnifiedMessage.from_dict({"role": "user", "content": stored})
    assert isinstance(message.content[0], SourceSetInputContent)
    again = validate_message_content(message.to_storage_dict()["content"])
    assert again == stored


def test_the_old_kind_spelling_is_read_and_stored_as_envelope():
    part = _part()
    part["source_set"]["__kind"] = part["source_set"].pop("envelope")
    stored = validate_message_content([part])
    assert stored[0]["source_set"]["envelope"] == "source_set"
    assert "__kind" not in stored[0]["source_set"]


def test_the_request_door_accepts_a_source_set_part():
    out = TypeAdapter(UserInputPart).validate_python(_part())
    assert out["type"] == "source_set"
    assert out["source_set"]["sources"][1]["resource_id"] == FILE_ID


# --- refusals ---------------------------------------------------------------


@pytest.mark.parametrize(
    "mutate",
    [
        lambda p: p["source_set"]["sources"][0].update(resource_id="not-a-uuid"),
        lambda p: p["source_set"]["sources"][0].update(part={"scope": "page", "page": 0}),
        lambda p: p["source_set"]["sources"][0].update(delivery="sideways"),
        lambda p: p["source_set"].update(version=2),
        lambda p: p.update(stray="field"),
        lambda p: p.pop("source_set"),
    ],
    ids=["bad-uuid", "page-zero", "bad-delivery", "version-2", "extra-part-key", "no-set"],
)
def test_an_invalid_source_set_part_is_refused(mutate):
    part = _part()
    mutate(part)
    with pytest.raises(ValueError):
        validate_message_content([part])
    with pytest.raises(ValidationError):
        TypeAdapter(UserInputPart).validate_python(part)


def test_an_unknown_part_type_is_refused():
    with pytest.raises(ValueError, match="unknown part type 'source_sets'"):
        validate_message_content([{"type": "source_sets", "source_set": {}}])


def test_an_invalid_set_never_becomes_a_content_block():
    with pytest.raises(ValidationError):
        SourceSetInputContent(source_set={"sources": [{"resource_type": "note", "resource_id": "x"}]})


# --- stored input_* parts stay readable --------------------------------------


def test_a_stored_input_part_still_parses():
    stored_row = {
        "type": "input_notes",
        "note_ids": [NOTE_ID],
        "template": "full",
        "convert_to_text": True,
        "optional_context": False,
        "keep_fresh": False,
        "metadata": {"resolved_text": "north apron"},
    }
    assert validate_message_content([stored_row])[0]["note_ids"] == [NOTE_ID]
    message = UnifiedMessage.from_dict({"role": "user", "content": [stored_row]})
    assert isinstance(message.content[0], NotesInputContent)
    assert message.content[0].get_output() == "north apron"


# --- the resolver seam -------------------------------------------------------


def test_the_seam_announces_when_unbound(monkeypatch, signed_in):
    monkeypatch.delitem(_ext._registry, _ext._SOURCE_SET_RESOLVER_KEY, raising=False)
    messages = MessageList([UnifiedMessage.from_dict({"role": "user", "content": [_part()]})])
    with pytest.raises(
        _ext.SourceSetResolverUnavailable,
        match="a source_set part reached a host with no resolver",
    ):
        asyncio.run(resolve_structured_inputs(messages))


def test_a_bound_seam_resolves_text_and_media_and_storage_keeps_only_the_set(resolver):
    message = UnifiedMessage.from_dict(
        {"role": "user", "content": [{"type": "text", "text": "Compare these"}, _part()]}
    )
    messages = MessageList([message])
    asyncio.run(resolve_structured_inputs(messages))

    (sent_set, sent_user), = resolver
    assert sent_user == USER_ID
    assert sent_set["envelope"] == "source_set"
    assert sent_set["sources"][0]["resource_id"] == NOTE_ID

    last = messages.get_last_by_role(Role.USER)
    block = last.content[1]
    assert isinstance(block, SourceSetInputContent)
    assert block.get_output().endswith("north apron</source>")
    media = last.content[2]
    assert media.metadata[SOURCE_SET_MEDIA_MARKER] is True

    # The provider request carries the text AND the media.
    blocks = last.to_anthropic_blocks()
    assert any(b.get("type") == "text" and "north apron" in b.get("text", "") for b in blocks)
    assert any(b.get("type") == "image" for b in blocks)

    # Storage holds the set (with what it resolved to), never the spliced media.
    stored = validate_message_content(last.to_storage_dict()["content"])
    assert [p["type"] for p in stored] == ["text", "source_set"]
    assert stored[1]["metadata"]["resolved_media"][0]["url"] == IMAGE_URL

    # Read-back re-splices the media once; a reloaded turn is not re-resolved.
    reloaded = UnifiedMessage.from_dict({"role": "user", "content": stored})
    kinds = [type(c).__name__ for c in reloaded.content]
    assert kinds == ["TextContent", "SourceSetInputContent", "ImageContent"]
    asyncio.run(resolve_structured_inputs(MessageList([reloaded])))
    assert len(resolver) == 1
    assert [type(c).__name__ for c in reloaded.content] == kinds
