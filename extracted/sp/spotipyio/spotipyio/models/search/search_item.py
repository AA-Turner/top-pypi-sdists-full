from dataclasses import dataclass, fields, field
from typing import Optional, Dict, List
from urllib.parse import quote

from spotipyio.logic.consts.spotify_consts import OFFSET, LIMIT
from spotipyio.logic.internal_models import ChunkSize
from spotipyio.models.search.spotify_search_type import SpotifySearchType
from spotipyio.models.search.search_item_filters import SearchItemFilters
from spotipyio.models.search.search_item_metadata import SearchItemMetadata


@dataclass
class SearchItem:
    text: Optional[str] = None
    filters: SearchItemFilters = field(default_factory=lambda: SearchItemFilters())
    metadata: SearchItemMetadata = field(default_factory=lambda: SearchItemMetadata())

    def __post_init__(self):
        self._validate_input()

    def to_query_params(self, search_types: Optional[List[SpotifySearchType]] = None) -> Dict[str, str]:
        if search_types:
            types = [search_type.value for search_type in search_types]
        else:
            types = [search_type.value for search_type in self.metadata.search_types]

        return {"q": self._build_query(), "type": ",".join(types), OFFSET: "0", LIMIT: f"{ChunkSize.SEARCH.value}"}

    def _build_query(self) -> str:
        query_components = self._get_query_component()
        query = " ".join(query_components)

        if self.metadata.quote:
            return quote(query)

        return query

    def _get_query_component(self) -> List[str]:
        query_components = []

        if self.text is not None:
            query_components.append(self.text)

        for filter_field in fields(self.filters):
            field_value = getattr(self.filters, filter_field.name)

            if field_value is not None:
                query_components.append(f"{filter_field.name}:{field_value}")

        return query_components

    def _validate_input(self) -> None:
        filters_values = [getattr(self.filters, field.name) for field in fields(self.filters)]
        are_all_filters_missing = all(value is None for value in filters_values)

        if self.text is None and are_all_filters_missing:
            raise ValueError("You must supply text or at least one search filter")
