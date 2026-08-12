import uuid
from typing import Any

import structlog
import temporalio.activity
import temporalio.workflow

from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.core.temporal.utils import TEMPORAL_SCHEDULE_ID_SEARCH_KEY, require_activity_context_value
from mistralai.workflows.exceptions import NotInTemporalContextError

logger = structlog.get_logger(__name__)


def _in_workflow() -> bool:
    """Check if currently running inside a workflow context."""
    return temporalio.workflow.in_workflow()


def _in_activity() -> bool:
    """Check if currently running inside an activity context."""
    return temporalio.activity.in_activity()


def get_lineage_workflow_exec_id() -> tuple[str, str | None]:
    """Get root and parent workflow execution ID.

    Works from both workflow and activity contexts.
    For activities, uses the propagated WorkflowContext to get the root workflow ID.

    Raises:
        NotInTemporalContextError: If not in a workflow or activity context.
    """
    if _in_workflow():
        info = temporalio.workflow.info()
        root_workflow_id = info.root.workflow_id if info.root else info.workflow_id
        parent_workflow_id = info.parent.workflow_id if info.parent else None
        return root_workflow_id, parent_workflow_id
    elif _in_activity():
        wf_context = retrieve_context()
        workflow_id = require_activity_context_value(
            temporalio.activity.info().workflow_id,
            field_name="workflow_id",
        )
        root_workflow_id = workflow_id
        parent_workflow_id = None

        if wf_context:
            if wf_context.root_workflow_exec_id:
                root_workflow_id = wf_context.root_workflow_exec_id
            if wf_context.parent_workflow_exec_id:
                parent_workflow_id = wf_context.parent_workflow_exec_id

        return root_workflow_id, parent_workflow_id
    else:
        raise NotInTemporalContextError()


def try_get_lineage_workflow_exec_id() -> tuple[str | None, str | None]:
    """Like get_lineage_workflow_exec_id but returns (None, None) outside a Temporal context.

    Convenient for log enrichment, which runs for every record including non-workflow logs.
    """
    try:
        return get_lineage_workflow_exec_id()
    except NotInTemporalContextError:
        return None, None


def create_base_event_fields() -> dict[str, Any]:
    """Create common fields for all workflow events.

    Works from both workflow and activity contexts.

    Raises:
        NotInTemporalContextError: If not in a workflow or activity context.
    """

    root_workflow_id, parent_workflow_id = get_lineage_workflow_exec_id()
    if _in_workflow():
        workflow_info = temporalio.workflow.info()
        return {
            "event_id": str(temporalio.workflow.uuid4()),
            "root_workflow_exec_id": root_workflow_id,
            "parent_workflow_exec_id": parent_workflow_id,
            "workflow_exec_id": workflow_info.workflow_id,
            "workflow_run_id": workflow_info.run_id,
            "workflow_name": workflow_info.workflow_type,
            "continued_run_id": workflow_info.continued_run_id,
            "first_execution_run_id": workflow_info.first_execution_run_id,
            "schedule_id": workflow_info.typed_search_attributes.get(TEMPORAL_SCHEDULE_ID_SEARCH_KEY),
        }
    elif _in_activity():
        wf_context = retrieve_context()
        activity_info = temporalio.activity.info()
        return {
            "event_id": str(uuid.uuid4()),
            "root_workflow_exec_id": root_workflow_id,
            "parent_workflow_exec_id": parent_workflow_id,
            "workflow_exec_id": require_activity_context_value(
                activity_info.workflow_id,
                field_name="workflow_id",
            ),
            "workflow_run_id": require_activity_context_value(
                activity_info.workflow_run_id,
                field_name="workflow_run_id",
            ),
            "workflow_name": require_activity_context_value(
                activity_info.workflow_type,
                field_name="workflow_type",
            ),
            "continued_run_id": wf_context.continued_run_id if wf_context else None,
            "first_execution_run_id": wf_context.first_execution_run_id if wf_context else None,
            "schedule_id": wf_context.schedule_id if wf_context else None,
        }
    else:
        raise NotInTemporalContextError()


def should_publish_event() -> bool:
    """Check if events should be published.

    Returns True if in workflow or activity context, False otherwise.
    """
    if _in_workflow() or _in_activity():
        return True
    logger.error(
        "should_publish_event called outside of Temporal context. "
        "Events can only be published from within a workflow or activity. "
        "Returning False to skip event publication."
    )
    return False
