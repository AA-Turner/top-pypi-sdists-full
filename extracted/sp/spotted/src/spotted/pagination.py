# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Generic, TypeVar, Optional
from typing_extensions import override

import httpx

from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

__all__ = ["SyncCursorURLPage", "AsyncCursorURLPage"]

_T = TypeVar("_T")


class SyncCursorURLPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    next: Optional[str] = None
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        url = self.next
        if url is None:
            return None

        return PageInfo(url=httpx.URL(url))


class AsyncCursorURLPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    next: Optional[str] = None
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        url = self.next
        if url is None:
            return None

        return PageInfo(url=httpx.URL(url))
