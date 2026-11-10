# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["APIKey"]


class APIKey(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    key: str
    """The full secret on creation or rotation only.

    Metadata reads return a masked preview. Store a newly created secret securely;
    it cannot be retrieved later.
    """

    project_id: Optional[str] = FieldInfo(alias="projectId", default=None)
    """The pinned project, or null for a global key, which binds to no project."""

    scope_type: Literal["project", "global"] = FieldInfo(alias="scopeType")
    """`project` pins the key to one project.

    `global` authorizes access across the organization and has no project binding.
    """

    updated_at: datetime = FieldInfo(alias="updatedAt")

    name: Optional[str] = None
