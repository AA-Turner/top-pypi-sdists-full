from typing import List

from spotipyio.logic.utils.spotify_utils import extract_artists_names
from spotipyio.tools.extractors.entity_extractor_interface import IEntityExtractor


class PrimaryArtistEntityExtractor(IEntityExtractor):
    def extract(self, entity: dict) -> List[str]:
        artists_names = extract_artists_names(entity)
        return [artists_names[0]] if artists_names else []

    @property
    def name(self) -> str:
        return "artist"
