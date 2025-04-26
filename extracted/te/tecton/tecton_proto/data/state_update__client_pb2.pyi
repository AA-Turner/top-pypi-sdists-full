from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import fco_args__client_pb2 as _fco_args__client_pb2
from tecton_proto.args import repo_metadata__client_pb2 as _repo_metadata__client_pb2
from tecton_proto.auth import principal__client_pb2 as _principal__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

AUTO: PlanIntegrationTestSelectType
CREATE: FcoTransitionType
DELETE: FcoTransitionType
DESCRIPTOR: _descriptor.FileDescriptor
JOB_STATUS_CANCELLED: IntegrationTestJobStatus
JOB_STATUS_FAILED: IntegrationTestJobStatus
JOB_STATUS_NOT_STARTED: IntegrationTestJobStatus
JOB_STATUS_RUNNING: IntegrationTestJobStatus
JOB_STATUS_SUCCEED: IntegrationTestJobStatus
JOB_STATUS_UNSPECIFIED: IntegrationTestJobStatus
MATERIALIZATION_TASK_DIFF_DESTINATION_BULK_LOAD_ONLINE: MaterializationTaskDiffDestination
MATERIALIZATION_TASK_DIFF_DESTINATION_OFFLINE: MaterializationTaskDiffDestination
MATERIALIZATION_TASK_DIFF_DESTINATION_ONLINE: MaterializationTaskDiffDestination
MATERIALIZATION_TASK_DIFF_DESTINATION_ONLINE_AND_OFFLINE: MaterializationTaskDiffDestination
MATERIALIZATION_TASK_DIFF_DESTINATION_UNSPECIFIED: MaterializationTaskDiffDestination
NONE: PlanIntegrationTestSelectType
PLAN_APPLIED: PlanStatusType
PLAN_APPLY_FAILED: PlanStatusType
PLAN_CREATED: PlanStatusType
PLAN_INTEGRATION_TESTS_CANCELLED: PlanStatusType
PLAN_INTEGRATION_TESTS_FAILED: PlanStatusType
PLAN_INTEGRATION_TESTS_NOT_STARTED: PlanStatusType
PLAN_INTEGRATION_TESTS_RUNNING: PlanStatusType
PLAN_INTEGRATION_TESTS_SKIPPED: PlanStatusType
PLAN_INTEGRATION_TESTS_SUCCEED: PlanStatusType
PLAN_UNSPECIFIED: PlanStatusType
RECREATE: FcoTransitionType
RESTART_STREAM_CHECKPOINTS_INVALIDATED: FcoTransitionSideEffectStreamRestartType
RESTART_STREAM_NONE: FcoTransitionSideEffectStreamRestartType
RESTART_STREAM_REUSE_CHECKPOINTS: FcoTransitionSideEffectStreamRestartType
SELECTED_FEATURE_VIEWS: PlanIntegrationTestSelectType
UNCHANGED: FcoTransitionType
UNKNOWN: FcoTransitionType
UNSPECIFIED: PlanIntegrationTestSelectType
UPDATE: FcoTransitionType
UPGRADE: FcoTransitionType

class BackfillFeaturePublishTaskDiff(_message.Message):
    __slots__ = ["display_string", "feature_end_time", "feature_start_time", "number_of_jobs"]
    DISPLAY_STRING_FIELD_NUMBER: _ClassVar[int]
    FEATURE_END_TIME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_JOBS_FIELD_NUMBER: _ClassVar[int]
    display_string: str
    feature_end_time: _timestamp_pb2.Timestamp
    feature_start_time: _timestamp_pb2.Timestamp
    number_of_jobs: int
    def __init__(self, display_string: _Optional[str] = ..., feature_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., feature_end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., number_of_jobs: _Optional[int] = ...) -> None: ...

