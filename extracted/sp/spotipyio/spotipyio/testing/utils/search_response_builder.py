from random import randint
from typing import List, Dict

from spotipyio.logic.consts.spotify_consts import (
    HREF,
    LIMIT,
    NEXT,
    OFFSET,
    PREVIOUS,
    TOTAL,
    ITEMS,
    ALBUMS,
    ARTISTS,
    AUDIOBOOKS,
    EPISODES,
    PLAYLISTS,
    SHOWS,
    TRACKS,
)
from spotipyio.models import SpotifySearchType, SearchItem


class SearchResponseBuilder:
    def __init__(self, search_item: SearchItem):
        self._search_item = search_item
        self._search_response = {}

    def add(self, search_type: SpotifySearchType, items: List[dict]) -> None:
        response = self._build_single_search_response(search_type)
        response[ITEMS] = items
        key = self._search_type_key_map[search_type]

        self._search_response[key] = response

    def build(self) -> dict:
        return self._search_response

    def _build_single_search_response(self, search_type: SpotifySearchType) -> dict:
        return {
            HREF: self._build_search_response_href(search_type, offset=0),
            LIMIT: 20,
            NEXT: self._build_search_response_href(search_type, offset=20),
            OFFSET: 0,
            PREVIOUS: None,
            TOTAL: randint(1, 1000),
        }

    def _build_search_response_href(self, search_type: SpotifySearchType, offset: int) -> str:
        query = self._search_item.to_query_params([search_type])
        return f"https://api.spotify.com/v1/search?query={query}&offset={offset}&limit=20"

    @property
    def _search_type_key_map(self) -> Dict[SpotifySearchType, str]:
        return {
            SpotifySearchType.ALBUM: ALBUMS,
            SpotifySearchType.ARTIST: ARTISTS,
            SpotifySearchType.AUDIOBOOK: AUDIOBOOKS,
            SpotifySearchType.EPISODE: EPISODES,
            SpotifySearchType.PLAYLIST: PLAYLISTS,
            SpotifySearchType.SHOW: SHOWS,
            SpotifySearchType.TRACK: TRACKS,
        }
