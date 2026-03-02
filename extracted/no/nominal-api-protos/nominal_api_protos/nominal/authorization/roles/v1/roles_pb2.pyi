from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROLE_UNSPECIFIED: _ClassVar[Role]
    ROLE_OWNER: _ClassVar[Role]
ROLE_UNSPECIFIED: Role
ROLE_OWNER: Role

class RoleAssignmentRequest(_message.Message):
    __slots__ = ("role", "user_rid")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    USER_RID_FIELD_NUMBER: _ClassVar[int]
    role: Role
    user_rid: str
    def __init__(self, role: _Optional[_Union[Role, str]] = ..., user_rid: _Optional[str] = ...) -> None: ...

class RoleAssignmentResponse(_message.Message):
    __slots__ = ("role", "user_rid")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    USER_RID_FIELD_NUMBER: _ClassVar[int]
    role: Role
    user_rid: str
    def __init__(self, role: _Optional[_Union[Role, str]] = ..., user_rid: _Optional[str] = ...) -> None: ...

class UpdateResourceRolesRequest(_message.Message):
    __slots__ = ("resource", "assignments_to_add", "assignments_to_remove")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    ASSIGNMENTS_TO_ADD_FIELD_NUMBER: _ClassVar[int]
    ASSIGNMENTS_TO_REMOVE_FIELD_NUMBER: _ClassVar[int]
    resource: str
    assignments_to_add: _containers.RepeatedCompositeFieldContainer[RoleAssignmentRequest]
    assignments_to_remove: _containers.RepeatedCompositeFieldContainer[RoleAssignmentRequest]
    def __init__(self, resource: _Optional[str] = ..., assignments_to_add: _Optional[_Iterable[_Union[RoleAssignmentRequest, _Mapping]]] = ..., assignments_to_remove: _Optional[_Iterable[_Union[RoleAssignmentRequest, _Mapping]]] = ...) -> None: ...

class UpdateResourceRolesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetResourceRolesRequest(_message.Message):
    __slots__ = ("resource",)
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: str
    def __init__(self, resource: _Optional[str] = ...) -> None: ...

class GetResourceRolesResponse(_message.Message):
    __slots__ = ("role_assignments",)
    ROLE_ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    role_assignments: _containers.RepeatedCompositeFieldContainer[RoleAssignmentResponse]
    def __init__(self, role_assignments: _Optional[_Iterable[_Union[RoleAssignmentResponse, _Mapping]]] = ...) -> None: ...

class BatchGetResourceRolesRequest(_message.Message):
    __slots__ = ("resources",)
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, resources: _Optional[_Iterable[str]] = ...) -> None: ...

class BatchGetResourceRolesResponse(_message.Message):
    __slots__ = ("role_assignments_by_resource",)
    class RoleAssignmentsByResourceEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: BatchGetResourceRolesResponse.RoleAssignmentWrapper
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[BatchGetResourceRolesResponse.RoleAssignmentWrapper, _Mapping]] = ...) -> None: ...
    class RoleAssignmentWrapper(_message.Message):
        __slots__ = ("role_assignments",)
        ROLE_ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
        role_assignments: _containers.RepeatedCompositeFieldContainer[RoleAssignmentResponse]
        def __init__(self, role_assignments: _Optional[_Iterable[_Union[RoleAssignmentResponse, _Mapping]]] = ...) -> None: ...
    ROLE_ASSIGNMENTS_BY_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    role_assignments_by_resource: _containers.MessageMap[str, BatchGetResourceRolesResponse.RoleAssignmentWrapper]
    def __init__(self, role_assignments_by_resource: _Optional[_Mapping[str, BatchGetResourceRolesResponse.RoleAssignmentWrapper]] = ...) -> None: ...
