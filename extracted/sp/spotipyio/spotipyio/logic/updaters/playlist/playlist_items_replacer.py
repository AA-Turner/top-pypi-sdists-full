from typing import List

from spotipyio.logic.consts.spotify_consts import TRACKS, URIS
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.logic.contract import BasePlaylistsUpdater


class PlaylistItemsReplacer(BasePlaylistsUpdater):
    async def run(self, playlist_id: str, uris: List[str]) -> Json:
        url = self._build_url(playlist_id)
        return await self._session.put(url=url, payload={URIS: uris})

    @property
    def _route(self) -> str:
        return TRACKS
