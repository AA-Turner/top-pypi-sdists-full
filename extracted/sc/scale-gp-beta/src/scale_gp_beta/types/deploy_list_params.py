# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .chat.sort_order import SortOrder

__all__ = ["DeployListParams"]


class DeployListParams(TypedDict, total=False):
    agent_name: str
    """Filter deployments by agent name (via associated build)"""

    build_id: str
    """Filter deployments by build ID"""

    ending_before: str

    limit: int

    preview_label: str
    """Filter deployments by preview label (e.g.

    branch name). The label is non-unique — many deployments can share it. Combine
    with limit=1 to get the latest deploy for that label.
    """

    sort_by: str

    sort_order: SortOrder

    starting_after: str
