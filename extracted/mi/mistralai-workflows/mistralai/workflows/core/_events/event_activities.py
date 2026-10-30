from datetime import timedelta
from typing import Any, Awaitable, Callable

import temporalio.common
import temporalio.workflow
from pydantic import BaseModel
from temporalio.exceptions import ActivityError, ApplicationError

from mistralai.workflows.core._events.event_context import (
    EVENT_PUBLISH_FAILED_ERROR_TYPE,
    EventContext,
    is_permanent_event_publish_failure,
)
from mistralai.workflows.core._events.event_utils import EMITTER_ACTIVITY_NAMES, create_emitter_event_fields
from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.config.config import INTERNAL_ACTIVITY_PREFIX
from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.protocol.v1.events import (
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

logger = get_logger(__name__)

_EMITTER_START_TO_CLOSE_TIMEOUT = timedelta(seconds=10)
# A backoff past the threshold reschedules the local activity under a new seq, which would change its event ids.
_EMITTER_LOCAL_RETRY_THRESHOLD = timedelta(seconds=60)
_EMITTER_RETRY_POLICY = temporalio.common.RetryPolicy(maximum_interval=_EMITTER_LOCAL_RETRY_THRESHOLD / 2)


def emitter_activity[T: Callable[..., Any]](name: str, **kwargs: Any) -> Callable[[T], T]:
    EMITTER_ACTIVITY_NAMES.add(name)
    return activity(name=name, **kwargs)


async def publish_emitter_event(build_event: Callable[[], WorkflowEvent]) -> None:
    context = EventContext.get_singleton()
    if context:
        await context.publish_event_or_raise(build_event())


async def execute_emitter(emitter: Callable[..., Awaitable[Any]], *args: Any) -> None:
    try:
        await temporalio.workflow.execute_local_activity(
            emitter,
            args=list(args),
            start_to_close_timeout=_EMITTER_START_TO_CLOSE_TIMEOUT,
            retry_policy=_EMITTER_RETRY_POLICY,
            local_retry_threshold=_EMITTER_LOCAL_RETRY_THRESHOLD,
        )
    except ActivityError as e:
        if not is_permanent_event_publish_failure(e.cause):
            raise
        raise ApplicationError(e.cause.message, type=EVENT_PUBLISH_FAILED_ERROR_TYPE, non_retryable=True) from e


async def execute_emitter_preserving_error(emitter: Callable[..., Awaitable[Any]], *args: Any) -> None:
    """For an event reporting an error the caller is about to raise, which a publish failure must not hide."""
    try:
        await execute_emitter(emitter, *args)
    except ApplicationError as e:
        if not is_permanent_event_publish_failure(e):
            raise
        logger.error("Failed to publish workflow event reporting an error", **extract_error_context(e))


class WaitForInputResult(BaseModel):
    task_id: str


@emitter_activity(name=f"{INTERNAL_ACTIVITY_PREFIX}emit_workflow_started", _allow_reserved_name=True)
async def _emit_workflow_started(
    task_id: str,
    workflow_name: str,
    input_args: list,
    display_name: str | None = None,
    attempt: int = 1,
) -> None:
    await publish_emitter_event(
        lambda: WorkflowExecutionStarted(
            **create_emitter_event_fields("payload"),
            attributes=WorkflowExecutionStartedAttributes(
                task_id=task_id,
                workflow_name=workflow_name,
                display_name=display_name,
                input=JSONPayload(value=input_args),
                attempt=attempt,
            ),
        )
    )


@emitter_activity(name=f"{INTERNAL_ACTIVITY_PREFIX}emit_workflow_completed", _allow_reserved_name=True)
async def _emit_workflow_completed(task_id: str, result: Any, attempt: int = 1) -> None:
    await publish_emitter_event(
        lambda: WorkflowExecutionCompleted(
            **create_emitter_event_fields("payload"),
            attributes=WorkflowExecutionCompletedAttributes(
                task_id=task_id,
                result=JSONPayload(value=result),
                attempt=attempt,
            ),
        )
    )


@emitter_activity(name=f"{INTERNAL_ACTIVITY_PREFIX}emit_workflow_canceled", _allow_reserved_name=True)
async def _emit_workflow_canceled(task_id: str, reason: str | None, attempt: int = 1) -> None:
    await publish_emitter_event(
        lambda: WorkflowExecutionCanceled(
            **create_emitter_event_fields("payload"),
            attributes=WorkflowExecutionCanceledAttributes(
                task_id=task_id,
                reason=reason,
                attempt=attempt,
            ),
        )
    )


@emitter_activity(name=f"{INTERNAL_ACTIVITY_PREFIX}emit_workflow_failed", _allow_reserved_name=True)
async def _emit_workflow_failed(task_id: str, error_message: str, attempt: int = 1) -> None:
    await publish_emitter_event(
        lambda: WorkflowExecutionFailed(
            **create_emitter_event_fields("payload"),
            attributes=WorkflowExecutionFailedAttributes(
                task_id=task_id,
                failure=Failure(message=error_message),
                attempt=attempt,
            ),
        )
    )


@emitter_activity(name="__emit_waiting_for_input_started")
async def _emit_waiting_for_input_started(
    task_id: str,
    input_schema: dict,
    label: str | None,
) -> WaitForInputResult:
    await publish_emitter_event(
        lambda: CustomTaskStarted(
            **create_emitter_event_fields("payload"),
            attributes=CustomTaskStartedAttributes(
                custom_task_id=task_id,
                custom_task_type="wait_for_input",
                payload=JSONPayload(value={"input_schema": input_schema, "label": label}),
            ),
        )
    )
    return WaitForInputResult(task_id=task_id)


@emitter_activity(name="__emit_waiting_for_input_completed")
async def _emit_waiting_for_input_completed(
    task_id: str, input_schema: dict, label: str | None, input_values: dict | None
) -> WaitForInputResult:
    await publish_emitter_event(
        lambda: CustomTaskCompleted(
            **create_emitter_event_fields("payload"),
            attributes=CustomTaskCompletedAttributes(
                custom_task_id=task_id,
                custom_task_type="wait_for_input",
                payload=JSONPayload(value={"input_schema": input_schema, "label": label, "input": input_values}),
            ),
        )
    )
    return WaitForInputResult(task_id=task_id)


@emitter_activity(name="__emit_waiting_for_input_failed")
async def _emit_waiting_for_input_failed(
    task_id: str, input_schema: dict, label: str | None, error: str
) -> WaitForInputResult:
    await publish_emitter_event(
        lambda: CustomTaskFailed(
            **create_emitter_event_fields("payload"),
            attributes=CustomTaskFailedAttributes(
                custom_task_id=task_id,
                custom_task_type="wait_for_input",
                failure=Failure(message=error),
            ),
        )
    )
    return WaitForInputResult(task_id=task_id)


@activity(name=f"{INTERNAL_ACTIVITY_PREFIX}persist_task_span_context", _allow_reserved_name=True)
async def _persist_task_span_context(trace_id: int, span_id: int, trace_flags: int) -> list[int]:
    """Record span IDs in workflow history so they survive replay after a worker restart."""
    return [trace_id, span_id, trace_flags]


@emitter_activity(name=f"{INTERNAL_ACTIVITY_PREFIX}emit_task_started", _allow_reserved_name=True)
async def _emit_task_started(task_id: str, task_type: str, state: Any) -> None:
    await publish_emitter_event(
        lambda: CustomTaskStarted(
            **create_emitter_event_fields("payload"),
            attributes=CustomTaskStartedAttributes(
                custom_task_id=task_id,
                custom_task_type=task_type,
                payload=JSONPayload(value=state),
            ),
        )
    )


@emitter_activity(name=f"{INTERNAL_ACTIVITY_PREFIX}emit_task_in_progress", _allow_reserved_name=True)
async def _emit_task_in_progress(
    task_id: str, task_type: str, patches: list[dict[str, Any]], encrypted_paths: list[str]
) -> None:
    from mistralai.workflows.core._events.json_patch import patches_to_json_patch
    from mistralai.workflows.protocol.v1.events import JSONPatchPayload

    # Convert patch dicts to JSONPatch models
    json_patches = patches_to_json_patch(patches)

    # Create payload and set encrypted_paths for the encoder
    payload = JSONPatchPayload(value=json_patches)
    payload._encrypted_paths = set(encrypted_paths)

    await publish_emitter_event(
        lambda: CustomTaskInProgress(
            **create_emitter_event_fields("payload"),
            attributes=CustomTaskInProgressAttributes(
                custom_task_id=task_id,
                custom_task_type=task_type,
                payload=payload,
            ),
        )
    )


@emitter_activity(name=f"{INTERNAL_ACTIVITY_PREFIX}emit_task_completed", _allow_reserved_name=True)
async def _emit_task_completed(task_id: str, task_type: str, state: Any) -> None:
    await publish_emitter_event(
        lambda: CustomTaskCompleted(
            **create_emitter_event_fields("payload"),
            attributes=CustomTaskCompletedAttributes(
                custom_task_id=task_id,
                custom_task_type=task_type,
                payload=JSONPayload(value=state),
            ),
        )
    )


@emitter_activity(name=f"{INTERNAL_ACTIVITY_PREFIX}emit_task_failed", _allow_reserved_name=True)
async def _emit_task_failed(task_id: str, task_type: str, error: str) -> None:
    await publish_emitter_event(
        lambda: CustomTaskFailed(
            **create_emitter_event_fields("payload"),
            attributes=CustomTaskFailedAttributes(
                custom_task_id=task_id,
                custom_task_type=task_type,
                failure=Failure(message=error),
            ),
        )
    )
