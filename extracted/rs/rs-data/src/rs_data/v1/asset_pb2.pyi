import datetime

from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AssetBase(_message.Message):
    __slots__ = ("uuid", "name", "other_tracking_number", "serial_number", "ip_address", "ipv6_address", "mac_address", "location", "manufacturer", "model", "cpu", "ram", "disk_storage", "operating_system", "os_version", "asset_type", "management_type", "cmmc_asset_type", "asset_category", "asset_owner_id", "system_administrator_id", "software_vendor", "software_name", "software_version", "software_acronym", "software_function", "patch_level", "cpe", "aws_identifier", "azure_identifier", "google_identifier", "other_cloud_identifier", "qualys_id", "sicura_id", "tenable_id", "wiz_id", "scanning_tool", "purchase_date", "end_of_life_date", "last_date_allowed", "status", "approval_status", "network_approval", "process_status", "is_public", "b_virtual", "b_public_facing", "b_authenticated_scan", "b_latest_scan", "b_ia_enabled", "b_fam_accepted", "b_externally_authorized", "diagram_level", "description", "notes", "net_bios", "baseline_configuration", "fqdn", "uri", "asset_tag_number", "vlan_id", "firmware_version", "purpose", "facility_id", "org_id", "emass_id", "batch_import_uuid", "parent_id", "parent_module")
    UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OTHER_TRACKING_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    IPV6_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MAC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    RAM_FIELD_NUMBER: _ClassVar[int]
    DISK_STORAGE_FIELD_NUMBER: _ClassVar[int]
    OPERATING_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    OS_VERSION_FIELD_NUMBER: _ClassVar[int]
    ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    MANAGEMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CMMC_ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSET_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    ASSET_OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_ADMINISTRATOR_ID_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_VENDOR_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_NAME_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_ACRONYM_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    PATCH_LEVEL_FIELD_NUMBER: _ClassVar[int]
    CPE_FIELD_NUMBER: _ClassVar[int]
    AWS_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    AZURE_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    OTHER_CLOUD_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    QUALYS_ID_FIELD_NUMBER: _ClassVar[int]
    SICURA_ID_FIELD_NUMBER: _ClassVar[int]
    TENABLE_ID_FIELD_NUMBER: _ClassVar[int]
    WIZ_ID_FIELD_NUMBER: _ClassVar[int]
    SCANNING_TOOL_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_DATE_FIELD_NUMBER: _ClassVar[int]
    END_OF_LIFE_DATE_FIELD_NUMBER: _ClassVar[int]
    LAST_DATE_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    APPROVAL_STATUS_FIELD_NUMBER: _ClassVar[int]
    NETWORK_APPROVAL_FIELD_NUMBER: _ClassVar[int]
    PROCESS_STATUS_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    B_VIRTUAL_FIELD_NUMBER: _ClassVar[int]
    B_PUBLIC_FACING_FIELD_NUMBER: _ClassVar[int]
    B_AUTHENTICATED_SCAN_FIELD_NUMBER: _ClassVar[int]
    B_LATEST_SCAN_FIELD_NUMBER: _ClassVar[int]
    B_IA_ENABLED_FIELD_NUMBER: _ClassVar[int]
    B_FAM_ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    B_EXTERNALLY_AUTHORIZED_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_LEVEL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    NET_BIOS_FIELD_NUMBER: _ClassVar[int]
    BASELINE_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    FQDN_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    ASSET_TAG_NUMBER_FIELD_NUMBER: _ClassVar[int]
    VLAN_ID_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    EMASS_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_IMPORT_UUID_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_MODULE_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    name: str
    other_tracking_number: str
    serial_number: str
    ip_address: str
    ipv6_address: str
    mac_address: str
    location: str
    manufacturer: str
    model: str
    cpu: str
    ram: str
    disk_storage: str
    operating_system: str
    os_version: str
    asset_type: str
    management_type: str
    cmmc_asset_type: str
    asset_category: str
    asset_owner_id: int
    system_administrator_id: int
    software_vendor: str
    software_name: str
    software_version: str
    software_acronym: str
    software_function: str
    patch_level: str
    cpe: str
    aws_identifier: str
    azure_identifier: str
    google_identifier: str
    other_cloud_identifier: str
    qualys_id: str
    sicura_id: str
    tenable_id: str
    wiz_id: str
    scanning_tool: str
    purchase_date: _timestamp_pb2.Timestamp
    end_of_life_date: _timestamp_pb2.Timestamp
    last_date_allowed: _timestamp_pb2.Timestamp
    status: str
    approval_status: str
    network_approval: str
    process_status: str
    is_public: bool
    b_virtual: bool
    b_public_facing: bool
    b_authenticated_scan: bool
    b_latest_scan: bool
    b_ia_enabled: bool
    b_fam_accepted: bool
    b_externally_authorized: bool
    diagram_level: int
    description: str
    notes: str
    net_bios: str
    baseline_configuration: str
    fqdn: str
    uri: str
    asset_tag_number: str
    vlan_id: str
    firmware_version: str
    purpose: str
    facility_id: int
    org_id: int
    emass_id: str
    batch_import_uuid: str
    parent_id: int
    parent_module: str
    def __init__(self, uuid: _Optional[str] = ..., name: _Optional[str] = ..., other_tracking_number: _Optional[str] = ..., serial_number: _Optional[str] = ..., ip_address: _Optional[str] = ..., ipv6_address: _Optional[str] = ..., mac_address: _Optional[str] = ..., location: _Optional[str] = ..., manufacturer: _Optional[str] = ..., model: _Optional[str] = ..., cpu: _Optional[str] = ..., ram: _Optional[str] = ..., disk_storage: _Optional[str] = ..., operating_system: _Optional[str] = ..., os_version: _Optional[str] = ..., asset_type: _Optional[str] = ..., management_type: _Optional[str] = ..., cmmc_asset_type: _Optional[str] = ..., asset_category: _Optional[str] = ..., asset_owner_id: _Optional[int] = ..., system_administrator_id: _Optional[int] = ..., software_vendor: _Optional[str] = ..., software_name: _Optional[str] = ..., software_version: _Optional[str] = ..., software_acronym: _Optional[str] = ..., software_function: _Optional[str] = ..., patch_level: _Optional[str] = ..., cpe: _Optional[str] = ..., aws_identifier: _Optional[str] = ..., azure_identifier: _Optional[str] = ..., google_identifier: _Optional[str] = ..., other_cloud_identifier: _Optional[str] = ..., qualys_id: _Optional[str] = ..., sicura_id: _Optional[str] = ..., tenable_id: _Optional[str] = ..., wiz_id: _Optional[str] = ..., scanning_tool: _Optional[str] = ..., purchase_date: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_of_life_date: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_date_allowed: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[str] = ..., approval_status: _Optional[str] = ..., network_approval: _Optional[str] = ..., process_status: _Optional[str] = ..., is_public: bool = ..., b_virtual: bool = ..., b_public_facing: bool = ..., b_authenticated_scan: bool = ..., b_latest_scan: bool = ..., b_ia_enabled: bool = ..., b_fam_accepted: bool = ..., b_externally_authorized: bool = ..., diagram_level: _Optional[int] = ..., description: _Optional[str] = ..., notes: _Optional[str] = ..., net_bios: _Optional[str] = ..., baseline_configuration: _Optional[str] = ..., fqdn: _Optional[str] = ..., uri: _Optional[str] = ..., asset_tag_number: _Optional[str] = ..., vlan_id: _Optional[str] = ..., firmware_version: _Optional[str] = ..., purpose: _Optional[str] = ..., facility_id: _Optional[int] = ..., org_id: _Optional[int] = ..., emass_id: _Optional[str] = ..., batch_import_uuid: _Optional[str] = ..., parent_id: _Optional[int] = ..., parent_module: _Optional[str] = ...) -> None: ...

