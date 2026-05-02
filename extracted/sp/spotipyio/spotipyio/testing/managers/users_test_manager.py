from typing import Dict, Type

from spotipyio.testing.components import UserPlaylistsTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class UsersTestManager(BaseTestManager):
    def __init__(self, playlists: UserPlaylistsTestComponent):
        super().__init__()
        self.playlists = playlists

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "playlists": UserPlaylistsTestComponent,
        }
