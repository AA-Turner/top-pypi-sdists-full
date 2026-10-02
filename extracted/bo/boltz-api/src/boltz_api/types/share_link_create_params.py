# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr

__all__ = [
    "ShareLinkCreateParams",
    "AccessParameters",
    "AccessParametersPublicShareLinkAccessParameters",
    "AccessParametersEmailShareLinkAccessParameters",
]


class ShareLinkCreateParams(TypedDict, total=False):
    expires_at: Required[str]

    access_parameters: AccessParameters
    """Access-control parameters for the share link.

    Discriminated by `access_mode`: `public` requires no other fields; `email`
    requires a non-empty `allowed_emails` list.
    """

    pipeline_ids: SequenceNotStr[str]
    """Pipelines to expose through the share link.

    Must belong to the resolved workspace. Up to 100 entries.
    """

    prediction_ids: SequenceNotStr[str]
    """Predictions to expose through the share link.

    Must belong to the resolved workspace. Up to 100 entries.
    """

    workspace_id: str
    """Workspace to target.

    Admin API keys and OAuth callers may select an authorized workspace; for
    workspace-scoped keys the value must match the key assignment.
    """


class AccessParametersPublicShareLinkAccessParameters(TypedDict, total=False):
    """Public access: anyone holding the share link ID can read."""

    access_mode: Required[Literal["public"]]


class AccessParametersEmailShareLinkAccessParameters(TypedDict, total=False):
    """
    Email-restricted access: only the addresses in `allowed_emails` can read the link.
    """

    access_mode: Required[Literal["email"]]

    allowed_emails: Required[SequenceNotStr[str]]
    """Email addresses allowed to read the link.

    Must contain at least one address; up to 100 entries.
    """


AccessParameters: TypeAlias = Union[
    AccessParametersPublicShareLinkAccessParameters, AccessParametersEmailShareLinkAccessParameters
]
