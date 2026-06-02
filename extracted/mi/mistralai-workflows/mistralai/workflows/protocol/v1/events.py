import time
from enum import StrEnum
from typing import Annotated, Any, Literal, TypedDict

import temporalio.workflow
from mistralai.extra.workflows.encoding.models import EncodedPayloadOptions
from pydantic import BaseModel, ConfigDict, Discriminator, Field, Tag
from typing_extensions import TypeAliasType


class WorkflowEventType(StrEnum):
    WORKFLOW_EXECUTION_STARTED = "WORKFLOW_EXECUTION_STARTED"
    WORKFLOW_EXECUTION_COMPLETED = "WORKFLOW_EXECUTION_COMPLETED"
    WORKFLOW_EXECUTION_FAILED = "WORKFLOW_EXECUTION_FAILED"
    WORKFLOW_EXECUTION_CANCELED = "WORKFLOW_EXECUTION_CANCELED"
    WORKFLOW_EXECUTION_CONTINUED_AS_NEW = "WORKFLOW_EXECUTION_CONTINUED_AS_NEW"
    WORKFLOW_TASK_TIMED_OUT = "WORKFLOW_TASK_TIMED_OUT"
    WORKFLOW_TASK_FAILED = "WORKFLOW_TASK_FAILED"
    CUSTOM_TASK_STARTED = "CUSTOM_TASK_STARTED"
    CUSTOM_TASK_IN_PROGRESS = "CUSTOM_TASK_IN_PROGRESS"
    CUSTOM_TASK_COMPLETED = "CUSTOM_TASK_COMPLETED"
    CUSTOM_TASK_FAILED = "CUSTOM_TASK_FAILED"
    CUSTOM_TASK_TIMED_OUT = "CUSTOM_TASK_TIMED_OUT"
    CUSTOM_TASK_CANCELED = "CUSTOM_TASK_CANCELED"
    ACTIVITY_TASK_STARTED = "ACTIVITY_TASK_STARTED"
    ACTIVITY_TASK_COMPLETED = "ACTIVITY_TASK_COMPLETED"
    ACTIVITY_TASK_RETRYING = "ACTIVITY_TASK_RETRYING"
    ACTIVITY_TASK_FAILED = "ACTIVITY_TASK_FAILED"


class EncryptedPatchValue(TypedDict):
    """Wrapper for encrypted patch values in selective json_patch encryption.

    When partial encryption mode is enabled and a patch targets an EncryptedStrField,
    the patch value is encrypted and wrapped in this structure.

    The type field acts as a discriminator to distinguish this from user data.
    """

    type: Literal["__encrypted__"]
    value: str


class JSONPatchBase(BaseModel):
    """
    A single JSON Patch operation as defined in RFC 6902, with extensions.

    Used for incremental updates to JSON documents without replacing the entire payload.

    Extensions beyond RFC 6902:
    - "append" operation: Optimized string concatenation for streaming text updates.
    - path can be an empty list [] for root-level operations (mutative compatibility).
    """

    path: str = Field(
        description="A JSON Pointer (RFC 6901) identifying the target location within the document. "
        "Can be a string path (e.g., '/foo/bar'), '/', '', or an empty list [] for root-level operations."
    )
    value: Any = Field(description="The value to use for the operation")


class JSONPatchAdd(JSONPatchBase):
    op: Literal["add"] = Field(description="Add operation ")


class JSONPatchReplace(JSONPatchBase):
    op: Literal["replace"] = Field(description="Replace operation")


class JSONPatchRemove(JSONPatchBase):
    op: Literal["remove"] = Field(description="Remove operation")


class JSONPatchAppend(JSONPatchBase):
    op: Literal["append"] = Field(
        description="'append' is an extension for efficient string concatenation in streaming scenarios."
    )
    value: str | EncryptedPatchValue = Field(
        description="The value to use for the operation. A string to append to the existing value, "
        "or an EncryptedPatchValue wrapper when encryption is applied."
    )


