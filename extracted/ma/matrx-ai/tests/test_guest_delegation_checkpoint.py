"""EXT-D-0172: a client handoff needs a reconstructable assistant tool_use."""

from types import SimpleNamespace

import pytest
from matrx_connect import AppContext
from matrx_connect.context.app_context import clear_app_context, set_app_context

from matrx_ai.config import UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator.executor import _ensure_assistant_tool_use_on_disk
from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult
from matrx_ai.tools.registry import ToolRegistry


@pytest.mark.asyncio
async def test_ephemeral_client_handoff_does_not_require_a_stored_message():
    events = []

    class Emitter:
        async def send_tool_event(self, event):
            events.append(event)

    class Logger:
        async def delegate_durably(self, row_id, **kwargs):
            pass

    token = set_app_context(AppContext(emitter=Emitter(), store=False))
    try:
        executor = ToolExecutor(
            registry=SimpleNamespace(bindings_for_tool=lambda _name: []),
            execution_logger=Logger(),
        )
        result = await executor._execute_delegated(
            ToolDefinition(name="get_page_text"), {},
            ToolContext(call_id="call-ephemeral", tool_name="get_page_text"),
        )
        assert result.delegated_pending is True
        assert [event.event for event in events] == ["tool_delegated"]
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_failed_assistant_checkpoint_never_publishes_client_handoff():
    events = []
    parks = []

    class Emitter:
        async def send_tool_event(self, event):
            events.append(event)

    class Logger:
        async def delegate_durably(self, row_id, **kwargs):
            parks.append(row_id)

    async def failed_checkpoint():
        raise RuntimeError("assistant checkpoint finalize failed")

    token = set_app_context(AppContext(emitter=Emitter(), store=True))
    try:
        executor = ToolExecutor(
            registry=SimpleNamespace(bindings_for_tool=lambda _name: []),
            execution_logger=Logger(),
        )
        with pytest.raises(RuntimeError, match="assistant checkpoint finalize failed"):
            await executor._execute_delegated(
                ToolDefinition(name="get_page_text"), {},
                ToolContext(
                    call_id="call-page", tool_name="get_page_text",
                    assistant_checkpoint=failed_checkpoint,
                ),
                row_id="tool-row",
            )
        assert events == []
        assert parks == []
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
@pytest.mark.parametrize("resumed", [False, True])
@pytest.mark.parametrize("client_tools", [[], ["get_page_text"]])
async def test_orchestrator_checkpoints_a_call_promoted_to_client_at_dispatch(
    monkeypatch, client_tools, resumed
):
    """A classifier miss must still leave a resumable assistant/tool pair."""
    import matrx_ai.orchestrator.executor as orchestrator
    import matrx_ai.orchestrator.send_once as send_module
    import matrx_ai.persistence.queue_helpers as qh
    import matrx_ai.tools.dynamic_drain as dynamic_drain
    import matrx_ai.tools.handle_tool_calls as tool_calls_module
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig
    from matrx_ai.db import cxm
    from matrx_ai.orchestrator.execution_state import ExecutionState
    from matrx_ai.orchestrator.requests import AIMatrixRequest

    conversation_id = "11111111-1111-1111-1111-111111111111"
    request_id = "33333333-3333-3333-3333-333333333333"
    rows = {}
    queued = []
    events = []
    server_message_ids = []

    class Coordinator:
        async def finalize(self, *, reason):
            for operation, row_id, fields in queued:
                if operation == "create":
                    rows[row_id] = SimpleNamespace(
                        **{
                            "created_at": None, "metadata": {}, "deleted_at": None,
                            "is_visible_to_model": True,
                            **fields,
                            "position": len(rows),
                        },
                        id=row_id,
                    )
                else:
                    for key, value in fields.items():
                        setattr(rows[row_id], key, value)
            queued.clear()

    coordinator = Coordinator()

    def create(**fields):
        queued.append(("create", fields["id"], {k: v for k, v in fields.items() if k != "id"}))

    def update(row_id, **fields):
        queued.append(("update", row_id, fields))

    async def read_message(**kwargs):
        return [rows[kwargs["id"]]] if kwargs["id"] in rows else []

    class Emitter:
        def reset_turn_text(self):
            pass

        async def send_phase(self, *args, **kwargs):
            pass

        async def send_info(self, *args, **kwargs):
            pass

        async def send_error(self, *args, **kwargs):
            raise AssertionError("provider path failed before the handoff")

        async def send_tool_event(self, event):
            events.append(event)

    class Tracker:
        async def reserve(self, **kwargs):
            pass

    class Logger:
        async def delegate_durably(self, row_id, **kwargs):
            assert any(
                row.status == "active" and any(
                    block.get("call_id") == "call-page" for block in row.content
                )
                for row in rows.values() if row.role == "assistant"
            )

    from matrx_ai.db.conversation_rebuild import rebuild_conversation_messages

    history = [UnifiedMessage(role="user", content=[TextContent(text="Read this page")])]
    if resumed:
        # Live resume: two physical message rows rebuild into three logical
        # messages because the tool-result row lives in the tool ledger.
        for row_id, role, position, content in [
            ("prior-user", "user", 0, [{"type": "text", "text": "Read this page"}]),
            ("prior-assistant", "assistant", 1,
             [{"type": "tool_call", "call_id": "prior-call", "name": "get_page_text", "arguments": {}}]),
        ]:
            rows[row_id] = SimpleNamespace(
                id=row_id, conversation_id=conversation_id, role=role,
                position=position, content=content, status="active",
                created_at=None, metadata={}, deleted_at=None, is_visible_to_model=True,
            )
        prior_tool = SimpleNamespace(
            id="prior-tool", call_id="prior-call", message_id="prior-assistant",
            tool_name="get_page_text", output="page text", is_error=False,
            status="completed", output_chars=9, output_preview=None,
            deleted_at=None, model_stub_at=None,
        )
        history = await rebuild_conversation_messages(list(rows.values()), [prior_tool], [])
        assert len(history) == 3 and len(rows) == 2

    response = UnifiedResponse(messages=[UnifiedMessage(
        role="assistant", content=[
            ToolCallContent(id="call-server", name="server_lookup"),
            ToolCallContent(id="call-page", name="get_page_text"),
        ]
    )])
    async def fake_send(*args, **kwargs):
        return SimpleNamespace(response=response)

    registry = ToolRegistry()
    registry.register(ToolDefinition(name="server_lookup", side_effect_class="read_only"))
    registry.register(ToolDefinition(name="get_page_text", side_effect_class="read_only"))
    executor = ToolExecutor(registry=registry, execution_logger=Logger())

    async def execute_tool(name, arguments, ctx, client_tools=None, allowed_tools=None):
        if name == "server_lookup":
            server_message_ids.append(ctx.message_id)
            result = ToolResult(
                success=True, output="server result", tool_name=name, call_id=ctx.call_id
            )
            return result.to_tool_result_content(), result
        result = await executor._execute_delegated(
            registry.get("get_page_text"), arguments, ctx, row_id="tool-row"
        )
        return result.to_tool_result_content(), result

    monkeypatch.setattr(executor, "execute", execute_tool)
    monkeypatch.setattr(tool_calls_module, "get_executor", lambda: executor)
    monkeypatch.setattr(tool_calls_module, "_is_handoff_call", lambda _name: False)
    monkeypatch.setattr(
        tool_calls_module.ToolLifecycleManager, "get_instance",
        classmethod(lambda cls: SimpleNamespace(sweep_running=True)),
    )

    async def noop(*args, **kwargs):
        return None

    monkeypatch.setattr(qh, "get_coordinator", lambda: coordinator)
    monkeypatch.setattr(qh, "queue_message_create", create)
    monkeypatch.setattr(qh, "queue_message_update", update)
    monkeypatch.setattr(qh, "queue_user_request_update", lambda *args, **kwargs: None)
    monkeypatch.setattr(cxm.message, "filter_items", read_message)
    monkeypatch.setattr(orchestrator, "ensure_conversation_exists", noop)
    monkeypatch.setattr(orchestrator, "ensure_user_request_exists", noop)
    monkeypatch.setattr(orchestrator, "get_tracker", lambda: Tracker())
    monkeypatch.setattr(orchestrator, "_schedule_labeling_if_new", lambda *a: None)
    monkeypatch.setattr(orchestrator, "_spine_stop_reason", noop)
    monkeypatch.setattr(orchestrator, "_is_request_cancelled", lambda *a: False)
    monkeypatch.setattr(orchestrator, "_request_snapshot_enabled", lambda *a: False)
    monkeypatch.setattr(orchestrator, "_response_has_live_client_delegated_call", lambda *a: False)
    monkeypatch.setattr(orchestrator, "_apply_turn_directives", noop)
    monkeypatch.setattr(orchestrator, "_persist_turn_and_commit", noop)
    async def suspended(**kwargs):
        assert kwargs["pending_call_ids"] == ["call-page"]
        return "suspended"
    monkeypatch.setattr(orchestrator, "_suspend_for_delegation", suspended)
    monkeypatch.setattr(send_module, "send_once", fake_send)
    async def no_drain(_config, ctx):
        return ctx
    monkeypatch.setattr(dynamic_drain, "drain_pending", no_drain)

    app_ctx = AppContext(
        emitter=Emitter(), conversation_id=conversation_id,
        client_tools=client_tools,
    )
    token = set_app_context(app_ctx)
    try:
        request = AIMatrixRequest(
            conversation_id=conversation_id,
            request_id=request_id,
            config=UnifiedConfig(model="test-model", messages=MessageList(_messages=history)),
        )
        exec_ctx = SimpleNamespace(
            conversation_id=conversation_id, request_id=request_id, user_id="", store=True,
            parent_conversation_id=None, debug=False, snapshot=False,
            emitter=app_ctx.emitter,
        )
        result = await orchestrator._execute_until_complete_inner(
            exec_ctx=exec_ctx, state=ExecutionState(), initial_request=request,
            client=SimpleNamespace(), max_iterations=1, max_retries_per_iteration=0,
        )
        assert result == "suspended"
        assert [event.event for event in events] == ["tool_delegated"]
        if client_tools:
            # The real batch router gave the server sibling the assistant ID
            # before its concurrent execution began.
            assert server_message_ids and server_message_ids[0] is not None
        from matrx_ai.db.conversation_rebuild import rebuild_conversation_messages
        assistant = next(row for row in rows.values() if row.role == "assistant" and row.id != "prior-assistant")
        assert assistant.position == (2 if resumed else 1)
        tool_row = SimpleNamespace(
            id="tool-row", call_id="call-page", message_id=assistant.id,
            tool_name="get_page_text", output="page text", is_error=False,
            status="completed", output_chars=9, output_preview=None,
            deleted_at=None, model_stub_at=None,
        )
        rebuilt = await rebuild_conversation_messages([assistant], [tool_row], [])
        assert [getattr(m.role, "value", m.role) for m in rebuilt] == ["assistant", "tool"]
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_client_handoff_repairs_empty_reservation_before_publication(monkeypatch):
    import matrx_connect.streaming.error_capture as error_capture

    import matrx_ai.persistence.queue_helpers as qh
    from matrx_ai.db import cxm

    conversation_id = "11111111-1111-1111-1111-111111111111"
    message_id = "22222222-2222-2222-2222-222222222222"
    call_id = "call-page"
    row = SimpleNamespace(
        id=message_id,
        conversation_id=conversation_id,
        position=1,
        role="assistant",
        status="pending",
        content=[],
        created_at=None,
        metadata={},
        deleted_at=None,
        is_visible_to_model=True,
    )
    writes = []
    events = []
    parks = []
    captures = []

    async def capture(_exc, **kwargs):
        captures.append(kwargs)

    async def read_message(**kwargs):
        assert kwargs == {"id": message_id}
        return [row]

    def queue_update(row_id, **fields):
        assert row_id == message_id
        writes.append(fields)

    class Coordinator:
        async def finalize(self, *, reason):
            assert reason == "assistant_delegation_checkpoint_repair"
            fields = writes[-1]
            row.status = fields["status"]
            row.content = fields["content"]

    class Emitter:
        async def send_tool_event(self, event):
            events.append(event)

    class Logger:
        async def delegate_durably(self, row_id, **kwargs):
            parks.append(row_id)

    monkeypatch.setattr(cxm.message, "filter_items", read_message)
    monkeypatch.setattr(qh, "queue_message_update", queue_update)
    monkeypatch.setattr(error_capture, "capture_error", capture)
    response = UnifiedResponse(
        messages=[
            UnifiedMessage(
                role="assistant", content=[ToolCallContent(id=call_id, name="get_page_text")]
            )
        ]
    )
    emitter = Emitter()
    token = set_app_context(AppContext(emitter=emitter, conversation_id=conversation_id))
    try:
        executor = ToolExecutor(
            registry=SimpleNamespace(bindings_for_tool=lambda _name: []),
            execution_logger=Logger(),
        )
        definition = ToolDefinition(name="get_page_text")
        ctx = ToolContext(call_id=call_id, tool_name="get_page_text", message_id=message_id)

        # The original pending/empty row cannot be published as a client call.
        with pytest.raises(RuntimeError, match="assistant tool_use is not durable"):
            await executor._execute_delegated(definition, {}, ctx, row_id="tool-row")
        assert not parks and not events

        await _ensure_assistant_tool_use_on_disk(
            message_id, response, Coordinator(), conversation_id=conversation_id
        )
        assert row.status == "active"
        assert captures[0]["kind"] == "assistant_delegation_checkpoint_missing"
        assert {part["call_id"] for part in row.content if part["type"] == "tool_call"} == {call_id}
        result = await executor._execute_delegated(definition, {}, ctx, row_id="tool-row")
        assert result.delegated_pending is True
        assert parks == ["tool-row"]
        assert [event.event for event in events] == ["tool_delegated"]

        # POST /tool_results completes the durable tool row; /resume rebuilds
        # from this exact assistant row and synthesizes its model-visible pair.
        from matrx_ai.db.conversation_rebuild import rebuild_conversation_messages

        tool_row = SimpleNamespace(
            id="tool-row",
            call_id=call_id,
            message_id=message_id,
            tool_name="get_page_text",
            output="page text",
            is_error=False,
            status="completed",
            output_chars=9,
            output_preview=None,
            deleted_at=None,
            model_stub_at=None,
        )
        rebuilt = await rebuild_conversation_messages([row], [tool_row], [])
        assert [getattr(m.role, "value", m.role) for m in rebuilt] == ["assistant", "tool"]
        assert rebuilt[0].content[0].id == call_id
        assert rebuilt[1].content[0].tool_use_id == call_id
        assert rebuilt[1].content[0].content == "page text"
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
@pytest.mark.parametrize("deleted", [False, True])
@pytest.mark.parametrize(
    ("conversation", "status", "content"),
    [
        ("another-conversation", "pending", []),
        ("another-conversation", "active", [{"type": "tool_call", "call_id": "call-page"}]),
        ("expected", "pending", [{"type": "text", "text": "prior answer"}]),
        ("expected", "active", [{"type": "tool_call", "call_id": "other-call"}]),
        ("expected", "active", [{"type": "tool_call", "call_id": "call-page"}]),
    ],
)
async def test_client_handoff_refuses_foreign_or_occupied_reservation(
    monkeypatch, conversation, status, content, deleted
):
    import matrx_connect.streaming.error_capture as error_capture

    import matrx_ai.persistence.queue_helpers as qh
    from matrx_ai.db import cxm

    row = SimpleNamespace(
        conversation_id=conversation,
        deleted_at="2026-10-08" if deleted else None,
        position=1,
        role="assistant",
        status=status,
        content=content,
    )

    async def read_message(**_kwargs):
        return [row]

    def forbidden_update(*_args, **_kwargs):
        raise AssertionError("a foreign reservation was overwritten")

    monkeypatch.setattr(cxm.message, "filter_items", read_message)
    monkeypatch.setattr(qh, "queue_message_update", forbidden_update)

    async def capture(_exc, **_kwargs):
        return None

    monkeypatch.setattr(error_capture, "capture_error", capture)
    response = UnifiedResponse(
        messages=[
            UnifiedMessage(
                role="assistant", content=[ToolCallContent(id="call-page", name="get_page_text")]
            )
        ]
    )
    if conversation == "expected" and status == "active" and content[0].get("call_id") == "call-page" and not deleted:
        await _ensure_assistant_tool_use_on_disk(
            "message-id", response, SimpleNamespace(), conversation_id="expected"
        )
        return
    with pytest.raises(RuntimeError, match="conflicts with reservation"):
        await _ensure_assistant_tool_use_on_disk(
            "message-id", response, SimpleNamespace(), conversation_id="expected"
        )
