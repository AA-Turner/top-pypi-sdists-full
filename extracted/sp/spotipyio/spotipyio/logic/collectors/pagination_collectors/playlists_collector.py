from typing import List, Optional, Dict

from spotipyio.logic.consts.spotify_consts import PLAYLISTS, TRACKS, NEXT, ITEMS, TRACK, ADDITIONAL_TYPES
from spotipyio.logic.contract import BasePaginationCollector
from spotipyio.logic.utils import safe_nested_get


class PlaylistsCollector(BasePaginationCollector):
    @property
    def _url_format(self) -> str:
        return f"{self._base_url}/{PLAYLISTS}/{{id}}"

    @property
    def _additional_items_request_params(self) -> Dict[str, str]:
        return {ADDITIONAL_TYPES: TRACK}

    def _extract_first_next_url(self, result: dict) -> Optional[str]:
        return safe_nested_get(result, [TRACKS, NEXT])

    def _extract_subsequent_next_url(self, page: dict) -> Optional[str]:
        return page[NEXT]

    def _extend_existing_items(self, result: dict, page: dict) -> None:
        existing_items: List[dict] = safe_nested_get(result, [TRACKS, ITEMS])

        if existing_items:
            page_items = page[ITEMS]
            existing_items.extend(page_items)
