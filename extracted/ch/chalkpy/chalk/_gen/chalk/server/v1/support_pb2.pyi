from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IncidentServiceReference(_message.Message):
    __slots__ = ("id", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class IncidentBody(_message.Message):
    __slots__ = ("type", "details")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    type: str
    details: str
    def __init__(self, type: _Optional[str] = ..., details: _Optional[str] = ...) -> None: ...

class Incident(_message.Message):
    __slots__ = ("type", "title", "service", "urgency", "incident_key", "body")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    URGENCY_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_KEY_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    type: str
    title: str
    service: IncidentServiceReference
    urgency: str
    incident_key: str
    body: IncidentBody
    def __init__(
        self,
        type: _Optional[str] = ...,
        title: _Optional[str] = ...,
        service: _Optional[_Union[IncidentServiceReference, _Mapping]] = ...,
        urgency: _Optional[str] = ...,
        incident_key: _Optional[str] = ...,
        body: _Optional[_Union[IncidentBody, _Mapping]] = ...,
    ) -> None: ...

class CreateCustomerIncidentRequest(_message.Message):
    __slots__ = ("incident",)
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    incident: Incident
    def __init__(self, incident: _Optional[_Union[Incident, _Mapping]] = ...) -> None: ...

class CreateCustomerIncidentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
