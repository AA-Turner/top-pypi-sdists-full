# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from ..._models import BaseModel

__all__ = ["TURNCreateResponse"]


class TURNCreateResponse(BaseModel):
    created: datetime
    """The date and time the item was created."""

    key: str
    """Bearer token"""

    modified: datetime
    """The date and time the item was last modified."""

    name: str
    """A short description of a TURN key, not shown to end users."""

    uid: str
    """A Cloudflare-generated unique identifier for a item."""
