import asyncio
import itertools
import time
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence
from contextlib import AsyncExitStack, aclosing, asynccontextmanager, suppress
from functools import lru_cache
from typing import TYPE_CHECKING, Any, cast

import langgraph.version
import langsmith
import structlog
from langchain_core.messages import (
    AIMessageChunk,
    # TODO: Remove explicit dependency
    BaseMessage,
    BaseMessageChunk,
    ToolMessageChunk,
    convert_to_messages,
    message_chunk_to_message,
)
from langgraph.constants import TAG_NOSTREAM
from langgraph.errors import (
    EmptyChannelError,
    EmptyInputError,
    GraphRecursionError,
    InvalidUpdateError,
)
from langgraph.pregel.debug import CheckpointPayload, TaskResultPayload
from langgraph.types import Command
from pydantic import ValidationError
from pydantic.v1 import ValidationError as ValidationErrorLegacy

from langgraph_api import __version__, agent_auth
from langgraph_api import _checkpointer as api_checkpointer
from langgraph_api import store as api_store
from langgraph_api.asyncio import ValueEvent, wait_if_not_done
from langgraph_api.command import keyed_by_interrupt_id, map_cmd
from langgraph_api.config import (
    FF_ASYNC_PUBLISH_QUEUE,
    LSD_PUBLISH_QUEUE_SIZE,
    RESUME_DRAINED_RUNS,
)
from langgraph_api.drain import mark_top_level
from langgraph_api.feature_flags import (
    IS_POSTGRES_OR_GRPC_BACKEND,
    TOOLS_STREAM_SUPPORT,
    UPDATES_NEEDED_FOR_INTERRUPTS,
    USE_DURABILITY,
    USE_RUNTIME_CONTEXT_API,
)
from langgraph_api.graph import get_graph
from langgraph_api.grpc.ops.runs import Runs as GrpcRuns
from langgraph_api.grpc.ops.runs import StreamPublishException
from langgraph_api.js.base import BaseRemotePregel
from langgraph_api.lifecycle import (
    HIDDEN_ERROR,
    LifecycleEvent,
    LifecycleFeed,
    SubgraphLifecycle,
)
from langgraph_api.metadata import HOST, USER_API_URL, current_plan, incr_nodes
from langgraph_api.metrics_otlp import (
    COUNTER_STREAMING_DATA_LOSS,
    GAUGE_PUBLISH_QUEUE_AVAILABILITY,
    HISTOGRAM_STREAM_DATA_SIZE,
    LATENCY_STREAM_PUBLISH,
    get_otlp_metrics_reporter,
)
from langgraph_api.schema import Run, StreamMode
from langgraph_api.serde import json_dumpb
from langgraph_api.stream_v2 import (
    astream_state_v2,
    is_v2_messages_chunk,
    normalize_protocol_event,
)
from langgraph_api.utils.config import run_in_executor
from langgraph_api.utils.uuids import uuid7

if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig

if IS_POSTGRES_OR_GRPC_BACKEND:
    from langgraph_api.grpc.ops import Runs
else:
    from langgraph_runtime.ops import Runs
from langgraph_api.tracing_session import run_tracing_replicas

logger = structlog.stdlib.get_logger(__name__)

# What each runtime's messages mode skips: Python's has honored only "nostream"
# since langgraph 0.6, while LangGraph.js tags "langsmith:nostream" and honors both.
NOSTREAM_TAGS = frozenset({TAG_NOSTREAM})
JS_NOSTREAM_TAGS = NOSTREAM_TAGS | {"langsmith:nostream"}
# The run join finds checkpoint markers by this prefix, so it must stay equal to the
# core's pubsub.CheckpointMarkerPrefix.
CHECKPOINT_MARKER_PREFIX = "ckpt:"
# langgraph's CONFIG_KEY_STRICT_RESUME, spelled out: older langgraph lacks it.
STRICT_RESUME_KEY = "__pregel_strict_resume"

# Python's `tools` payloads, renamed to the shape the v1 React hook parses (JS graphs
# already send it): (hook event, source field, field in the hook's event).
_HOOK_TOOL_EVENTS = {
    "tool-started": ("on_tool_start", "input", "input"),
    "tool-output-delta": ("on_tool_event", "delta", "data"),
    "tool-finished": ("on_tool_end", "output", "output"),
    "tool-error": ("on_tool_error", None, "error"),
}
_HOOK_EVENT_NAMES = frozenset(kind for kind, _, _ in _HOOK_TOOL_EVENTS.values())


def hide_js_task_error(task: Any) -> None:
    """Give a JS task result's error the shape serde gives a Python exception it hides.

    A JS error arrives as a plain value, which serde would send with its text.
    """
    if isinstance(task, dict) and task.get("error") is not None:
        task["error"] = HIDDEN_ERROR


