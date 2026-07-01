# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypedDict

__all__ = ["KnowledgeBaseDataSourceListParams"]


class KnowledgeBaseDataSourceListParams(TypedDict, total=False):
    account_id: str

    limit: int
    """Maximum number of artifacts to be returned by the given endpoint.

    Defaults to 100 and cannot be greater than 10k.
    """

    name: Union[int, str]

    page: int
    """Page number for pagination to be returned by the given endpoint.

    Starts at page 1
    """
