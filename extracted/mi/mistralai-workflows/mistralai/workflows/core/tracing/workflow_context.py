import temporalio.activity
import temporalio.workflow
from opentelemetry.context import Context
from opentelemetry.sdk.trace import Span, SpanProcessor
from opentelemetry.util.types import AttributeValue

from mistralai.workflows.models import EventAttributes

ContextInfo = temporalio.activity.Info | temporalio.workflow.Info

WORKFLOW_EXECUTION_ID_ATTRIBUTE = EventAttributes.workflow_execution_id.value
TEMPORAL_WORKFLOW_ID_ATTRIBUTE = "temporalWorkflowID"
# Key the Traces backend (dora) reads a trace's workflow name from; it does not index wf.workflow.type.
GEN_AI_WORKFLOW_NAME_ATTRIBUTE = "gen_ai.workflow.name"


def current_context_info() -> ContextInfo | None:
    """Activity or workflow info for the calling context, or None outside both.

    Activity is checked first because its info also carries the parent workflow's
    ids, so an activity context never needs the workflow lookup. The two contexts
    are normally mutually exclusive: Temporal only sets one on a given thread/task.
    """
    if temporalio.activity.in_activity():
        return temporalio.activity.info()
    if temporalio.workflow.in_workflow():
        return temporalio.workflow.info()
    return None


def workflow_execution_span_attributes(workflow_execution_id: str) -> dict[str, str]:
    return {
        WORKFLOW_EXECUTION_ID_ATTRIBUTE: workflow_execution_id,
        TEMPORAL_WORKFLOW_ID_ATTRIBUTE: workflow_execution_id,
    }


def workflow_context_span_attributes(info: ContextInfo | None = None) -> dict[str, AttributeValue]:
    """wf.* span attributes identifying the current workflow or activity context.

    Returns {} outside a workflow run. workflow-side spans are also enriched through
    the tracing interceptor's _completed_span override, but this helper is what
    makes enrichment possible from any code path (httpx, SDK clients, user code).
    """
    if info is None:
        info = current_context_info()
    if info is None:
        return {}

    attributes: dict[str, AttributeValue] = {}
    if info.workflow_id:
        attributes.update(workflow_execution_span_attributes(info.workflow_id))
    if info.workflow_type:
        attributes[EventAttributes.workflow_type] = info.workflow_type
        attributes[GEN_AI_WORKFLOW_NAME_ATTRIBUTE] = info.workflow_type

    if isinstance(info, temporalio.activity.Info):
        if info.workflow_run_id:
            attributes[EventAttributes.workflow_run_id] = info.workflow_run_id
        if info.activity_type:
            attributes[EventAttributes.activity_type] = info.activity_type
        attributes[EventAttributes.activity_execution_id] = info.activity_id
        attributes[EventAttributes.activity_attempt] = info.attempt
    else:
        attributes[EventAttributes.workflow_run_id] = info.run_id
    return attributes


class WorkflowContextSpanProcessor(SpanProcessor):
    """Stamps workflow context attributes on every span started inside a workflow run.

    Only fills in missing keys, so attributes set by the span producer are never
    overwritten. Workflow-side spans created through Temporal's tracing extern are
    enriched by the _MistralTracingWorkflowInboundInterceptor._completed_span override
    instead: the extern runs host-side where workflow.info() cannot be relied on.
    """

    def on_start(self, span: Span, parent_context: Context | None = None) -> None:
        context_attributes = workflow_context_span_attributes()
        if not context_attributes:
            return
        existing = span.attributes or {}
        for key, value in context_attributes.items():
            if key not in existing:
                span.set_attribute(key, value)
