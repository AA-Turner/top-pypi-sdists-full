import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from nominal.types import types_pb2 as _types_pb2
from nominal.versioning.v1 import versioning_pb2 as _versioning_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchConnectAppsSortField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEARCH_CONNECT_APPS_SORT_FIELD_UNSPECIFIED: _ClassVar[SearchConnectAppsSortField]
    SEARCH_CONNECT_APPS_SORT_FIELD_TITLE: _ClassVar[SearchConnectAppsSortField]
    SEARCH_CONNECT_APPS_SORT_FIELD_CREATED_AT: _ClassVar[SearchConnectAppsSortField]
    SEARCH_CONNECT_APPS_SORT_FIELD_DISPLAY_NAME: _ClassVar[SearchConnectAppsSortField]

class ConnectAppsServiceError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECT_APPS_SERVICE_ERROR_UNSPECIFIED: _ClassVar[ConnectAppsServiceError]
    CONNECT_APPS_SERVICE_ERROR_APP_NOT_FOUND: _ClassVar[ConnectAppsServiceError]
    CONNECT_APPS_SERVICE_ERROR_COMMIT_NOT_FOUND: _ClassVar[ConnectAppsServiceError]
    CONNECT_APPS_SERVICE_ERROR_CANNOT_COMMIT_TO_ARCHIVED_CONNECT_APP: _ClassVar[ConnectAppsServiceError]
    CONNECT_APPS_SERVICE_ERROR_INVALID_SEARCH_TOKEN: _ClassVar[ConnectAppsServiceError]
    CONNECT_APPS_SERVICE_ERROR_MISSING_BUNDLE: _ClassVar[ConnectAppsServiceError]
SEARCH_CONNECT_APPS_SORT_FIELD_UNSPECIFIED: SearchConnectAppsSortField
SEARCH_CONNECT_APPS_SORT_FIELD_TITLE: SearchConnectAppsSortField
SEARCH_CONNECT_APPS_SORT_FIELD_CREATED_AT: SearchConnectAppsSortField
SEARCH_CONNECT_APPS_SORT_FIELD_DISPLAY_NAME: SearchConnectAppsSortField
CONNECT_APPS_SERVICE_ERROR_UNSPECIFIED: ConnectAppsServiceError
CONNECT_APPS_SERVICE_ERROR_APP_NOT_FOUND: ConnectAppsServiceError
CONNECT_APPS_SERVICE_ERROR_COMMIT_NOT_FOUND: ConnectAppsServiceError
CONNECT_APPS_SERVICE_ERROR_CANNOT_COMMIT_TO_ARCHIVED_CONNECT_APP: ConnectAppsServiceError
CONNECT_APPS_SERVICE_ERROR_INVALID_SEARCH_TOKEN: ConnectAppsServiceError
CONNECT_APPS_SERVICE_ERROR_MISSING_BUNDLE: ConnectAppsServiceError

class CreateConnectAppRequest(_message.Message):
    __slots__ = ("display_name", "description", "labels", "properties", "is_published", "workspace", "bundle", "commit_message")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    description: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.ScalarMap[str, str]
    is_published: bool
    workspace: str
    bundle: ConnectAppBundle
    commit_message: str
    def __init__(self, display_name: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., is_published: bool = ..., workspace: _Optional[str] = ..., bundle: _Optional[_Union[ConnectAppBundle, _Mapping]] = ..., commit_message: _Optional[str] = ...) -> None: ...

class CreateConnectAppResponse(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: ConnectApp
    def __init__(self, app: _Optional[_Union[ConnectApp, _Mapping]] = ...) -> None: ...

class UpdateConnectAppMetadataRequest(_message.Message):
    __slots__ = ("rid", "display_name", "description", "labels", "properties", "is_archived", "is_published")
    RID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    rid: str
    display_name: str
    description: str
    labels: _types_pb2.LabelUpdateWrapper
    properties: _types_pb2.PropertyUpdateWrapper
    is_archived: bool
    is_published: bool
    def __init__(self, rid: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Union[_types_pb2.LabelUpdateWrapper, _Mapping]] = ..., properties: _Optional[_Union[_types_pb2.PropertyUpdateWrapper, _Mapping]] = ..., is_archived: bool = ..., is_published: bool = ...) -> None: ...

