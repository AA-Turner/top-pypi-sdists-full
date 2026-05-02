# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["KnowledgeBaseListParams"]


class KnowledgeBaseListParams(TypedDict, total=False):
    account_id: str
    """Optional search by account_id"""

    limit: int
    """Maximum number of artifacts to be returned by the given endpoint.

    Defaults to 100 and cannot be greater than 10k.
    """

    name: str
    """Optional search by knowledge base name (case-insensitive partial match)"""

    page: int
    """Page number for pagination to be returned by the given endpoint.

    Starts at page 1
    """

    view: List[Literal["Connections", "ArtifactCount"]]
