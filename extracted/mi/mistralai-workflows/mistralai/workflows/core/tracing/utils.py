import uuid
from typing import (
    Any,
    Dict,
)

import structlog
import temporalio
import temporalio.activity
import temporalio.client
import temporalio.common
import temporalio.workflow
from opentelemetry import trace
from opentelemetry.trace import format_trace_id

from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.utils import require_activity_context_value
from mistralai.workflows.core.tracing._otel_config import _get_calling_module_name
from mistralai.workflows.models import (
    EventAttributes,
    EventSpanType,
    EventType,
    SearchAttributes,
)

logger = structlog.getLogger(__name__)
tracer = trace.get_tracer(_get_calling_module_name())


CUSTOM_TRACING_ATTRIBUTES = "custom_tracing_attributes"
WORKFLOW_EXECUTION_ID_ATTRIBUTE = EventAttributes.workflow_execution_id.value
TEMPORAL_WORKFLOW_ID_ATTRIBUTE = "temporalWorkflowID"

# Temporal workflow header set by the API when the caller supplied an explicit traceparent.
# Its presence tells the worker to reuse the caller's trace/sampling as-is instead of forcing sampling.
USER_TRACEPARENT_HEADER = "x-mistral-user-traceparent"


def get_otel_trace_id(workflow_description: temporalio.client.WorkflowExecutionDescription) -> str | None:
    otel_trace_id_values = workflow_description.search_attributes.get(SearchAttributes.otel_trace_id)
    if otel_trace_id_values and len(otel_trace_id_values) > 0 and isinstance(otel_trace_id_values[0], str):
        otel_trace_id = otel_trace_id_values[0]
    else:
        otel_trace_id = None

    return otel_trace_id


def set_otel_trace_id_in_current_workflow_execution() -> None:
    if not temporalio.workflow.in_workflow():
        return

    info = temporalio.workflow.info()
    span = trace.get_current_span()
    ctx = span.get_span_context()
    trace_id = format_trace_id(ctx.trace_id)

    temporalio.workflow.upsert_search_attributes(
        temporalio.common.TypedSearchAttributes(
            [
                temporalio.common.SearchAttributePair(
                    key=temporalio.common.SearchAttributeKey.for_keyword(SearchAttributes.otel_trace_id),
                    value=trace_id,
                )
            ]
        )  # type: ignore
    )

    logger.debug("Set OpenTelemetry trace ID in workflow execution", trace_id=trace_id, execution_id=info.run_id)


def _get_event_id() -> str:
    return uuid.uuid4().hex


def workflow_execution_span_attributes(workflow_execution_id: str) -> dict[str, str]:
    return {
        WORKFLOW_EXECUTION_ID_ATTRIBUTE: workflow_execution_id,
        TEMPORAL_WORKFLOW_ID_ATTRIBUTE: workflow_execution_id,
    }


def get_span_attributes(
    event_type: str,
    span_type: EventSpanType,
    internal: bool = False,
    event_id: str | None = None,
    custom_attributes: dict[str, Any] | None = None,
) -> dict:
    attributes: Dict[str, Any] = {
        EventAttributes.type: span_type,
        EventAttributes.event_type: event_type,
        EventAttributes.id: event_id or _get_event_id(),
        EventAttributes.internal: internal,
    }

    if temporalio.activity.in_activity():
        activity_info = temporalio.activity.info()
        workflow_execution_id = require_activity_context_value(
            activity_info.workflow_id,
            field_name="workflow_id",
        )
        attributes[EventAttributes.workflow_type] = require_activity_context_value(
            activity_info.workflow_type,
            field_name="workflow_type",
        )
        attributes.update(workflow_execution_span_attributes(workflow_execution_id))
        attributes[EventAttributes.activity_execution_id] = activity_info.activity_id
        attributes[EventAttributes.activity_attempt] = activity_info.attempt
        attributes[EventAttributes.activity_max_attempts] = config.worker.retry_policy_max_attempts
        attributes["temporalRunID"] = activity_info.workflow_run_id

    if temporalio.workflow.in_workflow():
        workflow_info = temporalio.workflow.info()
        attributes[EventAttributes.workflow_type] = workflow_info.workflow_type
        attributes.update(workflow_execution_span_attributes(workflow_info.workflow_id))
        attributes["temporalRunID"] = workflow_info.run_id

    if custom_attributes:
        for key, value in custom_attributes.items():
            attributes[f"{EventAttributes.custom_prefix}.{key}"] = value

    return attributes


def _record_event(
    event_name: str,
    attributes: Dict[str, Any] | None = None,
    event_type: EventType = EventType.EVENT,
    event_id: str | None = None,
    internal: bool = False,
) -> None:
    """Records an event in the current span.

    Args:
        event_name (str): The name of the event.
        attributes (Dict[str, Any] | None, optional): Additional attributes to record with the event.
                                                         They are directly available in the event. Defaults to None.
        event_type (EventType, optional): The type of the event. Defaults to EventType.EVENT.
                                          This is used to categorize events.
                                          This is unlikely to be used by the user.
        event_id (str | None, optional): The ID of the event. Defaults to None.
                                            If not provided, a random UUID will be generated.
        internal (bool, optional): Whether the event is internal. Defaults to False.
                                   If True, the event will be recorded as an internal event.
                                   Internal events are supposed to be only used for debugging purposes.
    """
    if temporalio.workflow.in_workflow() and temporalio.workflow.unsafe.is_replaying():
        return

    if attributes is None:
        attributes = {}

    with tracer.start_as_current_span(f"CustomEvent:{event_name}") as span:
        logger.debug("Recording event", event_name=event_name, attributes=attributes)
        span.add_event(
            event_name,
            {
                **attributes,
                **get_span_attributes(
                    event_type=event_name, span_type=EventSpanType.event, event_id=event_id, internal=internal
                ),
                EventAttributes.type: event_type,
            },
        )
