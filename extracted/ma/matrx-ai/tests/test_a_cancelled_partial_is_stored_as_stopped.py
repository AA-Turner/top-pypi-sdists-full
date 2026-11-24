"""A helper stopped with ``task_stop`` is cancelled mid-stream (``asyncio.CancelledError``). It keeps what it
streamed, and that kept message must be STORED as a stopped partial, never as a finished answer.

Real shape (PB-08k r11, helper conversation a5740438): the 137-word partial was saved as an ordinary
assistant row, ``status='active'``, ``metadata={}`` -- indistinguishable from a finished answer except for the
marker sentence inside its text -- while the conversation said ``last_request_status='cancelled'``. The live
Stop path and the empty-reply path already stamp ``metadata.stopped``; this path did not."""

from __future__ import annotations

import asyncio

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.orchestrator.execution_state import ExecutionState

# The first words of the stored r11 row cb93491c (a streamed text cut by the cancel).
R11_PARTIAL = "Brennagh Archive §1\n\nThe printing press is often told as a single invention whose"


class _Ctx:
    conversation_id = "conv-1"
    user_id = "user-1"
    parent_conversation_id = None
    request_id = "req-1"
    store = True

    class _Emitter:
        async def send_info(self, *a, **k):
            return None

        def reset_turn_text(self):
            return None

        def get_turn_text(self):
            return R11_PARTIAL

    emitter = _Emitter()


async def _cancel_and_capture(monkeypatch, by):
    from matrx_ai.orchestrator.stop_origin import mark_stopped_by, open_stop_box
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.orchestrator.requests import AIMatrixRequest

    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _Ctx())
    cfg = UnifiedConfig(
        model="m",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="Write a 3,000-word history of the printing press.")])]
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

    async def fake_finalize(*, current_request, final_response, metadata, state, **_):
        captured["final_response"] = final_response
        captured["metadata"] = metadata
        state.persisted = True
        return object()

    monkeypatch.setattr(executor_mod, "_finalize_and_persist", fake_finalize)
    with open_stop_box() as box:  # the helper's run is started inside a box, like deferred_work does
        mark_stopped_by(box, by)
        with pytest.raises(asyncio.CancelledError):
            await executor_mod.execute_until_complete(initial_request=object(), client=object())

    messages = captured["final_response"].messages
    saved = messages if isinstance(messages, list) else [messages]
    assert len(saved) == 1
    assert captured["metadata"]["status"] == "cancelled"
    return saved[0], "".join(c.text for c in saved[0].content if hasattr(c, "text"))


@pytest.mark.asyncio
async def test_a_partial_kept_after_a_cancel_is_marked_stopped(monkeypatch):
    msg, text = await _cancel_and_capture(monkeypatch, None)
    assert "Brennagh Archive" in text  # what streamed is kept
    assert (msg.metadata or {}).get("stopped") is True  # and it says so on the stored row
    assert "stopped_by" not in msg.metadata and "by the user" not in text  # nobody said who: no stopper is claimed


@pytest.mark.asyncio
async def test_a_partial_stopped_by_the_lead_agent_says_so_and_not_the_user(monkeypatch):
    msg, text = await _cancel_and_capture(monkeypatch, "agent")
    assert msg.metadata["stopped"] is True and msg.metadata["stopped_by"] == "agent"
    assert "agent that started it" in text and "user" not in text.split("Brennagh")[-1].lower()


@pytest.mark.asyncio
async def test_a_partial_stopped_by_the_person_says_so(monkeypatch):
    msg, text = await _cancel_and_capture(monkeypatch, "person")
    assert msg.metadata["stopped_by"] == "person" and "stopped by the person" in text
