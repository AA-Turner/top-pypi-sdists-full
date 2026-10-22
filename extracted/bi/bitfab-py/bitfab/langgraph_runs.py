"""Replayable root spans for LangGraph graph runs, recorded from inside the graph."""

from __future__ import annotations

import base64
import uuid
from collections.abc import AsyncIterator, Callable, Iterator
from contextlib import aclosing
from typing import TYPE_CHECKING, Any, ClassVar, TypeVar

from bitfab.client import (
    CurrentSpan,
    _active_root_span_key,
    _active_trace_function_key,
    _trace_root_span_context,
)
from bitfab.constants import (
    INTEGRATION_FIXTURES_KEY,
    STREAM_RESULT_KEY,
    _replay_context,
)
from bitfab.integration_fixture import (
    create_integration_fixture_context,
    has_integration_fixture,
)
from bitfab.langgraph import _OutermostRunOutput
from bitfab.langgraph_integration import (
    _encode_nested,
    _is_command,
    _is_encoded_tool_result,
    _revive_nested,
)

if TYPE_CHECKING:
    from bitfab.langgraph_integration import BitfabLangGraphIntegration

GraphT = TypeVar("GraphT")


def thread_fixture_name(trace_function_key: str) -> str:
    return f"langgraph-thread:{trace_function_key}"


_THREAD_CONFIG_KEYS = ("thread_id", "checkpoint_ns", "checkpoint_id")
_REPLAY_THREADS_KEY = "langgraph_replay_threads"


class _BitfabInstrumentedGraph:
    _bitfab_integration: ClassVar[BitfabLangGraphIntegration]
    _bitfab_base: ClassVar[type]

    def stream(
        self, input: Any, config: dict[str, Any] | None = None, **kwargs: Any
    ) -> Iterator[Any]:
        yield from _GraphRun(self, input, config, kwargs).stream()

    async def astream(
        self, input: Any, config: dict[str, Any] | None = None, **kwargs: Any
    ) -> AsyncIterator[Any]:
        async with aclosing(_GraphRun(self, input, config, kwargs).astream()) as chunks:
            async for chunk in chunks:
                yield chunk


def instrument_graph(integration: BitfabLangGraphIntegration, graph: GraphT) -> GraphT:
    base = getattr(type(graph), "_bitfab_base", type(graph))
    instrumented_class = integration._instrumented_classes.get(base)
    if instrumented_class is None:
        instrumented_class = type(
            base.__name__,
            (_BitfabInstrumentedGraph, base),
            {
                "_bitfab_integration": integration,
                "_bitfab_base": base,
                "__module__": base.__module__,
                "__qualname__": base.__qualname__,
            },
        )
        integration._instrumented_classes[base] = instrumented_class
    fields = {
        name: value for name, value in vars(graph).items() if name != "__orig_class__"
    }
    return instrumented_class(**fields)


def _encode_root_input(value: Any) -> Any:
    return _encode_nested(value) if _is_command(value) else value


def _revive_root_input(value: Any) -> Any:
    return _revive_nested(value, "") if _is_encoded_tool_result(value) else value


def _with_callbacks(
    config: dict[str, Any] | None, handlers: list[Any]
) -> dict[str, Any]:
    run_config = dict(config or {})
    callbacks = run_config.get("callbacks")
    if callbacks is None:
        run_config["callbacks"] = list(handlers)
    elif isinstance(callbacks, list):
        run_config["callbacks"] = [
            *callbacks,
            *(handler for handler in handlers if handler not in callbacks),
        ]
    else:
        manager = callbacks.copy()
        for handler in handlers:
            if handler not in manager.handlers:
                manager.add_handler(handler, inherit=True)
        run_config["callbacks"] = manager
    return run_config


def _with_configurable(
    config: dict[str, Any], values: dict[str, Any]
) -> dict[str, Any]:
    return {**config, "configurable": {**config.get("configurable", {}), **values}}


def _thread_config(config: dict[str, Any]) -> dict[str, Any]:
    configurable = config.get("configurable", {})
    return {
        key: configurable[key] for key in _THREAD_CONFIG_KEYS if key in configurable
    }


def _saving_checkpointer(graph: Any) -> Any:
    checkpointer = getattr(graph, "checkpointer", None)
    return None if checkpointer in (None, True, False) else checkpointer


def _serde() -> Any:
    from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

    return JsonPlusSerializer()


