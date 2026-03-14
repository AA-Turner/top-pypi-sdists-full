from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal_api_protos.nominal.types.time import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteDataRequest(_message.Message):
    __slots__ = ("data_source_rid", "time_range", "tags", "channel_names", "delete_metadata")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DATA_SOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_NAMES_FIELD_NUMBER: _ClassVar[int]
    DELETE_METADATA_FIELD_NUMBER: _ClassVar[int]
    data_source_rid: str
    time_range: _time_pb2.Range
    tags: _containers.ScalarMap[str, str]
    channel_names: _containers.RepeatedScalarFieldContainer[str]
    delete_metadata: bool
    def __init__(self, data_source_rid: _Optional[str] = ..., time_range: _Optional[_Union[_time_pb2.Range, _Mapping]] = ..., tags: _Optional[_Mapping[str, str]] = ..., channel_names: _Optional[_Iterable[str]] = ..., delete_metadata: bool = ...) -> None: ...

class DeleteDataResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ChannelWithTags(_message.Message):
    __slots__ = ("channel", "tags")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    channel: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, channel: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class DeleteChannelWithTagsRequest(_message.Message):
    __slots__ = ("data_source_rid", "channel", "tags", "apply")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DATA_SOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    APPLY_FIELD_NUMBER: _ClassVar[int]
    data_source_rid: str
    channel: str
    tags: _containers.ScalarMap[str, str]
    apply: bool
    def __init__(self, data_source_rid: _Optional[str] = ..., channel: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ..., apply: bool = ...) -> None: ...

class DeleteChannelWithTagsResponse(_message.Message):
    __slots__ = ("channel_with_tags",)
    CHANNEL_WITH_TAGS_FIELD_NUMBER: _ClassVar[int]
    channel_with_tags: _containers.RepeatedCompositeFieldContainer[ChannelWithTags]
    def __init__(self, channel_with_tags: _Optional[_Iterable[_Union[ChannelWithTags, _Mapping]]] = ...) -> None: ...

class UndeleteChannelWithTagsRequest(_message.Message):
    __slots__ = ("data_source_rid", "channel_with_tags")
    DATA_SOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_WITH_TAGS_FIELD_NUMBER: _ClassVar[int]
    data_source_rid: str
    channel_with_tags: _containers.RepeatedCompositeFieldContainer[ChannelWithTags]
    def __init__(self, data_source_rid: _Optional[str] = ..., channel_with_tags: _Optional[_Iterable[_Union[ChannelWithTags, _Mapping]]] = ...) -> None: ...

class UndeleteChannelWithTagsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
