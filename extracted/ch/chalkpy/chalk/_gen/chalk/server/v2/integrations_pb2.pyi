from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.engine.v1 import datasource_service_pb2 as _datasource_service_pb2
from chalk._gen.chalk.server.v1 import integrations_pb2 as _integrations_pb2
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
    coverage_type: _datasource_service_pb2.DatasourceTestCoverage
    def __init__(
        self,
        kind: _Optional[_Union[_integrations_pb2.IntegrationKind, str]] = ...,
        config: _Optional[_Mapping[str, _integrations_pb2.IntegrationConfigValue]] = ...,
        integration_id: _Optional[str] = ...,
        include_preview: bool = ...,
        coverage_type: _Optional[_Union[_datasource_service_pb2.DatasourceTestCoverage, str]] = ...,
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
    status: _datasource_service_pb2.DatasourceTestStatus
    findings: _containers.RepeatedCompositeFieldContainer[_datasource_service_pb2.DatasourceTestFinding]
    summary: str
    preview_messages: _containers.RepeatedCompositeFieldContainer[_integrations_pb2.PreviewedMessage]
    coverage_ran: _datasource_service_pb2.DatasourceTestCoverage
    def __init__(
        self,
        kind: _Optional[_Union[_integrations_pb2.IntegrationKind, str]] = ...,
        status: _Optional[_Union[_datasource_service_pb2.DatasourceTestStatus, str]] = ...,
        findings: _Optional[_Iterable[_Union[_datasource_service_pb2.DatasourceTestFinding, _Mapping]]] = ...,
        summary: _Optional[str] = ...,
        preview_messages: _Optional[_Iterable[_Union[_integrations_pb2.PreviewedMessage, _Mapping]]] = ...,
        coverage_ran: _Optional[_Union[_datasource_service_pb2.DatasourceTestCoverage, str]] = ...,
    ) -> None: ...