def _encode_typed(serde: Any, value: Any) -> list[str]:
    type_name, data = serde.dumps_typed(value)
    return [type_name, base64.b64encode(data).decode("ascii")]


def _decode_typed(serde: Any, value: list[str]) -> Any:
    return serde.loads_typed((value[0], base64.b64decode(value[1])))


def _unstored_delta_channels(graph: Any, checkpoint_tuple: Any) -> list[str]:
    try:
        from langgraph.channels.delta import DeltaChannel
    except ImportError:
        return []
    checkpoint = checkpoint_tuple.checkpoint
    return [
        name
        for name, spec in getattr(graph, "channels", {}).items()
        if isinstance(spec, DeltaChannel)
        and name in checkpoint["channel_versions"]
        and name not in checkpoint["channel_values"]
    ]


def _with_channel_values(
    checkpoint_tuple: Any, names: list[str], values: dict[str, Any]
) -> Any:
    checkpoint = checkpoint_tuple.checkpoint
    return checkpoint_tuple._replace(
        checkpoint={
            **checkpoint,
            "channel_values": {
                **checkpoint["channel_values"],
                **{name: values[name] for name in names if name in values},
            },
        }
    )


def _self_contained(graph: Any, checkpoint_tuple: Any) -> Any:
    if checkpoint_tuple is None:
        return None
    names = _unstored_delta_channels(graph, checkpoint_tuple)
    if not names:
        return checkpoint_tuple
    state = graph.get_state(checkpoint_tuple.config)
    return _with_channel_values(checkpoint_tuple, names, state.values)


async def _aself_contained(graph: Any, checkpoint_tuple: Any) -> Any:
    if checkpoint_tuple is None:
        return None
    names = _unstored_delta_channels(graph, checkpoint_tuple)
    if not names:
        return checkpoint_tuple
    state = await graph.aget_state(checkpoint_tuple.config)
    return _with_channel_values(checkpoint_tuple, names, state.values)


def _encode_checkpoint(checkpoint_tuple: Any) -> dict[str, Any] | None:
    if checkpoint_tuple is None:
        return None
    serde = _serde()
    return {
        "config": _thread_config(checkpoint_tuple.config),
        "checkpoint": _encode_typed(serde, checkpoint_tuple.checkpoint),
        "metadata": _encode_typed(serde, checkpoint_tuple.metadata),
        "pendingWrites": [
            [task_id, channel, _encode_typed(serde, value)]
            for task_id, channel, value in checkpoint_tuple.pending_writes or []
        ],
    }


def _restored_checkpointer(
    recorded: dict[str, Any] | None,
) -> tuple[Any, dict[str, Any]]:
    from langgraph.checkpoint.memory import InMemorySaver

    saver = InMemorySaver()
    if not recorded:
        return saver, {}
    serde = _serde()
    thread = recorded["config"]
    checkpoint = _decode_typed(serde, recorded["checkpoint"])
    saved = saver.put(
        {
            "configurable": {
                "thread_id": thread["thread_id"],
                "checkpoint_ns": thread.get("checkpoint_ns", ""),
            }
        },
        checkpoint,
        _decode_typed(serde, recorded["metadata"]),
        checkpoint.get("channel_versions", {}),
    )
    writes_by_task: dict[str, list[tuple[str, Any]]] = {}
    for task_id, channel, value in recorded["pendingWrites"]:
        writes_by_task.setdefault(task_id, []).append(
            (channel, _decode_typed(serde, value))
        )
    for task_id, writes in writes_by_task.items():
        saver.put_writes(saved, writes, task_id)
    return saver, thread


