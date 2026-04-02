from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.invoice_growth_customer_period import InvoiceGrowthCustomerPeriod


T = TypeVar("T", bound="InvoiceGrowth")


@_attrs_define
class InvoiceGrowth:
    """
    Attributes:
        periods (list[str]):
        total_periods (list[float]):
        other_periods (list[float]):
        customer_periods (list['InvoiceGrowthCustomerPeriod']):
    """

    periods: list[str]
    total_periods: list[float]
    other_periods: list[float]
    customer_periods: list["InvoiceGrowthCustomerPeriod"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        periods = self.periods

        total_periods = self.total_periods

        other_periods = self.other_periods

        customer_periods = []
        for customer_periods_item_data in self.customer_periods:
            customer_periods_item = customer_periods_item_data.to_dict()
            customer_periods.append(customer_periods_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "periods": periods,
                "total_periods": total_periods,
                "other_periods": other_periods,
                "customer_periods": customer_periods,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invoice_growth_customer_period import InvoiceGrowthCustomerPeriod

        d = dict(src_dict)
        periods = cast(list[str], d.pop("periods"))

        total_periods = cast(list[float], d.pop("total_periods"))

        other_periods = cast(list[float], d.pop("other_periods"))

        customer_periods = []
        _customer_periods = d.pop("customer_periods")
        for customer_periods_item_data in _customer_periods:
            customer_periods_item = InvoiceGrowthCustomerPeriod.from_dict(customer_periods_item_data)

            customer_periods.append(customer_periods_item)

        invoice_growth = cls(
            periods=periods,
            total_periods=total_periods,
            other_periods=other_periods,
            customer_periods=customer_periods,
        )

        invoice_growth.additional_properties = d
        return invoice_growth

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
