from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.growth_period_enum import GrowthPeriodEnum

T = TypeVar("T", bound="TableGrowthAlert")


@_attrs_define
class TableGrowthAlert:
    """
    Attributes:
        table_name (str): Name of the table triggering the alert
        period (GrowthPeriodEnum):
        growth_percent (float): Actual growth percentage observed
        threshold (int): Configured threshold that was exceeded
    """

    table_name: str
    period: GrowthPeriodEnum
    growth_percent: float
    threshold: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        table_name = self.table_name

        period = self.period.value

        growth_percent = self.growth_percent

        threshold = self.threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "table_name": table_name,
                "period": period,
                "growth_percent": growth_percent,
                "threshold": threshold,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        table_name = d.pop("table_name")

        period = GrowthPeriodEnum(d.pop("period"))

        growth_percent = d.pop("growth_percent")

        threshold = d.pop("threshold")

        table_growth_alert = cls(
            table_name=table_name,
            period=period,
            growth_percent=growth_percent,
            threshold=threshold,
        )

        table_growth_alert.additional_properties = d
        return table_growth_alert

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
