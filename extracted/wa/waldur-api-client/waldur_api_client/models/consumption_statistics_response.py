from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.period_breakdown import PeriodBreakdown


T = TypeVar("T", bound="ConsumptionStatisticsResponse")


@_attrs_define
class ConsumptionStatisticsResponse:
    """
    Attributes:
        total_records (int):
        pending_records (int):
        finalized_records (int):
        reconciled_records (int):
        total_consumed_sell (str):
        total_adjustments (str):
        period_breakdown (list['PeriodBreakdown']):
    """

    total_records: int
    pending_records: int
    finalized_records: int
    reconciled_records: int
    total_consumed_sell: str
    total_adjustments: str
    period_breakdown: list["PeriodBreakdown"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_records = self.total_records

        pending_records = self.pending_records

        finalized_records = self.finalized_records

        reconciled_records = self.reconciled_records

        total_consumed_sell = self.total_consumed_sell

        total_adjustments = self.total_adjustments

        period_breakdown = []
        for period_breakdown_item_data in self.period_breakdown:
            period_breakdown_item = period_breakdown_item_data.to_dict()
            period_breakdown.append(period_breakdown_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_records": total_records,
                "pending_records": pending_records,
                "finalized_records": finalized_records,
                "reconciled_records": reconciled_records,
                "total_consumed_sell": total_consumed_sell,
                "total_adjustments": total_adjustments,
                "period_breakdown": period_breakdown,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.period_breakdown import PeriodBreakdown

        d = dict(src_dict)
        total_records = d.pop("total_records")

        pending_records = d.pop("pending_records")

        finalized_records = d.pop("finalized_records")

        reconciled_records = d.pop("reconciled_records")

        total_consumed_sell = d.pop("total_consumed_sell")

        total_adjustments = d.pop("total_adjustments")

        period_breakdown = []
        _period_breakdown = d.pop("period_breakdown")
        for period_breakdown_item_data in _period_breakdown:
            period_breakdown_item = PeriodBreakdown.from_dict(period_breakdown_item_data)

            period_breakdown.append(period_breakdown_item)

        consumption_statistics_response = cls(
            total_records=total_records,
            pending_records=pending_records,
            finalized_records=finalized_records,
            reconciled_records=reconciled_records,
            total_consumed_sell=total_consumed_sell,
            total_adjustments=total_adjustments,
            period_breakdown=period_breakdown,
        )

        consumption_statistics_response.additional_properties = d
        return consumption_statistics_response

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
