from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.common import analytics_options__client_pb2 as _analytics_options__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BasicInfo(_message.Message):
    __slots__ = ["description", "name", "owner", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    description: str
    name: str
    owner: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., owner: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...
