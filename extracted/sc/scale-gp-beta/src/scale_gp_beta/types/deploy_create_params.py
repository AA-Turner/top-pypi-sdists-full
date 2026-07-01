# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DeployCreateParams"]


class DeployCreateParams(TypedDict, total=False):
    environment_config: Required[str]

    manifest_file: Required[str]

    build_id: str
    """The build_id of the cloud build.

    Required if image_name and image_tag are not provided.
    """

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """ISO 8601 expiry timestamp.

    Only valid for preview deployments. If omitted on a preview deployment, defaults
    to 8 hours from now. Previews are always ephemeral and always have an
    expires_at.
    """

    image_name: str
    """Name of the image to deploy. Required if build_id is not provided."""

    image_tag: str
    """Tag of the image to deploy. Required if build_id is not provided."""

    preview: bool
    """
    When True, creates a preview deployment with a unique deployment-id suffix
    appended to the helm release name.
    """

    preview_label: str
    """Non-unique grouping label for the preview (e.g.

    branch name, PR number). Persisted on the deployment record so callers can list
    all deploys for a given label via
    `GET /v5/agentex/deployments?preview_label=X&limit=1` (get the latest).
    Sanitized to lowercase alphanumeric + hyphens for K8s DNS-label compatibility
    (max 30 characters after sanitization). Each deploy still gets a unique helm
    release name regardless of label, so concurrent redeploys never share K8s
    resources. Only valid when preview=True.
    """
