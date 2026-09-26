# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["CreditGetResponse"]


class CreditGetResponse(BaseModel):
    confirmed_balance_cents: Optional[int] = None
    """The confirmed credit balance in cents."""

    currency: Optional[str] = None
    """Currency of the credit balance."""

    days_remaining: Optional[int] = None
    """Days remaining until the credits expire."""

    eligible: Optional[bool] = None
    """Whether the account is eligible to receive credits."""

    has_record: Optional[bool] = None
    """Whether a credit record exists for the account."""

    original_amount_cents: Optional[int] = None
    """The original credit amount in cents."""

    percent_consumed: Optional[float] = None
    """Percentage of the original credit amount consumed."""

    projected_depletion_date: Optional[datetime] = None
    """Projected date when the credits will be depleted."""

    valid_from: Optional[datetime] = None
    """When the credits become valid."""

    valid_to: Optional[datetime] = None
    """When the credits expire."""