class BackfillMaterializationTaskDiff(_message.Message):
    __slots__ = ["destination", "display_string", "feature_end_time", "feature_start_time", "number_of_jobs"]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_STRING_FIELD_NUMBER: _ClassVar[int]
    FEATURE_END_TIME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_JOBS_FIELD_NUMBER: _ClassVar[int]
    destination: MaterializationTaskDiffDestination
    display_string: str
    feature_end_time: _timestamp_pb2.Timestamp
    feature_start_time: _timestamp_pb2.Timestamp
    number_of_jobs: int
    def __init__(self, display_string: _Optional[str] = ..., feature_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., feature_end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., number_of_jobs: _Optional[int] = ..., destination: _Optional[_Union[MaterializationTaskDiffDestination, str]] = ...) -> None: ...

class BatchMaterializationTaskDiff(_message.Message):
    __slots__ = ["destination", "display_string", "schedule_interval"]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_STRING_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    destination: MaterializationTaskDiffDestination
    display_string: str
    schedule_interval: _duration_pb2.Duration
    def __init__(self, display_string: _Optional[str] = ..., schedule_interval: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., destination: _Optional[_Union[MaterializationTaskDiffDestination, str]] = ...) -> None: ...

class FcoDiff(_message.Message):
    __slots__ = ["declared_args", "diff", "existing_args", "materialization_info", "transition_side_effects", "type"]
    DECLARED_ARGS_FIELD_NUMBER: _ClassVar[int]
    DIFF_FIELD_NUMBER: _ClassVar[int]
    EXISTING_ARGS_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_INFO_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_SIDE_EFFECTS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    declared_args: _fco_args__client_pb2.FcoArgs
    diff: _containers.RepeatedCompositeFieldContainer[FcoPropertyDiff]
    existing_args: _fco_args__client_pb2.FcoArgs
    materialization_info: MaterializationInfo
    transition_side_effects: FcoTransitionSideEffects
    type: FcoTransitionType
    def __init__(self, type: _Optional[_Union[FcoTransitionType, str]] = ..., transition_side_effects: _Optional[_Union[FcoTransitionSideEffects, _Mapping]] = ..., existing_args: _Optional[_Union[_fco_args__client_pb2.FcoArgs, _Mapping]] = ..., declared_args: _Optional[_Union[_fco_args__client_pb2.FcoArgs, _Mapping]] = ..., diff: _Optional[_Iterable[_Union[FcoPropertyDiff, _Mapping]]] = ..., materialization_info: _Optional[_Union[MaterializationInfo, _Mapping]] = ...) -> None: ...

class FcoFieldRef(_message.Message):
    __slots__ = ["fco_id"]
    FCO_ID_FIELD_NUMBER: _ClassVar[int]
    fco_id: _id__client_pb2.Id
    def __init__(self, fco_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ...) -> None: ...

class FcoPropertyDiff(_message.Message):
    __slots__ = ["custom_comparator", "property_name", "rendering_type", "val_declared", "val_existing"]
    CUSTOM_COMPARATOR_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_NAME_FIELD_NUMBER: _ClassVar[int]
    RENDERING_TYPE_FIELD_NUMBER: _ClassVar[int]
    VAL_DECLARED_FIELD_NUMBER: _ClassVar[int]
    VAL_EXISTING_FIELD_NUMBER: _ClassVar[int]
    custom_comparator: _diff_options__client_pb2.CustomComparator
    property_name: str
    rendering_type: _diff_options__client_pb2.FcoPropertyRenderingType
    val_declared: str
    val_existing: str
    def __init__(self, property_name: _Optional[str] = ..., val_existing: _Optional[str] = ..., val_declared: _Optional[str] = ..., rendering_type: _Optional[_Union[_diff_options__client_pb2.FcoPropertyRenderingType, str]] = ..., custom_comparator: _Optional[_Union[_diff_options__client_pb2.CustomComparator, str]] = ...) -> None: ...

