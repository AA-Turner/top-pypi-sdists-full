import datetime

from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VulnerabilitySeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VULNERABILITY_SEVERITY_UNSPECIFIED: _ClassVar[VulnerabilitySeverity]
    VULNERABILITY_SEVERITY_INFORMATIONAL: _ClassVar[VulnerabilitySeverity]
    VULNERABILITY_SEVERITY_LOW: _ClassVar[VulnerabilitySeverity]
    VULNERABILITY_SEVERITY_MODERATE: _ClassVar[VulnerabilitySeverity]
    VULNERABILITY_SEVERITY_HIGH: _ClassVar[VulnerabilitySeverity]
    VULNERABILITY_SEVERITY_CRITICAL: _ClassVar[VulnerabilitySeverity]

class VulnerabilityStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VULNERABILITY_STATUS_UNSPECIFIED: _ClassVar[VulnerabilityStatus]
    VULNERABILITY_STATUS_OPEN: _ClassVar[VulnerabilityStatus]
    VULNERABILITY_STATUS_CLOSED: _ClassVar[VulnerabilityStatus]
    VULNERABILITY_STATUS_FALSE_POSITIVE: _ClassVar[VulnerabilityStatus]
    VULNERABILITY_STATUS_RISK_ACCEPTED: _ClassVar[VulnerabilityStatus]
    VULNERABILITY_STATUS_DEVIATION_IN_PLACE: _ClassVar[VulnerabilityStatus]
    VULNERABILITY_STATUS_EXCEPTION_IN_PLACE: _ClassVar[VulnerabilityStatus]
    VULNERABILITY_STATUS_EXCEPTION_APPROVED: _ClassVar[VulnerabilityStatus]
    VULNERABILITY_STATUS_AWAITING_VENDOR_PATCH: _ClassVar[VulnerabilityStatus]
    VULNERABILITY_STATUS_MITIGATED: _ClassVar[VulnerabilityStatus]
VULNERABILITY_SEVERITY_UNSPECIFIED: VulnerabilitySeverity
VULNERABILITY_SEVERITY_INFORMATIONAL: VulnerabilitySeverity
VULNERABILITY_SEVERITY_LOW: VulnerabilitySeverity
VULNERABILITY_SEVERITY_MODERATE: VulnerabilitySeverity
VULNERABILITY_SEVERITY_HIGH: VulnerabilitySeverity
VULNERABILITY_SEVERITY_CRITICAL: VulnerabilitySeverity
VULNERABILITY_STATUS_UNSPECIFIED: VulnerabilityStatus
VULNERABILITY_STATUS_OPEN: VulnerabilityStatus
VULNERABILITY_STATUS_CLOSED: VulnerabilityStatus
VULNERABILITY_STATUS_FALSE_POSITIVE: VulnerabilityStatus
VULNERABILITY_STATUS_RISK_ACCEPTED: VulnerabilityStatus
VULNERABILITY_STATUS_DEVIATION_IN_PLACE: VulnerabilityStatus
VULNERABILITY_STATUS_EXCEPTION_IN_PLACE: VulnerabilityStatus
VULNERABILITY_STATUS_EXCEPTION_APPROVED: VulnerabilityStatus
VULNERABILITY_STATUS_AWAITING_VENDOR_PATCH: VulnerabilityStatus
VULNERABILITY_STATUS_MITIGATED: VulnerabilityStatus

