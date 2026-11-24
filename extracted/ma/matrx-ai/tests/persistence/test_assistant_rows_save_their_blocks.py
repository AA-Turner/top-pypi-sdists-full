"""FORCING TEST — an assistant row is saved with its text parts' blocks (PF-1 step 3).

Saved equals streamed: the server's one splitter reads every assistant text part into blocks in the
ONE chat.message write funnel (``queue_helpers._queue_or_drop``), after sealing and sanitizing. The
main writer reserves the row with a ``role`` INSERT and fills it with role-less UPDATEs (the
executor's mid-loop flush), so the funnel must annotate the UPDATE of a row it knows is assistant —
and never a user or tool row. A split that fails never fails the save. The switch is a host knob.
Lane: common-docs/systems/chat/projects/chat-ground-up/PF-1-saved-equals-streamed.md.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace

import pytest
from matrx_utils.source_guard import stable_source

_ORG = "66666666-6666-4666-8666-666666666666"
_USER = "11111111-1111-4111-8111-111111111111"
_REPLY = 'Here you go.\n\n```json\n{"__kind": "flashcard_set", "cards": []}\n```\n\nDone.'


class _MessageMeta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "message"
    db_schema = "chat"


class _PackageMessage:
    _meta = _MessageMeta()


@pytest.fixture
def funnel(monkeypatch):
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
    saved_blocks.configure_blocks_save(lambda: True)
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


def _text_part(payload: dict) -> dict:
    (part,) = [p for p in payload["content"] if p.get("type") == "text"]
    return part


def _has_blocks(part: dict) -> bool:
    from matrx_ai.processing.blocks.saved_blocks import has_current_blocks

    return has_current_blocks(part)


def test_the_reserved_reply_filled_by_a_roleless_update_lands_with_blocks(funnel) -> None:
    from matrx_ai.persistence.queue_helpers import queue_message_create, queue_message_update

    conv, reply = str(uuid.uuid4()), str(uuid.uuid4())
    queue_message_create(id=reply, conversation_id=conv, role="assistant", status="pending", content=[])
    queue_message_update(reply, status="active", content=[{"type": "text", "text": _REPLY}])
    part = _text_part(funnel()[reply])
    assert _has_blocks(part), part.keys()
    assert [b["type"] for b in part["blocks"]] == ["markdown", "kind", "markdown"]
    assert part["blocks"][1]["kind"] == "flashcard_set"


def test_persist_completed_request_shape_an_assistant_insert_lands_with_blocks(funnel) -> None:
    from matrx_ai.persistence.queue_helpers import queue_message_create

    conv, row = str(uuid.uuid4()), str(uuid.uuid4())
    queue_message_create(id=row, conversation_id=conv, role="assistant", content=[{"type": "text", "text": _REPLY}])
    assert _has_blocks(_text_part(funnel()[row]))


def test_an_update_of_a_row_this_process_never_inserted_is_an_assistant_writer(funnel) -> None:
    """Late stop and checkpoint repair update an assistant row inserted by an earlier request."""
    from matrx_ai.persistence.queue_helpers import queue_message_update

    row = str(uuid.uuid4())
    queue_message_update(row, content=[{"type": "text", "text": _REPLY}])
    assert _has_blocks(_text_part(funnel()[row]))


@pytest.mark.parametrize("role", ["user", "tool", "system"])
def test_other_rows_never_get_blocks(funnel, role) -> None:
    from matrx_ai.persistence.queue_helpers import queue_message_create, queue_message_update

    conv, row = str(uuid.uuid4()), str(uuid.uuid4())
    queue_message_create(id=row, conversation_id=conv, role=role, content=[{"type": "text", "text": _REPLY}])
    queue_message_update(row, content=[{"type": "text", "text": _REPLY + " more"}])
    assert "blocks" not in _text_part(funnel()[row])


def test_switch_off_saves_no_blocks(funnel) -> None:
    from matrx_ai.persistence.queue_helpers import queue_message_create
    from matrx_ai.processing.blocks import saved_blocks

    saved_blocks.configure_blocks_save(lambda: False)
    conv, row = str(uuid.uuid4()), str(uuid.uuid4())
    queue_message_create(id=row, conversation_id=conv, role="assistant", content=[{"type": "text", "text": _REPLY}])
    assert "blocks" not in _text_part(funnel()[row])


def test_a_switch_that_cannot_be_read_still_saves_blocks(funnel) -> None:
    """A script that never loaded the server's settings (its knob read raises) saved replies with no
    blocks on 2026-11-02; blocks are derived data, so an unreadable switch saves them, announced."""
    from matrx_ai.persistence.queue_helpers import queue_message_create
    from matrx_ai.processing.blocks import saved_blocks

    def _unprimed() -> bool:
        raise RuntimeError("feature knobs for 'platform.debug' were never loaded in this process")

    saved_blocks.configure_blocks_save(_unprimed)
    conv, row = str(uuid.uuid4()), str(uuid.uuid4())
    queue_message_create(id=row, conversation_id=conv, role="assistant", content=[{"type": "text", "text": _REPLY}])
    assert _text_part(funnel()[row]).get("blocks")


def test_a_failed_split_saves_the_row_without_blocks(funnel, monkeypatch) -> None:
    from matrx_ai.persistence.queue_helpers import queue_message_create
    from matrx_ai.processing.blocks import saved_blocks

    captured: list[BaseException] = []

    # Takes block_fields' whole keyword set (citations/stopped added in 4b44e6ffdfd).
    def boom(text, *, validate=None, contract=None, citations=None, stopped=False):
        raise RuntimeError("splitter exploded")

    monkeypatch.setattr(saved_blocks, "block_fields", boom)
    monkeypatch.setattr(saved_blocks, "_capture_split_failure", lambda exc, *, chars: captured.append(exc))
    conv, row = str(uuid.uuid4()), str(uuid.uuid4())
    queue_message_create(id=row, conversation_id=conv, role="assistant", content=[{"type": "text", "text": _REPLY}])
    part = _text_part(funnel()[row])
    assert part["text"] == _REPLY and "blocks" not in part
    assert captured and "exploded" in str(captured[0])


async def test_the_fingerprint_is_of_the_text_as_stored(funnel) -> None:
    """A NUL is replaced before storage; the fingerprint must describe the stored text."""
    from matrx_ai.persistence.queue_helpers import queue_message_create
    from matrx_ai.processing.blocks.saved_blocks import text_fingerprint

    conv, row = str(uuid.uuid4()), str(uuid.uuid4())
    queue_message_create(id=row, conversation_id=conv, role="assistant", content=[{"type": "text", "text": "a\x00b"}])
    part = _text_part(funnel()[row])
    assert "\x00" not in part["text"] and part["blocks_of"] == text_fingerprint(part["text"])


async def test_the_stream_hears_the_saved_blocks(funnel, monkeypatch) -> None:
    """Saved equals streamed: the request's emitter gets a message_blocks event with the saved parts."""
    import asyncio

    from matrx_ai.persistence import queue_helpers
    from matrx_ai.persistence.queue_helpers import queue_message_create, queue_message_update

    sent: list = []

    class _Emitter:
        async def send_data(self, payload):
            sent.append(payload)

    monkeypatch.setattr(
        queue_helpers,
        "_resolve_app_context",
        lambda: SimpleNamespace(organization_id=_ORG, request_id="r", user_id=_USER, conversation_id=None, emitter=_Emitter()),
    )
    conv, reply = str(uuid.uuid4()), str(uuid.uuid4())
    queue_message_create(id=reply, conversation_id=conv, role="assistant", status="pending", content=[])
    queue_message_update(reply, status="active", content=[{"type": "thinking", "text": "hm"}, {"type": "text", "text": _REPLY}])
    await asyncio.sleep(0)
    (event,) = sent
    assert event.type == "message_blocks" and event.message_id == reply
    (part,) = event.parts
    saved = _text_part(funnel()[reply])
    assert part.index == 1 and part.text == saved["text"] and part.blocks_of == saved["blocks_of"]
    assert [b.model_dump(exclude_none=True) for b in part.blocks] == [
        {k: v for k, v in b.items() if v is not None} for b in saved["blocks"]
    ]


