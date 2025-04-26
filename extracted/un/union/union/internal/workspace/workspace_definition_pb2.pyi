from union.internal.common import identity_pb2 as _identity_pb2
from flyteidl.admin import task_pb2 as _task_pb2
from flyteidl.core import identifier_pb2 as _identifier_pb2
from flyteidl.core import security_pb2 as _security_pb2
from flyteidl.core import tasks_pb2 as _tasks_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from union.internal.validate.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WorkspaceDefinitionState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    WORKSPACE_DEFINITION_STATE_UNSPECIFIED: _ClassVar[WorkspaceDefinitionState]
    WORKSPACE_DEFINITION_STATE_ACTIVE: _ClassVar[WorkspaceDefinitionState]
    WORKSPACE_DEFINITION_STATE_ARCHIVED: _ClassVar[WorkspaceDefinitionState]
WORKSPACE_DEFINITION_STATE_UNSPECIFIED: WorkspaceDefinitionState
WORKSPACE_DEFINITION_STATE_ACTIVE: WorkspaceDefinitionState
WORKSPACE_DEFINITION_STATE_ARCHIVED: WorkspaceDefinitionState

class WorkspaceDefinitionIdentifier(_message.Message):
    __slots__ = ["org", "project", "domain", "name", "version"]
    ORG_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    org: str
    project: str
    domain: str
    name: str
    version: str
    def __init__(self, org: _Optional[str] = ..., project: _Optional[str] = ..., domain: _Optional[str] = ..., name: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class WorkspaceDefinition(_message.Message):
    __slots__ = ["id", "spec"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    id: WorkspaceDefinitionIdentifier
    spec: WorkspaceDefinitionSpec
    def __init__(self, id: _Optional[_Union[WorkspaceDefinitionIdentifier, _Mapping]] = ..., spec: _Optional[_Union[WorkspaceDefinitionSpec, _Mapping]] = ...) -> None: ...

class WorkspaceDefinitionSpec(_message.Message):
    __slots__ = ["short_description", "created_at", "updated_at", "task_id", "state", "task_spec", "resources", "extended_resources", "ttl_seconds", "security_context", "python_environment", "conda_environment", "on_startup", "container_image", "workspace_root", "working_dir"]
    SHORT_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TASK_SPEC_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    TTL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    SECURITY_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    PYTHON_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    CONDA_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    ON_STARTUP_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_IMAGE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ROOT_FIELD_NUMBER: _ClassVar[int]
    WORKING_DIR_FIELD_NUMBER: _ClassVar[int]
    short_description: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    task_id: _identifier_pb2.Identifier
    state: WorkspaceDefinitionState
    task_spec: _task_pb2.TaskSpec
    resources: _tasks_pb2.Resources
    extended_resources: _tasks_pb2.ExtendedResources
    ttl_seconds: int
    security_context: _security_pb2.SecurityContext
    python_environment: PythonEnvironment
    conda_environment: CondaEnvironment
    on_startup: _containers.RepeatedScalarFieldContainer[str]
    container_image: str
    workspace_root: str
    working_dir: str
    def __init__(self, short_description: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., task_id: _Optional[_Union[_identifier_pb2.Identifier, _Mapping]] = ..., state: _Optional[_Union[WorkspaceDefinitionState, str]] = ..., task_spec: _Optional[_Union[_task_pb2.TaskSpec, _Mapping]] = ..., resources: _Optional[_Union[_tasks_pb2.Resources, _Mapping]] = ..., extended_resources: _Optional[_Union[_tasks_pb2.ExtendedResources, _Mapping]] = ..., ttl_seconds: _Optional[int] = ..., security_context: _Optional[_Union[_security_pb2.SecurityContext, _Mapping]] = ..., python_environment: _Optional[_Union[PythonEnvironment, _Mapping]] = ..., conda_environment: _Optional[_Union[CondaEnvironment, _Mapping]] = ..., on_startup: _Optional[_Iterable[str]] = ..., container_image: _Optional[str] = ..., workspace_root: _Optional[str] = ..., working_dir: _Optional[str] = ...) -> None: ...

class PythonEnvironment(_message.Message):
    __slots__ = ["packages"]
    PACKAGES_FIELD_NUMBER: _ClassVar[int]
    packages: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, packages: _Optional[_Iterable[str]] = ...) -> None: ...

class CondaEnvironment(_message.Message):
    __slots__ = ["packages", "channels"]
    PACKAGES_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    packages: _containers.RepeatedScalarFieldContainer[str]
    channels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, packages: _Optional[_Iterable[str]] = ..., channels: _Optional[_Iterable[str]] = ...) -> None: ...

class WorkspaceDefinitionEntityId(_message.Message):
    __slots__ = ["org", "project", "domain", "name"]
    ORG_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    org: str
    project: str
    domain: str
    name: str
    def __init__(self, org: _Optional[str] = ..., project: _Optional[str] = ..., domain: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class AuditMetadata(_message.Message):
    __slots__ = ["created_at", "updated_at", "created_by", "updated_by"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    created_by: _identity_pb2.EnrichedIdentity
    updated_by: _identity_pb2.EnrichedIdentity
    def __init__(self, created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_by: _Optional[_Union[_identity_pb2.EnrichedIdentity, _Mapping]] = ..., updated_by: _Optional[_Union[_identity_pb2.EnrichedIdentity, _Mapping]] = ...) -> None: ...

class WorkspaceDefinitionEntity(_message.Message):
    __slots__ = ["id", "state", "short_description", "audit_metadata"]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SHORT_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    AUDIT_METADATA_FIELD_NUMBER: _ClassVar[int]
    id: WorkspaceDefinitionEntityId
    state: WorkspaceDefinitionState
    short_description: str
    audit_metadata: AuditMetadata
    def __init__(self, id: _Optional[_Union[WorkspaceDefinitionEntityId, _Mapping]] = ..., state: _Optional[_Union[WorkspaceDefinitionState, str]] = ..., short_description: _Optional[str] = ..., audit_metadata: _Optional[_Union[AuditMetadata, _Mapping]] = ...) -> None: ...
