from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESOURCE_TYPE_UNSPECIFIED: _ClassVar[ResourceType]
    RESOURCE_TYPE_WORKBOOK: _ClassVar[ResourceType]
    RESOURCE_TYPE_CHECKLIST: _ClassVar[ResourceType]
    RESOURCE_TYPE_PROCEDURE: _ClassVar[ResourceType]
RESOURCE_TYPE_UNSPECIFIED: ResourceType
RESOURCE_TYPE_WORKBOOK: ResourceType
RESOURCE_TYPE_CHECKLIST: ResourceType
RESOURCE_TYPE_PROCEDURE: ResourceType

class ResourceOpenedEvent(_message.Message):
    __slots__ = ("resource_type", "rid", "is_creator")
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RID_FIELD_NUMBER: _ClassVar[int]
    IS_CREATOR_FIELD_NUMBER: _ClassVar[int]
    resource_type: ResourceType
    rid: str
    is_creator: bool
    def __init__(self, resource_type: _Optional[_Union[ResourceType, str]] = ..., rid: _Optional[str] = ..., is_creator: bool = ...) -> None: ...

class TrackEventRequest(_message.Message):
    __slots__ = ("workspace_rid", "resource_opened")
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_OPENED_FIELD_NUMBER: _ClassVar[int]
    workspace_rid: str
    resource_opened: ResourceOpenedEvent
    def __init__(self, workspace_rid: _Optional[str] = ..., resource_opened: _Optional[_Union[ResourceOpenedEvent, _Mapping]] = ...) -> None: ...

class TrackEventResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
