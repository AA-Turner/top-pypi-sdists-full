# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ProfileResponse", "Profile", "SearchResults"]


class Profile(BaseModel):
    buckets: Optional[Dict[str, List[str]]] = None
    """Per-bucket memory lists, keyed by bucket key"""

    dynamic: Optional[List[str]] = None
    """Dynamic profile information (recent memories)"""

    static: Optional[List[str]] = None
    """Static profile information that remains relevant long-term"""


class SearchResults(BaseModel):
    """Search results if a search query was provided"""

    results: List[object]
    """Search results for the provided query"""

    timing: float
    """Search timing in milliseconds"""

    total: float
    """Total number of search results"""


class ProfileResponse(BaseModel):
    profile: Profile

    search_results: Optional[SearchResults] = FieldInfo(alias="searchResults", default=None)
    """Search results if a search query was provided"""
