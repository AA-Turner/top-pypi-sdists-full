# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

from .._types import SequenceNotStr

__all__ = ["VectorStoreDeleteParams"]


class VectorStoreDeleteParams(TypedDict, total=False):
    filter: Dict[str, object]
    """Metadata filter expression for deletion"""

    ids: SequenceNotStr[str]
    """Array of document IDs to delete"""
