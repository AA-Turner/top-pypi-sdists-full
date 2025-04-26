from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from tecton_proto.auth import principal__client_pb2 as _principal__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PrincipalGroup(_message.Message):
    __slots__ = ["created_at", "created_by", "description", "id", "idp_mapping_names", "is_membership_editable", "name", "updated_at"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IDP_MAPPING_NAMES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_MEMBERSHIP_EDITABLE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    created_by: _principal__client_pb2.Principal
    description: str
    id: str
    idp_mapping_names: _containers.RepeatedScalarFieldContainer[str]
    is_membership_editable: bool
    name: str
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., idp_mapping_names: _Optional[_Iterable[str]] = ..., is_membership_editable: bool = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_by: _Optional[_Union[_principal__client_pb2.Principal, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
