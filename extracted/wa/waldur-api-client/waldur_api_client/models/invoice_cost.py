from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.invoice_cost_item import InvoiceCostItem


T = TypeVar("T", bound="InvoiceCost")


@_attrs_define
class InvoiceCost:
    """
    Attributes:
        price (float):
        year (int):
        month (int):
        items (Union[Unset, list['InvoiceCostItem']]):
    """

    price: float
    year: int
    month: int
    items: Union[Unset, list["InvoiceCostItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        price = self.price

        year = self.year

        month = self.month

        items: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()
                items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "price": price,
                "year": year,
                "month": month,
            }
        )
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invoice_cost_item import InvoiceCostItem

        d = dict(src_dict)
        price = d.pop("price")

        year = d.pop("year")

        month = d.pop("month")

        items = []
        _items = d.pop("items", UNSET)
        for items_item_data in _items or []:
            items_item = InvoiceCostItem.from_dict(items_item_data)

            items.append(items_item)

        invoice_cost = cls(
            price=price,
            year=year,
            month=month,
            items=items,
        )

        invoice_cost.additional_properties = d
        return invoice_cost

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
