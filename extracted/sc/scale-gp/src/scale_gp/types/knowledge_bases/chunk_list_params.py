# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ChunkListParams"]


class ChunkListParams(TypedDict, total=False):
    chunk_id: str
    """Optional search by chunk_id"""

    max_chunks: int
    """Maximum number of chunks returned by the get_chunks endpoint.

    Defaults to 10 and cannot be greater than 2000.
    """

    metadata_filters: str
    """Optional search by metadata fields, encoded as a JSON object"""
