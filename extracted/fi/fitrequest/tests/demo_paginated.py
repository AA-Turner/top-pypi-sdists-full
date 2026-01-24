from collections.abc import AsyncIterator, Callable, Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

import aiofiles
import pytest
from pydantic import BaseModel

from fitrequest.client import FitRequest
from fitrequest.decorators import AbstractPage, PageDict, fit, paginated


@dataclass
class CustomPageDict(PageDict):
    results_kw: str = 'data'
    next_kw: str = 'next_page'


class CustomPageString(AbstractPage):
    def __init__(self, data: str) -> None:
        self._results, self._next_url = data.split(sep='|', maxsplit=1)

    @property
    def results(self) -> Iterable:
        return map(int, self._results.split(sep=','))

    @property
    def next_url(self) -> str | None:
        return self._next_url if self._next_url != '' else None

    @staticmethod
    def save_results(filepath: Path, results: list) -> None:
        filepath.write_text('\n'.join(str(num) for num in results))

    @staticmethod
    async def async_save_results(filepath: Path, results: list) -> None:
        async with aiofiles.open(filepath, mode='x') as data_file:
            await data_file.write('\n'.join(str(num) for num in results))


class CustomObject(BaseModel):
    oid: int
    name: str


class TestClient(FitRequest):
    client_name = 'test_client'
    base_url = 'https://test.skillcorner.fr'

    @paginated
    @fit(endpoint='/items/')
    def get_items(self) -> list[dict]: ...

    @paginated
    @fit(endpoint='/items/')
    async def async_get_items(self) -> list[dict]: ...

    @paginated(page_cls=CustomPageDict)
    @fit(endpoint='/items/')
    def get_custom_dict_items(self) -> list[dict]: ...

    @paginated(page_cls=CustomPageDict)
    @fit(endpoint='/items/')
    async def async_get_custom_dict_items(self) -> list[dict]: ...

    @paginated(page_cls=CustomPageString)
    @fit(endpoint='/items/')
    def get_custom_str_items(self) -> list[int]: ...

    @paginated(page_cls=CustomPageString)
    @fit(endpoint='/items/')
    async def async_get_custom_str_items(self) -> list[int]: ...

    @paginated
    @fit(endpoint='/items/', save_method=True)
    def save_get_items(self, filepath: str) -> None: ...

    @paginated
    @fit(endpoint='/items/', save_method=True)
    async def async_save_get_items(self, filepath: str) -> None: ...

    @paginated(page_cls=CustomPageDict)
    @fit(endpoint='/items/', save_method=True)
    def get_custom_save_dict_items(self, filepath: str) -> None: ...

    @paginated(page_cls=CustomPageDict)
    @fit(endpoint='/items/', save_method=True)
    async def async_get_custom_save_dict_items(self, filepath: str) -> None: ...

    @paginated(page_cls=CustomPageString)
    @fit(endpoint='/items/', save_method=True)
    def get_custom_save_str_items(self, filepath: str) -> None: ...

    @paginated(page_cls=CustomPageString)
    @fit(endpoint='/items/', save_method=True)
    async def async_get_custom_save_str_items(self, filepath: str) -> None: ...

    @paginated
    @fit(endpoint='/items/')
    def get_items_model(self) -> list[CustomObject]: ...

    @paginated
    @fit(endpoint='/items/')
    async def async_get_items_model(self) -> list[CustomObject]: ...


@pytest.fixture
def test_client():
    return TestClient()
