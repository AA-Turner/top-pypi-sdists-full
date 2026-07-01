# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .offline_application_configuration import OfflineApplicationConfiguration

__all__ = ["OfflineApplicationVariantResponse"]


class OfflineApplicationVariantResponse(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    configuration: OfflineApplicationConfiguration

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    draft: bool
    """Boolean to indicate whether the variant is in draft mode"""

    name: str

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    version: Literal["OFFLINE"]

    created_by_identity_type: Optional[Literal["user", "service_account"]] = None
    """The type of identity that created the entity."""

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    description: Optional[str] = None
    """Optional description of the application variant"""

    published_at: Optional[datetime] = None
    """The date and time that the variant was published."""
