from union.internal.common import identity_pb2 as _identity_pb2
from flyteidl.core import identifier_pb2 as _identifier_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from union.internal.validate.validate import validate_pb2 as _validate_pb2
from union.internal.workspace import workspace_definition_pb2 as _workspace_definition_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WorkspaceInstanceIdentifier(_message.Message):
    __slots__ = ["org", "project", "domain", "name", "host"]
    ORG_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    org: str
    project: str
    domain: str
    name: str
    host: str
    def __init__(self, org: _Optional[str] = ..., project: _Optional[str] = ..., domain: _Optional[str] = ..., name: _Optional[str] = ..., host: _Optional[str] = ...) -> None: ...

class WorkspaceInstanceStatus(_message.Message):
    __slots__ = ["phase"]
    class WorkspaceInstancePhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        WORKSPACE_INSTANCE_PHASE_UNSPECIFIED: _ClassVar[WorkspaceInstanceStatus.WorkspaceInstancePhase]
        WORKSPACE_INSTANCE_PHASE_PENDING: _ClassVar[WorkspaceInstanceStatus.WorkspaceInstancePhase]
        WORKSPACE_INSTANCE_PHASE_RUNNING: _ClassVar[WorkspaceInstanceStatus.WorkspaceInstancePhase]
        WORKSPACE_INSTANCE_PHASE_TERMINATING: _ClassVar[WorkspaceInstanceStatus.WorkspaceInstancePhase]
        WORKSPACE_INSTANCE_PHASE_TERMINATED: _ClassVar[WorkspaceInstanceStatus.WorkspaceInstancePhase]
        WORKSPACE_INSTANCE_PHASE_FAILED: _ClassVar[WorkspaceInstanceStatus.WorkspaceInstancePhase]
    WORKSPACE_INSTANCE_PHASE_UNSPECIFIED: WorkspaceInstanceStatus.WorkspaceInstancePhase
    WORKSPACE_INSTANCE_PHASE_PENDING: WorkspaceInstanceStatus.WorkspaceInstancePhase
    WORKSPACE_INSTANCE_PHASE_RUNNING: WorkspaceInstanceStatus.WorkspaceInstancePhase
    WORKSPACE_INSTANCE_PHASE_TERMINATING: WorkspaceInstanceStatus.WorkspaceInstancePhase
    WORKSPACE_INSTANCE_PHASE_TERMINATED: WorkspaceInstanceStatus.WorkspaceInstancePhase
    WORKSPACE_INSTANCE_PHASE_FAILED: WorkspaceInstanceStatus.WorkspaceInstancePhase
    PHASE_FIELD_NUMBER: _ClassVar[int]
    phase: WorkspaceInstanceStatus.WorkspaceInstancePhase
    def __init__(self, phase: _Optional[_Union[WorkspaceInstanceStatus.WorkspaceInstancePhase, str]] = ...) -> None: ...

class WorkspaceInstanceSpec(_message.Message):
    __slots__ = ["status", "identity", "created_at", "updated_at", "workspace_definition_id", "workflow_execution_id", "uri"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    status: WorkspaceInstanceStatus
    identity: _identity_pb2.Identity
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    workspace_definition_id: _workspace_definition_pb2.WorkspaceDefinitionIdentifier
    workflow_execution_id: _identifier_pb2.WorkflowExecutionIdentifier
    uri: str
    def __init__(self, status: _Optional[_Union[WorkspaceInstanceStatus, _Mapping]] = ..., identity: _Optional[_Union[_identity_pb2.Identity, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., workspace_definition_id: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinitionIdentifier, _Mapping]] = ..., workflow_execution_id: _Optional[_Union[_identifier_pb2.WorkflowExecutionIdentifier, _Mapping]] = ..., uri: _Optional[str] = ...) -> None: ...

class WorkspaceInstance(_message.Message):
    __slots__ = ["id", "spec"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    id: WorkspaceInstanceIdentifier
    spec: WorkspaceInstanceSpec
    def __init__(self, id: _Optional[_Union[WorkspaceInstanceIdentifier, _Mapping]] = ..., spec: _Optional[_Union[WorkspaceInstanceSpec, _Mapping]] = ...) -> None: ...

class WorkspaceInstances(_message.Message):
    __slots__ = ["instances"]
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    instances: _containers.RepeatedCompositeFieldContainer[WorkspaceInstance]
    def __init__(self, instances: _Optional[_Iterable[_Union[WorkspaceInstance, _Mapping]]] = ...) -> None: ...

class StartEvent(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: WorkspaceInstance
    def __init__(self, workspace: _Optional[_Union[WorkspaceInstance, _Mapping]] = ...) -> None: ...

class UpdateEvent(_message.Message):
    __slots__ = ["updated_workspace", "old_workspace"]
    UPDATED_WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    OLD_WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    updated_workspace: WorkspaceInstance
    old_workspace: WorkspaceInstance
    def __init__(self, updated_workspace: _Optional[_Union[WorkspaceInstance, _Mapping]] = ..., old_workspace: _Optional[_Union[WorkspaceInstance, _Mapping]] = ...) -> None: ...

class StopEvent(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: WorkspaceInstanceIdentifier
    def __init__(self, id: _Optional[_Union[WorkspaceInstanceIdentifier, _Mapping]] = ...) -> None: ...

class StoppingEvent(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: WorkspaceInstanceIdentifier
    def __init__(self, id: _Optional[_Union[WorkspaceInstanceIdentifier, _Mapping]] = ...) -> None: ...
