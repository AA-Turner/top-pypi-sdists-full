"""Helpers for collecting cursor-paginated list responses."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

import runta as _public


LIST_PAGE_LIMIT = 100


@dataclass(slots=True)
class ListPaginationState:
    """Track opaque cursor pagination without exposing it publicly."""

    after: str | None = None
    _seen_cursors: set[str] = field(default_factory=set)

    def consume(
        self, payload: object, *, operation: str
    ) -> tuple[list[Mapping[str, Any]], bool]:
        if not isinstance(payload, Mapping):
            raise _public.ApiError(f"Invalid pagination response for {operation}")

        data = payload.get("data")
        if not isinstance(data, list) or not all(
            isinstance(item, Mapping) for item in data
        ):
            raise _public.ApiError(f"Invalid pagination response for {operation}")

        pagination = payload.get("pagination")
        if not isinstance(pagination, Mapping):
            raise _public.ApiError(f"Invalid pagination response for {operation}")

        has_more = pagination.get("has_more")
        if not isinstance(has_more, bool):
            raise _public.ApiError(f"Invalid pagination response for {operation}")
        if not has_more:
            return data, False

        next_cursor = pagination.get("next_cursor")
        if not isinstance(next_cursor, str) or not next_cursor.strip():
            raise _public.ApiError(f"Invalid pagination cursor for {operation}")
        if next_cursor in self._seen_cursors:
            raise _public.ApiError(f"Repeated pagination cursor for {operation}")
        self._seen_cursors.add(next_cursor)
        self.after = next_cursor
        return data, True
