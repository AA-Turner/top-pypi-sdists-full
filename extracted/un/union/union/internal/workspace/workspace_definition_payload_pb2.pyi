from union.internal.common import list_pb2 as _list_pb2
from flyteidl.admin import task_pb2 as _task_pb2
from union.internal.validate.validate import validate_pb2 as _validate_pb2
from union.internal.workspace import workspace_definition_pb2 as _workspace_definition_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateWorkspaceDefinitionRequest(_message.Message):
    __slots__ = ["id", "spec", "short_description", "workspace_spec", "create_workspace_definition_entity"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    SHORT_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATE_WORKSPACE_DEFINITION_ENTITY_FIELD_NUMBER: _ClassVar[int]
    id: _workspace_definition_pb2.WorkspaceDefinitionIdentifier
    spec: _task_pb2.TaskSpec
    short_description: str
    workspace_spec: _workspace_definition_pb2.WorkspaceDefinitionSpec
    create_workspace_definition_entity: bool
    def __init__(self, id: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinitionIdentifier, _Mapping]] = ..., spec: _Optional[_Union[_task_pb2.TaskSpec, _Mapping]] = ..., short_description: _Optional[str] = ..., workspace_spec: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinitionSpec, _Mapping]] = ..., create_workspace_definition_entity: bool = ...) -> None: ...

class CreateWorkspaceDefinitionResponse(_message.Message):
    __slots__ = ["workspace_definition"]
    WORKSPACE_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    workspace_definition: _workspace_definition_pb2.WorkspaceDefinition
    def __init__(self, workspace_definition: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinition, _Mapping]] = ...) -> None: ...

class GetWorkspaceDefinitionRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _workspace_definition_pb2.WorkspaceDefinitionIdentifier
    def __init__(self, id: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinitionIdentifier, _Mapping]] = ...) -> None: ...

class GetWorkspaceDefinitionResponse(_message.Message):
    __slots__ = ["workspace_definition"]
    WORKSPACE_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    workspace_definition: _workspace_definition_pb2.WorkspaceDefinition
    def __init__(self, workspace_definition: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinition, _Mapping]] = ...) -> None: ...

class UpdateWorkspaceDefinitionRequest(_message.Message):
    __slots__ = ["id", "spec", "state", "short_description", "workspace_spec"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SHORT_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_SPEC_FIELD_NUMBER: _ClassVar[int]
    id: _workspace_definition_pb2.WorkspaceDefinitionIdentifier
    spec: _task_pb2.TaskSpec
    state: _workspace_definition_pb2.WorkspaceDefinitionState
    short_description: str
    workspace_spec: _workspace_definition_pb2.WorkspaceDefinitionSpec
    def __init__(self, id: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinitionIdentifier, _Mapping]] = ..., spec: _Optional[_Union[_task_pb2.TaskSpec, _Mapping]] = ..., state: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinitionState, str]] = ..., short_description: _Optional[str] = ..., workspace_spec: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinitionSpec, _Mapping]] = ...) -> None: ...

class UpdateWorkspaceDefinitionResponse(_message.Message):
    __slots__ = ["workspace_definition"]
    WORKSPACE_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    workspace_definition: _workspace_definition_pb2.WorkspaceDefinition
    def __init__(self, workspace_definition: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinition, _Mapping]] = ...) -> None: ...

class ListWorkspaceDefinitionsRequest(_message.Message):
    __slots__ = ["org", "project", "domain", "name", "request"]
    ORG_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    org: str
    project: str
    domain: str
    name: str
    request: _list_pb2.ListRequest
    def __init__(self, org: _Optional[str] = ..., project: _Optional[str] = ..., domain: _Optional[str] = ..., name: _Optional[str] = ..., request: _Optional[_Union[_list_pb2.ListRequest, _Mapping]] = ...) -> None: ...

class ListWorkspaceDefinitionsResponse(_message.Message):
    __slots__ = ["workspace_definitions", "token"]
    WORKSPACE_DEFINITIONS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    workspace_definitions: _containers.RepeatedCompositeFieldContainer[_workspace_definition_pb2.WorkspaceDefinition]
    token: str
    def __init__(self, workspace_definitions: _Optional[_Iterable[_Union[_workspace_definition_pb2.WorkspaceDefinition, _Mapping]]] = ..., token: _Optional[str] = ...) -> None: ...

class ListWorkspaceDefinitionEntitiesRequest(_message.Message):
    __slots__ = ["org", "project", "domain", "request"]
    ORG_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    org: str
    project: str
    domain: str
    request: _list_pb2.ListRequest
    def __init__(self, org: _Optional[str] = ..., project: _Optional[str] = ..., domain: _Optional[str] = ..., request: _Optional[_Union[_list_pb2.ListRequest, _Mapping]] = ...) -> None: ...

class ListWorkspaceDefinitionEntitiesResponse(_message.Message):
    __slots__ = ["workspace_definition_entities", "token"]
    WORKSPACE_DEFINITION_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    workspace_definition_entities: _containers.RepeatedCompositeFieldContainer[_workspace_definition_pb2.WorkspaceDefinitionEntity]
    token: str
    def __init__(self, workspace_definition_entities: _Optional[_Iterable[_Union[_workspace_definition_pb2.WorkspaceDefinitionEntity, _Mapping]]] = ..., token: _Optional[str] = ...) -> None: ...

class UpdateWorkspaceDefinitionEntityRequest(_message.Message):
    __slots__ = ["entity"]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    entity: _workspace_definition_pb2.WorkspaceDefinitionEntity
    def __init__(self, entity: _Optional[_Union[_workspace_definition_pb2.WorkspaceDefinitionEntity, _Mapping]] = ...) -> None: ...

class UpdateWorkspaceDefinitionEntityResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
