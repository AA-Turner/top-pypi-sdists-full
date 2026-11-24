from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class QueryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUERY_STATUS_UNSPECIFIED: _ClassVar[QueryStatus]
    QUERY_STATUS_PENDING_SUBMISSION: _ClassVar[QueryStatus]
    QUERY_STATUS_SUBMITTED: _ClassVar[QueryStatus]
    QUERY_STATUS_RUNNING: _ClassVar[QueryStatus]
    QUERY_STATUS_ERROR: _ClassVar[QueryStatus]
    QUERY_STATUS_EXPIRED: _ClassVar[QueryStatus]
    QUERY_STATUS_CANCELLED: _ClassVar[QueryStatus]
    QUERY_STATUS_SUCCESSFUL: _ClassVar[QueryStatus]
    QUERY_STATUS_SUCCESSFUL_WITH_NONFATAL_ERRORS: _ClassVar[QueryStatus]

class CancellationReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CANCELLATION_REASON_UNSPECIFIED: _ClassVar[CancellationReason]
    CANCELLATION_REASON_MANUAL: _ClassVar[CancellationReason]
    CANCELLATION_REASON_UPSTREAM_FAILED: _ClassVar[CancellationReason]
    CANCELLATION_REASON_UPSTREAM_CANCELED: _ClassVar[CancellationReason]
    CANCELLATION_REASON_SCHEDULE_SKIPPED: _ClassVar[CancellationReason]
    CANCELLATION_REASON_SCHEDULER_CLEANUP: _ClassVar[CancellationReason]

QUERY_STATUS_UNSPECIFIED: QueryStatus
QUERY_STATUS_PENDING_SUBMISSION: QueryStatus
QUERY_STATUS_SUBMITTED: QueryStatus
QUERY_STATUS_RUNNING: QueryStatus
QUERY_STATUS_ERROR: QueryStatus
QUERY_STATUS_EXPIRED: QueryStatus
QUERY_STATUS_CANCELLED: QueryStatus
QUERY_STATUS_SUCCESSFUL: QueryStatus
QUERY_STATUS_SUCCESSFUL_WITH_NONFATAL_ERRORS: QueryStatus
CANCELLATION_REASON_UNSPECIFIED: CancellationReason
CANCELLATION_REASON_MANUAL: CancellationReason
CANCELLATION_REASON_UPSTREAM_FAILED: CancellationReason
CANCELLATION_REASON_UPSTREAM_CANCELED: CancellationReason
CANCELLATION_REASON_SCHEDULE_SKIPPED: CancellationReason
CANCELLATION_REASON_SCHEDULER_CLEANUP: CancellationReason
