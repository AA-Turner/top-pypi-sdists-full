from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DatabaseSourceReference(_message.Message):
    __slots__ = ("source_type", "name")
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    source_type: str
    name: str
    def __init__(self, source_type: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class DatabaseSource(_message.Message):
    __slots__ = ("source_type", "name", "options")
    class OptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    source_type: str
    name: str
    options: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        source_type: _Optional[str] = ...,
        name: _Optional[str] = ...,
        options: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...

class DatabaseSourceGroup(_message.Message):
    __slots__ = ("name", "default_source", "tagged_sources")
    class TaggedSourcesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: DatabaseSourceReference
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[DatabaseSourceReference, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    TAGGED_SOURCES_FIELD_NUMBER: _ClassVar[int]
    name: str
    default_source: DatabaseSourceReference
    tagged_sources: _containers.MessageMap[str, DatabaseSourceReference]
    def __init__(
        self,
        name: _Optional[str] = ...,
        default_source: _Optional[_Union[DatabaseSourceReference, _Mapping]] = ...,
        tagged_sources: _Optional[_Mapping[str, DatabaseSourceReference]] = ...,
    ) -> None: ...

class StreamSourceReference(_message.Message):
    __slots__ = ("source_type", "name")
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    source_type: str
    name: str
    def __init__(self, source_type: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class StreamSource(_message.Message):
    __slots__ = ("source_type", "name", "options")
    class OptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    source_type: str
    name: str
    options: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        source_type: _Optional[str] = ...,
        name: _Optional[str] = ...,
        options: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...

class SourceSecrets(_message.Message):
    __slots__ = ("secrets",)
    class SecretsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    SECRETS_FIELD_NUMBER: _ClassVar[int]
    secrets: _containers.ScalarMap[str, str]
    def __init__(self, secrets: _Optional[_Mapping[str, str]] = ...) -> None: ...
