from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.edit_webhook_json_body_events_item import EditWebhookJsonBodyEventsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="EditWebhookJsonBody")


@_attrs_define
class EditWebhookJsonBody:
    """
    Attributes:
        webhook (Union[Unset, str]): the URL to POST events to. Omitted or empty removes the webhook.
        events (Union[Unset, None, List[EditWebhookJsonBodyEventsItem]]): event types to send, at least one. Omitted
            keeps the stored filter, null sends every event.
    """

    webhook: Union[Unset, str] = UNSET
    events: Union[Unset, None, List[EditWebhookJsonBodyEventsItem]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        webhook = self.webhook
        events: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.events, Unset):
            if self.events is None:
                events = None
            else:
                events = []
                for events_item_data in self.events:
                    events_item = events_item_data.value

                    events.append(events_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if webhook is not UNSET:
            field_dict["webhook"] = webhook
        if events is not UNSET:
            field_dict["events"] = events

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        webhook = d.pop("webhook", UNSET)

        events = []
        _events = d.pop("events", UNSET)
        for events_item_data in _events or []:
            events_item = EditWebhookJsonBodyEventsItem(events_item_data)

            events.append(events_item)

        edit_webhook_json_body = cls(
            webhook=webhook,
            events=events,
        )

        edit_webhook_json_body.additional_properties = d
        return edit_webhook_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
