from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UpdateWebsocketTriggerJsonBodyFiltersItem")


@_attrs_define
class UpdateWebsocketTriggerJsonBodyFiltersItem:
    """
    Attributes:
        key (str):
        value (Any):
    """

    key: str
    value: Any
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        value = d.pop("value")

        update_websocket_trigger_json_body_filters_item = cls(
            key=key,
            value=value,
        )

        update_websocket_trigger_json_body_filters_item.additional_properties = d
        return update_websocket_trigger_json_body_filters_item

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
