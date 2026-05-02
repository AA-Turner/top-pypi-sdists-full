from typing import List, Optional

from multidict import CIMultiDict
from pytest_httpserver import RequestHandler, HTTPServer

from spotipyio.logic.consts.spotify_consts import PLAYLISTS, TRACKS, OFFSET, LIMIT, ADDITIONAL_TYPES, TRACK
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from spotipyio.testing.utils.random_paged_responses_builder import RandomPagedResponsesBuilder


class PlaylistsInfoTestComponent(BaseTestComponent):
    def __init__(self, server: HTTPServer, headers: CIMultiDict):
        super().__init__(server=server, headers=headers)
        self._paged_responses_builder = RandomPagedResponsesBuilder(base_url=self._base_url, page_max_size=100)

    def expect(self, id_: str, expected_pages: int = 1) -> List[RequestHandler]:
        return self._create_request_handlers(id_, expected_pages)

    def expect_success(self, id_: str, response_jsons: Optional[List[Json]] = None, expected_pages: int = 1) -> None:
        request_handlers = self._create_request_handlers(id_, expected_pages)
        responses = self._build_responses(
            provided_responses=response_jsons,
            request_handlers=request_handlers,
            playlist_id=id_,
            expected_pages=expected_pages,
        )

        for handler, response in zip(request_handlers, responses):
            handler.respond_with_json(response)

    def expect_failure(
        self, id_: str, status: Optional[int] = None, response_json: Optional[Json] = None, expected_pages: int = 1
    ) -> None:
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)
        request_handlers = self._create_request_handlers(id_, expected_pages)
        first_handler = request_handlers[0]

        first_handler.respond_with_json(status=status, response_json=response_json)

    def _create_request_handlers(self, id_: str, expected_pages: int) -> List[RequestHandler]:
        handlers = [self._expect_get_request(route=f"/{PLAYLISTS}/{id_}")]

        for i in range(1, expected_pages):
            params = {OFFSET: str(i * 100), LIMIT: "100", ADDITIONAL_TYPES: TRACK}
            page_handler = self._expect_get_request(route=f"/{PLAYLISTS}/{id_}/{TRACKS}", params=params)
            handlers.append(page_handler)

        return handlers

    def _build_responses(
        self,
        provided_responses: Optional[List[Json]],
        request_handlers: List[RequestHandler],
        playlist_id: str,
        expected_pages: int,
    ) -> List[Json]:
        if provided_responses is not None:
            self._validate_provided_responses(provided_responses, request_handlers)
            return provided_responses

        return self._paged_responses_builder.build(playlist_id, expected_pages)

    @staticmethod
    def _validate_provided_responses(provided_responses: List[Json], request_handlers: List[RequestHandler]) -> None:
        request_handlers_number = len(request_handlers)
        provided_responses_number = len(provided_responses)

        if request_handlers_number != provided_responses_number:
            raise ValueError(f"Expected {request_handlers_number} responses but got {provided_responses_number}")

    def _generate_random_responses(self, request_handlers: List[RequestHandler], playlist_id: str) -> List[Json]:
        handlers_number = len(request_handlers)

        if handlers_number == 1:
            next_url = None
        else:
            next_url = f"{self._base_url}/{PLAYLISTS}/{playlist_id}/{TRACKS}?{OFFSET}=100&{LIMIT}=100"

        tracks = SpotifyMockFactory.playlist_tracks(next=next_url)
        responses = [SpotifyMockFactory.playlist(id=playlist_id, tracks=tracks)]

        for _ in range(1, handlers_number):
            page_response = SpotifyMockFactory.playlist_tracks(entity_id=playlist_id)
            responses.append(page_response)

        return responses
