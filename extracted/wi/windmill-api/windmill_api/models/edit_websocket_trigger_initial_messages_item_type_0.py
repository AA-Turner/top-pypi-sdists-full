from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EditWebsocketTriggerInitialMessagesItemType0")


@_attrs_define
class EditWebsocketTriggerInitialMessagesItemType0:
    """
    Attributes:
        raw_message (str):
    """

    raw_message: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        raw_message = self.raw_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "raw_message": raw_message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        raw_message = d.pop("raw_message")

        edit_websocket_trigger_initial_messages_item_type_0 = cls(
            raw_message=raw_message,
        )

        edit_websocket_trigger_initial_messages_item_type_0.additional_properties = d
        return edit_websocket_trigger_initial_messages_item_type_0

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
