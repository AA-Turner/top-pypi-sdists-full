from typing import List, Optional

from pytest_httpserver import RequestHandler

from spotipyio.logic.consts.spotify_consts import PLAYLISTS, TRACKS, URIS
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class PlaylistItemsReplacerTestComponent(BaseTestComponent):
    def expect(self, playlist_id: str, uris: List[str]) -> List[RequestHandler]:
        request_handler = self._create_request_handler(playlist_id=playlist_id, uris=uris)
        return [request_handler]

    def expect_success(self, playlist_id: str, uris: List[str], response_json: Optional[Json] = None) -> None:
        request_handler = self._create_request_handler(playlist_id=playlist_id, uris=uris)
        response = response_json or SpotifyMockFactory.snapshot_response()

        request_handler.respond_with_json(response)

    def expect_failure(
        self,
        playlist_id: str,
        uris: List[str],
        response_json: Optional[Json] = None,
        status: Optional[int] = None,
    ) -> None:
        request_handler = self._create_request_handler(playlist_id=playlist_id, uris=uris)
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)

        request_handler.respond_with_json(status=status, response_json=response_json)

    def _create_request_handler(self, playlist_id: str, uris: List[str]) -> RequestHandler:
        return self._expect_put_request(route=f"/{PLAYLISTS}/{playlist_id}/{TRACKS}", payload={URIS: uris})
