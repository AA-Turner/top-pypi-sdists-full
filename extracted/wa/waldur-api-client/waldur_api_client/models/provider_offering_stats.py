from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.provider_offering_stats_offerings_item import ProviderOfferingStatsOfferingsItem


T = TypeVar("T", bound="ProviderOfferingStats")


@_attrs_define
class ProviderOfferingStats:
    """
    Attributes:
        offerings (list['ProviderOfferingStatsOfferingsItem']): Offering statistics including resources, revenue, and
            utilization
    """

    offerings: list["ProviderOfferingStatsOfferingsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offerings = []
        for offerings_item_data in self.offerings:
            offerings_item = offerings_item_data.to_dict()
            offerings.append(offerings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offerings": offerings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_offering_stats_offerings_item import ProviderOfferingStatsOfferingsItem

        d = dict(src_dict)
        offerings = []
        _offerings = d.pop("offerings")
        for offerings_item_data in _offerings:
            offerings_item = ProviderOfferingStatsOfferingsItem.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        provider_offering_stats = cls(
            offerings=offerings,
        )

        provider_offering_stats.additional_properties = d
        return provider_offering_stats

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
