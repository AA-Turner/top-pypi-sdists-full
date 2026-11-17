"""Complete artifact inventories from legacy and offset-paginated backends."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import httpx

from .. import errors

_PAGINATION_HEADER = "X-Artifact-Pagination"
_PAGINATION_VERSION = "offset-v1"
#: A full page of a run's own files names the next one; an older server sends none and pages by offset.
_NEXT_CURSOR_HEADER = "X-Next-Cursor"
_PAGE_LIMIT = 1000


def read_artifact_rows(
    fetch: Callable[[dict[str, Any] | None], httpx.Response],
    params: dict[str, Any] | None = None,
) -> list[dict]:
    """Page only when the server advertises it; legacy reads stay unbounded.

    An old server ignores offset, so a limit probe would lose rows or loop.
    Repeated IDs or a capability change raise instead of returning a wrong
    inventory. A server cursor anchors each page to the last row read, so a file
    deleted or moved mid-read never skips another; offset alone (an older server)
    can, so read a settled run there.
    """
    response = fetch(params or None)
    page = response.json()
    if response.headers.get(_PAGINATION_HEADER) is None:
        return page

    rows: list[dict] = []
    seen: set[str] = set()
    while True:
        if response.headers.get(_PAGINATION_HEADER) != _PAGINATION_VERSION:
            raise errors.CapabilityUnavailable(
                "artifact offset pagination",
                "Artifact pagination support changed during the read or is unsupported; "
                "retry against a backend supporting offset-v1.",
            )
        ids = {row["id"] for row in page}
        if len(ids) != len(page) or seen.intersection(ids):
            raise errors.RosError(
                "Artifact inventory changed while paging (repeated artifact IDs); "
                "retry after artifact writes have finished."
            )
        if len(page) > _PAGE_LIMIT:
            raise errors.RosError("Artifact backend exceeded its advertised page limit.")
        rows.extend(page)
        seen.update(ids)
        if len(page) < _PAGE_LIMIT:
            return rows
        cursor = response.headers.get(_NEXT_CURSOR_HEADER)
        response = fetch({
            **(params or {}), "limit": _PAGE_LIMIT, "offset": len(rows),
            **({"cursor": cursor} if cursor else {}),
        })
        page = response.json()
