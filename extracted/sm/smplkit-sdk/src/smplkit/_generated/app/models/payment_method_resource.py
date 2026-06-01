from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.payment_method_resource_type import check_payment_method_resource_type
from ..models.payment_method_resource_type import PaymentMethodResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.payment_method import PaymentMethod


T = TypeVar("T", bound="PaymentMethodResource")


@_attrs_define
class PaymentMethodResource:
    """JSON:API resource envelope for a payment method.

    `id` must not be specified for create requests (the server assigns it).

        Example:
            {'attributes': {'billing_details': {'email': 'jane@example.com', 'name': 'Jane Doe'}, 'brand': 'visa',
                'created_at': '2026-04-23T12:34:56Z', 'default': True, 'exp_month': 8, 'exp_year': 2028, 'last4': '4242',
                'updated_at': '2026-04-23T12:34:56Z'}, 'id': '0b8a9c9e-1111-2222-3333-444455556666', 'type': 'payment_method'}

        Attributes:
            type_ (PaymentMethodResourceType):
            attributes (PaymentMethod): A saved card on file for the account, used to charge subscription
                invoices.

                The default payment method is changed via the `set_default` action
                rather than by updating this field through PUT. Example: {'billing_details': {'address': {'city': 'Leesburg',
                'country': 'US', 'line1': '123 Main St', 'postal_code': '20175', 'state': 'VA'}, 'email': 'jane@example.com',
                'name': 'Jane Doe'}, 'brand': 'visa', 'created_at': '2026-04-23T12:34:56Z', 'default': True, 'exp_month': 8,
                'exp_year': 2028, 'last4': '4242', 'updated_at': '2026-04-23T12:34:56Z'}.
            id (None | str | Unset):
    """

    type_: PaymentMethodResourceType
    attributes: PaymentMethod
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.payment_method import PaymentMethod

        d = dict(src_dict)
        type_ = check_payment_method_resource_type(d.pop("type"))

        attributes = PaymentMethod.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        payment_method_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        payment_method_resource.additional_properties = d
        return payment_method_resource

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
