from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_assets_response_200_assets_item_usages_item_columns_additional_property import (
    ListAssetsResponse200AssetsItemUsagesItemColumnsAdditionalProperty,
)

T = TypeVar("T", bound="ListAssetsResponse200AssetsItemUsagesItemColumns")


@_attrs_define
class ListAssetsResponse200AssetsItemUsagesItemColumns:
    """The columns used (for tables)"""

    additional_properties: Dict[str, ListAssetsResponse200AssetsItemUsagesItemColumnsAdditionalProperty] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.value

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        list_assets_response_200_assets_item_usages_item_columns = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ListAssetsResponse200AssetsItemUsagesItemColumnsAdditionalProperty(prop_dict)

            additional_properties[prop_name] = additional_property

        list_assets_response_200_assets_item_usages_item_columns.additional_properties = additional_properties
        return list_assets_response_200_assets_item_usages_item_columns

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> ListAssetsResponse200AssetsItemUsagesItemColumnsAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: ListAssetsResponse200AssetsItemUsagesItemColumnsAdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
