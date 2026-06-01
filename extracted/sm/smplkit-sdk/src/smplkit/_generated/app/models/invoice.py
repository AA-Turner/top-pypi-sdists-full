from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast


T = TypeVar("T", bound="Invoice")


@_attrs_define
class Invoice:
    """A billing invoice issued for the account.

    Attributes:
        number (None | str): Invoice number assigned by the billing provider.
        status (str): Invoice lifecycle state, e.g. `draft`, `open`, `paid`, `uncollectible`, `void`.
        amount_due (int): Amount owed on the invoice in the smallest currency unit (e.g. cents).
        amount_paid (int): Amount paid against the invoice in the smallest currency unit.
        currency (str): ISO 4217 currency code, e.g. `usd`.
        description (None | str): Human-readable summary of the invoice's line items.
        period_start (None | str): Start of the service period the invoice covers (ISO 8601).
        period_end (None | str): End of the service period the invoice covers (ISO 8601).
        created_at (None | str): When the invoice was created (ISO 8601).
        paid_at (None | str): When the invoice was paid in full (ISO 8601), or `null` if unpaid.
        hosted_invoice_url (None | str): Link to the hosted invoice page.
        invoice_pdf (None | str): Link to the PDF rendering of the invoice.
    """

    number: None | str
    status: str
    amount_due: int
    amount_paid: int
    currency: str
    description: None | str
    period_start: None | str
    period_end: None | str
    created_at: None | str
    paid_at: None | str
    hosted_invoice_url: None | str
    invoice_pdf: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        number: None | str
        number = self.number

        status = self.status

        amount_due = self.amount_due

        amount_paid = self.amount_paid

        currency = self.currency

        description: None | str
        description = self.description

        period_start: None | str
        period_start = self.period_start

        period_end: None | str
        period_end = self.period_end

        created_at: None | str
        created_at = self.created_at

        paid_at: None | str
        paid_at = self.paid_at

        hosted_invoice_url: None | str
        hosted_invoice_url = self.hosted_invoice_url

        invoice_pdf: None | str
        invoice_pdf = self.invoice_pdf

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "number": number,
                "status": status,
                "amount_due": amount_due,
                "amount_paid": amount_paid,
                "currency": currency,
                "description": description,
                "period_start": period_start,
                "period_end": period_end,
                "created_at": created_at,
                "paid_at": paid_at,
                "hosted_invoice_url": hosted_invoice_url,
                "invoice_pdf": invoice_pdf,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        number = _parse_number(d.pop("number"))

        status = d.pop("status")

        amount_due = d.pop("amount_due")

        amount_paid = d.pop("amount_paid")

        currency = d.pop("currency")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        def _parse_period_start(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        period_start = _parse_period_start(d.pop("period_start"))

        def _parse_period_end(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        period_end = _parse_period_end(d.pop("period_end"))

        def _parse_created_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        created_at = _parse_created_at(d.pop("created_at"))

        def _parse_paid_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        paid_at = _parse_paid_at(d.pop("paid_at"))

        def _parse_hosted_invoice_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        hosted_invoice_url = _parse_hosted_invoice_url(d.pop("hosted_invoice_url"))

        def _parse_invoice_pdf(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        invoice_pdf = _parse_invoice_pdf(d.pop("invoice_pdf"))

        invoice = cls(
            number=number,
            status=status,
            amount_due=amount_due,
            amount_paid=amount_paid,
            currency=currency,
            description=description,
            period_start=period_start,
            period_end=period_end,
            created_at=created_at,
            paid_at=paid_at,
            hosted_invoice_url=hosted_invoice_url,
            invoice_pdf=invoice_pdf,
        )

        invoice.additional_properties = d
        return invoice

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
