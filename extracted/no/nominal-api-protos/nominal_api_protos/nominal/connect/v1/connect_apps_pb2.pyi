from buf.validate import validate_pb2 as _validate_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.types import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateConnectAppRequest(_message.Message):
    __slots__ = ("title", "description", "labels", "properties", "is_published", "workspace", "s3_path")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    S3_PATH_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.ScalarMap[str, str]
    is_published: bool
    workspace: str
    s3_path: _types_pb2.Handle
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., is_published: bool = ..., workspace: _Optional[str] = ..., s3_path: _Optional[_Union[_types_pb2.Handle, _Mapping]] = ...) -> None: ...

class UpdateConnectAppMetadataRequest(_message.Message):
    __slots__ = ("rid", "description", "labels", "properties", "is_archived", "is_published")
    RID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    rid: str
    description: str
    labels: _types_pb2.LabelUpdateWrapper
    properties: _types_pb2.PropertyUpdateWrapper
    is_archived: bool
    is_published: bool
    def __init__(self, rid: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Union[_types_pb2.LabelUpdateWrapper, _Mapping]] = ..., properties: _Optional[_Union[_types_pb2.PropertyUpdateWrapper, _Mapping]] = ..., is_archived: bool = ..., is_published: bool = ...) -> None: ...

class ConnectAppCommitMetadata(_message.Message):
    __slots__ = ("title", "contains_experimental_features")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTAINS_EXPERIMENTAL_FEATURES_FIELD_NUMBER: _ClassVar[int]
    title: str
    contains_experimental_features: bool
    def __init__(self, title: _Optional[str] = ..., contains_experimental_features: bool = ...) -> None: ...

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
