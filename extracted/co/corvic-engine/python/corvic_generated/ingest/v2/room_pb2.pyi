from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RoomEntry(_message.Message):
    __slots__ = ("id", "name", "user_id", "org_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    user_id: str
    org_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., user_id: _Optional[str] = ..., org_id: _Optional[str] = ...) -> None: ...

class CreateRoomRequest(_message.Message):
    __slots__ = ("name", "user_id", "org_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    user_id: str
    org_id: str
    def __init__(self, name: _Optional[str] = ..., user_id: _Optional[str] = ..., org_id: _Optional[str] = ...) -> None: ...

class CreateRoomResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: RoomEntry
    def __init__(self, entry: _Optional[_Union[RoomEntry, _Mapping]] = ...) -> None: ...

class DeleteRoomRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteRoomResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetRoomRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetRoomResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: RoomEntry
    def __init__(self, entry: _Optional[_Union[RoomEntry, _Mapping]] = ...) -> None: ...

class ListRoomsRequest(_message.Message):
    __slots__ = ("name", "user_id", "org_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    user_id: str
    org_id: str
    def __init__(self, name: _Optional[str] = ..., user_id: _Optional[str] = ..., org_id: _Optional[str] = ...) -> None: ...

class ListRoomsResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: RoomEntry
    def __init__(self, entry: _Optional[_Union[RoomEntry, _Mapping]] = ...) -> None: ...
