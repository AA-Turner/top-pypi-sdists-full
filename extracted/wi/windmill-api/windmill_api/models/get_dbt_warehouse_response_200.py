from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetDbtWarehouseResponse200")


@_attrs_define
class GetDbtWarehouseResponse200:
    """
    Attributes:
        value (Any): the resolved resource, rendered into profiles.yml
        target (Union[Unset, str]):
        resource_type (Union[Unset, str]): decides whether the value is translated into a profiles.yml target or already
            is one
    """

    value: Any
    target: Union[Unset, str] = UNSET
    resource_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        target = self.target
        resource_type = self.resource_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )
        if target is not UNSET:
            field_dict["target"] = target
        if resource_type is not UNSET:
            field_dict["resource_type"] = resource_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        target = d.pop("target", UNSET)

        resource_type = d.pop("resource_type", UNSET)

        get_dbt_warehouse_response_200 = cls(
            value=value,
            target=target,
            resource_type=resource_type,
        )

        get_dbt_warehouse_response_200.additional_properties = d
        return get_dbt_warehouse_response_200

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
