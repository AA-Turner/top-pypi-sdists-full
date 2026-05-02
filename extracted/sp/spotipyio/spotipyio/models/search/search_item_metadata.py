from dataclasses import dataclass, field
from typing import List

from spotipyio.logic.utils import get_all_enum_values
from spotipyio.models.search.spotify_search_type import SpotifySearchType


@dataclass
class SearchItemMetadata:
    search_types: List[SpotifySearchType] = field(default_factory=lambda: get_all_enum_values(SpotifySearchType))
    quote: bool = True

    def __post_init__(self):
        if not self.search_types:
            raise ValueError("SearchItemMetadata must include at least one SpotifySearchType")
