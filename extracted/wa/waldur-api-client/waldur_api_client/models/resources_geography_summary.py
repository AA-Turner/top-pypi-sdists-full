from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourcesGeographySummary")


@_attrs_define
class ResourcesGeographySummary:
    """
    Attributes:
        total_resources (int): Total number of active resources
        countries_count (int): Number of countries with active resources
        org_groups_count (int): Number of organization groups with active resources
        offerings_count (int): Number of offerings with active resources
    """

    total_resources: int
    countries_count: int
    org_groups_count: int
    offerings_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_resources = self.total_resources

        countries_count = self.countries_count

        org_groups_count = self.org_groups_count

        offerings_count = self.offerings_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_resources": total_resources,
                "countries_count": countries_count,
                "org_groups_count": org_groups_count,
                "offerings_count": offerings_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_resources = d.pop("total_resources")

        countries_count = d.pop("countries_count")

        org_groups_count = d.pop("org_groups_count")

        offerings_count = d.pop("offerings_count")

        resources_geography_summary = cls(
            total_resources=total_resources,
            countries_count=countries_count,
            org_groups_count=org_groups_count,
            offerings_count=offerings_count,
        )

        resources_geography_summary.additional_properties = d
        return resources_geography_summary

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
