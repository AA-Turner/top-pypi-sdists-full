from typing import Type, Dict

from spotipyio.logic.contract import BaseManager, ISpotifyComponent
from spotipyio.logic.collectors import UserPlaylistsCollector


class UsersManager(BaseManager):
    def __init__(self, playlists: UserPlaylistsCollector):
        super().__init__()
        self.playlists = playlists

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "playlists": UserPlaylistsCollector,
        }
