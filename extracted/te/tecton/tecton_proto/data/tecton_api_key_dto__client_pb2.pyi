from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.auth import principal__client_pb2 as _principal__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TectonApiKeyDto(_message.Message):
    __slots__ = ["archived", "created_at", "created_by", "creator", "description", "expires_at", "hashed_key", "id", "is_active", "is_admin", "is_system_managed", "is_temporary", "name", "obscured_key"]
    ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    HASHED_KEY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    IS_ADMIN_FIELD_NUMBER: _ClassVar[int]
    IS_SYSTEM_MANAGED_FIELD_NUMBER: _ClassVar[int]
    IS_TEMPORARY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBSCURED_KEY_FIELD_NUMBER: _ClassVar[int]
    archived: bool
    created_at: _timestamp_pb2.Timestamp
    created_by: str
    creator: _principal__client_pb2.Principal
    description: str
    expires_at: _timestamp_pb2.Timestamp
    hashed_key: str
    id: _id__client_pb2.Id
    is_active: bool
    is_admin: bool
    is_system_managed: bool
    is_temporary: bool
    name: str
    obscured_key: str
    def __init__(self, id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., hashed_key: _Optional[str] = ..., description: _Optional[str] = ..., archived: bool = ..., created_by: _Optional[str] = ..., obscured_key: _Optional[str] = ..., is_admin: bool = ..., name: _Optional[str] = ..., is_active: bool = ..., creator: _Optional[_Union[_principal__client_pb2.Principal, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., is_system_managed: bool = ..., is_temporary: bool = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
