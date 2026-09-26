# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["Deployment", "Version", "Annotations"]


class Version(BaseModel):
    percentage: float
    """Percentage of traffic served by this version."""

    version_id: str
    """Identifier of the Worker Version."""


class Annotations(BaseModel):
    workers_message: Optional[str] = FieldInfo(alias="workers/message", default=None)
    """Human-readable message about the deployment. Truncated to 1000 bytes if longer."""

    workers_triggered_by: Optional[str] = FieldInfo(alias="workers/triggered_by", default=None)
    """Operation that triggered the creation of the deployment."""


class Deployment(BaseModel):
    id: str

    created_on: datetime

    source: str

    strategy: Literal["percentage"]

    versions: List[Version]
    """Worker versions included in this deployment.

    Each object must contain a `version_id` UUID and a `percentage`; percentages
    across all objects must total 100. In the `cf` CLI, pass the entire array as one
    JSON value to `--versions`, either inline, for example
    `--versions '[{"version_id":"023e105f-2a42-4f8b-a1c1-73f6a2a30c0f","percentage":100}]'`,
    or from a JSON file with `--versions @versions.json`.
    """

    annotations: Optional[Annotations] = None

    author_email: Optional[str] = None
