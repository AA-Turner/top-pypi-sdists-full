"""First-class LangGraph tool-call tracing and replay interception."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator, Sequence
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, ParamSpec, Protocol, TypeVar

from bitfab import subtree
from bitfab.client import _active_span_context
from bitfab.constants import _replay_context
from bitfab.mock_matching import MATCHER
from bitfab.mock_override import SpanNodeMeta
from bitfab.warn_once import warn_once

if TYPE_CHECKING:
    from langchain_core.messages import ToolMessage
    from langgraph.prebuilt.tool_node import ToolCallRequest
    from langgraph.types import Command

    from bitfab.agent_middleware import BitfabAgentMiddleware

P = ParamSpec("P")
T = TypeVar("T")
GraphT = TypeVar("GraphT")

_TOOL_RESULT_TAG = "__bitfabLangGraphToolResult"
_STATE_WRITES_KEY = "stateWrites"
_PREGEL_KEY_PREFIX = "__pregel_"
_PREGEL_SEND_KEY = f"{_PREGEL_KEY_PREFIX}send"
_DEEPAGENTS_INSTALL = "pip install 'bitfab-py[deepagents]' (Python 3.11+)"
_LANGCHAIN_INSTALL = "pip install 'langchain>=1.0'"


def _missing_package(package: str, install: str) -> ImportError:
    return ImportError(
        f"{package} is required for this LangGraph integration method. "
        f"Install it with: {install}"
    )


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

    def stream(
        self,
        input: Any,
        config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Iterator[Any]: ...

    def astream(
        self,
        input: Any,
        config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[Any]: ...


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


def _encode_tool_result_with_state_writes(
    value: Any, state_writes: list[tuple[str, Any]]
) -> dict[str, Any]:
    encoded = _encode_tool_result(value)
    if state_writes and encoded[_TOOL_RESULT_TAG] != "unsupported":
        encoded[_STATE_WRITES_KEY] = [
            [channel, _encode_nested(update)] for channel, update in state_writes
        ]
    return encoded


def _tool_call_configurable(request: ToolCallRequest) -> dict[str, Any] | None:
    config = getattr(getattr(request, "runtime", None), "config", None)
    if not isinstance(config, dict):
        return None
    configurable = config.get("configurable")
    return configurable if isinstance(configurable, dict) else None


def _pregel_send(request: ToolCallRequest) -> Callable[[Any], None] | None:
    configurable = _tool_call_configurable(request)
    if configurable is None:
        return None
    send = configurable.get(_PREGEL_SEND_KEY)
    runs_inside_graph = any(
        isinstance(key, str) and key.startswith(_PREGEL_KEY_PREFIX)
        for key in configurable
    )
    if send is None and runs_inside_graph:
        warn_once(
            "langgraph-state-writes-unavailable",
            "this LangGraph version does not expose its state-write function to "
            "tool calls, so graph state a tool writes while it runs (such as a "
            "Deep Agents file) is not recorded and is not restored on replay.",
        )
    return send


@contextmanager
def _recording_state_writes(
    request: ToolCallRequest,
) -> Iterator[list[tuple[str, Any]]]:
    state_writes: list[tuple[str, Any]] = []
    send = _pregel_send(request)
    if send is None:
        yield state_writes
        return

    def record_and_send(writes: Any) -> None:
        entries = list(writes)
        state_writes.extend(entries)
        send(entries)

    config = request.runtime.config
    configurable = config["configurable"]
    config["configurable"] = {**configurable, _PREGEL_SEND_KEY: record_and_send}
    try:
        yield state_writes
    finally:
        config["configurable"] = configurable


def _resend_recorded_state_writes(request: ToolCallRequest, result: Any) -> None:
    if not _is_encoded_tool_result(result):
        return
    recorded_writes = result.get(_STATE_WRITES_KEY)
    if not recorded_writes:
        return
    send = _pregel_send(request)
    if send is None:
        raise RuntimeError(
            "The recorded LangGraph tool result updated graph state, but this "
            "replay has no LangGraph state to update."
        )
    send([(channel, update) for channel, update in recorded_writes])


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
        self._middleware: BitfabAgentMiddleware | None = None
        self._instrumented_classes: dict[type, type] = {}

    @property
    def middleware(self) -> BitfabAgentMiddleware:
        """LangChain agent middleware that makes each tool call replayable.

        Pass it to ``create_agent(middleware=[...])`` or
        ``create_deep_agent(middleware=[...])`` and run the agent through
        ``instrument()``. Each tool call the agent makes is recorded as a
        replayable span under the agent's ``tools`` step, the same as a
        ``ToolNode`` built with ``wrap_tool_call`` / ``awrap_tool_call``.

        Raises:
            ImportError: If ``langchain`` 1.0+ is not installed
        """
        if self._middleware is None:
            try:
                from bitfab.agent_middleware import BitfabAgentMiddleware
            except ImportError as err:
                raise _missing_package("langchain", _LANGCHAIN_INSTALL) from err

            self._middleware = BitfabAgentMiddleware(self)
        return self._middleware

    def _should_mock(self, tool_name: str) -> bool:
        if isinstance(self._mock_tools_on_replay, bool):
            return self._mock_tools_on_replay
        return tool_name in self._mock_tools_on_replay

    def instrument(self, graph: GraphT) -> GraphT:
        """Trace a compiled graph or agent as this trace function.

        Returns a copy of ``graph`` of the same type, so it can be used
        anywhere the graph can: called directly, nested as a node in another
        graph, or served by LangGraph Platform. Every way of running it
        (``invoke``, ``ainvoke``, ``stream``, ``astream``, ``batch``,
        ``stream_events``, ``astream_events``) attaches the Bitfab callback
        handler and records the run as a replayable root span carrying the
        graph input, with the final graph state as its output. Copies made
        with ``with_config`` or ``copy`` stay traced.

        When the graph has a checkpointer and the run has a ``thread_id``, the
        thread's checkpoint at the start of the run is recorded too, and
        replay runs against that checkpoint in memory instead of the
        graph's own checkpointer. Inside a ``trace()`` root, under any trace
        function key, the checkpoint is recorded on that trace's root, and any
        run of the graph during a replay uses an in-memory checkpointer.

        Replay a recorded run through any of its run methods, for example
        ``client.replay(key, agent.invoke)`` or ``client.replay(key,
        agent.astream)``; a streamed replay is drained and its result is the
        final graph state.

        Experimental: this API may change before it is stable.
        """
        from bitfab.langgraph_runs import instrument_graph

        return instrument_graph(self, graph)

    def create_invoker(self, graph: _LangGraphRunnable) -> Callable[..., Any]:
        """Deprecated alias for ``instrument(graph).invoke``. Warns once."""
        warn_once(
            "deprecated-create-invoker",
            "create_invoker(graph) is deprecated; use instrument(graph).invoke instead.",
        )
        return self.instrument(graph).invoke

    def create_async_invoker(
        self, graph: _LangGraphRunnable
    ) -> Callable[..., Awaitable[Any]]:
        """Deprecated alias for ``instrument(graph).ainvoke``. Warns once."""
        warn_once(
            "deprecated-create-async-invoker",
            "create_async_invoker(graph) is deprecated; use instrument(graph).ainvoke instead.",
        )
        return self.instrument(graph).ainvoke

    def create_deep_agent(
        self,
        *args: Any,
        middleware: Sequence[Any] = (),
        subagents: Sequence[Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Build a LangChain Deep Agents agent traced as this trace function.

        A drop-in for ``deepagents.create_deep_agent``: every argument is passed
        through unchanged, except that ``middleware`` and each declarative
        subagent's ``middleware`` gain this integration's ``middleware``, so the
        main agent's and its subagents' tool calls are replayable spans.
        Subagents given as a compiled ``runnable`` or a remote ``graph_id`` are
        passed through as they are. Returns the agent wrapped by
        ``instrument()``.

        Raises:
            ImportError: If ``deepagents`` is not installed
        """
        try:
            from deepagents import create_deep_agent
        except ImportError as err:
            raise _missing_package("deepagents", _DEEPAGENTS_INSTALL) from err

        return self.instrument(
            create_deep_agent(
                *args,
                middleware=self._with_middleware(middleware),
                subagents=self._with_subagent_middleware(subagents),
                **kwargs,
            )
        )

    def create_agent(
        self, *args: Any, middleware: Sequence[Any] = (), **kwargs: Any
    ) -> Any:
        """Build a LangChain ``create_agent`` agent traced as this trace function.

        A drop-in for ``langchain.agents.create_agent``: every argument is
        passed through unchanged, except that ``middleware`` gains this
        integration's ``middleware``. Returns the agent wrapped by
        ``instrument()``.

        Raises:
            ImportError: If ``langchain`` 1.0+ is not installed
        """
        try:
            from langchain.agents import create_agent
        except ImportError as err:
            raise _missing_package("langchain", _LANGCHAIN_INSTALL) from err

        return self.instrument(
            create_agent(*args, middleware=self._with_middleware(middleware), **kwargs)
        )

    def _with_middleware(self, middleware: Sequence[Any]) -> list[Any]:
        listed = list(middleware)
        return listed if self.middleware in listed else [*listed, self.middleware]

    def _with_subagent_middleware(
        self, subagents: Sequence[Any] | None
    ) -> list[Any] | None:
        if subagents is None:
            return None
        return [
            spec
            if "runnable" in spec or "graph_id" in spec
            else {
                **spec,
                "middleware": self._with_middleware(spec.get("middleware", ())),
            }
            for spec in subagents
        ]

    def _root_span(
        self, finalize: Callable[[Any], Any] | None = None
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        return self._client._integration_span(
            self._trace_function_key,
            name=self._trace_function_key,
            type="agent",
            finalize=finalize,
            instrumentation="langgraph",
        )

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

    def _tool_step_span_id(self, request: ToolCallRequest) -> str | None:
        stack_context = _active_span_context()
        if subtree.current_session() is not None or stack_context is None:
            return None
        config = getattr(getattr(request, "runtime", None), "config", None) or {}
        run_id = getattr(config.get("callbacks"), "parent_run_id", None)
        if run_id is None:
            return None
        return self.callback_handler._visible_span_id_in_trace(
            str(run_id), stack_context["trace_id"]
        )

    @contextmanager
    def _claimed_tool_call(
        self, request: ToolCallRequest, trace_id: str, tool_call_id: str
    ) -> Iterator[list[tuple[str, Any]]]:
        claimed = self.callback_handler._claimed_tool_calls
        claim = (trace_id, tool_call_id)
        claimed.add(claim)
        try:
            with _recording_state_writes(request) as state_writes:
                yield state_writes
        finally:
            claimed.discard(claim)

    def _recording_trace_id(self, tool_name: str) -> str | None:
        active_context = _active_span_context()
        if active_context is None:
            warn_once(
                f"langgraph-tool-call-outside-root:{self._trace_function_key}",
                f'tool call "{tool_name}" ran outside a Bitfab trace for '
                f'"{self._trace_function_key}", so it was not recorded as a '
                "replayable span. Run the agent through instrument(agent) and "
                "call invoke, ainvoke, stream, or astream on what it returns.",
            )
            return None
        return active_context["trace_id"]

    def _tool_span(
        self,
        request: ToolCallRequest,
        should_mock: bool,
        state_writes: list[tuple[str, Any]],
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        return self._client._integration_span(
            self._trace_function_key,
            name=request.tool_call["name"],
            type="function",
            capture_when="nested",
            mock_on_replay=should_mock,
            finalize=lambda value: _encode_tool_result_with_state_writes(
                value, state_writes
            ),
            instrumentation="langgraph",
            framework_parent_span_id=self._tool_step_span_id(request),
        )

    def _finish_tool_call(self, request: ToolCallRequest, result: Any) -> Any:
        _resend_recorded_state_writes(request, result)
        tool_call = request.tool_call
        return _revive_tool_override(result, tool_call["id"], tool_call["name"])

    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        """Intercept one synchronous call through ``ToolNode.wrap_tool_call``."""
        tool_call = request.tool_call
        tool_call_id = tool_call.get("id")
        should_mock = self._should_mock(tool_call["name"])
        self._assert_replay_tool_call_is_safe(
            tool_call["name"], tool_call_id, should_mock
        )
        trace_id = self._recording_trace_id(tool_call["name"])
        if not tool_call_id or trace_id is None:
            return handler(request)

        with self._claimed_tool_call(request, trace_id, tool_call_id) as state_writes:

            @self._tool_span(request, should_mock, state_writes)
            def execute(_args: dict[str, Any]) -> Any:
                return handler(request)

            result = execute(tool_call.get("args", {}))
        return self._finish_tool_call(request, result)

    async def awrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command]],
    ) -> ToolMessage | Command:
        """Intercept one asynchronous call through ``ToolNode.awrap_tool_call``."""
        tool_call = request.tool_call
        tool_call_id = tool_call.get("id")
        should_mock = self._should_mock(tool_call["name"])
        self._assert_replay_tool_call_is_safe(
            tool_call["name"], tool_call_id, should_mock
        )
        trace_id = self._recording_trace_id(tool_call["name"])
        if not tool_call_id or trace_id is None:
            return await handler(request)

        with self._claimed_tool_call(request, trace_id, tool_call_id) as state_writes:

            @self._tool_span(request, should_mock, state_writes)
            async def execute(_args: dict[str, Any]) -> Any:
                return await handler(request)

            result = await execute(tool_call.get("args", {}))
        return self._finish_tool_call(request, result)

    def wrap_invoke(self, fn: Callable[P, T]) -> Callable[P, T]:
        """Wrap the application function that invokes the compiled graph."""
        return self._root_span()(fn)
