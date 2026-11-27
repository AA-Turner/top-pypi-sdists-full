from typing import Any
from unittest.mock import AsyncMock

from pydantic import TypeAdapter

from mistralai.workflows.protocol.v1.events import (
    ActivityTaskCompleted,
    ActivityTaskCompletedAttributes,
    ActivityTaskStarted,
    ActivityTaskStartedAttributes,
    CustomTaskCompleted,
    CustomTaskCompletedAttributes,
    CustomTaskFailed,
    CustomTaskFailedAttributes,
    CustomTaskInProgress,
    CustomTaskInProgressAttributes,
    CustomTaskStarted,
    CustomTaskStartedAttributes,
    Failure,
    JSONPayload,
    Payload,
    WorkflowEvent,
    WorkflowEventCategory,
    WorkflowExecutionCanceled,
    WorkflowExecutionCanceledAttributes,
    WorkflowExecutionCompleted,
    WorkflowExecutionCompletedAttributes,
    WorkflowExecutionFailed,
    WorkflowExecutionFailedAttributes,
    WorkflowExecutionStarted,
    WorkflowExecutionStartedAttributes,
)

ALL_EVENT_CATEGORIES: frozenset[WorkflowEventCategory] = frozenset(WorkflowEventCategory)


def workflow_started(
    workflow_name: str = "",
    payload: dict[str, Any] | None = None,
) -> WorkflowExecutionStarted:
    return WorkflowExecutionStarted(
        event_id="",
        event_timestamp=0,
        root_workflow_exec_id="",
        workflow_exec_id="",
        workflow_run_id="",
        workflow_name=workflow_name,
        attributes=WorkflowExecutionStartedAttributes(
            task_id="",
            workflow_name=workflow_name,
            input=JSONPayload(value=payload or {}),
        ),
    )


def workflow_completed(
    workflow_name: str = "",
    result: dict[str, Any] | None = None,
) -> WorkflowExecutionCompleted:
    return WorkflowExecutionCompleted(
        event_id="",
        event_timestamp=0,
        root_workflow_exec_id="",
        workflow_exec_id="",
        workflow_run_id="",
        workflow_name=workflow_name,
        attributes=WorkflowExecutionCompletedAttributes(
            task_id="",
            result=JSONPayload(value=result or {}),
        ),
    )


def workflow_canceled(
    workflow_name: str = "",
    reason: str | None = None,
) -> WorkflowExecutionCanceled:
    return WorkflowExecutionCanceled(
        event_id="",
        event_timestamp=0,
        root_workflow_exec_id="",
        workflow_exec_id="",
        workflow_run_id="",
        workflow_name=workflow_name,
        attributes=WorkflowExecutionCanceledAttributes(
            task_id="",
            reason=reason,
        ),
    )


def workflow_failed(
    workflow_name: str = "",
    error_message: str = "",
) -> WorkflowExecutionFailed:
    return WorkflowExecutionFailed(
        event_id="",
        event_timestamp=0,
        root_workflow_exec_id="",
        workflow_exec_id="",
        workflow_run_id="",
        workflow_name=workflow_name,
        attributes=WorkflowExecutionFailedAttributes(
            task_id="",
            failure=Failure(message=error_message),
        ),
    )


def activity_started(
    activity_name: str = "",
    payload: dict[str, Any] | None = None,
    workflow_name: str = "",
) -> ActivityTaskStarted:
    return ActivityTaskStarted(
        event_id="",
        event_timestamp=0,
        root_workflow_exec_id="",
        workflow_exec_id="",
        workflow_run_id="",
        workflow_name=workflow_name,
        attributes=ActivityTaskStartedAttributes(
            task_id="",
            activity_name=activity_name,
            input=JSONPayload(value=payload or {}),
        ),
    )


def activity_completed(
    activity_name: str = "",
    result: dict[str, Any] | None = None,
    workflow_name: str = "",
) -> ActivityTaskCompleted:
    return ActivityTaskCompleted(
        event_id="",
        event_timestamp=0,
        root_workflow_exec_id="",
        workflow_exec_id="",
        workflow_run_id="",
        workflow_name=workflow_name,
        attributes=ActivityTaskCompletedAttributes(
            task_id="",
            activity_name=activity_name,
            result=JSONPayload(value=result or {}),
        ),
    )


def custom_task_started(
    custom_task_type: str,
    payload: dict[str, Any] | None = None,
    workflow_name: str = "",
) -> CustomTaskStarted:
    return CustomTaskStarted(
        event_id="",
        event_timestamp=0,
        root_workflow_exec_id="",
        workflow_exec_id="",
        workflow_run_id="",
        workflow_name=workflow_name,
        attributes=CustomTaskStartedAttributes(
            custom_task_id="",
            custom_task_type=custom_task_type,
            payload=JSONPayload(value=payload or {}),
        ),
    )


def custom_task_in_progress(
    custom_task_type: str,
    payload: Payload,
    workflow_name: str = "",
) -> CustomTaskInProgress:
    return CustomTaskInProgress(
        event_id="",
        event_timestamp=0,
        root_workflow_exec_id="",
        workflow_exec_id="",
        workflow_run_id="",
        workflow_name=workflow_name,
        attributes=CustomTaskInProgressAttributes(
            custom_task_id="",
            custom_task_type=custom_task_type,
            payload=payload,
        ),
    )


def custom_task_completed(
    custom_task_type: str,
    payload: dict[str, Any] | None = None,
    workflow_name: str = "",
) -> CustomTaskCompleted:
    return CustomTaskCompleted(
        event_id="",
        event_timestamp=0,
        root_workflow_exec_id="",
        workflow_exec_id="",
        workflow_run_id="",
        workflow_name=workflow_name,
        attributes=CustomTaskCompletedAttributes(
            custom_task_id="",
            custom_task_type=custom_task_type,
            payload=JSONPayload(value=payload or {}),
        ),
    )


def custom_task_failed(
    custom_task_type: str,
    error_message: str = "",
    workflow_name: str = "",
) -> CustomTaskFailed:
    return CustomTaskFailed(
        event_id="",
        event_timestamp=0,
        root_workflow_exec_id="",
        workflow_exec_id="",
        workflow_run_id="",
        workflow_name=workflow_name,
        attributes=CustomTaskFailedAttributes(
            custom_task_id="",
            custom_task_type=custom_task_type,
            failure=Failure(message=error_message),
        ),
    )


_event_adapter: TypeAdapter[WorkflowEvent] = TypeAdapter(WorkflowEvent)


def create_capturing_mock_event_publisher(captured_events: list[Any]) -> AsyncMock:
    """Create a mock event publisher that captures WorkflowEvent objects."""
    mock_publisher = AsyncMock()

    async def capture_publish(events: list[Any]) -> None:
        for event in events:
            captured_events.append(_event_adapter.validate_python(event))

    mock_publisher.publish = AsyncMock(side_effect=capture_publish)
    return mock_publisher
