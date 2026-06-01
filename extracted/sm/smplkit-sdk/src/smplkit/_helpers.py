"""Shared helpers used across multiple SDK modules."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeVar


def key_to_display_name(key: str) -> str:
    """Convert a slug-style key to a human-readable display name.

    ``"checkout-v2"`` → ``"Checkout V2"``
    ``"user_service"`` → ``"User Service"``
    """
    return key.replace("-", " ").replace("_", " ").title()


# Server caps page[size] at 1000; we always ask for the maximum so the
# runtime fetch-all paths reach completion in the fewest round-trips.
PAGE_SIZE = 1000

_T = TypeVar("_T")


def paginate_sync(fetch_page: Callable[[int, int], list[_T]]) -> list[_T]:
    """Drive an offset-paginated SDK list endpoint to completion.

    ``fetch_page(page_number, page_size)`` is called with 1-based page
    numbers and the server-max ``page_size``; it must return that page's
    rows. Iteration stops when a page returns fewer rows than requested,
    which is the standard last-page signal across the platform.
    """
    rows: list[_T] = []
    page = 1
    while True:
        page_rows = fetch_page(page, PAGE_SIZE)
        rows.extend(page_rows)
        if len(page_rows) < PAGE_SIZE:
            return rows
        page += 1


async def paginate_async(fetch_page: Callable[[int, int], Awaitable[list[_T]]]) -> list[_T]:
    """Async counterpart of :func:`paginate_sync`."""
    rows: list[_T] = []
    page = 1
    while True:
        page_rows = await fetch_page(page, PAGE_SIZE)
        rows.extend(page_rows)
        if len(page_rows) < PAGE_SIZE:
            return rows
        page += 1
