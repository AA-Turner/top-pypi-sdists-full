from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_type_enum import BillingTypeEnum
from ..models.limit_period_enum import LimitPeriodEnum

T = TypeVar("T", bound="BillingModeComponent")


@_attrs_define
class BillingModeComponent:
    """
    Attributes:
        type_ (str):
        billing_type (BillingTypeEnum):
        measured_unit (str):
        is_prepaid (bool):
        limit_period (LimitPeriodEnum):
    """

    type_: str
    billing_type: BillingTypeEnum
    measured_unit: str
    is_prepaid: bool
    limit_period: LimitPeriodEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        billing_type = self.billing_type.value

        measured_unit = self.measured_unit

        is_prepaid = self.is_prepaid

        limit_period = self.limit_period.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "billing_type": billing_type,
                "measured_unit": measured_unit,
                "is_prepaid": is_prepaid,
                "limit_period": limit_period,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        billing_type = BillingTypeEnum(d.pop("billing_type"))

        measured_unit = d.pop("measured_unit")

        is_prepaid = d.pop("is_prepaid")

        limit_period = LimitPeriodEnum(d.pop("limit_period"))

        billing_mode_component = cls(
            type_=type_,
            billing_type=billing_type,
            measured_unit=measured_unit,
            is_prepaid=is_prepaid,
            limit_period=limit_period,
        )

        billing_mode_component.additional_properties = d
        return billing_mode_component

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
