"""WorkflowAPIChannel — Channel backed by a Workflows API event stream.

Forwards JSON patches from the Workflows API task() events as
TaskStateUpdateEvent messages. The Workflows SDK computes patches
internally, so the channel is mostly a forwarder plus child-event
rerouting.

Child workflow streaming: when the executor dispatches a child workflow,
it emits a ``child_mapping`` event with ``child_exec_id`` and ``prefix``.
That prefix is relative to the emitting parent workflow, not necessarily
to the root workflow. The channel combines workflow stream context
(``workflow_exec_id`` / ``parent_workflow_exec_id``) with those mapping
events to rebuild the execution tree, compute root-relative prefixes, and
reroute child patches into the consumer's single root state. Child events
that arrive before enough ancestry is known are buffered and replayed once
they can be attached.

Pipeline architecture
=====================

Event processing is split into independently testable layers:

1. ``_raw_events(start_seq)`` — single-connection parse loop
2. ``_reconnecting_events()`` — wraps ``_raw_events`` with reconnection/backoff
3. ``_ExecutionTreeTracker`` — execution tree + prefix resolution + state rerouting
4. ``__aiter__`` — thin classify/route/yield with observability

State machine
=============

::

  Event Type                    Payload           Action
  ──────────────────────────────────────────────────────────────────
  CUSTOM_TASK_STARTED           json              diff(state, snapshot) → patches
  CUSTOM_TASK_STARTED           child_mapping     record child_exec_id → parent-relative prefix
  CUSTOM_TASK_STARTED           callback_request  yield CallbackCallEvent
  CUSTOM_TASK_IN_PROGRESS       json_patch        deserialize → patches
  CUSTOM_TASK_COMPLETED         json              diff(state, snapshot) → patches
  WORKFLOW_EXECUTION_COMPLETED  —                 load terminal state → TaskResultEvent
  WORKFLOW_EXECUTION_FAILED     —                 load terminal state → TaskResultEvent
  WORKFLOW_EXECUTION_CANCELED   —                 load terminal state → TaskResultEvent
"""

import asyncio
import contextlib
import inspect
import time
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

import structlog
from mistralai.client.workflows import Workflows
from pydantic import BaseModel, ConfigDict, TypeAdapter
from structlog.contextvars import bound_contextvars

from mistralai.vibe.sdk.execution_record.patching.json_patch import apply_patches, reroute_patches
from mistralai.vibe.sdk.execution_record.patching.produce import diff
from mistralai.vibe.sdk.execution_record.patching.types import Op
from mistralai.vibe.sdk.execution_record.pointers import join_pointers, split_pointer
from mistralai.vibe.sdk.execution_record.state import PendingOutput, TaskState
from mistralai.vibe.sdk.transports.channel import Channel
from mistralai.vibe.sdk.transports.events import (
    CallbackCallEvent,
    CallbackResultEvent,
    DownstreamMessage,
    TaskResultEvent,
    TaskResultPayload,
    TaskStateUpdateEvent,
    TaskStateUpdatePayload,
    UpstreamMessage,
)

logger = structlog.get_logger()


class _WorkflowEventType(StrEnum):
    CUSTOM_TASK_STARTED = "CUSTOM_TASK_STARTED"
    CUSTOM_TASK_IN_PROGRESS = "CUSTOM_TASK_IN_PROGRESS"
    CUSTOM_TASK_COMPLETED = "CUSTOM_TASK_COMPLETED"
    WORKFLOW_EXECUTION_COMPLETED = "WORKFLOW_EXECUTION_COMPLETED"
    WORKFLOW_EXECUTION_FAILED = "WORKFLOW_EXECUTION_FAILED"
    WORKFLOW_EXECUTION_CANCELED = "WORKFLOW_EXECUTION_CANCELED"


