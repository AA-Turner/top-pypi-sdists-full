from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from nominal.conjure.v1 import compat_pb2 as _compat_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from nominal.types import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SecurityError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SECURITY_ERROR_FORBIDDEN_CROSS_WORKSPACE_OPERATION: _ClassVar[SecurityError]
    SECURITY_ERROR_WORKSPACE_NOT_FOUND: _ClassVar[SecurityError]
    SECURITY_ERROR_WORKSPACE_NOT_SPECIFIED: _ClassVar[SecurityError]
SECURITY_ERROR_FORBIDDEN_CROSS_WORKSPACE_OPERATION: SecurityError
SECURITY_ERROR_WORKSPACE_NOT_FOUND: SecurityError
SECURITY_ERROR_WORKSPACE_NOT_SPECIFIED: SecurityError

class PreferredRefNameConfiguration(_message.Message):
    __slots__ = ("v1",)
    V1_FIELD_NUMBER: _ClassVar[int]
    v1: _containers.RepeatedCompositeFieldContainer[_types_pb2.RefNameAndType]
    def __init__(self, v1: _Optional[_Iterable[_Union[_types_pb2.RefNameAndType, _Mapping]]] = ...) -> None: ...

class RemoveType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateOrRemoveWorkspaceDisplayName(_message.Message):
    __slots__ = ("display_name", "remove_type")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    REMOVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    remove_type: RemoveType
    def __init__(self, display_name: _Optional[str] = ..., remove_type: _Optional[_Union[RemoveType, _Mapping]] = ...) -> None: ...

class UpdateOrRemoveWorkspaceSymbol(_message.Message):
    __slots__ = ("symbol", "remove_type")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    REMOVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    symbol: WorkspaceSymbol
    remove_type: RemoveType
    def __init__(self, symbol: _Optional[_Union[WorkspaceSymbol, _Mapping]] = ..., remove_type: _Optional[_Union[RemoveType, _Mapping]] = ...) -> None: ...

class UpdateWorkspaceRequest(_message.Message):
    __slots__ = ("display_name", "symbol", "settings")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    display_name: UpdateOrRemoveWorkspaceDisplayName
    symbol: UpdateOrRemoveWorkspaceSymbol
    settings: WorkspaceSettings
    def __init__(self, display_name: _Optional[_Union[UpdateOrRemoveWorkspaceDisplayName, _Mapping]] = ..., symbol: _Optional[_Union[UpdateOrRemoveWorkspaceSymbol, _Mapping]] = ..., settings: _Optional[_Union[WorkspaceSettings, _Mapping]] = ...) -> None: ...

class Workspace(_message.Message):
    __slots__ = ("id", "rid", "org", "display_name", "symbol", "settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    RID_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    rid: str
    org: str
    display_name: str
    symbol: WorkspaceSymbol
    settings: WorkspaceSettings
    def __init__(self, id: _Optional[str] = ..., rid: _Optional[str] = ..., org: _Optional[str] = ..., display_name: _Optional[str] = ..., symbol: _Optional[_Union[WorkspaceSymbol, _Mapping]] = ..., settings: _Optional[_Union[WorkspaceSettings, _Mapping]] = ...) -> None: ...

class WorkspaceSettings(_message.Message):
    __slots__ = ("ref_names",)
    REF_NAMES_FIELD_NUMBER: _ClassVar[int]
    ref_names: PreferredRefNameConfiguration
    def __init__(self, ref_names: _Optional[_Union[PreferredRefNameConfiguration, _Mapping]] = ...) -> None: ...

class WorkspaceSymbol(_message.Message):
    __slots__ = ("icon", "emoji", "image")
    ICON_FIELD_NUMBER: _ClassVar[int]
    EMOJI_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    icon: str
    emoji: str
    image: str
    def __init__(self, icon: _Optional[str] = ..., emoji: _Optional[str] = ..., image: _Optional[str] = ...) -> None: ...

class GetWorkspacesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetWorkspacesResponse(_message.Message):
    __slots__ = ("workspaces",)
    WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    workspaces: _containers.RepeatedCompositeFieldContainer[Workspace]
    def __init__(self, workspaces: _Optional[_Iterable[_Union[Workspace, _Mapping]]] = ...) -> None: ...

class GetWorkspaceRequest(_message.Message):
    __slots__ = ("workspace_rid",)
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    workspace_rid: str
    def __init__(self, workspace_rid: _Optional[str] = ...) -> None: ...

class GetWorkspaceResponse(_message.Message):
    __slots__ = ("workspace",)
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: Workspace
    def __init__(self, workspace: _Optional[_Union[Workspace, _Mapping]] = ...) -> None: ...

class UpdateWorkspaceRequestWrapper(_message.Message):
    __slots__ = ("rid", "request")
    RID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    rid: str
    request: UpdateWorkspaceRequest
    def __init__(self, rid: _Optional[str] = ..., request: _Optional[_Union[UpdateWorkspaceRequest, _Mapping]] = ...) -> None: ...

class UpdateWorkspaceResponse(_message.Message):
    __slots__ = ("workspace",)
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: Workspace
    def __init__(self, workspace: _Optional[_Union[Workspace, _Mapping]] = ...) -> None: ...

class GetDefaultWorkspaceRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDefaultWorkspaceResponse(_message.Message):
    __slots__ = ("workspace",)
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: Workspace
    def __init__(self, workspace: _Optional[_Union[Workspace, _Mapping]] = ...) -> None: ...
