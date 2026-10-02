from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AggregatedUsageTrend")


@_attrs_define
class AggregatedUsageTrend:
    """
    Attributes:
        period (str): Period in YYYY-MM format
        year (int): Year
        month (int): Month (1-12)
        total_usage (str): Total usage across all components
        resource_count (int): Number of distinct resources with usage
        component_count (int): Number of component usage records
    """

    period: str
    year: int
    month: int
    total_usage: str
    resource_count: int
    component_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period

        year = self.year

        month = self.month

        total_usage = self.total_usage

        resource_count = self.resource_count

        component_count = self.component_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
                "year": year,
                "month": month,
                "total_usage": total_usage,
                "resource_count": resource_count,
                "component_count": component_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period = d.pop("period")

        year = d.pop("year")

        month = d.pop("month")

        total_usage = d.pop("total_usage")

        resource_count = d.pop("resource_count")

        component_count = d.pop("component_count")

        aggregated_usage_trend = cls(
            period=period,
            year=year,
            month=month,
            total_usage=total_usage,
            resource_count=resource_count,
            component_count=component_count,
        )

        aggregated_usage_trend.additional_properties = d
        return aggregated_usage_trend

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
