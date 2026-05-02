# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.identity import Identity

__all__ = ["SecretRetrieveResponse"]


class SecretRetrieveResponse(BaseModel):
    """API response model for a secret. Never includes the secret value."""

    id: str

    account_id: str

    cloud_secret_path: str

    created_at: datetime

    created_by: Identity
    """The identity that created the entity."""

    key: str

    description: Optional[str] = None

    object: Optional[Literal["sgp_cloud_secret"]] = None

    updated_at: Optional[datetime] = None
    """Timestamp of last update."""

    updated_by: Optional[str] = None
    """User who last updated the secret."""