class ConnectAppBundle(_message.Message):
    __slots__ = ("s3_path", "metadata")
    S3_PATH_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    s3_path: _types_pb2.Handle
    metadata: ConnectAppBundleMetadata
    def __init__(self, s3_path: _Optional[_Union[_types_pb2.Handle, _Mapping]] = ..., metadata: _Optional[_Union[ConnectAppBundleMetadata, _Mapping]] = ...) -> None: ...

class ConnectAppBundleMetadata(_message.Message):
    __slots__ = ("title", "contains_experimental_features", "sha256_checksum", "connect_file_path")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTAINS_EXPERIMENTAL_FEATURES_FIELD_NUMBER: _ClassVar[int]
    SHA256_CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    CONNECT_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    title: str
    contains_experimental_features: bool
    sha256_checksum: str
    connect_file_path: str
    def __init__(self, title: _Optional[str] = ..., contains_experimental_features: bool = ..., sha256_checksum: _Optional[str] = ..., connect_file_path: _Optional[str] = ...) -> None: ...

class ConnectAppSearchQuery(_message.Message):
    __slots__ = ("search_text", "label", "property", "workspace", "is_archived")
    class ConnectAppSearchAndQuery(_message.Message):
        __slots__ = ("queries",)
        QUERIES_FIELD_NUMBER: _ClassVar[int]
        queries: _containers.RepeatedCompositeFieldContainer[ConnectAppSearchQuery]
        def __init__(self, queries: _Optional[_Iterable[_Union[ConnectAppSearchQuery, _Mapping]]] = ...) -> None: ...
    class ConnectAppSearchOrQuery(_message.Message):
        __slots__ = ("queries",)
        QUERIES_FIELD_NUMBER: _ClassVar[int]
        queries: _containers.RepeatedCompositeFieldContainer[ConnectAppSearchQuery]
        def __init__(self, queries: _Optional[_Iterable[_Union[ConnectAppSearchQuery, _Mapping]]] = ...) -> None: ...
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_FIELD_NUMBER: _ClassVar[int]
    AND_FIELD_NUMBER: _ClassVar[int]
    OR_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    label: str
    property: _types_pb2.Property
    workspace: str
    is_archived: bool
    def __init__(self, search_text: _Optional[str] = ..., label: _Optional[str] = ..., property: _Optional[_Union[_types_pb2.Property, _Mapping]] = ..., workspace: _Optional[str] = ..., is_archived: bool = ..., **kwargs) -> None: ...

class ConnectAppMetadata(_message.Message):
    __slots__ = ("rid", "display_name", "description", "labels", "properties", "is_archived", "is_published", "created_at", "created_by", "updated_at", "workspace")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    RID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    rid: str
    display_name: str
    description: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.ScalarMap[str, str]
    is_archived: bool
    is_published: bool
    created_at: _timestamp_pb2.Timestamp
    created_by: str
    updated_at: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, rid: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., is_archived: bool = ..., is_published: bool = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_by: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., workspace: _Optional[str] = ...) -> None: ...

class ConnectApp(_message.Message):
    __slots__ = ("rid", "commit", "metadata", "bundle", "version_number")
    RID_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_FIELD_NUMBER: _ClassVar[int]
    VERSION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    rid: str
    commit: str
    metadata: ConnectAppMetadata
    bundle: ConnectAppBundle
    version_number: int
    def __init__(self, rid: _Optional[str] = ..., commit: _Optional[str] = ..., metadata: _Optional[_Union[ConnectAppMetadata, _Mapping]] = ..., bundle: _Optional[_Union[ConnectAppBundle, _Mapping]] = ..., version_number: _Optional[int] = ...) -> None: ...

