# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

__all__ = ["VectorStoreConfigureParams"]


class VectorStoreConfigureParams(TypedDict, total=False):
    indexed_metadata_fields: Required[Dict[str, Literal["string", "number", "boolean"]]]
    """Dictionary mapping metadata field names to their types.

    Only STRING, NUMBER, and BOOLEAN types can be indexed.
    """
