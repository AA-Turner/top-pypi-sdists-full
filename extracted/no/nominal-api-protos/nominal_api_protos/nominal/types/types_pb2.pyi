from buf.validate import validate_pb2 as _validate_pb2
from nominal.conjure.v1 import compat_pb2 as _compat_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ArchivedStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ARCHIVED_STATUS_UNSPECIFIED: _ClassVar[ArchivedStatus]
    NOT_ARCHIVED: _ClassVar[ArchivedStatus]
    ARCHIVED: _ClassVar[ArchivedStatus]

class DataSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_SOURCE_TYPE_UNSPECIFIED: _ClassVar[DataSourceType]
    DATASET: _ClassVar[DataSourceType]
    CONNECTION: _ClassVar[DataSourceType]
    VIDEO: _ClassVar[DataSourceType]

class Granularity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GRANULARITY_UNSPECIFIED: _ClassVar[Granularity]
    PICOSECONDS: _ClassVar[Granularity]
    NANOSECONDS: _ClassVar[Granularity]

class IngestStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INGEST_STATUS_UNSPECIFIED: _ClassVar[IngestStatus]
    SUCCEEDED: _ClassVar[IngestStatus]
    FAILED: _ClassVar[IngestStatus]
    IN_PROGRESS: _ClassVar[IngestStatus]
    DELETION_IN_PROGRESS: _ClassVar[IngestStatus]
    DELETED: _ClassVar[IngestStatus]

class NominalDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOMINAL_DATA_TYPE_UNSPECIFIED: _ClassVar[NominalDataType]
    DOUBLE: _ClassVar[NominalDataType]
    STRING: _ClassVar[NominalDataType]
    LOG: _ClassVar[NominalDataType]
    INT64: _ClassVar[NominalDataType]
ARCHIVED_STATUS_UNSPECIFIED: ArchivedStatus
NOT_ARCHIVED: ArchivedStatus
ARCHIVED: ArchivedStatus
DATA_SOURCE_TYPE_UNSPECIFIED: DataSourceType
DATASET: DataSourceType
CONNECTION: DataSourceType
VIDEO: DataSourceType
GRANULARITY_UNSPECIFIED: Granularity
PICOSECONDS: Granularity
NANOSECONDS: Granularity
INGEST_STATUS_UNSPECIFIED: IngestStatus
SUCCEEDED: IngestStatus
FAILED: IngestStatus
IN_PROGRESS: IngestStatus
DELETION_IN_PROGRESS: IngestStatus
DELETED: IngestStatus
NOMINAL_DATA_TYPE_UNSPECIFIED: NominalDataType
DOUBLE: NominalDataType
STRING: NominalDataType
LOG: NominalDataType
INT64: NominalDataType

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ErrorResult(_message.Message):
    __slots__ = ("error_type", "message")
    ERROR_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    error_type: str
    message: str
    def __init__(self, error_type: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class Handle(_message.Message):
    __slots__ = ("s3",)
    S3_FIELD_NUMBER: _ClassVar[int]
    s3: str
    def __init__(self, s3: _Optional[str] = ...) -> None: ...

class InProgressResult(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IngestStatusV2(_message.Message):
    __slots__ = ("success", "error", "in_progress")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IN_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    success: SuccessResult
    error: ErrorResult
    in_progress: InProgressResult
    def __init__(self, success: _Optional[_Union[SuccessResult, _Mapping]] = ..., error: _Optional[_Union[ErrorResult, _Mapping]] = ..., in_progress: _Optional[_Union[InProgressResult, _Mapping]] = ...) -> None: ...

class McapChannelLocator(_message.Message):
    __slots__ = ("topic", "id")
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    topic: str
    id: int
    def __init__(self, topic: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...

class Property(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class LabelUpdateWrapper(_message.Message):
    __slots__ = ("labels",)
    LABELS_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, labels: _Optional[_Iterable[str]] = ...) -> None: ...

class PropertyUpdateWrapper(_message.Message):
    __slots__ = ("properties",)
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    properties: _containers.ScalarMap[str, str]
    def __init__(self, properties: _Optional[_Mapping[str, str]] = ...) -> None: ...

class RefNameAndType(_message.Message):
    __slots__ = ("name", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: DataSourceType
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[DataSourceType, str]] = ...) -> None: ...

class SerializableError(_message.Message):
    __slots__ = ("name", "message", "error_instance_id", "status_code", "params")
    class ParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    name: str
    message: str
    error_instance_id: str
    status_code: int
    params: _containers.ScalarMap[str, str]
    def __init__(self, name: _Optional[str] = ..., message: _Optional[str] = ..., error_instance_id: _Optional[str] = ..., status_code: _Optional[int] = ..., params: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SuccessResult(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
