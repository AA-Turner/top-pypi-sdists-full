from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.common.v2 import metadata_pb2 as _metadata_pb2
from chalk._gen.chalk.common.v2 import options_pb2 as _options_pb2
from chalk._gen.chalk.expression.v1 import expression_pb2 as _expression_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class ExecutePlanRequest(_message.Message):
    __slots__ = ("lazy_frame_calls", "execution_options", "planning_options")
    LAZY_FRAME_CALLS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PLANNING_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    lazy_frame_calls: _expression_pb2.LogicalExprNode
    execution_options: _options_pb2.ExecutionOptions
    planning_options: _options_pb2.PlanningOptions
    def __init__(
        self,
        lazy_frame_calls: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        execution_options: _Optional[_Union[_options_pb2.ExecutionOptions, _Mapping]] = ...,
        planning_options: _Optional[_Union[_options_pb2.PlanningOptions, _Mapping]] = ...,
    ) -> None: ...

class ExecutePlanResponse(_message.Message):
    __slots__ = ("feather", "errors", "execution_metadata", "environment_metadata", "meta")
    FEATHER_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_METADATA_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    feather: bytes
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    execution_metadata: _metadata_pb2.ExecutionMetadata
    environment_metadata: _metadata_pb2.EnvironmentMetadata
    meta: ExecutePlanRequest
    def __init__(
        self,
        feather: _Optional[bytes] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
        execution_metadata: _Optional[_Union[_metadata_pb2.ExecutionMetadata, _Mapping]] = ...,
        environment_metadata: _Optional[_Union[_metadata_pb2.EnvironmentMetadata, _Mapping]] = ...,
        meta: _Optional[_Union[ExecutePlanRequest, _Mapping]] = ...,
    ) -> None: ...
