from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from tecton_proto.auth import principal__client_pb2 as _principal__client_pb2
from tecton_proto.auth import resource_role_assignments__client_pb2 as _resource_role_assignments__client_pb2
from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from tecton_proto.data import principal_group__client_pb2 as _principal_group__client_pb2
from tecton_proto.data import user__client_pb2 as _user__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddPrincipalGroupMember(_message.Message):
    __slots__ = ["principal_id", "principal_type"]
    PRINCIPAL_ID_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    principal_id: str
    principal_type: _principal__client_pb2.PrincipalType
    def __init__(self, principal_type: _Optional[_Union[_principal__client_pb2.PrincipalType, str]] = ..., principal_id: _Optional[str] = ...) -> None: ...

class AddPrincipalGroupMembersRequest(_message.Message):
    __slots__ = ["members", "principal_group_id"]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    members: _containers.RepeatedCompositeFieldContainer[AddPrincipalGroupMember]
    principal_group_id: str
    def __init__(self, principal_group_id: _Optional[str] = ..., members: _Optional[_Iterable[_Union[AddPrincipalGroupMember, _Mapping]]] = ...) -> None: ...

class AddPrincipalGroupMembersResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CreatePrincipalGroupRequest(_message.Message):
    __slots__ = ["description", "idp_mapping_names", "name"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IDP_MAPPING_NAMES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    description: str
    idp_mapping_names: _containers.RepeatedScalarFieldContainer[str]
    name: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., idp_mapping_names: _Optional[_Iterable[str]] = ...) -> None: ...

class CreatePrincipalGroupResponse(_message.Message):
    __slots__ = ["principal_group"]
    PRINCIPAL_GROUP_FIELD_NUMBER: _ClassVar[int]
    principal_group: _principal_group__client_pb2.PrincipalGroup
    def __init__(self, principal_group: _Optional[_Union[_principal_group__client_pb2.PrincipalGroup, _Mapping]] = ...) -> None: ...

