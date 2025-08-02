from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_global_settings_response_200_item_value import ListGlobalSettingsResponse200ItemValue


T = TypeVar("T", bound="ListGlobalSettingsResponse200Item")


@_attrs_define
class ListGlobalSettingsResponse200Item:
    """
    Attributes:
        name (str):
        value (ListGlobalSettingsResponse200ItemValue):
    """

    name: str
    value: "ListGlobalSettingsResponse200ItemValue"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        value = self.value.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_global_settings_response_200_item_value import ListGlobalSettingsResponse200ItemValue

        d = src_dict.copy()
        name = d.pop("name")

        value = ListGlobalSettingsResponse200ItemValue.from_dict(d.pop("value"))

        list_global_settings_response_200_item = cls(
            name=name,
            value=value,
        )

        list_global_settings_response_200_item.additional_properties = d
        return list_global_settings_response_200_item

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
