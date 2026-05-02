# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ApplicationSpecUpdateResponse"]


class ApplicationSpecUpdateResponse(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    description: str
    """The description of the Application Spec"""

    name: str
    """The name of the Application Spec"""

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    created_by_identity_type: Optional[Literal["user", "service_account"]] = None
    """The type of identity that created the entity."""

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    run_online_evaluation: Optional[bool] = None
    """Whether the application spec should run online evaluation, default is `false`"""

    theme_id: Optional[str] = None