class DeletePrincipalGroupsRequest(_message.Message):
    __slots__ = ["ids"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DeletePrincipalGroupsResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListPrincipalGroupMembersRequest(_message.Message):
    __slots__ = ["id", "principal_types", "search"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_TYPES_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    id: str
    principal_types: _containers.RepeatedScalarFieldContainer[_principal__client_pb2.PrincipalType]
    search: str
    def __init__(self, id: _Optional[str] = ..., search: _Optional[str] = ..., principal_types: _Optional[_Iterable[_Union[_principal__client_pb2.PrincipalType, str]]] = ...) -> None: ...

class ListPrincipalGroupMembersResponse(_message.Message):
    __slots__ = ["members"]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    members: _containers.RepeatedCompositeFieldContainer[PrincipalGroupMember]
    def __init__(self, members: _Optional[_Iterable[_Union[PrincipalGroupMember, _Mapping]]] = ...) -> None: ...

class ListPrincipalGroupsDetailedRequest(_message.Message):
    __slots__ = ["ids", "search"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    search: str
    def __init__(self, search: _Optional[str] = ..., ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ListPrincipalGroupsDetailedResponse(_message.Message):
    __slots__ = ["groups"]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[PrincipalGroupDetailed]
    def __init__(self, groups: _Optional[_Iterable[_Union[PrincipalGroupDetailed, _Mapping]]] = ...) -> None: ...

class ListPrincipalGroupsForPrincipalRequest(_message.Message):
    __slots__ = ["principal_id", "principal_type", "search"]
    PRINCIPAL_ID_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    principal_id: str
    principal_type: _principal__client_pb2.PrincipalType
    search: str
    def __init__(self, principal_type: _Optional[_Union[_principal__client_pb2.PrincipalType, str]] = ..., principal_id: _Optional[str] = ..., search: _Optional[str] = ...) -> None: ...

class ListPrincipalGroupsForPrincipalResponse(_message.Message):
    __slots__ = ["groups"]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[PrincipalGroupForPrincipal]
    def __init__(self, groups: _Optional[_Iterable[_Union[PrincipalGroupForPrincipal, _Mapping]]] = ...) -> None: ...

class ListUsersRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListUsersResponse(_message.Message):
    __slots__ = ["users"]
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[_user__client_pb2.User]
    def __init__(self, users: _Optional[_Iterable[_Union[_user__client_pb2.User, _Mapping]]] = ...) -> None: ...

class PrincipalGroupDetailed(_message.Message):
    __slots__ = ["account_type", "created_at", "created_by", "description", "id", "idp_mapping_names", "is_membership_editable", "name", "num_members", "workspaces"]
    ACCOUNT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IDP_MAPPING_NAMES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_MEMBERSHIP_EDITABLE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NUM_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    account_type: str
    created_at: _timestamp_pb2.Timestamp
    created_by: _principal__client_pb2.PrincipalBasic
    description: str
    id: str
    idp_mapping_names: _containers.RepeatedScalarFieldContainer[str]
    is_membership_editable: bool
    name: str
    num_members: int
    workspaces: _containers.RepeatedCompositeFieldContainer[_resource_role_assignments__client_pb2.ResourceAndRoleAssignmentsV2]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., idp_mapping_names: _Optional[_Iterable[str]] = ..., is_membership_editable: bool = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., account_type: _Optional[str] = ..., num_members: _Optional[int] = ..., workspaces: _Optional[_Iterable[_Union[_resource_role_assignments__client_pb2.ResourceAndRoleAssignmentsV2, _Mapping]]] = ..., created_by: _Optional[_Union[_principal__client_pb2.PrincipalBasic, _Mapping]] = ...) -> None: ...

class PrincipalGroupForPrincipal(_message.Message):
    __slots__ = ["group", "is_from_idp_mapping"]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    IS_FROM_IDP_MAPPING_FIELD_NUMBER: _ClassVar[int]
    group: _principal_group__client_pb2.PrincipalGroup
    is_from_idp_mapping: bool
    def __init__(self, group: _Optional[_Union[_principal_group__client_pb2.PrincipalGroup, _Mapping]] = ..., is_from_idp_mapping: bool = ...) -> None: ...

class PrincipalGroupMember(_message.Message):
    __slots__ = ["is_from_idp_mapping", "principal"]
    IS_FROM_IDP_MAPPING_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    is_from_idp_mapping: bool
    principal: _principal__client_pb2.PrincipalBasic
    def __init__(self, principal: _Optional[_Union[_principal__client_pb2.PrincipalBasic, _Mapping]] = ..., is_from_idp_mapping: bool = ...) -> None: ...

class RemovePrincipalGroupMember(_message.Message):
    __slots__ = ["principal_id", "principal_type"]
    PRINCIPAL_ID_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    principal_id: str
    principal_type: _principal__client_pb2.PrincipalType
    def __init__(self, principal_type: _Optional[_Union[_principal__client_pb2.PrincipalType, str]] = ..., principal_id: _Optional[str] = ...) -> None: ...

class RemovePrincipalGroupMembersRequest(_message.Message):
    __slots__ = ["id", "members"]
    ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    members: _containers.RepeatedCompositeFieldContainer[RemovePrincipalGroupMember]
    def __init__(self, id: _Optional[str] = ..., members: _Optional[_Iterable[_Union[RemovePrincipalGroupMember, _Mapping]]] = ...) -> None: ...

class RemovePrincipalGroupMembersResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdatePrincipalGroupRequest(_message.Message):
    __slots__ = ["description", "id", "idp_mapping_names", "name"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IDP_MAPPING_NAMES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    description: str
    id: str
    idp_mapping_names: _containers.RepeatedScalarFieldContainer[str]
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., idp_mapping_names: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdatePrincipalGroupResponse(_message.Message):
    __slots__ = ["principal_group"]
    PRINCIPAL_GROUP_FIELD_NUMBER: _ClassVar[int]
    principal_group: _principal_group__client_pb2.PrincipalGroup
    def __init__(self, principal_group: _Optional[_Union[_principal_group__client_pb2.PrincipalGroup, _Mapping]] = ...) -> None: ...
