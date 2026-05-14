from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventBusEnvelope(_message.Message):
    __slots__ = ("event_id", "created_at", "environment_id", "message", "attributes")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    created_at: _timestamp_pb2.Timestamp
    environment_id: str
    message: EventBusMessage
    attributes: _containers.ScalarMap[str, str]
    def __init__(
        self,
        event_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        environment_id: _Optional[str] = ...,
        message: _Optional[_Union[EventBusMessage, _Mapping]] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class EventBusMessage(_message.Message):
    __slots__ = ("webhook_event",)
    WEBHOOK_EVENT_FIELD_NUMBER: _ClassVar[int]
    webhook_event: WebhookEvent
    def __init__(self, webhook_event: _Optional[_Union[WebhookEvent, _Mapping]] = ...) -> None: ...

class WebhookEvent(_message.Message):
    __slots__ = ("webhook_id", "subscription", "payload", "event_timestamp", "idempotency_key")
    WEBHOOK_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    EVENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    webhook_id: str
    subscription: str
    payload: _struct_pb2.Struct
    event_timestamp: _timestamp_pb2.Timestamp
    idempotency_key: str
    def __init__(
        self,
        webhook_id: _Optional[str] = ...,
        subscription: _Optional[str] = ...,
        payload: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        event_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        idempotency_key: _Optional[str] = ...,
    ) -> None: ...
