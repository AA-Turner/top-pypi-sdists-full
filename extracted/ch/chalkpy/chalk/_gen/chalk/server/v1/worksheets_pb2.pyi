from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import offline_query_pb2 as _offline_query_pb2
from chalk._gen.chalk.common.v1 import online_query_pb2 as _online_query_pb2
from chalk._gen.chalk.protosql.v1 import sql_service_pb2 as _sql_service_pb2
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

class WorksheetSpaceVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKSHEET_SPACE_VISIBILITY_UNSPECIFIED: _ClassVar[WorksheetSpaceVisibility]
    WORKSHEET_SPACE_VISIBILITY_SHARED: _ClassVar[WorksheetSpaceVisibility]
    WORKSHEET_SPACE_VISIBILITY_PRIVATE: _ClassVar[WorksheetSpaceVisibility]

class WorksheetNodeKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKSHEET_NODE_KIND_UNSPECIFIED: _ClassVar[WorksheetNodeKind]
    WORKSHEET_NODE_KIND_FOLDER: _ClassVar[WorksheetNodeKind]
    WORKSHEET_NODE_KIND_SQL_QUERY: _ClassVar[WorksheetNodeKind]
    WORKSHEET_NODE_KIND_ONLINE_QUERY: _ClassVar[WorksheetNodeKind]
    WORKSHEET_NODE_KIND_OFFLINE_QUERY: _ClassVar[WorksheetNodeKind]
    WORKSHEET_NODE_KIND_NOTEBOOK: _ClassVar[WorksheetNodeKind]

class WorksheetNodeState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKSHEET_NODE_STATE_UNSPECIFIED: _ClassVar[WorksheetNodeState]
    WORKSHEET_NODE_STATE_ACTIVE: _ClassVar[WorksheetNodeState]
    WORKSHEET_NODE_STATE_ARCHIVED: _ClassVar[WorksheetNodeState]

class WorksheetCommitState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKSHEET_COMMIT_STATE_UNSPECIFIED: _ClassVar[WorksheetCommitState]
    WORKSHEET_COMMIT_STATE_DRAFT: _ClassVar[WorksheetCommitState]
    WORKSHEET_COMMIT_STATE_SAVED: _ClassVar[WorksheetCommitState]

class WorksheetOperationKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKSHEET_OPERATION_KIND_UNSPECIFIED: _ClassVar[WorksheetOperationKind]
    WORKSHEET_OPERATION_KIND_AUTOSAVE: _ClassVar[WorksheetOperationKind]
    WORKSHEET_OPERATION_KIND_CREATE: _ClassVar[WorksheetOperationKind]
    WORKSHEET_OPERATION_KIND_SAVE: _ClassVar[WorksheetOperationKind]
    WORKSHEET_OPERATION_KIND_RENAME: _ClassVar[WorksheetOperationKind]
    WORKSHEET_OPERATION_KIND_MOVE: _ClassVar[WorksheetOperationKind]
    WORKSHEET_OPERATION_KIND_ARCHIVE: _ClassVar[WorksheetOperationKind]
    WORKSHEET_OPERATION_KIND_RESTORE: _ClassVar[WorksheetOperationKind]
    WORKSHEET_OPERATION_KIND_DUPLICATE: _ClassVar[WorksheetOperationKind]

WORKSHEET_SPACE_VISIBILITY_UNSPECIFIED: WorksheetSpaceVisibility
WORKSHEET_SPACE_VISIBILITY_SHARED: WorksheetSpaceVisibility
WORKSHEET_SPACE_VISIBILITY_PRIVATE: WorksheetSpaceVisibility
WORKSHEET_NODE_KIND_UNSPECIFIED: WorksheetNodeKind
WORKSHEET_NODE_KIND_FOLDER: WorksheetNodeKind
WORKSHEET_NODE_KIND_SQL_QUERY: WorksheetNodeKind
WORKSHEET_NODE_KIND_ONLINE_QUERY: WorksheetNodeKind
WORKSHEET_NODE_KIND_OFFLINE_QUERY: WorksheetNodeKind
WORKSHEET_NODE_KIND_NOTEBOOK: WorksheetNodeKind
WORKSHEET_NODE_STATE_UNSPECIFIED: WorksheetNodeState
WORKSHEET_NODE_STATE_ACTIVE: WorksheetNodeState
WORKSHEET_NODE_STATE_ARCHIVED: WorksheetNodeState
WORKSHEET_COMMIT_STATE_UNSPECIFIED: WorksheetCommitState
WORKSHEET_COMMIT_STATE_DRAFT: WorksheetCommitState
WORKSHEET_COMMIT_STATE_SAVED: WorksheetCommitState
WORKSHEET_OPERATION_KIND_UNSPECIFIED: WorksheetOperationKind
WORKSHEET_OPERATION_KIND_AUTOSAVE: WorksheetOperationKind
WORKSHEET_OPERATION_KIND_CREATE: WorksheetOperationKind
WORKSHEET_OPERATION_KIND_SAVE: WorksheetOperationKind
WORKSHEET_OPERATION_KIND_RENAME: WorksheetOperationKind
WORKSHEET_OPERATION_KIND_MOVE: WorksheetOperationKind
WORKSHEET_OPERATION_KIND_ARCHIVE: WorksheetOperationKind
WORKSHEET_OPERATION_KIND_RESTORE: WorksheetOperationKind
WORKSHEET_OPERATION_KIND_DUPLICATE: WorksheetOperationKind

