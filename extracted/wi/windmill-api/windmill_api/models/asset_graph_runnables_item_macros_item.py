from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AssetGraphRunnablesItemMacrosItem")


@_attrs_define
class AssetGraphRunnablesItemMacrosItem:
    """
    Attributes:
        name (str):
        params (str): verbatim parameter list
        is_table (bool):
    """

    name: str
    params: str
    is_table: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        params = self.params
        is_table = self.is_table

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "params": params,
                "is_table": is_table,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        params = d.pop("params")

        is_table = d.pop("is_table")

        asset_graph_runnables_item_macros_item = cls(
            name=name,
            params=params,
            is_table=is_table,
        )

        asset_graph_runnables_item_macros_item.additional_properties = d
        return asset_graph_runnables_item_macros_item

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