class FcoTransitionSideEffects(_message.Message):
    __slots__ = ["stream_restart_type"]
    STREAM_RESTART_TYPE_FIELD_NUMBER: _ClassVar[int]
    stream_restart_type: FcoTransitionSideEffectStreamRestartType
    def __init__(self, stream_restart_type: _Optional[_Union[FcoTransitionSideEffectStreamRestartType, str]] = ...) -> None: ...

class IntegrationTestJobSummary(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: IntegrationTestJobStatus
    def __init__(self, status: _Optional[_Union[IntegrationTestJobStatus, str]] = ...) -> None: ...

class MaterializationInfo(_message.Message):
    __slots__ = ["backfill_publish_task_diffs", "backfill_task_diffs", "batch_task_diff", "integration_test_task_diffs", "stream_task_diff"]
    BACKFILL_PUBLISH_TASK_DIFFS_FIELD_NUMBER: _ClassVar[int]
    BACKFILL_TASK_DIFFS_FIELD_NUMBER: _ClassVar[int]
    BATCH_TASK_DIFF_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_TEST_TASK_DIFFS_FIELD_NUMBER: _ClassVar[int]
    STREAM_TASK_DIFF_FIELD_NUMBER: _ClassVar[int]
    backfill_publish_task_diffs: _containers.RepeatedCompositeFieldContainer[BackfillFeaturePublishTaskDiff]
    backfill_task_diffs: _containers.RepeatedCompositeFieldContainer[BackfillMaterializationTaskDiff]
    batch_task_diff: BatchMaterializationTaskDiff
    integration_test_task_diffs: _containers.RepeatedCompositeFieldContainer[PlanIntegrationTestTaskDiff]
    stream_task_diff: StreamMaterializationTaskDiff
    def __init__(self, backfill_task_diffs: _Optional[_Iterable[_Union[BackfillMaterializationTaskDiff, _Mapping]]] = ..., batch_task_diff: _Optional[_Union[BatchMaterializationTaskDiff, _Mapping]] = ..., stream_task_diff: _Optional[_Union[StreamMaterializationTaskDiff, _Mapping]] = ..., backfill_publish_task_diffs: _Optional[_Iterable[_Union[BackfillFeaturePublishTaskDiff, _Mapping]]] = ..., integration_test_task_diffs: _Optional[_Iterable[_Union[PlanIntegrationTestTaskDiff, _Mapping]]] = ...) -> None: ...

class PlanIntegrationTestConfig(_message.Message):
    __slots__ = ["auto_apply_upon_test_success", "feature_view_names"]
    AUTO_APPLY_UPON_TEST_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAMES_FIELD_NUMBER: _ClassVar[int]
    auto_apply_upon_test_success: bool
    feature_view_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, auto_apply_upon_test_success: bool = ..., feature_view_names: _Optional[_Iterable[str]] = ...) -> None: ...

class PlanIntegrationTestSummary(_message.Message):
    __slots__ = ["feature_view_id", "feature_view_name", "job_summaries"]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    JOB_SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    feature_view_id: _id__client_pb2.Id
    feature_view_name: str
    job_summaries: _containers.RepeatedCompositeFieldContainer[IntegrationTestJobSummary]
    def __init__(self, feature_view_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., job_summaries: _Optional[_Iterable[_Union[IntegrationTestJobSummary, _Mapping]]] = ..., feature_view_name: _Optional[str] = ...) -> None: ...

class PlanIntegrationTestTaskDiff(_message.Message):
    __slots__ = ["display_string", "feature_view_name"]
    DISPLAY_STRING_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    display_string: str
    feature_view_name: str
    def __init__(self, display_string: _Optional[str] = ..., feature_view_name: _Optional[str] = ...) -> None: ...

