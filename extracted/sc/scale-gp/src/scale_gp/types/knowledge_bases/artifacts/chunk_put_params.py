# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["ChunkPutParams"]


class ChunkPutParams(TypedDict, total=False):
    knowledge_base_id: Required[str]

    artifact_id: Required[str]

    chunk_position: Required[int]
    """Position of the chunk in the artifact."""

    text: Required[str]
    """Associated text of the chunk."""

    metadata: Dict[str, object]
    """Additional metadata associated with the chunk."""
