# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.identity import Identity
from .agentex_cloud_deploy_event import AgentexCloudDeployEvent

__all__ = ["AgentexCloudDeploy"]


class AgentexCloudDeploy(BaseModel):
    id: str

    account_id: str

    created_at: datetime

    created_by: Identity
    """The identity that created the entity."""

    environment_config: str

    manifest_file: str

    namespace: str

    status: str

    build_id: Optional[str] = None

    deploy_events: Optional[List[AgentexCloudDeployEvent]] = None
    """Kubernetes events for this deployment."""

    helm_release_name: Optional[str] = None

    object: Optional[Literal["agentex_cloud_deploy"]] = None
