import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.daily_order_stats_by_state import DailyOrderStatsByState
    from ..models.daily_order_stats_by_type import DailyOrderStatsByType


T = TypeVar("T", bound="DailyOrderStats")


@_attrs_define
class DailyOrderStats:
    """
    Attributes:
        date (datetime.date): Date of the statistics
        total (int): Total number of orders
        total_cost (Union[None, str]): Total cost of orders
        revenue (Union[None, str]): Revenue from create/update orders
        by_state (DailyOrderStatsByState): Order counts grouped by state
        by_type (DailyOrderStatsByType): Order counts grouped by type
    """

    date: datetime.date
    total: int
    total_cost: Union[None, str]
    revenue: Union[None, str]
    by_state: "DailyOrderStatsByState"
    by_type: "DailyOrderStatsByType"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        total = self.total

        total_cost: Union[None, str]
        total_cost = self.total_cost

        revenue: Union[None, str]
        revenue = self.revenue

        by_state = self.by_state.to_dict()

        by_type = self.by_type.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "total": total,
                "total_cost": total_cost,
                "revenue": revenue,
                "by_state": by_state,
                "by_type": by_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_order_stats_by_state import DailyOrderStatsByState
        from ..models.daily_order_stats_by_type import DailyOrderStatsByType

        d = dict(src_dict)
        date = isoparse(d.pop("date")).date()

        total = d.pop("total")

        def _parse_total_cost(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        total_cost = _parse_total_cost(d.pop("total_cost"))

        def _parse_revenue(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        revenue = _parse_revenue(d.pop("revenue"))

        by_state = DailyOrderStatsByState.from_dict(d.pop("by_state"))

        by_type = DailyOrderStatsByType.from_dict(d.pop("by_type"))

        daily_order_stats = cls(
            date=date,
            total=total,
            total_cost=total_cost,
            revenue=revenue,
            by_state=by_state,
            by_type=by_type,
        )

        daily_order_stats.additional_properties = d
        return daily_order_stats

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
