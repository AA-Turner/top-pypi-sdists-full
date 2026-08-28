from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from chalk._gen.chalk.graph.v1 import source_file_reference_pb2 as _source_file_reference_pb2
from chalk._gen.chalk.graph.v1 import sql_resolver_retry_policy_pb2 as _sql_resolver_retry_policy_pb2
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

class GetAllNamedQueriesRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class GetNamedQueryByNameRequest(_message.Message):
    __slots__ = ("name", "query_version")
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    query_version: str
    def __init__(self, name: _Optional[str] = ..., query_version: _Optional[str] = ...) -> None: ...

class GetNamedQueryByNameResponse(_message.Message):
    __slots__ = ("named_queries",)
    NAMED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    named_queries: _containers.RepeatedCompositeFieldContainer[_graph_pb2.NamedQuery]
    def __init__(self, named_queries: _Optional[_Iterable[_Union[_graph_pb2.NamedQuery, _Mapping]]] = ...) -> None: ...

class GetAllNamedQueriesResponse(_message.Message):
    __slots__ = ("named_queries",)
    NAMED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    named_queries: _containers.RepeatedCompositeFieldContainer[_graph_pb2.NamedQuery]
    def __init__(self, named_queries: _Optional[_Iterable[_Union[_graph_pb2.NamedQuery, _Mapping]]] = ...) -> None: ...

class GetAllNamedQueriesActiveDeploymentRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAllNamedQueriesActiveDeploymentResponse(_message.Message):
    __slots__ = ("named_queries",)
    NAMED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    named_queries: _containers.RepeatedCompositeFieldContainer[_graph_pb2.NamedQuery]
    def __init__(self, named_queries: _Optional[_Iterable[_Union[_graph_pb2.NamedQuery, _Mapping]]] = ...) -> None: ...

class NamedQuerySummary(_message.Message):
    __slots__ = (
        "name",
        "is_code_defined",
        "version_count",
        "meta_query_count",
        "input_count",
        "output_count",
        "tags",
        "owner",
        "created_at",
        "last_executed_at",
        "latest_version",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_CODE_DEFINED_FIELD_NUMBER: _ClassVar[int]
    VERSION_COUNT_FIELD_NUMBER: _ClassVar[int]
    META_QUERY_COUNT_FIELD_NUMBER: _ClassVar[int]
    INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_EXECUTED_AT_FIELD_NUMBER: _ClassVar[int]
    LATEST_VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    is_code_defined: bool
    version_count: int
    meta_query_count: int
    input_count: int
    output_count: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    owner: str
    created_at: _timestamp_pb2.Timestamp
    last_executed_at: _timestamp_pb2.Timestamp
    latest_version: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        is_code_defined: bool = ...,
        version_count: _Optional[int] = ...,
        meta_query_count: _Optional[int] = ...,
        input_count: _Optional[int] = ...,
        output_count: _Optional[int] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        owner: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_executed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        latest_version: _Optional[str] = ...,
    ) -> None: ...

class NamedQueriesExecutedZoneCursor(_message.Message):
    __slots__ = ("last_executed_at", "name")
    LAST_EXECUTED_AT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    last_executed_at: _timestamp_pb2.Timestamp
    name: str
    def __init__(
        self, last_executed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., name: _Optional[str] = ...
    ) -> None: ...

class NamedQueriesUnexecutedZoneCursor(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ListAllNamedQueriesPageToken(_message.Message):
    __slots__ = ("executed", "unexecuted")
    EXECUTED_FIELD_NUMBER: _ClassVar[int]
    UNEXECUTED_FIELD_NUMBER: _ClassVar[int]
    executed: NamedQueriesExecutedZoneCursor
    unexecuted: NamedQueriesUnexecutedZoneCursor
    def __init__(
        self,
        executed: _Optional[_Union[NamedQueriesExecutedZoneCursor, _Mapping]] = ...,
        unexecuted: _Optional[_Union[NamedQueriesUnexecutedZoneCursor, _Mapping]] = ...,
    ) -> None: ...

class ListAllNamedQueriesRequest(_message.Message):
    __slots__ = ("page_size", "page_token", "name_prefix")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    NAME_PREFIX_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    name_prefix: str
    def __init__(
        self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., name_prefix: _Optional[str] = ...
    ) -> None: ...

class ListAllNamedQueriesResponse(_message.Message):
    __slots__ = ("named_queries", "next_page_token", "total_count")
    NAMED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    named_queries: _containers.RepeatedCompositeFieldContainer[NamedQuerySummary]
    next_page_token: str
    total_count: int
    def __init__(
        self,
        named_queries: _Optional[_Iterable[_Union[NamedQuerySummary, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
        total_count: _Optional[int] = ...,
    ) -> None: ...

class NamedQueryVersionSummary(_message.Message):
    __slots__ = (
        "query_version",
        "is_code_defined",
        "meta_query_count",
        "last_executed_at",
        "first_executed_at",
        "first_deployed",
        "last_deployed",
        "first_deployment_id",
        "last_deployment_id",
    )
    QUERY_VERSION_FIELD_NUMBER: _ClassVar[int]
    IS_CODE_DEFINED_FIELD_NUMBER: _ClassVar[int]
    META_QUERY_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_EXECUTED_AT_FIELD_NUMBER: _ClassVar[int]
    FIRST_EXECUTED_AT_FIELD_NUMBER: _ClassVar[int]
    FIRST_DEPLOYED_FIELD_NUMBER: _ClassVar[int]
    LAST_DEPLOYED_FIELD_NUMBER: _ClassVar[int]
    FIRST_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    query_version: str
    is_code_defined: bool
    meta_query_count: int
    last_executed_at: _timestamp_pb2.Timestamp
    first_executed_at: _timestamp_pb2.Timestamp
    first_deployed: _timestamp_pb2.Timestamp
    last_deployed: _timestamp_pb2.Timestamp
    first_deployment_id: str
    last_deployment_id: str
    def __init__(
        self,
        query_version: _Optional[str] = ...,
        is_code_defined: bool = ...,
        meta_query_count: _Optional[int] = ...,
        last_executed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        first_executed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        first_deployed: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_deployed: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        first_deployment_id: _Optional[str] = ...,
        last_deployment_id: _Optional[str] = ...,
    ) -> None: ...

class ListNamedQueryVersionsRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ListNamedQueryVersionsResponse(_message.Message):
    __slots__ = ("versions",)
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    versions: _containers.RepeatedCompositeFieldContainer[NamedQueryVersionSummary]
    def __init__(self, versions: _Optional[_Iterable[_Union[NamedQueryVersionSummary, _Mapping]]] = ...) -> None: ...
