"""Complete artifact inventories across legacy and offset-paginated backends."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import httpx

from . import errors

_PAGINATION_HEADER = "X-Artifact-Pagination"
_PAGINATION_VERSION = "offset-v1"
_PAGE_LIMIT = 1000


def read_artifact_rows(
    fetch: Callable[[dict[str, Any] | None], httpx.Response],
    params: dict[str, Any] | None = None,
) -> list[dict]:
    """Keep legacy reads unbounded; page only when the server advertises support.

    An old server ignores offset, so probing with a limit would lose rows or loop.
    Repeated IDs and capability changes fail explicitly instead of returning a
    misleading inventory. Offset reads do not provide snapshot isolation during
    concurrent deletion; callers needing a fixed inventory must read a settled run.
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
        response = fetch({**(params or {}), "limit": _PAGE_LIMIT, "offset": len(rows)})
        page = response.json()
