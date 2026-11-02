from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListSearchResourceResponse200Item")


@_attrs_define
class ListSearchResourceResponse200Item:
    """
    Attributes:
        path (str):
        value (str): pretty-printed JSON rendering of the resource value, capped at 4000 characters — a search preview,
            not the value itself (use get_value for that)
        truncated (bool): whether value was cut short by that cap
    """

    path: str
    value: str
    truncated: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        value = self.value
        truncated = self.truncated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "value": value,
                "truncated": truncated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        value = d.pop("value")

        truncated = d.pop("truncated")

        list_search_resource_response_200_item = cls(
            path=path,
            value=value,
            truncated=truncated,
        )

        list_search_resource_response_200_item.additional_properties = d
        return list_search_resource_response_200_item

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
