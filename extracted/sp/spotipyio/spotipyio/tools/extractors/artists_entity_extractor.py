from typing import Any, List

from spotipyio.logic.consts.matching_consts import FEATURE_STRINGS
from spotipyio.logic.utils.spotify_utils import extract_artists_names
from spotipyio.tools.extractors.entity_extractor_interface import IEntityExtractor


class ArtistsEntityExtractor(IEntityExtractor):
    def extract(self, entity: Any) -> List[str]:
        artists = extract_artists_names(entity)

        if len(artists) > 1:
            multi_artist_names = self._build_multi_artist_name(artists)
            artists.extend(multi_artist_names)

        return artists

    def _build_multi_artist_name(self, artists: List[str]) -> List[str]:
        if len(artists) == 2:
            return self._build_featuring_artist_name(artists)

        return [self._build_multiple_featured_artists_name(artists)]

    @staticmethod
    def _build_featuring_artist_name(artists: List[str]) -> List[str]:
        primary_artist = artists[0]
        featured_artist = artists[1]

        return [f"{primary_artist} {feat_string} {featured_artist}" for feat_string in FEATURE_STRINGS]

    @staticmethod
    def _build_multiple_featured_artists_name(artists: List[str]) -> str:
        multi_artist_name = artists[0]
        featured_artists = artists[1:]

        for i, artist_name in enumerate(featured_artists):
            if i == len(featured_artists) - 1:
                multi_artist_name += f" & {artist_name}"
            else:
                multi_artist_name += f", {artist_name}"

        return multi_artist_name

    @property
    def name(self) -> str:
        return "artist"
