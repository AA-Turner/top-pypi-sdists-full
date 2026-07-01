# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Theme", "ThemeVars"]


class ThemeVars(BaseModel):
    accent_primary: Optional[str] = FieldInfo(alias="accentPrimary", default=None)

    accent_secondary: Optional[str] = FieldInfo(alias="accentSecondary", default=None)

    background: Optional[str] = None

    foreground: Optional[str] = None


class Theme(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    logo_blob: str

    theme_vars: ThemeVars

    title: str

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""
