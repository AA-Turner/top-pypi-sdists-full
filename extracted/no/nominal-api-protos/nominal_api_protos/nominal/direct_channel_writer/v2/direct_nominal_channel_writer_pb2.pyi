from google.api import annotations_pb2 as _annotations_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from nominal.types.time import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NominalDirectChannelWriterError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_DATA_SOURCE_NOT_FOUND: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_DATA_SOURCES_NOT_FOUND: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_INVALID_NOMINAL_DATA_SOURCE: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_NOMINAL_DATA_SOURCE_CONFLICT: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_ARRAY_TOO_LARGE: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_CONFLICTING_DATA_TYPES: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_INVALID_DATA_SOURCE: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_INVALID_TELEGRAF_TIMESTAMP: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_INVALID_TIMESTAMP: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_MISMATCHED_TIMESTAMPS_AND_VALUES: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_STREAMING_DISABLED_ON_DATASET: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_INVALID_RANGE: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_POINTS_TYPE_NOT_SET: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_ARRAY_POINTS_TYPE_NOT_SET: _ClassVar[NominalDirectChannelWriterError]
    NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_NOT_AUTHORIZED: _ClassVar[NominalDirectChannelWriterError]
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_DATA_SOURCE_NOT_FOUND: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_DATA_SOURCES_NOT_FOUND: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_INVALID_NOMINAL_DATA_SOURCE: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_NOMINAL_DATA_SOURCE_CONFLICT: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_ARRAY_TOO_LARGE: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_CONFLICTING_DATA_TYPES: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_INVALID_DATA_SOURCE: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_INVALID_TELEGRAF_TIMESTAMP: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_INVALID_TIMESTAMP: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_MISMATCHED_TIMESTAMPS_AND_VALUES: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_STREAMING_DISABLED_ON_DATASET: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_INVALID_RANGE: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_POINTS_TYPE_NOT_SET: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_ARRAY_POINTS_TYPE_NOT_SET: NominalDirectChannelWriterError
NOMINAL_DIRECT_CHANNEL_WRITER_ERROR_NOT_AUTHORIZED: NominalDirectChannelWriterError

class WriteBatchesRequest(_message.Message):
    __slots__ = ("batches", "data_source_rid")
    BATCHES_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    batches: _containers.RepeatedCompositeFieldContainer[RecordsBatch]
    data_source_rid: str
    def __init__(self, batches: _Optional[_Iterable[_Union[RecordsBatch, _Mapping]]] = ..., data_source_rid: _Optional[str] = ...) -> None: ...

class ArrayPoints(_message.Message):
    __slots__ = ("double_array_points", "string_array_points")
    DOUBLE_ARRAY_POINTS_FIELD_NUMBER: _ClassVar[int]
    STRING_ARRAY_POINTS_FIELD_NUMBER: _ClassVar[int]
    double_array_points: DoubleArrayPoints
    string_array_points: StringArrayPoints
    def __init__(self, double_array_points: _Optional[_Union[DoubleArrayPoints, _Mapping]] = ..., string_array_points: _Optional[_Union[StringArrayPoints, _Mapping]] = ...) -> None: ...

class StringArrayPoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[StringArrayPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[StringArrayPoint, _Mapping]]] = ...) -> None: ...

class StringArrayPoint(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, value: _Optional[_Iterable[str]] = ...) -> None: ...

class DoubleArrayPoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[DoubleArrayPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[DoubleArrayPoint, _Mapping]]] = ...) -> None: ...

class DoubleArrayPoint(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, value: _Optional[_Iterable[float]] = ...) -> None: ...

class LogPoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[LogPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[LogPoint, _Mapping]]] = ...) -> None: ...

class LogPoint(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: LogValue
    def __init__(self, value: _Optional[_Union[LogValue, _Mapping]] = ...) -> None: ...

class StructPoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, points: _Optional[_Iterable[str]] = ...) -> None: ...

class LogValue(_message.Message):
    __slots__ = ("message", "args")
    class ArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    message: str
    args: _containers.ScalarMap[str, str]
    def __init__(self, message: _Optional[str] = ..., args: _Optional[_Mapping[str, str]] = ...) -> None: ...

class StringPoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, points: _Optional[_Iterable[str]] = ...) -> None: ...

class DoublePoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, points: _Optional[_Iterable[float]] = ...) -> None: ...

class IntPoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, points: _Optional[_Iterable[int]] = ...) -> None: ...

class Uint64Points(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, points: _Optional[_Iterable[int]] = ...) -> None: ...

class Points(_message.Message):
    __slots__ = ("timestamps", "double_points", "string_points", "log_points", "int_points", "array_points", "struct_points", "uint64_points")
    TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_POINTS_FIELD_NUMBER: _ClassVar[int]
    STRING_POINTS_FIELD_NUMBER: _ClassVar[int]
    LOG_POINTS_FIELD_NUMBER: _ClassVar[int]
    INT_POINTS_FIELD_NUMBER: _ClassVar[int]
    ARRAY_POINTS_FIELD_NUMBER: _ClassVar[int]
    STRUCT_POINTS_FIELD_NUMBER: _ClassVar[int]
    UINT64_POINTS_FIELD_NUMBER: _ClassVar[int]
    timestamps: _containers.RepeatedCompositeFieldContainer[_time_pb2.Timestamp]
    double_points: DoublePoints
    string_points: StringPoints
    log_points: LogPoints
    int_points: IntPoints
    array_points: ArrayPoints
    struct_points: StructPoints
    uint64_points: Uint64Points
    def __init__(self, timestamps: _Optional[_Iterable[_Union[_time_pb2.Timestamp, _Mapping]]] = ..., double_points: _Optional[_Union[DoublePoints, _Mapping]] = ..., string_points: _Optional[_Union[StringPoints, _Mapping]] = ..., log_points: _Optional[_Union[LogPoints, _Mapping]] = ..., int_points: _Optional[_Union[IntPoints, _Mapping]] = ..., array_points: _Optional[_Union[ArrayPoints, _Mapping]] = ..., struct_points: _Optional[_Union[StructPoints, _Mapping]] = ..., uint64_points: _Optional[_Union[Uint64Points, _Mapping]] = ...) -> None: ...

class RecordsBatch(_message.Message):
    __slots__ = ("channel", "tags", "points")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    channel: str
    tags: _containers.ScalarMap[str, str]
    points: Points
    def __init__(self, channel: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ..., points: _Optional[_Union[Points, _Mapping]] = ...) -> None: ...

class ChannelSeriesMetadata(_message.Message):
    __slots__ = ("series_id", "tags")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SERIES_ID_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    series_id: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, series_id: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ChannelSeriesMetadataBatch(_message.Message):
    __slots__ = ("series_metadata",)
    SERIES_METADATA_FIELD_NUMBER: _ClassVar[int]
    series_metadata: _containers.RepeatedCompositeFieldContainer[ChannelSeriesMetadata]
    def __init__(self, series_metadata: _Optional[_Iterable[_Union[ChannelSeriesMetadata, _Mapping]]] = ...) -> None: ...

class WriteBatchesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
