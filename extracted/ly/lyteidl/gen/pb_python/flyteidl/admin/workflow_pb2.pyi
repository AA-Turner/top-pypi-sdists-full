from flyteidl.core import compiler_pb2 as _compiler_pb2
from flyteidl.core import identifier_pb2 as _identifier_pb2
from flyteidl.core import workflow_pb2 as _workflow_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Workflow(_message.Message):
    __slots__ = ["closure", "id"]
    CLOSURE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    closure: WorkflowClosure
    id: _identifier_pb2.Identifier
    def __init__(self, id: _Optional[_Union[_identifier_pb2.Identifier, _Mapping]] = ..., closure: _Optional[_Union[WorkflowClosure, _Mapping]] = ...) -> None: ...

class WorkflowClosure(_message.Message):
    __slots__ = ["compiled_workflow", "created_at"]
    COMPILED_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    compiled_workflow: _compiler_pb2.CompiledWorkflowClosure
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, compiled_workflow: _Optional[_Union[_compiler_pb2.CompiledWorkflowClosure, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class WorkflowCreateRequest(_message.Message):
    __slots__ = ["id", "spec"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.Identifier
    spec: WorkflowSpec
    def __init__(self, id: _Optional[_Union[_identifier_pb2.Identifier, _Mapping]] = ..., spec: _Optional[_Union[WorkflowSpec, _Mapping]] = ...) -> None: ...

class WorkflowCreateResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class WorkflowList(_message.Message):
    __slots__ = ["token", "workflows"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    token: str
    workflows: _containers.RepeatedCompositeFieldContainer[Workflow]
    def __init__(self, workflows: _Optional[_Iterable[_Union[Workflow, _Mapping]]] = ..., token: _Optional[str] = ...) -> None: ...

class WorkflowSpec(_message.Message):
    __slots__ = ["sub_workflows", "template"]
    SUB_WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    sub_workflows: _containers.RepeatedCompositeFieldContainer[_workflow_pb2.WorkflowTemplate]
    template: _workflow_pb2.WorkflowTemplate
    def __init__(self, template: _Optional[_Union[_workflow_pb2.WorkflowTemplate, _Mapping]] = ..., sub_workflows: _Optional[_Iterable[_Union[_workflow_pb2.WorkflowTemplate, _Mapping]]] = ...) -> None: ...