JSONPatch = TypeAliasType(
    "JSONPatch",
    Annotated[
        Annotated[JSONPatchAppend, Tag("append")]
        | Annotated[JSONPatchAdd, Tag("add")]
        | Annotated[JSONPatchReplace, Tag("replace")]
        | Annotated[JSONPatchRemove, Tag("remove")],
        Discriminator("op"),
    ],
)

JSONPatchPayloadValue = TypeAliasType("JSONPatchPayloadValue", list[JSONPatch] | str)


def json_patch(op: str, path: str, value: Any) -> JSONPatch:
    if op == "add":
        return JSONPatchAdd(op="add", path=path, value=value)
    elif op == "replace":
        return JSONPatchReplace(op="replace", path=path, value=value)
    elif op == "remove":
        return JSONPatchRemove(op="remove", path=path, value=value)
    elif op == "append":
        return JSONPatchAppend(op="append", path=path, value=value)
    else:
        raise ValueError(f"Unknown operation: {op}")


def _make_encoding_options_optional(schema: dict[str, Any]) -> None:
    """Remove encoding_options from required fields in the JSON schema.

    json_schema_serialization_defaults_required makes all fields with defaults (e.g. type)
    required in the serialization schema. encoding_options must stay optional for backward
    compatibility since it only exists when encryption is active.
    """
    required = schema.get("required", [])
    if "encoding_options" in required:
        required.remove("encoding_options")


_PAYLOAD_MODEL_CONFIG = ConfigDict(
    json_schema_serialization_defaults_required=True,
    json_schema_extra=_make_encoding_options_optional,
)

_ENCODING_OPTIONS_FIELD = Field(
    default=None,
    description="Encoding options applied to the payload.",
)


class JSONPatchPayload(BaseModel):
    """A payload containing a list of JSON Patch operations.

    Used for streaming incremental updates to workflow state.
    When encrypted, the value field contains base64-encoded encrypted data
    and encoding_options indicates the type of encryption applied.
    """

    type: Literal["json_patch"] = Field(
        default="json_patch",
        description="Discriminator indicating this is a JSON Patch payload.",
    )
    value: JSONPatchPayloadValue = Field(
        description="The list of JSON Patch operations. When encrypted, contains base64-encoded data."
    )
    encoding_options: list[EncodedPayloadOptions] | None = _ENCODING_OPTIONS_FIELD

    model_config = _PAYLOAD_MODEL_CONFIG


class JSONPayload(BaseModel):
    """A payload containing arbitrary JSON data.

    Used for complete state snapshots or final results.
    When encrypted, the value field contains base64-encoded encrypted data
    and encoding_options indicates the type of encryption applied.
    """

    type: Literal["json"] = Field(
        default="json",
        description="Discriminator indicating this is a raw JSON payload.",
    )
    value: Any = Field(description="The JSON-serializable payload value. When encrypted, contains base64-encoded data.")
    encoding_options: list[EncodedPayloadOptions] | None = _ENCODING_OPTIONS_FIELD

    model_config = _PAYLOAD_MODEL_CONFIG


Payload = Annotated[
    Annotated[JSONPayload, Tag("json")] | Annotated[JSONPatchPayload, Tag("json_patch")],
    Discriminator("type"),
]
"""Union type for payload data, discriminated by the 'type' field."""


class Failure(BaseModel):
    """Represents an error or exception that occurred during execution."""

    message: str = Field(description="A human-readable description of the failure.")


def _get_timestamp_ns() -> int:
    """Get current timestamp in nanoseconds, workflow-safe."""
    if temporalio.workflow.in_workflow():
        return temporalio.workflow.time_ns()
    return time.time_ns()