class WorksheetSpace(_message.Message):
    __slots__ = ("id", "environment_id", "visibility", "owner_user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    OWNER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    visibility: WorksheetSpaceVisibility
    owner_user_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        visibility: _Optional[_Union[WorksheetSpaceVisibility, str]] = ...,
        owner_user_id: _Optional[str] = ...,
    ) -> None: ...

class WorksheetBlobRef(_message.Message):
    __slots__ = ("id", "environment_id", "content_schema", "content_hash", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    CONTENT_HASH_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    content_schema: str
    content_hash: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        content_schema: _Optional[str] = ...,
        content_hash: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class WorksheetContent(_message.Message):
    __slots__ = ("content_schema", "content_proto_bytes", "content_hash")
    CONTENT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    CONTENT_PROTO_BYTES_FIELD_NUMBER: _ClassVar[int]
    CONTENT_HASH_FIELD_NUMBER: _ClassVar[int]
    content_schema: str
    content_proto_bytes: bytes
    content_hash: str
    def __init__(
        self,
        content_schema: _Optional[str] = ...,
        content_proto_bytes: _Optional[bytes] = ...,
        content_hash: _Optional[str] = ...,
    ) -> None: ...

class WorksheetSqlQueryDocument(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _sql_service_pb2.ExecuteSqlQueryRequest
    def __init__(self, request: _Optional[_Union[_sql_service_pb2.ExecuteSqlQueryRequest, _Mapping]] = ...) -> None: ...

class WorksheetOnlineQueryDocument(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _online_query_pb2.OnlineQueryRequest
    def __init__(self, request: _Optional[_Union[_online_query_pb2.OnlineQueryRequest, _Mapping]] = ...) -> None: ...

class WorksheetOfflineQueryDocument(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _offline_query_pb2.OfflineQueryRequest
    def __init__(self, request: _Optional[_Union[_offline_query_pb2.OfflineQueryRequest, _Mapping]] = ...) -> None: ...

class WorksheetNotebookDocument(_message.Message):
    __slots__ = ("notebook_proto_bytes", "notebook_schema")
    NOTEBOOK_PROTO_BYTES_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    notebook_proto_bytes: bytes
    notebook_schema: str
    def __init__(self, notebook_proto_bytes: _Optional[bytes] = ..., notebook_schema: _Optional[str] = ...) -> None: ...

class WorksheetDocument(_message.Message):
    __slots__ = ("sql_query", "online_query", "offline_query", "notebook")
    SQL_QUERY_FIELD_NUMBER: _ClassVar[int]
    ONLINE_QUERY_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_QUERY_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_FIELD_NUMBER: _ClassVar[int]
    sql_query: WorksheetSqlQueryDocument
    online_query: WorksheetOnlineQueryDocument
    offline_query: WorksheetOfflineQueryDocument
    notebook: WorksheetNotebookDocument
    def __init__(
        self,
        sql_query: _Optional[_Union[WorksheetSqlQueryDocument, _Mapping]] = ...,
        online_query: _Optional[_Union[WorksheetOnlineQueryDocument, _Mapping]] = ...,
        offline_query: _Optional[_Union[WorksheetOfflineQueryDocument, _Mapping]] = ...,
        notebook: _Optional[_Union[WorksheetNotebookDocument, _Mapping]] = ...,
    ) -> None: ...

class WorksheetContentInput(_message.Message):
    __slots__ = ("raw_content", "document")
    RAW_CONTENT_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    raw_content: WorksheetContent
    document: WorksheetDocument
    def __init__(
        self,
        raw_content: _Optional[_Union[WorksheetContent, _Mapping]] = ...,
        document: _Optional[_Union[WorksheetDocument, _Mapping]] = ...,
    ) -> None: ...

class WorksheetNode(_message.Message):
    __slots__ = ("id", "space_id", "environment_id", "kind", "parent_node_id", "name", "state")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    PARENT_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    space_id: str
    environment_id: str
    kind: WorksheetNodeKind
    parent_node_id: str
    name: str
    state: WorksheetNodeState
    def __init__(
        self,
        id: _Optional[str] = ...,
        space_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        kind: _Optional[_Union[WorksheetNodeKind, str]] = ...,
        parent_node_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        state: _Optional[_Union[WorksheetNodeState, str]] = ...,
    ) -> None: ...

class WorksheetCommit(_message.Message):
    __slots__ = (
        "id",
        "space_id",
        "environment_id",
        "user_id",
        "created_at",
        "state",
        "operation_kind",
        "node_id",
        "parent_node_id",
        "name",
        "node_state",
        "blob_id",
        "blob",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_KIND_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_STATE_FIELD_NUMBER: _ClassVar[int]
    BLOB_ID_FIELD_NUMBER: _ClassVar[int]
    BLOB_FIELD_NUMBER: _ClassVar[int]
    id: int
    space_id: str
    environment_id: str
    user_id: str
    created_at: _timestamp_pb2.Timestamp
    state: WorksheetCommitState
    operation_kind: WorksheetOperationKind
    node_id: str
    parent_node_id: str
    name: str
    node_state: WorksheetNodeState
    blob_id: str
    blob: WorksheetBlobRef
    def __init__(
        self,
        id: _Optional[int] = ...,
        space_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        user_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        state: _Optional[_Union[WorksheetCommitState, str]] = ...,
        operation_kind: _Optional[_Union[WorksheetOperationKind, str]] = ...,
        node_id: _Optional[str] = ...,
        parent_node_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        node_state: _Optional[_Union[WorksheetNodeState, str]] = ...,
        blob_id: _Optional[str] = ...,
        blob: _Optional[_Union[WorksheetBlobRef, _Mapping]] = ...,
    ) -> None: ...

class CreateWorksheetSpaceRequest(_message.Message):
    __slots__ = ("visibility",)
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    visibility: WorksheetSpaceVisibility
    def __init__(self, visibility: _Optional[_Union[WorksheetSpaceVisibility, str]] = ...) -> None: ...

class CreateWorksheetSpaceResponse(_message.Message):
    __slots__ = ("space",)
    SPACE_FIELD_NUMBER: _ClassVar[int]
    space: WorksheetSpace
    def __init__(self, space: _Optional[_Union[WorksheetSpace, _Mapping]] = ...) -> None: ...

class ListWorksheetSpacesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListWorksheetSpacesResponse(_message.Message):
    __slots__ = ("spaces",)
    SPACES_FIELD_NUMBER: _ClassVar[int]
    spaces: _containers.RepeatedCompositeFieldContainer[WorksheetSpace]
    def __init__(self, spaces: _Optional[_Iterable[_Union[WorksheetSpace, _Mapping]]] = ...) -> None: ...

class GetWorksheetNodeRequest(_message.Message):
    __slots__ = ("node_id",)
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    def __init__(self, node_id: _Optional[str] = ...) -> None: ...

class GetWorksheetNodeResponse(_message.Message):
    __slots__ = ("node",)
    NODE_FIELD_NUMBER: _ClassVar[int]
    node: WorksheetNode
    def __init__(self, node: _Optional[_Union[WorksheetNode, _Mapping]] = ...) -> None: ...

class ListWorksheetNodesRequest(_message.Message):
    __slots__ = ("space_id", "parent_node_id", "include_archived")
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    space_id: str
    parent_node_id: str
    include_archived: bool
    def __init__(
        self, space_id: _Optional[str] = ..., parent_node_id: _Optional[str] = ..., include_archived: bool = ...
    ) -> None: ...

class ListWorksheetNodesResponse(_message.Message):
    __slots__ = ("nodes",)
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[WorksheetNode]
    def __init__(self, nodes: _Optional[_Iterable[_Union[WorksheetNode, _Mapping]]] = ...) -> None: ...

class CreateWorksheetNodeRequest(_message.Message):
    __slots__ = ("space_id", "kind", "parent_node_id", "name", "content")
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    PARENT_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    space_id: str
    kind: WorksheetNodeKind
    parent_node_id: str
    name: str
    content: WorksheetContentInput
    def __init__(
        self,
        space_id: _Optional[str] = ...,
        kind: _Optional[_Union[WorksheetNodeKind, str]] = ...,
        parent_node_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        content: _Optional[_Union[WorksheetContentInput, _Mapping]] = ...,
    ) -> None: ...

class CreateWorksheetNodeResponse(_message.Message):
    __slots__ = ("node", "commit")
    NODE_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    node: WorksheetNode
    commit: WorksheetCommit
    def __init__(
        self,
        node: _Optional[_Union[WorksheetNode, _Mapping]] = ...,
        commit: _Optional[_Union[WorksheetCommit, _Mapping]] = ...,
    ) -> None: ...

class RenameWorksheetNodeRequest(_message.Message):
    __slots__ = ("node_id", "name")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    name: str
    def __init__(self, node_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class RenameWorksheetNodeResponse(_message.Message):
    __slots__ = ("node", "commit")
    NODE_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    node: WorksheetNode
    commit: WorksheetCommit
    def __init__(
        self,
        node: _Optional[_Union[WorksheetNode, _Mapping]] = ...,
        commit: _Optional[_Union[WorksheetCommit, _Mapping]] = ...,
    ) -> None: ...

class MoveWorksheetNodeRequest(_message.Message):
    __slots__ = ("node_id", "parent_node_id", "space_id")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    parent_node_id: str
    space_id: str
    def __init__(
        self, node_id: _Optional[str] = ..., parent_node_id: _Optional[str] = ..., space_id: _Optional[str] = ...
    ) -> None: ...

class MoveWorksheetNodeResponse(_message.Message):
    __slots__ = ("node", "commit")
    NODE_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    node: WorksheetNode
    commit: WorksheetCommit
    def __init__(
        self,
        node: _Optional[_Union[WorksheetNode, _Mapping]] = ...,
        commit: _Optional[_Union[WorksheetCommit, _Mapping]] = ...,
    ) -> None: ...

class ArchiveWorksheetNodeRequest(_message.Message):
    __slots__ = ("node_id",)
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    def __init__(self, node_id: _Optional[str] = ...) -> None: ...

class ArchiveWorksheetNodeResponse(_message.Message):
    __slots__ = ("node", "commit")
    NODE_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    node: WorksheetNode
    commit: WorksheetCommit
    def __init__(
        self,
        node: _Optional[_Union[WorksheetNode, _Mapping]] = ...,
        commit: _Optional[_Union[WorksheetCommit, _Mapping]] = ...,
    ) -> None: ...

class RestoreWorksheetNodeRequest(_message.Message):
    __slots__ = ("node_id", "parent_node_id")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    parent_node_id: str
    def __init__(self, node_id: _Optional[str] = ..., parent_node_id: _Optional[str] = ...) -> None: ...

class RestoreWorksheetNodeResponse(_message.Message):
    __slots__ = ("node", "commit")
    NODE_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    node: WorksheetNode
    commit: WorksheetCommit
    def __init__(
        self,
        node: _Optional[_Union[WorksheetNode, _Mapping]] = ...,
        commit: _Optional[_Union[WorksheetCommit, _Mapping]] = ...,
    ) -> None: ...

class AutosaveWorksheetRequest(_message.Message):
    __slots__ = ("node_id", "content")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    content: WorksheetContentInput
    def __init__(
        self, node_id: _Optional[str] = ..., content: _Optional[_Union[WorksheetContentInput, _Mapping]] = ...
    ) -> None: ...

class AutosaveWorksheetResponse(_message.Message):
    __slots__ = ("commit",)
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    commit: WorksheetCommit
    def __init__(self, commit: _Optional[_Union[WorksheetCommit, _Mapping]] = ...) -> None: ...

class SaveWorksheetRequest(_message.Message):
    __slots__ = ("node_id", "content")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    content: WorksheetContentInput
    def __init__(
        self, node_id: _Optional[str] = ..., content: _Optional[_Union[WorksheetContentInput, _Mapping]] = ...
    ) -> None: ...

class SaveWorksheetResponse(_message.Message):
    __slots__ = ("commit",)
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    commit: WorksheetCommit
    def __init__(self, commit: _Optional[_Union[WorksheetCommit, _Mapping]] = ...) -> None: ...

class GetWorksheetCommitRequest(_message.Message):
    __slots__ = ("commit_id", "include_content")
    COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    commit_id: int
    include_content: bool
    def __init__(self, commit_id: _Optional[int] = ..., include_content: bool = ...) -> None: ...

class GetWorksheetCommitResponse(_message.Message):
    __slots__ = ("commit", "content")
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    commit: WorksheetCommit
    content: WorksheetContent
    def __init__(
        self,
        commit: _Optional[_Union[WorksheetCommit, _Mapping]] = ...,
        content: _Optional[_Union[WorksheetContent, _Mapping]] = ...,
    ) -> None: ...

class ListWorksheetCommitsRequest(_message.Message):
    __slots__ = ("node_id", "include_drafts", "before_commit_id", "limit")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DRAFTS_FIELD_NUMBER: _ClassVar[int]
    BEFORE_COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    include_drafts: bool
    before_commit_id: int
    limit: int
    def __init__(
        self,
        node_id: _Optional[str] = ...,
        include_drafts: bool = ...,
        before_commit_id: _Optional[int] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ListWorksheetCommitsResponse(_message.Message):
    __slots__ = ("commits",)
    COMMITS_FIELD_NUMBER: _ClassVar[int]
    commits: _containers.RepeatedCompositeFieldContainer[WorksheetCommit]
    def __init__(self, commits: _Optional[_Iterable[_Union[WorksheetCommit, _Mapping]]] = ...) -> None: ...
