import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.daily_maintenance_stats_by_state import DailyMaintenanceStatsByState


T = TypeVar("T", bound="DailyMaintenanceStats")


@_attrs_define
class DailyMaintenanceStats:
    """
    Attributes:
        date (datetime.date): Date
        count (int): Number of maintenances on this day
        by_state (DailyMaintenanceStatsByState): Maintenance counts grouped by state
    """

    date: datetime.date
    count: int
    by_state: "DailyMaintenanceStatsByState"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        count = self.count

        by_state = self.by_state.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "count": count,
                "by_state": by_state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_maintenance_stats_by_state import DailyMaintenanceStatsByState

        d = dict(src_dict)
        date = isoparse(d.pop("date")).date()

        count = d.pop("count")

        by_state = DailyMaintenanceStatsByState.from_dict(d.pop("by_state"))

        daily_maintenance_stats = cls(
            date=date,
            count=count,
            by_state=by_state,
        )

        daily_maintenance_stats.additional_properties = d
        return daily_maintenance_stats

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
