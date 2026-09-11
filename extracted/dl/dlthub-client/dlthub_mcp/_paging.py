"""The bounds every listing tool pages within.

Shared so one call cannot flood the agent, whichever listing it reached for.
"""

from __future__ import annotations

#: Rows per page when the caller does not say, and the ceiling it may ask for.
PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def page(limit: int) -> int:
    """Clamp a requested page size.

    Args:
        limit: What the caller asked for.

    Returns:
        A page size between 1 and :data:`MAX_PAGE_SIZE`.
    """
    return max(1, min(limit, MAX_PAGE_SIZE))


def skip(offset: int) -> int:
    """Clamp a requested offset, since the platform has no use for a negative one.

    Args:
        offset: What the caller asked for.

    Returns:
        The offset, floored at 0.
    """
    return max(0, offset)


__all__ = ["MAX_PAGE_SIZE", "PAGE_SIZE", "page", "skip"]
