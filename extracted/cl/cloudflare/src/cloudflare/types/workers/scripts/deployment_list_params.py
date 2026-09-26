# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DeploymentListParams"]


class DeploymentListParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier."""

    page: int
    """Current page."""

    per_page: int
    """Items per page."""

    since: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """Start of the deployment creation time range, inclusive."""

    until: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """End of the deployment creation time range, inclusive."""
