# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Any, List, Type, Generic, Mapping, TypeVar, Optional, cast
from typing_extensions import Protocol, override, runtime_checkable

from httpx import Response

from ._utils import is_mapping
from ._models import BaseModel
from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

__all__ = [
    "SyncPageResponse",
    "AsyncPageResponse",
    "SyncCursorPage",
    "AsyncCursorPage",
    "SyncTopLevelArray",
    "AsyncTopLevelArray",
    "SyncChunkPagination",
    "AsyncChunkPagination",
    "SyncGenerationJobsPagination",
    "AsyncGenerationJobsPagination",
]

_BaseModelT = TypeVar("_BaseModelT", bound=BaseModel)

_T = TypeVar("_T")


@runtime_checkable
class CursorPageItem(Protocol):
    id: str


class SyncPageResponse(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]
    current_page: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        current_page = self.current_page
        if current_page is None:
            current_page = 1

        return PageInfo(params={"page": current_page + 1})


class AsyncPageResponse(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]
    current_page: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        current_page = self.current_page
        if current_page is None:
            current_page = 1

        return PageInfo(params={"page": current_page + 1})


class SyncCursorPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

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
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

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


class SyncTopLevelArray(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
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

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {"items": data}),
            },
        )


class AsyncTopLevelArray(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
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

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {"items": data}),
            },
        )


class SyncChunkPagination(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    chunks: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        chunks = self.chunks
        if not chunks:
            return []
        return chunks

    @override
    def next_page_info(self) -> None:
        """
        This page represents a response that isn't actually paginated at the API level
        so there will never be a next page.
        """
        return None


class AsyncChunkPagination(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    chunks: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        chunks = self.chunks
        if not chunks:
            return []
        return chunks

    @override
    def next_page_info(self) -> None:
        """
        This page represents a response that isn't actually paginated at the API level
        so there will never be a next page.
        """
        return None


class SyncGenerationJobsPagination(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    generation_jobs: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        generation_jobs = self.generation_jobs
        if not generation_jobs:
            return []
        return generation_jobs

    @override
    def next_page_info(self) -> None:
        """
        This page represents a response that isn't actually paginated at the API level
        so there will never be a next page.
        """
        return None


class AsyncGenerationJobsPagination(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    generation_jobs: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        generation_jobs = self.generation_jobs
        if not generation_jobs:
            return []
        return generation_jobs

    @override
    def next_page_info(self) -> None:
        """
        This page represents a response that isn't actually paginated at the API level
        so there will never be a next page.
        """
        return None
