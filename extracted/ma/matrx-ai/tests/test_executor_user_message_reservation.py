"""Regression test for the user-message reservation contract.

The 2026-05-28 user-message-loss bug: on the client-delegated suspend path,
``_flush_assistant_message_mid_loop`` committed the assistant row and then
advanced ``state.committed_position`` past the user position. The subsequent
``_persist_turn_and_commit`` early-returned (post_count - 1 <= committed_position)
without ever UPDATEing the user row from its empty 'pending' placeholder. The
row aged off to ``status='abandoned'`` with ``content_blocks=0`` while the
model had clearly already received the user's input.

The structural fix: reserve the user message with the REAL content and
``status='active'`` from the start. The content is fully known at reservation
time (the user already typed it). Even if the downstream UPDATE never runs,
the row is correct from the first coordinator flush.

This test pins the contract: when ``_execute_until_complete_inner`` reserves
the user message row, ``queue_message_create`` MUST be called with the actual
user content blocks (non-empty), not an empty placeholder, AND
``status='active'`` so the row is durable immediately.
"""

from __future__ import annotations

from typing import Any

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.db.message_positions import APPEND_MESSAGE_POSITION
from matrx_ai.orchestrator.requests import AIMatrixRequest


class _StubEmitter:
    async def send_info(self, *a, **k):
        return None

    async def send_phase(self, *a, **k):
        return None

    async def send_data(self, *a, **k):
        return None

    async def send_chunk(self, *a, **k):
        return None

    async def send_end(self, *a, **k):
        return None

    async def fatal_error(self, *a, **k):
        return None

    def reset_turn_text(self):
        return None

    def get_turn_text(self):
        return ""


class _StubAppContext:
    conversation_id = "11111111-1111-1111-1111-111111111111"
    user_id = "22222222-2222-2222-2222-222222222222"
    parent_conversation_id = None
    request_id = "33333333-3333-3333-3333-333333333333"
    store = True
    debug = False
    snapshot = False
    metadata: dict[str, Any] = {}
    emitter = _StubEmitter()


class _StubTracker:
    async def reserve(self, *a, **k):
        return None

    async def mark_active(self, *a, **k):
        return None

    def register_existing(self, *a, **k):
        return None


class _StubCoordinator:
    """Truthy stand-in for the request WriteCoordinator.

    Message-row reservation is gated on ``get_coordinator() is not None``
    (it is a streaming-lane-only optimization — without a lane the queue
    calls would be silently dropped). A unit test that invokes the executor
    directly has no streaming lane, so ``get_coordinator()`` returns ``None``
    and the entire reservation block is skipped — which is exactly why these
    tests started failing with "0 reservations" once that guard landed.

    The reservation block itself only needs the coordinator to be *truthy*;
    it never calls a method on it. The finalize path that runs AFTER the
    deliberate abort does call ``finalize()`` — kept here as a benign no-op so
    the real ``BaseException`` the tests assert on comes from the unconfigured
    DB layer (the ``_Stub`` cxm), not from an AttributeError on this object.
    """

    def queue(self, *a, **k):
        return ""

    def commit_async(self, *a, **k):
        return None

    async def check_pending(self, *a, **k):
        return None

    async def finalize(self, *a, **k):
        return None

    async def drain_and_confirm(self, *a, **k):
        return []

    async def seal(self, *a, **k):
        return None


class _AbortIteration(Exception):
    """Raised by the stubbed client to abort iteration after the reservation
    block has run, so we can inspect the captured queue calls."""


