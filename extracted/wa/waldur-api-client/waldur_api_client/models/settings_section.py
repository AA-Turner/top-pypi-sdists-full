from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.settings_item import SettingsItem


T = TypeVar("T", bound="SettingsSection")


@_attrs_define
class SettingsSection:
    """
    Attributes:
        description (str):
        items (list['SettingsItem']):
    """

    description: str
    items: list["SettingsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.settings_item import SettingsItem

        d = dict(src_dict)
        description = d.pop("description")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = SettingsItem.from_dict(items_item_data)

            items.append(items_item)

        settings_section = cls(
            description=description,
            items=items,
        )

        settings_section.additional_properties = d
        return settings_section

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
