# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from ..._models import BaseModel

__all__ = ["TURNListResponse"]


class TURNListResponse(BaseModel):
    created: datetime
    """The date and time the item was created."""

    modified: datetime
    """The date and time the item was last modified."""

    name: str
    """A short description of a Realtime SFU app, not shown to end users."""

    uid: str
    """A Cloudflare-generated unique identifier for a item."""
