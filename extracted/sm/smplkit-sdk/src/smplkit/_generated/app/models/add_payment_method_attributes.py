from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


T = TypeVar("T", bound="AddPaymentMethodAttributes")


@_attrs_define
class AddPaymentMethodAttributes:
    """Attributes accepted when registering a new payment method.

    The customer first creates a Stripe payment method client-side using
    Stripe Elements, then submits its `pm_...` identifier here to persist
    it on the account.

        Example:
            {'default': False, 'stripe_payment_method_id': 'pm_1234567890abcdef'}

        Attributes:
            stripe_payment_method_id (str): Identifier of the Stripe payment method to register on the account, e.g.
                `pm_1234567890abcdef`.
            default (bool | Unset): When `true`, make the newly registered payment method the account's default. The first
                payment method on an account is always set as default regardless of this field. Default: False.
    """

    stripe_payment_method_id: str
    default: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stripe_payment_method_id = self.stripe_payment_method_id

        default = self.default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stripe_payment_method_id": stripe_payment_method_id,
            }
        )
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stripe_payment_method_id = d.pop("stripe_payment_method_id")

        default = d.pop("default", UNSET)

        add_payment_method_attributes = cls(
            stripe_payment_method_id=stripe_payment_method_id,
            default=default,
        )

        add_payment_method_attributes.additional_properties = d
        return add_payment_method_attributes

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
