# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Any, List, Generic, TypeVar, Optional, cast
from typing_extensions import Protocol, override, runtime_checkable

from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

__all__ = [
    "SyncCursorPage",
    "AsyncCursorPage",
    "SyncCursorPageVectors",
    "AsyncCursorPageVectors",
    "SyncCursorPageByName",
    "AsyncCursorPageByName",
    "SyncAPIListPage",
    "AsyncAPIListPage",
]

_T = TypeVar("_T")


@runtime_checkable
class CursorPageItem(Protocol):
    id: str


@runtime_checkable
class CursorPageVectorsItem(Protocol):
    id: str


@runtime_checkable
class CursorPageByNameItem(Protocol):
    name: str


class SyncCursorPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    has_more: Optional[bool] = None
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        is_forwards = not self._options.params.get("ending_before", False)

        items = self.items
        if not items:
            return None

        if is_forwards:
            item = cast(Any, items[-1])
            if not isinstance(item, CursorPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"starting_after": item.id})
        else:
            item = cast(Any, self.items[0])
            if not isinstance(item, CursorPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"ending_before": item.id})


class AsyncCursorPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    has_more: Optional[bool] = None
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        is_forwards = not self._options.params.get("ending_before", False)

        items = self.items
        if not items:
            return None

        if is_forwards:
            item = cast(Any, items[-1])
            if not isinstance(item, CursorPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"starting_after": item.id})
        else:
            item = cast(Any, self.items[0])
            if not isinstance(item, CursorPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"ending_before": item.id})


class SyncCursorPageVectors(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    has_more: Optional[bool] = None
    vectors: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        vectors = self.vectors
        if not vectors:
            return []
        return vectors

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        is_forwards = not self._options.params.get("ending_before", False)

        vectors = self.vectors
        if not vectors:
            return None

        if is_forwards:
            item = cast(Any, vectors[-1])
            if not isinstance(item, CursorPageVectorsItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"starting_after": item.id})
        else:
            item = cast(Any, self.vectors[0])
            if not isinstance(item, CursorPageVectorsItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"ending_before": item.id})


class AsyncCursorPageVectors(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    has_more: Optional[bool] = None
    vectors: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        vectors = self.vectors
        if not vectors:
            return []
        return vectors

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        is_forwards = not self._options.params.get("ending_before", False)

        vectors = self.vectors
        if not vectors:
            return None

        if is_forwards:
            item = cast(Any, vectors[-1])
            if not isinstance(item, CursorPageVectorsItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"starting_after": item.id})
        else:
            item = cast(Any, self.vectors[0])
            if not isinstance(item, CursorPageVectorsItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"ending_before": item.id})


class SyncCursorPageByName(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    has_more: Optional[bool] = None
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        is_forwards = not self._options.params.get("ending_before", False)

        items = self.items
        if not items:
            return None

        if is_forwards:
            item = cast(Any, items[-1])
            if not isinstance(item, CursorPageByNameItem) or item.name is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"starting_after": item.name})
        else:
            item = cast(Any, self.items[0])
            if not isinstance(item, CursorPageByNameItem) or item.name is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"ending_before": item.name})


class AsyncCursorPageByName(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    has_more: Optional[bool] = None
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        is_forwards = not self._options.params.get("ending_before", False)

        items = self.items
        if not items:
            return None

        if is_forwards:
            item = cast(Any, items[-1])
            if not isinstance(item, CursorPageByNameItem) or item.name is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"starting_after": item.name})
        else:
            item = cast(Any, self.items[0])
            if not isinstance(item, CursorPageByNameItem) or item.name is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"ending_before": item.name})


class SyncAPIListPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> None:
        """
        This page represents a response that isn't actually paginated at the API level
        so there will never be a next page.
        """
        return None


class AsyncAPIListPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> None:
        """
        This page represents a response that isn't actually paginated at the API level
        so there will never be a next page.
        """
        return None
