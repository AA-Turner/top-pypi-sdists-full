# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Required, TypedDict

from .text_content_param import TextContentParam

__all__ = ["VectorStoreUpsertParams", "Vector"]


class VectorStoreUpsertParams(TypedDict, total=False):
    vectors: Required[Iterable[Vector]]
    """Array of documents to upsert"""


class Vector(TypedDict, total=False):
    """A document for upsert operations.

    Documents support several modes:
    - ``content`` only: text is embedded and all fields are replaced.
    - ``embedding`` only: pre-computed embedding vector is used directly.
    - Both ``content`` and ``embedding``: the pre-computed embedding is used and text
      is stored for retrieval but not re-embedded.
    - Neither (metadata-only): only metadata is updated on an existing document without
      re-embedding. Omitting both on a document that does not exist yet will return a
      per-item failure in the batch response.
    """

    id: Required[str]
    """Unique document ID"""

    content: TextContentParam
    """Text content for documents."""

    embedding: Iterable[float]
    """Pre-computed embedding vector"""

    metadata: Dict[str, object]
    """Key-value metadata"""
