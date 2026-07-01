# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ChunkListParams"]


class ChunkListParams(TypedDict, total=False):
    knowledge_base_id: Required[str]

    chunk_status: Literal["Pending", "Completed", "Failed"]
    """Filter by the status of the chunks"""

    limit: int
    """Maximum number of artifacts to be returned by the given endpoint.

    Defaults to 100 and cannot be greater than 10k.
    """

    page: int
    """Page number for pagination to be returned by the given endpoint.

    Starts at page 1
    """
