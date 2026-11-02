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

class IssueSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ISSUE_SEVERITY_UNSPECIFIED: _ClassVar[IssueSeverity]
    ISSUE_SEVERITY_LOW: _ClassVar[IssueSeverity]
    ISSUE_SEVERITY_MODERATE: _ClassVar[IssueSeverity]
    ISSUE_SEVERITY_HIGH: _ClassVar[IssueSeverity]
    ISSUE_SEVERITY_CRITICAL: _ClassVar[IssueSeverity]

class IssueStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ISSUE_STATUS_UNSPECIFIED: _ClassVar[IssueStatus]
    ISSUE_STATUS_OPEN: _ClassVar[IssueStatus]
    ISSUE_STATUS_CLOSED: _ClassVar[IssueStatus]
    ISSUE_STATUS_DRAFT: _ClassVar[IssueStatus]
    ISSUE_STATUS_PENDING_SCREENING: _ClassVar[IssueStatus]
    ISSUE_STATUS_FALSE_POSITIVE: _ClassVar[IssueStatus]
    ISSUE_STATUS_RISK_ACCEPTED: _ClassVar[IssueStatus]
    ISSUE_STATUS_MITIGATED: _ClassVar[IssueStatus]
ISSUE_SEVERITY_UNSPECIFIED: IssueSeverity
ISSUE_SEVERITY_LOW: IssueSeverity
ISSUE_SEVERITY_MODERATE: IssueSeverity
ISSUE_SEVERITY_HIGH: IssueSeverity
ISSUE_SEVERITY_CRITICAL: IssueSeverity
ISSUE_STATUS_UNSPECIFIED: IssueStatus
ISSUE_STATUS_OPEN: IssueStatus
ISSUE_STATUS_CLOSED: IssueStatus
ISSUE_STATUS_DRAFT: IssueStatus
ISSUE_STATUS_PENDING_SCREENING: IssueStatus
ISSUE_STATUS_FALSE_POSITIVE: IssueStatus
ISSUE_STATUS_RISK_ACCEPTED: IssueStatus
ISSUE_STATUS_MITIGATED: IssueStatus

class IssueBase(_message.Message):
    __slots__ = ("integration_finding_id", "external_id", "title", "description", "issue_type", "severity", "status", "category", "asset_identifier", "asset_identifier_field", "due_date", "date_identified", "cci_ref", "rule_id", "rule_version", "vulnerability_number", "checklist_status", "is_known_exploited", "source", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    INTEGRATION_FINDING_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ISSUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    ASSET_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ASSET_IDENTIFIER_FIELD_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    DATE_IDENTIFIED_FIELD_NUMBER: _ClassVar[int]
    CCI_REF_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    RULE_VERSION_FIELD_NUMBER: _ClassVar[int]
    VULNERABILITY_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CHECKLIST_STATUS_FIELD_NUMBER: _ClassVar[int]
    IS_KNOWN_EXPLOITED_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    integration_finding_id: str
    external_id: str
    title: str
    description: str
    issue_type: str
    severity: IssueSeverity
    status: IssueStatus
    category: str
    asset_identifier: str
    asset_identifier_field: str
    due_date: _timestamp_pb2.Timestamp
    date_identified: _timestamp_pb2.Timestamp
    cci_ref: str
    rule_id: str
    rule_version: str
    vulnerability_number: str
    checklist_status: str
    is_known_exploited: bool
    source: str
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(self, integration_finding_id: _Optional[str] = ..., external_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., issue_type: _Optional[str] = ..., severity: _Optional[_Union[IssueSeverity, str]] = ..., status: _Optional[_Union[IssueStatus, str]] = ..., category: _Optional[str] = ..., asset_identifier: _Optional[str] = ..., asset_identifier_field: _Optional[str] = ..., due_date: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., date_identified: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., cci_ref: _Optional[str] = ..., rule_id: _Optional[str] = ..., rule_version: _Optional[str] = ..., vulnerability_number: _Optional[str] = ..., checklist_status: _Optional[str] = ..., is_known_exploited: bool = ..., source: _Optional[str] = ..., metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...

class IssueUpsert(_message.Message):
    __slots__ = ("base", "source")
    BASE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    base: IssueBase
    source: str
    def __init__(self, base: _Optional[_Union[IssueBase, _Mapping]] = ..., source: _Optional[str] = ...) -> None: ...

class BatchUpsertIssuesOptions(_message.Message):
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

class BatchUpsertIssuesRequest(_message.Message):
    __slots__ = ("issues", "options")
    ISSUES_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    issues: _containers.RepeatedCompositeFieldContainer[IssueUpsert]
    options: BatchUpsertIssuesOptions
    def __init__(self, issues: _Optional[_Iterable[_Union[IssueUpsert, _Mapping]]] = ..., options: _Optional[_Union[BatchUpsertIssuesOptions, _Mapping]] = ...) -> None: ...

class StreamBatchUpsertIssuesRequest(_message.Message):
    __slots__ = ("issues", "options")
    ISSUES_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    issues: _containers.RepeatedCompositeFieldContainer[IssueUpsert]
    options: BatchUpsertIssuesOptions
    def __init__(self, issues: _Optional[_Iterable[_Union[IssueUpsert, _Mapping]]] = ..., options: _Optional[_Union[BatchUpsertIssuesOptions, _Mapping]] = ...) -> None: ...

class IssueResponse(_message.Message):
    __slots__ = ("id", "base", "created_by", "last_updated_by", "date_created", "date_last_updated")
    ID_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    DATE_CREATED_FIELD_NUMBER: _ClassVar[int]
    DATE_LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    id: int
    base: IssueBase
    created_by: str
    last_updated_by: str
    date_created: _timestamp_pb2.Timestamp
    date_last_updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., base: _Optional[_Union[IssueBase, _Mapping]] = ..., created_by: _Optional[str] = ..., last_updated_by: _Optional[str] = ..., date_created: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., date_last_updated: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class BatchUpsertIssuesResponse(_message.Message):
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
    created: _containers.RepeatedCompositeFieldContainer[IssueResponse]
    updated: _containers.RepeatedCompositeFieldContainer[IssueResponse]
    total_processed: int
    is_successful: bool
    error_message: str
    processing_time_ms: int
    statistics: _containers.ScalarMap[str, int]
    def __init__(self, created: _Optional[_Iterable[_Union[IssueResponse, _Mapping]]] = ..., updated: _Optional[_Iterable[_Union[IssueResponse, _Mapping]]] = ..., total_processed: _Optional[int] = ..., is_successful: bool = ..., error_message: _Optional[str] = ..., processing_time_ms: _Optional[int] = ..., statistics: _Optional[_Mapping[str, int]] = ...) -> None: ...

class IssueBatchProcessingError(_message.Message):
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

class StreamBatchUpsertIssuesResponse(_message.Message):
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
    items: _containers.RepeatedCompositeFieldContainer[IssueResponse]
    timestamp: _timestamp_pb2.Timestamp
    errors: _containers.RepeatedCompositeFieldContainer[IssueBatchProcessingError]
    processed_count: int
    success_count: int
    error_count: int
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(self, chunk_number: _Optional[int] = ..., chunk_size: _Optional[int] = ..., processing_time_ms: _Optional[int] = ..., is_successful: bool = ..., error_message: _Optional[str] = ..., items: _Optional[_Iterable[_Union[IssueResponse, _Mapping]]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[IssueBatchProcessingError, _Mapping]]] = ..., processed_count: _Optional[int] = ..., success_count: _Optional[int] = ..., error_count: _Optional[int] = ..., metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...
