# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CredentialUpdateResponse"]


class CredentialUpdateResponse(BaseModel):
    created_at: datetime = FieldInfo(alias="createdAt")
    """Date and time the credential was created"""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Date and time the credential was last updated"""

    additional_origins: Optional[List[str]] = FieldInfo(alias="additionalOrigins", default=None)
    """
    Canonical http(s) origins, besides `origin`, this credential may be filled on,
    such as its login host or identity provider (e.g. `https://login.example.com`).
    Only the credential's origin and these ever match a page, exactly; at most 20.
    """

    label: Optional[str] = None
    """Label for the credential"""

    namespace: Optional[str] = None
    """The namespace the credential is stored against. Defaults to "default"."""

    origin: Optional[str] = None
    """Website origin the credential is for"""
