from __future__ import annotations

import inspect
import logging
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Callable, Iterable, Iterator
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any

import aiofiles
import makefun
import orjson
from pydantic import BaseModel

from fitrequest.decorators.hybrid_syntax import hybrid_syntax
from fitrequest.errors import InfinitePaginationError

logger = logging.getLogger(__name__)


@dataclass
class AbstractPage(ABC):
    """
    Represents a paginated request page with methods to access results and navigation.
    This structure must be overridden to customize behavior for different API responses.
    """

    data: Any

    @property
    @abstractmethod
    def results(self) -> Iterable:
        """Returns the iterable result extracted from the raw page data."""

    @property
    @abstractmethod
    def next_url(self) -> str | None:
        """Returns the URL for the next page if available, otherwise returns None."""

    @staticmethod
    @abstractmethod
    def save_results(filepath: Path, results: list[AbstractPage]) -> None:
        """Saves the list of page objects to the specified file path."""

    @staticmethod
    @abstractmethod
    async def async_save_results(filepath: Path, results: list[AbstractPage]) -> None:
        """Saves the list of page objects to the specified file path."""

    @classmethod
    def iterator(cls, get_page: Callable) -> Iterator[AbstractPage]:
        """Creates an iterator that retrieves all pages using the provided fitrequest method."""
        url_stack = []
        yield (next_page := cls(get_page()))

        while next_url := next_page.next_url:
            if next_url in url_stack:
                raise InfinitePaginationError(url_stack=[*url_stack, next_url])

            url_stack.append(next_url)
            yield (next_page := cls(get_page(url=next_url)))

    @classmethod
    async def async_iterator(cls, get_page: Callable) -> AsyncIterator[AbstractPage]:
        """Creates an async iterator that retrieves all pages using the provided fitrequest method."""
        url_stack = []
        yield (next_page := cls(await get_page()))

        while next_url := next_page.next_url:
            if next_url in url_stack:
                raise InfinitePaginationError(url_stack=[*url_stack, next_url])

            url_stack.append(next_url)
            yield (next_page := cls(await get_page(url=next_url)))

    @classmethod
    def merge_results(cls, get_page: Callable) -> list:
        """
        Combines all paginated results into a single merged list.
        Uses the provided fitrequest function to fetch pages and merges their results.
        """
        return [result for page in cls.iterator(get_page) for result in page.results]

    @classmethod
    async def async_merge_results(cls, get_page: Callable) -> list:
        """
        Combines all paginated results into a single merged list.
        Uses the provided fitrequest function to fetch pages and merges their results.
        """
        return [result async for page in cls.async_iterator(get_page) for result in page.results]


@dataclass
class PageDict(AbstractPage):
    """
    Specific implementation of pagination where the requests raw data is a dictionary containing two keywords:

    - ``result``: Iterable data for current page
    - ``next``: URL for next page
    """

    results_kw: str = 'results'
    next_kw: str = 'next'

    @property
    def results(self) -> Iterable:
        """Returns the iterable result extracted from the raw page data."""
        return self.data[self.results_kw]

    @property
    def next_url(self) -> str | None:
        """Returns the URL for the next page if available, otherwise returns None."""
        return self.data.get(self.next_kw)

    @staticmethod
    def save_results(filepath: Path, results: list) -> None:
        with open(filepath, mode='xb') as data_file:
            data_bytes = orjson.dumps(results, option=orjson.OPT_INDENT_2)
            data_file.write(data_bytes)

    @staticmethod
    async def async_save_results(filepath: Path, results: list) -> None:
        async with aiofiles.open(filepath, mode='xb') as data_file:
            data_bytes = orjson.dumps(results, option=orjson.OPT_INDENT_2)
            await data_file.write(data_bytes)


def _get_naked_method(fit_request: Callable, *args, **kwargs) -> Callable:
    """
    Creates a 'naked' version of a fitrequest request method.

    The **'naked' method** is designed to:
    * **Return the raw API response data** without applying Pydantic parsing or saving the result.
    * Be used primarily for **handling pagination**, allowing raw results from multiple pages to be collected first.

    This function also conveniently binds the provided positional (*args) and keyword (**kwargs)
    arguments to the new method.
    """
    from fitrequest.generator import Generator  # noqa: PLC0415

    method_config = fit_request.shared.get('method_config').model_copy(
        update={
            'save_method': False,
            'response_model': None,
        }
    )
    return partial(Generator.generate_method(method_config), *args, **kwargs)


def _apply_pydantic_model(data: Any, model: BaseModel) -> Any:
    if not model or not isinstance(model, type(BaseModel)):
        return data

    if isinstance(data, dict):
        return model(**data)

    if isinstance(data, list):
        return [model(**elem) for elem in data]

    return data


@hybrid_syntax
def paginated(page_cls: type[AbstractPage] = PageDict) -> Callable:
    """
    Decorator that automatically handles pagination for an endpoint.
    Combines all page results into one merged result instead of requiring manual handling.
    Custom behavior can be implemented by providing a specific AbstractPage subclass.
    """

    def decorator(fit_request: Callable) -> Callable:
        @makefun.wraps(fit_request)
        def wrapper(*args, **kwargs) -> Any:
            filepath = kwargs.get('filepath')
            kwargs['filepath'] = None

            get_page = _get_naked_method(fit_request, *args, **kwargs)
            final_results = page_cls.merge_results(get_page)

            if filepath is None:
                model = fit_request.shared.get('method_config').response_model
                return _apply_pydantic_model(final_results, model)

            page_cls.save_results(filepath, final_results)
            return None

        @makefun.wraps(fit_request)
        async def async_wrapper(*args, **kwargs) -> Any:
            filepath = kwargs.get('filepath')
            kwargs['filepath'] = None

            get_page = _get_naked_method(fit_request, *args, **kwargs)
            final_results = await page_cls.async_merge_results(get_page)

            if filepath is None:
                model = fit_request.shared.get('method_config').response_model
                return _apply_pydantic_model(final_results, model)

            await page_cls.async_save_results(filepath, final_results)
            return None

        return async_wrapper if inspect.iscoroutinefunction(fit_request) else wrapper

    return decorator
