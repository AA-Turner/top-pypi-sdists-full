from random import choice
from typing import List, Optional

from multidict import CIMultiDict
from pytest_httpserver import RequestHandler, HTTPServer

from spotipyio.logic.consts.spotify_consts import PLAYLISTS, TRACKS, URIS, POSITION
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.logic.internal_models import ChunkSize
from spotipyio.logic.internal_tools import DataChunksGenerator
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class PlaylistItemsAdderTestComponent(BaseTestComponent):
    def __init__(
        self,
        server: HTTPServer,
        headers: CIMultiDict[str],
        chunks_generator: DataChunksGenerator = DataChunksGenerator(),
    ):
        super().__init__(server=server, headers=headers)
        self._chunks_generator = chunks_generator

    def expect(self, playlist_id: str, uris: List[str], position: Optional[int] = None) -> List[RequestHandler]:
        return self._create_request_handlers(playlist_id=playlist_id, uris=uris, position=position)

    def expect_success(self, playlist_id: str, uris: List[str], position: Optional[int] = None) -> None:
        request_handlers = self._create_request_handlers(playlist_id=playlist_id, uris=uris, position=position)
        self._set_handlers_success(request_handlers)

    def expect_failure(
        self,
        playlist_id: str,
        uris: List[str],
        position: Optional[int] = None,
        response_json: Optional[Json] = None,
        status: Optional[int] = None,
    ) -> None:
        request_handlers = self._create_request_handlers(playlist_id=playlist_id, uris=uris, position=position)
        failed_handler = choice(request_handlers)
        successful_handlers = [handler for handler in request_handlers if handler != failed_handler]
        self._set_handlers_success(successful_handlers)
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)

        failed_handler.respond_with_json(status=status, response_json=response_json)

    def _create_request_handlers(
        self, playlist_id: str, uris: List[str], position: Optional[int]
    ) -> List[RequestHandler]:
        handlers = []

        for chunk in self._chunks_generator.generate_data_chunks(lst=uris, chunk_size=ChunkSize.ITEMS_ADDITION.value):
            payload = {URIS: chunk, POSITION: position}
            handler = self._expect_post_request(route=f"/{PLAYLISTS}/{playlist_id}/{TRACKS}", payload=payload)
            handlers.append(handler)

            if position is not None:
                position += ChunkSize.ITEMS_ADDITION.value

        return handlers

    @staticmethod
    def _set_handlers_success(request_handlers: List[RequestHandler]) -> None:
        for handler in request_handlers:
            response = SpotifyMockFactory.snapshot_response()
            handler.respond_with_json(response_json=response, status=201)
