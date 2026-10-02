# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["APIKeyListParams"]


class APIKeyListParams(TypedDict, total=False):
    after_id: str
    """Return results after this ID"""

    before_id: str
    """Return results before this ID"""

    limit: int
    """Max items to return"""

    workspace_id: str
    """Filter by workspace ID. If not provided, returns keys across all workspaces."""