class AssetUpsert(_message.Message):
    __slots__ = ("base", "source")
    BASE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    base: AssetBase
    source: str
    def __init__(self, base: _Optional[_Union[AssetBase, _Mapping]] = ..., source: _Optional[str] = ...) -> None: ...

class BatchCreateOrUpdateOptions(_message.Message):
    __slots__ = ("source", "batch_import_uuid", "unique_key_fields", "enable_mop_up", "mop_up_status", "batch_size", "parent_id", "parent_module")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    BATCH_IMPORT_UUID_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_KEY_FIELDS_FIELD_NUMBER: _ClassVar[int]
    ENABLE_MOP_UP_FIELD_NUMBER: _ClassVar[int]
    MOP_UP_STATUS_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_MODULE_FIELD_NUMBER: _ClassVar[int]
    source: str
    batch_import_uuid: str
    unique_key_fields: _containers.RepeatedScalarFieldContainer[str]
    enable_mop_up: bool
    mop_up_status: str
    batch_size: int
    parent_id: int
    parent_module: str
    def __init__(self, source: _Optional[str] = ..., batch_import_uuid: _Optional[str] = ..., unique_key_fields: _Optional[_Iterable[str]] = ..., enable_mop_up: bool = ..., mop_up_status: _Optional[str] = ..., batch_size: _Optional[int] = ..., parent_id: _Optional[int] = ..., parent_module: _Optional[str] = ...) -> None: ...

class BatchCreateOrUpdateAssetsRequest(_message.Message):
    __slots__ = ("assets", "options")
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    assets: _containers.RepeatedCompositeFieldContainer[AssetUpsert]
    options: BatchCreateOrUpdateOptions
    def __init__(self, assets: _Optional[_Iterable[_Union[AssetUpsert, _Mapping]]] = ..., options: _Optional[_Union[BatchCreateOrUpdateOptions, _Mapping]] = ...) -> None: ...

