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
    WorkflowExecutionCanceled,
    WorkflowExecutionCanceledAttributes,
    WorkflowExecutionCompleted,
    WorkflowExecutionCompletedAttributes,
    WorkflowExecutionFailed,
    WorkflowExecutionFailedAttributes,
    WorkflowExecutionStarted,
    WorkflowExecutionStartedAttributes,
)


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


def create_capturing_mock_events_client(captured_events: list[Any]) -> AsyncMock:
    """Create a mock Events client that captures deserialized WorkflowEvent objects.

    EventContext calls send_event_async(event=<dict>) and send_events_batch_async(events=[<dict>...])
    on the Events generated client. This helper creates a mock that intercepts those calls
    and deserializes the dicts back into WorkflowEvent Pydantic objects for easy assertion in tests.
    """
    mock_client = AsyncMock()

    async def capture_send_event(*, event: Any, **kwargs: Any) -> None:
        captured_events.append(_event_adapter.validate_python(event))

    async def capture_send_events_batch(*, events: list[Any], **kwargs: Any) -> None:
        for e in events:
            captured_events.append(_event_adapter.validate_python(e))

    mock_client.send_event_async = AsyncMock(side_effect=capture_send_event)
    mock_client.send_events_batch_async = AsyncMock(side_effect=capture_send_events_batch)
    return mock_client
