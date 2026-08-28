from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import cloud_config_pb2 as _cloud_config_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class CloudPermissionDecision(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOUD_PERMISSION_DECISION_UNSPECIFIED: _ClassVar[CloudPermissionDecision]
    CLOUD_PERMISSION_DECISION_ALLOWED: _ClassVar[CloudPermissionDecision]
    CLOUD_PERMISSION_DECISION_IMPLICIT_DENY: _ClassVar[CloudPermissionDecision]
    CLOUD_PERMISSION_DECISION_EXPLICIT_DENY: _ClassVar[CloudPermissionDecision]

CLOUD_PERMISSION_DECISION_UNSPECIFIED: CloudPermissionDecision
CLOUD_PERMISSION_DECISION_ALLOWED: CloudPermissionDecision
CLOUD_PERMISSION_DECISION_IMPLICIT_DENY: CloudPermissionDecision
CLOUD_PERMISSION_DECISION_EXPLICIT_DENY: CloudPermissionDecision

class ListCloudCredentialsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCloudCredentialsResponse(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: _containers.RepeatedCompositeFieldContainer[CloudCredentialsResponse]
    def __init__(self, credentials: _Optional[_Iterable[_Union[CloudCredentialsResponse, _Mapping]]] = ...) -> None: ...

class CloudCredentialsResponse(_message.Message):
    __slots__ = ("id", "team_id", "name", "kind", "spec", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    team_id: str
    name: str
    kind: str
    spec: _cloud_config_pb2.CloudConfig
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        spec: _Optional[_Union[_cloud_config_pb2.CloudConfig, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class CloudCredentialsRequest(_message.Message):
    __slots__ = ("name", "kind", "config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    kind: str
    config: _cloud_config_pb2.CloudConfig
    def __init__(
        self,
        name: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        config: _Optional[_Union[_cloud_config_pb2.CloudConfig, _Mapping]] = ...,
    ) -> None: ...

class CreateCloudCredentialsRequest(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: CloudCredentialsRequest
    def __init__(self, credentials: _Optional[_Union[CloudCredentialsRequest, _Mapping]] = ...) -> None: ...

class CreateCloudCredentialsResponse(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: CloudCredentialsResponse
    def __init__(self, credentials: _Optional[_Union[CloudCredentialsResponse, _Mapping]] = ...) -> None: ...

class GetCloudCredentialsRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCloudCredentialsResponse(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: CloudCredentialsResponse
    def __init__(self, credentials: _Optional[_Union[CloudCredentialsResponse, _Mapping]] = ...) -> None: ...

class UpdateCloudCredentialsRequest(_message.Message):
    __slots__ = ("id", "credentials")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    id: str
    credentials: CloudCredentialsRequest
    def __init__(
        self, id: _Optional[str] = ..., credentials: _Optional[_Union[CloudCredentialsRequest, _Mapping]] = ...
    ) -> None: ...

class UpdateCloudCredentialsResponse(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: CloudCredentialsResponse
    def __init__(self, credentials: _Optional[_Union[CloudCredentialsResponse, _Mapping]] = ...) -> None: ...

class DeleteCloudCredentialsRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteCloudCredentialsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TestCloudCredentialsRequest(_message.Message):
    __slots__ = ("id", "config")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    id: str
    config: CloudCredentialsRequest
    def __init__(
        self, id: _Optional[str] = ..., config: _Optional[_Union[CloudCredentialsRequest, _Mapping]] = ...
    ) -> None: ...

class TestCloudCredentialsResponse(_message.Message):
    __slots__ = ("success", "message", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    error: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class CloudPermissionContext(_message.Message):
    __slots__ = ("key", "values")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    key: str
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, key: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...

class CloudPermissionSimulation(_message.Message):
    __slots__ = ("action", "resource", "decision", "context")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    DECISION_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    action: str
    resource: str
    decision: CloudPermissionDecision
    context: _containers.RepeatedCompositeFieldContainer[CloudPermissionContext]
    def __init__(
        self,
        action: _Optional[str] = ...,
        resource: _Optional[str] = ...,
        decision: _Optional[_Union[CloudPermissionDecision, str]] = ...,
        context: _Optional[_Iterable[_Union[CloudPermissionContext, _Mapping]]] = ...,
    ) -> None: ...

class SimulateClusterPermissionsRequest(_message.Message):
    __slots__ = ("cloud_credential_id",)
    CLOUD_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    cloud_credential_id: str
    def __init__(self, cloud_credential_id: _Optional[str] = ...) -> None: ...

class SimulateClusterPermissionsResponse(_message.Message):
    __slots__ = ("simulations",)
    SIMULATIONS_FIELD_NUMBER: _ClassVar[int]
    simulations: _containers.RepeatedCompositeFieldContainer[CloudPermissionSimulation]
    def __init__(
        self, simulations: _Optional[_Iterable[_Union[CloudPermissionSimulation, _Mapping]]] = ...
    ) -> None: ...

class SimulateVPCPermissionsRequest(_message.Message):
    __slots__ = ("cloud_credential_id",)
    CLOUD_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    cloud_credential_id: str
    def __init__(self, cloud_credential_id: _Optional[str] = ...) -> None: ...

class SimulateVPCPermissionsResponse(_message.Message):
    __slots__ = ("simulations",)
    SIMULATIONS_FIELD_NUMBER: _ClassVar[int]
    simulations: _containers.RepeatedCompositeFieldContainer[CloudPermissionSimulation]
    def __init__(
        self, simulations: _Optional[_Iterable[_Union[CloudPermissionSimulation, _Mapping]]] = ...
    ) -> None: ...
