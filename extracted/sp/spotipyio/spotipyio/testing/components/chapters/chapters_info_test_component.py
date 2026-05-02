from typing import List

from spotipyio.logic.consts.spotify_consts import CHAPTERS
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.logic.internal_models import ChunkSize
from spotipyio.testing.infra.base_chunks_test_component import BaseChunksTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class ChaptersInfoTestComponent(BaseChunksTestComponent):
    @property
    def _route(self) -> str:
        return f"/{CHAPTERS}"

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.CHAPTERS

    @staticmethod
    def _random_valid_response(ids: List[str]) -> Json:
        return SpotifyMockFactory.several_chapters(ids)
