from tecton_proto.auth import resource__client_pb2 as _resource__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
ROLE_ASSIGNMENT_TYPE_DIRECT: RoleAssignmentType
ROLE_ASSIGNMENT_TYPE_FROM_PRINCIPAL_GROUP: RoleAssignmentType
ROLE_ASSIGNMENT_TYPE_UNSPECIFIED: RoleAssignmentType

class ResourceAndRoleAssignments(_message.Message):
    __slots__ = ["resource_id", "resource_type", "roles", "roles_granted"]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    ROLES_GRANTED_FIELD_NUMBER: _ClassVar[int]
    resource_id: str
    resource_type: _resource__client_pb2.ResourceType
    roles: _containers.RepeatedScalarFieldContainer[str]
    roles_granted: _containers.RepeatedCompositeFieldContainer[RoleAssignmentSummary]
    def __init__(self, resource_type: _Optional[_Union[_resource__client_pb2.ResourceType, str]] = ..., resource_id: _Optional[str] = ..., roles: _Optional[_Iterable[str]] = ..., roles_granted: _Optional[_Iterable[_Union[RoleAssignmentSummary, _Mapping]]] = ...) -> None: ...

class ResourceAndRoleAssignmentsV2(_message.Message):
    __slots__ = ["resource_id", "resource_type", "roles_granted"]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROLES_GRANTED_FIELD_NUMBER: _ClassVar[int]
    resource_id: str
    resource_type: _resource__client_pb2.ResourceType
    roles_granted: _containers.RepeatedCompositeFieldContainer[RoleAssignmentSummary]
    def __init__(self, resource_type: _Optional[_Union[_resource__client_pb2.ResourceType, str]] = ..., resource_id: _Optional[str] = ..., roles_granted: _Optional[_Iterable[_Union[RoleAssignmentSummary, _Mapping]]] = ...) -> None: ...

class RoleAssignmentSource(_message.Message):
    __slots__ = ["assignment_type", "principal_group_id", "principal_group_name"]
    ASSIGNMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    assignment_type: RoleAssignmentType
    principal_group_id: str
    principal_group_name: str
    def __init__(self, assignment_type: _Optional[_Union[RoleAssignmentType, str]] = ..., principal_group_name: _Optional[str] = ..., principal_group_id: _Optional[str] = ...) -> None: ...

class RoleAssignmentSummary(_message.Message):
    __slots__ = ["role", "role_assignment_sources"]
    ROLE_ASSIGNMENT_SOURCES_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: str
    role_assignment_sources: _containers.RepeatedCompositeFieldContainer[RoleAssignmentSource]
    def __init__(self, role: _Optional[str] = ..., role_assignment_sources: _Optional[_Iterable[_Union[RoleAssignmentSource, _Mapping]]] = ...) -> None: ...

class RoleAssignmentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
