# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["ArtifactUpdateParams"]


class ArtifactUpdateParams(TypedDict, total=False):
    knowledge_base_id: Required[str]

    tags: Dict[str, object]
    """Tags to associate with the artifact. Will overwrite existing tags."""
