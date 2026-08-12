import re
import uuid
from datetime import datetime
from enum import Enum, StrEnum
from typing import Annotated, Any, Dict, List, Self, Sequence, TypeAlias

from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    computed_field,
    field_validator,
    model_validator,
)
from temporalio.client import WorkflowExecutionStatus as TemporalWorkflowExecutionStatus

from mistralai.workflows.models import (
    EventProgressStatus,
    EventType,
    NetworkEncodedInput,
    PartialScheduleDefinition,
    ScheduleDefinition,
    ScheduleDefinitionOutput,
    ScheduleOverlapPolicy,
    Workflow,
    WorkflowRegistration,
    WorkflowSpecWithTaskQueue,
)
from mistralai.workflows.models.workflow import validate_workflow_tags
from mistralai.workflows.protocol.v1.tempo import TempoGetTraceResponse

CoercedStr: TypeAlias = Annotated[str, BeforeValidator(lambda v: str(v) if isinstance(v, uuid.UUID) else v)]

EXECUTION_ID_MAX_LENGTH = 256
EXECUTION_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")  # the + ensures at least one character
DEPLOYMENT_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_\-\.]+$")


def _validate_deployment_name(v: str | None) -> str | None:
    if v is None:
        return v
    if not DEPLOYMENT_NAME_PATTERN.match(v):
        raise ValueError(
            f"Deployment name `{v}` is invalid. "
            "Names can only contain alphanumeric characters, hyphens (-), underscores (_), and dots (.)."
        )
    return v


DeploymentName = Annotated[str | None, BeforeValidator(_validate_deployment_name)]


class LocationType(str, Enum):
    local = "local"
    k8s = "k8s"
    managed = "managed"


# aeon injects this as k8s_cluster to flag managed workers; SDKs < 3.10.0 crash on
# LOCATION_TYPE=managed. Mirrors managedK8sClusterSentinel in the aeon operator.
# TODO: drop with the validator once every managed worker is on >= 3.10.0.
MANAGED_K8S_CLUSTER_SENTINEL = "__mistral_managed__"


class DeploymentLocation(BaseModel):
    location_type: LocationType = Field(description="Where the deployment runs: 'local', 'k8s', or 'managed'")
    k8s_cluster: str | None = Field(default=None, description="K8s cluster name, if applicable")
    k8s_namespace: str | None = Field(default=None, description="K8s namespace, if applicable")

    @model_validator(mode="after")
    def _normalize_managed_sentinel(self) -> Self:
        if self.k8s_cluster == MANAGED_K8S_CLUSTER_SENTINEL:
            self.location_type = LocationType.managed
            self.k8s_cluster = None
        return self


class WorkflowSpecsRegisterRequest(BaseModel):
    definitions: List[WorkflowSpecWithTaskQueue] = Field(description="List of workflow specs to register")
    deployment_name: Annotated[str, BeforeValidator(_validate_deployment_name)] = Field(
        description="Name of the deployment this worker belongs to"
    )
    worker_name: str = Field(description="Human-readable name of this worker process (hostname or pod name)")
    deployment_location: DeploymentLocation | None = Field(
        default=None, description="Metadata about where this deployment is running (local, k8s, etc.)"
    )


class WorkflowDefinitionsRegisterResponse(BaseModel):
    has_conflicts: bool = Field(description="Whether one of the provided workflows has already been registered")


class WorkflowRegistrationRef(BaseModel):
    workflow_id: uuid.UUID = Field(description="The workflow ID")
    # Made optional so old clients sending only workflow_version_id still work
    workflow_registration_id: uuid.UUID | None = Field(default=None, description="The workflow registration ID")

    @model_validator(mode="before")
    @classmethod
    def _coerce_version_id_to_registration_id(cls, data: Any) -> Any:
        if isinstance(data, dict):
            d = dict(data)
            if not d.get("workflow_registration_id") and d.get("workflow_version_id"):
                d["workflow_registration_id"] = d.pop("workflow_version_id")
            d.pop("workflow_version_id", None)
            return d
        return data

    @model_validator(mode="after")
    def _ensure_registration_id_set(self) -> Self:
        if self.workflow_registration_id is None:
            raise ValueError("workflow_registration_id is required")
        return self

    @computed_field(description="Deprecated: use workflow_registration_id")  # type: ignore[prop-decorator]
    @property
    def workflow_version_id(self) -> uuid.UUID:
        assert self.workflow_registration_id is not None
        return self.workflow_registration_id


