# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .project import Project
from .._models import BaseModel

__all__ = ["ProjectRetrieveResponse"]


class ProjectRetrieveResponse(BaseModel):
    project: Project
