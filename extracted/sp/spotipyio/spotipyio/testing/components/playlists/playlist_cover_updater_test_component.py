from typing import List, Optional

from pytest_httpserver import RequestHandler
from werkzeug import Response

from spotipyio.logic.consts.spotify_consts import PLAYLISTS, IMAGES
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.logic.utils import encode_image_to_base64


class PlaylistsCoverUpdaterTestComponent(BaseTestComponent):
    def expect(self, playlist_id: str, image: bytes) -> List[RequestHandler]:
        return [self._create_request_handler(playlist_id, image)]

    def expect_success(self, playlist_id: str, image: bytes) -> None:
        request_handler = self._create_request_handler(playlist_id, image)
        response = Response(status=202)

        request_handler.respond_with_response(response)

    def expect_failure(
        self, playlist_id: str, image: bytes, status: Optional[int] = None, response_json: Optional[Json] = None
    ) -> None:
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)
        request_handler = self._create_request_handler(playlist_id, image)

        request_handler.respond_with_json(status=status, response_json=response_json)

    def _create_request_handler(self, playlist_id: str, image: bytes) -> RequestHandler:
        data = encode_image_to_base64(image)
        return self._expect_put_request(route=f"/{PLAYLISTS}/{playlist_id}/{IMAGES}", data=data)
