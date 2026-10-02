from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.feature_item import FeatureItem


T = TypeVar("T", bound="FeatureSection")


@_attrs_define
class FeatureSection:
    """
    Attributes:
        key (str):
        description (str):
        items (list['FeatureItem']):
    """

    key: str
    description: str
    items: list["FeatureItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        description = self.description

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "description": description,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.feature_item import FeatureItem

        d = dict(src_dict)
        key = d.pop("key")

        description = d.pop("description")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = FeatureItem.from_dict(items_item_data)

            items.append(items_item)

        feature_section = cls(
            key=key,
            description=description,
            items=items,
        )

        feature_section.additional_properties = d
        return feature_section

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
