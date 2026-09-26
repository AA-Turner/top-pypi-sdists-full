# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["PaymentMethodCreateParams"]


class PaymentMethodCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier"""

    address: str
    """Billing address line 1."""

    address2: str
    """Billing address line 2."""

    bank_account_type: str
    """Bank account type."""

    bank_code: str
    """Bank code."""

    bank_country: str
    """Bank country."""

    bank_name: str
    """Bank name for bank-based payment methods."""

    bank_routing_number: str
    """Bank routing number."""

    cashapp_cash_tag: str
    """Cash App cash tag."""

    city: str
    """Billing city."""

    country: str
    """Billing country."""

    default: bool
    """Whether this is the default payment method."""

    device_data: str
    """Device data for fraud prevention."""

    first_name: str
    """Billing first name."""

    last_name: str
    """Billing last name."""

    nick_name: str
    """A nickname for the payment method."""

    payment_account_email: str
    """Email associated with the payment account."""

    payment_email: str
    """Payment email address."""

    payment_gateway: str
    """The payment gateway used."""

    payment_nonce: str
    """Payment nonce for tokenized payments."""

    state: str
    """Billing state."""

    type: Literal["CREDIT_CARD", "PAYPAL", "CASHAPP", "SEPA_DEBIT", "LINK", "ACH_DIRECT_DEBIT"]
    """The payment method type."""

    zipcode: str
    """Billing zip code."""
