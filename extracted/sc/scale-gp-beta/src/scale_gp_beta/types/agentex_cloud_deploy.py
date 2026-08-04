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
    """The unique identifier of the deployment."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by: Identity
    """The identity that created the entity."""

    environment_config: str
    """YAML content of environment configuration from the environment config file."""

    manifest_file: str
    """YAML content of manifest configuration."""

    namespace: str
    """Kubernetes namespace where the deployment is deployed."""

    status: str
    """Deployment status: pending, running, completed, failed, or cancelled."""

    build_id: Optional[str] = None
    """The build_id of the cloud build that produced the deployed image."""

    deploy_events: Optional[List[AgentexCloudDeployEvent]] = None
    """Kubernetes events for this deployment."""

    expires_at: Optional[datetime] = None
    """When this deployment will be cleaned up.

    Always set on preview deployments (defaults to 8 hours from creation if the
    request omits it). Null on non-preview deployments — they have no TTL.
    """

    helm_release_name: Optional[str] = None
    """Helm release name after successful deployment."""

    object: Optional[Literal["agentex_cloud_deploy"]] = None

    preview_label: Optional[str] = None
    """Non-unique grouping label for preview deployments.

    Filter `?preview_label=X&limit=1` returns the latest deploy for the label.
    Sanitized (lowercase alphanumeric + hyphens) and capped at 30 characters.
    """
