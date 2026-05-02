from typing import Optional

from spotipyio.logic.consts.spotify_consts import NEXT, ITEMS, PLAYLISTS, USERS
from spotipyio.logic.contract import BasePaginationCollector


class UserPlaylistsCollector(BasePaginationCollector):
    @property
    def _url_format(self) -> str:
        return f"{self._base_url}/{USERS}/{{id}}/{PLAYLISTS}?offset=0&limit=50"

    @property
    def _additional_items_request_params(self) -> None:
        return None

    def _extract_first_next_url(self, result: dict) -> Optional[str]:
        return result[NEXT]

    def _extract_subsequent_next_url(self, page: dict) -> Optional[str]:
        return page[NEXT]

    def _extend_existing_items(self, result: dict, page: dict) -> None:
        existing_items = result[ITEMS]
        page_items = page[ITEMS]
        existing_items.extend(page_items)
