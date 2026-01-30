import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from nominal.procedures.v1 import procedures_pb2 as _procedures_pb2
from nominal.types import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RepeatStepBehavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REPEAT_STEP_BEHAVIOR_UNSPECIFIED: _ClassVar[RepeatStepBehavior]
    REPEAT_STEP_BEHAVIOR_ISOLATED: _ClassVar[RepeatStepBehavior]

class SearchProcedureExecutionsSortField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_UNSPECIFIED: _ClassVar[SearchProcedureExecutionsSortField]
    SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_CREATED_AT: _ClassVar[SearchProcedureExecutionsSortField]
    SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_STARTED_AT: _ClassVar[SearchProcedureExecutionsSortField]
    SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_FINISHED_AT: _ClassVar[SearchProcedureExecutionsSortField]
    SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_UPDATED_AT: _ClassVar[SearchProcedureExecutionsSortField]

class ProcedureExecutionsServiceError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_UNSPECIFIED: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_NOT_FOUND: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_PROC_NOT_FOUND: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_NODE_NOT_FOUND: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_NODE: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_GRAPH: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_STEP_TRANSITION: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_SEARCH_TOKEN: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_STEP_UPDATE: _ClassVar[ProcedureExecutionsServiceError]
REPEAT_STEP_BEHAVIOR_UNSPECIFIED: RepeatStepBehavior
REPEAT_STEP_BEHAVIOR_ISOLATED: RepeatStepBehavior
SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_UNSPECIFIED: SearchProcedureExecutionsSortField
SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_CREATED_AT: SearchProcedureExecutionsSortField
SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_STARTED_AT: SearchProcedureExecutionsSortField
SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_FINISHED_AT: SearchProcedureExecutionsSortField
SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_UPDATED_AT: SearchProcedureExecutionsSortField
PROCEDURE_EXECUTIONS_SERVICE_ERROR_UNSPECIFIED: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_NOT_FOUND: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_PROC_NOT_FOUND: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_NODE_NOT_FOUND: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_NODE: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_GRAPH: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_STEP_TRANSITION: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_SEARCH_TOKEN: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_STEP_UPDATE: ProcedureExecutionsServiceError

class ProcedureExecutionNode(_message.Message):
    __slots__ = ("section", "step")
    SECTION_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    section: ProcedureExecutionSectionNode
    step: ProcedureExecutionStepNode
    def __init__(self, section: _Optional[_Union[ProcedureExecutionSectionNode, _Mapping]] = ..., step: _Optional[_Union[ProcedureExecutionStepNode, _Mapping]] = ...) -> None: ...

