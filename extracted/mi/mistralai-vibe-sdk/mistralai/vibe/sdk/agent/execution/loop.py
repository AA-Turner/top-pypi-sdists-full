"""Execution engine for StateModule-based tasks.

ExecutionLoop
=============

Drives a ``StateModule`` with a sequential two-phase cycle:

  Phase 1 (Drain): pop all pending actions. For each, call
  ``module.reduce(state, action) → (new_state, effects)``. Update
  state. Compute and emit history patches if non-empty. Collect effects.

  Phase 2 (Gather): ``asyncio.gather`` all collected effects. When an
  ``EffectExecutor`` is configured, each effect is routed through it;
  otherwise, ``module.handle_effect(effect, sink)`` performs async work
  (LLM call, subtask spawn, callback) and returns a list of new actions.
  Extend the action queue. Go to Phase 1.

Loop exits when ``state.output`` is no longer ``PendingOutput``.

Concrete call trace for an agent that calls one tool then summarizes::

    loop.run(Initialize())
    │
    ├─ DRAIN
    │  reduce(Initialize) → (state, [CallLLM()])
    │  no patches; effects = [CallLLM()]
    │
    ├─ GATHER [CallLLM]
    │  handle_effect(CallLLM, emit):
    │    LLM streams tokens → emit(patches) for each delta   ← consumer sees
    │    LLM finishes with tool_call "get_weather"
    │    → [LLMTurnComplete(response=[...], tool_calls=[get_weather])]
    │
    ├─ DRAIN
    │  reduce(LLMTurnComplete) → (state, [SpawnSubTask(get_weather)])
    │  streaming patches already sent via emit(); reducer updates silently
    │
    ├─ GATHER [SpawnSubTask]
    │  handle_effect(SpawnSubTask, emit):
    │    child.run(child_state) → channel
    │    async for msg in channel: emit(rerouted patches)    ← consumer sees
    │    channel closes → [SubTaskCompleted(call_id=...)]
    │
    ├─ DRAIN
    │  reduce(SubTaskCompleted) → (new_state, [CallLLM()])
    │
    ├─ GATHER [CallLLM]
    │  handle_effect(CallLLM, emit):
    │    LLM responds with summary, no tool calls
    │    → [LLMTurnComplete(response=[...], tool_calls=[])]
    │
    └─ DRAIN
       reduce(LLMTurnComplete, tool_calls=[]) → (completed_state, [])
       emit terminal task_result
       loop exits

The sequential model maps to Temporal's workflow/activity design: the
drain phase is deterministic "workflow code"; the gather phase is async
"activities". Streaming patches flow through ``emit()`` directly, limiting
reducer actions to ~3–5 per LLM turn.

StateModule
===========

Abstract base class for all state machines. Subclasses implement:
- ``reduce(state, event) → (new_state, effects)``: synchronous, pure.
- ``handle_effect(effect, sink) → list[Any]``: async, for ExecutionLoop.
"""

import asyncio
from abc import ABC, abstractmethod
from collections.abc import Callable
from types import TracebackType
from typing import Any, ClassVar, Protocol, Self

import structlog
from structlog.contextvars import bound_contextvars

from mistralai.vibe.sdk.execution_record.patching.json_patch import apply_patches
from mistralai.vibe.sdk.execution_record.patching.produce import diff
from mistralai.vibe.sdk.execution_record.patching.types import Op
from mistralai.vibe.sdk.execution_record.projections.direct_state_sink import (
    AppendHistoryScope,
    FixedHistoryScope,
    HistoryScope,
    _project_history_patches,
)
from mistralai.vibe.sdk.execution_record.state import FailedOutput, PendingOutput, TaskState
from mistralai.vibe.sdk.transports.events import (
    CallbackCallEvent,
    CallbackResultEvent,
    DownstreamMessage,
    TaskResultEvent,
    TaskResultPayload,
    UpstreamMessage,
)

__all__ = [
    "AppendHistoryScope",
    "CallbackBridge",
    "DirectStateSink",
    "DownstreamWriter",
    "EffectExecutor",
    "EffectRegistry",
    "Emit",
    "ExecutionLoop",
    "FixedHistoryScope",
    "HistoryScope",
    "LocalCallbackBridge",
    "StateModule",
    "StateSink",
    "StreamScopeTracker",
    "_project_history_patches",
]

# Type alias for the emit callback used by ExecutionLoop and handle_effect
Emit = Callable[[list[Op]], None]


