from spotipyio.logic.consts.spotify_consts import PLAYLISTS, USERS
from spotipyio.logic.contract import ISpotifyComponent
from spotipyio.models import PlaylistCreationRequest


class PlaylistsCreator(ISpotifyComponent):
    async def run(self, request: PlaylistCreationRequest) -> dict:
        url = self._url_format.format(user_id=request.user_id)
        return await self._session.post(url=url, payload=request.to_payload())

    @property
    def _url_format(self) -> str:
        return f"{self._base_url}/{USERS}/{{user_id}}/{PLAYLISTS}"
