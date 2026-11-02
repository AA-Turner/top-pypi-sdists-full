from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AssetGraphMacroEdgesItem")


@_attrs_define
class AssetGraphMacroEdgesItem:
    """
    Attributes:
        lib_path (str):
        consumer_path (str):
        macro_names (List[str]):
        via_use (bool):
    """

    lib_path: str
    consumer_path: str
    macro_names: List[str]
    via_use: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        lib_path = self.lib_path
        consumer_path = self.consumer_path
        macro_names = self.macro_names

        via_use = self.via_use

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lib_path": lib_path,
                "consumer_path": consumer_path,
                "macro_names": macro_names,
                "via_use": via_use,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        lib_path = d.pop("lib_path")

        consumer_path = d.pop("consumer_path")

        macro_names = cast(List[str], d.pop("macro_names"))

        via_use = d.pop("via_use")

        asset_graph_macro_edges_item = cls(
            lib_path=lib_path,
            consumer_path=consumer_path,
            macro_names=macro_names,
            via_use=via_use,
        )

        asset_graph_macro_edges_item.additional_properties = d
        return asset_graph_macro_edges_item

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