def hook_tool_event(
    event: dict[str, Any], names: dict[str, str]
) -> dict[str, Any] | None:
    """A `tools` event in the v1 hook's shape, or None for a kind the hook throws on.

    A tool error's text can carry secrets, and its type isn't known here (a JS tool
    may throw a plain string), so every error is hidden. `names` keeps each call's
    tool name from its start, since only the start carries it in Python.
    """
    kind = event.get("event")
    if kind == "on_tool_error":
        return {**event, "error": HIDDEN_ERROR}
    if kind in _HOOK_EVENT_NAMES:
        return event
    if (renamed := _HOOK_TOOL_EVENTS.get(kind)) is None:
        return None
    hook_kind, source, target = renamed
    call_id = event["tool_call_id"]
    if hook_kind == "on_tool_start":
        names[call_id] = event.get("tool_name", "")
    value = event.get(source) if source else HIDDEN_ERROR
    return {
        "event": hook_kind,
        "toolCallId": call_id,
        "name": names.get(call_id, ""),
        target: value,
    }


async def _filter_context_by_schema(
    context: dict[str, Any], context_schema: dict | None
) -> dict[str, Any]:
    """Filter context parameters based on the context schema.

    Args:
        context: The context dictionary to filter
        context_schema: The JSON schema for valid context parameters

    Returns:
        Filtered context dictionary containing only valid parameters
    """
    if not context_schema or not context:
        return context

    # Extract valid properties from the schema
    properties = context_schema.get("properties", {})
    if not properties:
        return context

    # Filter context to only include parameters defined in the schema
    filtered_context = {}
    for key, value in context.items():
        if key in properties:
            filtered_context[key] = value
        else:
            await logger.adebug(
                f"Filtering out context parameter '{key}' not found in context schema",
                context_key=key,
                available_keys=list(properties.keys()),
            )

    return filtered_context


AnyStream = AsyncIterator[tuple[str, Any]]


def _preproces_debug_checkpoint_task(task: dict[str, Any]) -> dict[str, Any]:
    if (
        "state" not in task
        or not task["state"]
        or "configurable" not in task["state"]
        or not task["state"]["configurable"]
    ):
        return task

    task["checkpoint"] = task["state"]["configurable"]
    del task["state"]
    return task


def _preprocess_debug_checkpoint(
    payload: CheckpointPayload | None,
) -> dict[str, Any] | None:
    from langgraph_api.state import runnable_config_to_checkpoint  # noqa: PLC0415

    if not payload:
        return None

    # TODO: deprecate the `config`` and `parent_config`` fields
    return {
        **payload,
        "checkpoint": runnable_config_to_checkpoint(payload["config"]),
        "parent_checkpoint": runnable_config_to_checkpoint(
            payload.get("parent_config", None)
        ),
        "tasks": [_preproces_debug_checkpoint_task(t) for t in payload["tasks"]],
    }


def _record_debug_chunk(
    chunk: dict[str, Any],
    ns: Sequence[str] | None,
    on_checkpoint: Callable[[CheckpointPayload | None], None],
    on_task_result: Callable[[TaskResultPayload], None],
) -> str | None:
    """Returns the id of the root checkpoint the chunk reports, if it reports one."""
    # Only the root's events describe the thread; a subgraph's checkpoint would
    # become the thread's state at run end.
    if chunk["type"] == "checkpoint":
        chunk["payload"] = _preprocess_debug_checkpoint(chunk["payload"])
        if not ns:
            on_checkpoint(chunk["payload"])
            if chunk["payload"] and chunk["payload"]["checkpoint"]:
                return chunk["payload"]["checkpoint"]["checkpoint_id"]
    elif chunk["type"] == "task_result" and not ns:
        on_task_result(chunk["payload"])
    return None


@asynccontextmanager
async def async_tracing_context(*args, **kwargs):
    with langsmith.tracing_context(*args, **kwargs):
        yield


