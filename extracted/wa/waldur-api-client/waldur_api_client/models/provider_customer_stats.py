from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.provider_customer_stats_monthly_item import ProviderCustomerStatsMonthlyItem
    from ..models.provider_customer_stats_top_by_resources_item import ProviderCustomerStatsTopByResourcesItem
    from ..models.provider_customer_stats_top_by_revenue_item import ProviderCustomerStatsTopByRevenueItem


T = TypeVar("T", bound="ProviderCustomerStats")


@_attrs_define
class ProviderCustomerStats:
    """
    Attributes:
        total (int): Total number of customers
        new_this_month (int): New customers this month
        top_by_revenue (list['ProviderCustomerStatsTopByRevenueItem']): Top customers by revenue
        top_by_resources (list['ProviderCustomerStatsTopByResourcesItem']): Top customers by resource count
        monthly (list['ProviderCustomerStatsMonthlyItem']): Monthly customer counts
    """

    total: int
    new_this_month: int
    top_by_revenue: list["ProviderCustomerStatsTopByRevenueItem"]
    top_by_resources: list["ProviderCustomerStatsTopByResourcesItem"]
    monthly: list["ProviderCustomerStatsMonthlyItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        new_this_month = self.new_this_month

        top_by_revenue = []
        for top_by_revenue_item_data in self.top_by_revenue:
            top_by_revenue_item = top_by_revenue_item_data.to_dict()
            top_by_revenue.append(top_by_revenue_item)

        top_by_resources = []
        for top_by_resources_item_data in self.top_by_resources:
            top_by_resources_item = top_by_resources_item_data.to_dict()
            top_by_resources.append(top_by_resources_item)

        monthly = []
        for monthly_item_data in self.monthly:
            monthly_item = monthly_item_data.to_dict()
            monthly.append(monthly_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "new_this_month": new_this_month,
                "top_by_revenue": top_by_revenue,
                "top_by_resources": top_by_resources,
                "monthly": monthly,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_customer_stats_monthly_item import ProviderCustomerStatsMonthlyItem
        from ..models.provider_customer_stats_top_by_resources_item import ProviderCustomerStatsTopByResourcesItem
        from ..models.provider_customer_stats_top_by_revenue_item import ProviderCustomerStatsTopByRevenueItem

        d = dict(src_dict)
        total = d.pop("total")

        new_this_month = d.pop("new_this_month")

        top_by_revenue = []
        _top_by_revenue = d.pop("top_by_revenue")
        for top_by_revenue_item_data in _top_by_revenue:
            top_by_revenue_item = ProviderCustomerStatsTopByRevenueItem.from_dict(top_by_revenue_item_data)

            top_by_revenue.append(top_by_revenue_item)

        top_by_resources = []
        _top_by_resources = d.pop("top_by_resources")
        for top_by_resources_item_data in _top_by_resources:
            top_by_resources_item = ProviderCustomerStatsTopByResourcesItem.from_dict(top_by_resources_item_data)

            top_by_resources.append(top_by_resources_item)

        monthly = []
        _monthly = d.pop("monthly")
        for monthly_item_data in _monthly:
            monthly_item = ProviderCustomerStatsMonthlyItem.from_dict(monthly_item_data)

            monthly.append(monthly_item)

        provider_customer_stats = cls(
            total=total,
            new_this_month=new_this_month,
            top_by_revenue=top_by_revenue,
            top_by_resources=top_by_resources,
            monthly=monthly,
        )

        provider_customer_stats.additional_properties = d
        return provider_customer_stats

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
