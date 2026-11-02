"""Cursor pagination for the sync and async clients (SPEC 2.5, 3.5).

A ``Paginator`` walks a paginated SKU one page at a time, yielding either the
flattened items (``__iter__``) or whole run-result pages (``.pages()``). Items
are validated into the SKU's pydantic item model, so callers get attribute
access (``post.title``), not raw dicts (SPEC 3.3 erratum, B3).

Walk semantics (frozen):
    * Page 1 is ``run(slug, input, options)``.
    * Read the page data object: for a found-data SKU that is ``output.data``
      (or None when ``found`` is false); for a BARE SKU it is ``output`` itself
      (SPEC 1.2 erratum).
    * Yield each item from ``items_field``. If ``nextCursor`` is a non-empty
      string, set ``input["cursor"] = nextCursor`` and repeat; a null/empty
      ``nextCursor`` ends the walk.
    * ``options["max_items"]`` caps the TOTAL items yielded across all pages.
      It is NOT sent as the wire ``max_items`` shaping param from the iterator;
      the iterator manages paging itself.

The emitter targets the module-level helpers :func:`paginate` (sync) and
:func:`apaginate` (async): each takes the bound client, slug, input dict, the
items field name, the item model, the page-result model, and the envelope mode.
"""

from __future__ import annotations

import copy
from collections.abc import AsyncIterator, Iterator
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    TypeVar,
    cast,
)

from pydantic import BaseModel

from ._idempotency import page_idempotency_key
from ._transport import as_dict, validate_run_result
from .types import (
    AnyBareRunResult,
    BareRunResult,
    RequestOptions,
    RunResult,
)

if TYPE_CHECKING:
    from ._async_client import AsyncAnyAPI
    from ._client import AnyAPI

__all__ = ["Paginator", "AsyncPaginator", "paginate", "apaginate"]

Item = TypeVar("Item")
Data = TypeVar("Data")

_NEXT_CURSOR = "nextCursor"
_CURSOR = "cursor"


def _raw_page_data(raw: dict[str, Any], bare: bool) -> dict[str, Any] | None:
    """The page data dict from the RAW run dict, per envelope, using WIRE keys.

    For a bare SKU the data IS ``raw["output"]``; for a found-data SKU it is
    ``raw["output"]["data"]`` when ``found`` is true, else None. Reading from the
    raw dict (not the validated model) keeps cursor/items lookups keyed on the
    camelCase wire names even though the model exposes snake_case attributes.
    """
    output = raw.get("output")
    if not isinstance(output, dict):
        return None
    output_dict = cast("dict[str, Any]", output)
    if bare:
        return output_dict
    if output_dict.get("found") is not True:
        return None
    data = output_dict.get("data")
    return cast("dict[str, Any]", data) if isinstance(data, dict) else None


def _field(data: dict[str, Any] | None, key: str) -> object:
    """Read a WIRE-keyed field from the raw page data dict."""
    if data is None:
        return None
    return data.get(key)


def _validate_page(
    raw: dict[str, Any],
    data_model: type[BaseModel] | None,
    bare: bool,
) -> RunResult[Any] | BareRunResult[Any]:
    """Validate a raw run dict into the typed page result (found-data or bare)."""
    if bare:
        if data_model is None:
            return AnyBareRunResult.model_validate(raw)
        return BareRunResult[data_model].model_validate(raw)  # type: ignore[valid-type]
    if data_model is None:
        return validate_run_result(raw)
    return RunResult[data_model].model_validate(raw)  # type: ignore[valid-type]


def _validate_item(item: object, item_model: type[BaseModel] | None) -> Any:
    """Validate one page item into its pydantic model (or pass scalars through)."""
    if item_model is None:
        return item
    return item_model.model_validate(item)


class Paginator(Generic[Item, Data]):
    """Sync cursor walk over a paginated SKU."""

    def __init__(
        self,
        client: AnyAPI,
        slug: str,
        input: dict[str, Any],
        items_field: str,
        item_model: type[BaseModel] | None,
        data_model: type[BaseModel] | None,
        bare: bool,
        options: Any = None,
    ) -> None:
        self._client = client
        self._slug = slug
        self._input = copy.deepcopy(input)
        self._items_field = items_field
        self._item_model = item_model
        self._data_model = data_model
        self._bare = bare
        self._options = options
        self._cap = _max_items(options)
        self._page_options = _page_options(options)

    def _walk(
        self,
    ) -> Iterator[tuple[RunResult[Data] | BareRunResult[Data], dict[str, Any] | None]]:
        cursor: str | None = None
        page_number = 1
        while True:
            page_input = dict(self._input)
            if cursor is not None:
                page_input[_CURSOR] = cursor
            raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
                self._slug,
                page_input,
                cast(
                    "RequestOptions | None",
                    _options_for_page(self._page_options, page_number),
                ),
            )
            page = _validate_page(raw, self._data_model, self._bare)
            data = _raw_page_data(raw, self._bare)
            yield cast("RunResult[Data] | BareRunResult[Data]", page), data
            cursor = _next_cursor(data)
            if cursor is None:
                return
            page_number += 1

    def pages(self) -> Iterator[RunResult[Data] | BareRunResult[Data]]:
        """Yield whole run-result pages (read ``cost_usd`` per page)."""
        for page, _ in self._walk():
            yield page

    def __iter__(self) -> Iterator[Item]:
        count = 0
        for _page, data in self._walk():
            for item in _items(data, self._items_field):
                if self._cap is not None and count >= self._cap:
                    return
                yield cast("Item", _validate_item(item, self._item_model))
                count += 1
            if self._cap is not None and count >= self._cap:
                return


