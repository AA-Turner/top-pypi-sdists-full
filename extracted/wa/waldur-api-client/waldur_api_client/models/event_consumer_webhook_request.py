from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.observable_object_type_enum import ObservableObjectTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.event_consumer_scope_input_request import EventConsumerScopeInputRequest
    from ..models.event_consumer_webhook_request_payload_filters import EventConsumerWebhookRequestPayloadFilters


T = TypeVar("T", bound="EventConsumerWebhookRequest")


@_attrs_define
class EventConsumerWebhookRequest:
    """
    Attributes:
        webhook_url (str): HTTP(S) URL the messages are POSTed to as JSON. May carry its credential in the query string;
            it is stored as a secret and never returned.
        payload_filters (Union[Unset, EventConsumerWebhookRequestPayloadFilters]): Allow-list over message fields, e.g.
            {"role_name": ["CUSTOMER.OWNER"], "scope_type": ["customer"]}. A message is delivered only if every listed field
            holds one of its values.
        object_types (Union[Unset, list[ObservableObjectTypeEnum]]): Observable object types to receive. An explicit
            empty list means all types; omitting the field leaves an existing consumer's filter unchanged.
        scopes (Union[Unset, list['EventConsumerScopeInputRequest']]): Entity bindings this consumer receives events for
            — e.g. several projects, a customer, an offering, or your own user (type 'user', your own UUID) for identity
            events. You may only bind to an entity you hold a role on, or to yourself. AN EMPTY LIST MEANS GLOBAL (every
            event, including all-user PII) and is staff/support only.
    """

    webhook_url: str
    payload_filters: Union[Unset, "EventConsumerWebhookRequestPayloadFilters"] = UNSET
    object_types: Union[Unset, list[ObservableObjectTypeEnum]] = UNSET
    scopes: Union[Unset, list["EventConsumerScopeInputRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        webhook_url = self.webhook_url

        payload_filters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.payload_filters, Unset):
            payload_filters = self.payload_filters.to_dict()

        object_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.object_types, Unset):
            object_types = []
            for object_types_item_data in self.object_types:
                object_types_item = object_types_item_data.value
                object_types.append(object_types_item)

        scopes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = []
            for scopes_item_data in self.scopes:
                scopes_item = scopes_item_data.to_dict()
                scopes.append(scopes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "webhook_url": webhook_url,
            }
        )
        if payload_filters is not UNSET:
            field_dict["payload_filters"] = payload_filters
        if object_types is not UNSET:
            field_dict["object_types"] = object_types
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.event_consumer_scope_input_request import EventConsumerScopeInputRequest
        from ..models.event_consumer_webhook_request_payload_filters import EventConsumerWebhookRequestPayloadFilters

        d = dict(src_dict)
        webhook_url = d.pop("webhook_url")

        _payload_filters = d.pop("payload_filters", UNSET)
        payload_filters: Union[Unset, EventConsumerWebhookRequestPayloadFilters]
        if isinstance(_payload_filters, Unset):
            payload_filters = UNSET
        else:
            payload_filters = EventConsumerWebhookRequestPayloadFilters.from_dict(_payload_filters)

        object_types = []
        _object_types = d.pop("object_types", UNSET)
        for object_types_item_data in _object_types or []:
            object_types_item = ObservableObjectTypeEnum(object_types_item_data)

            object_types.append(object_types_item)

        scopes = []
        _scopes = d.pop("scopes", UNSET)
        for scopes_item_data in _scopes or []:
            scopes_item = EventConsumerScopeInputRequest.from_dict(scopes_item_data)

            scopes.append(scopes_item)

        event_consumer_webhook_request = cls(
            webhook_url=webhook_url,
            payload_filters=payload_filters,
            object_types=object_types,
            scopes=scopes,
        )

        event_consumer_webhook_request.additional_properties = d
        return event_consumer_webhook_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
