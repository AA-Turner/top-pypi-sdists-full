from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MarketplaceProviderOfferingsStatsRetrieveResponse200")


@_attrs_define
class MarketplaceProviderOfferingsStatsRetrieveResponse200:
    """
    Attributes:
        resources_count (Union[Unset, int]):
        customers_count (Union[Unset, int]):
    """

    resources_count: Union[Unset, int] = UNSET
    customers_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resources_count = self.resources_count

        customers_count = self.customers_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resources_count is not UNSET:
            field_dict["resources_count"] = resources_count
        if customers_count is not UNSET:
            field_dict["customers_count"] = customers_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resources_count = d.pop("resources_count", UNSET)

        customers_count = d.pop("customers_count", UNSET)

        marketplace_provider_offerings_stats_retrieve_response_200 = cls(
            resources_count=resources_count,
            customers_count=customers_count,
        )

        marketplace_provider_offerings_stats_retrieve_response_200.additional_properties = d
        return marketplace_provider_offerings_stats_retrieve_response_200

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