class AsyncPaginator(Generic[Item, Data]):
    """Async cursor walk over a paginated SKU."""

    def __init__(
        self,
        client: AsyncAnyAPI,
        slug: str,
        input: dict[str, Any],
        items_field: str,
        item_model: type[BaseModel] | None,
        data_model: type[BaseModel] | None,
        bare: bool,
        options: Any = None,
    ) -> None:
        self._client = client
        self._slug = slug
        self._input = copy.deepcopy(input)
        self._items_field = items_field
        self._item_model = item_model
        self._data_model = data_model
        self._bare = bare
        self._options = options
        self._cap = _max_items(options)
        self._page_options = _page_options(options)

    async def _walk(
        self,
    ) -> AsyncIterator[
        tuple[RunResult[Data] | BareRunResult[Data], dict[str, Any] | None]
    ]:
        cursor: str | None = None
        page_number = 1
        while True:
            page_input = dict(self._input)
            if cursor is not None:
                page_input[_CURSOR] = cursor
            raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
                self._slug,
                page_input,
                cast(
                    "RequestOptions | None",
                    _options_for_page(self._page_options, page_number),
                ),
            )
            page = _validate_page(raw, self._data_model, self._bare)
            data = _raw_page_data(raw, self._bare)
            yield cast("RunResult[Data] | BareRunResult[Data]", page), data
            cursor = _next_cursor(data)
            if cursor is None:
                return
            page_number += 1

    async def pages(self) -> AsyncIterator[RunResult[Data] | BareRunResult[Data]]:
        """Yield whole run-result pages (read ``cost_usd`` per page)."""
        async for page, _ in self._walk():
            yield page

    async def __aiter__(self) -> AsyncIterator[Item]:
        count = 0
        async for _page, data in self._walk():
            for item in _items(data, self._items_field):
                if self._cap is not None and count >= self._cap:
                    return
                yield cast("Item", _validate_item(item, self._item_model))
                count += 1
            if self._cap is not None and count >= self._cap:
                return


def _items(data: dict[str, Any] | None, items_field: str) -> list[Any]:
    raw_items = _field(data, items_field)
    if isinstance(raw_items, (list, tuple)):
        return list(cast("list[Any]", raw_items))
    return []


def _next_cursor(data: dict[str, Any] | None) -> str | None:
    next_cursor = _field(data, _NEXT_CURSOR)
    if isinstance(next_cursor, str) and next_cursor:
        return next_cursor
    return None


def _max_items(options: object) -> int | None:
    cap = as_dict(options).get("max_items")
    return cap if isinstance(cap, int) else None


def _page_options(options: object) -> object:
    """Strip max_items before sending: the iterator paces itself (SPEC 2.5)."""
    if not isinstance(options, dict):
        return options
    source = as_dict(cast("object", options))
    if "max_items" not in source:
        return source or None
    stripped: dict[str, object] = dict(source)
    stripped.pop("max_items", None)
    return stripped or None


def _options_for_page(options: object, page_number: int) -> object:
    """Derive a distinct explicit key for one page, preserving other options."""
    if not isinstance(options, dict):
        return options
    source = as_dict(cast("object", options))
    key = source.get("idempotency_key")
    if not isinstance(key, str):
        return source
    page_options: dict[str, object] = dict(source)
    page_options["idempotency_key"] = page_idempotency_key(key, page_number)
    return page_options


def paginate(
    client: AnyAPI,
    slug: str,
    input: dict[str, Any],
    items_field: str,
    item_model: type[BaseModel] | None = None,
    data_model: type[BaseModel] | None = None,
    bare: bool = False,
    options: Any = None,
) -> Paginator[Any, Any]:
    """Build a sync Paginator bound to the client's run seam (emitter target)."""
    return Paginator(
        client, slug, input, items_field, item_model, data_model, bare, options
    )


def apaginate(
    client: AsyncAnyAPI,
    slug: str,
    input: dict[str, Any],
    items_field: str,
    item_model: type[BaseModel] | None = None,
    data_model: type[BaseModel] | None = None,
    bare: bool = False,
    options: Any = None,
) -> AsyncPaginator[Any, Any]:
    """Build an async Paginator bound to the client's run seam (emitter target)."""
    return AsyncPaginator(
        client, slug, input, items_field, item_model, data_model, bare, options
    )
