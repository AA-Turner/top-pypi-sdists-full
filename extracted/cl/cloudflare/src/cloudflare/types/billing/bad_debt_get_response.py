# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["BadDebtGetResponse", "Invoice"]


class Invoice(BaseModel):
    id: Optional[str] = None
    """Billing history item identifier."""

    action: Optional[str] = None
    """The billing item action."""

    amount: Optional[float] = None
    """The amount associated with this billing item."""

    amount_to_pay: Optional[float] = None
    """The amount remaining to pay."""

    currency: Optional[str] = None
    """The currency of the billing item."""

    description: Optional[str] = None
    """The billing item description."""

    external_invoice_id: Optional[str] = None
    """The external invoice identifier."""

    hosted_invoice_url: Optional[str] = None
    """URL to the hosted invoice."""

    invoice_id: Optional[str] = None
    """The associated invoice identifier."""

    occurred_at: Optional[datetime] = None
    """When the billing event occurred."""

    receipt_id: Optional[str] = None
    """The associated receipt identifier."""

    source: Optional[str] = None
    """The source of the billing item."""

    source_invoice_id: Optional[str] = None
    """The source invoice identifier."""

    status: Optional[str] = None
    """The status of the billing item."""

    type: Optional[str] = None
    """The billing item type."""


class BadDebtGetResponse(BaseModel):
    already_paid: Optional[float] = None
    """Amount already paid towards the debt."""

    bad_debt_status: Optional[str] = None
    """The current bad debt status of the account."""

    invoices: Optional[List[Invoice]] = None
    """List of outstanding invoices contributing to bad debt."""

    total_debt_amount: Optional[float] = None
    """Total outstanding debt amount."""
