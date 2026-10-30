import asyncio
from typing import Any, Type

import temporalio.activity
import temporalio.client
import temporalio.worker
import temporalio.workflow
from temporalio.exceptions import ApplicationError

from mistralai.workflows.core._events.event_activities import (
    _emit_workflow_canceled,
    _emit_workflow_completed,
    _emit_workflow_failed,
    _emit_workflow_started,
    execute_emitter,
    execute_emitter_preserving_error,
)
from mistralai.workflows.core._events.event_context import (
    BackgroundEventPublisher,
    EventContext,
    _background_event_publisher,
    activity_attempts_exhausted,
)
from mistralai.workflows.core._events.event_failure import event_failure_message
from mistralai.workflows.core._events.event_utils import (
    create_stable_activity_event_fields,
)
from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.core._registration.registration_activity import (
    REGISTER_EXECUTION_ACTIVITY_NAME,
)
from mistralai.workflows.core.definition.workflow_definition import (
    get_workflow_display_name,
)
from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.core.utils.contextvars import reset_contextvar
from mistralai.workflows.protocol.v1.events import (
    ActivityTaskCompleted,
    ActivityTaskCompletedAttributes,
    ActivityTaskFailed,
    ActivityTaskFailedAttributes,
    ActivityTaskRetrying,
    ActivityTaskRetryingAttributes,
    ActivityTaskStarted,
    ActivityTaskStartedAttributes,
    Failure,
    JSONPayload,
    WorkflowEvent,
)

logger = get_logger(__name__)


def _is_final_attempt(info: temporalio.activity.Info, error: Exception) -> bool:
    if isinstance(error, ApplicationError) and error.non_retryable:
        return True
    return info.retry_policy is None or activity_attempts_exhausted(info)


async def _publish_activity_failure(
    context: EventContext, publisher: BackgroundEventPublisher, error: Exception
) -> None:
    """Best effort, so that a publish failure does not hide the error the activity is about to raise."""
    await publisher.drain_preserving_error()

    info = temporalio.activity.info()
    failure = Failure(message=event_failure_message(error))
    event: WorkflowEvent
    if _is_final_attempt(info, error):
        event = ActivityTaskFailed(
            **create_stable_activity_event_fields(f"failed:{info.attempt}"),
            attributes=ActivityTaskFailedAttributes(
                task_id=info.activity_id, activity_name=info.activity_type, attempt=info.attempt, failure=failure
            ),
        )
    else:
        event = ActivityTaskRetrying(
            **create_stable_activity_event_fields(f"retrying:{info.attempt}"),
            attributes=ActivityTaskRetryingAttributes(
                task_id=info.activity_id, activity_name=info.activity_type, attempt=info.attempt, failure=failure
            ),
        )
    try:
        await context.publish_event_with_retry(event)
    except Exception as publish_error:
        logger.error("Failed to publish activity failure event", **extract_error_context(publish_error))


class _EventActivityInboundInterceptor(temporalio.worker.ActivityInboundInterceptor):
    """Activity interceptor that sends activity task events to the API.

    Emits ACTIVITY_TASK_STARTED, ACTIVITY_TASK_COMPLETED, ACTIVITY_TASK_RETRYING,
    and ACTIVITY_TASK_FAILED events. The activity does not complete successfully
    until every event it sent is published.
    """

    async def execute_activity(self, input: temporalio.worker.ExecuteActivityInput) -> Any:
        context = EventContext.get_singleton()
        if not context:
            return await self.next.execute_activity(input)

        activity_info = temporalio.activity.info()
        task_id = activity_info.activity_id
        activity_name = activity_info.activity_type

        # Skip event emission for the registration activity — it is an
        # internal implementation detail that should not appear in SSE streams.
        if activity_name == REGISTER_EXECUTION_ACTIVITY_NAME:
            return await self.next.execute_activity(input)

        publisher = BackgroundEventPublisher(context)
        publisher_token = BackgroundEventPublisher.set_current(publisher)

        try:
            # Sent on every attempt: if an earlier attempt failed to publish it, this one does, under the same id.
            publisher.publish_event_background(
                ActivityTaskStarted(
                    **create_stable_activity_event_fields("started"),
                    attributes=ActivityTaskStartedAttributes(
                        task_id=task_id,
                        activity_name=activity_name,
                        input=JSONPayload(value=list(input.args)),
                    ),
                )
            )
            # Events the body sends directly, bypassing the queue, must not overtake it.
            await publisher.drain()
            result = await self.next.execute_activity(input)
            publisher.publish_event_background(
                ActivityTaskCompleted(
                    **create_stable_activity_event_fields("completed"),
                    attributes=ActivityTaskCompletedAttributes(
                        task_id=task_id,
                        activity_name=activity_name,
                        result=JSONPayload(value=result),
                    ),
                )
            )
            await publisher.drain()
            return result

        except Exception as e:
            await _publish_activity_failure(context, publisher, e)
            raise
        finally:
            await publisher.shutdown()
            reset_contextvar(_background_event_publisher, publisher_token)


class _EventWorkflowInboundInterceptor(temporalio.worker.WorkflowInboundInterceptor):
    """Workflow interceptor that sends workflow execution events to the API via internal activities.

    Emits WORKFLOW_EXECUTION_STARTED, WORKFLOW_EXECUTION_COMPLETED,
    WORKFLOW_EXECUTION_FAILED, and WORKFLOW_EXECUTION_CANCELED events.
    """

    async def execute_workflow(self, input: temporalio.worker.ExecuteWorkflowInput) -> Any:
        context = EventContext.get_singleton()
        if not context:
            return await super().execute_workflow(input)

        info = temporalio.workflow.info()
        task_id = str(temporalio.workflow.uuid4())
        display_name = get_workflow_display_name(info.workflow_type)

        try:
            await execute_emitter(
                _emit_workflow_started, task_id, info.workflow_type, list(input.args), display_name, info.attempt
            )
            result = await super().execute_workflow(input)
            await execute_emitter(_emit_workflow_completed, task_id, result, info.attempt)
            return result

        except asyncio.CancelledError as e:
            await execute_emitter_preserving_error(
                _emit_workflow_canceled, task_id, str(e) if str(e) else None, info.attempt
            )
            raise

        except Exception as e:
            await execute_emitter_preserving_error(
                _emit_workflow_failed, task_id, event_failure_message(e), info.attempt
            )
            raise


class EventInterceptor(temporalio.client.Interceptor, temporalio.worker.Interceptor):
    """Temporal interceptor that sends workflow and activity events to the Workflows API.

    Captures workflow lifecycle events (started, completed, failed, canceled)
    and activity lifecycle events (started, completed, retrying, failed).
    Events are published asynchronously via the EventContext's task group.
    """

    def intercept_activity(
        self, next: temporalio.worker.ActivityInboundInterceptor
    ) -> temporalio.worker.ActivityInboundInterceptor:
        return _EventActivityInboundInterceptor(next)

    def workflow_interceptor_class(
        self, input: temporalio.worker.WorkflowInterceptorClassInput
    ) -> Type[temporalio.worker.WorkflowInboundInterceptor] | None:
        return _EventWorkflowInboundInterceptor
