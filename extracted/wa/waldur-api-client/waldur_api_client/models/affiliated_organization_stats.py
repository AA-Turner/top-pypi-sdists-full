from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AffiliatedOrganizationStats")


@_attrs_define
class AffiliatedOrganizationStats:
    """
    Attributes:
        active_projects_count (int):
        resources_count (int):
        estimated_monthly_cost (str):
    """

    active_projects_count: int
    resources_count: int
    estimated_monthly_cost: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active_projects_count = self.active_projects_count

        resources_count = self.resources_count

        estimated_monthly_cost = self.estimated_monthly_cost

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active_projects_count": active_projects_count,
                "resources_count": resources_count,
                "estimated_monthly_cost": estimated_monthly_cost,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active_projects_count = d.pop("active_projects_count")

        resources_count = d.pop("resources_count")

        estimated_monthly_cost = d.pop("estimated_monthly_cost")

        affiliated_organization_stats = cls(
            active_projects_count=active_projects_count,
            resources_count=resources_count,
            estimated_monthly_cost=estimated_monthly_cost,
        )

        affiliated_organization_stats.additional_properties = d
        return affiliated_organization_stats

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
