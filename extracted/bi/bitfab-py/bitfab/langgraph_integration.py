"""First-class LangGraph tool-call tracing and replay interception."""

from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, ParamSpec, Protocol, TypeVar

from bitfab import subtree
from bitfab.constants import _replay_context
from bitfab.mock_matching import MATCHER
from bitfab.mock_override import SpanNodeMeta

if TYPE_CHECKING:
    from langchain_core.messages import ToolMessage
    from langgraph.prebuilt.tool_node import ToolCallRequest
    from langgraph.types import Command

P = ParamSpec("P")
T = TypeVar("T")

_TOOL_RESULT_TAG = "__bitfabLangGraphToolResult"


class _LangGraphRunnable(Protocol):
    def with_config(self, config: dict[str, Any]) -> _LangGraphRunnable: ...

    def invoke(
        self,
        input: Any,
        config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any: ...

    async def ainvoke(
        self,
        input: Any,
        config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any: ...


def _is_tool_message(value: Any) -> bool:
    return (
        getattr(value, "type", None) == "tool"
        and getattr(value, "tool_call_id", None) is not None
    )


def _is_command(value: Any) -> bool:
    return type(value).__name__ == "Command" and hasattr(value, "update")


def _encode_nested(value: Any) -> Any:
    if _is_tool_message(value) or _is_command(value):
        return _encode_tool_result(value)
    if isinstance(value, (list, tuple)):
        return [_encode_nested(entry) for entry in value]
    if isinstance(value, dict):
        return {key: _encode_nested(entry) for key, entry in value.items()}
    return value


def _encode_tool_result(value: Any) -> dict[str, Any]:
    if _is_tool_message(value):
        return {
            _TOOL_RESULT_TAG: "tool-message",
            "content": value.content,
            "name": getattr(value, "name", None),
            "id": getattr(value, "id", None),
            "status": getattr(value, "status", None),
            "artifact": _encode_nested(getattr(value, "artifact", None)),
            "metadata": _encode_nested(getattr(value, "metadata", None)),
            "additionalKwargs": _encode_nested(
                getattr(value, "additional_kwargs", None)
            ),
            "responseMetadata": _encode_nested(
                getattr(value, "response_metadata", None)
            ),
        }

    if _is_command(value):
        return {
            _TOOL_RESULT_TAG: "command",
            "graph": getattr(value, "graph", None),
            "update": _encode_nested(getattr(value, "update", None)),
            "resume": _encode_nested(getattr(value, "resume", None)),
            "goto": _encode_nested(getattr(value, "goto", None)),
        }

    return {
        _TOOL_RESULT_TAG: "unsupported",
        "constructorName": type(value).__name__,
    }


def _is_encoded_tool_result(value: Any) -> bool:
    return isinstance(value, dict) and isinstance(value.get(_TOOL_RESULT_TAG), str)


def _revive_nested(value: Any, tool_call_id: str) -> Any:
    if _is_encoded_tool_result(value):
        return _revive_tool_result(value, tool_call_id)
    if isinstance(value, list):
        return [_revive_nested(entry, tool_call_id) for entry in value]
    if isinstance(value, dict):
        return {
            key: _revive_nested(entry, tool_call_id) for key, entry in value.items()
        }
    return value


def _without_none(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


def _revive_tool_result(value: dict[str, Any], tool_call_id: str) -> Any:
    kind = value[_TOOL_RESULT_TAG]
    if kind == "tool-message":
        try:
            from langchain_core.messages import ToolMessage
        except ImportError as error:
            raise RuntimeError(
                "LangGraph tool replay requires langchain-core. Install "
                "bitfab-py[langgraph] before using get_langgraph_integration()."
            ) from error

        return ToolMessage(
            **_without_none(
                {
                    "content": value.get("content", ""),
                    "tool_call_id": tool_call_id,
                    "name": value.get("name"),
                    "id": value.get("id"),
                    "status": value.get("status"),
                    "artifact": _revive_nested(value.get("artifact"), tool_call_id),
                    "metadata": _revive_nested(value.get("metadata"), tool_call_id),
                    "additional_kwargs": _revive_nested(
                        value.get("additionalKwargs"), tool_call_id
                    ),
                    "response_metadata": _revive_nested(
                        value.get("responseMetadata"), tool_call_id
                    ),
                }
            )
        )

    if kind == "command":
        try:
            from langgraph.types import Command
        except ImportError as error:
            raise RuntimeError(
                "Replaying a LangGraph Command requires bitfab-py[langgraph]."
            ) from error

        return Command(
            **_without_none(
                {
                    "graph": value.get("graph"),
                    "update": _revive_nested(value.get("update"), tool_call_id),
                    "resume": _revive_nested(value.get("resume"), tool_call_id),
                    "goto": _revive_nested(value.get("goto"), tool_call_id),
                }
            )
        )

    constructor_name = value.get("constructorName")
    detail = f" ({constructor_name})" if constructor_name else ""
    raise RuntimeError(
        f"The recorded LangGraph tool result{detail} cannot be replayed. "
        "Bitfab currently supports ToolMessage and Command results."
    )


def _as_tool_message_content(value: Any) -> str | list[dict[str, Any]]:
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(entry, dict) for entry in value):
        return value
    if value is None:
        return ""
    if isinstance(value, dict):
        try:
            return json.dumps(value, default=str)
        except ValueError:
            return str(value)
    return str(value)


def _revive_tool_override(value: Any, tool_call_id: str, tool_name: str) -> Any:
    if _is_encoded_tool_result(value):
        return _revive_tool_result(value, tool_call_id)
    if _is_tool_message(value) or _is_command(value):
        return value

    try:
        from langchain_core.messages import ToolMessage
    except ImportError as error:
        raise RuntimeError(
            "LangGraph tool replay requires langchain-core. Install "
            "bitfab-py[langgraph] before using get_langgraph_integration()."
        ) from error
    return ToolMessage(
        content=_as_tool_message_content(value),
        tool_call_id=tool_call_id,
        name=tool_name,
    )


class BitfabLangGraphIntegration:
    """Experimental callback tracing and native ``ToolNode`` replay hooks.

    This API may change before it is stable.
    """

    def __init__(
        self,
        *,
        client: Any,
        trace_function_key: str,
        callback_handler: Any,
        mock_tools_on_replay: bool | list[str] | tuple[str, ...] = True,
    ) -> None:
        self._client = client
        self._trace_function_key = trace_function_key
        self._mock_tools_on_replay = mock_tools_on_replay
        self.callback_handler = callback_handler

    def _should_mock(self, tool_name: str) -> bool:
        if isinstance(self._mock_tools_on_replay, bool):
            return self._mock_tools_on_replay
        return tool_name in self._mock_tools_on_replay

    def create_invoker(self, graph: _LangGraphRunnable) -> Callable[..., Any]:
        """Create a sync graph entry point with callbacks and replay root.

        Experimental: this API may change before it is stable.
        """
        configured_graph = graph.with_config({"callbacks": [self.callback_handler]})

        def invoke(
            input: Any,
            config: dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> Any:
            def invoke_graph(root_input: Any) -> Any:
                return configured_graph.invoke(root_input, config=config, **kwargs)

            return self.wrap_invoke(invoke_graph)(input)

        return invoke

    def create_async_invoker(
        self, graph: _LangGraphRunnable
    ) -> Callable[..., Awaitable[Any]]:
        """Create an async graph entry point with callbacks and replay root.

        Experimental: this API may change before it is stable.
        """
        configured_graph = graph.with_config({"callbacks": [self.callback_handler]})

        async def invoke(
            input: Any,
            config: dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> Any:
            async def invoke_graph(root_input: Any) -> Any:
                return await configured_graph.ainvoke(
                    root_input,
                    config=config,
                    **kwargs,
                )

            return await self.wrap_invoke(invoke_graph)(input)

        return invoke

    def _recording_trace_function_key(self) -> str:
        session = subtree.current_session()
        return session.label if session is not None else self._trace_function_key

    def _assert_replay_tool_call_is_safe(
        self, tool_name: str, tool_call_id: str | None, should_mock: bool
    ) -> None:
        replay_context = _replay_context.get()
        if not replay_context or replay_context.get("mock_tree") is None:
            return

        trace_function_key = self._recording_trace_function_key()
        counter_key = MATCHER.key_for(
            replay_context,
            trace_function_key=trace_function_key,
            span_name=tool_name,
            variant_chain=self._client._current_variant_chain(),
        )
        call_index = replay_context.get("call_counters", {}).get(counter_key, 0)
        mock_entry = replay_context.get("mock_tree", {}).get(
            f"{counter_key}:{call_index}"
        )
        node = SpanNodeMeta(
            trace_function_key=trace_function_key,
            span_name=tool_name,
            type="function",
            original_span_id=(mock_entry.get("sourceSpanId") if mock_entry else None),
        )
        has_matching_override = any(
            override.match(node)
            for override in replay_context.get("mock_overrides", [])
        )
        expects_recorded_output = replay_context.get("mock_strategy") == "all" or (
            replay_context.get("mock_strategy") == "marked" and should_mock
        )

        if not tool_call_id and (has_matching_override or expects_recorded_output):
            raise RuntimeError(
                f'LangGraph tool call "{tool_name}" has no ID; refusing to '
                "execute the live tool during replay."
            )

        if not has_matching_override and expects_recorded_output and not mock_entry:
            raise RuntimeError(
                f'No recorded LangGraph tool result for "{tool_name}" at call '
                f"{call_index + 1}; refusing to execute the live tool during replay."
            )

    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        """Intercept one synchronous call through ``ToolNode.wrap_tool_call``."""
        tool_call = request.tool_call
        tool_name = tool_call["name"]
        tool_call_id = tool_call.get("id")
        should_mock = self._should_mock(tool_name)
        self._assert_replay_tool_call_is_safe(tool_name, tool_call_id, should_mock)
        if not tool_call_id:
            return handler(request)

        @self._client._integration_span(
            self._trace_function_key,
            name=tool_name,
            type="function",
            capture_when="nested",
            mock_on_replay=should_mock,
            finalize=_encode_tool_result,
            instrumentation="langgraph",
        )
        def execute(_args: dict[str, Any]) -> Any:
            return handler(request)

        result = execute(tool_call.get("args", {}))
        return _revive_tool_override(result, tool_call_id, tool_name)

    async def awrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command]],
    ) -> ToolMessage | Command:
        """Intercept one asynchronous call through ``ToolNode.awrap_tool_call``."""
        tool_call = request.tool_call
        tool_name = tool_call["name"]
        tool_call_id = tool_call.get("id")
        should_mock = self._should_mock(tool_name)
        self._assert_replay_tool_call_is_safe(tool_name, tool_call_id, should_mock)
        if not tool_call_id:
            return await handler(request)

        @self._client._integration_span(
            self._trace_function_key,
            name=tool_name,
            type="function",
            capture_when="nested",
            mock_on_replay=should_mock,
            finalize=_encode_tool_result,
            instrumentation="langgraph",
        )
        async def execute(_args: dict[str, Any]) -> Any:
            return await handler(request)

        result = await execute(tool_call.get("args", {}))
        return _revive_tool_override(result, tool_call_id, tool_name)

    def wrap_invoke(self, fn: Callable[P, T]) -> Callable[P, T]:
        """Wrap the application function that invokes the compiled graph."""
        return self._client._integration_span(
            self._trace_function_key,
            name=self._trace_function_key,
            type="agent",
            instrumentation="langgraph",
        )(fn)
