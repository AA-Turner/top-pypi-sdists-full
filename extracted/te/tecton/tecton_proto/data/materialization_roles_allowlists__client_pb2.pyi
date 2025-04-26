from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MaterializationRolesAllowlists(_message.Message):
    __slots__ = ["workspace_configurations"]
    WORKSPACE_CONFIGURATIONS_FIELD_NUMBER: _ClassVar[int]
    workspace_configurations: _containers.RepeatedCompositeFieldContainer[WorkspaceMaterializationRolesAllowlist]
    def __init__(self, workspace_configurations: _Optional[_Iterable[_Union[WorkspaceMaterializationRolesAllowlist, _Mapping]]] = ...) -> None: ...

class WorkspaceMaterializationRolesAllowlist(_message.Message):
    __slots__ = ["allowed_materialization_roles", "workspace_name"]
    ALLOWED_MATERIALIZATION_ROLES_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    allowed_materialization_roles: _containers.RepeatedScalarFieldContainer[str]
    workspace_name: str
    def __init__(self, workspace_name: _Optional[str] = ..., allowed_materialization_roles: _Optional[_Iterable[str]] = ...) -> None: ...