def _remap_deprecated(data: Any, renames: dict[str, str]) -> Any:
    """Before-validator: remap deprecated field names to their replacements."""
    if isinstance(data, dict):
        d = dict(data)
        for old, new in renames.items():
            if old in d and new not in d:
                d[new] = d.pop(old)
            else:
                d.pop(old, None)
        return d
    return data


class WorkflowSpecsRegisterResponse(BaseModel):
    has_conflicts: bool = Field(description="Whether one of the provided workflow specs has already been registered")

    workflow_registration_ids: List[uuid.UUID] = Field(
        default_factory=list,
        description="List of workflow IDs that were registered",
    )
    workflow_registration_refs: List[WorkflowRegistrationRef] = Field(
        default_factory=list,
        description="List of workflow registration references",
    )
    warnings: List[str] = Field(default_factory=list, description="Non-fatal warnings produced during registration")

    # Excluded from serialization — new clients use workflow_registration_ids/refs.
    @property
    def workflow_version_ids(self) -> List[uuid.UUID]:
        return list(self.workflow_registration_ids)

    @property
    def workflow_version_refs(self) -> List[WorkflowRegistrationRef]:
        return list(self.workflow_registration_refs)

    @model_validator(mode="before")
    @classmethod
    def _remap_register_deprecated_fields(cls, data: Any) -> Any:
        return _remap_deprecated(
            data,
            {
                "workflow_version_ids": "workflow_registration_ids",
                "workflow_version_refs": "workflow_registration_refs",
            },
        )


class WorkerHeartbeatRequest(BaseModel):
    workflow_registration_refs: List[WorkflowRegistrationRef] = Field(
        default_factory=list, description="List of workflow registration references to heartbeat"
    )
    deployment_name: Annotated[str, BeforeValidator(_validate_deployment_name)] = Field(
        description="Name of the deployment this worker belongs to"
    )
    worker_name: str = Field(description="Human-readable name of this worker process (hostname or pod name)")

    @model_validator(mode="before")
    @classmethod
    def _remap_heartbeat_deprecated_fields(cls, data: Any) -> Any:
        return _remap_deprecated(data, {"workflow_version_refs": "workflow_registration_refs"})


class WorkerHeartbeatResponse(BaseModel):
    all_active: bool = Field(description="Whether all workflow versions are still active")


class WorkflowMetadata(BaseModel):
    shared_namespace: str | None = Field(default=None, description="Namespace for shared workflows, None if user-owned")


class WorkflowBasicDefinition(BaseModel):
    id: uuid.UUID
    name: str = Field(description="The name of the workflow")
    display_name: str = Field(description="The display name of the workflow")
    description: str | None = Field(default=None, description="A description of the workflow")
    metadata: WorkflowMetadata = Field(default_factory=WorkflowMetadata, description="Workflow metadata")
    archived: bool = Field(description="Whether the workflow is archived")
    tags: List[str] = Field(default_factory=list, description="Workflow tags")


class WorkflowWithWorkerStatus(Workflow):
    active: bool = Field(description="Whether the workflow is active")


class WorkflowRegistrationWithWorkerStatus(WorkflowRegistration):
    active: bool = Field(description="Whether the workflow registration is active")


class WorkflowRegistrationListResponse(BaseModel):
    workflow_registrations: List[WorkflowRegistration] = Field(description="A list of workflow registrations")
    next_cursor: CoercedStr | None

    @computed_field(description="Deprecated: use workflow_registrations")  # type: ignore[prop-decorator]
    @property
    def workflow_versions(self) -> List[WorkflowRegistration]:
        return list(self.workflow_registrations)


class WorkflowGetResponse(BaseModel):
    workflow: WorkflowWithWorkerStatus = Field(description="The workflow spec")


class WorkflowRegistrationGetResponse(BaseModel):
    workflow_registration: WorkflowRegistrationWithWorkerStatus = Field(description="The workflow registration")

    @computed_field(description="Deprecated: use workflow_registration")  # type: ignore[prop-decorator]
    @property
    def workflow_version(self) -> WorkflowRegistrationWithWorkerStatus:
        return self.workflow_registration