class _GraphRun:
    def __init__(
        self,
        graph: _BitfabInstrumentedGraph,
        input: Any,
        config: dict[str, Any] | None,
        kwargs: dict[str, Any],
    ) -> None:
        self.graph = graph
        self.integration = type(graph)._bitfab_integration
        self.input = input
        self.kwargs = kwargs
        self.final_state = _OutermostRunOutput()
        self.config = _with_callbacks(
            config, [self.integration.callback_handler, self.final_state]
        )
        key = self.integration._trace_function_key
        self.opens_root = _active_trace_function_key() != key
        self.replaying = _replay_context.get() is not None
        self.reports_stream_result = (
            self.replaying and not self.opens_root and _active_root_span_key() == key
        )

    def _root_span(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        return self.integration._root_span(lambda _chunks: self.final_state.output)(fn)

    @property
    def _fixture_name(self) -> str:
        return thread_fixture_name(self.integration._trace_function_key)

    def _report_stream_result(self) -> None:
        replay_context = _replay_context.get()
        if self.reports_stream_result and replay_context is not None:
            replay_context[STREAM_RESULT_KEY] = self.final_state.output

    def _recorded_checkpoint(self) -> dict[str, Any] | None:
        replay_context = _replay_context.get() or {}
        fixtures = replay_context.get(INTEGRATION_FIXTURES_KEY) or {}
        return fixtures.get(self._fixture_name)

    def _replay_thread(self) -> tuple[Any, dict[str, Any]]:
        replay_context = _replay_context.get()
        threads = (
            replay_context.setdefault(_REPLAY_THREADS_KEY, {})
            if replay_context is not None
            else {}
        )
        if self._fixture_name not in threads:
            saver, thread = _restored_checkpointer(self._recorded_checkpoint())
            values = {
                key: thread[key]
                for key in ("thread_id", "checkpoint_ns")
                if key in thread
            } or {
                "thread_id": self.config.get("configurable", {}).get(
                    "thread_id", f"bitfab-replay-{uuid.uuid4()}"
                )
            }
            threads[self._fixture_name] = (saver, values)
        return threads[self._fixture_name]

    def _run_target(self) -> tuple[Any, dict[str, Any]]:
        if not self.replaying or _saving_checkpointer(self.graph) is None:
            return self.graph, self.config
        saver, values = self._replay_thread()
        replay_graph = self.graph.copy({"checkpointer": saver})  # type: ignore[attr-defined]
        return replay_graph, _with_configurable(self.config, values)

    def _base_on(self, graph: Any, method: str) -> Callable[..., Any]:
        return getattr(type(self.graph)._bitfab_base, method).__get__(graph)

    def _thread_to_record(
        self, graph: Any, config: dict[str, Any]
    ) -> tuple[Any, dict[str, Any], dict[str, Any]] | None:
        checkpointer = _saving_checkpointer(graph)
        thread = _thread_config(config)
        root = _trace_root_span_context()
        if (
            checkpointer is None
            or "thread_id" not in thread
            or root is None
            or has_integration_fixture(root, self._fixture_name)
        ):
            return None
        return checkpointer, {"configurable": thread}, root

    def _add_checkpoint_fixture(self, root: Any, checkpoint_tuple: Any) -> None:
        encoded = _encode_checkpoint(checkpoint_tuple)
        if not has_integration_fixture(root, self._fixture_name):
            CurrentSpan(root).add_context(
                create_integration_fixture_context(self._fixture_name, encoded)
            )

    def _record_checkpoint(self, graph: Any, config: dict[str, Any]) -> None:
        to_record = self._thread_to_record(graph, config)
        if to_record is not None:
            checkpointer, thread_config, root = to_record
            self._add_checkpoint_fixture(
                root, _self_contained(graph, checkpointer.get_tuple(thread_config))
            )

    async def _arecord_checkpoint(self, graph: Any, config: dict[str, Any]) -> None:
        to_record = self._thread_to_record(graph, config)
        if to_record is not None:
            checkpointer, thread_config, root = to_record
            self._add_checkpoint_fixture(
                root,
                await _aself_contained(
                    graph, await checkpointer.aget_tuple(thread_config)
                ),
            )

    def stream(self) -> Iterator[Any]:
        def run(root_input: Any) -> Iterator[Any]:
            graph, config = self._run_target()
            self._record_checkpoint(graph, config)
            yield from self._base_on(graph, "stream")(
                _revive_root_input(root_input), config, **self.kwargs
            )
            self._report_stream_result()

        if self.opens_root:
            yield from self._root_span(run)(_encode_root_input(self.input))
        else:
            yield from run(self.input)

    async def astream(self) -> AsyncIterator[Any]:
        async def run(root_input: Any) -> AsyncIterator[Any]:
            graph, config = self._run_target()
            await self._arecord_checkpoint(graph, config)
            async with aclosing(
                self._base_on(graph, "astream")(
                    _revive_root_input(root_input), config, **self.kwargs
                )
            ) as chunks:
                async for chunk in chunks:
                    yield chunk
            self._report_stream_result()

        chunks = (
            self._root_span(run)(_encode_root_input(self.input))
            if self.opens_root
            else run(self.input)
        )
        async with aclosing(chunks) as opened:
            async for chunk in opened:
                yield chunk