class VulnBase(_message.Message):
    __slots__ = ("plugin_id", "external_id", "cve", "title", "description", "severity", "status", "category", "cvss_v2_score", "cvss_v3_score", "cvss_v2_vector", "cvss_v3_vector", "vpr_score", "ip_address", "dns", "port", "asset_identifier", "asset_identifier_field", "first_seen", "last_seen", "scan_date", "affected_packages", "installed_versions", "fixed_versions", "fix_status", "affected_os", "package_path", "image_digest", "source", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    PLUGIN_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CVE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    CVSS_V2_SCORE_FIELD_NUMBER: _ClassVar[int]
    CVSS_V3_SCORE_FIELD_NUMBER: _ClassVar[int]
    CVSS_V2_VECTOR_FIELD_NUMBER: _ClassVar[int]
    CVSS_V3_VECTOR_FIELD_NUMBER: _ClassVar[int]
    VPR_SCORE_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DNS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    ASSET_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ASSET_IDENTIFIER_FIELD_FIELD_NUMBER: _ClassVar[int]
    FIRST_SEEN_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    SCAN_DATE_FIELD_NUMBER: _ClassVar[int]
    AFFECTED_PACKAGES_FIELD_NUMBER: _ClassVar[int]
    INSTALLED_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    FIXED_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    FIX_STATUS_FIELD_NUMBER: _ClassVar[int]
    AFFECTED_OS_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_PATH_FIELD_NUMBER: _ClassVar[int]
    IMAGE_DIGEST_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    plugin_id: str
    external_id: str
    cve: str
    title: str
    description: str
    severity: VulnerabilitySeverity
    status: VulnerabilityStatus
    category: str
    cvss_v2_score: float
    cvss_v3_score: float
    cvss_v2_vector: str
    cvss_v3_vector: str
    vpr_score: float
    ip_address: str
    dns: str
    port: str
    asset_identifier: str
    asset_identifier_field: str
    first_seen: _timestamp_pb2.Timestamp
    last_seen: _timestamp_pb2.Timestamp
    scan_date: _timestamp_pb2.Timestamp
    affected_packages: str
    installed_versions: str
    fixed_versions: str
    fix_status: str
    affected_os: str
    package_path: str
    image_digest: str
    source: str
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(self, plugin_id: _Optional[str] = ..., external_id: _Optional[str] = ..., cve: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., severity: _Optional[_Union[VulnerabilitySeverity, str]] = ..., status: _Optional[_Union[VulnerabilityStatus, str]] = ..., category: _Optional[str] = ..., cvss_v2_score: _Optional[float] = ..., cvss_v3_score: _Optional[float] = ..., cvss_v2_vector: _Optional[str] = ..., cvss_v3_vector: _Optional[str] = ..., vpr_score: _Optional[float] = ..., ip_address: _Optional[str] = ..., dns: _Optional[str] = ..., port: _Optional[str] = ..., asset_identifier: _Optional[str] = ..., asset_identifier_field: _Optional[str] = ..., first_seen: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_seen: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., scan_date: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., affected_packages: _Optional[str] = ..., installed_versions: _Optional[str] = ..., fixed_versions: _Optional[str] = ..., fix_status: _Optional[str] = ..., affected_os: _Optional[str] = ..., package_path: _Optional[str] = ..., image_digest: _Optional[str] = ..., source: _Optional[str] = ..., metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...

class VulnUpsert(_message.Message):
    __slots__ = ("base", "source")
    BASE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    base: VulnBase
    source: str
    def __init__(self, base: _Optional[_Union[VulnBase, _Mapping]] = ..., source: _Optional[str] = ...) -> None: ...

class BatchUpsertVulnsOptions(_message.Message):
    __slots__ = ("source", "batch_import_uuid", "unique_key_fields", "batch_size", "parent_id", "parent_module", "enable_mop_up", "mop_up_status")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    BATCH_IMPORT_UUID_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_KEY_FIELDS_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_MODULE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_MOP_UP_FIELD_NUMBER: _ClassVar[int]
    MOP_UP_STATUS_FIELD_NUMBER: _ClassVar[int]
    source: str
    batch_import_uuid: str
    unique_key_fields: _containers.RepeatedScalarFieldContainer[str]
    batch_size: int
    parent_id: int
    parent_module: str
    enable_mop_up: bool
    mop_up_status: str
    def __init__(self, source: _Optional[str] = ..., batch_import_uuid: _Optional[str] = ..., unique_key_fields: _Optional[_Iterable[str]] = ..., batch_size: _Optional[int] = ..., parent_id: _Optional[int] = ..., parent_module: _Optional[str] = ..., enable_mop_up: bool = ..., mop_up_status: _Optional[str] = ...) -> None: ...

class BatchUpsertVulnsRequest(_message.Message):
    __slots__ = ("vulns", "options")
    VULNS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    vulns: _containers.RepeatedCompositeFieldContainer[VulnUpsert]
    options: BatchUpsertVulnsOptions
    def __init__(self, vulns: _Optional[_Iterable[_Union[VulnUpsert, _Mapping]]] = ..., options: _Optional[_Union[BatchUpsertVulnsOptions, _Mapping]] = ...) -> None: ...

class StreamBatchUpsertVulnsRequest(_message.Message):
    __slots__ = ("vulns", "options")
    VULNS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    vulns: _containers.RepeatedCompositeFieldContainer[VulnUpsert]
    options: BatchUpsertVulnsOptions
    def __init__(self, vulns: _Optional[_Iterable[_Union[VulnUpsert, _Mapping]]] = ..., options: _Optional[_Union[BatchUpsertVulnsOptions, _Mapping]] = ...) -> None: ...

class VulnResponse(_message.Message):
    __slots__ = ("id", "base", "created_by", "last_updated_by", "date_created", "date_last_updated")
    ID_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    DATE_CREATED_FIELD_NUMBER: _ClassVar[int]
    DATE_LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    id: int
    base: VulnBase
    created_by: str
    last_updated_by: str
    date_created: _timestamp_pb2.Timestamp
    date_last_updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., base: _Optional[_Union[VulnBase, _Mapping]] = ..., created_by: _Optional[str] = ..., last_updated_by: _Optional[str] = ..., date_created: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., date_last_updated: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class BatchUpsertVulnsResponse(_message.Message):
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
    created: _containers.RepeatedCompositeFieldContainer[VulnResponse]
    updated: _containers.RepeatedCompositeFieldContainer[VulnResponse]
    total_processed: int
    is_successful: bool
    error_message: str
    processing_time_ms: int
    statistics: _containers.ScalarMap[str, int]
    def __init__(self, created: _Optional[_Iterable[_Union[VulnResponse, _Mapping]]] = ..., updated: _Optional[_Iterable[_Union[VulnResponse, _Mapping]]] = ..., total_processed: _Optional[int] = ..., is_successful: bool = ..., error_message: _Optional[str] = ..., processing_time_ms: _Optional[int] = ..., statistics: _Optional[_Mapping[str, int]] = ...) -> None: ...

class VulnBatchProcessingError(_message.Message):
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

class StreamBatchUpsertVulnsResponse(_message.Message):
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
    items: _containers.RepeatedCompositeFieldContainer[VulnResponse]
    timestamp: _timestamp_pb2.Timestamp
    errors: _containers.RepeatedCompositeFieldContainer[VulnBatchProcessingError]
    processed_count: int
    success_count: int
    error_count: int
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(self, chunk_number: _Optional[int] = ..., chunk_size: _Optional[int] = ..., processing_time_ms: _Optional[int] = ..., is_successful: bool = ..., error_message: _Optional[str] = ..., items: _Optional[_Iterable[_Union[VulnResponse, _Mapping]]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[VulnBatchProcessingError, _Mapping]]] = ..., processed_count: _Optional[int] = ..., success_count: _Optional[int] = ..., error_count: _Optional[int] = ..., metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...
