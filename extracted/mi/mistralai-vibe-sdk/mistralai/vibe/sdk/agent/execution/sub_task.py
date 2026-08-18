"""Subtask lifecycle: reducer for spawning and completing child tasks.

Provides ``sub_task_reducer`` for managing child task state within a parent
StateModule. Handles call requests (lookup, spawn, track results) and
callback resolution (local, bubble upstream, or fail).

``resolve_callback_request`` is the shared async resolver for child callback
requests. Both the local path (channel iteration in agent.py) and the
workflow path (signal handler) call it with different transport adapters.

Child patch rerouting is handled by effect handlers (``_handle_spawn_subtask``
in agent.py) which relay patches via the StateSink rather than through
the reducer.

Used by AgentModule to process tool calls as child tasks.
"""

from collections.abc import Awaitable, Callable
from typing import Any

from pydantic import BaseModel, SerializeAsAny

from mistralai.vibe.sdk.agent.execution.loop import HistoryScope
from mistralai.vibe.sdk.agent.execution.resources import spawn_child_scope
from mistralai.vibe.sdk.agent.tasks.core import StatefulTask, Task, TaskCallback
from mistralai.vibe.sdk.agent.tasks.runtime import TaskConfigBase
from mistralai.vibe.sdk.execution_record.snapshots import seed_child_state
from mistralai.vibe.sdk.execution_record.state import (
    FailedOutput,
    PendingOutput,
    TaskCallEntry,
    TaskResultEntry,
    TaskResultEntryPayload,
    TaskState,
)
from mistralai.vibe.sdk.transports.events import (
    CallbackCallEvent,
    CallbackCallPayload,
    CallbackResultEvent,
    CallbackResultPayload,
    TaskResultEvent,
    TaskStateUpdateEvent,
)

__all__ = [
    "CallbackResultReceived",
    "CallCallback",
    "FailSubTask",
    "SpawnSubTask",
    "SubTaskAction",
    "SubTaskCallRequest",
    "SubTaskCompleted",
    "SubTaskEffect",
    "_update_result_entry",
    "resolve_callback_request",
    "sub_task_reducer",
]

# ---------------------------------------------------------------------------
# Internal action types (reducer inputs)
# ---------------------------------------------------------------------------


class SubTaskCallRequest(BaseModel):
    """Action: a tool call or subtask invocation was requested."""

    call: TaskCallEntry


class CallbackResultReceived(BaseModel):
    """Action: callback result arrived from upstream.

    The parent resolved a callback request and sent back a
    CallbackResultEvent. This action feeds the result into the reducer
    to update the pending TaskResultEntry.
    """

    call_id: str
    result_state: TaskState


# ---------------------------------------------------------------------------
# Effect types
# ---------------------------------------------------------------------------


class SpawnSubTask(BaseModel):
    """Effect: spawn a child task. The handler will call task.run().

    Carries parent state so the handler can reroute child patches into
    the parent scope and call sink.update(parent_state).
    """

    state: TaskState  # parent state at effect creation (set by AgentModule reducer)
    call: TaskCallEntry
    child_state: TaskState
    result_index: int  # index of the TaskResultEntry in parent history
    task_config: SerializeAsAny[TaskConfigBase] | None = None  # TaskConfig for dispatch


class SubTaskCompleted(BaseModel):
    """Action: a subtask finished execution.

    Returned by the execution loop's effect handler after a child
    channel closes. The reducer uses it to update the embedded
    TaskResultEntry with the final child state, set generation_status
    to "complete", and compute patches via diff().
    """

    call_id: str
    final_state: TaskState
    stream_scope: HistoryScope | None = None


class CallCallback(BaseModel):
    """Effect: emit CallbackCallEvent downstream and await CallbackResultEvent upstream.

    The handler emits a CallbackCallEvent on the downstream queue and blocks
    until the parent responds with a CallbackResultEvent. Then it dispatches
    CallbackResultReceived to update the pending TaskResultEntry.
    """

    call: TaskCallEntry
    result_index: int  # index of the TaskResultEntry in parent history


class FailSubTask(BaseModel):
    """Effect: complete a synchronously-failed tool call (e.g. an unknown tool name)."""

    call_id: str
    final_state: TaskState


SubTaskAction = SubTaskCallRequest | CallbackResultReceived | SubTaskCompleted
SubTaskEffect = SpawnSubTask | SubTaskCompleted | CallCallback | FailSubTask


def _make_failed_callback_state(event_id: str, event_input: Any, name: str) -> TaskState:
    """Build a FailedOutput TaskState for an unresolved callback."""
    return TaskState(
        id=event_id,
        input=event_input,
        output=FailedOutput(error=f"Unhandled callback: {name}"),
    )


