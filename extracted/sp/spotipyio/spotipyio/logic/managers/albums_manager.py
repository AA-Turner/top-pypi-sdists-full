from typing import Type, Dict

from spotipyio.logic.contract import BaseManager, ISpotifyComponent
from spotipyio.logic.collectors import AlbumsCollector


class AlbumsManager(BaseManager):
    def __init__(self, info: AlbumsCollector):
        super().__init__()
        self.info = info

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "info": AlbumsCollector,
        }
