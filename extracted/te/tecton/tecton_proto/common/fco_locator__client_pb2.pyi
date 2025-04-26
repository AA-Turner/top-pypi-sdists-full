from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FcoLocator(_message.Message):
    __slots__ = ["id", "name", "workspace"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    id: _id__client_pb2.Id
    name: str
    workspace: str
    def __init__(self, name: _Optional[str] = ..., id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., workspace: _Optional[str] = ...) -> None: ...

class IdFcoLocator(_message.Message):
    __slots__ = ["id", "workspace", "workspace_state_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    id: _id__client_pb2.Id
    workspace: str
    workspace_state_id: _id__client_pb2.Id
    def __init__(self, id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., workspace: _Optional[str] = ..., workspace_state_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ...) -> None: ...