def _copy_scope_value(target: TaskState, source: TaskState, scope: HistoryScope) -> TaskState:
    if isinstance(scope, FixedHistoryScope):
        index = scope.index
        if index >= len(target.history) or index >= len(source.history):
            msg = f"Fixed stream scope /history/{index} is outside the available history"
            raise ValueError(msg)
        history = list(target.history)
        history[index] = source.history[index]
        return target.model_copy(update={"history": history})

    if len(target.history) < scope.start_index or len(source.history) < scope.start_index:
        msg = f"Append stream scope starts outside the available history: {scope.start_index}"
        raise ValueError(msg)
    history = [*target.history[: scope.start_index], *source.history[scope.start_index :]]
    return target.model_copy(update={"history": history})


def _scopes_equal(left: HistoryScope, right: HistoryScope) -> bool:
    if isinstance(left, FixedHistoryScope) and isinstance(right, FixedHistoryScope):
        return left.index == right.index
    if isinstance(left, AppendHistoryScope) and isinstance(right, AppendHistoryScope):
        return left.start_index == right.start_index
    return False


def _scopes_conflict(left: HistoryScope, right: HistoryScope) -> bool:
    if isinstance(left, FixedHistoryScope) and isinstance(right, FixedHistoryScope):
        return left.index == right.index
    if isinstance(left, AppendHistoryScope) and isinstance(right, AppendHistoryScope):
        return True
    if isinstance(left, FixedHistoryScope) and isinstance(right, AppendHistoryScope):
        return left.index >= right.start_index
    if isinstance(left, AppendHistoryScope) and isinstance(right, FixedHistoryScope):
        return right.index >= left.start_index
    return False


class StreamScopeTracker:
    """Tracks stream scopes visible to consumers but not yet reducer-committed."""

    def __init__(self) -> None:
        self._protected: list[HistoryScope] = []

    def mark_streamed(self, scope: HistoryScope) -> None:
        if any(_scopes_equal(scope, protected) for protected in self._protected):
            return
        for protected in self._protected:
            if _scopes_conflict(scope, protected):
                msg = f"Conflicting active stream scopes: {scope!r} conflicts with {protected!r}"
                raise RuntimeError(msg)
        self._protected.append(scope)

    def mark_committed(self, scope: HistoryScope) -> None:
        self._protected = [
            protected for protected in self._protected if not _scopes_equal(scope, protected)
        ]

    def protected_scopes(self) -> tuple[HistoryScope, ...]:
        return tuple(self._protected)


class StateSink(Protocol):
    """Port for streaming state snapshots during effect handling.

    Callers push full TaskState snapshots via update(); the sink computes
    diffs or publishes events as an implementation detail. Provides a
    context manager wrapping the streaming session.

    Adapters:
    - DirectStateSink: diffs prev/new, calls emit(patches) on the queue.
    - WorkflowStateSink: publishes via NATS task() CM.
    """

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

    async def update(self, new_state: TaskState) -> None: ...

    @property
    def scope(self) -> HistoryScope | None: ...

    def scoped(self, history_scope: HistoryScope) -> "StateSink": ...


class DirectStateSink(StateSink):
    """StateSink that diffs history vs prev and calls emit(patches).

    Used by both the local execution path (AgentTask.run) and the HTTP streaming
    path to stream patches to the in-process downstream queue. Each update()
    computes ``diff(prev.history, new_state.history, "/history")`` and passes
    the patches to the emit callback. Scoped sinks treat their scope as the
    only writable region and ignore changes outside it.
    """

    def __init__(
        self,
        emit: Emit,
        initial_state: TaskState,
        downstream: "DownstreamWriter | None" = None,
        *,
        scope: HistoryScope | None = None,
        mark_streamed: Callable[[HistoryScope], None] | None = None,
    ) -> None:
        self._emit = emit
        self._prev = initial_state
        self._downstream = downstream
        self._scope = scope
        self._mark_streamed = mark_streamed

    @property
    def scope(self) -> HistoryScope | None:
        return self._scope

    async def __aenter__(self) -> "DirectStateSink":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    async def update(self, new_state: TaskState) -> None:
        patches = _project_history_patches(self._prev, new_state, self._scope)
        if patches:
            self._emit(patches)
            if self._scope is not None and self._mark_streamed is not None:
                self._mark_streamed(self._scope)
        self._prev = self._next_prev(new_state)

    def scoped(self, history_scope: HistoryScope) -> "DirectStateSink":
        return DirectStateSink(
            self._emit,
            self._prev,
            self._downstream,
            scope=history_scope,
            mark_streamed=self._mark_streamed,
        )

    def _next_prev(self, new_state: TaskState) -> TaskState:
        if self._scope is None:
            return new_state
        return _copy_scope_value(
            target=self._prev,
            source=new_state,
            scope=self._scope,
        )


