# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.identity import Identity

__all__ = ["AgentexCloudBuild"]


class AgentexCloudBuild(BaseModel):
    id: str

    account_id: str

    agent_name: str

    build_status: Literal[
        "queued",
        "running",
        "success",
        "failed",
        "cancelling",
        "cancelled",
        "deleting",
        "delete_failed",
        "timed_out",
        "error",
        "unknown",
    ]
    """The current build lifecycle status"""

    cloud_provider_build_id: str

    created_at: datetime

    created_by: Identity
    """The identity that created the entity."""

    image_name: str

    image_tag: str

    agent_id: Optional[str] = None

    build_end_time: Optional[datetime] = None
    """When the cloud provider finished the build"""

    build_start_time: Optional[datetime] = None
    """When the cloud provider started the build"""

    image_url: Optional[str] = None

    object: Optional[Literal["agentex_cloud_build"]] = None
