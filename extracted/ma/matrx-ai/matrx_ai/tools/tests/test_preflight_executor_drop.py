"""Regression: ``merge_request_tools`` drops tools with NO viable executor
before the model ever sees them.

The live failure this prevents: the ``user`` tool (LOCAL, no server
function_path, normally client-delegated) routed server-side on a surface whose
client executor wasn't active, so the model was handed it, CALLED it, and only
then failed at dispatch with ``no_viable_executor`` — a hard error surfaced to
the user mid-turn. The pre-flight gate removes such tools from the model's set
so they can't be called; the real fix for a tool that SHOULD run is to delegate
it (active client) or wire a server handler.
"""

from __future__ import annotations

import asyncio
from typing import Any

from matrx_connect import AppContext

from matrx_ai.config.message_config import MessageList
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.tools.merge import merge_request_tools
from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry


class _NullEmitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_reasoning_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_warning(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_tool_event(self, *_a: Any, **_kw: Any) -> None: ...
    async def fatal_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_end(self, *_a: Any, **_kw: Any) -> None: ...


def _ctx() -> AppContext:
    return AppContext(emitter=_NullEmitter(), client_tools=[])


def _config(tools: list[str]) -> UnifiedConfig:
    return UnifiedConfig(
        model="test-model", messages=MessageList(_messages=[]), tools=list(tools)
    )


def _register(
    registry: ToolRegistry, name: str, *, function_path: str = "", binding: set[str] | None = None
) -> None:
    registry._tools[name] = ToolDefinition(
        name=name,
        description="fixture",
        parameters={},
        tool_type=ToolType.LOCAL,
        function_path=function_path,
        source_kind="native",
    )
    if binding is not None:
        registry._bindings_by_tool[name] = set(binding)


def test_drops_unviable_local_tool_when_no_client_active() -> None:
    registry = ToolRegistry.get_instance()
    saved_tools, saved_bind = dict(registry._tools), dict(registry._bindings_by_tool)
    try:
        # Bound to matrx-user (client) but client NOT active this request.
        _register(registry, "__pf_unviable__", function_path="", binding={"matrx-user"})
        # A real server tool — has a function_path → always viable.
        _register(registry, "__pf_server__", function_path="pkg.mod.fn")

        config = _config(["__pf_unviable__", "__pf_server__"])
        merge_request_tools(config, _ctx(), [], active_executors=frozenset())

        assert "__pf_unviable__" not in config.tools  # dropped — nowhere to run
        assert "__pf_server__" in config.tools  # server handler → kept
    finally:
        registry._tools, registry._bindings_by_tool = saved_tools, saved_bind


def test_keeps_unviable_tool_when_client_delegates_it() -> None:
    registry = ToolRegistry.get_instance()
    saved_tools, saved_bind = dict(registry._tools), dict(registry._bindings_by_tool)
    try:
        _register(registry, "__pf_user__", function_path="", binding={"matrx-user"})

        config = _config(["__pf_user__"])
        ctx = merge_request_tools(
            config, _ctx(), [], active_executors=frozenset({"matrx-user"})
        )

        # Delegated to the active client → viable → kept on the model's set AND
        # marked for client delegation.
        assert "__pf_user__" in config.tools
        assert "__pf_user__" in list(ctx.client_tools or [])
    finally:
        registry._tools, registry._bindings_by_tool = saved_tools, saved_bind


def test_unviable_tool_drop_creates_structured_capture(monkeypatch) -> None:
    registry = ToolRegistry.get_instance()
    saved_tools, saved_bind = dict(registry._tools), dict(registry._bindings_by_tool)
    captured: list[dict[str, Any]] = []

    async def fake_capture_error(exc: BaseException, **kwargs: Any) -> None:
        captured.append({"exc": exc, **kwargs})

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error", fake_capture_error
    )
    try:
        # No server function and no configured client binding: this is a real
        # broken declaration and must enter the repair queue.
        _register(registry, "__pf_capture__", function_path="")

        async def exercise() -> None:
            merge_request_tools(
                _config(["__pf_capture__"]),
                AppContext(
                    emitter=_NullEmitter(),
                    client_tools=[],
                    request_id="request-1",
                    conversation_id="conversation-1",
                    route="/ai/conversations/conversation-1/resume",
                ),
                [],
                active_executors=frozenset(),
            )
            await asyncio.sleep(0)
            await asyncio.sleep(0)

        asyncio.run(exercise())

        assert len(captured) == 1
        assert captured[0]["kind"] == "unrunnable_tool_configuration"
        assert captured[0]["error_type"] == "ToolRoutingConfigurationError"
        assert captured[0]["request_id"] == "request-1"
        assert captured[0]["conversation_id"] == "conversation-1"
        assert captured[0]["context"]["dropped_tools"] == ["__pf_capture__"]
    finally:
        registry._tools, registry._bindings_by_tool = saved_tools, saved_bind


def test_inactive_client_binding_is_expected_gate_not_configuration_error(
    monkeypatch,
) -> None:
    registry = ToolRegistry.get_instance()
    saved_tools, saved_bind = dict(registry._tools), dict(registry._bindings_by_tool)
    captured: list[dict[str, Any]] = []

    async def fake_capture_error(exc: BaseException, **kwargs: Any) -> None:
        captured.append({"exc": exc, **kwargs})

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error", fake_capture_error
    )
    try:
        _register(
            registry,
            "__pf_client_only__",
            function_path="",
            binding={"matrx-user"},
        )

        async def exercise() -> None:
            config = _config(["__pf_client_only__"])
            merge_request_tools(config, _ctx(), [], active_executors=frozenset())
            await asyncio.sleep(0)
            assert "__pf_client_only__" not in config.tools

        asyncio.run(exercise())

        assert captured == []
    finally:
        registry._tools, registry._bindings_by_tool = saved_tools, saved_bind