class ProcedureExecutionSectionNode(_message.Message):
    __slots__ = ("id", "template_node_id", "title", "description", "template_commit_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    template_node_id: str
    title: str
    description: str
    template_commit_id: str
    def __init__(self, id: _Optional[str] = ..., template_node_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., template_commit_id: _Optional[str] = ...) -> None: ...

class ProcedureExecutionStepNode(_message.Message):
    __slots__ = ("id", "template_node_id", "is_outdated", "state", "value", "auto_proceed_config", "success_condition_status", "completion_action_statuses", "outputs", "template_commit_id")
    class OutputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FieldOutput
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[FieldOutput, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    IS_OUTDATED_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    AUTO_PROCEED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_CONDITION_STATUS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_ACTION_STATUSES_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    template_node_id: str
    is_outdated: bool
    state: ExecutionStepState
    value: StepContentValue
    auto_proceed_config: _procedures_pb2.AutoProceedConfig
    success_condition_status: SuccessConditionStatus
    completion_action_statuses: _containers.RepeatedCompositeFieldContainer[CompletionActionStatus]
    outputs: _containers.MessageMap[str, FieldOutput]
    template_commit_id: str
    def __init__(self, id: _Optional[str] = ..., template_node_id: _Optional[str] = ..., is_outdated: bool = ..., state: _Optional[_Union[ExecutionStepState, _Mapping]] = ..., value: _Optional[_Union[StepContentValue, _Mapping]] = ..., auto_proceed_config: _Optional[_Union[_procedures_pb2.AutoProceedConfig, _Mapping]] = ..., success_condition_status: _Optional[_Union[SuccessConditionStatus, _Mapping]] = ..., completion_action_statuses: _Optional[_Iterable[_Union[CompletionActionStatus, _Mapping]]] = ..., outputs: _Optional[_Mapping[str, FieldOutput]] = ..., template_commit_id: _Optional[str] = ...) -> None: ...

class ExecutionStepNotStarted(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ExecutionStepSkipped(_message.Message):
    __slots__ = ("skipped_at", "skipped_by", "skip_reason", "started_at", "started_by", "submitted_at", "submitted_by")
    SKIPPED_AT_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_BY_FIELD_NUMBER: _ClassVar[int]
    SKIP_REASON_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_BY_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_BY_FIELD_NUMBER: _ClassVar[int]
    skipped_at: _timestamp_pb2.Timestamp
    skipped_by: str
    skip_reason: str
    started_at: _timestamp_pb2.Timestamp
    started_by: str
    submitted_at: _timestamp_pb2.Timestamp
    submitted_by: str
    def __init__(self, skipped_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., skipped_by: _Optional[str] = ..., skip_reason: _Optional[str] = ..., started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_by: _Optional[str] = ..., submitted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., submitted_by: _Optional[str] = ...) -> None: ...

class ExecutionStepInProgress(_message.Message):
    __slots__ = ("started_at", "started_by")
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_BY_FIELD_NUMBER: _ClassVar[int]
    started_at: _timestamp_pb2.Timestamp
    started_by: str
    def __init__(self, started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_by: _Optional[str] = ...) -> None: ...

class ExecutionStepSubmitted(_message.Message):
    __slots__ = ("started_at", "started_by", "submitted_at", "submitted_by")
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_BY_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_BY_FIELD_NUMBER: _ClassVar[int]
    started_at: _timestamp_pb2.Timestamp
    started_by: str
    submitted_at: _timestamp_pb2.Timestamp
    submitted_by: str
    def __init__(self, started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_by: _Optional[str] = ..., submitted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., submitted_by: _Optional[str] = ...) -> None: ...

class ExecutionStepSucceeded(_message.Message):
    __slots__ = ("started_at", "started_by", "submitted_at", "submitted_by", "succeeded_at", "succeeded_by")
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_BY_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_BY_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_AT_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_BY_FIELD_NUMBER: _ClassVar[int]
    started_at: _timestamp_pb2.Timestamp
    started_by: str
    submitted_at: _timestamp_pb2.Timestamp
    submitted_by: str
    succeeded_at: _timestamp_pb2.Timestamp
    succeeded_by: str
    def __init__(self, started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_by: _Optional[str] = ..., submitted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., submitted_by: _Optional[str] = ..., succeeded_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., succeeded_by: _Optional[str] = ...) -> None: ...

class ExecutionStepErrored(_message.Message):
    __slots__ = ("started_at", "started_by", "submitted_at", "submitted_by", "errored_at", "errored_by", "error", "skipped_at", "skipped_by", "skip_reason", "succeeded_at", "succeeded_by")
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_BY_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_BY_FIELD_NUMBER: _ClassVar[int]
    ERRORED_AT_FIELD_NUMBER: _ClassVar[int]
    ERRORED_BY_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_AT_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_BY_FIELD_NUMBER: _ClassVar[int]
    SKIP_REASON_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_AT_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_BY_FIELD_NUMBER: _ClassVar[int]
    started_at: _timestamp_pb2.Timestamp
    started_by: str
    submitted_at: _timestamp_pb2.Timestamp
    submitted_by: str
    errored_at: _timestamp_pb2.Timestamp
    errored_by: str
    error: str
    skipped_at: _timestamp_pb2.Timestamp
    skipped_by: str
    skip_reason: str
    succeeded_at: _timestamp_pb2.Timestamp
    succeeded_by: str
    def __init__(self, started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_by: _Optional[str] = ..., submitted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., submitted_by: _Optional[str] = ..., errored_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., errored_by: _Optional[str] = ..., error: _Optional[str] = ..., skipped_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., skipped_by: _Optional[str] = ..., skip_reason: _Optional[str] = ..., succeeded_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., succeeded_by: _Optional[str] = ...) -> None: ...

class ExecutionStepState(_message.Message):
    __slots__ = ("not_started", "in_progress", "submitted", "skipped", "succeeded", "errored")
    NOT_STARTED_FIELD_NUMBER: _ClassVar[int]
    IN_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    ERRORED_FIELD_NUMBER: _ClassVar[int]
    not_started: ExecutionStepNotStarted
    in_progress: ExecutionStepInProgress
    submitted: ExecutionStepSubmitted
    skipped: ExecutionStepSkipped
    succeeded: ExecutionStepSucceeded
    errored: ExecutionStepErrored
    def __init__(self, not_started: _Optional[_Union[ExecutionStepNotStarted, _Mapping]] = ..., in_progress: _Optional[_Union[ExecutionStepInProgress, _Mapping]] = ..., submitted: _Optional[_Union[ExecutionStepSubmitted, _Mapping]] = ..., skipped: _Optional[_Union[ExecutionStepSkipped, _Mapping]] = ..., succeeded: _Optional[_Union[ExecutionStepSucceeded, _Mapping]] = ..., errored: _Optional[_Union[ExecutionStepErrored, _Mapping]] = ...) -> None: ...

class StepInProgressRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StepSubmittedRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StepSkippedRequest(_message.Message):
    __slots__ = ("skip_reason",)
    SKIP_REASON_FIELD_NUMBER: _ClassVar[int]
    skip_reason: str
    def __init__(self, skip_reason: _Optional[str] = ...) -> None: ...

class StepErroredRequest(_message.Message):
    __slots__ = ("error_reason",)
    ERROR_REASON_FIELD_NUMBER: _ClassVar[int]
    error_reason: str
    def __init__(self, error_reason: _Optional[str] = ...) -> None: ...

class TargetStepStateRequest(_message.Message):
    __slots__ = ("in_progress", "submitted", "skipped", "errored")
    IN_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_FIELD_NUMBER: _ClassVar[int]
    ERRORED_FIELD_NUMBER: _ClassVar[int]
    in_progress: StepInProgressRequest
    submitted: StepSubmittedRequest
    skipped: StepSkippedRequest
    errored: StepErroredRequest
    def __init__(self, in_progress: _Optional[_Union[StepInProgressRequest, _Mapping]] = ..., submitted: _Optional[_Union[StepSubmittedRequest, _Mapping]] = ..., skipped: _Optional[_Union[StepSkippedRequest, _Mapping]] = ..., errored: _Optional[_Union[StepErroredRequest, _Mapping]] = ...) -> None: ...

class ProcedureAsyncTask(_message.Message):
    __slots__ = ("condition_observation",)
    CONDITION_OBSERVATION_FIELD_NUMBER: _ClassVar[int]
    condition_observation: ConditionObservation
    def __init__(self, condition_observation: _Optional[_Union[ConditionObservation, _Mapping]] = ...) -> None: ...

class ConditionObservation(_message.Message):
    __slots__ = ("user_rid", "org_rid", "procedure_execution_rid", "step_id", "success_condition")
    USER_RID_FIELD_NUMBER: _ClassVar[int]
    ORG_RID_FIELD_NUMBER: _ClassVar[int]
    PROCEDURE_EXECUTION_RID_FIELD_NUMBER: _ClassVar[int]
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_CONDITION_FIELD_NUMBER: _ClassVar[int]
    user_rid: str
    org_rid: str
    procedure_execution_rid: str
    step_id: str
    success_condition: _procedures_pb2.SuccessCondition
    def __init__(self, user_rid: _Optional[str] = ..., org_rid: _Optional[str] = ..., procedure_execution_rid: _Optional[str] = ..., step_id: _Optional[str] = ..., success_condition: _Optional[_Union[_procedures_pb2.SuccessCondition, _Mapping]] = ...) -> None: ...

class SuccessConditionStatus(_message.Message):
    __slots__ = ("timer", "ingest_job", "channel_validation", "in_progress", "satisfied", "failed", "canceled", "submitted")
    AND_FIELD_NUMBER: _ClassVar[int]
    TIMER_FIELD_NUMBER: _ClassVar[int]
    INGEST_JOB_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_VALIDATION_FIELD_NUMBER: _ClassVar[int]
    IN_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    SATISFIED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    CANCELED_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_FIELD_NUMBER: _ClassVar[int]
    timer: _procedures_pb2.TimerSuccessCondition
    ingest_job: _procedures_pb2.IngestJobSuccessCondition
    channel_validation: _procedures_pb2.ChannelValidationSuccessCondition
    in_progress: SuccessConditionInProgress
    satisfied: SuccessConditionSatisfied
    failed: SuccessConditionFailed
    canceled: SuccessConditionCanceled
    submitted: SuccessConditionSubmitted
    def __init__(self, timer: _Optional[_Union[_procedures_pb2.TimerSuccessCondition, _Mapping]] = ..., ingest_job: _Optional[_Union[_procedures_pb2.IngestJobSuccessCondition, _Mapping]] = ..., channel_validation: _Optional[_Union[_procedures_pb2.ChannelValidationSuccessCondition, _Mapping]] = ..., in_progress: _Optional[_Union[SuccessConditionInProgress, _Mapping]] = ..., satisfied: _Optional[_Union[SuccessConditionSatisfied, _Mapping]] = ..., failed: _Optional[_Union[SuccessConditionFailed, _Mapping]] = ..., canceled: _Optional[_Union[SuccessConditionCanceled, _Mapping]] = ..., submitted: _Optional[_Union[SuccessConditionSubmitted, _Mapping]] = ..., **kwargs) -> None: ...

class AndSuccessCondition(_message.Message):
    __slots__ = ("conditions",)
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[SuccessConditionStatus]
    def __init__(self, conditions: _Optional[_Iterable[_Union[SuccessConditionStatus, _Mapping]]] = ...) -> None: ...

class SuccessConditionSubmitted(_message.Message):
    __slots__ = ("submitted_at",)
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    submitted_at: _timestamp_pb2.Timestamp
    def __init__(self, submitted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SuccessConditionInProgress(_message.Message):
    __slots__ = ("started_at",)
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    started_at: _timestamp_pb2.Timestamp
    def __init__(self, started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SuccessConditionSatisfied(_message.Message):
    __slots__ = ("started_at", "satisfied_at")
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    SATISFIED_AT_FIELD_NUMBER: _ClassVar[int]
    started_at: _timestamp_pb2.Timestamp
    satisfied_at: _timestamp_pb2.Timestamp
    def __init__(self, started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., satisfied_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SuccessConditionFailed(_message.Message):
    __slots__ = ("started_at", "failed_at", "failure_reason")
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FAILED_AT_FIELD_NUMBER: _ClassVar[int]
    FAILURE_REASON_FIELD_NUMBER: _ClassVar[int]
    started_at: _timestamp_pb2.Timestamp
    failed_at: _timestamp_pb2.Timestamp
    failure_reason: str
    def __init__(self, started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., failed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., failure_reason: _Optional[str] = ...) -> None: ...

class SuccessConditionCanceled(_message.Message):
    __slots__ = ("started_at", "canceled_at")
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    CANCELED_AT_FIELD_NUMBER: _ClassVar[int]
    started_at: _timestamp_pb2.Timestamp
    canceled_at: _timestamp_pb2.Timestamp
    def __init__(self, started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., canceled_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CompletionActionStatus(_message.Message):
    __slots__ = ("state", "create_event", "create_run", "apply_workbook_templates", "apply_checklists")
    STATE_FIELD_NUMBER: _ClassVar[int]
    CREATE_EVENT_FIELD_NUMBER: _ClassVar[int]
    CREATE_RUN_FIELD_NUMBER: _ClassVar[int]
    APPLY_WORKBOOK_TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    APPLY_CHECKLISTS_FIELD_NUMBER: _ClassVar[int]
    state: CompletionActionState
    create_event: CreateEventResult
    create_run: CreateRunResult
    apply_workbook_templates: ApplyWorkbookTemplatesResult
    apply_checklists: ApplyChecklistsResult
    def __init__(self, state: _Optional[_Union[CompletionActionState, _Mapping]] = ..., create_event: _Optional[_Union[CreateEventResult, _Mapping]] = ..., create_run: _Optional[_Union[CreateRunResult, _Mapping]] = ..., apply_workbook_templates: _Optional[_Union[ApplyWorkbookTemplatesResult, _Mapping]] = ..., apply_checklists: _Optional[_Union[ApplyChecklistsResult, _Mapping]] = ...) -> None: ...

class CreateEventResult(_message.Message):
    __slots__ = ("event_rid",)
    EVENT_RID_FIELD_NUMBER: _ClassVar[int]
    event_rid: str
    def __init__(self, event_rid: _Optional[str] = ...) -> None: ...

class CreateRunResult(_message.Message):
    __slots__ = ("run_rid",)
    RUN_RID_FIELD_NUMBER: _ClassVar[int]
    run_rid: str
    def __init__(self, run_rid: _Optional[str] = ...) -> None: ...

class ApplyWorkbookTemplatesResult(_message.Message):
    __slots__ = ("workbook_rids",)
    WORKBOOK_RIDS_FIELD_NUMBER: _ClassVar[int]
    workbook_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, workbook_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class ApplyChecklistsResult(_message.Message):
    __slots__ = ("data_review_rids",)
    DATA_REVIEW_RIDS_FIELD_NUMBER: _ClassVar[int]
    data_review_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, data_review_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class CompletionActionState(_message.Message):
    __slots__ = ("not_run", "succeeded", "error")
    class NotRun(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Succeeded(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    NOT_RUN_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    not_run: CompletionActionState.NotRun
    succeeded: CompletionActionState.Succeeded
    error: str
    def __init__(self, not_run: _Optional[_Union[CompletionActionState.NotRun, _Mapping]] = ..., succeeded: _Optional[_Union[CompletionActionState.Succeeded, _Mapping]] = ..., error: _Optional[str] = ...) -> None: ...

class StepContentValue(_message.Message):
    __slots__ = ("form", "start_ingest", "select_or_create_asset")
    FORM_FIELD_NUMBER: _ClassVar[int]
    START_INGEST_FIELD_NUMBER: _ClassVar[int]
    SELECT_OR_CREATE_ASSET_FIELD_NUMBER: _ClassVar[int]
    form: FormStepValue
    start_ingest: StartIngestStepValue
    select_or_create_asset: SelectOrCreateAssetStepValue
    def __init__(self, form: _Optional[_Union[FormStepValue, _Mapping]] = ..., start_ingest: _Optional[_Union[StartIngestStepValue, _Mapping]] = ..., select_or_create_asset: _Optional[_Union[SelectOrCreateAssetStepValue, _Mapping]] = ...) -> None: ...

class FormStepValue(_message.Message):
    __slots__ = ("fields",)
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[FormFieldValue]
    def __init__(self, fields: _Optional[_Iterable[_Union[FormFieldValue, _Mapping]]] = ...) -> None: ...

class StartIngestStepValue(_message.Message):
    __slots__ = ("ingest_job_rid",)
    INGEST_JOB_RID_FIELD_NUMBER: _ClassVar[int]
    ingest_job_rid: str
    def __init__(self, ingest_job_rid: _Optional[str] = ...) -> None: ...

class SelectOrCreateAssetStepValue(_message.Message):
    __slots__ = ("asset_reference",)
    ASSET_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    asset_reference: _procedures_pb2.AssetReference
    def __init__(self, asset_reference: _Optional[_Union[_procedures_pb2.AssetReference, _Mapping]] = ...) -> None: ...

class FormFieldValue(_message.Message):
    __slots__ = ("asset", "checkbox", "text", "int", "double", "single_enum", "multi_enum", "file_upload", "multi_file_upload")
    ASSET_FIELD_NUMBER: _ClassVar[int]
    CHECKBOX_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    SINGLE_ENUM_FIELD_NUMBER: _ClassVar[int]
    MULTI_ENUM_FIELD_NUMBER: _ClassVar[int]
    FILE_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    MULTI_FILE_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    asset: AssetFieldValue
    checkbox: CheckboxFieldValue
    text: TextFieldValue
    int: IntFieldValue
    double: DoubleFieldValue
    single_enum: SingleEnumFieldValue
    multi_enum: MultiEnumFieldValue
    file_upload: FileUploadFieldValue
    multi_file_upload: MultiFileUploadFieldValue
    def __init__(self, asset: _Optional[_Union[AssetFieldValue, _Mapping]] = ..., checkbox: _Optional[_Union[CheckboxFieldValue, _Mapping]] = ..., text: _Optional[_Union[TextFieldValue, _Mapping]] = ..., int: _Optional[_Union[IntFieldValue, _Mapping]] = ..., double: _Optional[_Union[DoubleFieldValue, _Mapping]] = ..., single_enum: _Optional[_Union[SingleEnumFieldValue, _Mapping]] = ..., multi_enum: _Optional[_Union[MultiEnumFieldValue, _Mapping]] = ..., file_upload: _Optional[_Union[FileUploadFieldValue, _Mapping]] = ..., multi_file_upload: _Optional[_Union[MultiFileUploadFieldValue, _Mapping]] = ...) -> None: ...

class AssetFieldValue(_message.Message):
    __slots__ = ("asset_reference",)
    ASSET_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    asset_reference: _procedures_pb2.AssetReference
    def __init__(self, asset_reference: _Optional[_Union[_procedures_pb2.AssetReference, _Mapping]] = ...) -> None: ...

class CheckboxFieldValue(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bool
    def __init__(self, value: bool = ...) -> None: ...

class TextFieldValue(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class IntFieldValue(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class DoubleFieldValue(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: float
    def __init__(self, value: _Optional[float] = ...) -> None: ...

class SingleEnumFieldValue(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class MultiEnumFieldValue(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, value: _Optional[_Iterable[str]] = ...) -> None: ...

class FileUploadFieldValue(_message.Message):
    __slots__ = ("s3_upload",)
    S3_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    s3_upload: S3UploadFileValue
    def __init__(self, s3_upload: _Optional[_Union[S3UploadFileValue, _Mapping]] = ...) -> None: ...

class S3UploadFileValue(_message.Message):
    __slots__ = ("s3_path", "file_name", "file_type")
    S3_PATH_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    s3_path: str
    file_name: str
    file_type: str
    def __init__(self, s3_path: _Optional[str] = ..., file_name: _Optional[str] = ..., file_type: _Optional[str] = ...) -> None: ...

class MultiFileUploadFieldValue(_message.Message):
    __slots__ = ("uploads",)
    UPLOADS_FIELD_NUMBER: _ClassVar[int]
    uploads: _containers.RepeatedCompositeFieldContainer[FileUploadFieldValue]
    def __init__(self, uploads: _Optional[_Iterable[_Union[FileUploadFieldValue, _Mapping]]] = ...) -> None: ...

class ProcedureExecution(_message.Message):
    __slots__ = ("rid", "metadata", "state")
    RID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    rid: str
    metadata: ProcedureExecutionMetadata
    state: ProcedureExecutionState
    def __init__(self, rid: _Optional[str] = ..., metadata: _Optional[_Union[ProcedureExecutionMetadata, _Mapping]] = ..., state: _Optional[_Union[ProcedureExecutionState, _Mapping]] = ...) -> None: ...

class ProcedureExecutionMetadata(_message.Message):
    __slots__ = ("rid", "procedure_rid", "procedure_commit_id", "title", "description", "labels", "properties", "created_by", "created_at", "updated_by", "updated_at", "started_at", "started_by", "finished_at", "finished_by", "aborted_at", "aborted_by", "failed_at", "failed_by", "failed_reason")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    RID_FIELD_NUMBER: _ClassVar[int]
    PROCEDURE_RID_FIELD_NUMBER: _ClassVar[int]
    PROCEDURE_COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_BY_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_BY_FIELD_NUMBER: _ClassVar[int]
    ABORTED_AT_FIELD_NUMBER: _ClassVar[int]
    ABORTED_BY_FIELD_NUMBER: _ClassVar[int]
    FAILED_AT_FIELD_NUMBER: _ClassVar[int]
    FAILED_BY_FIELD_NUMBER: _ClassVar[int]
    FAILED_REASON_FIELD_NUMBER: _ClassVar[int]
    rid: str
    procedure_rid: str
    procedure_commit_id: str
    title: str
    description: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.ScalarMap[str, str]
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    updated_by: str
    updated_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    started_by: str
    finished_at: _timestamp_pb2.Timestamp
    finished_by: str
    aborted_at: _timestamp_pb2.Timestamp
    aborted_by: str
    failed_at: _timestamp_pb2.Timestamp
    failed_by: str
    failed_reason: str
    def __init__(self, rid: _Optional[str] = ..., procedure_rid: _Optional[str] = ..., procedure_commit_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., created_by: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_by: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_by: _Optional[str] = ..., finished_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., finished_by: _Optional[str] = ..., aborted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., aborted_by: _Optional[str] = ..., failed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., failed_by: _Optional[str] = ..., failed_reason: _Optional[str] = ...) -> None: ...

class ProcedureExecutionState(_message.Message):
    __slots__ = ("global_fields", "nodes", "section_edges", "step_edges")
    class GlobalFieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FieldOutput
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[FieldOutput, _Mapping]] = ...) -> None: ...
    class NodesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProcedureExecutionNode
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProcedureExecutionNode, _Mapping]] = ...) -> None: ...
    class SectionEdgesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _procedures_pb2.NodeList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_procedures_pb2.NodeList, _Mapping]] = ...) -> None: ...
    class StepEdgesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _procedures_pb2.NodeList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_procedures_pb2.NodeList, _Mapping]] = ...) -> None: ...
    GLOBAL_FIELDS_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    SECTION_EDGES_FIELD_NUMBER: _ClassVar[int]
    STEP_EDGES_FIELD_NUMBER: _ClassVar[int]
    global_fields: _containers.MessageMap[str, FieldOutput]
    nodes: _containers.MessageMap[str, ProcedureExecutionNode]
    section_edges: _containers.MessageMap[str, _procedures_pb2.NodeList]
    step_edges: _containers.MessageMap[str, _procedures_pb2.NodeList]
    def __init__(self, global_fields: _Optional[_Mapping[str, FieldOutput]] = ..., nodes: _Optional[_Mapping[str, ProcedureExecutionNode]] = ..., section_edges: _Optional[_Mapping[str, _procedures_pb2.NodeList]] = ..., step_edges: _Optional[_Mapping[str, _procedures_pb2.NodeList]] = ...) -> None: ...

class Strings(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class FieldOutput(_message.Message):
    __slots__ = ("asset_rid", "string_value", "double_value", "boolean_value", "int_value", "strings_value", "ingest_job_rid", "run_rid", "file_upload_value", "multi_file_upload_value")
    ASSET_RID_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRINGS_VALUE_FIELD_NUMBER: _ClassVar[int]
    INGEST_JOB_RID_FIELD_NUMBER: _ClassVar[int]
    RUN_RID_FIELD_NUMBER: _ClassVar[int]
    FILE_UPLOAD_VALUE_FIELD_NUMBER: _ClassVar[int]
    MULTI_FILE_UPLOAD_VALUE_FIELD_NUMBER: _ClassVar[int]
    asset_rid: str
    string_value: str
    double_value: float
    boolean_value: bool
    int_value: int
    strings_value: Strings
    ingest_job_rid: str
    run_rid: str
    file_upload_value: FileUploadFieldValue
    multi_file_upload_value: MultiFileUploadFieldValue
    def __init__(self, asset_rid: _Optional[str] = ..., string_value: _Optional[str] = ..., double_value: _Optional[float] = ..., boolean_value: bool = ..., int_value: _Optional[int] = ..., strings_value: _Optional[_Union[Strings, _Mapping]] = ..., ingest_job_rid: _Optional[str] = ..., run_rid: _Optional[str] = ..., file_upload_value: _Optional[_Union[FileUploadFieldValue, _Mapping]] = ..., multi_file_upload_value: _Optional[_Union[MultiFileUploadFieldValue, _Mapping]] = ...) -> None: ...

class CreateProcedureExecutionRequest(_message.Message):
    __slots__ = ("procedure_rid", "procedure_commit_id", "title", "description", "start_immediately")
    PROCEDURE_RID_FIELD_NUMBER: _ClassVar[int]
    PROCEDURE_COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    START_IMMEDIATELY_FIELD_NUMBER: _ClassVar[int]
    procedure_rid: str
    procedure_commit_id: str
    title: str
    description: str
    start_immediately: bool
    def __init__(self, procedure_rid: _Optional[str] = ..., procedure_commit_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., start_immediately: bool = ...) -> None: ...

class CreateProcedureExecutionResponse(_message.Message):
    __slots__ = ("procedure_execution",)
    PROCEDURE_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    procedure_execution: ProcedureExecution
    def __init__(self, procedure_execution: _Optional[_Union[ProcedureExecution, _Mapping]] = ...) -> None: ...

class GetProcedureExecutionRequest(_message.Message):
    __slots__ = ("procedure_execution_rid", "include_display_graph")
    PROCEDURE_EXECUTION_RID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DISPLAY_GRAPH_FIELD_NUMBER: _ClassVar[int]
    procedure_execution_rid: str
    include_display_graph: bool
    def __init__(self, procedure_execution_rid: _Optional[str] = ..., include_display_graph: bool = ...) -> None: ...

class GetProcedureExecutionResponse(_message.Message):
    __slots__ = ("procedure_execution", "display_graph")
    PROCEDURE_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_GRAPH_FIELD_NUMBER: _ClassVar[int]
    procedure_execution: ProcedureExecution
    display_graph: _procedures_pb2.ProcedureDisplayGraph
    def __init__(self, procedure_execution: _Optional[_Union[ProcedureExecution, _Mapping]] = ..., display_graph: _Optional[_Union[_procedures_pb2.ProcedureDisplayGraph, _Mapping]] = ...) -> None: ...

class UpdateProcedureExecutionMetadataRequest(_message.Message):
    __slots__ = ("procedure_execution_rid", "title", "description", "commit_id", "labels", "properties")
    PROCEDURE_EXECUTION_RID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    procedure_execution_rid: str
    title: str
    description: str
    commit_id: str
    labels: _types_pb2.LabelUpdateWrapper
    properties: _types_pb2.PropertyUpdateWrapper
    def __init__(self, procedure_execution_rid: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., commit_id: _Optional[str] = ..., labels: _Optional[_Union[_types_pb2.LabelUpdateWrapper, _Mapping]] = ..., properties: _Optional[_Union[_types_pb2.PropertyUpdateWrapper, _Mapping]] = ...) -> None: ...

class UpdateProcedureExecutionMetadataResponse(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: ProcedureExecutionMetadata
    def __init__(self, metadata: _Optional[_Union[ProcedureExecutionMetadata, _Mapping]] = ...) -> None: ...

class UpdateProcedureExecutionRequest(_message.Message):
    __slots__ = ("procedure_execution_rid", "title", "description", "commit_id", "labels", "properties", "state", "is_aborted", "started_at", "finished_at")
    PROCEDURE_EXECUTION_RID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    IS_ABORTED_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    procedure_execution_rid: str
    title: str
    description: str
    commit_id: str
    labels: _types_pb2.LabelUpdateWrapper
    properties: _types_pb2.PropertyUpdateWrapper
    state: ProcedureExecutionState
    is_aborted: bool
    started_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    def __init__(self, procedure_execution_rid: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., commit_id: _Optional[str] = ..., labels: _Optional[_Union[_types_pb2.LabelUpdateWrapper, _Mapping]] = ..., properties: _Optional[_Union[_types_pb2.PropertyUpdateWrapper, _Mapping]] = ..., state: _Optional[_Union[ProcedureExecutionState, _Mapping]] = ..., is_aborted: bool = ..., started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., finished_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UpdateProcedureExecutionResponse(_message.Message):
    __slots__ = ("procedure_execution",)
    PROCEDURE_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    procedure_execution: ProcedureExecution
    def __init__(self, procedure_execution: _Optional[_Union[ProcedureExecution, _Mapping]] = ...) -> None: ...

class UpdateStepRequest(_message.Message):
    __slots__ = ("procedure_execution_rid", "step_id", "value", "auto_proceed_config", "target_state")
    PROCEDURE_EXECUTION_RID_FIELD_NUMBER: _ClassVar[int]
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    AUTO_PROCEED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TARGET_STATE_FIELD_NUMBER: _ClassVar[int]
    procedure_execution_rid: str
    step_id: str
    value: StepContentValue
    auto_proceed_config: _procedures_pb2.AutoProceedConfig
    target_state: TargetStepStateRequest
    def __init__(self, procedure_execution_rid: _Optional[str] = ..., step_id: _Optional[str] = ..., value: _Optional[_Union[StepContentValue, _Mapping]] = ..., auto_proceed_config: _Optional[_Union[_procedures_pb2.AutoProceedConfig, _Mapping]] = ..., target_state: _Optional[_Union[TargetStepStateRequest, _Mapping]] = ...) -> None: ...

class UpdateStepResponse(_message.Message):
    __slots__ = ("procedure_execution",)
    PROCEDURE_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    procedure_execution: ProcedureExecution
    def __init__(self, procedure_execution: _Optional[_Union[ProcedureExecution, _Mapping]] = ...) -> None: ...

class UpdateStepSuccessConditionStatusRequest(_message.Message):
    __slots__ = ("procedure_execution_rid", "step_id", "success_condition_status")
    PROCEDURE_EXECUTION_RID_FIELD_NUMBER: _ClassVar[int]
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_CONDITION_STATUS_FIELD_NUMBER: _ClassVar[int]
    procedure_execution_rid: str
    step_id: str
    success_condition_status: SuccessConditionStatus
    def __init__(self, procedure_execution_rid: _Optional[str] = ..., step_id: _Optional[str] = ..., success_condition_status: _Optional[_Union[SuccessConditionStatus, _Mapping]] = ...) -> None: ...

class UpdateStepSuccessConditionStatusResponse(_message.Message):
    __slots__ = ("procedure_execution",)
    PROCEDURE_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    procedure_execution: ProcedureExecution
    def __init__(self, procedure_execution: _Optional[_Union[ProcedureExecution, _Mapping]] = ...) -> None: ...

class RepeatStepRequest(_message.Message):
    __slots__ = ("procedure_execution_rid", "step_id", "behavior", "value", "auto_proceed_config", "target_state")
    PROCEDURE_EXECUTION_RID_FIELD_NUMBER: _ClassVar[int]
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    AUTO_PROCEED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TARGET_STATE_FIELD_NUMBER: _ClassVar[int]
    procedure_execution_rid: str
    step_id: str
    behavior: RepeatStepBehavior
    value: StepContentValue
    auto_proceed_config: _procedures_pb2.AutoProceedConfig
    target_state: TargetStepStateRequest
    def __init__(self, procedure_execution_rid: _Optional[str] = ..., step_id: _Optional[str] = ..., behavior: _Optional[_Union[RepeatStepBehavior, str]] = ..., value: _Optional[_Union[StepContentValue, _Mapping]] = ..., auto_proceed_config: _Optional[_Union[_procedures_pb2.AutoProceedConfig, _Mapping]] = ..., target_state: _Optional[_Union[TargetStepStateRequest, _Mapping]] = ...) -> None: ...

class RepeatStepResponse(_message.Message):
    __slots__ = ("procedure_execution",)
    PROCEDURE_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    procedure_execution: ProcedureExecution
    def __init__(self, procedure_execution: _Optional[_Union[ProcedureExecution, _Mapping]] = ...) -> None: ...

class ProcedureExecutionSearchQuery(_message.Message):
    __slots__ = ("search_text", "label", "property", "workspace", "procedure_rid", "commit_id", "created_by")
    class ProcedureExecutionSearchAndQuery(_message.Message):
        __slots__ = ("queries",)
        QUERIES_FIELD_NUMBER: _ClassVar[int]
        queries: _containers.RepeatedCompositeFieldContainer[ProcedureExecutionSearchQuery]
        def __init__(self, queries: _Optional[_Iterable[_Union[ProcedureExecutionSearchQuery, _Mapping]]] = ...) -> None: ...
    class ProcedureExecutionSearchOrQuery(_message.Message):
        __slots__ = ("queries",)
        QUERIES_FIELD_NUMBER: _ClassVar[int]
        queries: _containers.RepeatedCompositeFieldContainer[ProcedureExecutionSearchQuery]
        def __init__(self, queries: _Optional[_Iterable[_Union[ProcedureExecutionSearchQuery, _Mapping]]] = ...) -> None: ...
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_FIELD_NUMBER: _ClassVar[int]
    AND_FIELD_NUMBER: _ClassVar[int]
    OR_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROCEDURE_RID_FIELD_NUMBER: _ClassVar[int]
    COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    label: str
    property: _types_pb2.Property
    workspace: str
    procedure_rid: str
    commit_id: str
    created_by: str
    def __init__(self, search_text: _Optional[str] = ..., label: _Optional[str] = ..., property: _Optional[_Union[_types_pb2.Property, _Mapping]] = ..., workspace: _Optional[str] = ..., procedure_rid: _Optional[str] = ..., commit_id: _Optional[str] = ..., created_by: _Optional[str] = ..., **kwargs) -> None: ...

class ProcedureExecutionSortOptions(_message.Message):
    __slots__ = ("is_descending", "sort_field")
    IS_DESCENDING_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_FIELD_NUMBER: _ClassVar[int]
    is_descending: bool
    sort_field: SearchProcedureExecutionsSortField
    def __init__(self, is_descending: bool = ..., sort_field: _Optional[_Union[SearchProcedureExecutionsSortField, str]] = ...) -> None: ...

class SearchProcedureExecutionsRequest(_message.Message):
    __slots__ = ("query", "sort_options", "page_size", "next_page_token")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    SORT_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query: ProcedureExecutionSearchQuery
    sort_options: ProcedureExecutionSortOptions
    page_size: int
    next_page_token: str
    def __init__(self, query: _Optional[_Union[ProcedureExecutionSearchQuery, _Mapping]] = ..., sort_options: _Optional[_Union[ProcedureExecutionSortOptions, _Mapping]] = ..., page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class SearchProcedureExecutionsResponse(_message.Message):
    __slots__ = ("procedure_executions", "next_page_token")
    PROCEDURE_EXECUTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    procedure_executions: _containers.RepeatedCompositeFieldContainer[ProcedureExecutionMetadata]
    next_page_token: str
    def __init__(self, procedure_executions: _Optional[_Iterable[_Union[ProcedureExecutionMetadata, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class BatchGetProcedureExecutionMetadataRequest(_message.Message):
    __slots__ = ("procedure_execution_rids",)
    PROCEDURE_EXECUTION_RIDS_FIELD_NUMBER: _ClassVar[int]
    procedure_execution_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, procedure_execution_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class BatchGetProcedureExecutionMetadataResponse(_message.Message):
    __slots__ = ("procedure_executions",)
    PROCEDURE_EXECUTIONS_FIELD_NUMBER: _ClassVar[int]
    procedure_executions: _containers.RepeatedCompositeFieldContainer[ProcedureExecutionMetadata]
    def __init__(self, procedure_executions: _Optional[_Iterable[_Union[ProcedureExecutionMetadata, _Mapping]]] = ...) -> None: ...
