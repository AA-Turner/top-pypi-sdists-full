from spotipyio.logic.consts.spotify_consts import IMAGES
from spotipyio.logic.contract import BasePlaylistsUpdater
from spotipyio.auth import SpotifySession
from spotipyio.logic.internal_tools import ImageCompressor
from spotipyio.logic.utils import encode_image_to_base64


class PlaylistCoverUpdater(BasePlaylistsUpdater):
    def __init__(self, base_url: str, session: SpotifySession, image_compressor: ImageCompressor = ImageCompressor()):
        super().__init__(base_url=base_url, session=session)
        self._image_compressor = image_compressor

    async def run(self, playlist_id: str, image: bytes, compress_if_needed: bool = True) -> None:
        url = self._build_url(playlist_id)

        if compress_if_needed:
            image = self._image_compressor.compress(image)

        if image is not None:
            data = encode_image_to_base64(image)
            await self._session.put(url=url, data=data)

    @property
    def _route(self) -> str:
        return IMAGES
