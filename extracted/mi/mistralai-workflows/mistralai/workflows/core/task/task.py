import json
import uuid
from datetime import timedelta
from typing import Any, Type

import structlog
import temporalio.activity
import temporalio.workflow
from opentelemetry import trace
from opentelemetry.trace import NonRecordingSpan, Span, SpanContext, StatusCode, TraceFlags
from pydantic import BaseModel, TypeAdapter
from pydantic_core import PydanticSerializationError

from mistralai.workflows.core._events.event_activities import (
    _emit_task_completed,
    _emit_task_failed,
    _emit_task_in_progress,
    _emit_task_started,
    _persist_task_span_context,
)
from mistralai.workflows.core._events.event_context import BackgroundEventPublisher
from mistralai.workflows.core._events.event_utils import create_base_event_fields, should_publish_event
from mistralai.workflows.core._events.json_patch import make_json_patch
from mistralai.workflows.core.temporal.utils import require_activity_context_value
from mistralai.workflows.core.tracing._otel_config import _get_calling_module_name
from mistralai.workflows.core.utils.contextvars import unwrap_contextual_result
from mistralai.workflows.models import EventSpanType
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
    JSONPatchPayload,
    JSONPayload,
    WorkflowEvent,
)

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(_get_calling_module_name())

adapter: TypeAdapter[Any] = TypeAdapter(Any)


def _to_json(obj: Any) -> Any:
    return adapter.dump_python(obj, mode="json")


def _publish_task_event(event: WorkflowEvent) -> None:
    if not should_publish_event():
        return

    publisher = BackgroundEventPublisher.get_current()
    if publisher is None:
        raise RuntimeError("BackgroundEventPublisher not available - ensure activity interceptor is configured")

    publisher.publish_event_background(event)


