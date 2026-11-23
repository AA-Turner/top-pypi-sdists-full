from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="BillingInvoice")


@_attrs_define
class BillingInvoice:
    """
    Attributes:
        id (str):
        top_up_id (str):
        source (str): `manual` for a top-up a person started, `automatic` for an automatic top-up.
        number (None | str):
        status (str):
        amount_minor (int): Amount in the minor unit of `currency`.
        currency (str):
        payment_status (None | str):
        hosted_invoice_url (None | str):
        invoice_pdf_url (None | str):
        created_at (datetime.datetime):
    """

    id: str
    top_up_id: str
    source: str
    number: None | str
    status: str
    amount_minor: int
    currency: str
    payment_status: None | str
    hosted_invoice_url: None | str
    invoice_pdf_url: None | str
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        top_up_id = self.top_up_id

        source = self.source

        number: None | str
        number = self.number

        status = self.status

        amount_minor = self.amount_minor

        currency = self.currency

        payment_status: None | str
        payment_status = self.payment_status

        hosted_invoice_url: None | str
        hosted_invoice_url = self.hosted_invoice_url

        invoice_pdf_url: None | str
        invoice_pdf_url = self.invoice_pdf_url

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "top_up_id": top_up_id,
                "source": source,
                "number": number,
                "status": status,
                "amount_minor": amount_minor,
                "currency": currency,
                "payment_status": payment_status,
                "hosted_invoice_url": hosted_invoice_url,
                "invoice_pdf_url": invoice_pdf_url,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        top_up_id = d.pop("top_up_id")

        source = d.pop("source")

        def _parse_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        number = _parse_number(d.pop("number"))

        status = d.pop("status")

        amount_minor = d.pop("amount_minor")

        currency = d.pop("currency")

        def _parse_payment_status(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        payment_status = _parse_payment_status(d.pop("payment_status"))

        def _parse_hosted_invoice_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        hosted_invoice_url = _parse_hosted_invoice_url(d.pop("hosted_invoice_url"))

        def _parse_invoice_pdf_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        invoice_pdf_url = _parse_invoice_pdf_url(d.pop("invoice_pdf_url"))

        created_at = datetime.datetime.fromisoformat(
            d.pop("created_at").replace("Z", "+00:00")
        )

        billing_invoice = cls(
            id=id,
            top_up_id=top_up_id,
            source=source,
            number=number,
            status=status,
            amount_minor=amount_minor,
            currency=currency,
            payment_status=payment_status,
            hosted_invoice_url=hosted_invoice_url,
            invoice_pdf_url=invoice_pdf_url,
            created_at=created_at,
        )

        return billing_invoice
