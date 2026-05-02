from random import randint
from typing import List
from urllib.parse import urlencode

from spotipyio.logic.consts.spotify_consts import OFFSET, LIMIT, PLAYLISTS, TRACKS
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class RandomPagedResponsesBuilder:
    def __init__(self, base_url: str, page_max_size: int):
        self._base_url = base_url
        self._page_max_size = page_max_size

    def build(self, playlist_id: str, max_pages: int) -> List[dict]:
        second_page_url = self._build_next_url(playlist_id, page_number=1)
        tracks = SpotifyMockFactory.playlist_tracks(next=second_page_url)
        playlist_response = SpotifyMockFactory.playlist(id=playlist_id, tracks=tracks, total=self._page_max_size)
        additional_pages_responses = self._build_additional_pages_responses(
            max_pages=max_pages, playlist_id=playlist_id
        )

        return [playlist_response] + additional_pages_responses

    def _build_next_url(self, playlist_id: str, page_number: int) -> str:
        params = {OFFSET: str(page_number * self._page_max_size), LIMIT: str(self._page_max_size)}
        encoded_params = urlencode(params)

        return f"{self._base_url}/{PLAYLISTS}/{playlist_id}/{TRACKS}?{encoded_params}"

    def _build_additional_pages_responses(self, max_pages: int, playlist_id: str) -> List[dict]:
        additional_pages_responses = []

        for i in range(1, max_pages):
            page_response = self._build_single_page_response(
                page_number=i + 1, max_pages=max_pages, playlist_id=playlist_id
            )
            additional_pages_responses.append(page_response)

        return additional_pages_responses

    def _build_single_page_response(self, page_number: int, max_pages: int, playlist_id: str) -> dict:
        if page_number == max_pages:
            next_url = None
            total_tracks = randint(1, self._page_max_size)
        else:
            next_url = self._build_next_url(playlist_id, page_number=page_number)
            total_tracks = self._page_max_size

        return SpotifyMockFactory.playlist_tracks(id=playlist_id, next=next_url, total=total_tracks)
