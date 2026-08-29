from enum import StrEnum


class SearchAttributes(StrEnum):
    otel_trace_id = "OtelTraceId"
    workflow_name = "WorkflowName"
    user_id = "UserId"
    customer_id = "CustomerId"
    workspace_id = "WorkspaceId"
    organization_id = "OrganizationId"
    allow_auto_remove = "AllowAutoRemove"
    custom_search_attributes = "CustomSearchAttributes"


class EventAttributes(StrEnum):
    type = "wf.type"
    id = "wf.id"
    event_type = "wf.event_type"
    arguments = "wf.arguments"
    result = "wf.result"
    internal = "wf.internal"

    activity_execution_id = "wf.activity.execution_id"
    activity_attempt = "wf.activity.attempt"
    activity_max_attempts = "wf.activity.max_attempts"
    activity_schedule_to_start_ms = "wf.activity.schedule_to_start.ms"
    activity_execution_ms = "wf.activity.execution.ms"

    workflow_execution_id = "wf.workflow.execution_id"
    workflow_type = "wf.workflow.type"
    workflow_duration_ms = "wf.workflow.duration.ms"
    workflow_attempt = "wf.workflow.attempt"
    workflow_max_attempts = "wf.workflow.max_attempts"

    progress_status = "wf.progress.status"
    progress_start_time_unix_ms = "wf.progress.start_time_unix_ms"
    progress_end_time_unix_ms = "wf.progress.end_time_unix_ms"
    progress_error = "wf.progress.error"

    custom_prefix = "wf.custom"