class WorkflowArchiveResponse(BaseModel):
    workflow: Workflow = Field(description="The workflow spec")


class WorkflowUnarchiveResponse(WorkflowArchiveResponse): ...


class WorkflowBulkArchiveRequest(BaseModel):
    workflow_ids: list[uuid.UUID] = Field(max_length=100, description="List of workflow IDs to archive")


class WorkflowBulkUnarchiveRequest(BaseModel):
    workflow_ids: list[uuid.UUID] = Field(max_length=100, description="List of workflow IDs to unarchive")


class WorkflowBulkError(BaseModel):
    workflow_id: uuid.UUID = Field(description="The requested workflow ID")
    workflow: Workflow | None = Field(default=None, description="The workflow, if found")
    message: str = Field(description="Error message describing why the operation failed")


class WorkflowBulkArchiveResponse(BaseModel):
    archived: list[Workflow] = Field(description="Workflows that were successfully archived or were already archived")
    errored: list[WorkflowBulkError] = Field(
        default_factory=list,
        description="Workflows that could not be archived and the corresponding error messages",
    )


class WorkflowBulkUnarchiveResponse(BaseModel):
    unarchived: list[Workflow] = Field(
        description="Workflows that were successfully unarchived or were already unarchived"
    )
    errored: list[WorkflowBulkError] = Field(
        default_factory=list,
        description="Workflows that could not be unarchived and the corresponding error messages",
    )


class WorkflowExecutionStatus(StrEnum):
    RUNNING = "RUNNING"
    """Workflow execution is running.
    """

    COMPLETED = "COMPLETED"
    """Workflow execution has completed successfully.
    """

    FAILED = "FAILED"
    """Workflow execution has failed.
    """

    CANCELED = "CANCELED"
    """Workflow execution has been canceled.
    """

    TERMINATED = "TERMINATED"
    """Workflow execution has been terminated.
    """

    CONTINUED_AS_NEW = "CONTINUED_AS_NEW"
    """Workflow execution has been continued as new.
    See https://docs.temporal.io/develop/python/continue-as-new#what for more details.
    """

    TIMED_OUT = "TIMED_OUT"
    """Workflow execution has timed out.
    """

    RETRYING_AFTER_ERROR = "RETRYING_AFTER_ERROR"
    """Deprecated. Kept for client compatibility and no longer returned by Abraxas.
    This is a custom status not present in Temporal.
    Temporal keeps a workflow in RUNNING state until it succeeds or fails.
    """

    @classmethod
    def from_temporal(cls, status: TemporalWorkflowExecutionStatus) -> "WorkflowExecutionStatus":
        mapping = {
            TemporalWorkflowExecutionStatus.RUNNING: cls.RUNNING,
            TemporalWorkflowExecutionStatus.COMPLETED: cls.COMPLETED,
            TemporalWorkflowExecutionStatus.FAILED: cls.FAILED,
            TemporalWorkflowExecutionStatus.CANCELED: cls.CANCELED,
            TemporalWorkflowExecutionStatus.TERMINATED: cls.TERMINATED,
            TemporalWorkflowExecutionStatus.CONTINUED_AS_NEW: cls.CONTINUED_AS_NEW,
            TemporalWorkflowExecutionStatus.TIMED_OUT: cls.TIMED_OUT,
        }
        return mapping[status]


class WorkflowExecutionWithoutResultResponse(BaseModel):
    workflow_name: str = Field(description="The name of the workflow")
    workflow_id: uuid.UUID | None = Field(default=None, description="The ID of the workflow")
    deployment_name: str | None = Field(default=None, description="The name of the deployment that ran this execution")
    execution_id: str = Field(description="The ID of the workflow execution")
    parent_execution_id: str | None = Field(None, description="The parent execution ID of the workflow execution")
    root_execution_id: str = Field(description="The root execution ID of the workflow execution")
    run_id: str | None = Field(default=None, description="The unique run identifier (database UUID)")
    user_id: str | None = Field(default=None, description="The ID of the user who triggered the execution")
    status: WorkflowExecutionStatus | None = Field(description="The status of the workflow execution")
    start_time: datetime = Field(description="The start time of the workflow execution")
    end_time: datetime | None = Field(description="The end time of the workflow execution, if available")
    total_duration_ms: int | None = Field(default=None, description="The total duration of the trace in milliseconds")