async def astream_state(
    run: Run,
    attempt: int,
    done: ValueEvent,
    *,
    on_checkpoint: Callable[[CheckpointPayload | None], None] = lambda _: None,
    on_task_result: Callable[[TaskResultPayload], None] = lambda _: None,
    control: Any | None = None,
    resume_from_checkpoint: bool = False,
    strict_resume: bool = False,
) -> AnyStream:
    """Stream messages from the runnable."""
    run_id = str(run["run_id"])
    # extract args from run
    kwargs = run["kwargs"].copy()
    kwargs.pop("webhook", None)
    kwargs.pop("resumable", None)
    kwargs.pop("strict_resume", None)
    if USE_DURABILITY:
        checkpoint_during = kwargs.pop("checkpoint_during")
        if not kwargs.get("durability") and checkpoint_during:
            kwargs["durability"] = "async" if checkpoint_during else "exit"
    else:
        durability = kwargs.pop("durability")
        if not kwargs.get("checkpoint_during") and durability in ("async", "exit"):
            kwargs["checkpoint_during"] = durability == "async"
    subgraphs = kwargs.get("subgraphs", False)
    temporary = kwargs.pop("temporary", False)
    context = kwargs.pop("context", None)
    config = cast("RunnableConfig", kwargs.pop("config"))
    configurable = config["configurable"]
    # Remove the internal marker before the graph receives or persists the configuration.
    context_provided_by_caller = configurable.pop("__context_provided__", False)
    # Before the graph loads, so a disabled agent's code never runs and the agent
    # never sees a caller's run_agent_identifier.
    config, context, run_agent_identifier = await agent_auth.verify_and_strip(
        config, context
    )
    configurable = config["configurable"]
    stack = AsyncExitStack()
    store = await api_store.get_store()
    checkpointer = None if temporary else await api_checkpointer.get_checkpointer()
    graph_load_start = time.perf_counter()
    graph = await stack.enter_async_context(
        get_graph(
            configurable["graph_id"],
            config,
            store=store,
            checkpointer=checkpointer,
            access_context="threads.create_run",
            run_id=run_id,
            context=context,
        )
    )
    graph_load_ms = round((time.perf_counter() - graph_load_start) * 1000, 2)

    # Filter context with the request's authentication context when the graph is remote.
    if context and USE_RUNTIME_CONTEXT_API:
        try:
            context_schema = (
                await graph.aget_context_jsonschema()
                if isinstance(graph, BaseRemotePregel)
                else graph.get_context_jsonschema()
            )
            filtered_context = await _filter_context_by_schema(context, context_schema)
            # Remove dropped keys from the mirrored configurable only when the caller supplied context.
            if context_provided_by_caller:
                for dropped_key in context.keys() - filtered_context.keys():
                    if configurable.get(dropped_key) == context[dropped_key]:
                        configurable.pop(dropped_key, None)
            context = filtered_context
        except Exception as e:
            await logger.adebug(
                f"Failed to get context schema for filtering: {e}", exc_info=e
            )

    input = kwargs.pop("input")
    if cmd := kwargs.pop("command"):
        input = map_cmd(cmd)
    is_remote_pregel = isinstance(graph, BaseRemotePregel)
    # Drains aren't implemented for JS graphs yet: the server doesn't forward
    # drain requests to the sidecar, so a JS graph's retries re-send the run's
    # input or command.
    if resume_from_checkpoint and not is_remote_pregel:
        # Continue where the run stopped: without its input (a Command would
        # apply twice) or its checkpoint pin (where it started).
        input = None
        # Copy: the config can be the stored run record's.
        configurable = {**configurable}
        config = {**config, "configurable": configurable}
        configurable.pop("checkpoint_id", None)
        configurable.pop("checkpoint_map", None)
    if strict_resume or STRICT_RESUME_KEY in configurable:
        # Copy: the config can be the stored run record's. Only the run's own
        # request turns the check on, never a key in a config it inherits.
        configurable = {k: v for k, v in configurable.items() if k != STRICT_RESUME_KEY}
        if strict_resume:
            configurable[STRICT_RESUME_KEY] = True
        config = {**config, "configurable": configurable}
    # A Command's first checkpoint keeps the id of the one it resumes but follows the
    # Command's update, so a join resumed after its marker would skip the update.
    skip_next_marker = isinstance(input, Command)
    stream_mode: list[StreamMode] = kwargs.pop("stream_mode")
    # Go maps unrecognized ``StreamMode`` enum values to ``unknown``; the
    # round-trip converts those to ``None``.
    stream_mode = [mode for mode in stream_mode if mode is not None]
    # Root checkpoint markers let a run's join skip what a client already
    # loaded. Only the Go core drops them before they reach clients. Under exit
    # durability no step is saved, and the JS loop and langgraph < 0.6 then report
    # every step under the last saved checkpoint's id. A JS graph's next step can send
    # its `events` starts and legacy `messages/metadata` before the checkpoint's event,
    # so a join after the marker would miss them; unmarked, such a join replays the run.
    mark_checkpoints = (
        IS_POSTGRES_OR_GRPC_BACKEND
        and kwargs.get("durability") != "exit"
        and kwargs.get("checkpoint_during") is not False
        and (not is_remote_pregel or {"events", "messages"}.isdisjoint(stream_mode))
    )
    feedback_keys = kwargs.pop("feedback_keys", None)
    stream_modes_set: set[StreamMode] = set(stream_mode) - {"events"}
    # This code path runs for every run, legacy and v2. The per-run
    # opt-in is the ``__event_streaming_v2`` configurable marker,
    # set only by the v2 endpoints (see ``event_streaming/service.py``). Once
    # set, the wire shape of ``messages`` events is incompatible with
    # v1 — v2 emits a single content-block-shaped ``event_dict`` under
    # mode ``messages``, while v1 emits ``messages/metadata`` plus
    # ``messages/partial``/``messages/complete`` with ``BaseMessage``
    # payloads — so the protocol contract is fixed for the lifetime
    # of the run. ``FF_V2_EVENT_STREAMING`` gates v2 *route
    # registration* in ``api/__init__.py``; we deliberately do not
    # re-check it here, because downgrading a queued run mid-flight
    # would break the v2 consumer that is already parsing v2-shaped
    # events from the same stream.
    event_streaming_v2_run = bool(configurable.get("__event_streaming_v2"))
    lifecycle_tasks: SubgraphLifecycle | None = None
    lifecycle_feed: LifecycleFeed | None = None
    if not event_streaming_v2_run:
        if "lifecycle" in stream_modes_set:
            if subgraphs:
                lifecycle_tasks = SubgraphLifecycle()
            elif is_remote_pregel:
                kwargs["lifecycle"] = True
            else:
                lifecycle_feed = LifecycleFeed()
        stream_modes_set.discard("lifecycle")
        if not (is_remote_pregel or TOOLS_STREAM_SUPPORT):
            stream_modes_set.discard("tools")
    elif is_remote_pregel:
        # Protocol v2 runs of a remote graph get neither mode: its v3 stream
        # doesn't implement them. ``capabilities.py`` documents this behavior,
        # so keep them in sync.
        stream_modes_set.discard("tools")
        stream_modes_set.discard("lifecycle")
    if "debug" not in stream_modes_set:
        stream_modes_set.add("debug")
    if "messages-tuple" in stream_modes_set and not is_remote_pregel:
        stream_modes_set.remove("messages-tuple")
        stream_modes_set.add("messages")
    if "updates" not in stream_modes_set and UPDATES_NEEDED_FOR_INTERRUPTS:
        stream_modes_set.add("updates")
        only_interrupt_updates = True
    else:
        only_interrupt_updates = False
    # attach attempt metadata
    config["metadata"]["run_attempt"] = attempt
    # attach langgraph metadata
    config["metadata"]["langgraph_version"] = langgraph.version.__version__
    config["metadata"]["langgraph_api_version"] = __version__
    config["metadata"]["langgraph_plan"] = current_plan()
    config["metadata"]["langgraph_host"] = HOST
    config["metadata"]["langgraph_api_url"] = USER_API_URL
    if run_agent_identifier:
        config["metadata"][agent_auth.RUN_AGENT_IDENTIFIER] = run_agent_identifier
    if not is_remote_pregel:
        # For remote (JS) graphs this would only time building the proxy, not
        # the sidecar's graph load.
        config["metadata"]["langgraph_graph_load_ms"] = graph_load_ms
        # attach node counter
        configurable["__pregel_node_finished"] = incr_nodes

    # attach run_id to config
    # for attempts beyond the first, use a fresh, unique run_id
    config = {**config, "run_id": run["run_id"]} if attempt == 1 else config
    # The events path matches the attempt's root chunks by run id. On the
    # first attempt that is the run's own id (set above); on later attempts
    # LangGraph generates a fresh one, so capture it from the root chain's
    # start event instead — writing it into the config would flow into
    # checkpoint metadata (run id lookups and LangGraph's own same-run
    # resume detection key on it) and break lookups by run. Only with
    # drained-run handling on (see the capture below): with the flag off,
    # later attempts' root_run_id stays None and root chunks are never
    # matched, exactly as on main.
    root_run_id: str | None = str(run["run_id"]) if attempt == 1 else None
    if lifecycle_feed:
        # Not `merge_configs`: it drops a `recursion_limit` equal to its own default, 25.
        config = {**config, "callbacks": [lifecycle_feed.listener]}
    tool_names: dict[str, str] = {}
    # set up state
    messages: dict[str, BaseMessageChunk] = {}
    # Protocol v2 runs against a remote (JS sidecar) graph drive the sidecar
    # through LangGraphJS's native v3 stream (``stream_protocol: "v3"``) so
    # protocol-aligned events (messages content blocks, tools, custom:*,
    # checkpoints) arrive ready to forward — no legacy ``on_chain_stream``
    # reconstruction. ``hasattr`` keeps any other ``BaseRemotePregel`` impl on
    # the legacy path. Legacy stream endpoints keep ``version="v2"``.
    use_remote_v3 = (
        event_streaming_v2_run
        and is_remote_pregel
        and hasattr(graph, "astream_protocol_events")
    )
    use_astream_events = (
        "events" in stream_mode or is_remote_pregel
    ) and not use_remote_v3
    use_stream_events_v3 = (
        event_streaming_v2_run and not use_astream_events and not is_remote_pregel
    )
    # Hand the run's control to the graph so a drain request stops it at the
    # next top-level step boundary (see ServerRunControl). Only native graphs
    # accept a control (langgraph >= 1.2); remote graphs run in the JS sidecar,
    # which the server cannot drain yet.
    if control is not None and not is_remote_pregel:
        mark_top_level(control)
        kwargs["control"] = control
    # A checkpoint join rebuilds this event in the core (afterMarker in
    # servers/stream.go), so its keys must match there.
    yield "metadata", {"run_id": run_id, "attempt": attempt}
    resume = cmd.get("resume") if cmd else None
    # Tells the thread's other clients which interrupts this run answers, before
    # the graph starts, so they stop offering them. A run continuing from its own
    # checkpoint (input None) doesn't send its command again.
    if input is not None and keyed_by_interrupt_id(resume):
        yield "interrupts", {"run_id": run_id, "answered": sorted(resume)}

    # If a langsmith tracing destination (project or agent) is specified, additionally pass it in to tracing context
    if replicas := run_tracing_replicas(configurable):
        await stack.enter_async_context(async_tracing_context(replicas=replicas))

    # stream run
    if use_astream_events:
        if USE_RUNTIME_CONTEXT_API:
            kwargs["context"] = context
        # JS graphs apply their output channels in the sidecar.
        if not is_remote_pregel:
            kwargs.setdefault("output_keys", graph.output_channels)
        graph_events = graph.astream_events(
            input,
            config,
            version="v2",
            stream_mode=list(stream_modes_set),
            **kwargs,
        )
        async with (
            stack,
            aclosing(
                lifecycle_feed.merge(graph_events) if lifecycle_feed else graph_events
            ) as stream,
        ):
            sentinel = object()
            while True:
                event = await wait_if_not_done(anext(stream, sentinel), done)
                if event is sentinel:
                    break
                if isinstance(event, LifecycleEvent):
                    yield event
                    continue
                event = cast("dict", event)
                if is_remote_pregel and event["event"] == "lifecycle":
                    # The sidecar's own listener, for JS runs without subgraphs.
                    namespace = event["data"]["namespace"]
                    yield f"lifecycle|{'|'.join(namespace)}", event["data"]
                    continue
                if event.get("tags") and "langsmith:hidden" in event["tags"]:
                    continue
                if (
                    "messages" in stream_mode
                    and isinstance(graph, BaseRemotePregel)
                    and event["event"] == "on_custom_event"
                    and event["name"]
                    in (
                        "messages/complete",
                        "messages/partial",
                        "messages/metadata",
                    )
                ):
                    yield event["name"], event["data"]
                # TODO support messages-tuple for js graphs
                # For JS (BaseRemotePregel) with subgraphs=True, subgraph events
                # carry the subgraph's own run_id. Accept them if the chunk is a
                # proper 3-tuple [ns, mode, chunk] — that's the sidecar's
                # normalized format. Limit this bypass to remote graphs only;
                # Python child events must fall through to the raw "events"
                # fallback below when the client requests stream_mode="events".
                _chunk_data = (
                    event["data"].get("chunk")
                    if event["event"] == "on_chain_stream"
                    else None
                )
                if (
                    root_run_id is None
                    and RESUME_DRAINED_RUNS
                    and not is_remote_pregel
                    and event["event"] == "on_chain_start"
                    and not event.get("parent_ids")
                ):
                    # Later attempts: the root chain's start event (no
                    # parents) reveals this attempt's root run id.
                    root_run_id = event["run_id"]
                if event["event"] == "on_chain_stream" and (
                    event["run_id"] == root_run_id
                    or (
                        subgraphs
                        and is_remote_pregel
                        and isinstance(_chunk_data, (list, tuple))
                        and len(_chunk_data) == 3
                    )
                ):
                    if subgraphs:
                        ns, mode, chunk = event["data"]["chunk"]
                    else:
                        mode, chunk = event["data"]["chunk"]
                        ns = None
                    if is_remote_pregel and mode in ("tasks", "debug"):
                        hide_js_task_error(
                            chunk["payload"] if mode == "debug" else chunk
                        )
                    # --- begin shared logic with astream ---
                    checkpoint_id = None
                    if mode == "debug":
                        checkpoint_id = _record_debug_chunk(
                            chunk, ns, on_checkpoint, on_task_result
                        )
                        if lifecycle_tasks and chunk["type"] != "checkpoint":
                            for lc_event in lifecycle_tasks.on_task(
                                tuple(ns), chunk["payload"]
                            ):
                                yield lc_event
                    if mode == "messages":
                        if event_streaming_v2_run and is_v2_messages_chunk(chunk):
                            event_dict, _meta = chunk
                            if subgraphs and ns:
                                yield f"messages|{'|'.join(ns)}", event_dict
                            else:
                                yield "messages", event_dict
                        elif (
                            not event_streaming_v2_run
                            and "messages-tuple" in stream_mode
                        ):
                            if subgraphs and ns:
                                yield f"messages|{'|'.join(ns)}", chunk
                            else:
                                yield "messages", chunk
                        elif not event_streaming_v2_run:
                            msg_, meta = cast(
                                "tuple[BaseMessage | dict, dict[str, Any]]", chunk
                            )
                            is_chunk = False
                            if isinstance(msg_, dict):
                                if (
                                    "chunk" in msg_.get("type", "").lower()
                                    or "chunk" in msg_.get("role", "").lower()
                                ):
                                    if "ai" in msg_.get("role", "").lower():
                                        msg = AIMessageChunk(**msg_)
                                    elif "tool" in msg_.get("role", "").lower():
                                        msg = ToolMessageChunk(**msg_)
                                    else:
                                        msg = BaseMessageChunk(**msg_)
                                    is_chunk = True
                                else:
                                    msg = convert_to_messages([msg_])[0]
                            else:
                                msg = msg_
                            if msg.id in messages:
                                messages[msg.id] += msg
                            else:
                                messages[msg.id] = msg
                                yield "messages/metadata", {msg.id: {"metadata": meta}}
                            yield (
                                (
                                    "messages/partial"
                                    if isinstance(msg, BaseMessageChunk)
                                    else "messages/complete"
                                ),
                                [
                                    (
                                        message_chunk_to_message(messages[msg.id])
                                        if not is_chunk
                                        else messages[msg.id]
                                    )
                                ],
                            )
                    elif mode in stream_mode or (
                        event_streaming_v2_run and mode in stream_modes_set
                    ):
                        # Forward natively-emitted ``tools`` / ``lifecycle``
                        # events for protocol v2 runs even when the client
                        # didn't explicitly request them — the session
                        # uses them for namespace registration and
                        # agent.getTree ordering.
                        if mode == "tools" and not event_streaming_v2_run:
                            chunk = hook_tool_event(chunk, tool_names)
                            if chunk is None:
                                continue
                        if subgraphs and ns:
                            yield f"{mode}|{'|'.join(ns)}", chunk
                        else:
                            yield mode, chunk
                    elif (
                        mode == "updates"
                        and isinstance(chunk, dict)
                        and "__interrupt__" in chunk
                        and len(chunk["__interrupt__"]) > 0
                        and only_interrupt_updates
                    ):
                        # If the interrupt doesn't have any actions (e.g. interrupt before or after a node is specified), we don't return the interrupt at all today.
                        if subgraphs and ns:
                            yield f"values|{'|'.join(ns)}", chunk
                        else:
                            yield "values", chunk
                    if mark_checkpoints and checkpoint_id:
                        if skip_next_marker:
                            skip_next_marker = False
                        else:
                            yield (
                                "control",
                                f"{CHECKPOINT_MARKER_PREFIX}{checkpoint_id}:{attempt}",
                            )
                    # --- end shared logic with astream ---
                elif "events" in stream_mode and (
                    JS_NOSTREAM_TAGS if is_remote_pregel else NOSTREAM_TAGS
                ).isdisjoint(event.get("tags") or ()):
                    yield "events", event
    elif use_stream_events_v3:
        async for ev in astream_state_v2(
            graph=graph,
            input=input,
            config=config,
            configurable=configurable,
            kwargs=kwargs,
            context=context,
            stack=stack,
            done=done,
            on_checkpoint=on_checkpoint,
            on_task_result=on_task_result,
        ):
            yield ev
    elif use_remote_v3:
        # Remote (JS) graph under Protocol v2: consume native v3
        # ProtocolEvents from the sidecar and forward them exactly like the
        # native-graph v3 path (``astream_state_v2``) does, so the
        # ``EventStreamingSession`` normalization is identical regardless of
        # graph language.
        if USE_RUNTIME_CONTEXT_API:
            kwargs["context"] = context
        async with (
            stack,
            aclosing(
                graph.astream_protocol_events(
                    input,
                    config,
                    stream_mode=list(stream_modes_set),
                    **kwargs,
                )
            ) as stream,
        ):
            sentinel = object()
            while True:
                event = await wait_if_not_done(anext(stream, sentinel), done)
                if event is sentinel:
                    break
                normalized = normalize_protocol_event(
                    cast("dict", event),
                    on_checkpoint=on_checkpoint,
                    on_task_result=on_task_result,
                )
                if normalized is not None:
                    yield normalized
    else:
        output_keys = kwargs.pop("output_keys", graph.output_channels)
        if USE_RUNTIME_CONTEXT_API:
            kwargs["context"] = context
        graph_chunks = graph.astream(
            input,
            config,
            stream_mode=list(stream_modes_set),
            output_keys=output_keys,
            **kwargs,
        )
        async with (
            stack,
            aclosing(
                lifecycle_feed.merge(graph_chunks) if lifecycle_feed else graph_chunks
            ) as stream,
        ):
            sentinel = object()
            while True:
                event = await wait_if_not_done(anext(stream, sentinel), done)
                if event is sentinel:
                    break
                if isinstance(event, LifecycleEvent):
                    yield event
                    continue
                if subgraphs:
                    ns, mode, chunk = cast("tuple[str, str, dict[str, Any]]", event)
                else:
                    mode, chunk = cast("tuple[str, dict[str, Any]]", event)
                    ns = None
                # --- begin shared logic with astream_events ---
                checkpoint_id = None
                if mode == "debug":
                    checkpoint_id = _record_debug_chunk(
                        chunk, ns, on_checkpoint, on_task_result
                    )
                    if lifecycle_tasks and chunk["type"] != "checkpoint":
                        for lc_event in lifecycle_tasks.on_task(
                            tuple(ns), chunk["payload"]
                        ):
                            yield lc_event
                if mode == "messages":
                    if event_streaming_v2_run and is_v2_messages_chunk(chunk):
                        event_dict, _meta = chunk
                        if subgraphs and ns:
                            yield f"messages|{'|'.join(ns)}", event_dict
                        else:
                            yield "messages", event_dict
                    elif not event_streaming_v2_run and "messages-tuple" in stream_mode:
                        if subgraphs and ns:
                            yield f"messages|{'|'.join(ns)}", chunk
                        else:
                            yield "messages", chunk
                    elif not event_streaming_v2_run:
                        msg_, meta = cast(
                            "tuple[BaseMessage | dict, dict[str, Any]]", chunk
                        )
                        is_chunk = False
                        if isinstance(msg_, dict):
                            if (
                                "chunk" in msg_.get("type", "").lower()
                                or "chunk" in msg_.get("role", "").lower()
                            ):
                                if "ai" in msg_.get("role", "").lower():
                                    msg = AIMessageChunk(**msg_)
                                elif "tool" in msg_.get("role", "").lower():
                                    msg = ToolMessageChunk(**msg_)
                                else:
                                    msg = BaseMessageChunk(**msg_)
                                is_chunk = True
                            else:
                                msg = convert_to_messages([msg_])[0]
                        else:
                            msg = msg_
                        if msg.id in messages:
                            messages[msg.id] += msg
                        else:
                            messages[msg.id] = msg
                            yield "messages/metadata", {msg.id: {"metadata": meta}}
                        yield (
                            (
                                "messages/partial"
                                if isinstance(msg, BaseMessageChunk)
                                else "messages/complete"
                            ),
                            [
                                (
                                    message_chunk_to_message(messages[msg.id])
                                    if not is_chunk
                                    else messages[msg.id]
                                )
                            ],
                        )
                elif mode in stream_mode or (
                    event_streaming_v2_run and mode in stream_modes_set
                ):
                    # Forward natively-emitted ``tools`` / ``lifecycle``
                    # events for protocol v2 runs even when the client
                    # didn't explicitly request them.
                    if mode == "tools" and not event_streaming_v2_run:
                        chunk = hook_tool_event(chunk, tool_names)
                        if chunk is None:
                            continue
                    if subgraphs and ns:
                        yield f"{mode}|{'|'.join(ns)}", chunk
                    else:
                        yield mode, chunk
                elif (
                    mode == "updates"
                    and isinstance(chunk, dict)
                    and "__interrupt__" in chunk
                    and len(chunk["__interrupt__"]) > 0
                    and only_interrupt_updates
                ):
                    # If the interrupt doesn't have any actions (e.g. interrupt before or after a node is specified), we don't return the interrupt at all today.
                    if subgraphs and ns:
                        yield f"values|{'|'.join(ns)}", chunk
                    else:
                        yield "values", chunk
                if mark_checkpoints and checkpoint_id:
                    if skip_next_marker:
                        skip_next_marker = False
                    else:
                        yield (
                            "control",
                            f"{CHECKPOINT_MARKER_PREFIX}{checkpoint_id}:{attempt}",
                        )
                # --- end shared logic with astream_events ---

    if is_remote_pregel:
        # increment the remote runs
        try:
            nodes_executed = await graph.fetch_nodes_executed()
            incr_nodes(None, incr=nodes_executed)
        except Exception as e:
            logger.warning(f"Failed to fetch nodes executed for {graph.graph_id}: {e}")
    else:
        await logger.adebug("Graph is not an instance of BaseRemotePregel")

    # Get feedback URLs
    if feedback_keys:
        feedback_urls = await run_in_executor(
            None, get_feedback_urls, run_id, feedback_keys
        )
        yield "feedback", feedback_urls