class Task[T]:
    """
    Observable task context manager that emits lifecycle events to the Workflows API.

    Lifecycle: Started → InProgress* → Completed|Failed

    Use for operations that need real-time observability (LLM streaming, file processing, etc).

    Each lifecycle point emits an immediately-completed (0-time) span rather than a single
    long-running span. This ensures spans are exported even if the worker crashes mid-task,
    since each span is finished and flushed at creation time. The "started" span is set as
    the active context so nested tasks and subsequent lifecycle spans form a proper
    parent-child tree.

    Usage:
        ```python
        # In activities
        @workflows.activity
        async def process_file():
            async with task("file_processing", state={"progress": 0}) as t:
                await t.set_state({"progress": 50})
                await t.set_state({"progress": 100})

        # In workflows - can span multiple activities!
        @workflows.workflow.define()
        class MyWorkflow:
            @workflows.workflow.entrypoint
            async def run(self):
                async with task("llm_generation", state={"tokens": 0}) as t:
                    result1 = await call_activity_1()
                    await t.set_state({"tokens": 100})

                    result2 = await call_activity_2()
                    await t.set_state({"tokens": 200})
        ```
    """

    _id: str
    _type: str
    _state: T | None
    _started: bool
    _span_context: Any  # Context manager from trace.use_span()

    def __init__(self, type: str, state: T | None = None, id: str | None = None) -> None:
        self._id = (
            id
            if id is not None
            else str(temporalio.workflow.uuid4() if temporalio.workflow.in_workflow() else uuid.uuid4())
        )
        self._type = type
        self._state = state
        self._started = False
        self._span_context = None

    def _truncate_state_preview(self, state: Any, max_length: int = 1024) -> str:
        """Create a truncated JSON preview of the state to avoid backend ingestion limits"""
        try:
            state_json = json.dumps(_to_json(state), default=str)
            if len(state_json) > max_length:
                return state_json[: max_length - 3] + "..."
            return state_json
        except Exception:
            return "<serialization error>"

    def _get_span_attributes(self) -> dict[str, Any]:
        attributes: dict[str, Any] = {
            "task.id": self._id,
            "task.type": self._type,
            "task.has_state": self._state is not None,
            "wf.type": EventSpanType.custom_task,
        }

        if temporalio.workflow.in_workflow():
            workflow_info = temporalio.workflow.info()
            attributes["wf.workflow.type"] = workflow_info.workflow_type
            attributes["wf.workflow.id"] = workflow_info.workflow_id
            attributes["wf.run.id"] = workflow_info.run_id
            attributes["wf.task_queue"] = workflow_info.task_queue
        elif temporalio.activity.in_activity():
            activity_info = temporalio.activity.info()
            attributes["wf.workflow.type"] = require_activity_context_value(
                activity_info.workflow_type,
                field_name="workflow_type",
            )
            attributes["wf.workflow.id"] = require_activity_context_value(
                activity_info.workflow_id,
                field_name="workflow_id",
            )
            attributes["wf.run.id"] = require_activity_context_value(
                activity_info.workflow_run_id,
                field_name="workflow_run_id",
            )
            attributes["wf.task_queue"] = activity_info.task_queue
            attributes["wf.activity.type"] = activity_info.activity_type
            attributes["wf.activity.attempt"] = activity_info.attempt

        return attributes

    def _emit_completed_span(
        self,
        name: str,
        attributes: dict[str, Any],
        exception: BaseException | None = None,
    ) -> Span | None:
        """Create and immediately end a 0-time span if not replaying"""
        if temporalio.workflow.in_workflow() and temporalio.workflow.unsafe.is_replaying():
            return None

        try:
            all_attributes = {**self._get_span_attributes(), **attributes}
            span = tracer.start_span(name, attributes=all_attributes)

            if exception is not None:
                span.set_status(StatusCode.ERROR, description=str(exception)[:1024])
                span.record_exception(exception)
            else:
                span.set_status(StatusCode.OK)

            span.end()
            return span
        except Exception:
            logger.warning("Failed to emit OTEL span", span_name=name)
            return None

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    @property
    def state(self) -> T | None:
        return self._state

    async def __aenter__(self) -> "Task[T]":
        lifecycle_attrs: dict[str, Any] = {"task.lifecycle": "started"}
        if self._state is not None:
            lifecycle_attrs["task.initial_state"] = self._truncate_state_preview(self._state)

        span = self._emit_completed_span(f"Task:{self._type}", lifecycle_attrs)

        if temporalio.workflow.in_workflow():
            span = await self._persist_and_restore_span_context(span)

        if span is not None:
            # Set the (already-ended) span as active context so nested tasks
            # and subsequent lifecycle spans discover it as parent.
            # An ended span's SpanContext is still valid for propagation.
            self._span_context = trace.use_span(span, end_on_exit=False)
            self._span_context.__enter__()

        try:
            if not should_publish_event():
                return self

            if temporalio.workflow.in_workflow():
                await temporalio.workflow.execute_local_activity(
                    _emit_task_started,
                    args=[self._id, self._type, _to_json(self._state)],
                    start_to_close_timeout=timedelta(seconds=10),
                )
            else:
                _publish_task_event(
                    CustomTaskStarted(
                        **create_base_event_fields(),
                        attributes=CustomTaskStartedAttributes(
                            custom_task_id=self._id,
                            custom_task_type=self._type,
                            payload=JSONPayload(value=_to_json(self._state)),
                        ),
                    )
                )
        # Ensure to restore the OTEL context to prevent incorrect parent-child relationships in subsequent spans
        except Exception:
            if self._span_context is not None:
                self._span_context.__exit__(None, None, None)
                self._span_context = None
            raise

        return self

    async def _persist_and_restore_span_context(self, span: Span | None) -> Span | None:
        """Persist span IDs in workflow history; reconstruct during replay.

        On first execution the real span's trace/span IDs are stored via a
        local-activity side-effect.  During replay after a worker restart the
        activity result is replayed, giving us the original IDs which we use
        to build a NonRecordingSpan so that post-replay lifecycle spans still
        form a correct parent-child tree.
        """
        if span is not None:
            sc = span.get_span_context()
            trace_id = sc.trace_id
            span_id = sc.span_id
            trace_flags = int(sc.trace_flags)
        else:
            trace_id = 0
            span_id = 0
            trace_flags = 0

        stored = await temporalio.workflow.execute_local_activity(
            _persist_task_span_context,
            args=[trace_id, span_id, trace_flags],
            start_to_close_timeout=timedelta(seconds=5),
        )
        _, stored = unwrap_contextual_result(stored)

        if span is not None:
            return span

        if not stored[0] or not stored[1]:
            return None

        restored_ctx = SpanContext(
            trace_id=stored[0],
            span_id=stored[1],
            is_remote=False,
            trace_flags=TraceFlags(stored[2]),
        )
        return NonRecordingSpan(restored_ctx)

    async def __aexit__(self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any) -> None:
        try:
            if exc_type is None:
                lifecycle_attrs: dict[str, Any] = {"task.lifecycle": "completed"}
                if self._state is not None:
                    lifecycle_attrs["task.final_state"] = self._truncate_state_preview(self._state)
                self._emit_completed_span(f"Task:{self._type}", lifecycle_attrs)
            else:
                error_message = str(exc_val)[:1024] if exc_val else "Unknown error"
                self._emit_completed_span(
                    f"Task:{self._type}",
                    {"task.lifecycle": "failed", "error.message": error_message},
                    exception=exc_val,
                )
        finally:
            # Restore the previous active span context
            if self._span_context is not None:
                self._span_context.__exit__(None, None, None)
                self._span_context = None

        if not should_publish_event():
            return

        if temporalio.workflow.in_workflow():
            if exc_type is None:
                await temporalio.workflow.execute_local_activity(
                    _emit_task_completed,
                    args=[self._id, self._type, _to_json(self._state)],
                    start_to_close_timeout=timedelta(seconds=10),
                )
            else:
                await temporalio.workflow.execute_local_activity(
                    _emit_task_failed,
                    args=[self._id, self._type, str(exc_val)],
                    start_to_close_timeout=timedelta(seconds=10),
                )
        else:
            if exc_type is None:
                _publish_task_event(
                    CustomTaskCompleted(
                        **create_base_event_fields(),
                        attributes=CustomTaskCompletedAttributes(
                            custom_task_id=self._id,
                            custom_task_type=self._type,
                            payload=JSONPayload(value=_to_json(self._state)),
                        ),
                    )
                )
            else:
                _publish_task_event(
                    CustomTaskFailed(
                        **create_base_event_fields(),
                        attributes=CustomTaskFailedAttributes(
                            custom_task_id=self._id,
                            custom_task_type=self._type,
                            failure=Failure(message=str(exc_val)),
                        ),
                    )
                )

    async def set_state(self, state: T) -> None:
        """
        Update state, emitting InProgress with JSON patch or full payload.

        Events are published in the background for observability.
        """
        if self._state is None:
            raise RuntimeError("Cannot set_state() on task created without state")

        previous = self._state
        self._state = state

        self._emit_completed_span(
            f"Task:{self._type}",
            {
                "task.lifecycle": "state_updated",
                "task.state_preview": self._truncate_state_preview(state),
            },
        )

        if not should_publish_event():
            return

        try:
            patches = make_json_patch(previous, state)

            if temporalio.workflow.in_workflow():
                await temporalio.workflow.execute_local_activity(
                    _emit_task_in_progress,
                    args=[self._id, self._type, patches],
                    start_to_close_timeout=timedelta(seconds=10),
                )
            else:
                _publish_task_event(
                    CustomTaskInProgress(
                        **create_base_event_fields(),
                        attributes=CustomTaskInProgressAttributes(
                            custom_task_id=self._id,
                            custom_task_type=self._type,
                            payload=JSONPatchPayload(value=patches),
                        ),
                    )
                )
        except PydanticSerializationError:
            logger.error(
                "Failed JSON patch - state updated locally but not published",
                previous=previous,
                new=state,
                task_id=self._id,
            )

    async def update_state(self, updates: dict[str, Any]) -> None:
        """
        Partial state update (only for BaseModel or dict).

        Events are published in the background for observability.
        """
        if self._state is None:
            raise RuntimeError("Cannot update_state() on task created without state")

        if isinstance(self._state, BaseModel):
            await self.set_state(self._state.model_copy(update=updates))
        elif isinstance(self._state, dict):
            new_dict: dict[str, Any] = self._state.copy()
            new_dict.update(updates)
            await self.set_state(new_dict)  # type: ignore
        else:
            raise TypeError(f"update_state() requires BaseModel or dict, got {type(self._state).__name__}")
