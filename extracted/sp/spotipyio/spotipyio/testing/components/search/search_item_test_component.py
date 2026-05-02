from typing import List, Optional

from pytest_httpserver import RequestHandler

from spotipyio.logic.consts.typing_consts import Json
from spotipyio.models import SearchItem
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class SearchItemTestComponent(BaseTestComponent):
    def expect(self, search_item: SearchItem) -> List[RequestHandler]:
        return [self._create_request_handler(search_item)]

    def expect_success(self, search_item: SearchItem, response_json: Optional[Json] = None) -> None:
        handler = self._create_request_handler(search_item)
        handler.respond_with_json(response_json=response_json or SpotifyMockFactory.search_response(search_item))

    def expect_failure(
        self, search_item: SearchItem, status: Optional[int] = None, response_json: Optional[Json] = None
    ) -> None:
        status, response_json = self._create_invalid_response(status, response_json)
        handler = self._create_request_handler(search_item)

        handler.respond_with_json(status=status, response_json=response_json)

    def _create_request_handler(self, search_item: SearchItem) -> RequestHandler:
        return self._expect_get_request(route="/search", params=search_item.to_query_params())
