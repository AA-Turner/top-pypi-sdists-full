# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.identity import Identity

__all__ = ["SGPFile"]


class SGPFile(BaseModel):
    id: str
    """The unique identifier of the entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by: Identity
    """The identity that created the entity."""

    filename: str

    md5_checksum: str

    mime_type: str

    size: int

    duration_seconds: Optional[int] = None

    object: Optional[Literal["file"]] = None

    tags: Optional[Dict[str, builtins.object]] = None