async def test_every_model_call_warms_the_kind_registry_before_the_reply_is_saved(monkeypatch) -> None:
    """Found live 2026-11-01: kinds saved 'unchecked — kind registry not loaded' because only the
    old engine's stream path primed it. The one seam every model call crosses now warms it."""

    from matrx_ai.orchestrator import send_once
    from matrx_ai.processing.blocks import kind_catalog, saved_blocks

    primed: list[bool] = []

    async def prime() -> None:
        primed.append(True)

    monkeypatch.setattr(kind_catalog, "prime_registered_kinds", prime)
    saved_blocks.configure_blocks_save(lambda: True)
    try:
        await saved_blocks.warm_kind_registry()
    finally:
        saved_blocks.configure_blocks_save(None)
    assert primed == [True]
    source = stable_source(send_once)
    assert source.index("await warm_kind_registry()") < source.index("await finish_blocks_shadow(response)")


# ── PF-1 D3b: a structured run's reply saves as its contract's block ────────────────────────────

_JSON_REPLY = '\n{"title": "Cells", "cards": [{"front": "Q", "back": "A"}]}\n'
_FLASH = {
    "type": "object",
    "required": ["__kind", "title"],
    "properties": {"__kind": {"const": "flashcard_set"}, "title": {"type": "string"}, "cards": {"type": "array"}},
}


