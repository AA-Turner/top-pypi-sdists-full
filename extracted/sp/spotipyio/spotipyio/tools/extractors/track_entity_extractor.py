import re
from typing import List

from spotipyio.logic.consts.matching_consts import LOWERCASED_FEATURE_STRINGS
from spotipyio.logic.consts.spotify_consts import NAME
from spotipyio.logic.utils.spotify_utils import extract_artists_names
from spotipyio.tools.extractors.entity_extractor_interface import IEntityExtractor


class TrackEntityExtractor(IEntityExtractor):
    def extract(self, entity: dict) -> List[str]:
        name = entity.get(NAME)
        if not isinstance(name, str):
            return []

        return self._generate_tracks_candidates(name, entity)

    def _generate_tracks_candidates(self, name: str, entity: dict) -> List[str]:
        candidates = [name]
        lower_name = name.lower()
        feature_indications = self._extract_feature_indications(lower_name)

        if self._contains_any_feature_indication(lower_name, feature_indications):
            feature_candidates = self._generate_feature_candidates(
                name=lower_name, entity=entity, feature_indications=feature_indications
            )
            candidates.extend(feature_candidates)

        return candidates

    @staticmethod
    def _extract_feature_indications(name: str) -> List[str]:
        return [feat_string for feat_string in LOWERCASED_FEATURE_STRINGS if feat_string in name]

    @staticmethod
    def _contains_any_feature_indication(name: str, feature_indications: List[str]) -> bool:
        return any(feat_string in name for feat_string in feature_indications)

    def _generate_feature_candidates(self, name: str, entity: dict, feature_indications: List[str]) -> List[str]:
        feature_candidates = []
        artists_names = extract_artists_names(entity)

        if self._contains_any_artists_name(name, artists_names):
            formatted_name = self._strip_name_from_featuring_artists(
                name=name, feature_indications=feature_indications, artists_names=artists_names
            )
            feature_candidates.append(formatted_name)

        return feature_candidates

    @staticmethod
    def _contains_any_artists_name(name: str, artists_names: List[str]) -> bool:
        return any(artist_name.lower() in name for artist_name in artists_names)

    @staticmethod
    def _strip_name_from_featuring_artists(name: str, feature_indications: List[str], artists_names: List[str]) -> str:
        for elem in artists_names + feature_indications:
            name = name.replace(elem.lower(), "")

        return re.sub(r"[()&,]", "", name).strip()

    @property
    def name(self) -> str:
        return "track"