class BaseEvent(BaseModel):
    """
    Base class for all workflow events.

    All events share common identification and timing fields to enable
    correlation and ordering across distributed workflow executions.
    """

    event_id: str = Field(description="Unique identifier for this event instance.")
    event_timestamp: int = Field(
        default_factory=_get_timestamp_ns,
        description="Unix timestamp in nanoseconds when the event was created.",
    )
    root_workflow_exec_id: str = Field(
        description="Execution ID of the root workflow that initiated this execution chain."
    )
    parent_workflow_exec_id: str | None = Field(
        default=None,
        description="Execution ID of the parent workflow that initiated this execution. "
        "If this is a root workflow, this field is not set.",
    )
    workflow_exec_id: str = Field(description="Execution ID of the workflow that emitted this event.")
    workflow_run_id: str = Field(
        description="Run ID of the workflow execution. "
        "Changes on continue-as-new while workflow_exec_id stays the same."
    )
    workflow_name: str = Field(description="The registered name of the workflow that emitted this event.")

    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class BaseTaskAttributes(BaseModel):
    """Base attributes shared by all workflow task events."""

    task_id: str = Field(description="Unique identifier for the task within the workflow execution.")


class WorkflowExecutionStartedAttributes(BaseTaskAttributes):
    """Attributes for workflow execution started events."""

    workflow_name: str = Field(description="The registered name of the workflow being executed.")
    display_name: str | None = Field(
        default=None,
        description="The user-friendly display name of the workflow, if available.",
    )
    input: JSONPayload = Field(description="The input arguments passed to the workflow.")


class WorkflowExecutionCompletedAttributes(BaseTaskAttributes):
    """Attributes for workflow execution completed events."""

    result: JSONPayload = Field(description="The final result returned by the workflow.")


class WorkflowExecutionFailedAttributes(BaseTaskAttributes):
    """Attributes for workflow execution failed events."""

    failure: Failure = Field(description="Details about the failure that caused the workflow to fail.")


class WorkflowExecutionCanceledAttributes(BaseTaskAttributes):
    """Attributes for workflow execution canceled events."""

    reason: str | None = Field(
        default=None,
        description="Optional reason provided for the cancellation.",
    )


class WorkflowExecutionContinuedAsNewAttributes(BaseTaskAttributes):
    """Attributes for workflow execution continued-as-new events."""

    new_execution_run_id: str = Field(
        description="The run ID of the new workflow execution that continues this workflow."
    )
    workflow_name: str = Field(description="The registered name of the continued workflow.")
    input: JSONPayload = Field(description="The input arguments passed to the new workflow execution.")


class WorkflowTaskTimedOutAttributes(BaseTaskAttributes):
    """Attributes for workflow task timed out events."""

    timeout_type: str | None = Field(
        default=None,
        description="The type of timeout that occurred (e.g., 'START_TO_CLOSE', 'SCHEDULE_TO_START').",
    )


class WorkflowTaskFailedAttributes(BaseTaskAttributes):
    """Attributes for workflow task failed events."""

    failure: Failure = Field(description="Details about the failure that caused the task to fail.")


class BaseCustomTaskAttributes(BaseModel):
    """Base attributes shared by all custom task events."""

    custom_task_id: str = Field(description="Unique identifier for the custom task within the workflow.")
    custom_task_type: str = Field(description="The type/category of the custom task (e.g., 'llm_call', 'api_request').")


class CustomTaskStartedAttributes(BaseCustomTaskAttributes):
    """Attributes for custom task started events."""

    payload: JSONPayload = Field(
        default_factory=lambda: JSONPayload(value=None), description="The initial state or payload for the custom task."
    )


class CustomTaskInProgressAttributes(BaseCustomTaskAttributes):
    """Attributes for custom task in-progress events with streaming updates."""

    payload: Payload = Field(description="The current state or incremental update for the task.")


class CustomTaskCompletedAttributes(BaseCustomTaskAttributes):
    """Attributes for custom task completed events."""

    payload: JSONPayload = Field(description="The final result of the custom task.")