def get_stream_event_type(mode: str) -> str:
    return mode.split("|", maxsplit=1)[0]


def publish_event(
    run_id: str | uuid.UUID,
    mode: str,
    payload: bytes,
    *,
    thread_id: str | uuid.UUID,
    resumable: bool,
    publisher_id: str,
    seq: int,
) -> Awaitable[None]:
    """Publish one run event as event `seq` of publisher `publisher_id`.

    The Redis publish scripts drop a retried publish instead of adding it twice.
    Each consume call numbers its events under a fresh publisher id, so a
    re-executed run (a new consume call) is never mistaken for a retry of an
    earlier attempt; a single event, like the worker's terminal error, gets a
    publisher id of its own with seq 0.
    """
    if IS_POSTGRES_OR_GRPC_BACKEND:
        return GrpcRuns.Stream.publish(
            run_id,
            mode,
            payload,
            thread_id=thread_id,
            resumable=resumable,
            publisher_id=publisher_id,
            seq=seq,
        )
    # langgraph-runtime-inmem is a separate package whose publish takes no such
    # keywords, and its in-process publish never retries.
    return Runs.Stream.publish(
        run_id, mode, payload, thread_id=thread_id, resumable=resumable
    )


async def consume(
    stream: AnyStream,
    run_id: str | uuid.UUID,
    resumable: bool = False,
    stream_modes: set[StreamMode] | None = None,
    *,
    thread_id: str | uuid.UUID,
) -> None:
    reporter = get_otlp_metrics_reporter()
    stream_modes = stream_modes or set()
    if "messages-tuple" in stream_modes:
        stream_modes.add("messages")
    stream_modes.add("metadata")
    stream_modes.add("control")
    # No run stream carries it, but a resumed thread stream replays it.
    stream_modes.add("interrupts")

    if FF_ASYNC_PUBLISH_QUEUE:
        await _consume_async_queue(
            stream,
            run_id,
            resumable,
            stream_modes,
            thread_id=thread_id,
            reporter=reporter,
        )
    else:
        await _consume_inline(
            stream,
            run_id,
            resumable,
            stream_modes,
            thread_id=thread_id,
            reporter=reporter,
        )


