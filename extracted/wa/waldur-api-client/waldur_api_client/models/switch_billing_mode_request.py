from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_mode_enum import BillingModeEnum

T = TypeVar("T", bound="SwitchBillingModeRequest")


@_attrs_define
class SwitchBillingModeRequest:
    """
    Attributes:
        billing_mode (BillingModeEnum):
    """

    billing_mode: BillingModeEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        billing_mode = self.billing_mode.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "billing_mode": billing_mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        billing_mode = BillingModeEnum(d.pop("billing_mode"))

        switch_billing_mode_request = cls(
            billing_mode=billing_mode,
        )

        switch_billing_mode_request.additional_properties = d
        return switch_billing_mode_request

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
