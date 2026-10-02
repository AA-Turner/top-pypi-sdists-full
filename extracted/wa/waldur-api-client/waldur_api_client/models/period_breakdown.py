from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PeriodBreakdown")


@_attrs_define
class PeriodBreakdown:
    """
    Attributes:
        period (str):
        count (int):
        consumed_sell (str):
        finalized_count (int):
        reconciled_count (int):
    """

    period: str
    count: int
    consumed_sell: str
    finalized_count: int
    reconciled_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period

        count = self.count

        consumed_sell = self.consumed_sell

        finalized_count = self.finalized_count

        reconciled_count = self.reconciled_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
                "count": count,
                "consumed_sell": consumed_sell,
                "finalized_count": finalized_count,
                "reconciled_count": reconciled_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period = d.pop("period")

        count = d.pop("count")

        consumed_sell = d.pop("consumed_sell")

        finalized_count = d.pop("finalized_count")

        reconciled_count = d.pop("reconciled_count")

        period_breakdown = cls(
            period=period,
            count=count,
            consumed_sell=consumed_sell,
            finalized_count=finalized_count,
            reconciled_count=reconciled_count,
        )

        period_breakdown.additional_properties = d
        return period_breakdown

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
