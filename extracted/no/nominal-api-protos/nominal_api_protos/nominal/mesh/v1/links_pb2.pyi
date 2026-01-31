from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESOURCE_TYPE_UNSPECIFIED: _ClassVar[ResourceType]
    RESOURCE_TYPE_DATASET: _ClassVar[ResourceType]

class MeshServiceError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MESH_SERVICE_ERROR_LINK_NOT_FOUND: _ClassVar[MeshServiceError]
    MESH_SERVICE_ERROR_LINK_ALREADY_EXISTS: _ClassVar[MeshServiceError]
    MESH_SERVICE_ERROR_REMOTE_CONNECTION_NOT_FOUND: _ClassVar[MeshServiceError]
    MESH_SERVICE_ERROR_REMOTE_CONNECTION_ALREADY_EXISTS: _ClassVar[MeshServiceError]
    MESH_SERVICE_ERROR_REMOTE_CONNECTION_HAS_DEPENDENT_LINKS: _ClassVar[MeshServiceError]
RESOURCE_TYPE_UNSPECIFIED: ResourceType
RESOURCE_TYPE_DATASET: ResourceType
MESH_SERVICE_ERROR_LINK_NOT_FOUND: MeshServiceError
MESH_SERVICE_ERROR_LINK_ALREADY_EXISTS: MeshServiceError
MESH_SERVICE_ERROR_REMOTE_CONNECTION_NOT_FOUND: MeshServiceError
MESH_SERVICE_ERROR_REMOTE_CONNECTION_ALREADY_EXISTS: MeshServiceError
MESH_SERVICE_ERROR_REMOTE_CONNECTION_HAS_DEPENDENT_LINKS: MeshServiceError

class Link(_message.Message):
    __slots__ = ("rid", "local_resource_rid", "remote_resource_rid", "remote_connection_rid", "enabled", "resource_type")
    RID_FIELD_NUMBER: _ClassVar[int]
    LOCAL_RESOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    REMOTE_RESOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    REMOTE_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    rid: str
    local_resource_rid: str
    remote_resource_rid: str
    remote_connection_rid: str
    enabled: bool
    resource_type: ResourceType
    def __init__(self, rid: _Optional[str] = ..., local_resource_rid: _Optional[str] = ..., remote_resource_rid: _Optional[str] = ..., remote_connection_rid: _Optional[str] = ..., enabled: bool = ..., resource_type: _Optional[_Union[ResourceType, str]] = ...) -> None: ...

class CreateLinkRequest(_message.Message):
    __slots__ = ("local_resource_rid", "remote_resource_rid", "remote_connection_rid", "enabled", "resource_type", "workspace_rid")
    LOCAL_RESOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    REMOTE_RESOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    REMOTE_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    local_resource_rid: str
    remote_resource_rid: str
    remote_connection_rid: str
    enabled: bool
    resource_type: ResourceType
    workspace_rid: str
    def __init__(self, local_resource_rid: _Optional[str] = ..., remote_resource_rid: _Optional[str] = ..., remote_connection_rid: _Optional[str] = ..., enabled: bool = ..., resource_type: _Optional[_Union[ResourceType, str]] = ..., workspace_rid: _Optional[str] = ...) -> None: ...

class CreateLinkResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetLinkRequest(_message.Message):
    __slots__ = ("link_rid",)
    LINK_RID_FIELD_NUMBER: _ClassVar[int]
    link_rid: str
    def __init__(self, link_rid: _Optional[str] = ...) -> None: ...

class GetLinkResponse(_message.Message):
    __slots__ = ("link",)
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: Link
    def __init__(self, link: _Optional[_Union[Link, _Mapping]] = ...) -> None: ...

class UpdateLinkRequest(_message.Message):
    __slots__ = ("link_rid", "remote_connection_rid", "enabled")
    LINK_RID_FIELD_NUMBER: _ClassVar[int]
    REMOTE_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    link_rid: str
    remote_connection_rid: str
    enabled: bool
    def __init__(self, link_rid: _Optional[str] = ..., remote_connection_rid: _Optional[str] = ..., enabled: bool = ...) -> None: ...

class UpdateLinkResponse(_message.Message):
    __slots__ = ("link",)
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: Link
    def __init__(self, link: _Optional[_Union[Link, _Mapping]] = ...) -> None: ...

class DeleteLinkRequest(_message.Message):
    __slots__ = ("link_rid",)
    LINK_RID_FIELD_NUMBER: _ClassVar[int]
    link_rid: str
    def __init__(self, link_rid: _Optional[str] = ...) -> None: ...

class DeleteLinkResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