class StateUpdateEntry(_message.Message):
    __slots__ = ["applied_at", "applied_by", "applied_by_principal", "commit_id", "created_at", "created_by", "error", "sdk_version", "status_type", "successful_plan_output", "workspace"]
    APPLIED_AT_FIELD_NUMBER: _ClassVar[int]
    APPLIED_BY_FIELD_NUMBER: _ClassVar[int]
    APPLIED_BY_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: _ClassVar[int]
    STATUS_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUCCESSFUL_PLAN_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    applied_at: _timestamp_pb2.Timestamp
    applied_by: str
    applied_by_principal: _principal__client_pb2.PrincipalBasic
    commit_id: str
    created_at: _timestamp_pb2.Timestamp
    created_by: str
    error: str
    sdk_version: str
    status_type: PlanStatusType
    successful_plan_output: SuccessfulPlanOutput
    workspace: str
    def __init__(self, commit_id: _Optional[str] = ..., applied_by: _Optional[str] = ..., applied_by_principal: _Optional[_Union[_principal__client_pb2.PrincipalBasic, _Mapping]] = ..., applied_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., workspace: _Optional[str] = ..., sdk_version: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status_type: _Optional[_Union[PlanStatusType, str]] = ..., error: _Optional[str] = ..., successful_plan_output: _Optional[_Union[SuccessfulPlanOutput, _Mapping]] = ..., created_by: _Optional[str] = ...) -> None: ...

class StateUpdatePlanSummary(_message.Message):
    __slots__ = ["applied_at", "applied_by", "applied_by_principal", "created_at", "created_by", "diff_items", "sdk_version", "workspace"]
    APPLIED_AT_FIELD_NUMBER: _ClassVar[int]
    APPLIED_BY_FIELD_NUMBER: _ClassVar[int]
    APPLIED_BY_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    DIFF_ITEMS_FIELD_NUMBER: _ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    applied_at: _timestamp_pb2.Timestamp
    applied_by: str
    applied_by_principal: _principal__client_pb2.PrincipalBasic
    created_at: _timestamp_pb2.Timestamp
    created_by: str
    diff_items: _containers.RepeatedCompositeFieldContainer[StateUpdatePlanSummaryDiff]
    sdk_version: str
    workspace: str
    def __init__(self, diff_items: _Optional[_Iterable[_Union[StateUpdatePlanSummaryDiff, _Mapping]]] = ..., applied_by: _Optional[str] = ..., applied_by_principal: _Optional[_Union[_principal__client_pb2.PrincipalBasic, _Mapping]] = ..., created_by: _Optional[str] = ..., applied_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., workspace: _Optional[str] = ..., sdk_version: _Optional[str] = ...) -> None: ...

