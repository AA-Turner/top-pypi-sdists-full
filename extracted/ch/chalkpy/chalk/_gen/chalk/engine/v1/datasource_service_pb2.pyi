from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class DatasourceTestCoverage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASOURCE_TEST_COVERAGE_UNSPECIFIED: _ClassVar[DatasourceTestCoverage]
    DATASOURCE_TEST_COVERAGE_FAST: _ClassVar[DatasourceTestCoverage]
    DATASOURCE_TEST_COVERAGE_FULL: _ClassVar[DatasourceTestCoverage]

class DatasourceTestStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASOURCE_TEST_STATUS_UNSPECIFIED: _ClassVar[DatasourceTestStatus]
    DATASOURCE_TEST_STATUS_PASS: _ClassVar[DatasourceTestStatus]
    DATASOURCE_TEST_STATUS_FAIL: _ClassVar[DatasourceTestStatus]
    DATASOURCE_TEST_STATUS_PASS_WITH_WARNINGS: _ClassVar[DatasourceTestStatus]

class DatasourceTestFindingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASOURCE_TEST_FINDING_STATUS_UNSPECIFIED: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_SKIPPED: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_PASS: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_WARNING_LOW_SEVERITY: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_WARNING_MEDIUM_SEVERITY: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_WARNING_HIGH_SEVERITY: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_ERROR: _ClassVar[DatasourceTestFindingStatus]

DATASOURCE_TEST_COVERAGE_UNSPECIFIED: DatasourceTestCoverage
DATASOURCE_TEST_COVERAGE_FAST: DatasourceTestCoverage
DATASOURCE_TEST_COVERAGE_FULL: DatasourceTestCoverage
DATASOURCE_TEST_STATUS_UNSPECIFIED: DatasourceTestStatus
DATASOURCE_TEST_STATUS_PASS: DatasourceTestStatus
DATASOURCE_TEST_STATUS_FAIL: DatasourceTestStatus
DATASOURCE_TEST_STATUS_PASS_WITH_WARNINGS: DatasourceTestStatus
DATASOURCE_TEST_FINDING_STATUS_UNSPECIFIED: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_SKIPPED: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_PASS: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_WARNING_LOW_SEVERITY: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_WARNING_MEDIUM_SEVERITY: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_WARNING_HIGH_SEVERITY: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_ERROR: DatasourceTestFindingStatus

class DatasourceTestFinding(_message.Message):
    __slots__ = ("status", "group", "title", "message", "config_keys")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_KEYS_FIELD_NUMBER: _ClassVar[int]
    status: DatasourceTestFindingStatus
    group: str
    title: str
    message: str
    config_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        status: _Optional[_Union[DatasourceTestFindingStatus, str]] = ...,
        group: _Optional[str] = ...,
        title: _Optional[str] = ...,
        message: _Optional[str] = ...,
        config_keys: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class PreviewedStreamMessage(_message.Message):
    __slots__ = ("value_base64", "key_base64", "topic", "partition", "offset", "timestamp_ms")
    VALUE_BASE64_FIELD_NUMBER: _ClassVar[int]
    KEY_BASE64_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_MS_FIELD_NUMBER: _ClassVar[int]
    value_base64: str
    key_base64: str
    topic: str
    partition: str
    offset: str
    timestamp_ms: int
    def __init__(
        self,
        value_base64: _Optional[str] = ...,
        key_base64: _Optional[str] = ...,
        topic: _Optional[str] = ...,
        partition: _Optional[str] = ...,
        offset: _Optional[str] = ...,
        timestamp_ms: _Optional[int] = ...,
    ) -> None: ...

class TestDatasourceRequest(_message.Message):
    __slots__ = ("kind", "parameters", "include_preview", "coverage")
    KIND_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_FIELD_NUMBER: _ClassVar[int]
    kind: str
    parameters: _struct_pb2.Struct
    include_preview: bool
    coverage: DatasourceTestCoverage
    def __init__(
        self,
        kind: _Optional[str] = ...,
        parameters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        include_preview: bool = ...,
        coverage: _Optional[_Union[DatasourceTestCoverage, str]] = ...,
    ) -> None: ...

class TestDatasourceResponse(_message.Message):
    __slots__ = ("status", "findings", "summary", "latency_seconds", "preview_messages", "coverage_ran")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FINDINGS_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    LATENCY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_RAN_FIELD_NUMBER: _ClassVar[int]
    status: DatasourceTestStatus
    findings: _containers.RepeatedCompositeFieldContainer[DatasourceTestFinding]
    summary: str
    latency_seconds: float
    preview_messages: _containers.RepeatedCompositeFieldContainer[PreviewedStreamMessage]
    coverage_ran: DatasourceTestCoverage
    def __init__(
        self,
        status: _Optional[_Union[DatasourceTestStatus, str]] = ...,
        findings: _Optional[_Iterable[_Union[DatasourceTestFinding, _Mapping]]] = ...,
        summary: _Optional[str] = ...,
        latency_seconds: _Optional[float] = ...,
        preview_messages: _Optional[_Iterable[_Union[PreviewedStreamMessage, _Mapping]]] = ...,
        coverage_ran: _Optional[_Union[DatasourceTestCoverage, str]] = ...,
    ) -> None: ...
