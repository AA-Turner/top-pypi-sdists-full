# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ProjectsList", "Project"]


class Project(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    is_default: bool = FieldInfo(alias="isDefault")

    is_production: bool = FieldInfo(alias="isProduction")

    name: str

    promoted_to_production_at: Optional[datetime] = FieldInfo(alias="promotedToProductionAt", default=None)

    slug: str

    updated_at: datetime = FieldInfo(alias="updatedAt")


class ProjectsList(BaseModel):
    projects: List[Project]
