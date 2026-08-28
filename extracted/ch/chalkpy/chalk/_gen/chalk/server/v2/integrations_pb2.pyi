from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import integrations_pb2 as _integrations_pb2
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

class IntegrationTestCoverageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTEGRATION_TEST_COVERAGE_TYPE_UNSPECIFIED: _ClassVar[IntegrationTestCoverageType]
    INTEGRATION_TEST_COVERAGE_TYPE_FAST: _ClassVar[IntegrationTestCoverageType]
    INTEGRATION_TEST_COVERAGE_TYPE_FULL: _ClassVar[IntegrationTestCoverageType]

class IntegrationTestStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTEGRATION_TEST_STATUS_UNSPECIFIED: _ClassVar[IntegrationTestStatus]
    INTEGRATION_TEST_STATUS_PASS: _ClassVar[IntegrationTestStatus]
    INTEGRATION_TEST_STATUS_FAIL: _ClassVar[IntegrationTestStatus]
    INTEGRATION_TEST_STATUS_PASS_WITH_WARNINGS: _ClassVar[IntegrationTestStatus]

class IntegrationTestFindingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTEGRATION_TEST_FINDING_STATUS_UNSPECIFIED: _ClassVar[IntegrationTestFindingStatus]
    INTEGRATION_TEST_FINDING_STATUS_SKIPPED: _ClassVar[IntegrationTestFindingStatus]
    INTEGRATION_TEST_FINDING_STATUS_PASS: _ClassVar[IntegrationTestFindingStatus]
    INTEGRATION_TEST_FINDING_STATUS_WARNING_LOW_SEVERITY: _ClassVar[IntegrationTestFindingStatus]
    INTEGRATION_TEST_FINDING_STATUS_WARNING_MEDIUM_SEVERITY: _ClassVar[IntegrationTestFindingStatus]
    INTEGRATION_TEST_FINDING_STATUS_WARNING_HIGH_SEVERITY: _ClassVar[IntegrationTestFindingStatus]
    INTEGRATION_TEST_FINDING_STATUS_ERROR: _ClassVar[IntegrationTestFindingStatus]

INTEGRATION_TEST_COVERAGE_TYPE_UNSPECIFIED: IntegrationTestCoverageType
INTEGRATION_TEST_COVERAGE_TYPE_FAST: IntegrationTestCoverageType
INTEGRATION_TEST_COVERAGE_TYPE_FULL: IntegrationTestCoverageType
INTEGRATION_TEST_STATUS_UNSPECIFIED: IntegrationTestStatus
INTEGRATION_TEST_STATUS_PASS: IntegrationTestStatus
INTEGRATION_TEST_STATUS_FAIL: IntegrationTestStatus
INTEGRATION_TEST_STATUS_PASS_WITH_WARNINGS: IntegrationTestStatus
INTEGRATION_TEST_FINDING_STATUS_UNSPECIFIED: IntegrationTestFindingStatus
INTEGRATION_TEST_FINDING_STATUS_SKIPPED: IntegrationTestFindingStatus
INTEGRATION_TEST_FINDING_STATUS_PASS: IntegrationTestFindingStatus
INTEGRATION_TEST_FINDING_STATUS_WARNING_LOW_SEVERITY: IntegrationTestFindingStatus
INTEGRATION_TEST_FINDING_STATUS_WARNING_MEDIUM_SEVERITY: IntegrationTestFindingStatus
INTEGRATION_TEST_FINDING_STATUS_WARNING_HIGH_SEVERITY: IntegrationTestFindingStatus
INTEGRATION_TEST_FINDING_STATUS_ERROR: IntegrationTestFindingStatus

class IntegrationTestFinding(_message.Message):
    __slots__ = ("status", "group", "title", "message", "config_keys")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_KEYS_FIELD_NUMBER: _ClassVar[int]
    status: IntegrationTestFindingStatus
    group: str
    title: str
    message: str
    config_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        status: _Optional[_Union[IntegrationTestFindingStatus, str]] = ...,
        group: _Optional[str] = ...,
        title: _Optional[str] = ...,
        message: _Optional[str] = ...,
        config_keys: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class TestIntegrationRequest(_message.Message):
    __slots__ = ("kind", "config", "integration_id", "include_preview", "coverage_type")
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _integrations_pb2.IntegrationConfigValue
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[_integrations_pb2.IntegrationConfigValue, _Mapping]] = ...,
        ) -> None: ...

    KIND_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    kind: _integrations_pb2.IntegrationKind
    config: _containers.MessageMap[str, _integrations_pb2.IntegrationConfigValue]
    integration_id: str
    include_preview: bool
    coverage_type: IntegrationTestCoverageType
    def __init__(
        self,
        kind: _Optional[_Union[_integrations_pb2.IntegrationKind, str]] = ...,
        config: _Optional[_Mapping[str, _integrations_pb2.IntegrationConfigValue]] = ...,
        integration_id: _Optional[str] = ...,
        include_preview: bool = ...,
        coverage_type: _Optional[_Union[IntegrationTestCoverageType, str]] = ...,
    ) -> None: ...

class TestIntegrationResponse(_message.Message):
    __slots__ = ("kind", "status", "findings", "summary", "preview_messages", "coverage_ran")
    KIND_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FINDINGS_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_RAN_FIELD_NUMBER: _ClassVar[int]
    kind: _integrations_pb2.IntegrationKind
    status: IntegrationTestStatus
    findings: _containers.RepeatedCompositeFieldContainer[IntegrationTestFinding]
    summary: str
    preview_messages: _containers.RepeatedCompositeFieldContainer[_integrations_pb2.PreviewedMessage]
    coverage_ran: IntegrationTestCoverageType
    def __init__(
        self,
        kind: _Optional[_Union[_integrations_pb2.IntegrationKind, str]] = ...,
        status: _Optional[_Union[IntegrationTestStatus, str]] = ...,
        findings: _Optional[_Iterable[_Union[IntegrationTestFinding, _Mapping]]] = ...,
        summary: _Optional[str] = ...,
        preview_messages: _Optional[_Iterable[_Union[_integrations_pb2.PreviewedMessage, _Mapping]]] = ...,
        coverage_ran: _Optional[_Union[IntegrationTestCoverageType, str]] = ...,
    ) -> None: ...