async def _consume_inline(
    stream: AnyStream,
    run_id: str | uuid.UUID,
    resumable: bool,
    stream_modes: set[StreamMode],
    *,
    thread_id: str | uuid.UUID,
    reporter: Any,
) -> None:
    """Publish each stream event inline (synchronous with stream consumption).

    This preserves natural backpressure: each event must be published before the
    next one is consumed.
    """
    publisher_id = uuid7().hex
    seqs = itertools.count()
    publishing = True
    async with aclosing(stream):
        try:
            async for mode, payload in stream:
                if not publishing:
                    continue
                event_type = get_stream_event_type(mode)
                payload_bytes = await run_in_executor(None, json_dumpb, payload)
                is_resumable = resumable and event_type.split("/")[0] in stream_modes
                try:
                    with reporter.track_latency_ms(
                        LATENCY_STREAM_PUBLISH,
                        attributes={"stream_event_type": event_type},
                    ):
                        await publish_event(
                            run_id,
                            mode,
                            payload_bytes,
                            thread_id=thread_id,
                            resumable=is_resumable,
                            publisher_id=publisher_id,
                            seq=next(seqs),
                        )
                except StreamPublishException as e:
                    # Stop publishing for the rest of the run: transient errors
                    # were already retried for up to a minute, and retrying every
                    # later event would stall the graph again each time. The run
                    # still finishes, and the worker records its real outcome.
                    publishing = False
                    await logger.aerror(
                        "Stream publish failed, finishing the run without streaming",
                        run_id=str(run_id),
                        thread_id=str(thread_id),
                        error_type=type(e).__name__,
                        error=str(e),
                    )
                    reporter.inc_counter(COUNTER_STREAMING_DATA_LOSS)
                    continue
                reporter.record_histogram(
                    HISTOGRAM_STREAM_DATA_SIZE,
                    float(len(payload_bytes)),
                    attributes={"stream_event_type": event_type},
                )
        except Exception as e:
            if isinstance(e, ExceptionGroup):
                e = e.exceptions[0]
            raise e