@pytest.mark.asyncio
async def test_invalid_stored_request_id_refuses_before_provider_or_persistence(monkeypatch):
    class _SyntheticStoredContext(_StubAppContext):
        request_id = "test-req"

    class _ClientThatMustNotRun:
        calls = 0

        async def execute(self, *args, **kwargs):
            self.calls += 1
            raise AssertionError("provider execution must not start")

    async def _persistence_gate_must_not_run(*args, **kwargs):
        raise AssertionError("invalid identity must refuse before persistence")

    monkeypatch.setattr(
        executor_mod, "ensure_conversation_exists", _persistence_gate_must_not_run
    )
    request = AIMatrixRequest(
        conversation_id=_SyntheticStoredContext.conversation_id,
        config=UnifiedConfig(model="test-model", messages=MessageList()),
        request_id=_SyntheticStoredContext.request_id,
    )
    client = _ClientThatMustNotRun()

    from matrx_ai.orchestrator.execution_state import ExecutionState

    with pytest.raises(ValueError, match="require a UUID request_id"):
        await executor_mod._execute_until_complete_inner(
            exec_ctx=_SyntheticStoredContext(),
            state=ExecutionState(),
            initial_request=request,
            client=client,
            max_iterations=1,
            max_retries_per_iteration=0,
        )

    assert client.calls == 0


@pytest.mark.asyncio
async def test_user_message_reservation_carries_real_content(monkeypatch):
    """The user message reservation MUST include the actual user content +
    ``status='active'`` so the row is durable even when the downstream
    UPDATE path is skipped (the client-delegated suspend race)."""

    # ------------------------------------------------------------------ #
    # 1. Capture every queue_message_create call. This is the assertion
    #    surface — we'll inspect what was queued for the user row.
    # ------------------------------------------------------------------ #
    captured_creates: list[dict[str, Any]] = []

    def fake_queue_message_create(**kwargs):
        captured_creates.append(kwargs)
        return "msg-id"

    import matrx_ai.persistence.queue_helpers as qh

    monkeypatch.setattr(qh, "queue_message_create", fake_queue_message_create)
    # Reservation is gated on a live coordinator (streaming lane). The unit
    # harness has none, so present a truthy stub to exercise the block.
    monkeypatch.setattr(qh, "get_coordinator", lambda: _StubCoordinator())

    # ------------------------------------------------------------------ #
    # 2. Stub out the conversation / user_request gates — they hit the DB,
    #    and we don't care about them for this test.
    # ------------------------------------------------------------------ #
    async def _noop_async(*a, **k):
        return None

    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _StubTracker())

    # ------------------------------------------------------------------ #
    # 3. Build a realistic AIMatrixRequest with a NON-EMPTY user message
    #    sitting at position 0 — exactly what agent_run.py would hand to
    #    the executor after appending request.user_input.
    # ------------------------------------------------------------------ #
    user_text = "What is the 2,000 limit? Please look it up."
    cfg = UnifiedConfig(
        model="claude-haiku-4-5",
        messages=MessageList(
            _messages=[
                UnifiedMessage(
                    role="user",
                    content=[TextContent(text=user_text)],
                )
            ]
        ),
    )
    req = AIMatrixRequest(
        conversation_id=_StubAppContext.conversation_id,
        config=cfg,
        request_id=_StubAppContext.request_id,
    )

    # ------------------------------------------------------------------ #
    # 4. Stub the AppContext getter so the inner function sees our fixture.
    # ------------------------------------------------------------------ #
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _StubAppContext())

    # ------------------------------------------------------------------ #
    # 5. Abort iteration AFTER the reservation block has run by having the
    #    UnifiedAIClient raise. We don't care about the actual API call
    #    here — we just want to inspect the queue calls made before it.
    # ------------------------------------------------------------------ #
    class _AbortingClient:
        async def execute(self, *a, **k):
            raise _AbortIteration()

    # ------------------------------------------------------------------ #
    # 6. Run the executor. It will get past the reservation block and
    #    then bail out when the client raises.
    # ------------------------------------------------------------------ #
    from matrx_ai.orchestrator.execution_state import ExecutionState

    state = ExecutionState()

    # We invoke the inner directly to avoid the outer cancel-shield
    # machinery (which would try to call _finalize_and_persist with our
    # stubbed dependencies and add noise to the test).
    with pytest.raises(BaseException):
        await executor_mod._execute_until_complete_inner(
            exec_ctx=_StubAppContext(),
            state=state,
            initial_request=req,
            client=_AbortingClient(),
            max_iterations=1,
            max_retries_per_iteration=0,
        )

    # ------------------------------------------------------------------ #
    # 7. Find the user message reservation and assert its shape. There
    #    will also be an assistant reservation — we filter by role.
    # ------------------------------------------------------------------ #
    user_reservations = [c for c in captured_creates if c.get("role") == "user"]
    assert len(user_reservations) == 1, (
        f"expected exactly one user message reservation, got "
        f"{len(user_reservations)}: {user_reservations}"
    )

    user_call = user_reservations[0]

    # Physical transcript order is allocated atomically by the database. The
    # model-visible index must never be written as a durable coordinate.
    assert user_call.get("position") == APPEND_MESSAGE_POSITION

    # Content MUST be non-empty — this is the bug class we're guarding
    # against. The placeholder content=[] caused content_blocks=0 in the DB.
    content = user_call.get("content") or []
    assert content, (
        "user message reservation has empty content — this is the "
        "2026-05-28 user-message-loss regression"
    )

    # The content must include the user's actual text.
    text_blocks = [b for b in content if isinstance(b, dict) and b.get("type") == "text"]
    assert text_blocks, f"no text block in user reservation content: {content}"
    assert user_text in text_blocks[0].get("text", ""), (
        f"user text not in reservation content: {text_blocks[0]}"
    )

    # Status MUST be 'active', not 'pending'. The 'pending' placeholder is
    # what the watchdog later flipped to 'abandoned' when the UPDATE never
    # arrived.
    assert user_call.get("status") == "active", (
        f"user reservation status is {user_call.get('status')!r} but must be "
        f"'active' so the row is durable on the first coordinator flush"
    )


