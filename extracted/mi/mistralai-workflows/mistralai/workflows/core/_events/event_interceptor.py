import asyncio
from datetime import timedelta
from typing import Any, Type

import structlog
import temporalio.activity
import temporalio.client
import temporalio.common
import temporalio.worker
import temporalio.workflow

from mistralai.workflows.core._events.event_activities import (
    _emit_workflow_canceled,
    _emit_workflow_completed,
    _emit_workflow_failed,
    _emit_workflow_started,
)
from mistralai.workflows.core._events.event_context import (
    BackgroundEventPublisher,
    EventContext,
    _background_event_publisher,
)
from mistralai.workflows.core._events.event_utils import create_base_event_fields
from mistralai.workflows.core._registration.registration_activity import (
    REGISTER_EXECUTION_ACTIVITY_NAME,
)
from mistralai.workflows.core.definition.workflow_definition import (
    get_workflow_display_name,
)
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

logger = structlog.get_logger(__name__)


async def _publish_event(event: WorkflowEvent) -> None:
    """Publish event via the EventContext (for activities - blocks until sent)."""
    context = EventContext.get_singleton()
    if not context:
        logger.warning(
            "EventContext not available, skipping event",
            event_type=event.event_type,
        )
        return
    await context.publish_event(event)


class _EventActivityInboundInterceptor(temporalio.worker.ActivityInboundInterceptor):
    """Activity interceptor that sends activity task events to the API.

    Emits ACTIVITY_TASK_STARTED, ACTIVITY_TASK_COMPLETED, ACTIVITY_TASK_RETRYING,
    and ACTIVITY_TASK_FAILED events.
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

        attempt = activity_info.attempt

        max_attempts = 1
        if activity_info.retry_policy and activity_info.retry_policy.maximum_attempts > 0:
            max_attempts = activity_info.retry_policy.maximum_attempts

        if attempt == 1:
            await _publish_event(
                ActivityTaskStarted(
                    **create_base_event_fields(),
                    attributes=ActivityTaskStartedAttributes(
                        task_id=task_id,
                        activity_name=activity_name,
                        input=JSONPayload(value=list(input.args)),
                    ),
                )
            )

        publisher = BackgroundEventPublisher(context)
        publisher_token = BackgroundEventPublisher.set_current(publisher)

        try:
            result = await self.next.execute_activity(input)

            # Wait for all custom task events to be sent before marking activity as complete
            await publisher.drain()

            await _publish_event(
                ActivityTaskCompleted(
                    **create_base_event_fields(),
                    attributes=ActivityTaskCompletedAttributes(
                        task_id=task_id,
                        activity_name=activity_name,
                        result=JSONPayload(value=result),
                    ),
                )
            )
            return result

        except Exception as e:
            await publisher.drain()

            is_final_attempt = max_attempts > 0 and attempt >= max_attempts

            if is_final_attempt:
                await _publish_event(
                    ActivityTaskFailed(
                        **create_base_event_fields(),
                        attributes=ActivityTaskFailedAttributes(
                            task_id=task_id,
                            activity_name=activity_name,
                            attempt=attempt,
                            failure=Failure(message=str(e)),
                        ),
                    )
                )
            else:
                await _publish_event(
                    ActivityTaskRetrying(
                        **create_base_event_fields(),
                        attributes=ActivityTaskRetryingAttributes(
                            task_id=task_id,
                            activity_name=activity_name,
                            attempt=attempt,
                            failure=Failure(message=str(e)),
                        ),
                    )
                )
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

        await temporalio.workflow.execute_local_activity(
            _emit_workflow_started,
            args=[task_id, info.workflow_type, list(input.args), display_name],
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=temporalio.common.RetryPolicy(maximum_attempts=3),
        )

        try:
            result = await super().execute_workflow(input)

            await temporalio.workflow.execute_local_activity(
                _emit_workflow_completed,
                args=[task_id, result],
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=temporalio.common.RetryPolicy(maximum_attempts=3),
            )

            return result

        except asyncio.CancelledError as e:
            await temporalio.workflow.execute_local_activity(
                _emit_workflow_canceled,
                args=[task_id, str(e) if str(e) else None],
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=temporalio.common.RetryPolicy(maximum_attempts=3),
            )
            raise

        except Exception as e:
            await temporalio.workflow.execute_local_activity(
                _emit_workflow_failed,
                args=[task_id, str(e)],
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=temporalio.common.RetryPolicy(maximum_attempts=3),
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
