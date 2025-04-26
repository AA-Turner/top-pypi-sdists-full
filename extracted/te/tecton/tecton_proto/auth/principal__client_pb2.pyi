from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
PRINCIPAL_TYPE_GROUP: PrincipalType
PRINCIPAL_TYPE_SERVICE_ACCOUNT: PrincipalType
PRINCIPAL_TYPE_UNSPECIFIED: PrincipalType
PRINCIPAL_TYPE_USER: PrincipalType
PRINCIPAL_TYPE_WORKSPACE: PrincipalType

class GroupBasic(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class Principal(_message.Message):
    __slots__ = ["id", "principal_type"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    principal_type: PrincipalType
    def __init__(self, principal_type: _Optional[_Union[PrincipalType, str]] = ..., id: _Optional[str] = ...) -> None: ...

class PrincipalBasic(_message.Message):
    __slots__ = ["group", "service_account", "user", "workspace"]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    group: GroupBasic
    service_account: ServiceAccountBasic
    user: UserBasic
    workspace: WorkspaceBasic
    def __init__(self, user: _Optional[_Union[UserBasic, _Mapping]] = ..., service_account: _Optional[_Union[ServiceAccountBasic, _Mapping]] = ..., group: _Optional[_Union[GroupBasic, _Mapping]] = ..., workspace: _Optional[_Union[WorkspaceBasic, _Mapping]] = ...) -> None: ...

class ServiceAccountBasic(_message.Message):
    __slots__ = ["creator", "description", "id", "is_active", "name", "owner"]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    creator: Principal
    description: str
    id: str
    is_active: bool
    name: str
    owner: PrincipalBasic
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_active: bool = ..., creator: _Optional[_Union[Principal, _Mapping]] = ..., owner: _Optional[_Union[PrincipalBasic, _Mapping]] = ...) -> None: ...

class UserBasic(_message.Message):
    __slots__ = ["first_name", "last_name", "login_email", "okta_id"]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    LOGIN_EMAIL_FIELD_NUMBER: _ClassVar[int]
    OKTA_ID_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    login_email: str
    okta_id: str
    def __init__(self, okta_id: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., login_email: _Optional[str] = ...) -> None: ...

class WorkspaceBasic(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class PrincipalType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