@pytest.fixture
def run_contract(monkeypatch):
    """Install a structured run's ExecutionState, with a warm registry knowing ``flashcard_set``."""
    from matrx_ai.orchestrator.execution_state import (
        ExecutionState,
        clear_execution_state,
        set_execution_state,
    )
    from matrx_ai.processing.blocks import saved_blocks
    from matrx_ai.processing.blocks.blocks_v1 import KindRegistryView, kind_validator

    registry = KindRegistryView(
        schema=lambda s: _FLASH if s == "flashcard_set" else None,
        version=lambda s: 3 if s == "flashcard_set" else None,
        known=lambda s: s == "flashcard_set",
        warm=lambda: True,
    )
    monkeypatch.setattr(saved_blocks, "kind_validator", lambda: kind_validator(registry))
    tokens = []

    def install(contract):
        tokens.append(set_execution_state(ExecutionState(reply_contract=contract)))

    yield install
    for t in reversed(tokens):
        clear_execution_state(t)


def _save(text: str, funnel) -> dict:
    from matrx_ai.persistence.queue_helpers import queue_message_create

    row = str(uuid.uuid4())
    queue_message_create(id=row, conversation_id=str(uuid.uuid4()), role="assistant", content=[{"type": "text", "text": text}])
    return _text_part(funnel()[row])


def _wire_valid(part: dict) -> None:
    from matrx_connect.context.reply_blocks import SavedTextPartBlocks

    SavedTextPartBlocks.model_validate({"index": 0, **{k: part[k] for k in ("text", "blocks_version", "blocks_of", "blocks")}})


def test_a_kind_bound_run_saves_one_validated_kind_block_with_its_marker(funnel, run_contract) -> None:
    from matrx_ai.processing.blocks.saved_blocks import ReplyContract

    run_contract(ReplyContract(kind="flashcard_set", schema_name="flashcards"))
    part = _save(_JSON_REPLY, funnel)
    assert part["text"] == _JSON_REPLY  # the model's words, byte for byte
    (block,) = part["blocks"]
    assert (block["type"], block["start"], block["end"]) == ("kind", 0, len(_JSON_REPLY.encode()))
    assert (block["kind"], block["kind_version"], block["status"]) == ("flashcard_set", 3, "valid")
    assert next(iter(block["value"])) == "__kind" and block["value"]["__kind"] == "flashcard_set"
    assert block["value"]["cards"] == [{"front": "Q", "back": "A"}]
    _wire_valid(part)


