# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PayInvoiceCreateParams"]


class PayInvoiceCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier"""

    invoice_id: str
    """The identifier of the invoice to pay."""

    payment_method_id: str
    """The payment method to use. If omitted, the default payment method is used."""

    validate_payment_method: bool
    """Whether to validate the payment method before processing."""
