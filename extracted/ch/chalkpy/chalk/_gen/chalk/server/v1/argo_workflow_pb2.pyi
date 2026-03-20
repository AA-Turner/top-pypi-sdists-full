from chalk._gen.chalk.argo.v1 import workflow_pb2 as _workflow_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import kube_events_pb2 as _kube_events_pb2
from chalk._gen.chalk.server.v1 import log_pb2 as _log_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
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

class GetArgoBuildLogsRequest(_message.Message):
    __slots__ = ("workflow_name", "node_name", "start_time", "end_time", "limit", "page_token")
    WORKFLOW_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    workflow_name: str
    node_name: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    limit: int
    page_token: _log_pb2.SearchLogEntriesPageToken
    def __init__(
        self,
        workflow_name: _Optional[str] = ...,
        node_name: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        page_token: _Optional[_Union[_log_pb2.SearchLogEntriesPageToken, _Mapping]] = ...,
    ) -> None: ...

class GetArgoBuildLogsResponse(_message.Message):
    __slots__ = ("logs", "next_page_token")
    LOGS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[_log_pb2.LogEntry]
    next_page_token: _log_pb2.SearchLogEntriesPageToken
    def __init__(
        self,
        logs: _Optional[_Iterable[_Union[_log_pb2.LogEntry, _Mapping]]] = ...,
        next_page_token: _Optional[_Union[_log_pb2.SearchLogEntriesPageToken, _Mapping]] = ...,
    ) -> None: ...

class GetArgoBuildKubeEventsRequest(_message.Message):
    __slots__ = ("workflow_name", "node_name", "limit", "page_token")
    WORKFLOW_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    workflow_name: str
    node_name: str
    limit: int
    page_token: _kube_events_pb2.ListKubeEventsPageToken
    def __init__(
        self,
        workflow_name: _Optional[str] = ...,
        node_name: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        page_token: _Optional[_Union[_kube_events_pb2.ListKubeEventsPageToken, _Mapping]] = ...,
    ) -> None: ...

class GetArgoBuildKubeEventsResponse(_message.Message):
    __slots__ = ("events", "next_page_token")
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[_kube_events_pb2.KubeEvent]
    next_page_token: _kube_events_pb2.ListKubeEventsPageToken
    def __init__(
        self,
        events: _Optional[_Iterable[_Union[_kube_events_pb2.KubeEvent, _Mapping]]] = ...,
        next_page_token: _Optional[_Union[_kube_events_pb2.ListKubeEventsPageToken, _Mapping]] = ...,
    ) -> None: ...
