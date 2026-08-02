"""Typed envelopes for channel communication."""

from typing import Any, Literal

from pydantic import BaseModel, Field

from mistralai.vibe.sdk.execution_record.patching.types import Op
from mistralai.vibe.sdk.execution_record.state import TaskState


class TaskStateUpdatePayload(BaseModel):
    """Payload for history-only downstream patches."""

    task_id: str = ""
    patches: list[Op] = Field(default_factory=list)


class TaskStateUpdateEvent(BaseModel):
    """Downstream history update for an in-flight task."""

    type: Literal["history_update"] = "history_update"
    payload: TaskStateUpdatePayload = Field(default_factory=TaskStateUpdatePayload)


class TaskResultPayload(BaseModel):
    """Payload for the terminal downstream task result."""

    task_id: str = ""
    result: TaskState


class TaskResultEvent(BaseModel):
    """Downstream final TaskState after a task completes."""

    type: Literal["task_result"] = "task_result"
    payload: TaskResultPayload


class CallbackCallPayload(BaseModel):
    """Payload for a callback request emitted by a child task."""

    id: str
    name: str
    input: Any = None
    path: list[str] = Field(default_factory=list)


class CallbackCallEvent(BaseModel):
    """Downstream request for callback execution."""

    type: Literal["callback_call"] = "callback_call"
    payload: CallbackCallPayload


class CallbackStateUpdatePayload(BaseModel):
    """Payload for callback progress streamed upstream."""

    id: str
    name: str = ""
    patches: list[Op] = Field(default_factory=list)
    path: list[str] = Field(default_factory=list)


class CallbackStateUpdateEvent(BaseModel):
    """Upstream callback progress event."""

    type: Literal["callback_state_update"] = "callback_state_update"
    payload: CallbackStateUpdatePayload


class CallbackResultPayload(BaseModel):
    """Payload for a completed callback result."""

    id: str
    name: str = ""
    state: TaskState
    path: list[str] = Field(default_factory=list)


class CallbackResultEvent(BaseModel):
    """Upstream completed callback result."""

    type: Literal["callback_result"] = "callback_result"
    payload: CallbackResultPayload


class TaskCancellationEvent(BaseModel):
    """Signal to stop execution."""

    type: Literal["task_cancellation"] = "task_cancellation"


DownstreamMessage = TaskStateUpdateEvent | TaskResultEvent | CallbackCallEvent
UpstreamMessage = CallbackStateUpdateEvent | CallbackResultEvent | TaskCancellationEvent

__all__ = [
    "CallbackCallEvent",
    "CallbackCallPayload",
    "CallbackResultEvent",
    "CallbackResultPayload",
    "CallbackStateUpdateEvent",
    "CallbackStateUpdatePayload",
    "DownstreamMessage",
    "TaskCancellationEvent",
    "TaskResultEvent",
    "TaskResultPayload",
    "TaskStateUpdateEvent",
    "TaskStateUpdatePayload",
    "UpstreamMessage",
]
