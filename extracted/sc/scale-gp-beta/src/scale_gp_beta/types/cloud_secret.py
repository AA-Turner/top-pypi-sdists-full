# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.identity import Identity

__all__ = ["CloudSecret"]


class CloudSecret(BaseModel):
    """API response model for a secret. Never includes the secret value."""

    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    cloud_secret_path: str
    """Full path in the cloud secret store."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by: Identity
    """The identity that created the entity."""

    key: str
    """Secret name, e.g. OPENAI_API_KEY."""

    description: Optional[str] = None
    """Optional human-readable description of the secret."""

    object: Optional[Literal["sgp_cloud_secret"]] = None

    updated_at: Optional[datetime] = None
    """Timestamp of last update."""

    updated_by: Optional[str] = None
    """User who last updated the secret."""
