"""Cursor paging for identity-service list responses ({items, next_cursor})."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from istari_digital_client.sdk._base import Page


def paginate_cursor(fetch: Callable[[str | None], Any]) -> Page[Any]:
    """Wrap ``fetch(cursor)`` (returns a generated page with ``items`` and ``next_cursor``) as a Page."""

    def make(cursor: str | None, seen: frozenset[str]) -> Page[Any]:
        raw = fetch(cursor)
        items = list(raw.items or [])
        nxt = getattr(raw, "next_cursor", None)
        has_next = bool(nxt) and nxt != cursor and nxt not in seen
        next_seen = seen | {cursor} if cursor is not None else seen
        return Page(items, fetch_next=(lambda: make(nxt, next_seen)) if has_next else None)

    return make(None, frozenset())
