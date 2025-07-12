from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.dataobs import validation_task__client_pb2 as _validation_task__client_pb2
from tecton_proto.workflows import state_machine_workflow__client_pb2 as _state_machine_workflow__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DATA_VALIDATION_TASK_RESULT_INTERRUPTED: ValidationTaskResult
DATA_VALIDATION_TASK_RESULT_UNKNOWN: ValidationTaskResult
DATA_VALIDATION_TASK_RESULT_VALIDATION_FAILED: ValidationTaskResult
DATA_VALIDATION_TASK_RESULT_VALIDATION_PASSED: ValidationTaskResult
DATA_VALIDATION_WORKFLOW_STATE_CANCELLATION_REQUESTED: DataValidationWorkflowState
DATA_VALIDATION_WORKFLOW_STATE_JOB_CANCELED: DataValidationWorkflowState
DATA_VALIDATION_WORKFLOW_STATE_JOB_FAILED: DataValidationWorkflowState
DATA_VALIDATION_WORKFLOW_STATE_JOB_SUBMITTED: DataValidationWorkflowState
DATA_VALIDATION_WORKFLOW_STATE_JOB_SUCCEED: DataValidationWorkflowState
DATA_VALIDATION_WORKFLOW_STATE_STARTED: DataValidationWorkflowState
DATA_VALIDATION_WORKFLOW_STATE_SUBMISSION_FAILED: DataValidationWorkflowState
DATA_VALIDATION_WORKFLOW_STATE_UNKNOWN: DataValidationWorkflowState
DESCRIPTOR: _descriptor.FileDescriptor

class DataValidationWorkflow(_message.Message):
    __slots__ = ["is_completed", "run_details", "state_transitions", "validation_task"]
    IS_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    RUN_DETAILS_FIELD_NUMBER: _ClassVar[int]
    STATE_TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_TASK_FIELD_NUMBER: _ClassVar[int]
    is_completed: bool
    run_details: RunDetails
    state_transitions: _containers.RepeatedCompositeFieldContainer[DataValidationWorkflowStateTransition]
    validation_task: _validation_task__client_pb2.ValidationTask
    def __init__(self, state_transitions: _Optional[_Iterable[_Union[DataValidationWorkflowStateTransition, _Mapping]]] = ..., validation_task: _Optional[_Union[_validation_task__client_pb2.ValidationTask, _Mapping]] = ..., run_details: _Optional[_Union[RunDetails, _Mapping]] = ..., is_completed: bool = ...) -> None: ...

class DataValidationWorkflowStateTransition(_message.Message):
    __slots__ = ["timestamp", "workflow_state"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_STATE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    workflow_state: DataValidationWorkflowState
    def __init__(self, workflow_state: _Optional[_Union[DataValidationWorkflowState, str]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RunDetails(_message.Message):
    __slots__ = ["error_message", "job_start_time", "result"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    JOB_START_TIME_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    job_start_time: _timestamp_pb2.Timestamp
    result: ValidationTaskResult
    def __init__(self, job_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., result: _Optional[_Union[ValidationTaskResult, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class DataValidationWorkflowState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ValidationTaskResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
