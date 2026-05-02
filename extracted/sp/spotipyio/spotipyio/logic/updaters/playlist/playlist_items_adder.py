from typing import List, Optional

from spotipyio.logic.consts.spotify_consts import URIS, TRACKS, POSITION, SNAPSHOT_ID
from spotipyio.logic.contract import BasePlaylistsUpdater
from spotipyio.auth import SpotifySession
from spotipyio.logic.internal_models import ChunkSize
from spotipyio.logic.internal_tools import DataChunksGenerator


class PlaylistItemsAdder(BasePlaylistsUpdater):
    def __init__(
        self, base_url: str, session: SpotifySession, chunks_generator: DataChunksGenerator = DataChunksGenerator()
    ):
        super().__init__(base_url=base_url, session=session)
        self._chunks_generator = chunks_generator

    async def run(self, playlist_id: str, uris: List[str], position: Optional[int] = None) -> List[str]:
        chunks = self._chunks_generator.generate_data_chunks(lst=uris, chunk_size=ChunkSize.ITEMS_ADDITION.value)
        url = self._build_url(playlist_id)
        snapshots = []

        for chunk in chunks:
            chunk_snapshot = await self._post_single_chunk(url=url, uris=chunk, position=position)
            snapshots.append(chunk_snapshot)

            if position is not None:
                position += ChunkSize.ITEMS_ADDITION.value

        return snapshots

    async def _post_single_chunk(self, url: str, uris: List[str], position: Optional[int] = None) -> str:
        payload = {URIS: uris, POSITION: position}
        response = await self._session.post(url=url, payload=payload)

        return response[SNAPSHOT_ID]

    @property
    def _route(self) -> str:
        return TRACKS