class _ExecutionStatus(StrEnum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
    TERMINATED = "TERMINATED"
    TIMED_OUT = "TIMED_OUT"


class _CustomTaskType(StrEnum):
    CHILD_MAPPING = "child_mapping"
    CALLBACK_REQUEST = "callback_request"


class _PayloadType(StrEnum):
    JSON = "json"
    JSON_PATCH = "json_patch"


_TERMINAL_EVENT_TYPES = (
    _WorkflowEventType.WORKFLOW_EXECUTION_COMPLETED,
    _WorkflowEventType.WORKFLOW_EXECUTION_FAILED,
    _WorkflowEventType.WORKFLOW_EXECUTION_CANCELED,
)

_TERMINAL_EXECUTION_STATUSES = {
    _ExecutionStatus.COMPLETED,
    _ExecutionStatus.FAILED,
    _ExecutionStatus.CANCELED,
    _ExecutionStatus.TERMINATED,
    _ExecutionStatus.TIMED_OUT,
}


class _SignalPayload(BaseModel):
    """Wrapper for client.signal_workflow which requires a BaseModel."""

    payload: dict[str, Any]


# TypeAdapter for deserializing SDK patch dicts into our Op union.
_op_list_adapter: TypeAdapter[list[Op]] = TypeAdapter(list[Op])


def _deserialize_patches(raw: list[Any]) -> list[Op]:
    """Deserialize SDK JSONPatch dicts into vibe_sdk Op types."""
    return _op_list_adapter.validate_python(raw)


# ---------------------------------------------------------------------------
# Typed event models for NATS stream parsing
# ---------------------------------------------------------------------------


class _EventPayload(BaseModel):
    """Payload inside a Workflows API task event attributes."""

    model_config = ConfigDict(extra="ignore")
    type: str = ""
    value: Any = None


class _EventAttributes(BaseModel):
    """Attributes of a Workflows API task event."""

    model_config = ConfigDict(extra="ignore")
    custom_task_type: str = ""
    payload: _EventPayload = _EventPayload()


class _TaskEventData(BaseModel):
    """Top-level event data from the Workflows API NATS stream."""

    model_config = ConfigDict(extra="ignore")
    event_type: str = ""
    attributes: _EventAttributes = _EventAttributes()


class _ChildMapping(BaseModel):
    """Child workflow → parent prefix mapping, emitted by the executor."""

    child_exec_id: str = ""
    prefix: str = ""


# ---------------------------------------------------------------------------
# _ParsedEvent — typed wrapper for stream events
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _ParsedEvent:
    """Parsed and enriched event from the NATS stream."""

    event: _TaskEventData
    exec_id: str | None
    parent_exec_id: str | None
    root_exec_id: str | None
    broker_seq: int | None


# ---------------------------------------------------------------------------
# _ExecutionTreeTracker — execution tree state management
# ---------------------------------------------------------------------------


@dataclass
class _ExecutionNode:
    """Execution-local routing metadata used by the channel."""

    exec_id: str
    parent_exec_id: str | None = None
    relative_prefix: str | None = None
    absolute_prefix: str | None = None
    state: TaskState | None = None


@dataclass(frozen=True)
class _BufferedPayload:
    """A detached child payload waiting for enough ancestry to reroute."""

    exec_id: str
    payload: _EventPayload


@dataclass
class _ExecutionTreeTracker:
    """Tracks workflow execution ancestry, prefixes, and per-exec local state.

    The channel exposes a single root ``TaskState`` to consumers. Internally we
    keep one local ``TaskState`` per workflow execution and an execution tree
    rooted at the workflow the channel was opened on.
    """

    root_exec_id: str
    _nodes: dict[str, _ExecutionNode] = field(default_factory=dict)
    _buffered_payloads: list[_BufferedPayload] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._nodes[self.root_exec_id] = _ExecutionNode(
            exec_id=self.root_exec_id,
            absolute_prefix="",
        )

    def observe_execution(self, exec_id: str, parent_exec_id: str | None) -> None:
        """Record ancestry from stream context when present."""
        node = self._node(exec_id)
        if parent_exec_id is not None and node.parent_exec_id != parent_exec_id:
            node.parent_exec_id = parent_exec_id
        self._resolve_prefixes()

    def register_child(
        self,
        *,
        parent_exec_id: str,
        child_exec_id: str,
        prefix: str,
    ) -> None:
        """Record a parent-relative child mapping emitted by a workflow."""
        child = self._node(child_exec_id)
        child.parent_exec_id = parent_exec_id
        child.relative_prefix = prefix
        self._resolve_prefixes()
        logger.info(
            "channel.child_registered",
            child_exec_id=child_exec_id,
            prefix=prefix,
            parent_exec_id=parent_exec_id,
            absolute_prefix=child.absolute_prefix,
        )

    def is_child(self, exec_id: str) -> bool:
        return self._absolute_prefix(exec_id) is not None

    def stash(self, exec_id: str, payload: _EventPayload) -> None:
        self._buffered_payloads.append(_BufferedPayload(exec_id=exec_id, payload=payload))
        logger.debug(
            "channel.child_buffered",
            child_exec_id=exec_id,
            buffered_count=len(self._buffered_payloads),
        )

    def reroute(
        self,
        exec_id: str,
        payload: _EventPayload,
        parent_state: TaskState,
    ) -> list[Op] | None:
        """Reroute a child execution payload into root-relative parent scope.

        Returns rerouted patches, or None if no patches were produced.
        """
        prefix = self._absolute_prefix(exec_id)
        if prefix is None:
            return None
        node = self._node(exec_id)
        if node.state is None:
            node.state = _extract_child_state(parent_state, prefix)
        child_state = node.state

        patches = _extract_patches_from_payload(payload, child_state)
        if not patches:
            return None

        rerouted = reroute_patches(patches, prefix)
        node.state = apply_patches(child_state, patches)
        self._sync_ancestor_states(exec_id, patches, parent_state)
        return rerouted

    def drain_ready(self, parent_state: TaskState) -> list[Op]:
        """Replay buffered payloads whose ancestry/prefix is now known."""
        if not self._buffered_payloads:
            return []
        rerouted: list[Op] = []
        while True:
            progressed = False
            remaining: list[_BufferedPayload] = []
            for item in self._buffered_payloads:
                if not self.is_child(item.exec_id):
                    remaining.append(item)
                    continue
                progressed = True
                if patches := self.reroute(item.exec_id, item.payload, parent_state):
                    rerouted.extend(patches)
            self._buffered_payloads = remaining
            if not progressed:
                return rerouted

    def _node(self, exec_id: str) -> _ExecutionNode:
        return self._nodes.setdefault(exec_id, _ExecutionNode(exec_id=exec_id))

    def _absolute_prefix(self, exec_id: str) -> str | None:
        if exec_id == self.root_exec_id:
            return None
        node = self._nodes.get(exec_id)
        if node is None:
            return None
        return node.absolute_prefix

    def _resolve_prefixes(self) -> None:
        """Compute root-relative prefixes for newly attached child executions."""
        changed = True
        while changed:
            changed = False
            for node in self._nodes.values():
                if node.exec_id == self.root_exec_id or node.absolute_prefix is not None:
                    continue
                if node.parent_exec_id is None or node.relative_prefix is None:
                    continue
                parent_prefix = ""
                if node.parent_exec_id != self.root_exec_id:
                    parent_prefix = self._absolute_prefix(node.parent_exec_id) or ""
                    if not parent_prefix:
                        continue
                node.absolute_prefix = join_pointers(parent_prefix, node.relative_prefix)
                changed = True
                logger.debug(
                    "channel.child_attached",
                    child_exec_id=node.exec_id,
                    parent_exec_id=node.parent_exec_id,
                    absolute_prefix=node.absolute_prefix,
                )

    def _sync_ancestor_states(
        self,
        exec_id: str,
        child_patches: list[Op],
        root_state: TaskState,
    ) -> None:
        """Apply child-local patches into ancestor local states.

        This keeps parent execution snapshots in sync with descendant updates so
        later parent STARTED/COMPLETED snapshots diff against the up-to-date
        embedded child subtree instead of re-emitting it.
        """
        current_exec_id = exec_id
        current_patches = child_patches
        while True:
            current = self._nodes.get(current_exec_id)
            if current is None or current.parent_exec_id is None or current.relative_prefix is None:
                return
            if current.parent_exec_id == self.root_exec_id:
                return

            parent = self._node(current.parent_exec_id)
            if parent.absolute_prefix is None:
                return
            if parent.state is None:
                parent.state = _extract_child_state(root_state, parent.absolute_prefix)

            current_patches = reroute_patches(current_patches, current.relative_prefix)
            parent.state = apply_patches(parent.state, current_patches)
            current_exec_id = parent.exec_id


# ---------------------------------------------------------------------------
# Standalone helpers
# ---------------------------------------------------------------------------


def _extract_child_state(parent_state: TaskState, prefix: str) -> TaskState:
    """Extract the child's TaskState from the parent state at prefix path.

    Falls back to a minimal empty state if the path can't be resolved.
    """
    parts = split_pointer(prefix)
    obj: Any = parent_state
    for part in parts:
        if isinstance(obj, list):
            try:
                obj = obj[int(part)]
            except (ValueError, IndexError):
                return TaskState(id="unknown", input=None, output=PendingOutput())
        elif hasattr(obj, part):
            obj = getattr(obj, part)
        elif isinstance(obj, dict):
            obj = obj.get(part)
        else:
            return TaskState(id="unknown", input=None, output=PendingOutput())
    if isinstance(obj, TaskState):
        return obj
    return TaskState(id="unknown", input=None, output=PendingOutput())


def _extract_patches_from_payload(payload: _EventPayload, ref_state: TaskState) -> list[Op]:
    """Extract patches from a typed event payload.

    json_patch payloads are deserialized directly.
    json payloads are diffed against ref_state to produce patches.
    """
    if payload.type == _PayloadType.JSON_PATCH:
        if not isinstance(payload.value, list) or not payload.value:
            return []
        return _deserialize_patches(payload.value)

    if payload.type == _PayloadType.JSON:
        if not isinstance(payload.value, dict):
            return []
        try:
            snapshot = TaskState.model_validate(payload.value)
        except Exception:
            logger.warning("channel.invalid_snapshot", payload_type=payload.type)
            return []
        return list(diff(ref_state, snapshot))

    return []


def _project_workflow_history_update(
    state: TaskState, patches: list[Op] | None
) -> tuple[TaskState, TaskStateUpdateEvent | None]:
    if not patches:
        return state, None

    new_state = apply_patches(state, patches)
    public_patches = list(diff(state.history, new_state.history, "/history"))
    if not public_patches:
        return new_state, None

    return new_state, TaskStateUpdateEvent(
        payload=TaskStateUpdatePayload(task_id=new_state.id, patches=public_patches)
    )


# ---------------------------------------------------------------------------
# WorkflowAPIChannel
# ---------------------------------------------------------------------------


class WorkflowAPIChannel(Channel):
    """Channel backed by a NATS subscription on a running Workflows API workflow.

    Tracks state internally to compute diffs from full-state snapshots
    (STARTED/COMPLETED events) and forwards SDK-computed patches
    (IN_PROGRESS events) directly.

    Usage:
        channel = WorkflowAPIChannel(client, exec_id, initial_state)
        async for message in channel:
            apply_patches(state, message.payload.patches)
    """

    def __init__(
        self,
        client: Workflows,
        exec_id: str,
        initial_state: TaskState,
    ) -> None:
        self._client = client
        self._exec_id = exec_id
        self._state = initial_state

    async def _raw_events(self, start_seq: int) -> AsyncIterator[_ParsedEvent]:
        """Yield parsed events from a single stream connection."""
        stream_result = self._client.events.get_stream_events_async(
            **self._make_stream_query(start_seq)
        )
        stream = await stream_result if inspect.isawaitable(stream_result) else stream_result
        try:
            async for event in stream:
                data = self._get_event_data(event)
                if not isinstance(data, dict):
                    logger.debug(
                        "channel.non_dict_event",
                        data_type=type(data).__name__,
                        stream=getattr(event, "stream", ""),
                    )
                    continue
                parsed = _TaskEventData.model_validate(data)
                yield _ParsedEvent(
                    event=parsed,
                    exec_id=self._get_event_exec_id(event),
                    parent_exec_id=self._get_event_parent_exec_id(event),
                    root_exec_id=self._get_event_root_exec_id(event),
                    broker_seq=self._get_broker_sequence(event),
                )
        finally:
            closer = getattr(stream, "aclose", None)
            if callable(closer):
                with contextlib.suppress(Exception):
                    result = closer()
                    if inspect.isawaitable(result):
                        await result

    async def _reconnecting_events(self) -> AsyncIterator[_ParsedEvent]:
        """Yield events with automatic reconnection on stream errors.

        Tracks broker sequence for resume-from-last-seen. On stream close
        or error, checks whether the workflow has already terminated before
        reconnecting.
        """
        next_seq = 0
        reconnect_attempt = 0
        while True:
            try:
                async for item in self._raw_events(next_seq):
                    reconnect_attempt = 0
                    if item.broker_seq is not None:
                        next_seq = item.broker_seq + 1
                    yield item
                logger.warning("channel.stream_closed", next_seq=next_seq)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.warning(
                    "channel.stream_error",
                    error=str(exc),
                    next_seq=next_seq,
                )

            if await self._execution_has_terminated():
                logger.info("channel.terminal_polled", next_seq=next_seq)
                return

            reconnect_attempt += 1
            delay = min(0.25 * (2 ** (reconnect_attempt - 1)), 5.0)
            logger.info(
                "channel.reconnect",
                attempt=reconnect_attempt,
                delay=delay,
                next_seq=next_seq,
            )
            await asyncio.sleep(delay)

    # --- Pipeline layer 3: __aiter__ — classify/route/yield ---

    async def __aiter__(self) -> AsyncIterator[DownstreamMessage]:
        with bound_contextvars(exec_id=self._exec_id):
            t0 = time.monotonic()
            event_count = 0
            logger.info("channel.start")
            tracker = _ExecutionTreeTracker(root_exec_id=self._exec_id)

            async for item in self._reconnecting_events():
                event_count += 1
                parsed = item.event
                if item.exec_id is not None:
                    tracker.observe_execution(item.exec_id, item.parent_exec_id)

                if parsed.event_type in _TERMINAL_EVENT_TYPES:
                    if item.exec_id is None or item.exec_id == self._exec_id:
                        if terminal_state := await self._load_terminal_state():
                            self._state = terminal_state
                        logger.info(
                            "channel.terminal",
                            event_type=parsed.event_type,
                            total_events=event_count,
                        )
                        yield TaskResultEvent(
                            payload=TaskResultPayload(task_id=self._state.id, result=self._state)
                        )
                        return
                    logger.debug(
                        "channel.child_terminal",
                        child_exec_id=item.exec_id,
                        event_type=parsed.event_type,
                    )
                    continue

                custom_type = parsed.attributes.custom_task_type

                if (
                    custom_type == _CustomTaskType.CHILD_MAPPING
                    and parsed.event_type == _WorkflowEventType.CUSTOM_TASK_STARTED
                ):
                    mapping = _ChildMapping.model_validate(parsed.attributes.payload.value or {})
                    if item.exec_id and mapping.child_exec_id and mapping.prefix:
                        tracker.register_child(
                            parent_exec_id=item.exec_id,
                            child_exec_id=mapping.child_exec_id,
                            prefix=mapping.prefix,
                        )
                        if message := self._project_patches_to_history_update(
                            tracker.drain_ready(self._state)
                        ):
                            yield message
                    continue

                if custom_type == _CustomTaskType.CALLBACK_REQUEST:
                    cb_data = parsed.attributes.payload.value
                    if isinstance(cb_data, dict):
                        try:
                            call_event = CallbackCallEvent.model_validate(cb_data)
                            logger.info(
                                "channel.callback_request",
                                call_id=call_event.payload.id,
                                name=call_event.payload.name,
                            )
                            yield call_event
                        except Exception:
                            logger.warning(
                                "channel.callback_request.invalid",
                                data=cb_data,
                            )
                    continue

                if item.exec_id and tracker.is_child(item.exec_id):
                    if message := self._project_patches_to_history_update(
                        tracker.reroute(
                            item.exec_id,
                            parsed.attributes.payload,
                            self._state,
                        )
                    ):
                        logger.debug(
                            "channel.child_patches",
                            child_exec_id=item.exec_id,
                            count=len(message.payload.patches),
                            t=f"{time.monotonic() - t0:.3f}s",
                        )
                        yield message
                    continue

                if item.exec_id and item.exec_id != self._exec_id:
                    tracker.stash(item.exec_id, parsed.attributes.payload)
                    continue

                if message := self._project_patches_to_history_update(
                    _extract_patches_from_payload(parsed.attributes.payload, self._state)
                ):
                    logger.debug(
                        "channel.patches",
                        event_type=parsed.event_type,
                        count=len(message.payload.patches),
                        t=f"{time.monotonic() - t0:.3f}s",
                    )
                    yield message

            if final_state := await self._load_terminal_state():
                logger.info(
                    "channel.terminal_fallback",
                    total_events=event_count,
                )
                self._state = final_state
                yield TaskResultEvent(
                    payload=TaskResultPayload(task_id=self._state.id, result=self._state)
                )

    def _project_patches_to_history_update(
        self, patches: list[Op] | None
    ) -> TaskStateUpdateEvent | None:
        self._state, message = _project_workflow_history_update(self._state, patches)
        return message

    # --- Helpers ---

    @staticmethod
    def _get_event_data(event: Any) -> dict[str, Any] | None:
        """Extract event data from the SDK SSE wrapper."""
        payload = getattr(event, "data", None)
        if isinstance(payload, dict):
            return payload

        nested_data = getattr(payload, "data", None)
        if isinstance(nested_data, dict):
            return nested_data
        if isinstance(nested_data, BaseModel):
            dumped = nested_data.model_dump(mode="json")
            if isinstance(dumped, dict):
                return dumped

        return None

    @staticmethod
    def _get_event_exec_id(event: Any) -> str | None:
        """Extract workflow_exec_id from event.workflow_context."""
        ctx = WorkflowAPIChannel._get_event_workflow_context(event)
        if ctx is None:
            return None
        if isinstance(ctx, dict):
            return ctx.get("workflow_exec_id")
        return getattr(ctx, "workflow_exec_id", None)

    @staticmethod
    def _get_event_parent_exec_id(event: Any) -> str | None:
        """Extract parent_workflow_exec_id from event.workflow_context."""
        ctx = WorkflowAPIChannel._get_event_workflow_context(event)
        if ctx is None:
            return None
        if isinstance(ctx, dict):
            return ctx.get("parent_workflow_exec_id")
        return getattr(ctx, "parent_workflow_exec_id", None)

    @staticmethod
    def _get_event_root_exec_id(event: Any) -> str | None:
        """Extract root_workflow_exec_id from event.workflow_context."""
        ctx = WorkflowAPIChannel._get_event_workflow_context(event)
        if ctx is None:
            return None
        if isinstance(ctx, dict):
            return ctx.get("root_workflow_exec_id")
        return getattr(ctx, "root_workflow_exec_id", None)

    @staticmethod
    def _get_event_workflow_context(event: Any) -> Any | None:
        """Extract workflow_context from the SDK SSE wrapper."""
        payload = getattr(event, "data", None)
        return getattr(payload, "workflow_context", None) or getattr(
            event, "workflow_context", None
        )

    @staticmethod
    def _get_broker_sequence(event: Any) -> int | None:
        """Extract broker_sequence from an SDK stream event if present."""
        payload = getattr(event, "data", None)
        nested = getattr(payload, "broker_sequence", None)
        if isinstance(nested, int):
            return nested

        sequence = getattr(event, "broker_sequence", None)
        if isinstance(sequence, int):
            return sequence

        return None

    def _make_stream_query(self, start_seq: int) -> dict[str, Any]:
        """Build the event stream query for this workflow subscription."""
        return {
            "root_workflow_exec_id": self._exec_id,
            "start_seq": start_seq,
            "workflow_event_types": [
                _WorkflowEventType.CUSTOM_TASK_STARTED,
                _WorkflowEventType.CUSTOM_TASK_IN_PROGRESS,
                _WorkflowEventType.CUSTOM_TASK_COMPLETED,
                _WorkflowEventType.WORKFLOW_EXECUTION_COMPLETED,
                _WorkflowEventType.WORKFLOW_EXECUTION_FAILED,
                _WorkflowEventType.WORKFLOW_EXECUTION_CANCELED,
            ],
        }

    async def _execution_has_terminated(self) -> bool:
        """Check whether the parent workflow has already reached a terminal state."""
        try:
            execution = await self._client.executions.get_workflow_execution_async(
                execution_id=self._exec_id
            )
        except Exception as exc:
            logger.warning("channel.execution_status_failed", error=str(exc))
            return False

        return execution.status in _TERMINAL_EXECUTION_STATUSES

    async def _load_terminal_state(self) -> TaskState | None:
        """Fetch the final state from the execution API after stream termination."""
        try:
            execution = await self._client.executions.get_workflow_execution_async(
                execution_id=self._exec_id
            )
        except Exception as exc:
            logger.warning("channel.terminal_state_failed", error=str(exc))
            return None

        if execution.status not in _TERMINAL_EXECUTION_STATUSES:
            return None

        result = getattr(execution, "result", None)
        if isinstance(result, dict):
            try:
                return TaskState.model_validate(result)
            except Exception as exc:
                logger.warning("channel.terminal_state_invalid", error=str(exc))

        return self._state

    async def send(self, message: UpstreamMessage) -> None:
        """Send upstream message to the workflow.

        CallbackResultEvent is delivered via signal_workflow on_callback_result.
        The workflow's signal handler buffers it in pending_callback_results,
        unblocking the WorkflowCallbackBridge.receive_result() wait.
        """
        if isinstance(message, CallbackResultEvent):
            await self._client.executions.signal_workflow_execution_async(
                execution_id=self._exec_id,
                name="on_callback_result",
                input=_SignalPayload(payload=message.model_dump(mode="json")).model_dump(
                    mode="json"
                ),
            )
        else:
            type_name = type(message).__name__
            msg = f"Unsupported upstream message type: {type_name}"
            raise NotImplementedError(msg)

    async def close(self) -> None:
        pass


class _DeferredWorkflowAPIChannel(Channel):
    """Awaits the exec_id future, then buffers NATS events in the background.

    Needed because WorkflowAPIRemoteTask.run() must return a Channel immediately
    (the Task protocol is ``async def run(state) -> Channel``), but the
    exec_id is only available after ``execute_workflow()`` completes. This
    wrapper starts the workflow subscription as soon as the exec_id is
    available so downstream consumers do not miss early events.
    """

    def __init__(
        self,
        client: Workflows,
        exec_id_future: asyncio.Task[str],
        initial_state: TaskState,
    ) -> None:
        self._client = client
        self._future = exec_id_future
        self._initial_state = initial_state
        self._downstream: asyncio.Queue[DownstreamMessage | None] = asyncio.Queue()
        self._channel_ready: asyncio.Future[WorkflowAPIChannel] = (
            asyncio.get_running_loop().create_future()
        )
        self._bg = asyncio.create_task(self._stream_bg())

    async def __aiter__(self) -> AsyncIterator[DownstreamMessage]:
        while True:
            msg = await self._downstream.get()
            if msg is None:
                break
            yield msg
        if self._bg.done():
            exc = self._bg.exception()
            if exc is not None:
                raise exc

    async def send(self, message: UpstreamMessage) -> None:
        """Forward to the inner WorkflowAPIChannel once exec_id is available."""
        channel = await self._channel_ready
        await channel.send(message)

    async def close(self) -> None:
        self._bg.cancel()
        self._future.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._bg

    async def _stream_bg(self) -> None:
        """Start the workflow subscription immediately and buffer downstream messages."""
        try:
            exec_id = await self._future
            channel = WorkflowAPIChannel(self._client, exec_id, self._initial_state)
            if not self._channel_ready.done():
                self._channel_ready.set_result(channel)
            async for msg in channel:
                await self._downstream.put(msg)
        except asyncio.CancelledError:
            if not self._channel_ready.done():
                self._channel_ready.cancel()
            raise
        except Exception as exc:
            if not self._channel_ready.done():
                self._channel_ready.set_exception(exc)
            raise
        finally:
            await self._downstream.put(None)
