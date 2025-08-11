from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
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

class PagerDutySeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAGER_DUTY_SEVERITY_UNSPECIFIED: _ClassVar[PagerDutySeverity]
    PAGER_DUTY_SEVERITY_INFO: _ClassVar[PagerDutySeverity]
    PAGER_DUTY_SEVERITY_WARNING: _ClassVar[PagerDutySeverity]
    PAGER_DUTY_SEVERITY_ERROR: _ClassVar[PagerDutySeverity]
    PAGER_DUTY_SEVERITY_CRITICAL: _ClassVar[PagerDutySeverity]

class PagerDutyEventAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAGER_DUTY_EVENT_ACTION_UNSPECIFIED: _ClassVar[PagerDutyEventAction]
    PAGER_DUTY_EVENT_ACTION_TRIGGER: _ClassVar[PagerDutyEventAction]
    PAGER_DUTY_EVENT_ACTION_ACKNOWLEDGE: _ClassVar[PagerDutyEventAction]
    PAGER_DUTY_EVENT_ACTION_RESOLVE: _ClassVar[PagerDutyEventAction]

PAGER_DUTY_SEVERITY_UNSPECIFIED: PagerDutySeverity
PAGER_DUTY_SEVERITY_INFO: PagerDutySeverity
PAGER_DUTY_SEVERITY_WARNING: PagerDutySeverity
PAGER_DUTY_SEVERITY_ERROR: PagerDutySeverity
PAGER_DUTY_SEVERITY_CRITICAL: PagerDutySeverity
PAGER_DUTY_EVENT_ACTION_UNSPECIFIED: PagerDutyEventAction
PAGER_DUTY_EVENT_ACTION_TRIGGER: PagerDutyEventAction
PAGER_DUTY_EVENT_ACTION_ACKNOWLEDGE: PagerDutyEventAction
PAGER_DUTY_EVENT_ACTION_RESOLVE: PagerDutyEventAction

class PagerDutyEventV2Payload(_message.Message):
    __slots__ = ("summary", "timestamp", "severity", "source", "component", "group")
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    CLASS_FIELD_NUMBER: _ClassVar[int]
    summary: str
    timestamp: _timestamp_pb2.Timestamp
    severity: PagerDutySeverity
    source: str
    component: str
    group: str
    def __init__(
        self,
        summary: _Optional[str] = ...,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        severity: _Optional[_Union[PagerDutySeverity, str]] = ...,
        source: _Optional[str] = ...,
        component: _Optional[str] = ...,
        group: _Optional[str] = ...,
        **kwargs,
    ) -> None: ...

class PagerDutyEventV2Link(_message.Message):
    __slots__ = ("href", "text")
    HREF_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    href: str
    text: str
    def __init__(self, href: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class PagerDutyEventV2Image(_message.Message):
    __slots__ = ("src", "href", "alt")
    SRC_FIELD_NUMBER: _ClassVar[int]
    HREF_FIELD_NUMBER: _ClassVar[int]
    ALT_FIELD_NUMBER: _ClassVar[int]
    src: str
    href: str
    alt: str
    def __init__(self, src: _Optional[str] = ..., href: _Optional[str] = ..., alt: _Optional[str] = ...) -> None: ...

class PagerDutyEventV2(_message.Message):
    __slots__ = ("payload", "routing_key", "event_action", "dedup_key", "client", "client_url", "links", "images")
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ROUTING_KEY_FIELD_NUMBER: _ClassVar[int]
    EVENT_ACTION_FIELD_NUMBER: _ClassVar[int]
    DEDUP_KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_URL_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    payload: PagerDutyEventV2Payload
    routing_key: str
    event_action: PagerDutyEventAction
    dedup_key: str
    client: str
    client_url: str
    links: _containers.RepeatedCompositeFieldContainer[PagerDutyEventV2Link]
    images: _containers.RepeatedCompositeFieldContainer[PagerDutyEventV2Image]
    def __init__(
        self,
        payload: _Optional[_Union[PagerDutyEventV2Payload, _Mapping]] = ...,
        routing_key: _Optional[str] = ...,
        event_action: _Optional[_Union[PagerDutyEventAction, str]] = ...,
        dedup_key: _Optional[str] = ...,
        client: _Optional[str] = ...,
        client_url: _Optional[str] = ...,
        links: _Optional[_Iterable[_Union[PagerDutyEventV2Link, _Mapping]]] = ...,
        images: _Optional[_Iterable[_Union[PagerDutyEventV2Image, _Mapping]]] = ...,
    ) -> None: ...

class PagerDutyIntegration(_message.Message):
    __slots__ = ("id", "name", "default", "token", "environment_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    default: bool
    token: str
    environment_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        default: bool = ...,
        token: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
    ) -> None: ...

class IncidentIoIntegration(_message.Message):
    __slots__ = ("id", "token", "environment_id", "name", "source_id", "source_token", "severity_id", "severity_token")
    ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_ID_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_TOKEN_FIELD_NUMBER: _ClassVar[int]
    id: str
    token: str
    environment_id: str
    name: str
    source_id: str
    source_token: str
    severity_id: str
    severity_token: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        token: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        source_id: _Optional[str] = ...,
        source_token: _Optional[str] = ...,
        severity_id: _Optional[str] = ...,
        severity_token: _Optional[str] = ...,
    ) -> None: ...

