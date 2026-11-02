"""Session event types.

Any runtime implementing the SessionWorkflow contract emits durable public
session-history rows via `Task(SESSION_EVENT_TASK_TYPE, state=...)`, where
`state` is a serialized concrete workflow-session event variant. Those events
land on NATS + Abraxas Postgres through the Workflows platform and are lazily
read by vibe_agents via the workflow_sdk client.

This module only exposes the types for the envelope. Emitting is just a
one-liner `workflows.task(...)` call, so we don't ship a helper here and
the SDK stays free of any `mistralai.workflows` import.
"""

from enum import StrEnum
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator

from mistralai.vibe_agents.session_workflow.task_protocol import (
    GenerationStatus,
    HistoryEntry,
    TaskOutputPayload,
    TaskResultHistoryEntry,
)

SESSION_EVENT_TASK_TYPE = "vibe_agents.session_event"
SESSION_V1_EVENT_TASK_TYPE = "vibe_agents.session_event.v1"
SESSION_V1_TURN_EVENT_TASK_TYPE = "vibe_agents.session_event.v1.turn"
SESSION_V1_STATUS_EVENT_TASK_TYPE = "vibe_agents.session_event.v1.session.status"
SESSION_V1_CALLBACK_EVENT_TASK_TYPE = "vibe_agents.session_event.v1.callback"
SESSION_V1_COMMAND_ACK_TASK_TYPE = "vibe_agents.session_event.v1.command_ack"
SESSION_V1_PROMPT_SUGGESTION_TASK_TYPE = "vibe_agents.session_event.v1.prompt_suggestion"
SESSION_V1_ARTIFACT_TASK_TYPE = "vibe_agents.session_event.v1.artifact"
# Carries a ``SubscriptionUpdateStateContent``. The control plane applies it to the session's
# subscriptions and stores no session event.
SESSION_SUBSCRIPTION_UPDATE_TASK_TYPE = "vibe_agents.session_subscription_update"


class WorkflowSessionEventType(StrEnum):
    HISTORY_ENTRY = "history_entry"
    SESSION_STATUS_CHANGED = "session_status_changed"
    SUBTASK_STARTED = "subtask_started"
    SUBTASK_RESULT = "subtask_result"


class WorkflowSessionStatus(StrEnum):
    RUNNING = "running"
    WAITING = "waiting"


class WorkflowSessionV1CommandAckTaskState(BaseModel):
    """A workflow resolved a command, emitted with the command id as the task id.

    The control plane stores it as the command's durable outcome and never serves it
    on ``/events``. A successful message needs none: its user entry carries the same task id.
    Failed skill preflight emits a message acknowledgement with a terminal rejection reason.
    """

    session_id: str
    command_id: UUID
    command_type: Literal["message", "integration_event"]
    source: str | None = None
    rejection_reason: Literal["skill_loading_failed", "skill_assets_too_large"] | None = None

    @model_validator(mode="after")
    def validate_rejection(self) -> "WorkflowSessionV1CommandAckTaskState":
        if (self.command_type == "message") != (self.rejection_reason is not None):
            raise ValueError("Only rejected messages use a skill-loading command acknowledgement")
        return self


class _WorkflowSessionEventModel(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)


class WorkflowSessionHistoryEntryEvent(_WorkflowSessionEventModel):
    type: Literal[WorkflowSessionEventType.HISTORY_ENTRY] = WorkflowSessionEventType.HISTORY_ENTRY
    entry: HistoryEntry


class WorkflowSessionStatusChangedEvent(_WorkflowSessionEventModel):
    type: Literal[WorkflowSessionEventType.SESSION_STATUS_CHANGED] = WorkflowSessionEventType.SESSION_STATUS_CHANGED
    status: WorkflowSessionStatus
    reason: str | None = None


class WorkflowSessionSubtaskStartedEvent(_WorkflowSessionEventModel):
    type: Literal[WorkflowSessionEventType.SUBTASK_STARTED] = WorkflowSessionEventType.SUBTASK_STARTED
    entry_path: str = Field(alias="entryPath")
    shell: TaskResultHistoryEntry


class WorkflowSessionSubtaskResultEvent(_WorkflowSessionEventModel):
    type: Literal[WorkflowSessionEventType.SUBTASK_RESULT] = WorkflowSessionEventType.SUBTASK_RESULT
    entry_path: str = Field(alias="entryPath")
    output: TaskOutputPayload
    generation_status: GenerationStatus = Field(
        default=GenerationStatus.COMPLETE,
        alias="generationStatus",
    )


type WorkflowSessionEvent = Annotated[
    WorkflowSessionHistoryEntryEvent
    | WorkflowSessionStatusChangedEvent
    | WorkflowSessionSubtaskStartedEvent
    | WorkflowSessionSubtaskResultEvent,
    Field(discriminator="type"),
]

WorkflowSessionEventAdapter: TypeAdapter[WorkflowSessionEvent] = TypeAdapter(WorkflowSessionEvent)


__all__ = [
    "SESSION_EVENT_TASK_TYPE",
    "SESSION_V1_ARTIFACT_TASK_TYPE",
    "SESSION_V1_COMMAND_ACK_TASK_TYPE",
    "SESSION_V1_EVENT_TASK_TYPE",
    "SESSION_V1_PROMPT_SUGGESTION_TASK_TYPE",
    "SESSION_V1_STATUS_EVENT_TASK_TYPE",
    "SESSION_V1_TURN_EVENT_TASK_TYPE",
    "WorkflowSessionEventType",
    "WorkflowSessionStatus",
    "WorkflowSessionEvent",
    "WorkflowSessionEventAdapter",
    "WorkflowSessionHistoryEntryEvent",
    "WorkflowSessionStatusChangedEvent",
    "WorkflowSessionSubtaskResultEvent",
    "WorkflowSessionSubtaskStartedEvent",
    "WorkflowSessionV1CommandAckTaskState",
]
