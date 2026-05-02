from typing import List, Optional

from pytest_httpserver import RequestHandler

from spotipyio.logic.consts.typing_consts import Json
from spotipyio.testing.infra.base_test_component import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class ArtistsTopTracksTestComponent(BaseTestComponent):
    def expect(self, ids: List[str]) -> List[RequestHandler]:
        request_handlers = []

        for artist_id in ids:
            handler = self._create_request_handler(artist_id)
            request_handlers.append(handler)

        return request_handlers

    def expect_success(self, id_: str, response_json: Optional[Json] = None) -> None:
        response = response_json or SpotifyMockFactory.several_tracks()
        request_handler = self._create_request_handler(id_)

        request_handler.respond_with_json(response)

    def expect_failure(self, id_: str, status: Optional[int] = None, response_json: Optional[Json] = None) -> None:
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)
        request_handler = self._create_request_handler(id_)

        request_handler.respond_with_json(response_json=response_json, status=status)

    def _create_request_handler(self, artist_id: str) -> RequestHandler:
        return self._expect_get_request(f"/artists/{artist_id}/top-tracks")
