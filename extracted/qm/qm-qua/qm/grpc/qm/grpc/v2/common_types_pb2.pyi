from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JobExecutionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNSET: _ClassVar[JobExecutionStatus]
    UNKNOWN: _ClassVar[JobExecutionStatus]
    PENDING: _ClassVar[JobExecutionStatus]
    RUNNING: _ClassVar[JobExecutionStatus]
    COMPLETED: _ClassVar[JobExecutionStatus]
    CANCELED: _ClassVar[JobExecutionStatus]
    LOADING: _ClassVar[JobExecutionStatus]
    ERROR: _ClassVar[JobExecutionStatus]
    PROCESSING: _ClassVar[JobExecutionStatus]
UNSET: JobExecutionStatus
UNKNOWN: JobExecutionStatus
PENDING: JobExecutionStatus
RUNNING: JobExecutionStatus
COMPLETED: JobExecutionStatus
CANCELED: JobExecutionStatus
LOADING: JobExecutionStatus
ERROR: JobExecutionStatus
PROCESSING: JobExecutionStatus

class Range(_message.Message):
    __slots__ = ["to"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    to: _wrappers_pb2.Int64Value
    def __init__(self, to: _Optional[_Union[_wrappers_pb2.Int64Value, _Mapping]] = ..., **kwargs) -> None: ...
