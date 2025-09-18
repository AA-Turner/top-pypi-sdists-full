from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class ChalkStatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHALK_STATUS_CODE_UNSPECIFIED: _ClassVar[ChalkStatusCode]
    CHALK_STATUS_CODE_OK: _ClassVar[ChalkStatusCode]
    CHALK_STATUS_CODE_ERROR: _ClassVar[ChalkStatusCode]

class ChalkSpanKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHALK_SPAN_KIND_UNSPECIFIED: _ClassVar[ChalkSpanKind]
    CHALK_SPAN_KIND_SERVER: _ClassVar[ChalkSpanKind]
    CHALK_SPAN_KIND_CLIENT: _ClassVar[ChalkSpanKind]
    CHALK_SPAN_KIND_PRODUCER: _ClassVar[ChalkSpanKind]
    CHALK_SPAN_KIND_CONSUMER: _ClassVar[ChalkSpanKind]
    CHALK_SPAN_KIND_INTERNAL: _ClassVar[ChalkSpanKind]

CHALK_STATUS_CODE_UNSPECIFIED: ChalkStatusCode
CHALK_STATUS_CODE_OK: ChalkStatusCode
CHALK_STATUS_CODE_ERROR: ChalkStatusCode
CHALK_SPAN_KIND_UNSPECIFIED: ChalkSpanKind
CHALK_SPAN_KIND_SERVER: ChalkSpanKind
CHALK_SPAN_KIND_CLIENT: ChalkSpanKind
CHALK_SPAN_KIND_PRODUCER: ChalkSpanKind
CHALK_SPAN_KIND_CONSUMER: ChalkSpanKind
CHALK_SPAN_KIND_INTERNAL: ChalkSpanKind

class ChalkSpan(_message.Message):
    __slots__ = (
        "span_id",
        "trace_id",
        "parent_span_id",
        "operation_name",
        "start_time",
        "end_time",
        "duration",
        "status",
        "attributes",
        "events",
        "links",
        "kind",
    )
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    span_id: str
    trace_id: str
    parent_span_id: str
    operation_name: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    duration: _duration_pb2.Duration
    status: ChalkSpanStatus
    attributes: _containers.ScalarMap[str, str]
    events: _containers.RepeatedCompositeFieldContainer[ChalkSpanEvent]
    links: _containers.RepeatedCompositeFieldContainer[ChalkSpanLink]
    kind: ChalkSpanKind
    def __init__(
        self,
        span_id: _Optional[str] = ...,
        trace_id: _Optional[str] = ...,
        parent_span_id: _Optional[str] = ...,
        operation_name: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        status: _Optional[_Union[ChalkSpanStatus, _Mapping]] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
        events: _Optional[_Iterable[_Union[ChalkSpanEvent, _Mapping]]] = ...,
        links: _Optional[_Iterable[_Union[ChalkSpanLink, _Mapping]]] = ...,
        kind: _Optional[_Union[ChalkSpanKind, str]] = ...,
    ) -> None: ...

class ChalkSpanStatus(_message.Message):
    __slots__ = ("code", "description")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    code: ChalkStatusCode
    description: str
    def __init__(
        self, code: _Optional[_Union[ChalkStatusCode, str]] = ..., description: _Optional[str] = ...
    ) -> None: ...

class ChalkSpanEvent(_message.Message):
    __slots__ = ("name", "timestamp", "attributes")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    name: str
    timestamp: _timestamp_pb2.Timestamp
    attributes: _containers.ScalarMap[str, str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ChalkSpanLink(_message.Message):
    __slots__ = ("trace_id", "span_id", "attributes")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    trace_id: str
    span_id: str
    attributes: _containers.ScalarMap[str, str]
    def __init__(
        self,
        trace_id: _Optional[str] = ...,
        span_id: _Optional[str] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ChalkTrace(_message.Message):
    __slots__ = ("trace_id", "spans", "root_span_id", "service_name", "resource_attributes")
    class ResourceAttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    SPANS_FIELD_NUMBER: _ClassVar[int]
    ROOT_SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    trace_id: str
    spans: _containers.RepeatedCompositeFieldContainer[ChalkSpan]
    root_span_id: str
    service_name: str
    resource_attributes: _containers.ScalarMap[str, str]
    def __init__(
        self,
        trace_id: _Optional[str] = ...,
        spans: _Optional[_Iterable[_Union[ChalkSpan, _Mapping]]] = ...,
        root_span_id: _Optional[str] = ...,
        service_name: _Optional[str] = ...,
        resource_attributes: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class GetTraceRequest(_message.Message):
    __slots__ = ("operation_id", "trace_id")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    trace_id: str
    def __init__(self, operation_id: _Optional[str] = ..., trace_id: _Optional[str] = ...) -> None: ...

class GetTraceResponse(_message.Message):
    __slots__ = ("trace",)
    TRACE_FIELD_NUMBER: _ClassVar[int]
    trace: ChalkTrace
    def __init__(self, trace: _Optional[_Union[ChalkTrace, _Mapping]] = ...) -> None: ...
