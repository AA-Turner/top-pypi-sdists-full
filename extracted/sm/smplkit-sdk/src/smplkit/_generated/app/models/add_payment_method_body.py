from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.add_payment_method_data import AddPaymentMethodData


T = TypeVar("T", bound="AddPaymentMethodBody")


@_attrs_define
class AddPaymentMethodBody:
    """JSON:API request envelope for registering a new payment method.

    Example:
        {'data': {'attributes': {'default': False, 'stripe_payment_method_id': 'pm_1234567890abcdef'}, 'type':
            'payment_method'}}

    Attributes:
        data (AddPaymentMethodData): Resource object for the add-payment-method request.
    """

    data: AddPaymentMethodData
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_payment_method_data import AddPaymentMethodData

        d = dict(src_dict)
        data = AddPaymentMethodData.from_dict(d.pop("data"))

        add_payment_method_body = cls(
            data=data,
        )

        add_payment_method_body.additional_properties = d
        return add_payment_method_body

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
