from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedPriceEstimate")


@_attrs_define
class NestedPriceEstimate:
    """
    Attributes:
        total (Union[Unset, str]):
        current (Union[Unset, str]):
        tax (Union[Unset, str]):
        tax_current (Union[Unset, str]):
    """

    total: Union[Unset, str] = UNSET
    current: Union[Unset, str] = UNSET
    tax: Union[Unset, str] = UNSET
    tax_current: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        current = self.current

        tax = self.tax

        tax_current = self.tax_current

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total is not UNSET:
            field_dict["total"] = total
        if current is not UNSET:
            field_dict["current"] = current
        if tax is not UNSET:
            field_dict["tax"] = tax
        if tax_current is not UNSET:
            field_dict["tax_current"] = tax_current

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total = d.pop("total", UNSET)

        current = d.pop("current", UNSET)

        tax = d.pop("tax", UNSET)

        tax_current = d.pop("tax_current", UNSET)

        nested_price_estimate = cls(
            total=total,
            current=current,
            tax=tax,
            tax_current=tax_current,
        )

        nested_price_estimate.additional_properties = d
        return nested_price_estimate

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
