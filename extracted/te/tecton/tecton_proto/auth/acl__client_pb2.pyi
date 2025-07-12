from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Acl(_message.Message):
    __slots__ = ["api_key_ids", "api_key_str_ids", "okta_ids", "permission"]
    API_KEY_IDS_FIELD_NUMBER: _ClassVar[int]
    API_KEY_STR_IDS_FIELD_NUMBER: _ClassVar[int]
    OKTA_IDS_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    api_key_ids: _containers.RepeatedCompositeFieldContainer[_id__client_pb2.Id]
    api_key_str_ids: _containers.RepeatedScalarFieldContainer[str]
    okta_ids: _containers.RepeatedScalarFieldContainer[str]
    permission: str
    def __init__(self, permission: _Optional[str] = ..., okta_ids: _Optional[_Iterable[str]] = ..., api_key_ids: _Optional[_Iterable[_Union[_id__client_pb2.Id, _Mapping]]] = ..., api_key_str_ids: _Optional[_Iterable[str]] = ...) -> None: ...