def test_an_invalid_answer_keeps_its_kind_block_with_the_errors(funnel, run_contract) -> None:
    from matrx_ai.processing.blocks.saved_blocks import ReplyContract

    run_contract(ReplyContract(kind="flashcard_set"))
    (block,) = _save('{"cards": []}', funnel)["blocks"]
    assert block["type"] == "kind" and block["status"] == "invalid" and block["errors"]


def test_a_schema_only_run_saves_one_data_block(funnel, run_contract) -> None:
    from matrx_ai.processing.blocks.saved_blocks import ReplyContract

    run_contract(ReplyContract(kind=None, schema_name="page_clean"))
    part = _save(_JSON_REPLY, funnel)
    assert part["text"] == _JSON_REPLY
    assert part["blocks"] == [
        {
            "type": "data",
            "start": 0,
            "end": len(_JSON_REPLY.encode()),
            "complete": True,
            "schema_name": "page_clean",
            "value": {"title": "Cells", "cards": [{"front": "Q", "back": "A"}]},
        }
    ]
    assert "__kind" not in part["blocks"][0]["value"]  # no kind is ever invented
    _wire_valid(part)


def test_a_marker_the_model_wrote_and_prose_keep_the_splitters_blocks(funnel, run_contract) -> None:
    from matrx_ai.processing.blocks.saved_blocks import ReplyContract

    run_contract(ReplyContract(kind="flashcard_set", schema_name="flashcards"))
    own = _save('{"__kind": "flashcard_set", "title": "T"}', funnel)["blocks"]
    assert [b["type"] for b in own] == ["kind"] and own[0]["value"] == {"__kind": "flashcard_set", "title": "T"}
    assert [b["type"] for b in _save("I could not find any cards.", funnel)["blocks"]] == ["markdown"]
    assert [b["type"] for b in _save(_REPLY, funnel)["blocks"]] == ["markdown", "kind", "markdown"]


def test_without_a_contract_whole_json_is_read_from_its_text_alone(funnel, run_contract) -> None:
    part = _save(_JSON_REPLY, funnel)
    assert [b["type"] for b in part["blocks"]] == ["markdown"]


def test_switch_off_saves_no_contract_blocks(funnel, run_contract) -> None:
    from matrx_ai.processing.blocks import saved_blocks
    from matrx_ai.processing.blocks.saved_blocks import ReplyContract

    run_contract(ReplyContract(kind="flashcard_set"))
    saved_blocks.configure_blocks_save(lambda: False)
    assert "blocks" not in _save(_JSON_REPLY, funnel)


def test_the_run_contract_comes_from_the_runs_schema_and_the_hosts_resolved_kind() -> None:
    from matrx_ai.orchestrator.executor import _reply_contract_for_run
    from matrx_ai.processing.blocks.saved_blocks import ReplyContract

    rf = {"type": "json_schema", "json_schema": {"name": "flashcards", "schema": {"type": "object", "properties": {}}}}
    request = SimpleNamespace(config=SimpleNamespace(response_format=rf))
    kinded = SimpleNamespace(metadata={"structured_output_content_ir": {"kind": "flashcard_set", "version": 3}})
    assert _reply_contract_for_run(request, kinded) == ReplyContract(kind="flashcard_set", schema_name="flashcards")
    assert _reply_contract_for_run(request, SimpleNamespace(metadata={})) == ReplyContract(None, "flashcards")
    generic = SimpleNamespace(metadata={"structured_output_content_ir": {"kind": "json"}})
    assert _reply_contract_for_run(request, generic) == ReplyContract(None, "flashcards")
    text_run = SimpleNamespace(config=SimpleNamespace(response_format=None))
    assert _reply_contract_for_run(text_run, SimpleNamespace(metadata={})) is None
