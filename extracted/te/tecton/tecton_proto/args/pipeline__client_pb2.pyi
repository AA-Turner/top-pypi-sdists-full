from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CONTEXT_TYPE_MATERIALIZATION: ContextType
CONTEXT_TYPE_REALTIME: ContextType
CONTEXT_TYPE_UNSPECIFIED: ContextType
DESCRIPTOR: _descriptor.FileDescriptor
TIME_REFERENCE_MATERIALIZATION_END_TIME: TimeReference
TIME_REFERENCE_MATERIALIZATION_START_TIME: TimeReference
TIME_REFERENCE_UNBOUNDED_FUTURE: TimeReference
TIME_REFERENCE_UNBOUNDED_PAST: TimeReference
TIME_REFERENCE_UNSPECIFIED: TimeReference

class ConstantNode(_message.Message):
    __slots__ = ["bool_const", "float_const", "int_const", "null_const", "string_const"]
    BOOL_CONST_FIELD_NUMBER: _ClassVar[int]
    FLOAT_CONST_FIELD_NUMBER: _ClassVar[int]
    INT_CONST_FIELD_NUMBER: _ClassVar[int]
    NULL_CONST_FIELD_NUMBER: _ClassVar[int]
    STRING_CONST_FIELD_NUMBER: _ClassVar[int]
    bool_const: bool
    float_const: str
    int_const: str
    null_const: _empty_pb2.Empty
    string_const: str
    def __init__(self, string_const: _Optional[str] = ..., int_const: _Optional[str] = ..., float_const: _Optional[str] = ..., bool_const: bool = ..., null_const: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...

class ContextNode(_message.Message):
    __slots__ = ["context_type", "input_name"]
    CONTEXT_TYPE_FIELD_NUMBER: _ClassVar[int]
    INPUT_NAME_FIELD_NUMBER: _ClassVar[int]
    context_type: ContextType
    input_name: str
    def __init__(self, context_type: _Optional[_Union[ContextType, str]] = ..., input_name: _Optional[str] = ...) -> None: ...

class DataSourceNode(_message.Message):
    __slots__ = ["filter_end_time", "filter_start_time", "input_name", "schedule_offset", "start_time_offset", "virtual_data_source_id", "window", "window_unbounded", "window_unbounded_preceding"]
    FILTER_END_TIME_FIELD_NUMBER: _ClassVar[int]
    FILTER_START_TIME_FIELD_NUMBER: _ClassVar[int]
    INPUT_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    START_TIME_OFFSET_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FIELD_NUMBER: _ClassVar[int]
    WINDOW_UNBOUNDED_FIELD_NUMBER: _ClassVar[int]
    WINDOW_UNBOUNDED_PRECEDING_FIELD_NUMBER: _ClassVar[int]
    filter_end_time: FilterDateTime
    filter_start_time: FilterDateTime
    input_name: str
    schedule_offset: _duration_pb2.Duration
    start_time_offset: _duration_pb2.Duration
    virtual_data_source_id: _id__client_pb2.Id
    window: _duration_pb2.Duration
    window_unbounded: bool
    window_unbounded_preceding: bool
    def __init__(self, virtual_data_source_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., window: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., window_unbounded_preceding: bool = ..., window_unbounded: bool = ..., start_time_offset: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., schedule_offset: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., input_name: _Optional[str] = ..., filter_start_time: _Optional[_Union[FilterDateTime, _Mapping]] = ..., filter_end_time: _Optional[_Union[FilterDateTime, _Mapping]] = ...) -> None: ...

class FeatureViewNode(_message.Message):
    __slots__ = ["feature_reference", "feature_view_id", "input_name"]
    FEATURE_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_reference: _feature_service__client_pb2.FeatureReference
    feature_view_id: _id__client_pb2.Id
    input_name: str
    def __init__(self, feature_view_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., feature_reference: _Optional[_Union[_feature_service__client_pb2.FeatureReference, _Mapping]] = ..., input_name: _Optional[str] = ...) -> None: ...

class FilterDateTime(_message.Message):
    __slots__ = ["relative_time", "timestamp"]
    RELATIVE_TIME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    relative_time: RelativeTime
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., relative_time: _Optional[_Union[RelativeTime, _Mapping]] = ...) -> None: ...

