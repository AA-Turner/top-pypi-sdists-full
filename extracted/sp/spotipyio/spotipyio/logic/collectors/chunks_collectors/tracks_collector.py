from spotipyio.logic.consts.spotify_consts import TRACKS
from spotipyio.logic.contract import BaseChunksCollector
from spotipyio.logic.internal_models import ChunkSize


class TracksCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return TRACKS

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.TRACKS
