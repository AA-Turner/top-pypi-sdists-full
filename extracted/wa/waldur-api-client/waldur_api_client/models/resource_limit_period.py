from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceLimitPeriod")


@_attrs_define
class ResourceLimitPeriod:
    """
    Attributes:
        start (Union[Unset, str]): Start date of the resource limit period
        end (Union[Unset, str]): End date of the resource limit period
        quantity (Union[Unset, int]): Quantity of resources consumed during this period
        billing_periods (Union[Unset, int]): Number of billing periods
        total (Union[Unset, str]): Total amount for this period
    """

    start: Union[Unset, str] = UNSET
    end: Union[Unset, str] = UNSET
    quantity: Union[Unset, int] = UNSET
    billing_periods: Union[Unset, int] = UNSET
    total: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start = self.start

        end = self.end

        quantity = self.quantity

        billing_periods = self.billing_periods

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if billing_periods is not UNSET:
            field_dict["billing_periods"] = billing_periods
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start = d.pop("start", UNSET)

        end = d.pop("end", UNSET)

        quantity = d.pop("quantity", UNSET)

        billing_periods = d.pop("billing_periods", UNSET)

        total = d.pop("total", UNSET)

        resource_limit_period = cls(
            start=start,
            end=end,
            quantity=quantity,
            billing_periods=billing_periods,
            total=total,
        )

        resource_limit_period.additional_properties = d
        return resource_limit_period

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
