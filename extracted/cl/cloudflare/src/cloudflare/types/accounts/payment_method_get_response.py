# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["PaymentMethodGetResponse"]


class PaymentMethodGetResponse(BaseModel):
    id: Optional[str] = None
    """Payment method identifier."""

    address: Optional[str] = None
    """Billing address line 1."""

    address2: Optional[str] = None
    """Billing address line 2."""

    bank_account_type: Optional[str] = None
    """Bank account type."""

    bank_code: Optional[str] = None
    """Bank code."""

    bank_country: Optional[str] = None
    """Bank country."""

    bank_name: Optional[str] = None
    """Bank name for bank-based payment methods."""

    bank_routing_number: Optional[str] = None
    """Bank routing number."""

    cashapp_cash_tag: Optional[str] = None
    """Cash App cash tag."""

    city: Optional[str] = None
    """Billing city."""

    country: Optional[str] = None
    """Billing country."""

    default: Optional[bool] = None
    """Whether this is the default payment method."""

    expiration_date: Optional[str] = None
    """Card expiration date."""

    first_name: Optional[str] = None
    """Billing first name."""

    last_four: Optional[str] = None
    """Last four digits of the card number."""

    last_name: Optional[str] = None
    """Billing last name."""

    nick_name: Optional[str] = None
    """A nickname for the payment method."""

    payment_account_email: Optional[str] = None
    """Email associated with the payment account."""

    payment_email: Optional[str] = None
    """Payment email address."""

    state: Optional[str] = None
    """Billing state."""

    type: Optional[Literal["CREDIT_CARD", "PAYPAL", "CASHAPP", "SEPA_DEBIT", "LINK", "ACH_DIRECT_DEBIT"]] = None
    """The payment method type."""

    zipcode: Optional[str] = None
    """Billing zip code."""
