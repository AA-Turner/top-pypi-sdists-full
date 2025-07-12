from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import fco_locator__client_pb2 as _fco_locator__client_pb2
from tecton_proto.workflows import state_machine_workflow__client_pb2 as _state_machine_workflow__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
IMPORT_TABLE_STATE_CANCELLED: ImportTableState
IMPORT_TABLE_STATE_CANCELLING: ImportTableState
IMPORT_TABLE_STATE_COMPLETED: ImportTableState
IMPORT_TABLE_STATE_FAILED: ImportTableState
IMPORT_TABLE_STATE_IMPORT_RUNNING: ImportTableState
IMPORT_TABLE_STATE_UNKNOWN: ImportTableState

class DynamoImportTableWorkflow(_message.Message):
    __slots__ = ["debug_message", "import_arn", "import_table_description", "params", "state_transitions", "success"]
    DEBUG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IMPORT_ARN_FIELD_NUMBER: _ClassVar[int]
    IMPORT_TABLE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    STATE_TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    debug_message: str
    import_arn: str
    import_table_description: str
    params: ImportParams
    state_transitions: _containers.RepeatedCompositeFieldContainer[ObservedImportTableState]
    success: bool
    def __init__(self, params: _Optional[_Union[ImportParams, _Mapping]] = ..., import_arn: _Optional[str] = ..., state_transitions: _Optional[_Iterable[_Union[ObservedImportTableState, _Mapping]]] = ..., import_table_description: _Optional[str] = ..., debug_message: _Optional[str] = ..., success: bool = ...) -> None: ...

class ImportParams(_message.Message):
    __slots__ = ["client_token", "compression_type", "dynamo_table_name", "fv_locator", "import_path", "s3_bucket_owner", "table_watermark", "update_fv_materialization"]
    CLIENT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    DYNAMO_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    FV_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    IMPORT_PATH_FIELD_NUMBER: _ClassVar[int]
    S3_BUCKET_OWNER_FIELD_NUMBER: _ClassVar[int]
    TABLE_WATERMARK_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FV_MATERIALIZATION_FIELD_NUMBER: _ClassVar[int]
    client_token: str
    compression_type: str
    dynamo_table_name: str
    fv_locator: _fco_locator__client_pb2.IdFcoLocator
    import_path: str
    s3_bucket_owner: str
    table_watermark: _timestamp_pb2.Timestamp
    update_fv_materialization: bool
    def __init__(self, import_path: _Optional[str] = ..., compression_type: _Optional[str] = ..., s3_bucket_owner: _Optional[str] = ..., fv_locator: _Optional[_Union[_fco_locator__client_pb2.IdFcoLocator, _Mapping]] = ..., dynamo_table_name: _Optional[str] = ..., client_token: _Optional[str] = ..., table_watermark: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_fv_materialization: bool = ...) -> None: ...

class ObservedImportTableState(_message.Message):
    __slots__ = ["state", "timestamp"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    state: ImportTableState
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, state: _Optional[_Union[ImportTableState, str]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ImportTableState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
