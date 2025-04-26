from union.internal.common import identifier_pb2 as _identifier_pb2
from union.internal.common import list_pb2 as _list_pb2
from flyteidl.admin import execution_pb2 as _execution_pb2
from flyteidl.core import literals_pb2 as _literals_pb2
from union.internal.validate.validate import validate_pb2 as _validate_pb2
from union.internal.workspace import workspace_definition_pb2 as _workspace_definition_pb2
from union.internal.workspace import workspace_instance_pb2 as _workspace_instance_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartWorkspaceInstanceRequest(_message.Message):
    __slots__ = ["org", "project", "domain", "name", "workspace_definition_id", "spec", "inputs"]
    ORG_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    org: str
    project: str
    domain: str
    name: str
    workspace_definition_id: _workspace_definition_pb2.WorkspaceDefinitionIdentifier
    spec: _execution_pb2.ExecutionSpec
    inputs: _literals_pb2.LiteralMap
    def __init__(self, org: _Optional[str] = ..., project: _Optional[str] = ..., domain: _Optional[str] = ..., name: _Optional[str] = ..., workspace_definition_id: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinitionIdentifier, _Mapping]] = ..., spec: _Optional[_Union[_execution_pb2.ExecutionSpec, _Mapping]] = ..., inputs: _Optional[_Union[_literals_pb2.LiteralMap, _Mapping]] = ...) -> None: ...

class StartWorkspaceInstanceResponse(_message.Message):
    __slots__ = ["workspace_instance"]
    WORKSPACE_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    workspace_instance: _workspace_instance_pb2.WorkspaceInstance
    def __init__(self, workspace_instance: _Optional[_Union[_workspace_instance_pb2.WorkspaceInstance, _Mapping]] = ...) -> None: ...

class GetWorkspaceInstanceRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _workspace_instance_pb2.WorkspaceInstanceIdentifier
    def __init__(self, id: _Optional[_Union[_workspace_instance_pb2.WorkspaceInstanceIdentifier, _Mapping]] = ...) -> None: ...

class GetWorkspaceInstanceResponse(_message.Message):
    __slots__ = ["workspace_instance"]
    WORKSPACE_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    workspace_instance: _workspace_instance_pb2.WorkspaceInstance
    def __init__(self, workspace_instance: _Optional[_Union[_workspace_instance_pb2.WorkspaceInstance, _Mapping]] = ...) -> None: ...

class ListWorkspaceInstancesRequest(_message.Message):
    __slots__ = ["request", "org", "project", "workspace_definition_id", "principal"]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    request: _list_pb2.ListRequest
    org: str
    project: _identifier_pb2.ProjectIdentifier
    workspace_definition_id: _workspace_definition_pb2.WorkspaceDefinitionIdentifier
    principal: str
    def __init__(self, request: _Optional[_Union[_list_pb2.ListRequest, _Mapping]] = ..., org: _Optional[str] = ..., project: _Optional[_Union[_identifier_pb2.ProjectIdentifier, _Mapping]] = ..., workspace_definition_id: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinitionIdentifier, _Mapping]] = ..., principal: _Optional[str] = ...) -> None: ...

class ListWorkspaceInstancesResponse(_message.Message):
    __slots__ = ["workspace_instances", "token"]
    WORKSPACE_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    workspace_instances: _containers.RepeatedCompositeFieldContainer[_workspace_instance_pb2.WorkspaceInstance]
    token: str
    def __init__(self, workspace_instances: _Optional[_Iterable[_Union[_workspace_instance_pb2.WorkspaceInstance, _Mapping]]] = ..., token: _Optional[str] = ...) -> None: ...

class WatchWorkspaceInstancesRequest(_message.Message):
    __slots__ = ["org", "project", "workspace_definition_id", "workspace_instance_id", "principal"]
    ORG_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    org: str
    project: _identifier_pb2.ProjectIdentifier
    workspace_definition_id: _workspace_definition_pb2.WorkspaceDefinitionIdentifier
    workspace_instance_id: _workspace_instance_pb2.WorkspaceInstanceIdentifier
    principal: str
    def __init__(self, org: _Optional[str] = ..., project: _Optional[_Union[_identifier_pb2.ProjectIdentifier, _Mapping]] = ..., workspace_definition_id: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinitionIdentifier, _Mapping]] = ..., workspace_instance_id: _Optional[_Union[_workspace_instance_pb2.WorkspaceInstanceIdentifier, _Mapping]] = ..., principal: _Optional[str] = ...) -> None: ...

class WatchWorkspaceInstancesResponse(_message.Message):
    __slots__ = ["start_event", "update_event", "stop_event", "stopping_event"]
    START_EVENT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_EVENT_FIELD_NUMBER: _ClassVar[int]
    STOP_EVENT_FIELD_NUMBER: _ClassVar[int]
    STOPPING_EVENT_FIELD_NUMBER: _ClassVar[int]
    start_event: _workspace_instance_pb2.StartEvent
    update_event: _workspace_instance_pb2.UpdateEvent
    stop_event: _workspace_instance_pb2.StopEvent
    stopping_event: _workspace_instance_pb2.StoppingEvent
    def __init__(self, start_event: _Optional[_Union[_workspace_instance_pb2.StartEvent, _Mapping]] = ..., update_event: _Optional[_Union[_workspace_instance_pb2.UpdateEvent, _Mapping]] = ..., stop_event: _Optional[_Union[_workspace_instance_pb2.StopEvent, _Mapping]] = ..., stopping_event: _Optional[_Union[_workspace_instance_pb2.StoppingEvent, _Mapping]] = ...) -> None: ...

class StopWorkspaceInstanceRequest(_message.Message):
    __slots__ = ["id", "cause"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CAUSE_FIELD_NUMBER: _ClassVar[int]
    id: _workspace_instance_pb2.WorkspaceInstanceIdentifier
    cause: str
    def __init__(self, id: _Optional[_Union[_workspace_instance_pb2.WorkspaceInstanceIdentifier, _Mapping]] = ..., cause: _Optional[str] = ...) -> None: ...

class StopWorkspaceInstanceResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
