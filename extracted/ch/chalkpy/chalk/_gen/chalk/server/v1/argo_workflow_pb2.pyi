from chalk._gen.chalk.argo.v1 import workflow_pb2 as _workflow_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class ListArgoBuildsRequest(_message.Message):
    __slots__ = ("environment_id", "limit", "offset", "phase", "field_mask")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    PHASE_FIELD_NUMBER: _ClassVar[int]
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    limit: int
    offset: int
    phase: _workflow_pb2.ArgoWorkflowPhase
    field_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        offset: _Optional[int] = ...,
        phase: _Optional[_Union[_workflow_pb2.ArgoWorkflowPhase, str]] = ...,
        field_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class ListArgoBuildsResponse(_message.Message):
    __slots__ = ("builds", "total_count")
    BUILDS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    builds: _containers.RepeatedCompositeFieldContainer[_workflow_pb2.ArgoWorkflow]
    total_count: int
    def __init__(
        self,
        builds: _Optional[_Iterable[_Union[_workflow_pb2.ArgoWorkflow, _Mapping]]] = ...,
        total_count: _Optional[int] = ...,
    ) -> None: ...

class GetArgoBuildRequest(_message.Message):
    __slots__ = ("workflow_name",)
    WORKFLOW_NAME_FIELD_NUMBER: _ClassVar[int]
    workflow_name: str
    def __init__(self, workflow_name: _Optional[str] = ...) -> None: ...

class GetArgoBuildResponse(_message.Message):
    __slots__ = ("build",)
    BUILD_FIELD_NUMBER: _ClassVar[int]
    build: _workflow_pb2.ArgoWorkflow
    def __init__(self, build: _Optional[_Union[_workflow_pb2.ArgoWorkflow, _Mapping]] = ...) -> None: ...
