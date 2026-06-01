from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="NextTierResponse")


@_attrs_define
class NextTierResponse:
    """Hint describing how the customer could unlock a better discount.

    Attributes:
        products_needed (int): Number of additional paid products required to reach the next discount tier.
        discount_pct (int): Discount percentage that would apply at the next tier.
        additional_savings_cents (int): Estimated additional monthly savings (in cents) at the next tier, compared to
            paying full list price for the added product.
    """

    products_needed: int
    discount_pct: int
    additional_savings_cents: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        products_needed = self.products_needed

        discount_pct = self.discount_pct

        additional_savings_cents = self.additional_savings_cents

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "products_needed": products_needed,
                "discount_pct": discount_pct,
                "additional_savings_cents": additional_savings_cents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        products_needed = d.pop("products_needed")

        discount_pct = d.pop("discount_pct")

        additional_savings_cents = d.pop("additional_savings_cents")

        next_tier_response = cls(
            products_needed=products_needed,
            discount_pct=discount_pct,
            additional_savings_cents=additional_savings_cents,
        )

        next_tier_response.additional_properties = d
        return next_tier_response

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