class CustomTaskFailedAttributes(BaseCustomTaskAttributes):
    """Attributes for custom task failed events."""

    failure: Failure = Field(description="Details about the failure that caused the task to fail.")


class CustomTaskTimedOutAttributes(BaseCustomTaskAttributes):
    """Attributes for custom task timed out events."""

    timeout_type: str | None = Field(
        default=None,
        description="The type of timeout that occurred.",
    )


class CustomTaskCanceledAttributes(BaseCustomTaskAttributes):
    """Attributes for custom task canceled events."""

    reason: str | None = Field(
        default=None,
        description="Optional reason provided for the cancellation.",
    )


class BaseActivityTaskAttributes(BaseModel):
    """Base attributes shared by all activity task events."""

    task_id: str = Field(description="Unique identifier for the activity task within the workflow.")
    activity_name: str = Field(description="The registered name of the activity being executed.")


class ActivityTaskStartedAttributes(BaseActivityTaskAttributes):
    """Attributes for activity task started events."""

    input: JSONPayload = Field(description="The input arguments passed to the activity.")


class ActivityTaskCompletedAttributes(BaseActivityTaskAttributes):
    """Attributes for activity task completed events."""

    result: JSONPayload = Field(description="The result returned by the activity.")


class ActivityTaskRetryingAttributes(BaseActivityTaskAttributes):
    """Attributes for activity task retrying events."""

    attempt: int = Field(description="The attempt number that failed (1-indexed).")
    failure: Failure = Field(description="Details about the failure that caused the retry.")


class ActivityTaskFailedAttributes(BaseActivityTaskAttributes):
    """Attributes for activity task failed events (final failure after all retries)."""

    attempt: int = Field(description="The final attempt number that failed (1-indexed).")
    failure: Failure = Field(description="Details about the failure that caused the activity to fail.")


