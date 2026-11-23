from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.fresh_billing_usage_freshness import FreshBillingUsageFreshness

if TYPE_CHECKING:
    from ..models.daily_usage import DailyUsage
    from ..models.rated_breakdown import RatedBreakdown
    from ..models.usage_quantity import UsageQuantity


T = TypeVar("T", bound="FreshBillingUsage")


@_attrs_define
class FreshBillingUsage:
    """
    Attributes:
        freshness (FreshBillingUsageFreshness):
        quantities (list[UsageQuantity]):
        breakdown (list[RatedBreakdown]):
        daily_usage (list[DailyUsage]):
        as_of_unix_seconds (int):
        period_start_unix_seconds (int):
        period_end_unix_seconds (int):
    """

    freshness: FreshBillingUsageFreshness
    quantities: list[UsageQuantity]
    breakdown: list[RatedBreakdown]
    daily_usage: list[DailyUsage]
    as_of_unix_seconds: int
    period_start_unix_seconds: int
    period_end_unix_seconds: int

    def to_dict(self) -> dict[str, Any]:
        freshness = self.freshness.value

        quantities = []
        for quantities_item_data in self.quantities:
            quantities_item = quantities_item_data.to_dict()
            quantities.append(quantities_item)

        breakdown = []
        for breakdown_item_data in self.breakdown:
            breakdown_item = breakdown_item_data.to_dict()
            breakdown.append(breakdown_item)

        daily_usage = []
        for daily_usage_item_data in self.daily_usage:
            daily_usage_item = daily_usage_item_data.to_dict()
            daily_usage.append(daily_usage_item)

        as_of_unix_seconds = self.as_of_unix_seconds

        period_start_unix_seconds = self.period_start_unix_seconds

        period_end_unix_seconds = self.period_end_unix_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "freshness": freshness,
                "quantities": quantities,
                "breakdown": breakdown,
                "daily_usage": daily_usage,
                "as_of_unix_seconds": as_of_unix_seconds,
                "period_start_unix_seconds": period_start_unix_seconds,
                "period_end_unix_seconds": period_end_unix_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_usage import DailyUsage
        from ..models.rated_breakdown import RatedBreakdown
        from ..models.usage_quantity import UsageQuantity

        d = dict(src_dict)
        freshness = FreshBillingUsageFreshness(d.pop("freshness"))

        quantities = []
        _quantities = d.pop("quantities")
        for quantities_item_data in _quantities:
            quantities_item = UsageQuantity.from_dict(quantities_item_data)

            quantities.append(quantities_item)

        breakdown = []
        _breakdown = d.pop("breakdown")
        for breakdown_item_data in _breakdown:
            breakdown_item = RatedBreakdown.from_dict(breakdown_item_data)

            breakdown.append(breakdown_item)

        daily_usage = []
        _daily_usage = d.pop("daily_usage")
        for daily_usage_item_data in _daily_usage:
            daily_usage_item = DailyUsage.from_dict(daily_usage_item_data)

            daily_usage.append(daily_usage_item)

        as_of_unix_seconds = d.pop("as_of_unix_seconds")

        period_start_unix_seconds = d.pop("period_start_unix_seconds")

        period_end_unix_seconds = d.pop("period_end_unix_seconds")

        fresh_billing_usage = cls(
            freshness=freshness,
            quantities=quantities,
            breakdown=breakdown,
            daily_usage=daily_usage,
            as_of_unix_seconds=as_of_unix_seconds,
            period_start_unix_seconds=period_start_unix_seconds,
            period_end_unix_seconds=period_end_unix_seconds,
        )

        return fresh_billing_usage
