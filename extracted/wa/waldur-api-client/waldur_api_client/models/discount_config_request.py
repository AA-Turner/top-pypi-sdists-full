from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.discount_aggregation_enum import DiscountAggregationEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="DiscountConfigRequest")


@_attrs_define
class DiscountConfigRequest:
    """
    Attributes:
        discount_formula (Union[None, Unset, str]): Volume discount formula evaluated with the billed quantity bound to
            `usage`; returns a discount percentage (0-100). Empty removes the discount. Example: '10 if usage >= 100 else
            0'.
        discount_aggregation (Union[Unset, DiscountAggregationEnum]):
    """

    discount_formula: Union[None, Unset, str] = UNSET
    discount_aggregation: Union[Unset, DiscountAggregationEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        discount_formula: Union[None, Unset, str]
        if isinstance(self.discount_formula, Unset):
            discount_formula = UNSET
        else:
            discount_formula = self.discount_formula

        discount_aggregation: Union[Unset, str] = UNSET
        if not isinstance(self.discount_aggregation, Unset):
            discount_aggregation = self.discount_aggregation.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if discount_formula is not UNSET:
            field_dict["discount_formula"] = discount_formula
        if discount_aggregation is not UNSET:
            field_dict["discount_aggregation"] = discount_aggregation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_discount_formula(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        discount_formula = _parse_discount_formula(d.pop("discount_formula", UNSET))

        _discount_aggregation = d.pop("discount_aggregation", UNSET)
        discount_aggregation: Union[Unset, DiscountAggregationEnum]
        if isinstance(_discount_aggregation, Unset):
            discount_aggregation = UNSET
        else:
            discount_aggregation = DiscountAggregationEnum(_discount_aggregation)

        discount_config_request = cls(
            discount_formula=discount_formula,
            discount_aggregation=discount_aggregation,
        )

        discount_config_request.additional_properties = d
        return discount_config_request

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