class CallbackBridge(Protocol):
    """Port for bidirectional callback communication with the parent.

    Abstracts the transport for callback request/result exchange between
    a task and its parent (or external consumer).

    Adapters:
    - LocalCallbackBridge: sends via DownstreamWriter + awaits via ExecutionLoop.
    - WorkflowCallbackBridge: signals parent workflow or emits NATS events.

    Callback ID uniqueness invariant:
      Correlation is keyed by ``call_id`` alone (not ``(call_id, path)``).
      call_id is the SDK-owned internal key (generated via uuid4 in the
      completion bridge, or by programmatic callers). Each workflow
      instance has its own pending-results dict, so there is no
      cross-workflow collision risk. The provider-facing identifier
      (e.g. LLM tool_call.id) is stored separately as ``provider_id``
      and is never used for matching.
    """

    async def send_request(self, event: CallbackCallEvent) -> None:
        """Send a callback request to the parent."""
        ...

    async def receive_result(self, call_id: str) -> CallbackResultEvent:
        """Wait for the callback result matching call_id (SDK-owned ID)."""
        ...


class DownstreamWriter(Protocol):
    """Port for pushing patches and messages toward the consumer.

    Adapters wrap the underlying transport (asyncio.Queue, HTTP SSE,
    Temporal no-op) and present a uniform write interface to
    ExecutionLoop and effect handlers.
    """

    def send_patches(self, task_id: str, patches: list[Op]) -> None:
        """Wrap history patches in TaskStateUpdateEvent and send downstream."""
        ...

    def send(self, message: DownstreamMessage) -> None:
        """Send an arbitrary downstream message (e.g. CallbackCallEvent)."""
        ...


class LocalCallbackBridge(CallbackBridge):
    """CallbackBridge for in-process execution.

    Sends CallbackCallEvent via DownstreamWriter, awaits CallbackResultEvent via
    ExecutionLoop.receive_upstream(). Used by the local execution path.
    """

    def __init__(self, downstream: DownstreamWriter, loop: "ExecutionLoop") -> None:
        self._downstream = downstream
        self._loop = loop

    async def send_request(self, event: CallbackCallEvent) -> None:
        self._downstream.send(event)

    async def receive_result(self, call_id: str) -> CallbackResultEvent:
        return await self._loop.receive_upstream(call_id)


logger = structlog.get_logger()


class EffectExecutor(Protocol):
    """Protocol for routing effects to external handlers.

    Injected into ExecutionLoop to make the gather phase pluggable.
    The executor is fully responsible for providing its own sink —
    no sink or module parameter on execute().

    Default (None) = local path via module.handle_effect(effect, sink).
    Workflow path injects a WorkflowEffectExecutor that routes effects
    by category (activity effects to Temporal activities, etc.).
    """

    async def execute(self, effect: Any) -> list[Any]: ...


