from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.common.v1 import online_query_pb2 as _online_query_pb2
from chalk._gen.chalk.planner.v1 import logical_plan_pb2 as _logical_plan_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class PlanRequest(_message.Message):
    __slots__ = ("inputs", "outputs", "staleness", "context", "response_options")
    class StalenessEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    STALENESS_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.RepeatedScalarFieldContainer[str]
    outputs: _containers.RepeatedCompositeFieldContainer[_online_query_pb2.OutputExpr]
    staleness: _containers.ScalarMap[str, str]
    context: _online_query_pb2.OnlineQueryContext
    response_options: PlanResponseOptions
    def __init__(
        self,
        inputs: _Optional[_Iterable[str]] = ...,
        outputs: _Optional[_Iterable[_Union[_online_query_pb2.OutputExpr, _Mapping]]] = ...,
        staleness: _Optional[_Mapping[str, str]] = ...,
        context: _Optional[_Union[_online_query_pb2.OnlineQueryContext, _Mapping]] = ...,
        response_options: _Optional[_Union[PlanResponseOptions, _Mapping]] = ...,
    ) -> None: ...

class PlanResponseOptions(_message.Message):
    __slots__ = ("metadata", "num_input_rows", "planner_options")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class PlannerOptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    METADATA_FIELD_NUMBER: _ClassVar[int]
    NUM_INPUT_ROWS_FIELD_NUMBER: _ClassVar[int]
    PLANNER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.ScalarMap[str, str]
    num_input_rows: int
    planner_options: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        metadata: _Optional[_Mapping[str, str]] = ...,
        num_input_rows: _Optional[int] = ...,
        planner_options: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...

class PlanResponse(_message.Message):
    __slots__ = ("logical_plan", "errors")
    LOGICAL_PLAN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    logical_plan: _logical_plan_pb2.LogicalPlan
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        logical_plan: _Optional[_Union[_logical_plan_pb2.LogicalPlan, _Mapping]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...