class WorkflowExecutionStarted(BaseEvent):
    """
    Emitted when a workflow execution begins.

    This is the first event in any workflow execution lifecycle.
    """

    event_type: Literal[WorkflowEventType.WORKFLOW_EXECUTION_STARTED] = Field(
        default=WorkflowEventType.WORKFLOW_EXECUTION_STARTED,
        description="Event type discriminator.",
    )
    attributes: WorkflowExecutionStartedAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class WorkflowExecutionCompleted(BaseEvent):
    """
    Emitted when a workflow execution completes successfully.

    This is a terminal event indicating the workflow finished without errors.
    """

    event_type: Literal[WorkflowEventType.WORKFLOW_EXECUTION_COMPLETED] = Field(
        default=WorkflowEventType.WORKFLOW_EXECUTION_COMPLETED,
        description="Event type discriminator.",
    )
    attributes: WorkflowExecutionCompletedAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class WorkflowExecutionFailed(BaseEvent):
    """
    Emitted when a workflow execution fails due to an unhandled exception.

    This is a terminal event indicating the workflow ended with an error.
    """

    event_type: Literal[WorkflowEventType.WORKFLOW_EXECUTION_FAILED] = Field(
        default=WorkflowEventType.WORKFLOW_EXECUTION_FAILED,
        description="Event type discriminator.",
    )
    attributes: WorkflowExecutionFailedAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class WorkflowExecutionCanceled(BaseEvent):
    """
    Emitted when a workflow execution is canceled.

    This is a terminal event indicating the workflow was explicitly canceled.
    """

    event_type: Literal[WorkflowEventType.WORKFLOW_EXECUTION_CANCELED] = Field(
        default=WorkflowEventType.WORKFLOW_EXECUTION_CANCELED,
        description="Event type discriminator.",
    )
    attributes: WorkflowExecutionCanceledAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class WorkflowExecutionContinuedAsNew(BaseEvent):
    """
    Emitted when a workflow continues as a new execution.

    This occurs when a workflow uses continue-as-new to reset its history
    while maintaining logical continuity.
    """

    event_type: Literal[WorkflowEventType.WORKFLOW_EXECUTION_CONTINUED_AS_NEW] = Field(
        default=WorkflowEventType.WORKFLOW_EXECUTION_CONTINUED_AS_NEW,
        description="Event type discriminator.",
    )
    attributes: WorkflowExecutionContinuedAsNewAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class WorkflowTaskTimedOut(BaseEvent):
    """
    Emitted when a workflow task times out.

    This indicates the workflow task (a unit of workflow execution) exceeded
    its configured timeout.
    """

    event_type: Literal[WorkflowEventType.WORKFLOW_TASK_TIMED_OUT] = Field(
        default=WorkflowEventType.WORKFLOW_TASK_TIMED_OUT,
        description="Event type discriminator.",
    )
    attributes: WorkflowTaskTimedOutAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class WorkflowTaskFailed(BaseEvent):
    """
    Emitted when a workflow task fails.

    This indicates an error occurred during workflow task execution,
    which may trigger a retry depending on configuration.
    """

    event_type: Literal[WorkflowEventType.WORKFLOW_TASK_FAILED] = Field(
        default=WorkflowEventType.WORKFLOW_TASK_FAILED,
        description="Event type discriminator.",
    )
    attributes: WorkflowTaskFailedAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class CustomTaskStarted(BaseEvent):
    """
    Emitted when a custom task begins execution.

    Custom tasks represent user-defined units of work within a workflow,
    such as LLM calls, API requests, or data processing steps.
    """

    event_type: Literal[WorkflowEventType.CUSTOM_TASK_STARTED] = Field(
        default=WorkflowEventType.CUSTOM_TASK_STARTED,
        description="Event type discriminator.",
    )
    attributes: CustomTaskStartedAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class CustomTaskInProgress(BaseEvent):
    """
    Emitted during custom task execution to report progress.

    This event supports streaming updates via JSON or JSON Patch payloads,
    enabling real-time progress tracking for long-running tasks.
    """

    event_type: Literal[WorkflowEventType.CUSTOM_TASK_IN_PROGRESS] = Field(
        default=WorkflowEventType.CUSTOM_TASK_IN_PROGRESS,
        description="Event type discriminator.",
    )
    attributes: CustomTaskInProgressAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class CustomTaskCompleted(BaseEvent):
    """
    Emitted when a custom task completes successfully.

    Contains the final result of the task execution.
    """

    event_type: Literal[WorkflowEventType.CUSTOM_TASK_COMPLETED] = Field(
        default=WorkflowEventType.CUSTOM_TASK_COMPLETED,
        description="Event type discriminator.",
    )
    attributes: CustomTaskCompletedAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class CustomTaskFailed(BaseEvent):
    """
    Emitted when a custom task fails.

    Contains details about the failure for debugging and error handling.
    """

    event_type: Literal[WorkflowEventType.CUSTOM_TASK_FAILED] = Field(
        default=WorkflowEventType.CUSTOM_TASK_FAILED,
        description="Event type discriminator.",
    )
    attributes: CustomTaskFailedAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class CustomTaskTimedOut(BaseEvent):
    """
    Emitted when a custom task exceeds its timeout.

    Indicates the task did not complete within its configured time limit.
    """

    event_type: Literal[WorkflowEventType.CUSTOM_TASK_TIMED_OUT] = Field(
        default=WorkflowEventType.CUSTOM_TASK_TIMED_OUT,
        description="Event type discriminator.",
    )
    attributes: CustomTaskTimedOutAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class CustomTaskCanceled(BaseEvent):
    """
    Emitted when a custom task is canceled.

    Indicates the task was explicitly stopped before completion.
    """

    event_type: Literal[WorkflowEventType.CUSTOM_TASK_CANCELED] = Field(
        default=WorkflowEventType.CUSTOM_TASK_CANCELED,
        description="Event type discriminator.",
    )
    attributes: CustomTaskCanceledAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class ActivityTaskStarted(BaseEvent):
    """
    Emitted when an activity task begins execution.

    This is the first event for an activity, emitted on the first attempt only.
    Subsequent retry attempts emit ACTIVITY_TASK_RETRYING instead.
    """

    event_type: Literal[WorkflowEventType.ACTIVITY_TASK_STARTED] = Field(
        default=WorkflowEventType.ACTIVITY_TASK_STARTED,
        description="Event type discriminator.",
    )
    attributes: ActivityTaskStartedAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class ActivityTaskCompleted(BaseEvent):
    """
    Emitted when an activity task completes successfully.

    Contains timing information about the successful execution.
    """

    event_type: Literal[WorkflowEventType.ACTIVITY_TASK_COMPLETED] = Field(
        default=WorkflowEventType.ACTIVITY_TASK_COMPLETED,
        description="Event type discriminator.",
    )
    attributes: ActivityTaskCompletedAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class ActivityTaskRetrying(BaseEvent):
    """
    Emitted when an activity task fails and will be retried.

    Contains information about the failed attempt and the error that occurred.
    """

    event_type: Literal[WorkflowEventType.ACTIVITY_TASK_RETRYING] = Field(
        default=WorkflowEventType.ACTIVITY_TASK_RETRYING,
        description="Event type discriminator.",
    )
    attributes: ActivityTaskRetryingAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


