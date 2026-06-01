from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.payment_method_resource import PaymentMethodResource


T = TypeVar("T", bound="PaymentMethodResponse")


@_attrs_define
class PaymentMethodResponse:
    """JSON:API single-resource response envelope for a payment method.

    Attributes:
        data (PaymentMethodResource): JSON:API resource envelope for a payment method.

            `id` must not be specified for create requests (the server assigns it). Example: {'attributes':
            {'billing_details': {'email': 'jane@example.com', 'name': 'Jane Doe'}, 'brand': 'visa', 'created_at':
            '2026-04-23T12:34:56Z', 'default': True, 'exp_month': 8, 'exp_year': 2028, 'last4': '4242', 'updated_at':
            '2026-04-23T12:34:56Z'}, 'id': '0b8a9c9e-1111-2222-3333-444455556666', 'type': 'payment_method'}.
    """

    data: PaymentMethodResource
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
        from ..models.payment_method_resource import PaymentMethodResource

        d = dict(src_dict)
        data = PaymentMethodResource.from_dict(d.pop("data"))

        payment_method_response = cls(
            data=data,
        )

        payment_method_response.additional_properties = d
        return payment_method_response

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
