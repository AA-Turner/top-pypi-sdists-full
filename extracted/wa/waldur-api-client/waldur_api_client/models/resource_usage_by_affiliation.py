from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourceUsageByAffiliation")


@_attrs_define
class ResourceUsageByAffiliation:
    """
    Attributes:
        affiliation (str): User affiliation value
        component_type (str): Component type
        total_usage (str): Total usage
        total_cost (str): Total cost
        resource_count (int): Number of resources
    """

    affiliation: str
    component_type: str
    total_usage: str
    total_cost: str
    resource_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        affiliation = self.affiliation

        component_type = self.component_type

        total_usage = self.total_usage

        total_cost = self.total_cost

        resource_count = self.resource_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "affiliation": affiliation,
                "component_type": component_type,
                "total_usage": total_usage,
                "total_cost": total_cost,
                "resource_count": resource_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        affiliation = d.pop("affiliation")

        component_type = d.pop("component_type")

        total_usage = d.pop("total_usage")

        total_cost = d.pop("total_cost")

        resource_count = d.pop("resource_count")

        resource_usage_by_affiliation = cls(
            affiliation=affiliation,
            component_type=component_type,
            total_usage=total_usage,
            total_cost=total_cost,
            resource_count=resource_count,
        )

        resource_usage_by_affiliation.additional_properties = d
        return resource_usage_by_affiliation

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
