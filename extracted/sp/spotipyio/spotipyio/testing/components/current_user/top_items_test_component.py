from typing import List, Optional

from pytest_httpserver import RequestHandler

from spotipyio.logic.consts.spotify_consts import TIME_RANGE, LIMIT
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.models import ItemsType, TimeRange
from spotipyio.testing.infra.base_test_component import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class TopItemsTestComponent(BaseTestComponent):
    def expect(self, items_type: ItemsType, time_range: TimeRange, limit: int = 50) -> List[RequestHandler]:
        request_handler = self._create_request_handler(items_type=items_type, time_range=time_range, limit=limit)
        return [request_handler]

    def expect_success(
        self, items_type: ItemsType, time_range: TimeRange, response_json: Optional[Json] = None, limit: int = 50
    ) -> None:
        handler = self._create_request_handler(items_type=items_type, time_range=time_range, limit=limit)

        if response_json is None:
            response_json = SpotifyMockFactory.user_top_items(items_type)

        handler.respond_with_json(response_json)

    def expect_failure(
        self,
        items_type: ItemsType,
        time_range: TimeRange,
        limit: int = 50,
        status: Optional[int] = None,
        response_json: Optional[int] = None,
    ) -> None:
        handler = self._create_request_handler(items_type=items_type, time_range=time_range, limit=limit)
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)

        handler.respond_with_json(status=status, response_json=response_json)

    def _create_request_handler(self, items_type: ItemsType, time_range: TimeRange, limit: int) -> RequestHandler:
        params = {TIME_RANGE: time_range.value, LIMIT: limit}
        return self._expect_get_request(route=f"/me/top/{items_type.value}", params=params, encode=True)
