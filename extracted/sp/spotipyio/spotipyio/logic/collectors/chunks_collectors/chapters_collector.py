from spotipyio.logic.consts.spotify_consts import CHAPTERS
from spotipyio.logic.contract import BaseChunksCollector
from spotipyio.logic.internal_models import ChunkSize


class ChaptersCollector(BaseChunksCollector):
    @property
    def _route(self) -> str:
        return CHAPTERS

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.CHAPTERS
