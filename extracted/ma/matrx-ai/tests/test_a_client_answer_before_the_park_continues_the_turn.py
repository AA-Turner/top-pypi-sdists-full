"""A client that answers before the turn parks never strands the turn.

Live case (ops.system_error ``stream_ended_run_unfinished`` / ``suspended_awaiting_client``, conversation
101a5675, 2026-11-19/20, four rows): the client answered a delegated ``get_page_text`` 0.4 s after the call
was created. The batch's own look (``answered_meanwhile`` in handle_tool_calls) had already run and found
nothing; the answer landed during the turn's barrier commit, and the run parked 0.2 s later over a call
nobody had open. The client's /resume met the still-running run (409), so the turn stopped.

The guard drives the real loop: the answer lands during the barrier, and the turn must continue in its own
stream with that answer in the next model call, never park.
"""

from types import SimpleNamespace

import pytest
from matrx_connect import AppContext
from matrx_connect.context.app_context import clear_app_context, set_app_context

from matrx_ai.config import UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry


class _Emitter:
    def __init__(self) -> None:
        self.infos: list[str] = []

    def reset_turn_text(self):
        pass

    async def send_phase(self, *args, **kwargs):
        pass

    async def send_info(self, payload, *args, **kwargs):
        self.infos.append(getattr(payload, "code", ""))

    async def send_tool_event(self, *args, **kwargs):
        pass

    async def send_resource_changed(self, **kwargs):
        pass

    async def send_error(self, *args, **kwargs):
        raise AssertionError("the loop failed")


def _call_response(call_id: str) -> UnifiedResponse:
    return UnifiedResponse(messages=[UnifiedMessage(
        role="assistant", content=[ToolCallContent(id=call_id, name="get_page_text", arguments={})],
    )])


async def _drive(monkeypatch, *, answer_lands_during_barrier: bool):
    import matrx_ai.orchestrator.executor as orchestrator
    import matrx_ai.orchestrator.send_once as send_module
    import matrx_ai.tools.delegated_hold as delegated_hold
    import matrx_ai.tools.dynamic_drain as dynamic_drain
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig
    from matrx_ai.orchestrator.execution_state import ExecutionState
    from matrx_ai.orchestrator.requests import AIMatrixRequest

    conversation_id = "11111111-1111-1111-1111-111111111111"
    request_id = "33333333-3333-3333-3333-333333333333"

    registry = ToolRegistry.get_instance()
    saved_tools = dict(registry._tools)
    registry._tools["get_page_text"] = ToolDefinition(
        name="get_page_text", description="fixture", parameters={},
        tool_type=ToolType.LOCAL, function_path="os.path.join",
    )

    sent_messages: list[list] = []
    responses = [_call_response("call-1"), _call_response("call-2")]

    async def fake_send(_client, request, *args, **kwargs):
        sent_messages.append(list(request.config.messages.to_list()))
        return SimpleNamespace(response=responses[len(sent_messages) - 1])

    batches = iter([["call-1"], ["call-2"]])

    async def one_batch(_response, _request, _iteration, **_kwargs):
        # The client-run call is delegated; nothing is answered at the batch's end.
        return [], None, [], next(batches), [], None

    answered: dict[str, dict] = {}

    async def barrier(**kwargs):
        # The client's POST /tool_results lands while the barrier commits.
        if answer_lands_during_barrier and "call-1" not in answered:
            answered["call-1"] = {
                "type": "tool_result", "tool_use_id": "call-1", "call_id": "call-1",
                "name": "get_page_text", "content": "page text", "is_error": False,
            }

    async def read_answers(_conversation_id, call_ids):
        return {c: answered[c] for c in call_ids if c in answered}

    suspended: list[list[str]] = []

    async def suspend(**kwargs):
        suspended.append(list(kwargs["pending_call_ids"]))
        return "suspended"

    async def noop(*args, **kwargs):
        return None

    async def no_loop_top_drain(_config, ctx):
        return ctx

    class Tracker:
        async def reserve(self, **kwargs):
            pass

    monkeypatch.setattr(send_module, "send_once", fake_send)
    monkeypatch.setattr(orchestrator, "handle_tool_calls", one_batch)
    monkeypatch.setattr(orchestrator, "_suspend_for_delegation", suspend)
    monkeypatch.setattr(orchestrator, "_persist_turn_and_commit", barrier)
    monkeypatch.setattr(delegated_hold, "answered_meanwhile", read_answers)
    monkeypatch.setattr(orchestrator, "_apply_turn_directives", noop)
    monkeypatch.setattr(orchestrator, "ensure_conversation_exists", noop)
    monkeypatch.setattr(orchestrator, "ensure_user_request_exists", noop)
    monkeypatch.setattr(orchestrator, "get_tracker", lambda: Tracker())
    monkeypatch.setattr(orchestrator, "_schedule_labeling_if_new", lambda *a: None)
    monkeypatch.setattr(orchestrator, "_spine_stop_reason", noop)
    monkeypatch.setattr(orchestrator, "_is_request_cancelled", lambda *a: False)
    monkeypatch.setattr(orchestrator, "_request_snapshot_enabled", lambda *a: False)
    monkeypatch.setattr(orchestrator, "_response_has_live_client_delegated_call", lambda *a: False)
    monkeypatch.setattr(dynamic_drain, "drain_pending", no_loop_top_drain)

    emitter = _Emitter()
    app_ctx = AppContext(emitter=emitter, conversation_id=conversation_id, request_id=request_id)
    token = set_app_context(app_ctx)
    try:
        request = AIMatrixRequest(
            conversation_id=conversation_id,
            request_id=request_id,
            config=UnifiedConfig(
                model="test-model",
                tools=["get_page_text"],
                messages=MessageList(_messages=[
                    UnifiedMessage(role="user", content=[TextContent(text="Read this page")])
                ]),
            ),
        )
        exec_ctx = SimpleNamespace(
            conversation_id=conversation_id, request_id=request_id, user_id="", store=True,
            parent_conversation_id=None, debug=False, snapshot=False, emitter=emitter,
        )
        result = await orchestrator._execute_until_complete_inner(
            exec_ctx=exec_ctx, state=ExecutionState(), initial_request=request,
            client=SimpleNamespace(), max_iterations=3, max_retries_per_iteration=0,
        )
    finally:
        clear_app_context(token)
        registry._tools = saved_tools
    return result, suspended, sent_messages, emitter


@pytest.mark.asyncio
async def test_an_answer_that_lands_during_the_barrier_continues_the_turn(monkeypatch):
    result, suspended, sent, emitter = await _drive(monkeypatch, answer_lands_during_barrier=True)

    assert suspended and suspended[0] != ["call-1"], (
        "the turn parked on call-1 although its answer was stored before the park "
        f"(parks: {suspended})"
    )
    assert len(sent) == 2, "the turn did not make its next model call with the answer"
    results = [
        c for m in sent[1] if m.role == "tool" for c in m.content if isinstance(c, ToolResultContent)
    ]
    assert [r.call_id for r in results] == ["call-1"], "the next model call lacks the client's answer"
    assert "delegated_answer_taken_before_park" in emitter.infos, "the in-stream take was not announced"
    # The second call is still open: that one parks, as before.
    assert result == "suspended" and suspended == [["call-2"]]


@pytest.mark.asyncio
async def test_an_unanswered_call_still_parks(monkeypatch):
    result, suspended, sent, emitter = await _drive(monkeypatch, answer_lands_during_barrier=False)

    assert result == "suspended" and suspended == [["call-1"]]
    assert len(sent) == 1
    assert "delegated_answer_taken_before_park" not in emitter.infos