class IncidentIoEventV2(_message.Message):
    __slots__ = ("route_id", "route_token", "dedup_key", "source_url", "description", "status", "title")
    ROUTE_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DEDUP_KEY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_URL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    route_id: str
    route_token: str
    dedup_key: str
    source_url: str
    description: str
    status: str
    title: str
    def __init__(
        self,
        route_id: _Optional[str] = ...,
        route_token: _Optional[str] = ...,
        dedup_key: _Optional[str] = ...,
        source_url: _Optional[str] = ...,
        description: _Optional[str] = ...,
        status: _Optional[str] = ...,
        title: _Optional[str] = ...,
    ) -> None: ...

class TestPagerDutyIntegrationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetPagerDutyIntegrationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetPagerDutyIntegrationResponse(_message.Message):
    __slots__ = ("integration",)
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: PagerDutyIntegration
    def __init__(self, integration: _Optional[_Union[PagerDutyIntegration, _Mapping]] = ...) -> None: ...

class TestPagerDutyIntegrationResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class AddPagerDutyIntegrationRequest(_message.Message):
    __slots__ = ("name", "token")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    name: str
    token: str
    def __init__(self, name: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class AddPagerDutyIntegrationResponse(_message.Message):
    __slots__ = ("integration",)
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: PagerDutyIntegration
    def __init__(self, integration: _Optional[_Union[PagerDutyIntegration, _Mapping]] = ...) -> None: ...

class DeletePagerDutyIntegrationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeletePagerDutyIntegrationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdatePagerDutyIntegrationRequest(_message.Message):
    __slots__ = ("id", "name", "default", "token")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    default: bool
    token: str
    def __init__(
        self, id: _Optional[str] = ..., name: _Optional[str] = ..., default: bool = ..., token: _Optional[str] = ...
    ) -> None: ...

class UpdatePagerDutyIntegrationResponse(_message.Message):
    __slots__ = ("integration",)
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: PagerDutyIntegration
    def __init__(self, integration: _Optional[_Union[PagerDutyIntegration, _Mapping]] = ...) -> None: ...

class SetDefaultPagerDutyIntegrationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class SetDefaultPagerDutyIntegrationResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetAllPagerDutyIntegrationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAllPagerDutyIntegrationsResponse(_message.Message):
    __slots__ = ("integrations",)
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[PagerDutyIntegration]
    def __init__(self, integrations: _Optional[_Iterable[_Union[PagerDutyIntegration, _Mapping]]] = ...) -> None: ...

class TestIncidentIoIntegrationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TestIncidentIoIntegrationResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class GetIncidentIoIntegrationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetIncidentIoIntegrationResponse(_message.Message):
    __slots__ = ("integration",)
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: IncidentIoIntegration
    def __init__(self, integration: _Optional[_Union[IncidentIoIntegration, _Mapping]] = ...) -> None: ...

class AddIncidentIoIntegrationRequest(_message.Message):
    __slots__ = ("integration_name", "integration_token", "integration_source_id")
    INTEGRATION_NAME_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    integration_name: str
    integration_token: str
    integration_source_id: str
    def __init__(
        self,
        integration_name: _Optional[str] = ...,
        integration_token: _Optional[str] = ...,
        integration_source_id: _Optional[str] = ...,
    ) -> None: ...

class AddIncidentIoIntegrationResponse(_message.Message):
    __slots__ = ("integration",)
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: IncidentIoIntegration
    def __init__(self, integration: _Optional[_Union[IncidentIoIntegration, _Mapping]] = ...) -> None: ...

class DeleteIncidentIoIntegrationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteIncidentIoIntegrationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateIncidentIoIntegrationRequest(_message.Message):
    __slots__ = ("id", "name", "token", "source_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    token: str
    source_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        token: _Optional[str] = ...,
        source_id: _Optional[str] = ...,
    ) -> None: ...

class UpdateIncidentIoIntegrationResponse(_message.Message):
    __slots__ = ("integration",)
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: IncidentIoIntegration
    def __init__(self, integration: _Optional[_Union[IncidentIoIntegration, _Mapping]] = ...) -> None: ...

class GetAllIncidentIoIntegrationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAllIncidentIoIntegrationsResponse(_message.Message):
    __slots__ = ("integrations",)
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[IncidentIoIntegration]
    def __init__(self, integrations: _Optional[_Iterable[_Union[IncidentIoIntegration, _Mapping]]] = ...) -> None: ...
