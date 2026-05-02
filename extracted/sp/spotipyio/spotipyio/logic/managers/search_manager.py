from typing import Type, Dict

from spotipyio.logic.collectors import SearchCollector
from spotipyio.logic.contract import BaseManager, ISpotifyComponent


class SearchManager(BaseManager):
    def __init__(self, search_item: SearchCollector):
        super().__init__()
        self.search_item = search_item

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "search_item": SearchCollector,
        }
