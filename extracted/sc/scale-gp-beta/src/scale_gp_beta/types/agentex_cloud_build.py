# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.identity import Identity

__all__ = ["AgentexCloudBuild"]


class AgentexCloudBuild(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    agent_name: str
    """The name of the agent that this build belongs to"""

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
    """
    The unique identifier of the build from the cloud provider, or an internal UUID
    when an existing image is copied without a provider build.
    """

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by: Identity
    """The identity that created the entity."""

    image_name: str
    """The name of the container image to build."""

    image_tag: str
    """The tag for the container image."""

    source_commit: Optional[str] = None
    """Git commit the build context was at, when a git work tree."""

    source_dirty: Optional[bool] = None
    """Whether the work tree had uncommitted changes at build time (null outside git)."""

    source_ref: Optional[str] = None
    """Git branch or tag for source_commit, when resolvable."""

    source_repo: Optional[str] = None
    """Normalized git remote the build context came from (host/path, no credentials)."""

    source_subpath: Optional[str] = None
    """Build-context path relative to the repo root (which agent, in a monorepo)."""

    working_tree_hash: Optional[str] = None
    """Deterministic SHA-256 content hash of the build inputs (not the tarball)."""

    agent_id: Optional[str] = None
    """The UUID of the agent that this build belongs to"""

    build_end_time: Optional[datetime] = None
    """When the cloud provider finished the build"""

    build_start_time: Optional[datetime] = None
    """When the cloud provider started the build"""

    image_url: Optional[str] = None
    """The URL of the container image.

    This is not guaranteed to be present until the build is complete.
    """

    object: Optional[Literal["agentex_cloud_build"]] = None
