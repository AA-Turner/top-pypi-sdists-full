from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
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

class Webhook(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "team_id",
        "name",
        "url",
        "subscriptions",
        "secret",
        "headers",
        "created_at",
        "updated_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    team_id: str
    name: str
    url: str
    subscriptions: _containers.RepeatedScalarFieldContainer[str]
    secret: str
    headers: _struct_pb2.Struct
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        url: _Optional[str] = ...,
        subscriptions: _Optional[_Iterable[str]] = ...,
        secret: _Optional[str] = ...,
        headers: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class CreateWebhookRequest(_message.Message):
    __slots__ = ("environment_id", "name", "url", "subscriptions", "secret", "headers")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    name: str
    url: str
    subscriptions: _containers.RepeatedScalarFieldContainer[str]
    secret: str
    headers: _struct_pb2.Struct
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        url: _Optional[str] = ...,
        subscriptions: _Optional[_Iterable[str]] = ...,
        secret: _Optional[str] = ...,
        headers: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
    ) -> None: ...

class CreateWebhookResponse(_message.Message):
    __slots__ = ("webhook",)
    WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    webhook: Webhook
    def __init__(self, webhook: _Optional[_Union[Webhook, _Mapping]] = ...) -> None: ...

class UpdateWebhookRequest(_message.Message):
    __slots__ = ("id", "name", "url", "subscriptions", "secret", "headers")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    url: str
    subscriptions: _containers.RepeatedScalarFieldContainer[str]
    secret: str
    headers: _struct_pb2.Struct
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        url: _Optional[str] = ...,
        subscriptions: _Optional[_Iterable[str]] = ...,
        secret: _Optional[str] = ...,
        headers: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
    ) -> None: ...

class UpdateWebhookResponse(_message.Message):
    __slots__ = ("webhook",)
    WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    webhook: Webhook
    def __init__(self, webhook: _Optional[_Union[Webhook, _Mapping]] = ...) -> None: ...

class DeleteWebhookRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteWebhookResponse(_message.Message):
    __slots__ = ("webhook",)
    WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    webhook: Webhook
    def __init__(self, webhook: _Optional[_Union[Webhook, _Mapping]] = ...) -> None: ...

class GetWebhookRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetWebhookResponse(_message.Message):
    __slots__ = ("webhook",)
    WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    webhook: Webhook
    def __init__(self, webhook: _Optional[_Union[Webhook, _Mapping]] = ...) -> None: ...

class ListWebhooksRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class ListWebhooksResponse(_message.Message):
    __slots__ = ("webhooks",)
    WEBHOOKS_FIELD_NUMBER: _ClassVar[int]
    webhooks: _containers.RepeatedCompositeFieldContainer[Webhook]
    def __init__(self, webhooks: _Optional[_Iterable[_Union[Webhook, _Mapping]]] = ...) -> None: ...
