from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TableGrowthStats")


@_attrs_define
class TableGrowthStats:
    """
    Attributes:
        table_name (str): Name of the database table
        current_total_size (int): Current total size including indexes in bytes
        current_data_size (int): Current data-only size in bytes
        current_row_estimate (Union[None, int]): Current estimated row count
        week_ago_total_size (Union[None, int]): Total size from 7 days ago in bytes
        week_ago_row_estimate (Union[None, int]): Row estimate from 7 days ago
        month_ago_total_size (Union[None, int]): Total size from 30 days ago in bytes
        month_ago_row_estimate (Union[None, int]): Row estimate from 30 days ago
        weekly_growth_percent (Union[None, float]): Percentage growth over the past week
        monthly_growth_percent (Union[None, float]): Percentage growth over the past month
        weekly_row_growth_percent (Union[None, float]): Percentage row count growth over the past week
        monthly_row_growth_percent (Union[None, float]): Percentage row count growth over the past month
    """

    table_name: str
    current_total_size: int
    current_data_size: int
    current_row_estimate: Union[None, int]
    week_ago_total_size: Union[None, int]
    week_ago_row_estimate: Union[None, int]
    month_ago_total_size: Union[None, int]
    month_ago_row_estimate: Union[None, int]
    weekly_growth_percent: Union[None, float]
    monthly_growth_percent: Union[None, float]
    weekly_row_growth_percent: Union[None, float]
    monthly_row_growth_percent: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        table_name = self.table_name

        current_total_size = self.current_total_size

        current_data_size = self.current_data_size

        current_row_estimate: Union[None, int]
        current_row_estimate = self.current_row_estimate

        week_ago_total_size: Union[None, int]
        week_ago_total_size = self.week_ago_total_size

        week_ago_row_estimate: Union[None, int]
        week_ago_row_estimate = self.week_ago_row_estimate

        month_ago_total_size: Union[None, int]
        month_ago_total_size = self.month_ago_total_size

        month_ago_row_estimate: Union[None, int]
        month_ago_row_estimate = self.month_ago_row_estimate

        weekly_growth_percent: Union[None, float]
        weekly_growth_percent = self.weekly_growth_percent

        monthly_growth_percent: Union[None, float]
        monthly_growth_percent = self.monthly_growth_percent

        weekly_row_growth_percent: Union[None, float]
        weekly_row_growth_percent = self.weekly_row_growth_percent

        monthly_row_growth_percent: Union[None, float]
        monthly_row_growth_percent = self.monthly_row_growth_percent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "table_name": table_name,
                "current_total_size": current_total_size,
                "current_data_size": current_data_size,
                "current_row_estimate": current_row_estimate,
                "week_ago_total_size": week_ago_total_size,
                "week_ago_row_estimate": week_ago_row_estimate,
                "month_ago_total_size": month_ago_total_size,
                "month_ago_row_estimate": month_ago_row_estimate,
                "weekly_growth_percent": weekly_growth_percent,
                "monthly_growth_percent": monthly_growth_percent,
                "weekly_row_growth_percent": weekly_row_growth_percent,
                "monthly_row_growth_percent": monthly_row_growth_percent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        table_name = d.pop("table_name")

        current_total_size = d.pop("current_total_size")

        current_data_size = d.pop("current_data_size")

        def _parse_current_row_estimate(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        current_row_estimate = _parse_current_row_estimate(d.pop("current_row_estimate"))

        def _parse_week_ago_total_size(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        week_ago_total_size = _parse_week_ago_total_size(d.pop("week_ago_total_size"))

        def _parse_week_ago_row_estimate(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        week_ago_row_estimate = _parse_week_ago_row_estimate(d.pop("week_ago_row_estimate"))

        def _parse_month_ago_total_size(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        month_ago_total_size = _parse_month_ago_total_size(d.pop("month_ago_total_size"))

        def _parse_month_ago_row_estimate(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        month_ago_row_estimate = _parse_month_ago_row_estimate(d.pop("month_ago_row_estimate"))

        def _parse_weekly_growth_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        weekly_growth_percent = _parse_weekly_growth_percent(d.pop("weekly_growth_percent"))

        def _parse_monthly_growth_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        monthly_growth_percent = _parse_monthly_growth_percent(d.pop("monthly_growth_percent"))

        def _parse_weekly_row_growth_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        weekly_row_growth_percent = _parse_weekly_row_growth_percent(d.pop("weekly_row_growth_percent"))

        def _parse_monthly_row_growth_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        monthly_row_growth_percent = _parse_monthly_row_growth_percent(d.pop("monthly_row_growth_percent"))

        table_growth_stats = cls(
            table_name=table_name,
            current_total_size=current_total_size,
            current_data_size=current_data_size,
            current_row_estimate=current_row_estimate,
            week_ago_total_size=week_ago_total_size,
            week_ago_row_estimate=week_ago_row_estimate,
            month_ago_total_size=month_ago_total_size,
            month_ago_row_estimate=month_ago_row_estimate,
            weekly_growth_percent=weekly_growth_percent,
            monthly_growth_percent=monthly_growth_percent,
            weekly_row_growth_percent=weekly_row_growth_percent,
            monthly_row_growth_percent=monthly_row_growth_percent,
        )

        table_growth_stats.additional_properties = d
        return table_growth_stats

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