@pytest.mark.asyncio
async def test_user_reservation_falls_back_to_pending_when_no_user_message(monkeypatch):
    """Edge case: no user message in config.messages (e.g. an internal call
    with messages=[]) — the reservation must still queue, but with the
    legacy empty/pending shape so any later code path that DID add a user
    message can finalize the row via the UPDATE."""

    captured_creates: list[dict[str, Any]] = []

    def fake_queue_message_create(**kwargs):
        captured_creates.append(kwargs)
        return "msg-id"

    import matrx_ai.persistence.queue_helpers as qh

    monkeypatch.setattr(qh, "queue_message_create", fake_queue_message_create)
    monkeypatch.setattr(qh, "get_coordinator", lambda: _StubCoordinator())

    async def _noop_async(*a, **k):
        return None

    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _StubTracker())
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _StubAppContext())

    # Empty messages list — pre_execution_message_count = 0.
    cfg = UnifiedConfig(
        model="claude-haiku-4-5",
        messages=MessageList(_messages=[]),
    )
    req = AIMatrixRequest(
        conversation_id=_StubAppContext.conversation_id,
        config=cfg,
        request_id=_StubAppContext.request_id,
    )

    class _AbortingClient:
        async def execute(self, *a, **k):
            raise _AbortIteration()

    from matrx_ai.orchestrator.execution_state import ExecutionState

    state = ExecutionState()

    with pytest.raises(BaseException):
        await executor_mod._execute_until_complete_inner(
            exec_ctx=_StubAppContext(),
            state=state,
            initial_request=req,
            client=_AbortingClient(),
            max_iterations=1,
            max_retries_per_iteration=0,
        )

    user_reservations = [c for c in captured_creates if c.get("role") == "user"]
    assert len(user_reservations) == 1
    user_call = user_reservations[0]

    # Empty content + pending status — there was nothing to write yet.
    assert user_call.get("content") in ([], None)
    assert user_call.get("status") == "pending"


