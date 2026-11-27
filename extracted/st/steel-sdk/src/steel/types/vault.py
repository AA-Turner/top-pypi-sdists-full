# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Vault"]


class Vault(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    description: Optional[str] = None

    name: str
    """
    1–63 lowercase letters, digits, hyphens, underscores or dots; must start with a
    letter or digit.
    """

    project_id: str = FieldInfo(alias="projectId")

    updated_at: datetime = FieldInfo(alias="updatedAt")
