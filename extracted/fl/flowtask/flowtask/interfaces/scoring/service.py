"""Scorer Facade (FEAT-190, spec Module 4).

``SweetSpotScorer`` is the single public entry point of the scoring engine:
it orchestrates extractors → feature matrix → ``ScoringEngine``. Both the
DAG component (TASK-130) and any future agentic adapter call this class.

The facade never re-implements scoring logic — it is pure orchestration and
delegates all deterministic math to ``ScoringEngine`` (TASK-125).
"""
import asyncio
from typing import Optional

import numpy as np

from .abstract import ExtractorRegistry, extractor_registry
from .engine import ScoringEngine
from .models import CandidateGrid, POILayer, ScoreResult, ScoringPolicy


class SweetSpotScorer:
    """Framework-agnostic facade. Public entry point of the scoring engine."""

    def __init__(self, extractors: Optional[ExtractorRegistry] = None) -> None:
        self._extractors = extractors or extractor_registry
        self._engine = ScoringEngine()

    async def score(
        self,
        candidates: CandidateGrid,
        layers: dict[str, POILayer],
        policy: ScoringPolicy,
    ) -> ScoreResult:
        """Score every candidate against the policy.

        Args:
            candidates: Candidate locations to score.
            layers: Mapping of dataset name → ``POILayer``, keyed by the
                ``dataset`` field referenced by each ``Criterion``/``HardFilter``.
            policy: Frozen scoring policy.

        Returns:
            A ``ScoreResult`` with ``candidate_ids`` populated from
            ``candidates.ids``.
        """
        # Ensure concrete extractors are registered (idempotent, cheap after
        # the first call — Python caches module imports).
        import flowtask.interfaces.scoring.extractors  # noqa: F401

        n_candidates = len(candidates.latitudes)

        async def _extract(feature_type: str, dataset: str, params) -> np.ndarray:
            try:
                poi_layer = layers[dataset]
            except KeyError as exc:
                # Framework-agnostic: raise a plain, actionable ValueError
                # here rather than a bare KeyError — this facade has no
                # dependency on flowtask's DAG runtime (spec G2), so it
                # must not import flowtask-specific exceptions. The DAG
                # component wrapper (SweetSpotScore) re-wraps this into a
                # ComponentError for pipeline-friendly error reporting.
                raise ValueError(
                    f"No POILayer found for dataset {dataset!r}. "
                    f"Available datasets: {sorted(layers.keys())}"
                ) from exc
            extractor_cls = self._extractors.get(feature_type)
            extractor = extractor_cls()
            return await extractor.compute(candidates, poi_layer, params)

        # Extract criteria features concurrently (spec Module 4).
        criteria_columns = await asyncio.gather(
            *[
                _extract(criterion.feature_type, criterion.dataset, criterion.params)
                for criterion in policy.criteria
            ]
        )
        if criteria_columns:
            feature_matrix = np.column_stack(criteria_columns)
        else:
            feature_matrix = np.zeros((n_candidates, 0))

        # Extract hard-filter features concurrently, same mechanism.
        filter_matrix: Optional[np.ndarray] = None
        if policy.filters:
            filter_columns = await asyncio.gather(
                *[
                    _extract(hard_filter.feature_type, hard_filter.dataset, hard_filter.params)
                    for hard_filter in policy.filters
                ]
            )
            filter_matrix = np.column_stack(filter_columns)

        return self._engine.score(
            feature_matrix,
            policy,
            filter_matrix=filter_matrix,
            candidate_ids=candidates.ids,
        )
