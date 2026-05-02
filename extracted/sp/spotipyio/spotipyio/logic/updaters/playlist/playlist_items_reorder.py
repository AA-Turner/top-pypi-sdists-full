from spotipyio.logic.consts.spotify_consts import TRACKS
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.logic.contract import BasePlaylistsUpdater
from spotipyio.models import PlaylistReorderRequest


class PlaylistItemsReorder(BasePlaylistsUpdater):
    async def run(self, request: PlaylistReorderRequest) -> Json:
        url = self._build_url(request.playlist_id)
        return await self._session.put(url=url, payload=request.to_payload())

    @property
    def _route(self) -> str:
        return TRACKS