class StateUpdatePlanSummaryDiff(_message.Message):
    __slots__ = ["description", "diffs", "fco_type", "materialization_info", "name", "transition_side_effects", "type"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DIFFS_FIELD_NUMBER: _ClassVar[int]
    FCO_TYPE_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_INFO_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_SIDE_EFFECTS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    description: str
    diffs: _containers.RepeatedCompositeFieldContainer[FcoPropertyDiff]
    fco_type: str
    materialization_info: MaterializationInfo
    name: str
    transition_side_effects: FcoTransitionSideEffects
    type: FcoTransitionType
    def __init__(self, fco_type: _Optional[str] = ..., type: _Optional[_Union[FcoTransitionType, str]] = ..., transition_side_effects: _Optional[_Union[FcoTransitionSideEffects, _Mapping]] = ..., diffs: _Optional[_Iterable[_Union[FcoPropertyDiff, _Mapping]]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., materialization_info: _Optional[_Union[MaterializationInfo, _Mapping]] = ...) -> None: ...

class StateUpdateRequest(_message.Message):
    __slots__ = ["fco_args", "plan_integration_config", "plan_integration_type", "repo_source_info", "requested_by", "requested_by_principal", "sdk_version", "suppress_recreates", "upgrade_all", "workspace"]
    FCO_ARGS_FIELD_NUMBER: _ClassVar[int]
    PLAN_INTEGRATION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PLAN_INTEGRATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    REPO_SOURCE_INFO_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_BY_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_BY_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: _ClassVar[int]
    SUPPRESS_RECREATES_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_ALL_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    fco_args: _containers.RepeatedCompositeFieldContainer[_fco_args__client_pb2.FcoArgs]
    plan_integration_config: PlanIntegrationTestConfig
    plan_integration_type: PlanIntegrationTestSelectType
    repo_source_info: _repo_metadata__client_pb2.FeatureRepoSourceInfo
    requested_by: str
    requested_by_principal: _principal__client_pb2.Principal
    sdk_version: str
    suppress_recreates: bool
    upgrade_all: bool
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., fco_args: _Optional[_Iterable[_Union[_fco_args__client_pb2.FcoArgs, _Mapping]]] = ..., repo_source_info: _Optional[_Union[_repo_metadata__client_pb2.FeatureRepoSourceInfo, _Mapping]] = ..., suppress_recreates: bool = ..., upgrade_all: bool = ..., requested_by: _Optional[str] = ..., requested_by_principal: _Optional[_Union[_principal__client_pb2.Principal, _Mapping]] = ..., sdk_version: _Optional[str] = ..., plan_integration_type: _Optional[_Union[PlanIntegrationTestSelectType, str]] = ..., plan_integration_config: _Optional[_Union[PlanIntegrationTestConfig, _Mapping]] = ...) -> None: ...

class StreamMaterializationTaskDiff(_message.Message):
    __slots__ = ["display_string"]
    DISPLAY_STRING_FIELD_NUMBER: _ClassVar[int]
    display_string: str
    def __init__(self, display_string: _Optional[str] = ...) -> None: ...

class SuccessfulPlanOutput(_message.Message):
    __slots__ = ["apply_warnings", "json_output", "num_fcos_changed", "num_warnings", "plan_url", "string_output", "test_summaries"]
    APPLY_WARNINGS_FIELD_NUMBER: _ClassVar[int]
    JSON_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    NUM_FCOS_CHANGED_FIELD_NUMBER: _ClassVar[int]
    NUM_WARNINGS_FIELD_NUMBER: _ClassVar[int]
    PLAN_URL_FIELD_NUMBER: _ClassVar[int]
    STRING_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TEST_SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    apply_warnings: str
    json_output: str
    num_fcos_changed: int
    num_warnings: int
    plan_url: str
    string_output: str
    test_summaries: _containers.RepeatedCompositeFieldContainer[PlanIntegrationTestSummary]
    def __init__(self, string_output: _Optional[str] = ..., json_output: _Optional[str] = ..., apply_warnings: _Optional[str] = ..., num_fcos_changed: _Optional[int] = ..., num_warnings: _Optional[int] = ..., test_summaries: _Optional[_Iterable[_Union[PlanIntegrationTestSummary, _Mapping]]] = ..., plan_url: _Optional[str] = ...) -> None: ...

class ValidationMessage(_message.Message):
    __slots__ = ["fco_refs", "message"]
    FCO_REFS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    fco_refs: _containers.RepeatedCompositeFieldContainer[FcoFieldRef]
    message: str
    def __init__(self, message: _Optional[str] = ..., fco_refs: _Optional[_Iterable[_Union[FcoFieldRef, _Mapping]]] = ...) -> None: ...

class ValidationResult(_message.Message):
    __slots__ = ["errors", "warnings"]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    errors: _containers.RepeatedCompositeFieldContainer[ValidationMessage]
    warnings: _containers.RepeatedCompositeFieldContainer[ValidationMessage]
    def __init__(self, errors: _Optional[_Iterable[_Union[ValidationMessage, _Mapping]]] = ..., warnings: _Optional[_Iterable[_Union[ValidationMessage, _Mapping]]] = ...) -> None: ...

class FcoTransitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FcoTransitionSideEffectStreamRestartType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class MaterializationTaskDiffDestination(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class IntegrationTestJobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class PlanIntegrationTestSelectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class PlanStatusType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