WorkflowRunWithoutResultResponse = WorkflowExecutionWithoutResultResponse


class RunSummary(BaseModel):
    execution_id: str = Field(description="The ID of the workflow execution")
    run_id: uuid.UUID = Field(description="The unique run identifier (database UUID)")
    status: WorkflowExecutionStatus = Field(description="Execution status")
    duration_ms: int | None = Field(description="Execution duration in milliseconds")
    start_time: datetime = Field(description="When the execution started")


class WorkflowBasicDefinitionWithMetadata(WorkflowBasicDefinition):
    run_count: int | float = Field(
        description="The total number of runs of the workflow, including retries. Deprecated: prefer execution_count.",
        deprecated=True,
    )
    execution_count: int | float = Field(
        description="The number of distinct executions of the workflow (excludes retried runs of the same execution)"
    )
    last_run: WorkflowExecutionWithoutResultResponse | None = Field(
        default=None, description="The last run of the workflow"
    )
    is_active: bool = Field(description="Whether a worker is currently available to run the workflow")
    available_in_chat_assistant: bool = Field(description="Whether the workflow is available in the chat assistant")
    # None when favorite status is not computed (e.g. public API), False/True when resolved for a specific user
    is_favorite: bool | None = Field(default=None, description="Whether the workflow is favorited by the current user")


class RunMetricsResponse(BaseModel):
    stats: dict[str, list[RunSummary]] = Field(description="Mapping of workflow ID to its recent run summaries")
    reliability: dict[str, float | None] = Field(
        description="Mapping of workflow ID to overall success rate (0.0–1.0), null if no runs"
    )


class WorkflowListResponseInternal(BaseModel):
    workflows: Sequence[WorkflowBasicDefinitionWithMetadata] = Field(description="A list of workflows")
    next_cursor: CoercedStr | None


class WorkflowGetResponseInternal(BaseModel):
    workflow: WorkflowBasicDefinitionWithMetadata = Field(description="The workflow")


class WorkflowListResponse(BaseModel):
    workflows: Sequence[WorkflowBasicDefinition] = Field(description="A list of workflows")
    next_cursor: CoercedStr | None


class WorkflowSpecResponse(BaseModel):
    workflow: WorkflowSpecWithTaskQueue = Field(description="The workflow spec")


class WorkflowUpdateRequest(BaseModel):
    display_name: str | None = Field(None, description="New display name value", max_length=128)
    description: str | None = Field(None, description="New description value")
    available_in_chat_assistant: bool | None = Field(
        None, description="Whether to make the workflow available in the chat assistant"
    )
    tags: List[str] | None = Field(None, description="New tags. Replaces the existing tag list.")

    @field_validator("tags")
    @classmethod
    def _validate_tags(cls, v: List[str] | None) -> List[str] | None:
        if v is None:
            return v
        return validate_workflow_tags(v)

    @model_validator(mode="after")
    def validate_display_name_not_empty(self) -> Self:
        if self.display_name is not None and self.display_name.strip() == "":
            raise ValueError("display_name cannot be empty")
        return self


class WorkflowUpdateResponse(BaseModel):
    workflow: Workflow = Field(description="Updated workflow")


