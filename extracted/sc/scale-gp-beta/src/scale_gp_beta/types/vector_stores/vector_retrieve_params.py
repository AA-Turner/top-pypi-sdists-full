# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["VectorRetrieveParams"]


class VectorRetrieveParams(TypedDict, total=False):
    vector_store_name: Required[str]
    """The name of the vector store"""

    include_vectors: bool
    """Include embedding vectors"""
