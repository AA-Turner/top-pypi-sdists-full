# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ShareLinkListPipelineResultsParams"]


class ShareLinkListPipelineResultsParams(TypedDict, total=False):
    id: Required[str]

    after_id: str
    """Return results after this ID"""

    before_id: str
    """Return results before this ID"""

    ids: str
    """Comma-separated list of result IDs to filter by (max 200).

    Only results whose ID matches one of these is returned; missing IDs are silently
    skipped. Composes with `limit`, `after_id`, and `before_id` — the filter is
    applied before pagination.
    """

    limit: int
    """Max results to return. Defaults to 100."""