class ActivityTaskFailed(BaseEvent):
    """
    Emitted when an activity task fails after exhausting all retry attempts.

    This is a terminal event indicating the activity could not complete successfully.
    """

    event_type: Literal[WorkflowEventType.ACTIVITY_TASK_FAILED] = Field(
        default=WorkflowEventType.ACTIVITY_TASK_FAILED,
        description="Event type discriminator.",
    )
    attributes: ActivityTaskFailedAttributes = Field(description="Event-specific attributes.")
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)


def _get_event_type_discriminator(v: Any) -> str:
    """Extract event type for discriminated union parsing."""
    if isinstance(v, dict):
        event_type_val = v.get("event_type", "")
        # Handle both string and WorkflowEventType enum values
        if isinstance(event_type_val, WorkflowEventType):
            return event_type_val.value
        return str(event_type_val)

    event_type_attr = getattr(v, "event_type", "")
    if isinstance(event_type_attr, WorkflowEventType):
        return event_type_attr.value
    return str(event_type_attr)


WorkflowExecutionEvent = Annotated[
    Annotated[WorkflowExecutionStarted, Tag(WorkflowEventType.WORKFLOW_EXECUTION_STARTED.value)]
    | Annotated[WorkflowExecutionCompleted, Tag(WorkflowEventType.WORKFLOW_EXECUTION_COMPLETED.value)]
    | Annotated[WorkflowExecutionFailed, Tag(WorkflowEventType.WORKFLOW_EXECUTION_FAILED.value)]
    | Annotated[WorkflowExecutionCanceled, Tag(WorkflowEventType.WORKFLOW_EXECUTION_CANCELED.value)]
    | Annotated[WorkflowExecutionContinuedAsNew, Tag(WorkflowEventType.WORKFLOW_EXECUTION_CONTINUED_AS_NEW.value)]
    | Annotated[WorkflowTaskTimedOut, Tag(WorkflowEventType.WORKFLOW_TASK_TIMED_OUT.value)]
    | Annotated[WorkflowTaskFailed, Tag(WorkflowEventType.WORKFLOW_TASK_FAILED.value)],
    Discriminator(_get_event_type_discriminator),
]
"""
Union of all workflow execution events, discriminated by 'event_type'.

Use this type when parsing workflow lifecycle events.
"""


