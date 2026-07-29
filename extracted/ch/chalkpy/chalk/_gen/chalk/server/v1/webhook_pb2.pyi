from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class WebhookComparatorKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WEBHOOK_COMPARATOR_KIND_UNSPECIFIED: _ClassVar[WebhookComparatorKind]
    WEBHOOK_COMPARATOR_KIND_EQ: _ClassVar[WebhookComparatorKind]
    WEBHOOK_COMPARATOR_KIND_NEQ: _ClassVar[WebhookComparatorKind]
    WEBHOOK_COMPARATOR_KIND_ONE_OF: _ClassVar[WebhookComparatorKind]

WEBHOOK_COMPARATOR_KIND_UNSPECIFIED: WebhookComparatorKind
WEBHOOK_COMPARATOR_KIND_EQ: WebhookComparatorKind
WEBHOOK_COMPARATOR_KIND_NEQ: WebhookComparatorKind
WEBHOOK_COMPARATOR_KIND_ONE_OF: WebhookComparatorKind

class WebhookSubscriptionFilter(_message.Message):
    __slots__ = ("key", "comparator", "values")
    KEY_FIELD_NUMBER: _ClassVar[int]
    COMPARATOR_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    key: str
    comparator: WebhookComparatorKind
    values: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Value]
    def __init__(
        self,
        key: _Optional[str] = ...,
        comparator: _Optional[_Union[WebhookComparatorKind, str]] = ...,
        values: _Optional[_Iterable[_Union[_struct_pb2.Value, _Mapping]]] = ...,
    ) -> None: ...

class WebhookSubscription(_message.Message):
    __slots__ = ("subscription", "filters")
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    subscription: str
    filters: _containers.RepeatedCompositeFieldContainer[WebhookSubscriptionFilter]
    def __init__(
        self,
        subscription: _Optional[str] = ...,
        filters: _Optional[_Iterable[_Union[WebhookSubscriptionFilter, _Mapping]]] = ...,
    ) -> None: ...

class WebhookSubscriptionFilterOptionValue(_message.Message):
    __slots__ = ("label", "value")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    label: str
    value: _struct_pb2.Value
    def __init__(
        self, label: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
    ) -> None: ...

class WebhookSubscriptionFilterOption(_message.Message):
    __slots__ = ("key", "options", "allow_freeform")
    KEY_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_FREEFORM_FIELD_NUMBER: _ClassVar[int]
    key: str
    options: _containers.RepeatedCompositeFieldContainer[WebhookSubscriptionFilterOptionValue]
    allow_freeform: bool
    def __init__(
        self,
        key: _Optional[str] = ...,
        options: _Optional[_Iterable[_Union[WebhookSubscriptionFilterOptionValue, _Mapping]]] = ...,
        allow_freeform: bool = ...,
    ) -> None: ...

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
        "subscriptions_with_filters",
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
    SUBSCRIPTIONS_WITH_FILTERS_FIELD_NUMBER: _ClassVar[int]
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
    subscriptions_with_filters: _containers.RepeatedCompositeFieldContainer[WebhookSubscription]
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
        subscriptions_with_filters: _Optional[_Iterable[_Union[WebhookSubscription, _Mapping]]] = ...,
    ) -> None: ...

class CreateWebhookRequest(_message.Message):
    __slots__ = ("environment_id", "name", "url", "subscriptions", "secret", "headers", "subscriptions_with_filters")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_WITH_FILTERS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    name: str
    url: str
    subscriptions: _containers.RepeatedScalarFieldContainer[str]
    secret: str
    headers: _struct_pb2.Struct
    subscriptions_with_filters: _containers.RepeatedCompositeFieldContainer[WebhookSubscription]
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        url: _Optional[str] = ...,
        subscriptions: _Optional[_Iterable[str]] = ...,
        secret: _Optional[str] = ...,
        headers: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        subscriptions_with_filters: _Optional[_Iterable[_Union[WebhookSubscription, _Mapping]]] = ...,
    ) -> None: ...

class CreateWebhookResponse(_message.Message):
    __slots__ = ("webhook",)
    WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    webhook: Webhook
    def __init__(self, webhook: _Optional[_Union[Webhook, _Mapping]] = ...) -> None: ...

class UpdateWebhookRequest(_message.Message):
    __slots__ = ("id", "name", "url", "subscriptions", "secret", "headers", "subscriptions_with_filters")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_WITH_FILTERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    url: str
    subscriptions: _containers.RepeatedScalarFieldContainer[str]
    secret: str
    headers: _struct_pb2.Struct
    subscriptions_with_filters: _containers.RepeatedCompositeFieldContainer[WebhookSubscription]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        url: _Optional[str] = ...,
        subscriptions: _Optional[_Iterable[str]] = ...,
        secret: _Optional[str] = ...,
        headers: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        subscriptions_with_filters: _Optional[_Iterable[_Union[WebhookSubscription, _Mapping]]] = ...,
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

class TestWebhookRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TestWebhookResponse(_message.Message):
    __slots__ = ("success", "status_code", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_code: int
    error_message: str
    def __init__(
        self, success: bool = ..., status_code: _Optional[int] = ..., error_message: _Optional[str] = ...
    ) -> None: ...

class GetWebhookSubscriptionFilterOptionsRequest(_message.Message):
    __slots__ = ("subscription",)
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    subscription: str
    def __init__(self, subscription: _Optional[str] = ...) -> None: ...

class GetWebhookSubscriptionFilterOptionsResponse(_message.Message):
    __slots__ = ("options",)
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    options: _containers.RepeatedCompositeFieldContainer[WebhookSubscriptionFilterOption]
    def __init__(
        self, options: _Optional[_Iterable[_Union[WebhookSubscriptionFilterOption, _Mapping]]] = ...
    ) -> None: ...
