# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ...._models import BaseModel

__all__ = ["PaymentMethodCreateResponse"]


class PaymentMethodCreateResponse(BaseModel):
    client_secret: Optional[str] = None
    """The Stripe client secret for frontend payment method collection."""

    intent_type: Optional[str] = None
    """The type of Stripe intent created."""
