"""THE DURABLE ROW CARRIES NO DECLARED CONTROL LINE.

The streaming emitter strips a declared machine line (``WRAP_RATING: 4``) out of
the text a person sees and re-emits it as a structured event. The ``cx_message``
row is written from the PROVIDER RESPONSE instead — so before
``matrx_ai/db/control_tokens.py`` existed, the person saw clean prose while the
stored assistant message kept the token, and every later reader (a rebuild sent
back to the provider, a transcript, an export) got the raw line back.

Forcing function, not decoration: every assertion here reads what the REAL
persistence seams queued for the row — ``_flush_assistant_message_mid_loop``,
``persist_completed_request``, and the native runner's ``append_turn``. Delete
any call to ``clean_assistant_content`` and these fail; store the value nowhere
and they fail.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

import pytest
from aidream.services.ai_execution.ai_task_blocks import BlockStreamingEmitter
from aidream.services.runtime.workflow_events import EventRecordingEmitter
from matrx_connect.emitters.control_tokens import (
    CONTROL_TOKEN_REGISTRY,
    ControlTokenRegistry,
    ControlTokenSpec,
)

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.db.control_tokens import (
    CONTROL_TOKEN_METADATA_KEY,
    clean_assistant_content,
    merge_control_token_metadata,
)
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

CONVERSATION_ID = "11111111-1111-1111-1111-111111111111"
USER_ID = "22222222-2222-2222-2222-222222222222"
REQUEST_ID = "33333333-3333-3333-3333-333333333333"

#: Byte-identical to aidream's own declaration
#: (``aidream/services/mandates/control_token_declarations.py``) so registering
#: it is a no-op when the host's declarations are already loaded in the process.
WRAP_RATING = ControlTokenSpec(
    name="WRAP_RATING",
    declared_by="vision_interview room primary role (DB system prompt)",
    purpose="the primary voice's 1-5 self-rating of how ready this stage is to wrap",
    value_pattern=r"[1-5]",
)


@pytest.fixture()
def declared(monkeypatch):
    """WRAP_RATING declared on the CANONICAL registry, restored afterwards.

    The persistence seams read the one global registry (that is the point — one
    registry, two seams), so the guard declares into it rather than threading a
    private one through production code.
    """
    saved = dict(CONTROL_TOKEN_REGISTRY._specs)
    CONTROL_TOKEN_REGISTRY.register(WRAP_RATING)
    yield WRAP_RATING
    CONTROL_TOKEN_REGISTRY._specs.clear()
    CONTROL_TOKEN_REGISTRY._specs.update(saved)


# ---------------------------------------------------------------------------
# The seam itself
# ---------------------------------------------------------------------------


def _registry() -> ControlTokenRegistry:
    reg = ControlTokenRegistry()
    reg.register(WRAP_RATING)
    return reg


def test_declared_line_leaves_the_text_and_becomes_a_hit():
    blocks = [{"type": "text", "text": "That lands well.\nWRAP_RATING: 4\n"}]
    cleaned, hits = clean_assistant_content(blocks, registry=_registry())
    assert cleaned == [{"type": "text", "text": "That lands well.\n"}]
    assert [(h.name, h.value) for h in hits] == [("WRAP_RATING", "4")]
    assert hits[0].declared_by == WRAP_RATING.declared_by


def test_ordinary_prose_is_returned_untouched_and_unallocated():
    blocks = [{"type": "text", "text": "No machine lines here at all."}]
    cleaned, hits = clean_assistant_content(blocks, registry=_registry())
    assert cleaned is blocks
    assert hits == ()


def test_a_block_that_was_only_the_control_line_is_dropped():
    blocks = [
        {"type": "text", "text": "the answer"},
        {"type": "text", "text": "WRAP_RATING: 5"},
    ]
    cleaned, hits = clean_assistant_content(blocks, registry=_registry())
    # An empty text block is refused by providers when the conversation is
    # rebuilt and sent back — a leak must never be traded for a 400.
    assert cleaned == [{"type": "text", "text": "the answer"}]
    assert hits[0].value == "5"


def test_non_text_blocks_are_never_inspected():
    blocks = [{"type": "tool_use", "id": "toolu_a", "input": {"q": "WRAP_RATING: 4"}}]
    cleaned, hits = clean_assistant_content(blocks, registry=_registry())
    assert cleaned is blocks
    assert hits == ()


def test_metadata_carries_the_stream_event_shape_and_is_idempotent():
    _, hits = clean_assistant_content(
        [{"type": "text", "text": "x\nWRAP_RATING: 3\n"}], registry=_registry()
    )
    meta = merge_control_token_metadata({"provider_iteration": 1}, hits)
    assert meta[CONTROL_TOKEN_METADATA_KEY] == [
        {"name": "WRAP_RATING", "value": "3", "declared_by": WRAP_RATING.declared_by}
    ]
    assert meta["provider_iteration"] == 1
    assert merge_control_token_metadata(meta, hits) == meta


# ---------------------------------------------------------------------------
# Seam 1 — the mid-loop durability checkpoint
# ---------------------------------------------------------------------------


class _StubEmitter:
    async def send_record_reserved(self, *a, **k):
        return None


class _StubTracker:
    async def reserve(self, *a, **k):
        return None

    async def mark_active(self, *a, **k):
        return None


class _ExecCtx:
    conversation_id = CONVERSATION_ID
    user_id = USER_ID
    store = True
    system_run = False
    emitter = _StubEmitter()


def _request(*messages: UnifiedMessage) -> AIMatrixRequest:
    return AIMatrixRequest(
        conversation_id=CONVERSATION_ID,
        config=UnifiedConfig(model="claude-test", messages=MessageList(_messages=list(messages))),
        request_id=REQUEST_ID,
    )


@pytest.mark.asyncio
async def test_mid_loop_flush_stores_clean_text_and_the_value(monkeypatch, declared):
    import matrx_ai.persistence.queue_helpers as qh

    updates: list[tuple[str, dict[str, Any]]] = []
    monkeypatch.setattr(
        qh, "queue_message_update", lambda mid, **kw: updates.append((mid, kw)) or ""
    )
    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: "")
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _StubTracker())

    request = _request(UnifiedMessage(role="user", content=[TextContent(text="go")]))
    reserved_id = str(uuid4())
    position = len(request.config.messages.to_list())

    await executor_mod._flush_assistant_message_mid_loop(
        response=UnifiedResponse(
            messages=[
                UnifiedMessage(
                    role="assistant",
                    content=[TextContent(text="Here is the shape.\nWRAP_RATING: 4\n")],
                )
            ]
        ),
        current_request=request,
        exec_ctx=_ExecCtx(),
        reserved_messages={position: reserved_id},
        parent_refs={},
    )

    assert len(updates) == 1
    _mid, fields = updates[0]
    stored = "".join(b.get("text", "") for b in fields["content"] if b.get("type") == "text")
    assert "WRAP_RATING" not in stored
    assert stored.startswith("Here is the shape.")
    assert fields["metadata"][CONTROL_TOKEN_METADATA_KEY] == [
        {"name": "WRAP_RATING", "value": "4", "declared_by": WRAP_RATING.declared_by}
    ]


# ---------------------------------------------------------------------------
# Seam 2 — the end-of-loop persist (the row every mandate gets)
# ---------------------------------------------------------------------------


class _StubModelManager:
    async def load_model_get_string_uuid(self, name):
        return "44444444-4444-4444-4444-444444444444"


class _StubCoordinator:
    def queue(self, *a, **k):
        return ""


class _AsyncAnything:
    def __getattr__(self, name):
        return _AsyncAnything()

    async def __call__(self, *a, **k):
        return []


class _StubAppContext:
    user_id = USER_ID
    conversation_id = CONVERSATION_ID
    store = True
    emitter = _StubEmitter()


@pytest.fixture()
def persist_harness(monkeypatch):
    import matrx_ai.context.app_context as app_ctx_mod
    import matrx_ai.db.persistence as persistence_mod

    monkeypatch.setattr(app_ctx_mod, "get_app_context", lambda: _StubAppContext())
    monkeypatch.setattr(app_ctx_mod, "try_get_app_context", lambda: _StubAppContext())

    creates: list[dict[str, Any]] = []
    updates: list[tuple[str, dict[str, Any]]] = []

    monkeypatch.setattr(persistence_mod, "ai_model_manager_instance", _StubModelManager())
    monkeypatch.setattr(persistence_mod, "_get_coordinator", lambda: _StubCoordinator())
    monkeypatch.setattr(
        persistence_mod, "_queue_message_create", lambda **kw: creates.append(kw) or ""
    )
    monkeypatch.setattr(
        persistence_mod, "_queue_message_update", lambda mid, **kw: updates.append((mid, kw)) or ""
    )
    monkeypatch.setattr(persistence_mod, "_queue_conversation_update", lambda cid, **kw: "")
    monkeypatch.setattr(persistence_mod, "_queue_request_create", lambda **kw: "")
    monkeypatch.setattr(persistence_mod, "_queue_user_request_update", lambda rid, **kw: "")

    async def _no_hide(*a, **k):
        return 0

    async def _no_backfill(*a, **k):
        return []

    async def _no_op(*a, **k):
        return None

    monkeypatch.setattr(persistence_mod, "_hide_superseded_failed_turns", _no_hide)
    monkeypatch.setattr(persistence_mod, "_backfill_tool_message", _no_backfill)
    monkeypatch.setattr(persistence_mod, "_refresh_cache_state", _no_op)
    monkeypatch.setattr(persistence_mod, "_emit_context_state", _no_op)
    monkeypatch.setattr(persistence_mod, "cxm", _AsyncAnything())
    monkeypatch.setattr(persistence_mod, "try_get_tracker", lambda: None)

    return persistence_mod, creates, updates


def _completed_turn(user_text: str, assistant_text: str) -> CompletedRequest:
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text=user_text)]),
        UnifiedMessage(role="assistant", content=[TextContent(text=assistant_text)]),
    ]
    request = _request(*messages)
    return CompletedRequest(
        request=request,
        iterations=1,
        final_response=UnifiedResponse(messages=[messages[-1]]),
        trigger_message_position=0,
        result_start_position=1,
        result_end_position=1,
    )


def _row_text(fields: dict[str, Any]) -> str:
    return "".join(
        b.get("text", "")
        for b in fields.get("content", [])
        if isinstance(b, dict) and b.get("type") == "text"
    )


@pytest.mark.asyncio
async def test_completed_turn_persists_clean_text_plus_metadata(persist_harness, declared):
    persistence_mod, creates, _updates = persist_harness

    await persistence_mod.persist_completed_request(
        _completed_turn("how ready are we?", "We are nearly there.\nWRAP_RATING: 4\n"),
        conversation_id=CONVERSATION_ID,
        state=ExecutionState(),
    )

    assistant_rows = [c for c in creates if c.get("role") == "assistant"]
    assert len(assistant_rows) == 1
    row = assistant_rows[0]
    assert "WRAP_RATING" not in _row_text(row), (
        "the stored assistant message still carries the declared control line — "
        "the emitter cleaned the stream, nothing cleaned the row"
    )
    assert _row_text(row).startswith("We are nearly there.")
    assert row["metadata"][CONTROL_TOKEN_METADATA_KEY] == [
        {"name": "WRAP_RATING", "value": "4", "declared_by": WRAP_RATING.declared_by}
    ], "the value must survive as structured metadata — cleaning is not discarding"


@pytest.mark.asyncio
async def test_event_recording_block_stream_replays_token_at_completed_persistence(
    persist_harness, declared
):
    """The detached event recorder has no live token channel, but its explicit
    terminal persistence path retains the value in the resulting row.
    """

    class _WorkflowBlockSink:
        accepts_render_blocks = True

        async def send_chunk(self, _text: str) -> None:
            return None

        async def send_render_block(self, _data: dict[str, Any]) -> None:
            return None

    persistence_mod, creates, _updates = persist_harness
    raw = "We are nearly there.\nWRAP_RATING: 4\n"
    event_recorder = EventRecordingEmitter(base=_WorkflowBlockSink(), run_id="run-1")
    block_emitter = BlockStreamingEmitter(
        event_recorder, terminal_control_token_replay=True
    )

    await block_emitter.send_chunk(raw)
    await block_emitter.finalize_blocks()
    assert "WRAP_RATING" not in block_emitter.get_turn_text()

    await persistence_mod.persist_completed_request(
        _completed_turn("how ready are we?", raw),
        conversation_id=CONVERSATION_ID,
        state=ExecutionState(),
    )

    assistant_rows = [c for c in creates if c.get("role") == "assistant"]
    assert len(assistant_rows) == 1
    row = assistant_rows[0]
    assert "WRAP_RATING" not in _row_text(row)
    assert row["metadata"][CONTROL_TOKEN_METADATA_KEY] == [
        {"name": "WRAP_RATING", "value": "4", "declared_by": WRAP_RATING.declared_by}
    ]


@pytest.mark.asyncio
async def test_a_persons_own_words_are_never_cleaned(persist_harness, declared):
    persistence_mod, creates, _updates = persist_harness

    await persistence_mod.persist_completed_request(
        _completed_turn("WRAP_RATING: 4 is what your prompt says, right?", "Right."),
        conversation_id=CONVERSATION_ID,
        state=ExecutionState(),
    )

    user_rows = [c for c in creates if c.get("role") == "user"]
    assert len(user_rows) == 1
    assert "WRAP_RATING: 4" in _row_text(user_rows[0])
    assert CONTROL_TOKEN_METADATA_KEY not in (user_rows[0].get("metadata") or {})


# ---------------------------------------------------------------------------
# Seam 3 — the native ConversationRunner's turn writer
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_native_runner_append_turn_stores_clean_text_and_the_value(declared):
    from matrx_ai.orchestrator.conversation_persistence import CxmConversationPersistence

    queued: list[dict[str, Any]] = []

    async def _ensure(conversation_id, user_id):
        return None

    cx = CxmConversationPersistence(
        user_id=USER_ID,
        ensure_conversation=_ensure,
        queue_message=lambda **kw: queued.append(kw),
        conversation_data=None,
        rebuild_messages=None,
        id_factory=lambda: "fixed-id",
    )

    await cx.append_turn(
        conversation_id=CONVERSATION_ID,
        execution_id="e1",
        role="assistant",
        content="Nearly there.\nWRAP_RATING: 2\n",
    )
    await cx.append_turn(
        conversation_id=CONVERSATION_ID,
        execution_id="e1",
        role="user",
        content="WRAP_RATING: 2 is your own line, right?",
    )

    assistant, user = queued
    assert "WRAP_RATING" not in _row_text(assistant)
    assert assistant["metadata"][CONTROL_TOKEN_METADATA_KEY] == [
        {"name": "WRAP_RATING", "value": "2", "declared_by": WRAP_RATING.declared_by}
    ]
    assert "WRAP_RATING: 2" in _row_text(user)
    assert CONTROL_TOKEN_METADATA_KEY not in user["metadata"]
