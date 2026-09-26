# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ..._models import BaseModel

__all__ = ["RatePlanGetResponse"]


class RatePlanGetResponse(BaseModel):
    id: Optional[str] = None
    """The uppercase rate plan public key."""

    components: Optional[List[Dict[str, object]]] = None
    """Pricing components that make up this rate plan."""

    currency: Optional[str] = None
    """Currency of the rate plan pricing."""

    public_name: Optional[str] = None
    """Human-readable description of the rate plan."""
