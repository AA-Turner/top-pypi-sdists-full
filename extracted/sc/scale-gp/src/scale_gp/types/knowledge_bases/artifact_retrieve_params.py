# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ArtifactRetrieveParams"]


class ArtifactRetrieveParams(TypedDict, total=False):
    knowledge_base_id: Required[str]

    status_filter: str
