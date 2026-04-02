from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InvoiceCostItem")


@_attrs_define
class InvoiceCostItem:
    """
    Attributes:
        name (str):
        unit_price (str):
        unit (str):
        quantity (str):
        measured_unit (str):
        price (float):
    """

    name: str
    unit_price: str
    unit: str
    quantity: str
    measured_unit: str
    price: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        unit_price = self.unit_price

        unit = self.unit

        quantity = self.quantity

        measured_unit = self.measured_unit

        price = self.price

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "unit_price": unit_price,
                "unit": unit,
                "quantity": quantity,
                "measured_unit": measured_unit,
                "price": price,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        unit_price = d.pop("unit_price")

        unit = d.pop("unit")

        quantity = d.pop("quantity")

        measured_unit = d.pop("measured_unit")

        price = d.pop("price")

        invoice_cost_item = cls(
            name=name,
            unit_price=unit_price,
            unit=unit,
            quantity=quantity,
            measured_unit=measured_unit,
            price=price,
        )

        invoice_cost_item.additional_properties = d
        return invoice_cost_item

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