class EffectRegistry:
    """Registry mapping effect types to standalone handler functions.

    Handlers are standalone async functions (not methods) registered at module
    scope via ``@registry.handles(EffectType)``. The registry is then assigned
    to the ``effect_handlers`` ClassVar on a StateModule subclass.

    Why standalone functions instead of methods?
    - The workflow path wraps each handler as a named Temporal activity
      (via ``make_effect_activities``). Standalone functions with explicit
      signatures let the activity wrapper inspect annotations — no class
      instance needed.
    - Handlers are independently testable without constructing a module.
    - Effects carry the serializable data needed by their handlers, keeping
      handler signatures identical across local and workflow paths.

    Usage::

        registry = EffectRegistry()

        @registry.handles(CallLLM)
        async def _handle_call_llm(effect, sink):
            ...

        class MyModule(StateModule):
            effect_handlers = registry
            initial_action_type = Initialize
    """

    def __init__(self) -> None:
        self._handlers: dict[type, Callable[..., Any]] = {}

    def handles(
        self,
        effect_type: type,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator: register a handler function for an effect type."""

        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            self._handlers[effect_type] = fn
            return fn

        return decorator

    def get(self, key: type, default: Any = None) -> Callable[..., Any] | None:
        """Look up the handler for an effect type."""
        return self._handlers.get(key, default)

    def items(self) -> Any:
        """Iterate over (effect_type, handler) pairs."""
        return self._handlers.items()


class StateModule(ABC):
    """Abstract base for state machines driven by ExecutionLoop.

    Subclasses must implement:
    - ``reduce(state, event)``: synchronous pure function.
    - ``handle_effect(effect, sink)``: async, for ExecutionLoop.

    Subclasses should set:
    - ``effect_handlers``: EffectRegistry mapping effect types to handlers.
    - ``initial_action_type``: the action class that seeds the loop.
    """

    effect_handlers: ClassVar[EffectRegistry] = EffectRegistry()
    initial_action_type: ClassVar[type]

    @abstractmethod
    def reduce(self, state: TaskState, action: Any) -> tuple[TaskState, list[Any]]:
        """(state, action) -> (new_state, effects)"""
        ...

    @abstractmethod
    async def handle_effect(self, effect: Any, sink: "StateSink") -> list[Any]:
        """Execute a side effect, stream state updates via sink, return new actions.

        Performs async work (LLM call, subtask spawn, callback) and returns
        a list of actions for the next drain phase. Streaming state updates
        are sent via sink.update() rather than through the reducer.
        """
        ...

    def bind_exec_loop(  # noqa: B027
        self,
        loop: "ExecutionLoop",
        downstream: "DownstreamWriter | None" = None,
    ) -> None:
        """Called after ExecutionLoop construction.

        Override if the module needs references to the loop or downstream.
        """


class ExecutionLoop:
    """Sequential execution loop for any StateModule-based task.

    Two-phase cycle:
    1. Drain: pop actions from queue, reduce each, collect effects, emit history patches.
    2. Gather: execute all effects concurrently via asyncio.gather, collect
       returned actions from each effect handler.

    Repeat until state.output is no longer PendingOutput.

    Effects return actions that are processed in the next drain phase.
    This maps directly to Temporal's workflow/activity model.

    Streaming patches (LLM tokens, child task progress) flow through
    the emit callback, not through the reducer, keeping the reducer
    action count low (~3 actions/turn).
    """

    def __init__(
        self,
        initial_state: TaskState,
        module: StateModule,
        downstream: DownstreamWriter,
        effect_executor: EffectExecutor | None = None,
    ) -> None:
        """Initialize the execution loop.

        Args:
            initial_state: Starting TaskState. Owned by the loop.
            module: StateModule whose reduce/handle_effect methods drive
                the loop.
            downstream: DownstreamWriter for pushing patches and messages
                toward the consumer.
            effect_executor: Optional EffectExecutor for routing effects to
                external handlers (e.g. Temporal activities). When None,
                effects are handled locally via module.handle_effect with
                a DirectStateSink.
        """
        self._state = initial_state
        self._view_state = initial_state
        self._module = module
        self._downstream = downstream
        self._effect_executor = effect_executor
        self._action_queue: list[Any] = []
        self._upstream: asyncio.Queue[UpstreamMessage] | None = None
        self._upstream_buffer: dict[str, CallbackResultEvent] = {}
        self._stream_tracker = StreamScopeTracker()

    @property
    def state(self) -> TaskState:
        """Current state (read-only access for effect handlers)."""
        return self._state

    def update_view(self, patches: list[Op]) -> None:
        """Update internal view state AND propagate patches to consumer.

        Called during gather (streaming tokens/child progress) and drain
        (reducer diffs). Named 'update_view' because it advances both the
        loop's internal _view_state and the consumer's external view.

        In drain: patches = diff(_view_state, new_state), so this call is
        followed by an explicit _view_state = new_state assignment as the
        real safety guarantee. The apply_patches here is redundant but
        harmless (Option A — same method in both drain and gather for
        simplicity).
        """
        self._view_state = apply_patches(self._view_state, patches)
        self._downstream.send_patches(self._state.id, patches)

    async def run(self, initial_action: Any) -> None:
        """Main loop. Runs until state.output is terminal.

        1. Seed the action queue with initial_action
        2. Drain all actions through the reducer, collecting effects
        3. If terminal, exit
        4. Execute all effects concurrently, collecting returned actions
        5. Extend action queue with returned actions
        6. Go to step 2

        Args:
            initial_action: First action to process (typically Initialize).
        """
        with bound_contextvars(
            task_id=self._state.id,
            module=type(self._module).__name__,
        ):
            logger.info("loop.start")
            self._action_queue.append(initial_action)
            iteration = 0

            while True:
                iteration += 1

                # Phase 1: drain actions through reducer
                effects: list[Any] = []
                while self._action_queue:
                    action = self._action_queue.pop(0)
                    action_name = type(action).__name__
                    logger.info("loop.drain", action=action_name, iteration=iteration)
                    logger.debug("loop.drain.detail", action_data=repr(action))

                    committed_scope = getattr(action, "stream_scope", None)
                    new_state, new_effects = self._module.reduce(self._state, action)
                    self._state = new_state
                    if committed_scope is not None:
                        self._stream_tracker.mark_committed(committed_scope)

                    visible_target = self._visible_target_for_drain(new_state)
                    patches = diff(self._view_state.history, visible_target.history, "/history")
                    if patches:
                        logger.debug("loop.drain.patches", count=len(patches))
                        self.update_view(patches)
                    self._view_state = visible_target  # explicit sync — safety guarantee

                    if new_effects:
                        logger.debug(
                            "loop.drain.effects",
                            effects=[type(e).__name__ for e in new_effects],
                        )
                    effects.extend(new_effects)

                # Check terminal
                if not isinstance(self._state.output, PendingOutput):
                    logger.info(
                        "loop.terminal",
                        output_type=type(self._state.output).__name__,
                        iteration=iteration,
                    )
                    self._send_terminal_result()
                    break

                if not effects:  # and implictly with output being PendingOutput
                    logger.warning("loop.stall", iteration=iteration)
                    self._state = self._state.model_copy(
                        update={
                            "output": FailedOutput(
                                error="Execution loop stalled with pending output and no effects"
                            )
                        }
                    )
                    self._send_terminal_result()
                    break

                # Phase 2: execute effects concurrently, gather returned actions
                returned = await self._gather_effects(effects, iteration)
                self._action_queue.extend(returned)

            logger.info("loop.end", iterations=iteration)

    async def _gather_effects(self, effects: list[Any], iteration: int) -> list[Any]:
        """Execute effects concurrently and return collected actions."""
        effect_names = [type(e).__name__ for e in effects]
        logger.info("loop.gather", effects=effect_names, iteration=iteration)

        if self._effect_executor:
            results = await asyncio.gather(
                *[self._effect_executor.execute(effect) for effect in effects]
            )
        else:
            results = await asyncio.gather(
                *[
                    self._module.handle_effect(
                        effect,
                        DirectStateSink(
                            self.update_view,
                            self._state,
                            self._downstream,
                            mark_streamed=self._stream_tracker.mark_streamed,
                        ),
                    )
                    for effect in effects
                ]
            )
        total_actions = sum(len(al) for al in results)
        logger.info(
            "loop.gather.complete",
            returned_actions=total_actions,
            iteration=iteration,
        )
        actions: list[Any] = []
        for action_list in results:
            actions.extend(action_list)
        return actions

    def _visible_target_for_drain(self, new_state: TaskState) -> TaskState:
        visible_target = new_state
        for protected_scope in self._stream_tracker.protected_scopes():
            visible_target = _copy_scope_value(
                target=visible_target,
                source=self._view_state,
                scope=protected_scope,
            )
        return visible_target

    async def receive_upstream(self, call_id: str) -> CallbackResultEvent:
        """Wait for an upstream CallbackResultEvent matching call_id.

        Reads from the upstream queue, buffering non-matching messages
        for later retrieval. Blocks until the matching message arrives.

        Relies on the callback ID uniqueness invariant: call_id is the
        SDK-owned correlation key (see CallbackBridge docstring).

        Args:
            call_id: The SDK-owned correlation ID to match.

        Raises:
            RuntimeError: If no upstream queue was configured.
        """
        if self._upstream is None:
            msg = "No upstream queue configured"
            raise RuntimeError(msg)

        if call_id in self._upstream_buffer:
            return self._upstream_buffer.pop(call_id)

        while True:
            raw = await self._upstream.get()
            if isinstance(raw, CallbackResultEvent) and raw.payload.id == call_id:
                return raw
            if isinstance(raw, CallbackResultEvent):
                self._upstream_buffer[raw.payload.id] = raw

    def _send_terminal_result(self) -> None:
        """Send the terminal TaskResultEvent carrying the final TaskState."""
        self._downstream.send(
            TaskResultEvent(
                payload=TaskResultPayload(
                    task_id=self._state.id,
                    result=self._state,
                )
            )
        )
