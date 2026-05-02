from spotipyio.logic.consts.spotify_consts import ALBUMS
from spotipyio.logic.contract import BaseChunksCollector
from spotipyio.logic.internal_models import ChunkSize


class AlbumsCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return ALBUMS

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.ALBUMS
