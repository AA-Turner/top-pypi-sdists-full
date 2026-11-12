"""iter_pages: every item of a cursor-paged list route, following `X-Next-Cursor` (`Page`) until the
server sends none. The one cursor loop the SDK has (Reader, compare and `client.runs.iter` use it)."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Any

from ... import errors
from .transport import Transport


def iter_pages(transport: Transport, path: str, query: Mapping[str, Any] | None = None) -> Iterator[Any]:
    """Yield every item of `path`, one page per request; each request carries `query` plus the last
    page's cursor. Lazy: a caller that stops early sends no further request."""
    page_query = dict(query or {})
    while True:
        page = transport.get_page(path, params=page_query)
        yield from page.items
        if not page.next_cursor:
            return
        if page.next_cursor == page_query.get("cursor"):
            # The same page again, forever: a server bug, never the end of the list.
            raise errors.ServerError(
                f"GET {path} answered the cursor it was asked for (the same page again), so paging stopped"
            )
        page_query["cursor"] = page.next_cursor
