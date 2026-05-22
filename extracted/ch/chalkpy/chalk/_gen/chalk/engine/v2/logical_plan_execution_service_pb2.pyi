from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.common.v2 import metadata_pb2 as _metadata_pb2
from chalk._gen.chalk.common.v2 import options_pb2 as _options_pb2
from chalk._gen.chalk.common.v2 import table_pb2 as _table_pb2
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

class LogicalPlanExecutionServiceDummy(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ExecutePlanRequest(_message.Message):
    __slots__ = ("logical_plan_proto_bytes", "tables", "skip_planning_time_validation", "execution_options")
    class TablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _table_pb2.Table
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_table_pb2.Table, _Mapping]] = ...
        ) -> None: ...

    LOGICAL_PLAN_PROTO_BYTES_FIELD_NUMBER: _ClassVar[int]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    SKIP_PLANNING_TIME_VALIDATION_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    logical_plan_proto_bytes: bytes
    tables: _containers.MessageMap[str, _table_pb2.Table]
    skip_planning_time_validation: bool
    execution_options: _options_pb2.ExecutionOptions
    def __init__(
        self,
        logical_plan_proto_bytes: _Optional[bytes] = ...,
        tables: _Optional[_Mapping[str, _table_pb2.Table]] = ...,
        skip_planning_time_validation: bool = ...,
        execution_options: _Optional[_Union[_options_pb2.ExecutionOptions, _Mapping]] = ...,
    ) -> None: ...

class ExecutePlanResponse(_message.Message):
    __slots__ = ("feather", "errors", "execution_metadata", "environment_metadata")
    FEATHER_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_METADATA_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    feather: bytes
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    execution_metadata: _metadata_pb2.ExecutionMetadata
    environment_metadata: _metadata_pb2.EnvironmentMetadata
    def __init__(
        self,
        feather: _Optional[bytes] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
        execution_metadata: _Optional[_Union[_metadata_pb2.ExecutionMetadata, _Mapping]] = ...,
        environment_metadata: _Optional[_Union[_metadata_pb2.EnvironmentMetadata, _Mapping]] = ...,
    ) -> None: ...
