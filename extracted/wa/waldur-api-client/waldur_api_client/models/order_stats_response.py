from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.daily_order_stats import DailyOrderStats
    from ..models.order_stats_response_by_state import OrderStatsResponseByState
    from ..models.order_stats_response_by_type import OrderStatsResponseByType
    from ..models.order_stats_summary import OrderStatsSummary


T = TypeVar("T", bound="OrderStatsResponse")


@_attrs_define
class OrderStatsResponse:
    """
    Attributes:
        summary (OrderStatsSummary):
        by_state (OrderStatsResponseByState): Total order counts grouped by state
        by_type (OrderStatsResponseByType): Total order counts grouped by type
        daily (list['DailyOrderStats']): Daily breakdown
    """

    summary: "OrderStatsSummary"
    by_state: "OrderStatsResponseByState"
    by_type: "OrderStatsResponseByType"
    daily: list["DailyOrderStats"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        summary = self.summary.to_dict()

        by_state = self.by_state.to_dict()

        by_type = self.by_type.to_dict()

        daily = []
        for daily_item_data in self.daily:
            daily_item = daily_item_data.to_dict()
            daily.append(daily_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summary": summary,
                "by_state": by_state,
                "by_type": by_type,
                "daily": daily,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_order_stats import DailyOrderStats
        from ..models.order_stats_response_by_state import OrderStatsResponseByState
        from ..models.order_stats_response_by_type import OrderStatsResponseByType
        from ..models.order_stats_summary import OrderStatsSummary

        d = dict(src_dict)
        summary = OrderStatsSummary.from_dict(d.pop("summary"))

        by_state = OrderStatsResponseByState.from_dict(d.pop("by_state"))

        by_type = OrderStatsResponseByType.from_dict(d.pop("by_type"))

        daily = []
        _daily = d.pop("daily")
        for daily_item_data in _daily:
            daily_item = DailyOrderStats.from_dict(daily_item_data)

            daily.append(daily_item)

        order_stats_response = cls(
            summary=summary,
            by_state=by_state,
            by_type=by_type,
            daily=daily,
        )

        order_stats_response.additional_properties = d
        return order_stats_response

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