@pytest.mark.asyncio
async def test_no_user_reservation_on_resume_shaped_history(monkeypatch):
    """A /resume run's trigger slot is the REBUILT tail of the conversation
    (a role='tool' message after a delegated suspend, or a persisted user
    message carrying its cx_message.id). Reserving a user row there used to
    INSERT an empty role='user' status='pending' placeholder at an
    already-occupied position — one per resume — which aged off to
    status='abandoned' (live evidence: conversation
    417e64ce-74ff-4fcd-b976-df1f0df56671 positions 24-27, 2026-06-09)."""

    captured_creates: list[dict[str, Any]] = []

    def fake_queue_message_create(**kwargs):
        captured_creates.append(kwargs)
        return "msg-id"

    import matrx_ai.persistence.queue_helpers as qh

    monkeypatch.setattr(qh, "queue_message_create", fake_queue_message_create)
    monkeypatch.setattr(qh, "get_coordinator", lambda: _StubCoordinator())

    async def _noop_async(*a, **k):
        return None

    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _StubTracker())
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _StubAppContext())

    # Rebuilt history: persisted user message (carries its id), assistant
    # with a tool call, and the tool-result tail — exactly what
    # ConversationResolver hands a /resume run.
    from matrx_ai.config import ToolResultContent

    persisted_user = UnifiedMessage(
        role="user",
        content=[TextContent(text="original question")],
        id="44444444-4444-4444-4444-444444444444",
    )
    assistant = UnifiedMessage(
        role="assistant",
        content=[TextContent(text="checking...")],
        id="55555555-5555-5555-5555-555555555555",
    )
    tool_tail = UnifiedMessage(
        role="tool",
        content=[ToolResultContent(tool_use_id="call-1", call_id="call-1", name="tabs")],
    )

    cfg = UnifiedConfig(
        model="claude-haiku-4-5",
        messages=MessageList(_messages=[persisted_user, assistant, tool_tail]),
    )
    req = AIMatrixRequest(
        conversation_id=_StubAppContext.conversation_id,
        config=cfg,
        request_id=_StubAppContext.request_id,
    )

    class _AbortingClient:
        async def execute(self, *a, **k):
            raise _AbortIteration()

    from matrx_ai.orchestrator.execution_state import ExecutionState

    state = ExecutionState()

    with pytest.raises(BaseException):
        await executor_mod._execute_until_complete_inner(
            exec_ctx=_StubAppContext(),
            state=state,
            initial_request=req,
            client=_AbortingClient(),
            max_iterations=1,
            max_retries_per_iteration=0,
        )

    # No role='user' reservation may be queued — the trigger slot is a
    # rebuilt tool message. The assistant reservation still queues.
    user_reservations = [c for c in captured_creates if c.get("role") == "user"]
    assert user_reservations == [], (
        f"resume-shaped history must not reserve a user row, got: {user_reservations}"
    )
    assistant_reservations = [c for c in captured_creates if c.get("role") == "assistant"]
    assert len(assistant_reservations) == 1
    assert assistant_reservations[0]["position"] == APPEND_MESSAGE_POSITION


@pytest.mark.asyncio
async def test_mid_loop_flush_appends_without_overwriting_reserved_position(monkeypatch):
    creates: list[dict[str, Any]] = []
    updates: list[tuple[str, dict[str, Any]]] = []

    import matrx_ai.persistence.queue_helpers as qh

    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: creates.append(kw) or "")
    monkeypatch.setattr(
        qh,
        "queue_message_update",
        lambda message_id, **kw: updates.append((message_id, kw)) or "",
    )
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _StubTracker())

    cfg = UnifiedConfig(
        model="claude-haiku-4-5",
        messages=MessageList(
            _messages=[
                UnifiedMessage(role="user", content=[TextContent(text="delegate this")])
            ]
        ),
    )
    request = AIMatrixRequest(
        conversation_id=_StubAppContext.conversation_id,
        config=cfg,
        request_id=_StubAppContext.request_id,
    )
    response = executor_mod.UnifiedResponse(
        messages=[
            UnifiedMessage(role="assistant", content=[TextContent(text="delegating")])
        ]
    )

    from matrx_ai.orchestrator.execution_state import ExecutionState

    state = ExecutionState()
    state.committed_position = -1
    reserved = {0: "user-message-id"}

    message_id = await executor_mod._flush_assistant_message_mid_loop(
        response=response,
        current_request=request,
        exec_ctx=_StubAppContext(),
        reserved_messages=reserved,
        parent_refs={"conversation_id": _StubAppContext.conversation_id},
        trigger_position=0,
        state=state,
    )

    assert message_id is not None
    assert updates[0][0] == "user-message-id"
    assert "position" not in updates[0][1]
    assert len(creates) == 1
    assert creates[0]["position"] == APPEND_MESSAGE_POSITION
    assert reserved[1] == message_id
