"""Regression test for the close-the-loop guarantee.

The whole persistence system exists to ensure that a client disconnect /
server shutdown mid-stream can NEVER eat the request's cost data. The
mechanism: when ``_execute_until_complete_inner`` raises CancelledError,
the outer ``execute_until_complete`` must shield-persist the in-flight
request (using the cost/usage on ``state.current_request``) BEFORE
re-raising — so the lane's drain finalizer has queued ops to flush.

This test pins that behavior. If someone removes the cancel handler, this
test fails loudly. The original incident was: cancellation propagated past
every ``except Exception`` (CancelledError doesn't inherit from Exception)
and the persist step never ran.
"""

from __future__ import annotations

import asyncio

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.orchestrator.execution_state import ExecutionState


class _StubAppContext:
    conversation_id = "conv-1"
    user_id = "user-1"
    parent_conversation_id = None
    request_id = "req-1"
    store = True

    class _Emitter:
        async def send_info(self, *a, **k):
            return None

    emitter = _Emitter()


class _SentinelRequest:
    """Stand-in for the in-flight AIMatrixRequest carrying accumulated cost."""

    def __init__(self):
        self.request_id = "req-1"
        self.conversation_id = "conv-1"
        self.total_cost = "0.92"  # the money that must not be lost


@pytest.mark.asyncio
async def test_cancel_midstream_persists_before_reraising(monkeypatch):
    """A CancelledError from the inner loop must trigger a cancelled-status
    persist of state.current_request, then re-raise."""

    monkeypatch.setattr(
        executor_mod, "get_app_context", lambda: _StubAppContext()
    )

    sentinel = _SentinelRequest()

    async def fake_inner(*, state: ExecutionState, **kwargs):
        # Simulate the loop having run far enough to accumulate cost, then a
        # client disconnect mid-stream.
        state.current_request = sentinel
        state.iteration = 2
        state.trigger_position = 0
        state.pre_execution_message_count = 1
        raise asyncio.CancelledError()

    monkeypatch.setattr(executor_mod, "_execute_until_complete_inner", fake_inner)

    persisted: dict = {}

    async def fake_finalize(*, current_request, iteration, final_response,
                            metadata, trigger_position,
                            pre_execution_message_count, debug, state):
        persisted["current_request"] = current_request
        persisted["metadata"] = metadata
        persisted["iteration"] = iteration
        if state is not None:
            state.persisted = True
        return object()  # CompletedRequest stand-in (not used on this path)

    monkeypatch.setattr(executor_mod, "_finalize_and_persist", fake_finalize)

    # The cancellation MUST still propagate (the stream layer relies on it).
    with pytest.raises(asyncio.CancelledError):
        await executor_mod.execute_until_complete(
            initial_request=object(),
            client=object(),
        )

    # ...but ONLY after persisting the in-flight cost.
    assert persisted, "cancel handler did not persist — the loop is open again"
    assert persisted["current_request"] is sentinel
    assert persisted["metadata"]["status"] == "cancelled"
    assert persisted["iteration"] == 2


@pytest.mark.asyncio
async def test_no_double_persist_when_already_persisted(monkeypatch):
    """If a normal completion already persisted (state.persisted=True) and a
    cancel races in, the cancel handler must NOT persist again."""

    monkeypatch.setattr(
        executor_mod, "get_app_context", lambda: _StubAppContext()
    )

    async def fake_inner(*, state: ExecutionState, **kwargs):
        state.current_request = _SentinelRequest()
        state.persisted = True  # normal completion already finalized
        raise asyncio.CancelledError()

    monkeypatch.setattr(executor_mod, "_execute_until_complete_inner", fake_inner)

    calls = {"n": 0}

    async def fake_finalize(**kwargs):
        calls["n"] += 1
        return object()

    monkeypatch.setattr(executor_mod, "_finalize_and_persist", fake_finalize)

    with pytest.raises(asyncio.CancelledError):
        await executor_mod.execute_until_complete(
            initial_request=object(), client=object(),
        )

    assert calls["n"] == 0, "double-persisted on cancel after normal completion"


