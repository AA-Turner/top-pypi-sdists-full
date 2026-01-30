from chalk._gen.chalk.argo.v1 import workflow_pb2 as _workflow_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.flags.v1 import flags_pb2 as _flags_pb2
from google.protobuf.internal import containers as _containers
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

class ListMetadataArgoWorkflowsRequest(_message.Message):
    __slots__ = ("phase",)
    PHASE_FIELD_NUMBER: _ClassVar[int]
    phase: _workflow_pb2.ArgoWorkflowPhase
    def __init__(self, phase: _Optional[_Union[_workflow_pb2.ArgoWorkflowPhase, str]] = ...) -> None: ...

class ListMetadataArgoWorkflowsResponse(_message.Message):
    __slots__ = ("workflows",)
    WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    workflows: _containers.RepeatedCompositeFieldContainer[_workflow_pb2.ArgoWorkflow]
    def __init__(self, workflows: _Optional[_Iterable[_Union[_workflow_pb2.ArgoWorkflow, _Mapping]]] = ...) -> None: ...

class GetMetadataArgoWorkflowRequest(_message.Message):
    __slots__ = ("workflow_name",)
    WORKFLOW_NAME_FIELD_NUMBER: _ClassVar[int]
    workflow_name: str
    def __init__(self, workflow_name: _Optional[str] = ...) -> None: ...

class GetMetadataArgoWorkflowResponse(_message.Message):
    __slots__ = ("workflow",)
    WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    workflow: _workflow_pb2.ArgoWorkflow
    def __init__(self, workflow: _Optional[_Union[_workflow_pb2.ArgoWorkflow, _Mapping]] = ...) -> None: ...

class ResumeMetadataArgoWorkflowRequest(_message.Message):
    __slots__ = ("workflow_name", "node_name")
    WORKFLOW_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    workflow_name: str
    node_name: str
    def __init__(self, workflow_name: _Optional[str] = ..., node_name: _Optional[str] = ...) -> None: ...

class ResumeMetadataArgoWorkflowResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class StopMetadataArgoWorkflowRequest(_message.Message):
    __slots__ = ("workflow_name", "message")
    WORKFLOW_NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    workflow_name: str
    message: str
    def __init__(self, workflow_name: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class StopMetadataArgoWorkflowResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class GetMetadataArgoWorkflowLogsRequest(_message.Message):
    __slots__ = ("workflow_name", "node_name")
    WORKFLOW_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    workflow_name: str
    node_name: str
    def __init__(self, workflow_name: _Optional[str] = ..., node_name: _Optional[str] = ...) -> None: ...

class GetMetadataArgoWorkflowLogsResponse(_message.Message):
    __slots__ = ("pod_name", "node_name", "logs")
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    pod_name: str
    node_name: str
    logs: str
    def __init__(
        self, pod_name: _Optional[str] = ..., node_name: _Optional[str] = ..., logs: _Optional[str] = ...
    ) -> None: ...
