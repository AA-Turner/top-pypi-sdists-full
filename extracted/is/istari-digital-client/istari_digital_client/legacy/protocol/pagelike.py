from __future__ import annotations

from typing import Any, List, Optional, Protocol, runtime_checkable


@runtime_checkable
class PageLike(Protocol):
    """
    Protocol defining the structure of a paginated response model.

    This protocol is used to verify that a class has all the required fields
    for pagination support before adding Pageable capabilities.
    """

    items: List[Any]
    total: Optional[int]
    page: Optional[int]
    size: Optional[int]
    pages: Optional[int]
