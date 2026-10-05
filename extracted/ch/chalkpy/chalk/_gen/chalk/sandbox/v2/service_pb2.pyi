from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.container.v1 import service_pb2 as _service_pb2
from chalk._gen.chalk.flags.v1 import flags_pb2 as _flags_pb2
from google.protobuf import duration_pb2 as _duration_pb2
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

class SandboxStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SANDBOX_STATUS_UNSPECIFIED: _ClassVar[SandboxStatus]
    SANDBOX_STATUS_PENDING: _ClassVar[SandboxStatus]
    SANDBOX_STATUS_RUNNING: _ClassVar[SandboxStatus]
    SANDBOX_STATUS_SUCCEEDED: _ClassVar[SandboxStatus]
    SANDBOX_STATUS_FAILED: _ClassVar[SandboxStatus]
    SANDBOX_STATUS_TERMINATED: _ClassVar[SandboxStatus]
    SANDBOX_STATUS_ERROR: _ClassVar[SandboxStatus]
    SANDBOX_STATUS_UNKNOWN: _ClassVar[SandboxStatus]
    SANDBOX_STATUS_SUSPENDED: _ClassVar[SandboxStatus]

class SandboxSortColumn(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SANDBOX_SORT_COLUMN_UNSPECIFIED: _ClassVar[SandboxSortColumn]
    SANDBOX_SORT_COLUMN_CREATED_AT: _ClassVar[SandboxSortColumn]

class SandboxSortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SANDBOX_SORT_ORDER_UNSPECIFIED: _ClassVar[SandboxSortOrder]
    SANDBOX_SORT_ORDER_DESC: _ClassVar[SandboxSortOrder]
    SANDBOX_SORT_ORDER_ASC: _ClassVar[SandboxSortOrder]

class SandboxResourceKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SANDBOX_RESOURCE_KIND_UNSPECIFIED: _ClassVar[SandboxResourceKind]
    SANDBOX_RESOURCE_KIND_NOTEBOOK: _ClassVar[SandboxResourceKind]
    SANDBOX_RESOURCE_KIND_CHALKCOMPUTE_FUNCTION: _ClassVar[SandboxResourceKind]
    SANDBOX_RESOURCE_KIND_ONLINE_QUERY: _ClassVar[SandboxResourceKind]
    SANDBOX_RESOURCE_KIND_OFFLINE_QUERY: _ClassVar[SandboxResourceKind]
    SANDBOX_RESOURCE_KIND_SQL_QUERY: _ClassVar[SandboxResourceKind]
    SANDBOX_RESOURCE_KIND_STORED_ARTIFACT: _ClassVar[SandboxResourceKind]
    SANDBOX_RESOURCE_KIND_GITHUB_PR: _ClassVar[SandboxResourceKind]

SANDBOX_STATUS_UNSPECIFIED: SandboxStatus
SANDBOX_STATUS_PENDING: SandboxStatus
SANDBOX_STATUS_RUNNING: SandboxStatus
SANDBOX_STATUS_SUCCEEDED: SandboxStatus
SANDBOX_STATUS_FAILED: SandboxStatus
SANDBOX_STATUS_TERMINATED: SandboxStatus
SANDBOX_STATUS_ERROR: SandboxStatus
SANDBOX_STATUS_UNKNOWN: SandboxStatus
SANDBOX_STATUS_SUSPENDED: SandboxStatus
SANDBOX_SORT_COLUMN_UNSPECIFIED: SandboxSortColumn
SANDBOX_SORT_COLUMN_CREATED_AT: SandboxSortColumn
SANDBOX_SORT_ORDER_UNSPECIFIED: SandboxSortOrder
SANDBOX_SORT_ORDER_DESC: SandboxSortOrder
SANDBOX_SORT_ORDER_ASC: SandboxSortOrder
SANDBOX_RESOURCE_KIND_UNSPECIFIED: SandboxResourceKind
SANDBOX_RESOURCE_KIND_NOTEBOOK: SandboxResourceKind
SANDBOX_RESOURCE_KIND_CHALKCOMPUTE_FUNCTION: SandboxResourceKind
SANDBOX_RESOURCE_KIND_ONLINE_QUERY: SandboxResourceKind
SANDBOX_RESOURCE_KIND_OFFLINE_QUERY: SandboxResourceKind
SANDBOX_RESOURCE_KIND_SQL_QUERY: SandboxResourceKind
SANDBOX_RESOURCE_KIND_STORED_ARTIFACT: SandboxResourceKind
SANDBOX_RESOURCE_KIND_GITHUB_PR: SandboxResourceKind

class SandboxInfo(_message.Message):
    __slots__ = (
        "id",
        "name",
        "status",
        "status_message",
        "spec",
        "created_at",
        "finished_at",
        "web_url",
        "region",
        "created_by",
        "status_details",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    WEB_URL_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    status: SandboxStatus
    status_message: str
    spec: _service_pb2.ChalkContainerSpec
    created_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    web_url: str
    region: str
    created_by: str
    status_details: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        status: _Optional[_Union[SandboxStatus, str]] = ...,
        status_message: _Optional[str] = ...,
        spec: _Optional[_Union[_service_pb2.ChalkContainerSpec, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finished_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        web_url: _Optional[str] = ...,
        region: _Optional[str] = ...,
        created_by: _Optional[str] = ...,
        status_details: _Optional[str] = ...,
    ) -> None: ...

class CreateSandboxRequest(_message.Message):
    __slots__ = ("spec", "snapshot_id")
    SPEC_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_ID_FIELD_NUMBER: _ClassVar[int]
    spec: _service_pb2.ChalkContainerSpec
    snapshot_id: str
    def __init__(
        self,
        spec: _Optional[_Union[_service_pb2.ChalkContainerSpec, _Mapping]] = ...,
        snapshot_id: _Optional[str] = ...,
    ) -> None: ...

class CreateSandboxResponse(_message.Message):
    __slots__ = ("sandbox",)
    SANDBOX_FIELD_NUMBER: _ClassVar[int]
    sandbox: SandboxInfo
    def __init__(self, sandbox: _Optional[_Union[SandboxInfo, _Mapping]] = ...) -> None: ...

class GetSandboxRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSandboxResponse(_message.Message):
    __slots__ = ("sandbox",)
    SANDBOX_FIELD_NUMBER: _ClassVar[int]
    sandbox: SandboxInfo
    def __init__(self, sandbox: _Optional[_Union[SandboxInfo, _Mapping]] = ...) -> None: ...

class ListSandboxesFilters(_message.Message):
    __slots__ = ("names", "statuses", "images", "created_by")
    NAMES_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    statuses: _containers.RepeatedScalarFieldContainer[SandboxStatus]
    images: _containers.RepeatedScalarFieldContainer[str]
    created_by: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        names: _Optional[_Iterable[str]] = ...,
        statuses: _Optional[_Iterable[_Union[SandboxStatus, str]]] = ...,
        images: _Optional[_Iterable[str]] = ...,
        created_by: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class ListSandboxesRequest(_message.Message):
    __slots__ = ("limit", "cursor", "search", "filters", "sort_column", "sort_order")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    SORT_COLUMN_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    search: str
    filters: ListSandboxesFilters
    sort_column: SandboxSortColumn
    sort_order: SandboxSortOrder
    def __init__(
        self,
        limit: _Optional[int] = ...,
        cursor: _Optional[str] = ...,
        search: _Optional[str] = ...,
        filters: _Optional[_Union[ListSandboxesFilters, _Mapping]] = ...,
        sort_column: _Optional[_Union[SandboxSortColumn, str]] = ...,
        sort_order: _Optional[_Union[SandboxSortOrder, str]] = ...,
    ) -> None: ...

class ListSandboxesResponse(_message.Message):
    __slots__ = ("sandboxes", "next_cursor")
    SANDBOXES_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    sandboxes: _containers.RepeatedCompositeFieldContainer[SandboxInfo]
    next_cursor: str
    def __init__(
        self, sandboxes: _Optional[_Iterable[_Union[SandboxInfo, _Mapping]]] = ..., next_cursor: _Optional[str] = ...
    ) -> None: ...

class SuspendSandboxRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class SuspendSandboxResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResumeSandboxRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ResumeSandboxResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TerminateSandboxRequest(_message.Message):
    __slots__ = ("id", "grace_period")
    ID_FIELD_NUMBER: _ClassVar[int]
    GRACE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    id: str
    grace_period: _duration_pb2.Duration
    def __init__(
        self, id: _Optional[str] = ..., grace_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...
    ) -> None: ...

class TerminateSandboxResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SandboxResource(_message.Message):
    __slots__ = ("id", "sandbox_id", "kind", "resource_id", "version_id", "created_at", "agent_id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    SANDBOX_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    sandbox_id: str
    kind: SandboxResourceKind
    resource_id: str
    version_id: str
    created_at: _timestamp_pb2.Timestamp
    agent_id: str
    name: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        sandbox_id: _Optional[str] = ...,
        kind: _Optional[_Union[SandboxResourceKind, str]] = ...,
        resource_id: _Optional[str] = ...,
        version_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        agent_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
    ) -> None: ...

class ListSandboxResourcesFilters(_message.Message):
    __slots__ = ("kinds", "resource_ids", "created_after", "created_before")
    KINDS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AFTER_FIELD_NUMBER: _ClassVar[int]
    CREATED_BEFORE_FIELD_NUMBER: _ClassVar[int]
    kinds: _containers.RepeatedScalarFieldContainer[SandboxResourceKind]
    resource_ids: _containers.RepeatedScalarFieldContainer[str]
    created_after: _timestamp_pb2.Timestamp
    created_before: _timestamp_pb2.Timestamp
    def __init__(
        self,
        kinds: _Optional[_Iterable[_Union[SandboxResourceKind, str]]] = ...,
        resource_ids: _Optional[_Iterable[str]] = ...,
        created_after: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        created_before: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListSandboxResourcesRequest(_message.Message):
    __slots__ = ("sandbox_id", "filters", "page_size", "page_token")
    SANDBOX_ID_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    sandbox_id: str
    filters: ListSandboxResourcesFilters
    page_size: int
    page_token: str
    def __init__(
        self,
        sandbox_id: _Optional[str] = ...,
        filters: _Optional[_Union[ListSandboxResourcesFilters, _Mapping]] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
    ) -> None: ...

class ListSandboxResourcesResponse(_message.Message):
    __slots__ = ("resources", "next_page_token")
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.RepeatedCompositeFieldContainer[SandboxResource]
    next_page_token: str
    def __init__(
        self,
        resources: _Optional[_Iterable[_Union[SandboxResource, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...

class RecordSandboxResourceRequest(_message.Message):
    __slots__ = ("kind", "resource_id", "version_id")
    KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    kind: SandboxResourceKind
    resource_id: str
    version_id: str
    def __init__(
        self,
        kind: _Optional[_Union[SandboxResourceKind, str]] = ...,
        resource_id: _Optional[str] = ...,
        version_id: _Optional[str] = ...,
    ) -> None: ...

class RecordSandboxResourceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
