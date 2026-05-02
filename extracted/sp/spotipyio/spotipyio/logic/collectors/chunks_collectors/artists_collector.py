from spotipyio.logic.consts.spotify_consts import ARTISTS
from spotipyio.logic.contract import BaseChunksCollector
from spotipyio.logic.internal_models import ChunkSize


class ArtistsCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return ARTISTS

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.ARTISTS