class StreamBatchCreateOrUpdateAssetsRequest(_message.Message):
    __slots__ = ("assets", "options")
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    assets: _containers.RepeatedCompositeFieldContainer[AssetUpsert]
    options: BatchCreateOrUpdateOptions
    def __init__(self, assets: _Optional[_Iterable[_Union[AssetUpsert, _Mapping]]] = ..., options: _Optional[_Union[BatchCreateOrUpdateOptions, _Mapping]] = ...) -> None: ...

class AssetResponse(_message.Message):
    __slots__ = ("id", "base", "asset_owner", "system_administrator", "facility", "org", "created_by", "last_updated_by", "created_by_id", "date_created", "last_updated_by_id", "date_last_updated")
    ID_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    ASSET_OWNER_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_ADMINISTRATOR_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_ID_FIELD_NUMBER: _ClassVar[int]
    DATE_CREATED_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_BY_ID_FIELD_NUMBER: _ClassVar[int]
    DATE_LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    id: int
    base: AssetBase
    asset_owner: str
    system_administrator: str
    facility: str
    org: str
    created_by: str
    last_updated_by: str
    created_by_id: str
    date_created: _timestamp_pb2.Timestamp
    last_updated_by_id: str
    date_last_updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., base: _Optional[_Union[AssetBase, _Mapping]] = ..., asset_owner: _Optional[str] = ..., system_administrator: _Optional[str] = ..., facility: _Optional[str] = ..., org: _Optional[str] = ..., created_by: _Optional[str] = ..., last_updated_by: _Optional[str] = ..., created_by_id: _Optional[str] = ..., date_created: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_updated_by_id: _Optional[str] = ..., date_last_updated: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class BatchCreateOrUpdateAssetsResponse(_message.Message):
    __slots__ = ("created", "updated", "total_processed", "is_successful", "error_message", "processing_time_ms", "statistics")
    class StatisticsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    CREATED_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PROCESSED_FIELD_NUMBER: _ClassVar[int]
    IS_SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    STATISTICS_FIELD_NUMBER: _ClassVar[int]
    created: _containers.RepeatedCompositeFieldContainer[AssetResponse]
    updated: _containers.RepeatedCompositeFieldContainer[AssetResponse]
    total_processed: int
    is_successful: bool
    error_message: str
    processing_time_ms: int
    statistics: _containers.ScalarMap[str, int]
    def __init__(self, created: _Optional[_Iterable[_Union[AssetResponse, _Mapping]]] = ..., updated: _Optional[_Iterable[_Union[AssetResponse, _Mapping]]] = ..., total_processed: _Optional[int] = ..., is_successful: bool = ..., error_message: _Optional[str] = ..., processing_time_ms: _Optional[int] = ..., statistics: _Optional[_Mapping[str, int]] = ...) -> None: ...

class BatchProcessingError(_message.Message):
    __slots__ = ("item_index", "error_message", "exception_type", "timestamp", "stack_trace")
    ITEM_INDEX_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STACK_TRACE_FIELD_NUMBER: _ClassVar[int]
    item_index: int
    error_message: str
    exception_type: str
    timestamp: _timestamp_pb2.Timestamp
    stack_trace: str
    def __init__(self, item_index: _Optional[int] = ..., error_message: _Optional[str] = ..., exception_type: _Optional[str] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., stack_trace: _Optional[str] = ...) -> None: ...

class StreamBatchCreateOrUpdateAssetsResponse(_message.Message):
    __slots__ = ("chunk_number", "chunk_size", "processing_time_ms", "is_successful", "error_message", "items", "timestamp", "errors", "processed_count", "success_count", "error_count", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    CHUNK_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CHUNK_SIZE_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    IS_SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_COUNT_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_COUNT_FIELD_NUMBER: _ClassVar[int]
    ERROR_COUNT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    chunk_number: int
    chunk_size: int
    processing_time_ms: int
    is_successful: bool
    error_message: str
    items: _containers.RepeatedCompositeFieldContainer[AssetResponse]
    timestamp: _timestamp_pb2.Timestamp
    errors: _containers.RepeatedCompositeFieldContainer[BatchProcessingError]
    processed_count: int
    success_count: int
    error_count: int
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(self, chunk_number: _Optional[int] = ..., chunk_size: _Optional[int] = ..., processing_time_ms: _Optional[int] = ..., is_successful: bool = ..., error_message: _Optional[str] = ..., items: _Optional[_Iterable[_Union[AssetResponse, _Mapping]]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[BatchProcessingError, _Mapping]]] = ..., processed_count: _Optional[int] = ..., success_count: _Optional[int] = ..., error_count: _Optional[int] = ..., metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...
