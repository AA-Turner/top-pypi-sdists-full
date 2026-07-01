from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from typing import TypeVar

T = TypeVar("T")

CursorParams = Mapping[str, object]


def paginate(
    fetch_page: Callable[[dict[str, object]], Mapping[str, object]],
    params: CursorParams | None = None,
) -> Iterator[object]:
    page_params = dict(params or {})
    cursor = page_params.get("cursor")

    while True:
        if cursor is None:
            page_params.pop("cursor", None)
        else:
            page_params["cursor"] = cursor

        page = fetch_page(page_params)
        data = page.get("data", [])
        if isinstance(data, list):
            yield from data

        cursor = page.get("next_cursor")
        if not cursor:
            break
