from abc import ABC, abstractmethod
from functools import partial
from typing import List, Optional

from spotipyio.logic.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.auth import SpotifySession
from spotipyio.logic.internal_tools import PoolExecutor


class BasePaginationCollector(ISpotifyComponent, ABC):
    def __init__(self, base_url: str, session: SpotifySession, pool_executor: PoolExecutor = PoolExecutor()):
        super().__init__(base_url=base_url, session=session)
        self._pool_executor = pool_executor

    async def run(self, ids: List[str], max_pages: int = 1) -> List[dict]:
        func = partial(self.run_single, max_pages=max_pages)
        return await self._pool_executor.run(iterable=ids, func=func, expected_type=dict)

    async def run_single(self, id_: str, max_pages: int = 1) -> dict:
        url = self._url_format.format(id=id_)
        result = await self._session.get(url=url)

        if max_pages > 1:
            await self._append_additional_pages_items(result, max_pages)

        return result

    async def _append_additional_pages_items(self, result: dict, max_pages: int) -> None:
        current_page = 2
        next_url = self._extract_first_next_url(result)

        while next_url is not None and current_page <= max_pages:
            page = await self._session.get(url=next_url, params=self._additional_items_request_params)
            self._extend_existing_items(result, page)
            next_url = self._extract_subsequent_next_url(page)
            current_page += 1

    @property
    @abstractmethod
    def _url_format(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def _additional_items_request_params(self) -> Optional[dict]:
        raise NotImplementedError

    @abstractmethod
    def _extract_first_next_url(self, result: dict) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def _extract_subsequent_next_url(self, page: dict) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def _extend_existing_items(self, result: dict, page: dict) -> None:
        raise NotImplementedError
