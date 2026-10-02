from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingCostsSummary")


@_attrs_define
class OfferingCostsSummary:
    """
    Attributes:
        total_cost (str): Total cost of all active resources across all offerings
        offering_count (int): Number of offerings with active resources
        average_cost (str): Average cost per offering
    """

    total_cost: str
    offering_count: int
    average_cost: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_cost = self.total_cost

        offering_count = self.offering_count

        average_cost = self.average_cost

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_cost": total_cost,
                "offering_count": offering_count,
                "average_cost": average_cost,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_cost = d.pop("total_cost")

        offering_count = d.pop("offering_count")

        average_cost = d.pop("average_cost")

        offering_costs_summary = cls(
            total_cost=total_cost,
            offering_count=offering_count,
            average_cost=average_cost,
        )

        offering_costs_summary.additional_properties = d
        return offering_costs_summary

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
