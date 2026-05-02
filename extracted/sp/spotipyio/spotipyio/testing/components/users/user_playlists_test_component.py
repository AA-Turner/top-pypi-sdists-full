from typing import List, Optional

from pytest_httpserver import RequestHandler

from spotipyio.logic.consts.spotify_consts import PLAYLISTS, USERS
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class UserPlaylistsTestComponent(BaseTestComponent):
    def expect(self, user_id: str) -> List[RequestHandler]:
        return [self._create_request_handler(user_id)]

    def expect_success(self, user_id: str, response_json: Optional[Json] = None) -> None:
        request_handler = self._create_request_handler(user_id)
        response = response_json or SpotifyMockFactory.paged_playlists()

        request_handler.respond_with_json(response)

    def expect_failure(self, user_id: str, status: Optional[int] = None, response_json: Optional[Json] = None) -> None:
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)
        request_handler = self._create_request_handler(user_id)

        request_handler.respond_with_json(status=status, response_json=response_json)

    def _create_request_handler(self, user_id: str) -> RequestHandler:
        return self._expect_get_request(route=f"/{USERS}/{user_id}/{PLAYLISTS}", params={"offset": "0", "limit": "50"})
