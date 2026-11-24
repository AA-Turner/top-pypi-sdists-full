"""Tools a tool loads in the SAME batch as a client-delegated call survive the suspend.

Live case (conversation 318c8f35, 2026-11-18): the browser agent called
``load_chrome_tools(category='reading')`` and ``tabs`` (client-delegated) in ONE
iteration. ``load_chrome_tools`` queued its 19 tools on the request's metadata to be
applied at the next loop top; the delegated ``tabs`` suspended the turn first, so that
loop top never ran. The queued additions died with the request, the conversation row
was stored without them, and after ``/resume`` the model's call to ``data_patterns``
was refused: "was not provided to the model for this request".

The guard drives the real orchestrator loop to the delegation suspend and checks the
config the suspend persists carries the loaded tool as a sticky conversation tool and
in the allowed set.
"""

from types import SimpleNamespace

import pytest
from matrx_connect import AppContext
from matrx_connect.context.app_context import clear_app_context, set_app_context

from matrx_ai.config import UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry
from matrx_ai.tools.specs import RegisteredToolSpec


class _Emitter:
    def __init__(self) -> None:
        self.resource_changes: list[dict] = []

    def reset_turn_text(self):
        pass

    async def send_phase(self, *args, **kwargs):
        pass

    async def send_info(self, *args, **kwargs):
        pass

    async def send_tool_event(self, *args, **kwargs):
        pass

    async def send_resource_changed(self, **kwargs):
        self.resource_changes.append(kwargs)

    async def send_error(self, *args, **kwargs):
        raise AssertionError("the loop failed before the delegation suspend")


@pytest.mark.asyncio
async def test_a_tool_loaded_beside_a_delegated_call_is_kept_through_the_suspend(monkeypatch):
    import matrx_ai.orchestrator.executor as orchestrator
    import matrx_ai.orchestrator.send_once as send_module
    import matrx_ai.tools.dynamic_drain as dynamic_drain
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig
    from matrx_ai.orchestrator.execution_state import ExecutionState
    from matrx_ai.orchestrator.requests import AIMatrixRequest

    conversation_id = "11111111-1111-1111-1111-111111111111"
    request_id = "33333333-3333-3333-3333-333333333333"

    registry = ToolRegistry.get_instance()
    saved_tools = dict(registry._tools)
    for name in ("load_chrome_tools", "tabs", "data_patterns"):
        registry._tools[name] = ToolDefinition(
            name=name, description="fixture", parameters={},
            tool_type=ToolType.LOCAL, function_path="os.path.join",
        )

    response = UnifiedResponse(messages=[UnifiedMessage(
        role="assistant", content=[
            ToolCallContent(id="call-load", name="load_chrome_tools", arguments={"category": "reading"}),
            ToolCallContent(id="call-tabs", name="tabs", arguments={}),
        ],
    )])

    async def fake_send(*args, **kwargs):
        return SimpleNamespace(response=response)

    async def one_batch(_response, _request, _iteration, **_kwargs):
        # What the real batch does: load_chrome_tools queues its loaded set (the real
        # ToolContext API) and tabs is delegated to the client, so the turn suspends.
        ToolContext(call_id="call-load", tool_name="load_chrome_tools").queue_tool_changes(
            add=[RegisteredToolSpec(name="data_patterns")]
        )
        return [], None, [], ["call-tabs"], [], None

    persisted = {}

    async def suspended(**kwargs):
        config = kwargs["current_request"].config
        persisted["dynamic_tools"] = list(config.dynamic_tools or [])
        persisted["allowed"] = orchestrator._resolve_allowed_tools(config)
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
    monkeypatch.setattr(orchestrator, "_suspend_for_delegation", suspended)
    monkeypatch.setattr(orchestrator, "_persist_turn_and_commit", noop)
    monkeypatch.setattr(orchestrator, "_apply_turn_directives", noop)
    monkeypatch.setattr(orchestrator, "ensure_conversation_exists", noop)
    monkeypatch.setattr(orchestrator, "ensure_user_request_exists", noop)
    monkeypatch.setattr(orchestrator, "get_tracker", lambda: Tracker())
    monkeypatch.setattr(orchestrator, "_schedule_labeling_if_new", lambda *a: None)
    monkeypatch.setattr(orchestrator, "_spine_stop_reason", noop)
    monkeypatch.setattr(orchestrator, "_is_request_cancelled", lambda *a: False)
    monkeypatch.setattr(orchestrator, "_request_snapshot_enabled", lambda *a: False)
    monkeypatch.setattr(orchestrator, "_response_has_live_client_delegated_call", lambda *a: False)
    # The loop-top drain (inbox + host refresh) never runs again in this request, which
    # is the point: only the batch's own queue is under test.
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
                tools=["load_chrome_tools", "tabs"],
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

    assert result == "suspended"
    # The stored conversation config is what /resume rebuilds the toolset from.
    assert "data_patterns" in persisted["dynamic_tools"], (
        "a tool loaded in the same batch as a delegated call was dropped at the suspend; "
        f"stored dynamic_tools={persisted['dynamic_tools']}"
    )
    assert "data_patterns" in (persisted["allowed"] or frozenset())
    # The client was told its active toolset changed (the same event the loop top sends).
    assert any(
        "data_patterns" in (ev.get("metadata") or {}).get("added_tools", [])
        for ev in emitter.resource_changes
    )
