# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.identity import Identity

__all__ = ["DatasetItem"]


class DatasetItem(BaseModel):
    id: str
    """The unique identifier of the entity."""

    content_hash: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by: Identity
    """The identity that created the entity."""

    data: Dict[str, object]

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    dataset_id: Optional[str] = None

    files: Optional[Dict[str, str]] = None

    object: Optional[Literal["dataset.item"]] = None
