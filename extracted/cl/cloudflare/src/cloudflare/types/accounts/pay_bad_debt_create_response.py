# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["PayBadDebtCreateResponse"]


class PayBadDebtCreateResponse(BaseModel):
    client_secret: Optional[str] = None
    """The Stripe client secret for frontend payment confirmation."""
