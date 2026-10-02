from __future__ import annotations

from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    TypeVar,
)

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from typing_extensions import Annotated

from istari_digital_client.legacy.log_utils import log_method
from istari_digital_client.legacy.protocol import PageLike

T = TypeVar("T", bound=BaseModel)

__all__ = ["Pageable", "PageLike"]


class Pageable(BaseModel, Generic[T]):
    """
    A mixin providing iteration capabilities for paginated API responses.

    This mixin adds iter_pages() and iter_items() methods to paginated response classes,
    allowing iteration through all pages and all items across multiple API calls.

    It represents a single page of items returned from a paginated API and includes
    metadata such as total item count, current page number, and total pages.
    """

    items: List[T]
    total: Optional[Annotated[int, Field(strict=True, ge=0)]]
    page: Optional[Annotated[int, Field(strict=True, ge=1)]]
    size: Optional[Annotated[int, Field(strict=True, ge=1)]]
    pages: Optional[Annotated[int, Field(strict=True, ge=0)]] = None
    __client_fields__: ClassVar[List[str]] = ["items"]
    _list_method: Optional[Callable[..., "Pageable[T]"]] = PrivateAttr(default=None)
    _list_method_args: Optional[Dict[str, Any]] = PrivateAttr(default=None)
    __properties: ClassVar[List[str]] = ["items", "total", "page", "size", "pages"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def _validate_pagination_setup(self) -> None:
        """Validate that pagination is properly configured."""
        if self._list_method is None:
            raise ValueError("No list method defined for pagination")
        if self._list_method_args is None:
            raise ValueError("No list method arguments defined for pagination")

    def _get_base_args(self) -> Dict[str, Any]:
        """
        Prepare base arguments for the list method, excluding pagination parameters
        and private attributes.
        """
        return {
            k: v
            for k, v in (self._list_method_args or {}).items()
            if k not in {"page", "size", "self"} and not k.startswith("__")
        }

    @log_method
    def iter_pages(self) -> Iterator["Pageable[T]"]:
        """
        Iterate over all pages, starting with the current page.

        Yields the current page first, then fetches subsequent pages using
        the configured list method.

        :raises ValueError: If either `_list_method` or `_list_method_args` is not set.
        """
        # Early exit for empty results - don't yield empty page
        if self.total == 0:
            return

        # Yield current page first (no API call needed)
        yield self

        # Early exit if this is the only page
        if self.pages and (self.page or 1) >= self.pages:
            return

        self._validate_pagination_setup()
        assert self._list_method is not None  # Validated above, helps mypy

        current_page = (self.page or 1) + 1
        size = self.size or 10
        base_args = self._get_base_args()

        while True:
            page = self._list_method(**base_args, page=current_page, size=size)

            if page.total == 0:
                break

            yield page

            current_page += 1

            if page.pages and current_page > page.pages:
                break

    @log_method
    def iter_items(self) -> Iterator[T]:
        """
        Iterate over all items across all pages, starting with the current page.

        Yields items from the current page first, then fetches subsequent pages
        and yields their items. This method is independent of iter_pages().
        """
        # Yield items from current page first (no API call needed)
        yield from self.items

        # Early exit if this is the only page or no more pages
        if self.total == 0 or (self.pages and (self.page or 1) >= self.pages):
            return

        self._validate_pagination_setup()
        assert self._list_method is not None  # Validated above, helps mypy

        current_page = (self.page or 1) + 1
        size = self.size or 10
        base_args = self._get_base_args()

        while True:
            page = self._list_method(**base_args, page=current_page, size=size)

            if page.total == 0:
                break

            yield from page.items

            current_page += 1

            if page.pages and current_page > page.pages:
                break
