from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

AUTH_METADATA_FIELD_NUMBER: _ClassVar[int]
DESCRIPTOR: _descriptor.FileDescriptor
RESOURCE_REF_TYPE_PRINCIPAL_GROUP_ID: ResourceRefTypeEnum
RESOURCE_REF_TYPE_SECRET_SCOPE: ResourceRefTypeEnum
RESOURCE_REF_TYPE_SERVICE_ACCOUNT_ID: ResourceRefTypeEnum
RESOURCE_REF_TYPE_UNSPECIFIED: ResourceRefTypeEnum
RESOURCE_REF_TYPE_WORKSPACE_NAME: ResourceRefTypeEnum
auth_metadata: _descriptor.FieldDescriptor

class AuthMetadata(_message.Message):
    __slots__ = ["advanced_permission_overrides", "defer_authorization_to_service", "permission", "resource_reference", "skip_authentication", "skip_authorization"]
    ADVANCED_PERMISSION_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    DEFER_AUTHORIZATION_TO_SERVICE_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    SKIP_AUTHENTICATION_FIELD_NUMBER: _ClassVar[int]
    SKIP_AUTHORIZATION_FIELD_NUMBER: _ClassVar[int]
    advanced_permission_overrides: _containers.RepeatedCompositeFieldContainer[PermissionOverride]
    defer_authorization_to_service: bool
    permission: str
    resource_reference: ResourceReference
    skip_authentication: bool
    skip_authorization: bool
    def __init__(self, skip_authentication: bool = ..., skip_authorization: bool = ..., permission: _Optional[str] = ..., advanced_permission_overrides: _Optional[_Iterable[_Union[PermissionOverride, _Mapping]]] = ..., resource_reference: _Optional[_Union[ResourceReference, _Mapping]] = ..., defer_authorization_to_service: bool = ...) -> None: ...

class PermissionOverride(_message.Message):
    __slots__ = ["condition_field_path", "condition_value", "permission_override"]
    CONDITION_FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    CONDITION_VALUE_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    condition_field_path: str
    condition_value: str
    permission_override: str
    def __init__(self, condition_field_path: _Optional[str] = ..., condition_value: _Optional[str] = ..., permission_override: _Optional[str] = ...) -> None: ...

class ResourceReference(_message.Message):
    __slots__ = ["path", "type"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    path: str
    type: ResourceRefTypeEnum
    def __init__(self, type: _Optional[_Union[ResourceRefTypeEnum, str]] = ..., path: _Optional[str] = ...) -> None: ...

class ResourceRefTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
