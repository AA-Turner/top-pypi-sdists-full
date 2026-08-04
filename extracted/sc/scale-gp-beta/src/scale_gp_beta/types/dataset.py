# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.identity import Identity

__all__ = ["Dataset"]


class Dataset(BaseModel):
    id: str
    """The unique identifier of the entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by: Identity
    """The identity that created the entity."""

    current_version_num: int

    name: str

    tags: List[str]
    """The tags associated with the entity"""

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    description: Optional[str] = None

    object: Optional[Literal["dataset"]] = None
