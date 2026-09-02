from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_TYPE_UNSPECIFIED: _ClassVar[DataType]
    DATA_TYPE_BFLOAT16: _ClassVar[DataType]
    DATA_TYPE_FLOAT16: _ClassVar[DataType]
    DATA_TYPE_FLOAT32: _ClassVar[DataType]
    DATA_TYPE_FLOAT64: _ClassVar[DataType]
    DATA_TYPE_INT8: _ClassVar[DataType]
    DATA_TYPE_INT32: _ClassVar[DataType]
    DATA_TYPE_INT64: _ClassVar[DataType]
    DATA_TYPE_UINT8: _ClassVar[DataType]
    DATA_TYPE_UINT32: _ClassVar[DataType]
    DATA_TYPE_UINT64: _ClassVar[DataType]
    DATA_TYPE_BOOL: _ClassVar[DataType]

class CompressionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMPRESSION_TYPE_NONE: _ClassVar[CompressionType]
    COMPRESSION_TYPE_ZSTD: _ClassVar[CompressionType]
DATA_TYPE_UNSPECIFIED: DataType
DATA_TYPE_BFLOAT16: DataType
DATA_TYPE_FLOAT16: DataType
DATA_TYPE_FLOAT32: DataType
DATA_TYPE_FLOAT64: DataType
DATA_TYPE_INT8: DataType
DATA_TYPE_INT32: DataType
DATA_TYPE_INT64: DataType
DATA_TYPE_UINT8: DataType
DATA_TYPE_UINT32: DataType
DATA_TYPE_UINT64: DataType
DATA_TYPE_BOOL: DataType
COMPRESSION_TYPE_NONE: CompressionType
COMPRESSION_TYPE_ZSTD: CompressionType

class Tensor(_message.Message):
    __slots__ = ("shape", "data_type", "array", "chunk_count")
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARRAY_FIELD_NUMBER: _ClassVar[int]
    CHUNK_COUNT_FIELD_NUMBER: _ClassVar[int]
    shape: _containers.RepeatedScalarFieldContainer[int]
    data_type: DataType
    array: TensorChunk
    chunk_count: int
    def __init__(self, shape: _Optional[_Iterable[int]] = ..., data_type: _Optional[_Union[DataType, str]] = ..., array: _Optional[_Union[TensorChunk, _Mapping]] = ..., chunk_count: _Optional[int] = ...) -> None: ...

class TensorChunk(_message.Message):
    __slots__ = ("data", "compression_type")
    DATA_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    compression_type: CompressionType
    def __init__(self, data: _Optional[bytes] = ..., compression_type: _Optional[_Union[CompressionType, str]] = ...) -> None: ...
