"""End-to-end client-host execution: the CLASSIC path (execute_until_complete
via UnifiedAIClient) with an in-memory ConversationStore + static ModelCatalog
+ fake key resolver and the mock provider — zero DB, zero coordinator.

Asserts the store call order the desktop host relies on:
    ensure_conversation_exists → create_pending_user_request →
    persist_completed_request
and that the tool logger routes its start/update writes to the store.
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


class InMemoryStore:
    """Minimal ConversationStore implementation (host-side reference shape)."""

    def __init__(self) -> None:
        self.calls: list[str] = []
        self.conversations: dict[str, dict[str, Any]] = {}
        self.user_requests: dict[str, dict[str, Any]] = {}
        self.completed: list[Any] = []
        self.tool_rows: dict[str, dict[str, Any]] = {}

    async def ensure_conversation_exists(
        self,
        conversation_id: str,
        user_id: str,
        parent_conversation_id: str | None = None,
        variables: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> None:
        self.calls.append("ensure_conversation_exists")
        self.conversations.setdefault(
            conversation_id,
            {
                "id": conversation_id,
                "user_id": user_id,
                "parent_conversation_id": parent_conversation_id,
                "variables": variables or {},
                "overrides": overrides or {},
            },
        )

    async def create_pending_user_request(
        self, request_id: str, conversation_id: str, user_id: str
    ) -> None:
        self.calls.append("create_pending_user_request")
        self.user_requests.setdefault(
            request_id,
            {"id": request_id, "conversation_id": conversation_id, "user_id": user_id},
        )

    async def persist_completed_request(
        self, completed: Any, conversation_id: str | None = None
    ) -> dict[str, Any]:
        self.calls.append("persist_completed_request")
        self.completed.append(completed)
        return {
            "conversation_id": conversation_id or "",
            "user_request_id": "",
            "message_ids": [],
            "request_ids": [],
        }

    async def log_tool_call_start(self, row_id: str, data: dict[str, Any]) -> None:
        self.calls.append("log_tool_call_start")
        self.tool_rows[row_id] = dict(data)

    async def log_tool_call_update(self, row_id: str, data: dict[str, Any]) -> None:
        self.calls.append("log_tool_call_update")
        self.tool_rows.setdefault(row_id, {}).update(data)

    async def get_conversation_config(self, conversation_id: str) -> dict[str, Any]:
        self.calls.append("get_conversation_config")
        return self.conversations[conversation_id].get("config", {})

    async def get_conversation_data(self, conversation_id: str) -> dict[str, Any]:
        self.calls.append("get_conversation_data")
        return {
            "conversation": self.conversations[conversation_id],
            "messages": [],
            "tool_calls": [],
            "media": [],
            "user_requests": [],
            "requests": [],
        }


class StaticCatalog:
    def __init__(self, models: list[dict[str, Any]]) -> None:
        self._models = models

    async def list_models(self) -> list[dict[str, Any]]:
        return self._models

    async def get_model(self, id_or_name: str) -> dict[str, Any] | None:
        for model in self._models:
            if id_or_name in (str(model.get("id")), model.get("name")):
                return model
        return None


class FakeEmitter:
    """Every async emitter method is a no-op; the sync turn-text helpers exist."""

    def __init__(self) -> None:
        self.events: list[str] = []
        self._turn_text = ""

    def reset_turn_text(self) -> None:
        self._turn_text = ""

    def get_turn_text(self) -> str:
        return self._turn_text

    def __getattr__(self, name: str):
        async def _noop(*args: Any, **kwargs: Any) -> None:
            self.events.append(name)

        return _noop


_MOCK_MODEL = {
    "id": str(uuid.uuid4()),
    "name": "mock-model",
    "api_class": "mock_standard",
    "wire_format": "mock_chat",
    "provider": "mock",
    "capabilities": {
        "input": ["text"],
        "output": ["text"],
        "features": ["function_calling"],
    },
}


def _configure_client_host(store: InMemoryStore) -> None:
    configure_ext(
        conversation_store=store,
        model_catalog=StaticCatalog([_MOCK_MODEL]),
        api_key_resolver=lambda name: "not-a-real-key",
    )


def _set_context(emitter: FakeEmitter) -> tuple[str, str, str]:
    from matrx_connect.context.app_context import AppContext, set_app_context

    conversation_id = str(uuid.uuid4())
    request_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    ctx = AppContext(
        emitter=emitter,
        user_id=user_id,
        request_id=request_id,
        conversation_id=conversation_id,
        # Internal-agent marker keeps the fire-and-forget conversation labeler
        # (a second LLM call) out of this test.
        is_internal_agent=True,
        store=True,
        source_app="client_host_tests",
        source_feature="test",
    )
    set_app_context(ctx)
    return conversation_id, request_id, user_id


@pytest.mark.asyncio
async def test_classic_execution_routes_everything_to_store():
    store = InMemoryStore()
    _configure_client_host(store)
    emitter = FakeEmitter()
    conversation_id, request_id, _user_id = _set_context(emitter)

    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.orchestrator.executor import execute_until_complete
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.unified_client import UnifiedAIClient

    config = UnifiedConfig(
        model="mock-model",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="hi there")])]
        ),
        metadata={
            "mock": {
                "latency_ms": 1,
                "ttft_ms": 0,
                "chunks": 1,
                "mode": "text",
                "text": "hello from the mock model",
            }
        },
    )
    request = AIMatrixRequest(
        conversation_id=conversation_id,
        config=config,
        request_id=request_id,
    )

    completed = await execute_until_complete(request, UnifiedAIClient())

    # The mock's answer came back through the real path.
    final_text = "".join(
        c.text
        for m in completed.final_response.messages
        for c in (m.content or [])
        if getattr(c, "text", None)
    )
    assert "hello from the mock model" in final_text

    # Store call order — the contract the desktop host relies on.
    gate_and_persist = [
        c
        for c in store.calls
        if c
        in (
            "ensure_conversation_exists",
            "create_pending_user_request",
            "persist_completed_request",
        )
    ]
    assert gate_and_persist[0] == "ensure_conversation_exists"
    assert gate_and_persist[1] == "create_pending_user_request"
    assert "persist_completed_request" in gate_and_persist[2:]

    assert conversation_id in store.conversations
    assert request_id in store.user_requests
    assert store.completed, "persist_completed_request never received the CompletedRequest"
    assert store.completed[-1] is completed or hasattr(store.completed[-1], "final_response")


@pytest.mark.asyncio
async def test_tool_logger_routes_to_store():
    store = InMemoryStore()
    _configure_client_host(store)
    emitter = FakeEmitter()
    _conversation_id, _request_id, _user_id = _set_context(emitter)

    from matrx_ai.tools.logger import ToolExecutionLogger
    from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType

    logger = ToolExecutionLogger()
    tool_def = ToolDefinition(name="test_tool", tool_type=ToolType.LOCAL)
    ctx = ToolContext(call_id="call-1", tool_name="test_tool", iteration=1)

    row_id = await logger.log_started(ctx, tool_def, {"arg": "value"})
    assert row_id, "store-backed log_started must return the row id"
    assert store.tool_rows[row_id]["tool_name"] == "test_tool"
    assert store.tool_rows[row_id]["status"] == "running"

    result = ToolResult(success=True, output={"answer": 42})
    logger.prepare_metadata(result)
    await logger.log_completed(row_id, result)
    assert store.tool_rows[row_id]["status"] == "completed"
    assert store.tool_rows[row_id]["success"] is True

    # backfill is a host concern in a client host — must be a silent no-op.
    await logger.backfill_message_id("call-1", "conv-1", "msg-1")

    assert store.calls.count("log_tool_call_start") == 1
    assert store.calls.count("log_tool_call_update") == 1


@pytest.mark.asyncio
async def test_history_read_comes_from_store():
    store = InMemoryStore()
    _configure_client_host(store)
    emitter = FakeEmitter()
    conversation_id, _request_id, user_id = _set_context(emitter)

    await store.ensure_conversation_exists(conversation_id, user_id)
    store.conversations[conversation_id]["config"] = {
        "model": "mock-model",
        "messages": [{"role": "user", "content": "earlier turn"}],
    }

    from matrx_ai.agents.resolver import _load_unified_config

    config = await _load_unified_config(conversation_id)
    assert config.model == "mock-model"
    assert "get_conversation_config" in store.calls
