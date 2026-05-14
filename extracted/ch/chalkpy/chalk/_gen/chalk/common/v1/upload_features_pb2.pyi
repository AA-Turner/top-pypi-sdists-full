from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class UploadFeaturesOptions(_message.Message):
    __slots__ = ("update_mataggs", "write_offline", "write_online")
    UPDATE_MATAGGS_FIELD_NUMBER: _ClassVar[int]
    WRITE_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    WRITE_ONLINE_FIELD_NUMBER: _ClassVar[int]
    update_mataggs: bool
    write_offline: bool
    write_online: bool
    def __init__(self, update_mataggs: bool = ..., write_offline: bool = ..., write_online: bool = ...) -> None: ...

class UploadFeaturesRequest(_message.Message):
    __slots__ = ("inputs_table", "options")
    INPUTS_TABLE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    inputs_table: bytes
    options: UploadFeaturesOptions
    def __init__(
        self, inputs_table: _Optional[bytes] = ..., options: _Optional[_Union[UploadFeaturesOptions, _Mapping]] = ...
    ) -> None: ...

class UploadFeaturesResponse(_message.Message):
    __slots__ = ("errors", "operation_id")
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    operation_id: str
    def __init__(
        self,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
        operation_id: _Optional[str] = ...,
    ) -> None: ...
