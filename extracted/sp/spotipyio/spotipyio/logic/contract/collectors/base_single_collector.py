from abc import abstractmethod, ABC
from functools import partial
from typing import List, Optional

from spotipyio.logic.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.auth import SpotifySession
from spotipyio.logic.internal_tools import PoolExecutor


class BaseSingleCollector(ISpotifyComponent, ABC):
    def __init__(self, base_url: str, session: SpotifySession, pool_executor: PoolExecutor = PoolExecutor()):
        super().__init__(base_url=base_url, session=session)
        self._pool_executor = pool_executor

    async def run(self, ids: List[str], **params) -> List[dict]:
        func = partial(self.run_single, params=params)
        return await self._pool_executor.run(iterable=ids, func=func, expected_type=dict)

    async def run_single(self, id_: str, params: Optional[dict] = None) -> dict:
        route = self._route_format.format(id=id_)
        url = f"{self._base_url}/{route}"

        return await self._session.get(url=url, params=params)

    @property
    @abstractmethod
    def _route_format(self) -> str:
        raise NotImplementedError