class WorkflowExecutionRequest(BaseModel):
    execution_id: str | None = Field(
        default=None,
        max_length=EXECUTION_ID_MAX_LENGTH,
        description="Allows you to specify a custom execution ID. If not provided, a random ID will be generated.",
    )
    input: Dict | None = Field(
        description="The input to the workflow. This should be a dictionary or a BaseModel that matches the workflow's"
        " input schema.",
        default=None,
        json_schema_extra={
            "additionalProperties": True,
            "anyOf": [
                {"type": "object", "additionalProperties": True},  # to accept dicts in the generated client
                {"type": "object", "properties": {}},  # to accept BaseModel in the generated client
                {"type": "null"},
            ],
        },
    )
    # Hidden from generated SDKs. The clean way is Annotated[..., SdkFieldVisibility(SdkVisibility.EXCLUDED)]
    # from kazekit (see openapi/.agents/skills/add-endpoint-to-sdk/SKILL.md), but workflow_sdk doesn't
    # depend on kazekit. Once WFL-946 moves this schema to abraxas we can switch to kazekit.
    encoded_input: NetworkEncodedInput | None = Field(
        description="Encoded input to the workflow, used when payload encoding is enabled.",
        default=None,
        json_schema_extra={"x-mistral-field-visibility": "excluded"},
    )
    wait_for_result: bool = Field(
        default=False, description="If true, wait for the workflow to complete and return the result directly."
    )
    timeout_seconds: float | None = Field(
        default=None,
        description="Maximum time to wait for completion when wait_for_result is true.",
    )
    custom_tracing_attributes: dict[str, str] | None = Field(default=None)
    force_new_trace: bool = Field(
        default=False,
        description="If true, ignore the caller's trace context and start a new, independent trace for "
        "this execution instead of joining the caller's trace.",
    )
    extensions: Dict[str, Any] | None = Field(
        default=None,
        description="Plugin-specific data to propagate into WorkflowContext.extensions at execution time.",
    )
    task_queue: str | None = Field(
        default=None,
        description="Deprecated. Use deployment_name instead.",
        deprecated="Deprecated. Use deployment_name instead.",
        # TODO for SDK 4: json_schema_extra={"x-mistral-field-visibility": "excluded"},
    )
    deployment_name: DeploymentName = Field(
        default=None, description="Name of the deployment to route this execution to"
    )

    @model_validator(mode="after")
    def validate_input_fields(self) -> Self:
        if self.input is not None and self.encoded_input is not None:
            raise ValueError("Only one of 'input' or 'encoded_input' can be provided")
        # TODO: once all SDK users have migrated to `encoded_input`, reject `b64payload` in `input`
        return self

    @field_validator("execution_id")
    @classmethod
    def validate_execution_id(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not EXECUTION_ID_PATTERN.match(v):
            raise ValueError(
                "Execution ID is invalid. "
                "IDs can only contain alphanumeric characters, hyphens (-), and underscores (_)."
            )
        return v


class WorkflowExecutionResponse(WorkflowExecutionWithoutResultResponse):
    result: Any | None = Field(description="The result of the workflow execution, if available")


WorkflowRunResponse = WorkflowExecutionResponse


class WorkflowExecutionListResponse(BaseModel):
    """Deprecated: use WorkflowRunListResponse instead. Will be removed in the next major version."""

    executions: List[WorkflowExecutionWithoutResultResponse] = Field(description="A list of workflow executions")

    next_page_token: str | None = Field(
        default=None, description="Token to use for fetching the next page of results. Null if this is the last page."
    )


class WorkflowRunListResponse(BaseModel):
    runs: List[WorkflowExecutionWithoutResultResponse] = Field(description="A list of workflow runs")

    next_page_token: str | None = Field(
        default=None, description="Token to use for fetching the next page of results. Null if this is the last page."
    )


type WorkflowExecutionTraceSummaryAttributesValues = str | int | float | bool | list | None
WorkflowExecutionTraceSummaryAttributes = Dict[str, WorkflowExecutionTraceSummaryAttributesValues]


class WorkflowExecutionTraceEvent(BaseModel):
    type: EventType = EventType.EVENT

    name: str = Field(description="Name of the event")
    id: str = Field(description="The ID of the event")
    timestamp_unix_nano: int = Field(description="The timestamp of the event in nanoseconds since the Unix epoch")
    attributes: WorkflowExecutionTraceSummaryAttributes = Field(description="The attributes of the event")
    internal: bool = Field(default=False, description="Whether the event is internal")


class WorkflowExecutionProgressTraceEvent(WorkflowExecutionTraceEvent):
    type: EventType = EventType.EVENT_PROGRESS

    status: EventProgressStatus = Field(default=EventProgressStatus.RUNNING, description="The progress message")
    start_time_unix_ms: int = Field(description="The start time of the event in milliseconds since the Unix epoch")
    end_time_unix_ms: int | None = Field(
        default=None, description="The end time of the event in milliseconds since the Unix epoch"
    )
    error: str | None = Field(default=None, description="The error message, if any")


class WorkflowExecutionTraceSummarySpan(BaseModel):
    span_id: str = Field(description="The ID of the span")
    name: str = Field(description="The name of the span")
    start_time_unix_nano: int = Field(description="The start time of the span in nanoseconds since the Unix epoch")
    end_time_unix_nano: int | None = Field(description="The end time of the span in nanoseconds since the Unix epoch")
    attributes: WorkflowExecutionTraceSummaryAttributes = Field(description="The attributes of the span")
    events: List[WorkflowExecutionTraceEvent] = Field(description="The events of the span")
    children: List["WorkflowExecutionTraceSummarySpan"] = Field(
        default_factory=list, description="The child spans of the span"
    )


class WorkflowExecutionTraceOTelResponse(WorkflowExecutionResponse):
    data_source: str = Field(description="The data source of the trace")
    otel_trace_id: str | None = Field(default=None, description="The ID of the trace")
    otel_trace_data: TempoGetTraceResponse | None = Field(default=None, description="The raw OpenTelemetry trace data")


class WorkflowExecutionTraceSummaryResponse(WorkflowExecutionResponse):
    span_tree: WorkflowExecutionTraceSummarySpan | None = Field(default=None, description="The root span of the trace")


class WorkflowExecutionTraceEventsResponse(WorkflowExecutionResponse):
    events: List[WorkflowExecutionTraceEvent | WorkflowExecutionProgressTraceEvent] = Field(
        default_factory=list, description="The events of the workflow execution"
    )


class WorkflowExecutionSyncResponse(BaseModel):
    """Response model for synchronous workflow execution"""

    workflow_name: str = Field(description="Name of the workflow that was executed")
    execution_id: str = Field(description="ID of the workflow execution")
    result: Any = Field(description="The result of the workflow execution")


class SignalWorkflowRequest(BaseModel):
    execution_id: str = Field(description="The ID of the workflow execution")
    signal_name: str = Field(description="The name of the signal to send")
    input: NetworkEncodedInput | Dict[str, Any] | None = Field(
        default=None, description="Input data for the signal, matching its schema"
    )


class SignalWorkflowResponse(BaseModel):
    message: str = Field(default="Signal accepted")


class QueryWorkflowRequest(BaseModel):
    execution_id: str = Field(description="The ID of the workflow execution")
    query_name: str = Field(description="the name of the query to request")
    input: NetworkEncodedInput | Dict[str, Any] | None = Field(
        default=None, description="Input data for the query, matching its schema (Deprecated)"
    )


class QueryWorkflowResponse(BaseModel):
    query_name: str
    result: Any = Field(description="The result of the Query workflow call")


class UpdateWorkflowRequest(BaseModel):
    execution_id: str = Field(description="The ID of the workflow execution")
    update_name: str = Field(description="the name of the update to request")
    input: NetworkEncodedInput | Dict[str, Any] | None = Field(
        default=None, description="Input data for the update, matching its schema (Deprecated)"
    )


class UpdateWorkflowResponse(BaseModel):
    update_name: str
    result: Any = Field(description="The result of the Update workflow call")


class TerminateWorkflowRequest(BaseModel):
    execution_id: str = Field(description="The ID of the workflow execution")


class CancelWorkflowRequest(BaseModel):
    execution_id: str = Field(description="The ID of the workflow execution")


class ResetWorkflowRequest(BaseModel):
    execution_id: str = Field(description="The ID of the workflow execution")
    event_id: int = Field(description="The event ID to reset the workflow execution to")
    reason: str | None = Field(default=None, description="Reason for resetting the workflow execution")
    exclude_signals: bool = Field(
        default=False, description="Whether to exclude signals that happened after the reset point"
    )
    exclude_updates: bool = Field(
        default=False, description="Whether to exclude updates that happened after the reset point"
    )


class SignalInvocationBody(BaseModel):
    name: str = Field(description="The name of the signal to send")
    input: NetworkEncodedInput | Dict[str, Any] | None = Field(
        default=None,
        description="Input data for the signal, matching its schema",
        json_schema_extra={"additionalProperties": True},
    )


class QueryInvocationBody(BaseModel):
    name: str = Field(description="The name of the query to request")
    input: NetworkEncodedInput | Dict[str, Any] | None = Field(
        default=None, description="Input data for the query, matching its schema"
    )


class UpdateInvocationBody(BaseModel):
    name: str = Field(description="The name of the update to request")
    input: NetworkEncodedInput | Dict[str, Any] | None = Field(
        default=None, description="Input data for the update, matching its schema"
    )


class ResetInvocationBody(BaseModel):
    event_id: int = Field(description="The event ID to reset the workflow execution to")
    reason: str | None = Field(default=None, description="Reason for resetting the workflow execution")
    exclude_signals: bool = Field(
        default=False, description="Whether to exclude signals that happened after the reset point"
    )
    exclude_updates: bool = Field(
        default=False, description="Whether to exclude updates that happened after the reset point"
    )


class BatchExecutionBody(BaseModel):
    execution_ids: list[str] = Field(min_length=1, max_length=100, description="List of execution IDs to process")


class BatchExecutionResult(BaseModel):
    status: str = Field(description="Status of the operation (success/failure)")
    error: str | None = Field(default=None, description="Error message if operation failed")


class BatchExecutionResponse(BaseModel):
    results: dict[str, BatchExecutionResult] = Field(
        default_factory=dict,
        description="Mapping of execution_id to result with status and optional error message",
    )


class WorkflowScheduleRequest(BaseModel):
    schedule: ScheduleDefinition = Field(description="The schedule definition")
    workflow_registration_id: uuid.UUID | None = Field(
        default=None, description="The ID of the workflow registration to schedule"
    )
    # Deprecated alias kept for backward compatibility
    workflow_version_id: uuid.UUID | None = Field(default=None, description="Deprecated: use workflow_registration_id")

    workflow_identifier: str | None = Field(default=None, description="The name or ID of the workflow to schedule")
    workflow_task_queue: str | None = Field(
        default=None,
        description="Deprecated. Use deployment_name instead.",
        deprecated="Deprecated. Use deployment_name instead.",
        # TODO for SDK 4: json_schema_extra={"x-mistral-field-visibility": "excluded"},
    )

    schedule_id: str | None = Field(
        default=None,
        description="Allows you to specify a custom schedule ID. If not provided, a random ID will be generated.",
    )
    deployment_name: DeploymentName = Field(
        default=None, description="Name of the deployment to route this schedule to"
    )

    @model_validator(mode="after")
    def check_workflow_registration_identifiers(self) -> Self:
        # Coerce deprecated field
        if self.workflow_version_id and not self.workflow_registration_id:
            self.workflow_registration_id = self.workflow_version_id
        if not self.workflow_registration_id and not self.workflow_identifier:
            raise ValueError("Either workflow_registration_id or workflow_identifier must be provided")
        if self.workflow_registration_id and self.workflow_identifier:
            raise ValueError("Only one of workflow_registration_id or workflow_identifier can be provided")
        return self


class WorkflowScheduleResponse(BaseModel):
    schedule_id: str = Field(description="The ID of the schedule")


class WorkflowScheduleListResponse(BaseModel):
    schedules: List[ScheduleDefinitionOutput] = Field(description="A list of workflow schedules")
    next_page_token: str | None = Field(default=None, description="Token for the next page of results")


class WorkflowScheduleUpdateRequest(BaseModel):
    schedule: PartialScheduleDefinition = Field(
        description="Partial schedule definition to update. Unset fields preserve existing values.",
    )


class WorkflowChatAssistantPublishRequest(BaseModel):
    available_in_chat_assistant: bool = Field(description="Whether to publish the workflow to the chat assistant")


class WorkflowChatAssistantPublishResponse(BaseModel):
    workflow: Workflow = Field()


class WorkflowSchedulePauseRequest(BaseModel):
    note: str | None = Field(
        default=None,
        description="Optional note recorded in Temporal when pausing or resuming a schedule",
    )


class NameListResponse(BaseModel):
    names: list[str] = Field(description="List of distinct names")
    next_cursor: CoercedStr | None = Field(default=None, description="Cursor for the next page of results")


class WorkflowScheduleTriggerRequest(BaseModel):
    overlap: ScheduleOverlapPolicy | None = Field(
        default=None,
        description="Optional overlap policy override to use for the immediate trigger.",
    )
