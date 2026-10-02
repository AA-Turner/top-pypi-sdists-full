from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProviderOfferingCosts")


@_attrs_define
class ProviderOfferingCosts:
    """
    Attributes:
        period (str): Billing period (YYYY-MM)
        price (float): Price amount excluding tax
        tax (float): Tax amount
        total (float): Total amount including tax
    """

    period: str
    price: float
    tax: float
    total: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period

        price = self.price

        tax = self.tax

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
                "price": price,
                "tax": tax,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period = d.pop("period")

        price = d.pop("price")

        tax = d.pop("tax")

        total = d.pop("total")

        provider_offering_costs = cls(
            period=period,
            price=price,
            tax=tax,
            total=total,
        )

        provider_offering_costs.additional_properties = d
        return provider_offering_costs

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
