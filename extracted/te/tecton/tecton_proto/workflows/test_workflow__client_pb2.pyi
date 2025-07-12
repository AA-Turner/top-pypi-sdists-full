from tecton_proto.workflows import state_machine_workflow__client_pb2 as _state_machine_workflow__client_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

CANCELED: TestWorkflowState
DESCRIPTOR: _descriptor.FileDescriptor
RUNNING: TestWorkflowState
SUCCESS: TestWorkflowState
UNKNOWN: TestWorkflowState

class TestWorkflow(_message.Message):
    __slots__ = ["current_iteration", "iteration_sleep_secs", "max_iterations", "num_attempts", "state"]
    CURRENT_ITERATION_FIELD_NUMBER: _ClassVar[int]
    ITERATION_SLEEP_SECS_FIELD_NUMBER: _ClassVar[int]
    MAX_ITERATIONS_FIELD_NUMBER: _ClassVar[int]
    NUM_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    current_iteration: int
    iteration_sleep_secs: int
    max_iterations: int
    num_attempts: int
    state: TestWorkflowState
    def __init__(self, max_iterations: _Optional[int] = ..., iteration_sleep_secs: _Optional[int] = ..., current_iteration: _Optional[int] = ..., state: _Optional[_Union[TestWorkflowState, str]] = ..., num_attempts: _Optional[int] = ...) -> None: ...

class TestWorkflowState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
