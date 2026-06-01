from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.add_payment_method_data_type import AddPaymentMethodDataType
from ..models.add_payment_method_data_type import check_add_payment_method_data_type

if TYPE_CHECKING:
    from ..models.add_payment_method_attributes import AddPaymentMethodAttributes


T = TypeVar("T", bound="AddPaymentMethodData")


@_attrs_define
class AddPaymentMethodData:
    """Resource object for the add-payment-method request.

    Attributes:
        type_ (AddPaymentMethodDataType):
        attributes (AddPaymentMethodAttributes): Attributes accepted when registering a new payment method.

            The customer first creates a Stripe payment method client-side using
            Stripe Elements, then submits its `pm_...` identifier here to persist
            it on the account. Example: {'default': False, 'stripe_payment_method_id': 'pm_1234567890abcdef'}.
    """

    type_: AddPaymentMethodDataType
    attributes: AddPaymentMethodAttributes
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_payment_method_attributes import AddPaymentMethodAttributes

        d = dict(src_dict)
        type_ = check_add_payment_method_data_type(d.pop("type"))

        attributes = AddPaymentMethodAttributes.from_dict(d.pop("attributes"))

        add_payment_method_data = cls(
            type_=type_,
            attributes=attributes,
        )

        add_payment_method_data.additional_properties = d
        return add_payment_method_data

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
