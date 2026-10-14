from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_type_enum import BillingTypeEnum
from ..models.discount_aggregation_enum import DiscountAggregationEnum
from ..models.limit_period_enum import LimitPeriodEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedPlanComponent")


@_attrs_define
class NestedPlanComponent:
    """
    Attributes:
        type_ (Union[Unset, str]): Unique internal name of the measured unit, for example floating_ip.
        name (Union[Unset, str]): Display name for the measured unit, for example, Floating IP.
        measured_unit (Union[None, Unset, str]):
        billing_type (Union[Unset, BillingTypeEnum]):
        is_prepaid (Union[Unset, bool]):
        limit_period (Union[Unset, LimitPeriodEnum]):
        amount (Union[Unset, int]):
        price (Union[Unset, str]):
        future_price (Union[None, Unset, str]):
        discount_formula (Union[Unset, str]): Volume discount formula evaluated with the billed quantity bound to
            `usage`; returns a discount percentage (clamped to 0-100). Empty means no discount. Example: '10 if usage >= 100
            else 0'.
        discount_aggregation (Union[Unset, DiscountAggregationEnum]):
        discount_description (Union[None, Unset, str]):
    """

    type_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    measured_unit: Union[None, Unset, str] = UNSET
    billing_type: Union[Unset, BillingTypeEnum] = UNSET
    is_prepaid: Union[Unset, bool] = UNSET
    limit_period: Union[Unset, LimitPeriodEnum] = UNSET
    amount: Union[Unset, int] = UNSET
    price: Union[Unset, str] = UNSET
    future_price: Union[None, Unset, str] = UNSET
    discount_formula: Union[Unset, str] = UNSET
    discount_aggregation: Union[Unset, DiscountAggregationEnum] = UNSET
    discount_description: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        name = self.name

        measured_unit: Union[None, Unset, str]
        if isinstance(self.measured_unit, Unset):
            measured_unit = UNSET
        else:
            measured_unit = self.measured_unit

        billing_type: Union[Unset, str] = UNSET
        if not isinstance(self.billing_type, Unset):
            billing_type = self.billing_type.value

        is_prepaid = self.is_prepaid

        limit_period: Union[Unset, str] = UNSET
        if not isinstance(self.limit_period, Unset):
            limit_period = self.limit_period.value

        amount = self.amount

        price = self.price

        future_price: Union[None, Unset, str]
        if isinstance(self.future_price, Unset):
            future_price = UNSET
        else:
            future_price = self.future_price

        discount_formula = self.discount_formula

        discount_aggregation: Union[Unset, str] = UNSET
        if not isinstance(self.discount_aggregation, Unset):
            discount_aggregation = self.discount_aggregation.value

        discount_description: Union[None, Unset, str]
        if isinstance(self.discount_description, Unset):
            discount_description = UNSET
        else:
            discount_description = self.discount_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if measured_unit is not UNSET:
            field_dict["measured_unit"] = measured_unit
        if billing_type is not UNSET:
            field_dict["billing_type"] = billing_type
        if is_prepaid is not UNSET:
            field_dict["is_prepaid"] = is_prepaid
        if limit_period is not UNSET:
            field_dict["limit_period"] = limit_period
        if amount is not UNSET:
            field_dict["amount"] = amount
        if price is not UNSET:
            field_dict["price"] = price
        if future_price is not UNSET:
            field_dict["future_price"] = future_price
        if discount_formula is not UNSET:
            field_dict["discount_formula"] = discount_formula
        if discount_aggregation is not UNSET:
            field_dict["discount_aggregation"] = discount_aggregation
        if discount_description is not UNSET:
            field_dict["discount_description"] = discount_description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        name = d.pop("name", UNSET)

        def _parse_measured_unit(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        measured_unit = _parse_measured_unit(d.pop("measured_unit", UNSET))

        _billing_type = d.pop("billing_type", UNSET)
        billing_type: Union[Unset, BillingTypeEnum]
        if isinstance(_billing_type, Unset):
            billing_type = UNSET
        else:
            billing_type = BillingTypeEnum(_billing_type)

        is_prepaid = d.pop("is_prepaid", UNSET)

        _limit_period = d.pop("limit_period", UNSET)
        limit_period: Union[Unset, LimitPeriodEnum]
        if isinstance(_limit_period, Unset):
            limit_period = UNSET
        else:
            limit_period = LimitPeriodEnum(_limit_period)

        amount = d.pop("amount", UNSET)

        price = d.pop("price", UNSET)

        def _parse_future_price(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        future_price = _parse_future_price(d.pop("future_price", UNSET))

        discount_formula = d.pop("discount_formula", UNSET)

        _discount_aggregation = d.pop("discount_aggregation", UNSET)
        discount_aggregation: Union[Unset, DiscountAggregationEnum]
        if isinstance(_discount_aggregation, Unset):
            discount_aggregation = UNSET
        else:
            discount_aggregation = DiscountAggregationEnum(_discount_aggregation)

        def _parse_discount_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        discount_description = _parse_discount_description(d.pop("discount_description", UNSET))

        nested_plan_component = cls(
            type_=type_,
            name=name,
            measured_unit=measured_unit,
            billing_type=billing_type,
            is_prepaid=is_prepaid,
            limit_period=limit_period,
            amount=amount,
            price=price,
            future_price=future_price,
            discount_formula=discount_formula,
            discount_aggregation=discount_aggregation,
            discount_description=discount_description,
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
