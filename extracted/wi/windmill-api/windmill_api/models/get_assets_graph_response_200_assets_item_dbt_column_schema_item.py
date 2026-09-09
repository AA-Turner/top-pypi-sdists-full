from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAssetsGraphResponse200AssetsItemDbtColumnSchemaItem")


@_attrs_define
class GetAssetsGraphResponse200AssetsItemDbtColumnSchemaItem:
    """
    Attributes:
        name (str):
        type (Union[Unset, str]): The declared type where `schema.yml` gives one, else the inferred one. Omitted when
            neither is known.
    """

    name: str
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = d.pop("type", UNSET)

        get_assets_graph_response_200_assets_item_dbt_column_schema_item = cls(
            name=name,
            type=type,
        )

        get_assets_graph_response_200_assets_item_dbt_column_schema_item.additional_properties = d
        return get_assets_graph_response_200_assets_item_dbt_column_schema_item

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
