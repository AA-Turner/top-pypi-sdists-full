from functools import partial
from typing import List, Dict

from spotipyio.auth import SpotifySession
from spotipyio.logic.consts.spotify_consts import NEXT, ITEMS
from spotipyio.logic.contract import ISpotifyComponent
from spotipyio.logic.internal_tools import PoolExecutor
from spotipyio.logic.utils import safe_nested_get
from spotipyio.models import SearchItem


class SearchCollector(ISpotifyComponent):
    def __init__(self, base_url: str, session: SpotifySession, pool_executor: PoolExecutor = PoolExecutor()):
        super().__init__(base_url=base_url, session=session)
        self._pool_executor = pool_executor

    async def run(self, search_items: List[SearchItem], max_pages: int = 1) -> List[dict]:
        func = partial(self.run_single, max_pages=max_pages)
        return await self._pool_executor.run(iterable=search_items, func=func, expected_type=dict)

    async def run_single(self, search_item: SearchItem, max_pages: int = 1) -> dict:
        result = await self._session.get(url=self._url, params=search_item.to_query_params())

        if max_pages > 1:
            await self._append_additional_pages_items(result, max_pages)

        return result

    async def _append_additional_pages_items(self, result: dict, max_pages: int) -> None:
        current_page = 2
        next_urls = self._extract_first_next_urls(result)

        while next_urls and current_page <= max_pages:
            for search_type, next_url in next_urls.items():
                page = await self._session.get(url=next_url)
                self._extend_existing_items(search_type, result, page)
                self._update_next_urls(next_urls, page, search_type)

            current_page += 1

    @staticmethod
    def _extract_first_next_urls(result: dict) -> Dict[str, str]:
        next_urls = {}

        for search_type in result.keys():
            next_type_url = safe_nested_get(result, [search_type, NEXT])

            if isinstance(next_type_url, str):
                next_urls[search_type] = next_type_url

        return next_urls

    @staticmethod
    def _update_next_urls(next_urls: Dict[str, str], page: dict, search_type: str) -> None:
        next_type_url = safe_nested_get(page, [search_type, NEXT])

        if isinstance(next_type_url, str):
            next_urls[search_type] = next_type_url
        else:
            next_urls.pop(search_type)

    @staticmethod
    def _extend_existing_items(search_type: str, result: dict, page: dict) -> None:
        existing_items: List[dict] = safe_nested_get(result, [search_type, ITEMS])

        if existing_items:
            page_items = safe_nested_get(page, [search_type, ITEMS], default=[])
            existing_items.extend(page_items)

    @property
    def _url(self) -> str:
        return f"{self._base_url}/search"
