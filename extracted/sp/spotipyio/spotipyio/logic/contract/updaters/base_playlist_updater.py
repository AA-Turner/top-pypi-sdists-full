from abc import ABC, abstractmethod

from spotipyio.logic.consts.spotify_consts import PLAYLISTS
from spotipyio.logic.contract import ISpotifyComponent


class BasePlaylistsUpdater(ISpotifyComponent, ABC):
    @property
    @abstractmethod
    def _route(self) -> str:
        raise NotImplementedError

    def _build_url(self, playlist_id: str) -> str:
        return f"{self._base_url}/{PLAYLISTS}/{playlist_id}/{self._route}"
