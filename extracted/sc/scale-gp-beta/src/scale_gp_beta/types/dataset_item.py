# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.identity import Identity

__all__ = ["DatasetItem"]


class DatasetItem(BaseModel):
    id: str

    content_hash: str

    created_at: datetime

    created_by: Identity
    """The identity that created the entity."""

    data: Dict[str, object]

    updated_at: datetime

    archived_at: Optional[datetime] = None

    dataset_id: Optional[str] = None

    files: Optional[Dict[str, str]] = None

    object: Optional[Literal["dataset.item"]] = None
