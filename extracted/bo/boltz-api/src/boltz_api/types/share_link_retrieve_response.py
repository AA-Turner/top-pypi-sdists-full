# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "ShareLinkRetrieveResponse",
    "AccessParameters",
    "AccessParametersPublicShareLinkAccessParameters",
    "AccessParametersEmailShareLinkAccessParameters",
]


class AccessParametersPublicShareLinkAccessParameters(BaseModel):
    """Public access: anyone holding the share link ID can read."""

    access_mode: Literal["public"]


class AccessParametersEmailShareLinkAccessParameters(BaseModel):
    """
    Email-restricted access: only the addresses in `allowed_emails` can read the link.
    """

    access_mode: Literal["email"]

    allowed_emails: List[str]
    """Email addresses allowed to read the link.

    Must contain at least one address; up to 100 entries.
    """


AccessParameters: TypeAlias = Union[
    AccessParametersPublicShareLinkAccessParameters, AccessParametersEmailShareLinkAccessParameters
]


class ShareLinkRetrieveResponse(BaseModel):
    id: str
    """Share link ID.

    This value is the bearer credential used to access the linked resources — treat
    it as a secret.
    """

    access_parameters: AccessParameters
    """Access-control parameters for the share link.

    Discriminated by `access_mode`: `public` requires no other fields; `email`
    requires a non-empty `allowed_emails` list.
    """

    archived_at: Optional[datetime] = None
    """When the share link was archived, or null if it has never been archived."""

    created_at: datetime
    """When the share link was created."""

    expires_at: datetime
    """When the share link stops granting access."""

    pipeline_ids: List[str]
    """Pipelines exposed by this share link."""

    prediction_ids: List[str]
    """Predictions exposed by this share link."""

    workspace_id: str
    """Workspace that owns the share link and the referenced resources."""

    url: Optional[str] = None
    """Visitable share link URL for the deployment's public app.

    Present when the deployment has a configured app host; otherwise construct as
    `<your-app-host>/share/{id}`. Treat as a secret — the `{id}` segment is the
    bearer credential.
    """
