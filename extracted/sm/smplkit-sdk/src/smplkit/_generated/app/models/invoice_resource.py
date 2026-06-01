from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.invoice_resource_type import check_invoice_resource_type
from ..models.invoice_resource_type import InvoiceResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.invoice import Invoice


T = TypeVar("T", bound="InvoiceResource")


@_attrs_define
class InvoiceResource:
    """JSON:API resource envelope for an invoice.

    Example:
        {'attributes': {'amount_due': 2900, 'amount_paid': 2900, 'created_at': '2026-03-01T00:00:00Z', 'currency':
            'usd', 'description': 'Smpl Flags - Pro', 'hosted_invoice_url': 'https://invoice.stripe.com/i/acct_xxx/inv_xxx',
            'invoice_pdf': 'https://pay.stripe.com/invoice/acct_xxx/inv_xxx/pdf', 'number': 'INV-0001', 'paid_at':
            '2026-03-01T12:00:00Z', 'period_end': '2026-04-01T00:00:00Z', 'period_start': '2026-03-01T00:00:00Z', 'status':
            'paid'}, 'id': 'in_1234567890abcdef', 'type': 'invoice'}

    Attributes:
        type_ (InvoiceResourceType):
        attributes (Invoice): A billing invoice issued for the account.
        id (None | str | Unset):
    """

    type_: InvoiceResourceType
    attributes: Invoice
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
        from ..models.invoice import Invoice

        d = dict(src_dict)
        type_ = check_invoice_resource_type(d.pop("type"))

        attributes = Invoice.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        invoice_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        invoice_resource.additional_properties = d
        return invoice_resource

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