class GetConnectAppRequest(_message.Message):
    __slots__ = ("rid", "branch_or_commit")
    RID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_OR_COMMIT_FIELD_NUMBER: _ClassVar[int]
    rid: str
    branch_or_commit: _versioning_pb2.BranchOrCommit
    def __init__(self, rid: _Optional[str] = ..., branch_or_commit: _Optional[_Union[_versioning_pb2.BranchOrCommit, _Mapping]] = ...) -> None: ...

class GetConnectAppBundleDownloadUrlRequest(_message.Message):
    __slots__ = ("rid", "branch_or_commit")
    RID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_OR_COMMIT_FIELD_NUMBER: _ClassVar[int]
    rid: str
    branch_or_commit: _versioning_pb2.BranchOrCommit
    def __init__(self, rid: _Optional[str] = ..., branch_or_commit: _Optional[_Union[_versioning_pb2.BranchOrCommit, _Mapping]] = ...) -> None: ...

class GetConnectAppBundleDownloadUrlResponse(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class GetConnectAppResponse(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: ConnectApp
    def __init__(self, app: _Optional[_Union[ConnectApp, _Mapping]] = ...) -> None: ...

class UpdateConnectAppMetadataResponse(_message.Message):
    __slots__ = ("app_metadata",)
    APP_METADATA_FIELD_NUMBER: _ClassVar[int]
    app_metadata: ConnectAppMetadata
    def __init__(self, app_metadata: _Optional[_Union[ConnectAppMetadata, _Mapping]] = ...) -> None: ...

class CommitRequest(_message.Message):
    __slots__ = ("rid", "bundle", "message")
    RID_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    rid: str
    bundle: ConnectAppBundle
    message: str
    def __init__(self, rid: _Optional[str] = ..., bundle: _Optional[_Union[ConnectAppBundle, _Mapping]] = ..., message: _Optional[str] = ...) -> None: ...

class CommitResponse(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: ConnectApp
    def __init__(self, app: _Optional[_Union[ConnectApp, _Mapping]] = ...) -> None: ...

class SearchConnectAppsOptions(_message.Message):
    __slots__ = ("is_descending", "sort_field")
    IS_DESCENDING_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_FIELD_NUMBER: _ClassVar[int]
    is_descending: bool
    sort_field: SearchConnectAppsSortField
    def __init__(self, is_descending: bool = ..., sort_field: _Optional[_Union[SearchConnectAppsSortField, str]] = ...) -> None: ...

class SearchConnectAppsRequest(_message.Message):
    __slots__ = ("query", "options", "page_size", "next_page_token")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query: ConnectAppSearchQuery
    options: SearchConnectAppsOptions
    page_size: int
    next_page_token: str
    def __init__(self, query: _Optional[_Union[ConnectAppSearchQuery, _Mapping]] = ..., options: _Optional[_Union[SearchConnectAppsOptions, _Mapping]] = ..., page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class SearchConnectAppsResponse(_message.Message):
    __slots__ = ("app_metadata", "next_page_token")
    APP_METADATA_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    app_metadata: _containers.RepeatedCompositeFieldContainer[ConnectAppMetadata]
    next_page_token: str
    def __init__(self, app_metadata: _Optional[_Iterable[_Union[ConnectAppMetadata, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class ArchiveConnectAppsRequest(_message.Message):
    __slots__ = ("rids",)
    RIDS_FIELD_NUMBER: _ClassVar[int]
    rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, rids: _Optional[_Iterable[str]] = ...) -> None: ...

class UnarchiveConnectAppsRequest(_message.Message):
    __slots__ = ("rids",)
    RIDS_FIELD_NUMBER: _ClassVar[int]
    rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, rids: _Optional[_Iterable[str]] = ...) -> None: ...

class ArchiveConnectAppsResponse(_message.Message):
    __slots__ = ("rids",)
    RIDS_FIELD_NUMBER: _ClassVar[int]
    rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, rids: _Optional[_Iterable[str]] = ...) -> None: ...

class UnarchiveConnectAppsResponse(_message.Message):
    __slots__ = ("rids",)
    RIDS_FIELD_NUMBER: _ClassVar[int]
    rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, rids: _Optional[_Iterable[str]] = ...) -> None: ...
