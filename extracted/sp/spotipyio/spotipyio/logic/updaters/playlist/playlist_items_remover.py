from typing import List

from spotipyio.logic.consts.spotify_consts import TRACKS, URI, SNAPSHOT_ID
from spotipyio.logic.contract import BasePlaylistsUpdater
from spotipyio.auth import SpotifySession
from spotipyio.logic.internal_models import ChunkSize
from spotipyio.logic.internal_tools import DataChunksGenerator


class PlaylistItemsRemover(BasePlaylistsUpdater):
    def __init__(
        self, base_url: str, session: SpotifySession, chunks_generator: DataChunksGenerator = DataChunksGenerator()
    ):
        super().__init__(base_url=base_url, session=session)
        self._chunks_generator = chunks_generator

    async def run(self, playlist_id: str, uris: List[str], snapshot_id: str) -> str:
        chunks = self._chunks_generator.generate_data_chunks(lst=uris, chunk_size=ChunkSize.ITEMS_REMOVAL.value)
        url = self._build_url(playlist_id)

        for chunk in chunks:
            snapshot_id = await self._remove_single_chunk(url=url, uris=chunk, snapshot_id=snapshot_id)

        return snapshot_id

    async def _remove_single_chunk(self, url: str, snapshot_id: str, uris: List[str]) -> str:
        payload = {TRACKS: [{URI: uri} for uri in uris], SNAPSHOT_ID: snapshot_id}
        response = await self._session.delete(url=url, payload=payload)

        return response[SNAPSHOT_ID]

    @property
    def _route(self) -> str:
        return TRACKS
