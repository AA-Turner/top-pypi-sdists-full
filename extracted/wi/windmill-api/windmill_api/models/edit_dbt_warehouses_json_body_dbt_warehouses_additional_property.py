from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditDbtWarehousesJsonBodyDbtWarehousesAdditionalProperty")


@_attrs_define
class EditDbtWarehousesJsonBodyDbtWarehousesAdditionalProperty:
    """
    Attributes:
        resource_path (str):
        target (Union[Unset, str]):
    """

    resource_path: str
    target: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resource_path = self.resource_path
        target = self.target

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_path": resource_path,
            }
        )
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        resource_path = d.pop("resource_path")

        target = d.pop("target", UNSET)

        edit_dbt_warehouses_json_body_dbt_warehouses_additional_property = cls(
            resource_path=resource_path,
            target=target,
        )

        edit_dbt_warehouses_json_body_dbt_warehouses_additional_property.additional_properties = d
        return edit_dbt_warehouses_json_body_dbt_warehouses_additional_property

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
