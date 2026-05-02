from typing import Any, List, Optional

from spotipyio.logic.internal_tools import logger
from spotipyio.models import MatchingEntity, MatchingMethod
from spotipyio.tools.matching import EntityMatcher


class MultiEntityMatcher:
    def __init__(self, entity_matcher: EntityMatcher):
        self._entity_matcher = entity_matcher

    def match(
        self,
        entities: List[MatchingEntity],
        candidates: List[Any],
        method: MatchingMethod = MatchingMethod.HIGHEST_MATCH_SCORE,
    ) -> Optional[Any]:
        matching_candidate = self._get_matching_candidate(entities=entities, candidates=candidates, method=method)
        if matching_candidate:
            return matching_candidate

        logger.info("Failed to match any of the provided candidates. Returning None")

    def _get_matching_candidate(
        self,
        entities: List[MatchingEntity],
        candidates: List[Any],
        method: MatchingMethod = MatchingMethod.HIGHEST_MATCH_SCORE,
    ) -> Optional[Any]:
        if method == MatchingMethod.FIRST_MATCHING:
            return self._get_first_matching_candidate(entities, candidates)
        elif method == MatchingMethod.HIGHEST_MATCH_SCORE:
            return self._get_candidate_with_highest_match_score(entities, candidates)
        else:
            raise ValueError(f"Unsupported matching method: `{method}`")

    def _get_first_matching_candidate(self, entities: List[MatchingEntity], candidates: List[Any]) -> Optional[Any]:
        for entity in entities:
            for candidate in candidates:
                is_matching, _ = self._entity_matcher.match(entity, candidate)

                if is_matching:
                    return candidate

    def _get_candidate_with_highest_match_score(
        self, entities: List[MatchingEntity], candidates: List[Any]
    ) -> Optional[Any]:
        selected_candidate = None
        selected_candidate_score = 0

        for entity in entities:
            for candidate in candidates:
                is_matching, score = self._entity_matcher.match(entity, candidate)

                if is_matching and score > selected_candidate_score:
                    selected_candidate = candidate
                    selected_candidate_score = score

        return selected_candidate
