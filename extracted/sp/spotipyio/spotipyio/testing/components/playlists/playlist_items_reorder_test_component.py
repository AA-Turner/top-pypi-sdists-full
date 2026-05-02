from typing import List, Optional

from pytest_httpserver import RequestHandler

from spotipyio.logic.consts.spotify_consts import PLAYLISTS, TRACKS
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.models import PlaylistReorderRequest
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class PlaylistItemsReorderTestComponent(BaseTestComponent):
    def expect(self, request: PlaylistReorderRequest) -> List[RequestHandler]:
        request_handler = self._create_request_handler(request)
        return [request_handler]

    def expect_success(self, request: PlaylistReorderRequest, response_json: Optional[Json] = None) -> None:
        request_handler = self._create_request_handler(request)
        response = response_json or SpotifyMockFactory.snapshot_response()

        request_handler.respond_with_json(response)

    def expect_failure(
        self,
        request: PlaylistReorderRequest,
        response_json: Optional[Json] = None,
        status: Optional[int] = None,
    ) -> None:
        request_handler = self._create_request_handler(request)
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)

        request_handler.respond_with_json(status=status, response_json=response_json)

    def _create_request_handler(self, request: PlaylistReorderRequest) -> RequestHandler:
        return self._expect_put_request(
            route=f"/{PLAYLISTS}/{request.playlist_id}/{TRACKS}", payload=request.to_payload()
        )