async def _consume_async_queue(
    stream: AnyStream,
    run_id: str | uuid.UUID,
    resumable: bool,
    stream_modes: set[StreamMode],
    *,
    thread_id: str | uuid.UUID,
    reporter: Any,
) -> None:
    """Publish stream events via a background asyncio queue.

    Decouples stream consumption from publishing so that slow publishes don't
    block graph execution. Enable with FF_ASYNC_PUBLISH_QUEUE=true.
    """
    publish_queue: asyncio.Queue[tuple[str, bytes, str, bool] | object] = asyncio.Queue(
        maxsize=LSD_PUBLISH_QUEUE_SIZE
    )
    publish_sentinel = object()
    publisher_id = uuid7().hex
    seqs = itertools.count()

    async def _publish_worker() -> None:
        while True:
            item = await publish_queue.get()
            event_type = "unknown"
            try:
                if item is publish_sentinel:
                    return
                mode, payload_bytes, event_type, is_resumable = cast(
                    "tuple[str, bytes, str, bool]", item
                )
                with reporter.track_latency_ms(
                    LATENCY_STREAM_PUBLISH,
                    attributes={"stream_event_type": event_type},
                ):
                    await publish_event(
                        run_id,
                        mode,
                        payload_bytes,
                        thread_id=thread_id,
                        resumable=is_resumable,
                        publisher_id=publisher_id,
                        seq=next(seqs),
                    )
                reporter.record_histogram(
                    HISTOGRAM_STREAM_DATA_SIZE,
                    float(len(payload_bytes)),
                    attributes={"stream_event_type": event_type},
                )
            except Exception:
                await logger.aerror(
                    "Publish failed, skipping event",
                    run_id=str(run_id),
                    thread_id=str(thread_id),
                    stream_event_type=event_type,
                )
                reporter.inc_counter(
                    COUNTER_STREAMING_DATA_LOSS,
                    attributes={"stream_event_type": event_type},
                )
            finally:
                publish_queue.task_done()

    async def _enqueue(item: tuple[str, bytes, str, bool] | object) -> None:
        reporter.record_gauge(
            GAUGE_PUBLISH_QUEUE_AVAILABILITY,
            float(publish_queue.maxsize - publish_queue.qsize()),
        )
        await publish_queue.put(item)

    publisher_task = asyncio.create_task(_publish_worker())
    try:
        async with aclosing(stream):
            async for mode, payload in stream:
                event_type = get_stream_event_type(mode)
                payload_bytes = await run_in_executor(None, json_dumpb, payload)
                is_resumable = resumable and event_type.split("/")[0] in stream_modes
                await _enqueue((mode, payload_bytes, event_type, is_resumable))

    except Exception as e:
        if isinstance(e, ExceptionGroup):
            e = e.exceptions[0]
        raise e
    finally:
        with suppress(Exception):
            await _enqueue(publish_sentinel)
        if not publisher_task.done():
            await publisher_task


def get_feedback_urls(run_id: str, feedback_keys: list[str]) -> dict[str, str]:
    client = get_langsmith_client()
    tokens = client.create_presigned_feedback_tokens(run_id, feedback_keys)
    return {key: token.url for key, token in zip(feedback_keys, tokens, strict=False)}


@lru_cache(maxsize=1)
def get_langsmith_client() -> langsmith.Client:
    return langsmith.Client()


EXPECTED_ERRORS = (
    ValueError,
    InvalidUpdateError,
    GraphRecursionError,
    EmptyInputError,
    EmptyChannelError,
    ValidationError,
    ValidationErrorLegacy,
)
