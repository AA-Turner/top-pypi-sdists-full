import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.table_growth_alert import TableGrowthAlert
    from ..models.table_growth_stats import TableGrowthStats


T = TypeVar("T", bound="TableGrowthStatsResponse")


@_attrs_define
class TableGrowthStatsResponse:
    """
    Attributes:
        date (datetime.date): Current date of the statistics
        weekly_threshold_percent (int): Configured weekly growth alert threshold
        monthly_threshold_percent (int): Configured monthly growth alert threshold
        tables (list['TableGrowthStats']): Table growth statistics sorted by growth rate
        alerts (list['TableGrowthAlert']): List of tables that exceeded configured growth thresholds
    """

    date: datetime.date
    weekly_threshold_percent: int
    monthly_threshold_percent: int
    tables: list["TableGrowthStats"]
    alerts: list["TableGrowthAlert"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        weekly_threshold_percent = self.weekly_threshold_percent

        monthly_threshold_percent = self.monthly_threshold_percent

        tables = []
        for tables_item_data in self.tables:
            tables_item = tables_item_data.to_dict()
            tables.append(tables_item)

        alerts = []
        for alerts_item_data in self.alerts:
            alerts_item = alerts_item_data.to_dict()
            alerts.append(alerts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "weekly_threshold_percent": weekly_threshold_percent,
                "monthly_threshold_percent": monthly_threshold_percent,
                "tables": tables,
                "alerts": alerts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.table_growth_alert import TableGrowthAlert
        from ..models.table_growth_stats import TableGrowthStats

        d = dict(src_dict)
        date = isoparse(d.pop("date")).date()

        weekly_threshold_percent = d.pop("weekly_threshold_percent")

        monthly_threshold_percent = d.pop("monthly_threshold_percent")

        tables = []
        _tables = d.pop("tables")
        for tables_item_data in _tables:
            tables_item = TableGrowthStats.from_dict(tables_item_data)

            tables.append(tables_item)

        alerts = []
        _alerts = d.pop("alerts")
        for alerts_item_data in _alerts:
            alerts_item = TableGrowthAlert.from_dict(alerts_item_data)

            alerts.append(alerts_item)

        table_growth_stats_response = cls(
            date=date,
            weekly_threshold_percent=weekly_threshold_percent,
            monthly_threshold_percent=monthly_threshold_percent,
            tables=tables,
            alerts=alerts,
        )

        table_growth_stats_response.additional_properties = d
        return table_growth_stats_response

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
