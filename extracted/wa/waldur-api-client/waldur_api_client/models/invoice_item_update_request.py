import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="InvoiceItemUpdateRequest")


@_attrs_define
class InvoiceItemUpdateRequest:
    """
    Attributes:
        article_code (Union[Unset, str]):
        quantity (Union[Unset, str]):
        unit_price (Union[Unset, str]):
        start (Union[Unset, datetime.datetime]): Date and time when item usage has started.
        end (Union[Unset, datetime.datetime]): Date and time when item usage has ended.
    """

    article_code: Union[Unset, str] = UNSET
    quantity: Union[Unset, str] = UNSET
    unit_price: Union[Unset, str] = UNSET
    start: Union[Unset, datetime.datetime] = UNSET
    end: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        article_code = self.article_code

        quantity = self.quantity

        unit_price = self.unit_price

        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        end: Union[Unset, str] = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if article_code is not UNSET:
            field_dict["article_code"] = article_code
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if unit_price is not UNSET:
            field_dict["unit_price"] = unit_price
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        article_code = d.pop("article_code", UNSET)

        quantity = d.pop("quantity", UNSET)

        unit_price = d.pop("unit_price", UNSET)

        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.datetime]
        if isinstance(_start, Unset):
            start = UNSET
        else:
            start = isoparse(_start)

        _end = d.pop("end", UNSET)
        end: Union[Unset, datetime.datetime]
        if isinstance(_end, Unset):
            end = UNSET
        else:
            end = isoparse(_end)

        invoice_item_update_request = cls(
            article_code=article_code,
            quantity=quantity,
            unit_price=unit_price,
            start=start,
            end=end,
        )

        invoice_item_update_request.additional_properties = d
        return invoice_item_update_request

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
