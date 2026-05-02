# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ChatThread"]


class ChatThread(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    title: str

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    thread_metadata: Optional[Dict[str, object]] = None
