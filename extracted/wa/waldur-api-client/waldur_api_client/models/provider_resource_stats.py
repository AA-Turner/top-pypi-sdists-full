from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.provider_resource_stats_by_offering_item import ProviderResourceStatsByOfferingItem
    from ..models.provider_resource_stats_by_state import ProviderResourceStatsByState
    from ..models.provider_resource_stats_monthly_item import ProviderResourceStatsMonthlyItem


T = TypeVar("T", bound="ProviderResourceStats")


@_attrs_define
class ProviderResourceStats:
    """
    Attributes:
        total (int): Total number of resources
        by_state (ProviderResourceStatsByState): Resource counts grouped by state
        by_offering (list['ProviderResourceStatsByOfferingItem']): Resource counts grouped by offering
        monthly (list['ProviderResourceStatsMonthlyItem']): Monthly resource counts
    """

    total: int
    by_state: "ProviderResourceStatsByState"
    by_offering: list["ProviderResourceStatsByOfferingItem"]
    monthly: list["ProviderResourceStatsMonthlyItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        by_state = self.by_state.to_dict()

        by_offering = []
        for by_offering_item_data in self.by_offering:
            by_offering_item = by_offering_item_data.to_dict()
            by_offering.append(by_offering_item)

        monthly = []
        for monthly_item_data in self.monthly:
            monthly_item = monthly_item_data.to_dict()
            monthly.append(monthly_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "by_state": by_state,
                "by_offering": by_offering,
                "monthly": monthly,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_resource_stats_by_offering_item import ProviderResourceStatsByOfferingItem
        from ..models.provider_resource_stats_by_state import ProviderResourceStatsByState
        from ..models.provider_resource_stats_monthly_item import ProviderResourceStatsMonthlyItem

        d = dict(src_dict)
        total = d.pop("total")

        by_state = ProviderResourceStatsByState.from_dict(d.pop("by_state"))

        by_offering = []
        _by_offering = d.pop("by_offering")
        for by_offering_item_data in _by_offering:
            by_offering_item = ProviderResourceStatsByOfferingItem.from_dict(by_offering_item_data)

            by_offering.append(by_offering_item)

        monthly = []
        _monthly = d.pop("monthly")
        for monthly_item_data in _monthly:
            monthly_item = ProviderResourceStatsMonthlyItem.from_dict(monthly_item_data)

            monthly.append(monthly_item)

        provider_resource_stats = cls(
            total=total,
            by_state=by_state,
            by_offering=by_offering,
            monthly=monthly,
        )

        provider_resource_stats.additional_properties = d
        return provider_resource_stats

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
