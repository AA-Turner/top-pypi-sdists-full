from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.invoice_resource import InvoiceResource


T = TypeVar("T", bound="InvoiceSingleResponse")


@_attrs_define
class InvoiceSingleResponse:
    """JSON:API single-resource response envelope for an invoice.

    Attributes:
        data (InvoiceResource): JSON:API resource envelope for an invoice. Example: {'attributes': {'amount_due': 2900,
            'amount_paid': 2900, 'created_at': '2026-03-01T00:00:00Z', 'currency': 'usd', 'description': 'Smpl Flags - Pro',
            'hosted_invoice_url': 'https://invoice.stripe.com/i/acct_xxx/inv_xxx', 'invoice_pdf':
            'https://pay.stripe.com/invoice/acct_xxx/inv_xxx/pdf', 'number': 'INV-0001', 'paid_at': '2026-03-01T12:00:00Z',
            'period_end': '2026-04-01T00:00:00Z', 'period_start': '2026-03-01T00:00:00Z', 'status': 'paid'}, 'id':
            'in_1234567890abcdef', 'type': 'invoice'}.
    """

    data: InvoiceResource
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
        from ..models.invoice_resource import InvoiceResource

        d = dict(src_dict)
        data = InvoiceResource.from_dict(d.pop("data"))

        invoice_single_response = cls(
            data=data,
        )

        invoice_single_response.additional_properties = d
        return invoice_single_response

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