CustomTaskEvent = Annotated[
    Annotated[CustomTaskStarted, Tag(WorkflowEventType.CUSTOM_TASK_STARTED.value)]
    | Annotated[CustomTaskInProgress, Tag(WorkflowEventType.CUSTOM_TASK_IN_PROGRESS.value)]
    | Annotated[CustomTaskCompleted, Tag(WorkflowEventType.CUSTOM_TASK_COMPLETED.value)]
    | Annotated[CustomTaskFailed, Tag(WorkflowEventType.CUSTOM_TASK_FAILED.value)]
    | Annotated[CustomTaskTimedOut, Tag(WorkflowEventType.CUSTOM_TASK_TIMED_OUT.value)]
    | Annotated[CustomTaskCanceled, Tag(WorkflowEventType.CUSTOM_TASK_CANCELED.value)],
    Discriminator(_get_event_type_discriminator),
]
"""
Union of all custom task events, discriminated by 'event_type'.

Use this type when parsing custom task lifecycle events.
"""


ActivityTaskEvent = Annotated[
    Annotated[ActivityTaskStarted, Tag(WorkflowEventType.ACTIVITY_TASK_STARTED.value)]
    | Annotated[ActivityTaskCompleted, Tag(WorkflowEventType.ACTIVITY_TASK_COMPLETED.value)]
    | Annotated[ActivityTaskRetrying, Tag(WorkflowEventType.ACTIVITY_TASK_RETRYING.value)]
    | Annotated[ActivityTaskFailed, Tag(WorkflowEventType.ACTIVITY_TASK_FAILED.value)],
    Discriminator(_get_event_type_discriminator),
]
"""
Union of all activity task events, discriminated by 'event_type'.

Use this type when parsing activity task lifecycle events.
"""


WorkflowEvent = Annotated[
    Annotated[WorkflowExecutionStarted, Tag(WorkflowEventType.WORKFLOW_EXECUTION_STARTED.value)]
    | Annotated[WorkflowExecutionCompleted, Tag(WorkflowEventType.WORKFLOW_EXECUTION_COMPLETED.value)]
    | Annotated[WorkflowExecutionFailed, Tag(WorkflowEventType.WORKFLOW_EXECUTION_FAILED.value)]
    | Annotated[WorkflowExecutionCanceled, Tag(WorkflowEventType.WORKFLOW_EXECUTION_CANCELED.value)]
    | Annotated[WorkflowExecutionContinuedAsNew, Tag(WorkflowEventType.WORKFLOW_EXECUTION_CONTINUED_AS_NEW.value)]
    | Annotated[WorkflowTaskTimedOut, Tag(WorkflowEventType.WORKFLOW_TASK_TIMED_OUT.value)]
    | Annotated[WorkflowTaskFailed, Tag(WorkflowEventType.WORKFLOW_TASK_FAILED.value)]
    | Annotated[CustomTaskStarted, Tag(WorkflowEventType.CUSTOM_TASK_STARTED.value)]
    | Annotated[CustomTaskInProgress, Tag(WorkflowEventType.CUSTOM_TASK_IN_PROGRESS.value)]
    | Annotated[CustomTaskCompleted, Tag(WorkflowEventType.CUSTOM_TASK_COMPLETED.value)]
    | Annotated[CustomTaskFailed, Tag(WorkflowEventType.CUSTOM_TASK_FAILED.value)]
    | Annotated[CustomTaskTimedOut, Tag(WorkflowEventType.CUSTOM_TASK_TIMED_OUT.value)]
    | Annotated[CustomTaskCanceled, Tag(WorkflowEventType.CUSTOM_TASK_CANCELED.value)]
    | Annotated[ActivityTaskStarted, Tag(WorkflowEventType.ACTIVITY_TASK_STARTED.value)]
    | Annotated[ActivityTaskCompleted, Tag(WorkflowEventType.ACTIVITY_TASK_COMPLETED.value)]
    | Annotated[ActivityTaskRetrying, Tag(WorkflowEventType.ACTIVITY_TASK_RETRYING.value)]
    | Annotated[ActivityTaskFailed, Tag(WorkflowEventType.ACTIVITY_TASK_FAILED.value)],
    Discriminator(_get_event_type_discriminator),
]
"""
Union of all workflow events (execution + custom task + activity task), discriminated by 'event_type'.

This is the primary type for parsing any event from the workflow event stream.

Example:
    ```python
    from pydantic import TypeAdapter

    event_adapter = TypeAdapter(WorkflowEvent)
    event = event_adapter.validate_python(event_dict)
    ```
"""


