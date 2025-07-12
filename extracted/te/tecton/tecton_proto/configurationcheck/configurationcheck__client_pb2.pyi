from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CHECK_ID_TESTONLY_CONFIGURATION_VALIDATION: CheckId
CHECK_ID_TESTONLY_DATABASE_CONNECTIVITY: CheckId
CHECK_ID_TEST_VALUE: CheckId
CHECK_ID_UNSPECIFIED: CheckId
DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
DESCRIPTOR: _descriptor.FileDescriptor
RESULT_STATUS_FAILED: ResultStatus
RESULT_STATUS_PASSED: ResultStatus
RESULT_STATUS_UNSPECIFIED: ResultStatus
SHORT_NAME_FIELD_NUMBER: _ClassVar[int]
description: _descriptor.FieldDescriptor
short_name: _descriptor.FieldDescriptor

class CheckResult(_message.Message):
    __slots__ = ["description", "error_message", "short_name", "start_time", "status"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    description: str
    error_message: str
    short_name: str
    start_time: _timestamp_pb2.Timestamp
    status: ResultStatus
    def __init__(self, short_name: _Optional[str] = ..., description: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[ResultStatus, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class CheckRun(_message.Message):
    __slots__ = ["check_results", "completed_time"]
    CHECK_RESULTS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_TIME_FIELD_NUMBER: _ClassVar[int]
    check_results: _containers.RepeatedCompositeFieldContainer[CheckResult]
    completed_time: _timestamp_pb2.Timestamp
    def __init__(self, completed_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., check_results: _Optional[_Iterable[_Union[CheckResult, _Mapping]]] = ...) -> None: ...

class CheckId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ResultStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
