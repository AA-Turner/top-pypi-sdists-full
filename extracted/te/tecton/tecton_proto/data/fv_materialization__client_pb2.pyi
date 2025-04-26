from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import fco_locator__client_pb2 as _fco_locator__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DATA_TABLE_STATE_DELETED: OnlineDataTableState
DATA_TABLE_STATE_NOT_READY: OnlineDataTableState
DATA_TABLE_STATE_PENDING_DELETION: OnlineDataTableState
DATA_TABLE_STATE_READY: OnlineDataTableState
DATA_TABLE_STATE_UNKNOWN_UNSPECIFIED: OnlineDataTableState
DESCRIPTOR: _descriptor.FileDescriptor
ONLINE_BACKFILL_LOAD_TYPE_BULK: OnlineBackfillLoadType
ONLINE_BACKFILL_LOAD_TYPE_COMPACTION: OnlineBackfillLoadType
ONLINE_BACKFILL_LOAD_TYPE_TASK: OnlineBackfillLoadType
ONLINE_BACKFILL_LOAD_TYPE_UNSPECIFIED: OnlineBackfillLoadType
TABLE_FORMAT_VERSION_DEFAULT_UNSPECIFIED: TableFormatVersion
TABLE_FORMAT_VERSION_V2: TableFormatVersion
TABLE_FORMAT_VERSION_V3: TableFormatVersion

class FileLocation(_message.Message):
    __slots__ = ["path"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...

class FvMaterialization(_message.Message):
    __slots__ = ["feature_export_data_location", "feature_store_format_version", "has_been_revisted", "has_materialized_data", "id_feature_view_locator", "last_revisited_ts", "materialization_serial_version", "materialized_data_location", "misc_offline_data_location", "online_data_tables", "online_table_import_complete", "online_table_imported_by_materialization", "streaming_checkpoint_locations"]
    FEATURE_EXPORT_DATA_LOCATION_FIELD_NUMBER: _ClassVar[int]
    FEATURE_STORE_FORMAT_VERSION_FIELD_NUMBER: _ClassVar[int]
    HAS_BEEN_REVISTED_FIELD_NUMBER: _ClassVar[int]
    HAS_MATERIALIZED_DATA_FIELD_NUMBER: _ClassVar[int]
    ID_FEATURE_VIEW_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    LAST_REVISITED_TS_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_SERIAL_VERSION_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZED_DATA_LOCATION_FIELD_NUMBER: _ClassVar[int]
    MISC_OFFLINE_DATA_LOCATION_FIELD_NUMBER: _ClassVar[int]
    ONLINE_DATA_TABLES_FIELD_NUMBER: _ClassVar[int]
    ONLINE_TABLE_IMPORTED_BY_MATERIALIZATION_FIELD_NUMBER: _ClassVar[int]
    ONLINE_TABLE_IMPORT_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    STREAMING_CHECKPOINT_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    feature_export_data_location: FileLocation
    feature_store_format_version: int
    has_been_revisted: bool
    has_materialized_data: bool
    id_feature_view_locator: _fco_locator__client_pb2.IdFcoLocator
    last_revisited_ts: _timestamp_pb2.Timestamp
    materialization_serial_version: int
    materialized_data_location: FileLocation
    misc_offline_data_location: FileLocation
    online_data_tables: _containers.RepeatedCompositeFieldContainer[OnlineDataTable]
    online_table_import_complete: bool
    online_table_imported_by_materialization: bool
    streaming_checkpoint_locations: _containers.RepeatedCompositeFieldContainer[FileLocation]
    def __init__(self, id_feature_view_locator: _Optional[_Union[_fco_locator__client_pb2.IdFcoLocator, _Mapping]] = ..., materialization_serial_version: _Optional[int] = ..., materialized_data_location: _Optional[_Union[FileLocation, _Mapping]] = ..., streaming_checkpoint_locations: _Optional[_Iterable[_Union[FileLocation, _Mapping]]] = ..., has_materialized_data: bool = ..., feature_store_format_version: _Optional[int] = ..., misc_offline_data_location: _Optional[_Union[FileLocation, _Mapping]] = ..., online_table_imported_by_materialization: bool = ..., online_table_import_complete: bool = ..., feature_export_data_location: _Optional[_Union[FileLocation, _Mapping]] = ..., online_data_tables: _Optional[_Iterable[_Union[OnlineDataTable, _Mapping]]] = ..., has_been_revisted: bool = ..., last_revisited_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class OnlineDataTable(_message.Message):
    __slots__ = ["batch_table_format_version", "feature_data_watermark", "name", "state_transitions"]
    BATCH_TABLE_FORMAT_VERSION_FIELD_NUMBER: _ClassVar[int]
    FEATURE_DATA_WATERMARK_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    batch_table_format_version: TableFormatVersion
    feature_data_watermark: _timestamp_pb2.Timestamp
    name: str
    state_transitions: _containers.RepeatedCompositeFieldContainer[OnlineDataTableStateTransition]
    def __init__(self, name: _Optional[str] = ..., feature_data_watermark: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., state_transitions: _Optional[_Iterable[_Union[OnlineDataTableStateTransition, _Mapping]]] = ..., batch_table_format_version: _Optional[_Union[TableFormatVersion, str]] = ...) -> None: ...

class OnlineDataTableStateTransition(_message.Message):
    __slots__ = ["state", "timestamp"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    state: OnlineDataTableState
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, state: _Optional[_Union[OnlineDataTableState, str]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class OnlineBackfillLoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class TableFormatVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class OnlineDataTableState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