class WorkflowEventRequest(BaseModel):
    """Request model containing a workflow event."""

    event: WorkflowEvent = Field(description="The workflow event payload.")


class ListWorkflowEventResponse(BaseModel):
    events: list[WorkflowEvent] = Field(description="List of workflow events.")
    next_cursor: str | None = Field(default=None, description="Cursor for pagination.")


class WorkflowEventResponse(BaseModel):
    """Response model for workflow event reception."""

    status: Literal["success", "error"] = Field(description="Status of the event reception")
    message: str | None = Field(default=None, description="Optional message")


class WorkflowEventBatchRequest(BaseModel):
    """Request model containing multiple workflow events."""

    events: list[WorkflowEvent] = Field(description="List of workflow events to send.")


class WorkflowEventBatchResponse(BaseModel):
    """Response model for batch workflow event reception."""

    status: Literal["success", "error"] = Field(description="Status of the batch event reception")
    message: str | None = Field(default=None, description="Optional message")
    events_received: int = Field(description="Number of events successfully received")


class EventSource(StrEnum):
    DATABASE = "DATABASE"
    LIVE = "LIVE"
    HYBRID = "HYBRID"


__all__ = [
    # Enums
    "WorkflowEventType",
    # Payload models
    "EncryptedPatchValue",
    "JSONPatch",
    "JSONPatchPayload",
    "JSONPayload",
    "Payload",
    # Failure model
    "Failure",
    # Base models
    "BaseEvent",
    "BaseTaskAttributes",
    "BaseCustomTaskAttributes",
    "BaseActivityTaskAttributes",
    # Workflow execution attributes
    "WorkflowExecutionStartedAttributes",
    "WorkflowExecutionCompletedAttributes",
    "WorkflowExecutionFailedAttributes",
    "WorkflowExecutionCanceledAttributes",
    "WorkflowExecutionContinuedAsNewAttributes",
    "WorkflowTaskTimedOutAttributes",
    "WorkflowTaskFailedAttributes",
    # Custom task attributes
    "CustomTaskStartedAttributes",
    "CustomTaskInProgressAttributes",
    "CustomTaskCompletedAttributes",
    "CustomTaskFailedAttributes",
    "CustomTaskTimedOutAttributes",
    "CustomTaskCanceledAttributes",
    # Activity task attributes
    "ActivityTaskStartedAttributes",
    "ActivityTaskCompletedAttributes",
    "ActivityTaskRetryingAttributes",
    "ActivityTaskFailedAttributes",
    # Workflow execution events
    "WorkflowExecutionStarted",
    "WorkflowExecutionCompleted",
    "WorkflowExecutionFailed",
    "WorkflowExecutionCanceled",
    "WorkflowExecutionContinuedAsNew",
    "WorkflowTaskTimedOut",
    "WorkflowTaskFailed",
    # Custom task events
    "CustomTaskStarted",
    "CustomTaskInProgress",
    "CustomTaskCompleted",
    "CustomTaskFailed",
    "CustomTaskTimedOut",
    "CustomTaskCanceled",
    # Activity task events
    "ActivityTaskStarted",
    "ActivityTaskCompleted",
    "ActivityTaskRetrying",
    "ActivityTaskFailed",
    # Discriminated unions
    "WorkflowExecutionEvent",
    "CustomTaskEvent",
    "ActivityTaskEvent",
    "WorkflowEvent",
    # Request/Response models
    "WorkflowEventRequest",
    "WorkflowEventResponse",
    "WorkflowEventBatchRequest",
    "WorkflowEventBatchResponse",
]
