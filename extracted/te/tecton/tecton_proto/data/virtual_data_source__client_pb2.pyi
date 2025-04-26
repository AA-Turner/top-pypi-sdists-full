from tecton_proto.common import data_source_type__client_pb2 as _data_source_type__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema_container__client_pb2 as _schema_container__client_pb2
from tecton_proto.data import batch_data_source__client_pb2 as _batch_data_source__client_pb2
from tecton_proto.data import fco_metadata__client_pb2 as _fco_metadata__client_pb2
from tecton_proto.data import stream_data_source__client_pb2 as _stream_data_source__client_pb2
from tecton_proto.validation import validator__client_pb2 as _validator__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VirtualDataSource(_message.Message):
    __slots__ = ["batch_data_source", "data_source_type", "fco_metadata", "options", "schema", "stream_data_source", "validation_args", "virtual_data_source_id"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BATCH_DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FCO_METADATA_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    STREAM_DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_ARGS_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    batch_data_source: _batch_data_source__client_pb2.BatchDataSource
    data_source_type: _data_source_type__client_pb2.DataSourceType
    fco_metadata: _fco_metadata__client_pb2.FcoMetadata
    options: _containers.ScalarMap[str, str]
    schema: _schema_container__client_pb2.SchemaContainer
    stream_data_source: _stream_data_source__client_pb2.StreamDataSource
    validation_args: _validator__client_pb2.VirtualDataSourceValidationArgs
    virtual_data_source_id: _id__client_pb2.Id
    def __init__(self, virtual_data_source_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., batch_data_source: _Optional[_Union[_batch_data_source__client_pb2.BatchDataSource, _Mapping]] = ..., stream_data_source: _Optional[_Union[_stream_data_source__client_pb2.StreamDataSource, _Mapping]] = ..., data_source_type: _Optional[_Union[_data_source_type__client_pb2.DataSourceType, str]] = ..., fco_metadata: _Optional[_Union[_fco_metadata__client_pb2.FcoMetadata, _Mapping]] = ..., schema: _Optional[_Union[_schema_container__client_pb2.SchemaContainer, _Mapping]] = ..., validation_args: _Optional[_Union[_validator__client_pb2.VirtualDataSourceValidationArgs, _Mapping]] = ..., options: _Optional[_Mapping[str, str]] = ...) -> None: ...
