from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="DiscountTier")


@_attrs_define
class DiscountTier:
    """A single tier of the multi-product volume discount schedule.

    Attributes:
        products_count (int): Minimum number of paid product subscriptions a customer must hold for this tier's discount
            to apply. Counts above the highest defined tier are clamped to that tier.
        percent_off (int): Discount percentage applied to every paid subscription item when the customer holds at least
            ``products_count`` paid products. 0 means no discount at this tier.
    """

    products_count: int
    percent_off: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        products_count = self.products_count

        percent_off = self.percent_off

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "products_count": products_count,
                "percent_off": percent_off,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        products_count = d.pop("products_count")

        percent_off = d.pop("percent_off")

        discount_tier = cls(
            products_count=products_count,
            percent_off=percent_off,
        )

        discount_tier.additional_properties = d
        return discount_tier

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