class Input(_message.Message):
    __slots__ = ["arg_index", "arg_name", "node"]
    ARG_INDEX_FIELD_NUMBER: _ClassVar[int]
    ARG_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    arg_index: int
    arg_name: str
    node: PipelineNode
    def __init__(self, arg_index: _Optional[int] = ..., arg_name: _Optional[str] = ..., node: _Optional[_Union[PipelineNode, _Mapping]] = ...) -> None: ...

class JoinInputsNode(_message.Message):
    __slots__ = ["nodes"]
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[PipelineNode]
    def __init__(self, nodes: _Optional[_Iterable[_Union[PipelineNode, _Mapping]]] = ...) -> None: ...

class MaterializationContextNode(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Pipeline(_message.Message):
    __slots__ = ["root"]
    ROOT_FIELD_NUMBER: _ClassVar[int]
    root: PipelineNode
    def __init__(self, root: _Optional[_Union[PipelineNode, _Mapping]] = ...) -> None: ...

class PipelineNode(_message.Message):
    __slots__ = ["constant_node", "context_node", "data_source_node", "feature_view_node", "join_inputs_node", "materialization_context_node", "request_data_source_node", "transformation_node"]
    CONSTANT_NODE_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_NODE_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_NODE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NODE_FIELD_NUMBER: _ClassVar[int]
    JOIN_INPUTS_NODE_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_CONTEXT_NODE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_DATA_SOURCE_NODE_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_NODE_FIELD_NUMBER: _ClassVar[int]
    constant_node: ConstantNode
    context_node: ContextNode
    data_source_node: DataSourceNode
    feature_view_node: FeatureViewNode
    join_inputs_node: JoinInputsNode
    materialization_context_node: MaterializationContextNode
    request_data_source_node: RequestDataSourceNode
    transformation_node: TransformationNode
    def __init__(self, transformation_node: _Optional[_Union[TransformationNode, _Mapping]] = ..., data_source_node: _Optional[_Union[DataSourceNode, _Mapping]] = ..., constant_node: _Optional[_Union[ConstantNode, _Mapping]] = ..., request_data_source_node: _Optional[_Union[RequestDataSourceNode, _Mapping]] = ..., feature_view_node: _Optional[_Union[FeatureViewNode, _Mapping]] = ..., materialization_context_node: _Optional[_Union[MaterializationContextNode, _Mapping]] = ..., context_node: _Optional[_Union[ContextNode, _Mapping]] = ..., join_inputs_node: _Optional[_Union[JoinInputsNode, _Mapping]] = ...) -> None: ...

class RelativeTime(_message.Message):
    __slots__ = ["offset", "time_reference"]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    TIME_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    offset: _duration_pb2.Duration
    time_reference: TimeReference
    def __init__(self, time_reference: _Optional[_Union[TimeReference, str]] = ..., offset: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class RequestContext(_message.Message):
    __slots__ = ["schema", "tecton_schema"]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TECTON_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    schema: _spark_schema__client_pb2.SparkSchema
    tecton_schema: _schema__client_pb2.Schema
    def __init__(self, tecton_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., schema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ...) -> None: ...

class RequestDataSourceNode(_message.Message):
    __slots__ = ["input_name", "request_context"]
    INPUT_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    input_name: str
    request_context: RequestContext
    def __init__(self, request_context: _Optional[_Union[RequestContext, _Mapping]] = ..., input_name: _Optional[str] = ...) -> None: ...

class TransformationNode(_message.Message):
    __slots__ = ["inputs", "transformation_id"]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_ID_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.RepeatedCompositeFieldContainer[Input]
    transformation_id: _id__client_pb2.Id
    def __init__(self, transformation_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., inputs: _Optional[_Iterable[_Union[Input, _Mapping]]] = ...) -> None: ...

class TimeReference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ContextType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
