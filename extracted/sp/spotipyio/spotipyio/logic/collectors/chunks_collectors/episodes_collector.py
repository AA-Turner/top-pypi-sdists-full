from spotipyio.logic.consts.spotify_consts import EPISODES
from spotipyio.logic.contract import BaseChunksCollector
from spotipyio.logic.internal_models import ChunkSize


class EpisodesCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return EPISODES

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.EPISODES
