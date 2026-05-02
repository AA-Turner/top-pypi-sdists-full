from typing import List, Optional

from pytest_httpserver import RequestHandler

from spotipyio.logic.consts.spotify_consts import PLAYLISTS, USERS
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.models import PlaylistCreationRequest
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class PlaylistsCreatorTestComponent(BaseTestComponent):
    def expect(self, request: PlaylistCreationRequest) -> List[RequestHandler]:
        return [self._create_request_handler(request)]

    def expect_success(self, request: PlaylistCreationRequest, response_json: Optional[Json] = None) -> None:
        request_handler = self._create_request_handler(request)
        response = response_json or SpotifyMockFactory.playlist(
            user_id=request.user_id, name=request.name, public=request.public, description=request.description
        )

        request_handler.respond_with_json(response_json=response, status=201)

    def expect_failure(
        self, request: PlaylistCreationRequest, status: Optional[int] = None, response_json: Optional[Json] = None
    ) -> None:
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)
        request_handler = self._create_request_handler(request)

        request_handler.respond_with_json(status=status, response_json=response_json)

    def _create_request_handler(self, request: PlaylistCreationRequest) -> RequestHandler:
        return self._expect_post_request(route=f"/{USERS}/{request.user_id}/{PLAYLISTS}", payload=request.to_payload())
