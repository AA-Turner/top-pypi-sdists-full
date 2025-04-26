from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.data import fco_metadata__client_pb2 as _fco_metadata__client_pb2
from tecton_proto.validation import validator__client_pb2 as _validator__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Entity(_message.Message):
    __slots__ = ["entity_id", "fco_metadata", "join_keys", "join_keys_legacy", "options", "validation_args"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    FCO_METADATA_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEYS_LEGACY_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_ARGS_FIELD_NUMBER: _ClassVar[int]
    entity_id: _id__client_pb2.Id
    fco_metadata: _fco_metadata__client_pb2.FcoMetadata
    join_keys: _containers.RepeatedCompositeFieldContainer[_schema__client_pb2.Column]
    join_keys_legacy: _containers.RepeatedScalarFieldContainer[str]
    options: _containers.ScalarMap[str, str]
    validation_args: _validator__client_pb2.EntityValidationArgs
    def __init__(self, entity_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., join_keys_legacy: _Optional[_Iterable[str]] = ..., fco_metadata: _Optional[_Union[_fco_metadata__client_pb2.FcoMetadata, _Mapping]] = ..., validation_args: _Optional[_Union[_validator__client_pb2.EntityValidationArgs, _Mapping]] = ..., options: _Optional[_Mapping[str, str]] = ..., join_keys: _Optional[_Iterable[_Union[_schema__client_pb2.Column, _Mapping]]] = ...) -> None: ...
