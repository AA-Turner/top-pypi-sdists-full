from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedPlanComponent")


@_attrs_define
class NestedPlanComponent:
    """
    Attributes:
        type_ (Union[Unset, str]): Unique internal name of the measured unit, for example floating_ip.
        name (Union[Unset, str]): Display name for the measured unit, for example, Floating IP.
        measured_unit (Union[Unset, str]): Unit of measurement, for example, GB.
        amount (Union[Unset, int]):
        price (Union[Unset, str]):
        future_price (Union[None, Unset, str]):
        discount_threshold (Union[None, Unset, int]): Minimum amount to be eligible for discount.
        discount_rate (Union[None, Unset, int]): Discount rate in percentage.
    """

    type_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    measured_unit: Union[Unset, str] = UNSET
    amount: Union[Unset, int] = UNSET
    price: Union[Unset, str] = UNSET
    future_price: Union[None, Unset, str] = UNSET
    discount_threshold: Union[None, Unset, int] = UNSET
    discount_rate: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        name = self.name

        measured_unit = self.measured_unit

        amount = self.amount

        price = self.price

        future_price: Union[None, Unset, str]
        if isinstance(self.future_price, Unset):
            future_price = UNSET
        else:
            future_price = self.future_price

        discount_threshold: Union[None, Unset, int]
        if isinstance(self.discount_threshold, Unset):
            discount_threshold = UNSET
        else:
            discount_threshold = self.discount_threshold

        discount_rate: Union[None, Unset, int]
        if isinstance(self.discount_rate, Unset):
            discount_rate = UNSET
        else:
            discount_rate = self.discount_rate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if measured_unit is not UNSET:
            field_dict["measured_unit"] = measured_unit
        if amount is not UNSET:
            field_dict["amount"] = amount
        if price is not UNSET:
            field_dict["price"] = price
        if future_price is not UNSET:
            field_dict["future_price"] = future_price
        if discount_threshold is not UNSET:
            field_dict["discount_threshold"] = discount_threshold
        if discount_rate is not UNSET:
            field_dict["discount_rate"] = discount_rate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        name = d.pop("name", UNSET)

        measured_unit = d.pop("measured_unit", UNSET)

        amount = d.pop("amount", UNSET)

        price = d.pop("price", UNSET)

        def _parse_future_price(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        future_price = _parse_future_price(d.pop("future_price", UNSET))

        def _parse_discount_threshold(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        discount_threshold = _parse_discount_threshold(d.pop("discount_threshold", UNSET))

        def _parse_discount_rate(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        discount_rate = _parse_discount_rate(d.pop("discount_rate", UNSET))

        nested_plan_component = cls(
            type_=type_,
            name=name,
            measured_unit=measured_unit,
            amount=amount,
            price=price,
            future_price=future_price,
            discount_threshold=discount_threshold,
            discount_rate=discount_rate,
        )

        nested_plan_component.additional_properties = d
        return nested_plan_component

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
