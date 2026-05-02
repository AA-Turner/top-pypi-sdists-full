from typing import List

from spotipyio.logic.consts.spotify_consts import ARTISTS
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.logic.internal_models import ChunkSize
from spotipyio.testing.infra.base_chunks_test_component import BaseChunksTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class ArtistsInfoTestComponent(BaseChunksTestComponent):
    @property
    def _route(self) -> str:
        return f"/{ARTISTS}"

    @property
    def _chunk_size(self) -> ChunkSize:
        return ChunkSize.ARTISTS

    @staticmethod
    def _random_valid_response(ids: List[str]) -> Json:
        return SpotifyMockFactory.several_artists(ids)
