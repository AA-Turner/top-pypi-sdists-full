"""Extractor ABC & Registry (FEAT-190).

Defines the extensibility seam for spatial feature extractors:
``AbstractFeatureExtractor`` (spec Module 2) plus a simple dict-based
``ExtractorRegistry``. Concrete extractors (TASK-127) self-register via the
``register_extractor`` decorator on import.

Only ``abc`` and ``numpy`` are imported here — no scipy, no h3 (spec AC11).
"""
from abc import ABC, abstractmethod

import numpy as np

from .models import CandidateGrid, ExtractorParams, POILayer


class AbstractFeatureExtractor(ABC):
    """ABC for spatial aggregators. Returns raw scalars only (spec D7).

    Implementations MUST return raw feature values (counts, meters,
    gravity mass) — NEVER a normalized/utility value. Normalization to
    [0,100] is the responsibility of ``ValueFunction`` in the scoring
    engine, not the extractor.
    """

    feature_type: str

    @abstractmethod
    async def compute(
        self,
        candidates: CandidateGrid,
        poi_layer: POILayer,
        params: ExtractorParams,
    ) -> np.ndarray:
        """Compute the raw feature value for each candidate.

        Args:
            candidates: Candidate locations to score.
            poi_layer: Points-of-interest layer to aggregate against.
            params: Extractor-specific parameters (radius, k, kernel, etc).

        Returns:
            A numpy array of shape ``(len(candidates.latitudes),)`` with
            raw (non-normalized) scalar values.
        """
        ...


class ExtractorRegistry:
    """Simple dict-based registry for feature extractors."""

    def __init__(self) -> None:
        self._registry: dict[str, type] = {}

    def register(self, feature_type: str, cls: type) -> None:
        """Register an extractor class under a feature_type key."""
        self._registry[feature_type] = cls

    def get(self, feature_type: str) -> type:
        """Look up an extractor class by feature_type.

        Raises:
            KeyError: if no extractor is registered for ``feature_type``.
        """
        if feature_type not in self._registry:
            raise KeyError(
                f"Unknown feature_type: {feature_type!r}. "
                f"Available: {list(self._registry.keys())}"
            )
        return self._registry[feature_type]

    def list_types(self) -> list[str]:
        """List all registered feature_type keys."""
        return list(self._registry.keys())


# Module-level singleton — extractors register themselves here on import
# (spec Module 5 / TASK-127).
extractor_registry = ExtractorRegistry()


def register_extractor(feature_type: str):
    """Class decorator to register an extractor with the singleton registry.

    Also sets ``cls.feature_type`` for convenience.
    """

    def decorator(cls: type) -> type:
        extractor_registry.register(feature_type, cls)
        cls.feature_type = feature_type
        return cls

    return decorator
