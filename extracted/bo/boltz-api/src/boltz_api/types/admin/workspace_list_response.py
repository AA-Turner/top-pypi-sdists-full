# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["WorkspaceListResponse", "DataRetention"]


class DataRetention(BaseModel):
    """How long result data is retained before automatic deletion.

    Defaults to 7 days if not specified. Maximum retention is 14 days (336 hours).
    """

    unit: Literal["hours", "days"]
    """Time unit for retention duration"""

    value: int
    """Duration value. Maximum retention is 14 days (or 336 hours)."""


class WorkspaceListResponse(BaseModel):
    id: str
    """Workspace ID"""

    archived_at: Optional[datetime] = None

    created_at: datetime

    data_retention: DataRetention
    """How long result data is retained before automatic deletion.

    Defaults to 7 days if not specified. Maximum retention is 14 days (336 hours).
    """

    is_default: bool
    """Whether this is the default workspace"""

    name: Optional[str] = None
    """Workspace name"""

    updated_at: datetime
