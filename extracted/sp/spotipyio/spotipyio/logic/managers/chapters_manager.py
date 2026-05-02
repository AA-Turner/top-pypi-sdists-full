from typing import Type, Dict

from spotipyio.logic.contract import BaseManager, ISpotifyComponent
from spotipyio.logic.collectors import ChaptersCollector


class ChaptersManager(BaseManager):
    def __init__(self, info: ChaptersCollector):
        super().__init__()
        self.info = info

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "info": ChaptersCollector,
        }
