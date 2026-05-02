from random import choice
from typing import List, Optional

from multidict import CIMultiDict
from pytest_httpserver import RequestHandler, HTTPServer

from spotipyio.logic.consts.spotify_consts import PLAYLISTS, TRACKS, SNAPSHOT_ID, URI
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.logic.internal_models import ChunkSize
from spotipyio.logic.internal_tools import DataChunksGenerator
from spotipyio.testing.infra import BaseTestComponent
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class PlaylistsItemsRemoverTestComponent(BaseTestComponent):
    def __init__(
        self, server: HTTPServer, headers: CIMultiDict, chunks_generator: DataChunksGenerator = DataChunksGenerator()
    ):
        super().__init__(server=server, headers=headers)
        self._chunks_generator = chunks_generator

    def expect(self, playlist_id: str, uris: List[str], snapshot_id: str) -> List[RequestHandler]:
        chunks = self._to_chunks(uris)
        snapshots_ids = self._create_snapshots_ids(
            chunks=chunks,
            provided_snapshot=snapshot_id,
        )
        return self._create_request_handlers(
            playlist_id=playlist_id,
            chunks=chunks,
            snapshots_ids=snapshots_ids,
        )

    def expect_success(
        self, playlist_id: str, uris: List[str], snapshot_id: str, expected_snapshots: Optional[List[str]] = None
    ) -> None:
        chunks = self._to_chunks(uris)
        snapshots_ids = self._create_snapshots_ids(
            chunks=chunks, provided_snapshot=snapshot_id, expected_snapshots=expected_snapshots
        )
        request_handlers = self._create_request_handlers(
            playlist_id=playlist_id,
            chunks=chunks,
            snapshots_ids=snapshots_ids,
        )

        self._set_handlers_success(request_handlers, snapshots_ids)

    def expect_failure(
        self,
        playlist_id: str,
        uris: List[str],
        snapshot_id: str,
        response_json: Optional[Json] = None,
        status: Optional[int] = None,
    ) -> None:
        chunks = self._to_chunks(uris)
        snapshots_ids = self._create_snapshots_ids(
            chunks=chunks,
            provided_snapshot=snapshot_id,
        )
        request_handlers = self._create_request_handlers(
            playlist_id=playlist_id,
            chunks=chunks,
            snapshots_ids=snapshots_ids,
        )
        status, response_json = self._create_invalid_response(status=status, response_json=response_json)

        self._set_handlers_failure(
            request_handlers=request_handlers, snapshots_ids=snapshots_ids, response_json=response_json, status=status
        )

    def _create_request_handlers(
        self, playlist_id: str, chunks: List[List[str]], snapshots_ids: List[str]
    ) -> List[RequestHandler]:
        handlers = []

        for (
            i,
            chunk,
        ) in enumerate(chunks):
            payload = {TRACKS: [{URI: uri} for uri in chunk], SNAPSHOT_ID: snapshots_ids[i]}
            handler = self._expect_delete_request(route=f"/{PLAYLISTS}/{playlist_id}/{TRACKS}", payload=payload)
            handlers.append(handler)

        return handlers

    def _create_snapshots_ids(
        self, chunks: List[List[str]], provided_snapshot: str, expected_snapshots: Optional[List[str]] = None
    ) -> List[str]:
        if expected_snapshots:
            self._validate_expected_snapshots_number(chunks, expected_snapshots)
            snapshots_ids = expected_snapshots
        else:
            snapshots_ids = [SpotifyMockFactory.snapshot_id() for _ in chunks]

        return [provided_snapshot] + snapshots_ids

    @staticmethod
    def _validate_expected_snapshots_number(chunks: List[List[str]], expected_snapshots: List[str]) -> None:
        snapshots_number = len(expected_snapshots)
        requests_number = len(chunks)

        if snapshots_number != requests_number:
            raise ValueError(
                f"Received {snapshots_number} expected snapshots while expecting only {requests_number} requests"
            )

    @staticmethod
    def _set_handlers_success(request_handlers: List[RequestHandler], snapshots_ids: List[str]) -> None:
        for i, handler in enumerate(request_handlers):
            snapshot_id = snapshots_ids[i + 1]
            response = SpotifyMockFactory.snapshot_response(snapshot_id)
            handler.respond_with_json(response_json=response, status=200)

    def _set_handlers_failure(
        self, request_handlers: List[RequestHandler], snapshots_ids: List[str], response_json: Json, status: int
    ) -> None:
        failed_handler_index = choice(list(range(len(request_handlers))))

        for i, handler in enumerate(request_handlers):
            if i == failed_handler_index:
                handler.respond_with_json(response_json=response_json, status=status)
            else:
                self._set_handlers_success(request_handlers=[handler], snapshots_ids=snapshots_ids[i : i + 2])

    def _to_chunks(self, uris: List[str]) -> List[List[str]]:
        chunks = self._chunks_generator.generate_data_chunks(lst=uris, chunk_size=ChunkSize.ITEMS_REMOVAL.value)
        return list(chunks)
