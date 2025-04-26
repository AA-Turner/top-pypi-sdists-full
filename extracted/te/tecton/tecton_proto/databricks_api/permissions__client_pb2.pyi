from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccessControlListResponse(_message.Message):
    __slots__ = ["all_permissions", "display_name", "group_name", "service_principal_name", "user_name"]
    ALL_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_PRINCIPAL_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    all_permissions: _containers.RepeatedCompositeFieldContainer[PermissionObject]
    display_name: str
    group_name: str
    service_principal_name: str
    user_name: str
    def __init__(self, user_name: _Optional[str] = ..., group_name: _Optional[str] = ..., service_principal_name: _Optional[str] = ..., display_name: _Optional[str] = ..., all_permissions: _Optional[_Iterable[_Union[PermissionObject, _Mapping]]] = ...) -> None: ...

class GroupPermissionsObject(_message.Message):
    __slots__ = ["group_name", "permission_level", "service_principal_name", "user_name"]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_PRINCIPAL_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    group_name: str
    permission_level: str
    service_principal_name: str
    user_name: str
    def __init__(self, group_name: _Optional[str] = ..., permission_level: _Optional[str] = ..., user_name: _Optional[str] = ..., service_principal_name: _Optional[str] = ...) -> None: ...

class PermissionObject(_message.Message):
    __slots__ = ["inherited", "inherited_from_object", "permission_level"]
    INHERITED_FIELD_NUMBER: _ClassVar[int]
    INHERITED_FROM_OBJECT_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    inherited: bool
    inherited_from_object: _containers.RepeatedScalarFieldContainer[str]
    permission_level: str
    def __init__(self, permission_level: _Optional[str] = ..., inherited: bool = ..., inherited_from_object: _Optional[_Iterable[str]] = ...) -> None: ...

class PermissionsRequest(_message.Message):
    __slots__ = ["access_control_list"]
    ACCESS_CONTROL_LIST_FIELD_NUMBER: _ClassVar[int]
    access_control_list: _containers.RepeatedCompositeFieldContainer[GroupPermissionsObject]
    def __init__(self, access_control_list: _Optional[_Iterable[_Union[GroupPermissionsObject, _Mapping]]] = ...) -> None: ...

class PermissionsResponse(_message.Message):
    __slots__ = ["access_control_list", "object_id", "object_type"]
    ACCESS_CONTROL_LIST_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    access_control_list: _containers.RepeatedCompositeFieldContainer[AccessControlListResponse]
    object_id: str
    object_type: str
    def __init__(self, object_id: _Optional[str] = ..., object_type: _Optional[str] = ..., access_control_list: _Optional[_Iterable[_Union[AccessControlListResponse, _Mapping]]] = ...) -> None: ...