async def resolve_callback_request(
    request: CallbackCallEvent,
    child_path_segment: str,
    send_result_to_child: Callable[[CallbackResultEvent], Awaitable[None]],
    task_implementations: dict[str, Task],
    callback_schemas: dict[str, TaskCallback],
    bubble_upstream: Any | None,
) -> None:
    """Resolve a callback request from a child task.

    Shared resolver used by both the local path (channel iteration in
    agent.py) and the workflow path (signal handler). Resolution order:

    1. Name in task_implementations → run locally, send result to child.
    2. Name in callback_schemas → bubble upstream with path prepended.
    3. Unknown → send FailedOutput to child.

    Args:
        request: The CallbackCallEvent from the child.
        child_path_segment: Logical child id to prepend to path when bubbling.
            This is the TaskState.id of the child, NOT the transport exec_id.
        send_result_to_child: Transport adapter for sending CallbackResultEvent
            back to the child. Local: child_channel.send(). Workflow:
            signal_external_workflow().
        task_implementations: Tasks that can resolve callbacks locally.
        callback_schemas: Callback schemas — if a name is here but not in
            task_implementations, the request is bubbled upstream.
        bubble_upstream: CallbackBridge for bubbling. On the local path,
            a LocalCallbackBridge. On the workflow path, a
            WorkflowCallbackBridge. None if bubbling is not supported
            (top-level task with no external consumer).
    """
    from mistralai.vibe.sdk.execution_record.patching.json_patch import apply_patches

    name = request.payload.name

    if name in task_implementations:
        impl = task_implementations[name]
        cb_state = TaskState(
            id=request.payload.id,
            input=request.payload.input,
            output=PendingOutput(),
        )

        async with spawn_child_scope(should_raise=False):
            impl_channel = await impl.run(cb_state)
            async for impl_msg in impl_channel:
                if isinstance(impl_msg, TaskStateUpdateEvent):
                    cb_state = apply_patches(cb_state, impl_msg.payload.patches)
                elif isinstance(impl_msg, TaskResultEvent):
                    cb_state = impl_msg.payload.result
                elif isinstance(impl_msg, CallbackCallEvent):
                    # Nested callbacks from callback implementations are not
                    # supported. The config-time check in AgentTask.__init__
                    # prevents this, but guard at runtime too.
                    msg = (
                        f"Callback implementation '{name}' emitted a nested "
                        f"callback request '{impl_msg.payload.name}' which cannot be "
                        f"resolved. Nested callbacks are not supported."
                    )
                    raise RuntimeError(msg)
        await send_result_to_child(
            CallbackResultEvent(
                payload=CallbackResultPayload(
                    id=request.payload.id,
                    name=request.payload.name,
                    state=cb_state,
                    path=[],
                )
            )
        )

    elif name in callback_schemas and bubble_upstream is not None:
        bubbled = CallbackCallEvent(
            payload=CallbackCallPayload(
                id=request.payload.id,
                name=request.payload.name,
                input=request.payload.input,
                path=[child_path_segment, *request.payload.path],
            )
        )
        await bubble_upstream.send_request(bubbled)
        result = await bubble_upstream.receive_result(request.payload.id)
        await send_result_to_child(
            CallbackResultEvent(
                payload=CallbackResultPayload(
                    id=request.payload.id,
                    name=request.payload.name,
                    state=result.payload.state,
                    path=[],
                )
            )
        )

    else:
        failed_state = _make_failed_callback_state(
            request.payload.id,
            request.payload.input,
            name,
        )
        await send_result_to_child(
            CallbackResultEvent(
                payload=CallbackResultPayload(
                    id=request.payload.id,
                    name=request.payload.name,
                    state=failed_state,
                    path=[],
                )
            )
        )


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _make_child_state(call: TaskCallEntry) -> TaskState:
    """Build the initial TaskState for a child task from a call entry."""
    return TaskState(
        id=call.payload.id,
        input=call.payload.input,
        output=PendingOutput(),
    )


def _update_result_entry(
    state: TaskState,
    call_id: str,
    final_state: TaskState,
) -> TaskState | None:
    """Find a TaskResultEntry by call_id and replace its state, marking complete.

    Returns the new TaskState, or None if no matching entry was found.
    Produces a new history list (safe for diff()).
    """
    for idx, entry in enumerate(state.history):
        if isinstance(entry, TaskResultEntry) and entry.payload.id == call_id:
            new_result_entry = TaskResultEntry(
                payload=TaskResultEntryPayload(
                    id=entry.payload.id,
                    name=entry.payload.name,
                    state=final_state,
                ),
                generation_status="complete",
                annotations=entry.annotations,
            )
            new_history = list(state.history)
            new_history[idx] = new_result_entry
            return state.model_copy(update={"history": new_history})
    return None