@pytest.mark.asyncio
async def test_cancel_captures_partial_assistant_turn(monkeypatch):
    """An interrupt mid-stream must keep the partial assistant text the model
    already produced — saved as a real assistant turn with the interrupt marker
    — instead of dropping it (the old final_response=messages=[] behavior)."""
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.orchestrator.requests import AIMatrixRequest

    class _CtxWithPartial(_StubAppContext):
        class _Emitter:
            async def send_info(self, *a, **k):
                return None

            def reset_turn_text(self):
                return None

            def get_turn_text(self):
                return "Here is the partial answer the model produced"

        emitter = _Emitter()

    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _CtxWithPartial())

    cfg = UnifiedConfig(
        model="m",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]
        ),
    )
    req = AIMatrixRequest(conversation_id="conv-1", config=cfg)

    async def fake_inner(*, state: ExecutionState, **kwargs):
        state.current_request = req
        state.iteration = 1
        state.trigger_position = 0
        state.pre_execution_message_count = 1
        raise asyncio.CancelledError()

    monkeypatch.setattr(executor_mod, "_execute_until_complete_inner", fake_inner)

    captured: dict = {}

    async def fake_finalize(*, current_request, iteration, final_response, metadata,
                            trigger_position, pre_execution_message_count, debug, state):
        captured["final_response"] = final_response
        captured["metadata"] = metadata
        captured["current_request"] = current_request
        if state is not None:
            state.persisted = True
        return object()

    monkeypatch.setattr(executor_mod, "_finalize_and_persist", fake_finalize)

    with pytest.raises(asyncio.CancelledError):
        await executor_mod.execute_until_complete(
            initial_request=object(), client=object(),
        )

    fr = captured["final_response"]
    msgs = fr.messages if isinstance(fr.messages, list) else [fr.messages]
    assert len(msgs) == 1
    saved_text = "".join(c.text for c in msgs[0].content if hasattr(c, "text"))
    assert "Here is the partial answer the model produced" in saved_text
    assert "interrupted" in saved_text.lower()  # the marker landed
    assert captured["metadata"]["interrupted"] is True
    assert captured["metadata"]["partial_assistant_captured"] is True
    # The partial was appended to history (user trigger + the partial assistant turn).
    assert len(captured["current_request"].config.messages) == 2


@pytest.mark.asyncio
async def test_cancel_persists_provider_response_completed_after_cancel(monkeypatch):
    from matrx_ai.config import (
        MessageList,
        TextContent,
        UnifiedConfig,
        UnifiedMessage,
        UnifiedResponse,
    )
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.errors import attach_completed_response

    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _StubAppContext())

    cfg = UnifiedConfig(
        model="m",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="generate")])]
        ),
    )
    req = AIMatrixRequest(conversation_id="conv-1", config=cfg)
    completed_response = UnifiedResponse(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[TextContent(text="completed paid media result")],
            )
        ]
    )

    async def fake_inner(*, state: ExecutionState, **kwargs):
        state.current_request = req
        state.iteration = 1
        state.trigger_position = 0
        state.pre_execution_message_count = 1
        cancellation = asyncio.CancelledError()
        attach_completed_response(cancellation, completed_response)
        raise cancellation

    monkeypatch.setattr(executor_mod, "_execute_until_complete_inner", fake_inner)

    captured: dict = {}

    async def fake_finalize(
        *,
        current_request,
        iteration,
        final_response,
        metadata,
        trigger_position,
        pre_execution_message_count,
        debug,
        state,
    ):
        captured["final_response"] = final_response
        captured["metadata"] = metadata
        captured["current_request"] = current_request
        state.persisted = True
        return object()

    monkeypatch.setattr(executor_mod, "_finalize_and_persist", fake_finalize)

    with pytest.raises(asyncio.CancelledError):
        await executor_mod.execute_until_complete(
            initial_request=object(),
            client=object(),
        )

    assert captured["final_response"] is completed_response
    assert captured["metadata"]["provider_completed_after_cancellation"] is True
    assert captured["metadata"]["partial_assistant_captured"] is False
    assert len(captured["current_request"].config.messages) == 2


@pytest.mark.asyncio
async def test_cancel_with_no_inflight_request_still_reraises(monkeypatch):
    """If cancellation happens before any request is in flight (nothing to
    persist), the handler must still cleanly re-raise without crashing."""

    monkeypatch.setattr(
        executor_mod, "get_app_context", lambda: _StubAppContext()
    )

    async def fake_inner(*, state: ExecutionState, **kwargs):
        # state.current_request stays None
        raise asyncio.CancelledError()

    monkeypatch.setattr(executor_mod, "_execute_until_complete_inner", fake_inner)

    called = {"n": 0}

    async def fake_finalize(**kwargs):
        called["n"] += 1
        return object()

    monkeypatch.setattr(executor_mod, "_finalize_and_persist", fake_finalize)

    with pytest.raises(asyncio.CancelledError):
        await executor_mod.execute_until_complete(
            initial_request=object(), client=object(),
        )

    assert called["n"] == 0  # nothing to persist, but no crash
