# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ShareLinkArchiveResponse"]


class ShareLinkArchiveResponse(BaseModel):
    id: str

    archived: Literal[True]

    archived_at: datetime
    """When the share link was first archived."""