# ---------------------------------------------------------------------------
# Reducer
# ---------------------------------------------------------------------------


def sub_task_reducer(
    state: TaskState,
    action: SubTaskAction,
    task_implementations: dict[str, Task],
    callback_schemas: dict[str, TaskCallback] | None = None,
) -> tuple[TaskState, list[SubTaskEffect]]:
    """Pure reducer for subtask lifecycle.

    Returns ``(new_state, effects)``. Transport patches are now computed
    by the execution loop rather than returned from reducers.

    Args:
        state: Current parent TaskState.
        action: A SubTaskCallRequest, SubTaskCompleted, or
            CallbackResultReceived.
        task_implementations: Available task implementations keyed by name.
            Used to look up implementations for call requests.
        callback_schemas: Callback schemas keyed by name. When a call
            request targets a name in this dict (but not in
            task_implementations), a CallCallback effect is returned
            instead of FailedOutput.
    """
    schemas = callback_schemas or {}
    match action:
        case SubTaskCallRequest(call=call):
            return _handle_call_request(state, call, task_implementations, schemas)

        case CallbackResultReceived(call_id=call_id, result_state=result_state):
            return _handle_callback_result(state, call_id, result_state)

        case SubTaskCompleted(call_id=call_id, final_state=final_state):
            return _handle_subtask_completed(state, call_id, final_state)

    return (state, [])  # pragma: no cover


def _handle_call_request(
    state: TaskState,
    call: TaskCallEntry,
    task_implementations: dict[str, Task],
    callback_schemas: dict[str, TaskCallback],
) -> tuple[TaskState, list[SubTaskEffect]]:
    """Handle a subtask call request.

    Resolution order:
    1. Name in task_implementations → SpawnSubTask effect (local execution).
    2. Name in callback_schemas → CallCallback effect (delegate upstream).
    3. Neither → FailedOutput (unknown subtask).
    """
    name = call.payload.name

    # 1. Local implementation takes priority
    if name in task_implementations:
        child_state = _make_child_state(call)
        impl = task_implementations[name]
        if isinstance(impl, StatefulTask):
            child_state = seed_child_state(
                child_state, state, task_name=name, snapshot_type=impl.snapshot_type
            )

        result_index = len(state.history) + 1  # after TaskCallEntry
        result_entry = TaskResultEntry(
            payload=TaskResultEntryPayload(
                id=call.payload.id,
                name=name,
                state=child_state,
            ),
            generation_status="generating",
        )
        new_state = state.model_copy(update={"history": [*state.history, call, result_entry]})
        return (
            new_state,
            [
                SpawnSubTask(
                    state=new_state, call=call, child_state=child_state, result_index=result_index
                )
            ],
        )

    # 2. Callback — delegate upstream
    if name in callback_schemas:
        child_state = _make_child_state(call)
        result_index = len(state.history) + 1  # after TaskCallEntry
        result_entry = TaskResultEntry(
            payload=TaskResultEntryPayload(
                id=call.payload.id,
                name=name,
                state=child_state,
            ),
            generation_status="generating",
        )
        new_state = state.model_copy(update={"history": [*state.history, call, result_entry]})
        return (
            new_state,
            [CallCallback(call=call, result_index=result_index)],
        )

    # 3. Unknown
    failed_state = TaskState(
        id=call.payload.id,
        input=call.payload.input,
        output=FailedOutput(error=f"Unknown subtask: {name}"),
    )
    result_entry = TaskResultEntry(
        payload=TaskResultEntryPayload(
            id=call.payload.id,
            name=name,
            state=failed_state,
        ),
        generation_status="generating",
    )
    new_state = state.model_copy(update={"history": [*state.history, call, result_entry]})
    return (new_state, [FailSubTask(call_id=call.payload.id, final_state=failed_state)])


def _handle_callback_result(
    state: TaskState,
    call_id: str,
    result_state: TaskState,
) -> tuple[TaskState, list[SubTaskEffect]]:
    """Handle a callback result arriving from upstream.

    Finds the pending TaskResultEntry matching call_id, replaces its
    child state with the completed result_state, and sets generation_status
    to "complete".
    """
    new_state = _update_result_entry(state, call_id, result_state)
    if new_state is None:
        return (state, [])
    return (new_state, [])


def _handle_subtask_completed(
    state: TaskState,
    call_id: str,
    final_state: TaskState,
) -> tuple[TaskState, list[SubTaskEffect]]:
    """Handle a subtask completion action.

    Finds the TaskResultEntry matching call_id, replaces its embedded
    child state with final_state, sets generation_status to "complete",
    and computes patches via diff().
    """
    new_state = _update_result_entry(state, call_id, final_state)
    if new_state is None:
        return (state, [])
    return (new_state, [])
