# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["AdmeListParams"]


class AdmeListParams(TypedDict, total=False):
    after_id: str
    """Return results after this ID"""

    before_id: str
    """Return results before this ID"""

    limit: int
    """Max items to return. Defaults to 100."""

    workspace_id: str
    """Filter by workspace ID.

    Only used with admin API keys. If not provided, defaults to the workspace
    associated with the API key, or the default workspace for admin keys.
    """
