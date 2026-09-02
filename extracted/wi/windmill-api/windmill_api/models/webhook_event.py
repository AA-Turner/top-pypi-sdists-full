from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.webhook_event_request_type import WebhookEventRequestType
from ..models.webhook_event_type import WebhookEventType

T = TypeVar("T", bound="WebhookEvent")


@_attrs_define
class WebhookEvent:
    """
    Attributes:
        type (WebhookEventType):
        request_type (WebhookEventRequestType): The type of webhook request (define possible values here)
    """

    type: WebhookEventType
    request_type: WebhookEventRequestType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        request_type = self.request_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "request_type": request_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = WebhookEventType(d.pop("type"))

        request_type = WebhookEventRequestType(d.pop("request_type"))

        webhook_event = cls(
            type=type,
            request_type=request_type,
        )

        webhook_event.additional_properties = d
        return webhook_event

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
