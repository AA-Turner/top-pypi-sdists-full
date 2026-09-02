"""CountWithinRadius extractor (FEAT-190, spec Module 5).

Counts POIs within ``params.radius_m`` of each candidate. Returns raw
counts only (spec D7) — never a normalized/utility value.

``sklearn`` is imported lazily, inside ``compute()``, so this module has no
top-level heavy dependency (spec: "Lazy scipy/sklearn import").
"""
import numpy as np

from ..abstract import AbstractFeatureExtractor, register_extractor
from ..models import CandidateGrid, ExtractorParams, POILayer

# WGS-84 mean Earth radius, in meters — used to convert a meter radius to
# the radian radius expected by BallTree(metric='haversine').
_EARTH_RADIUS_M = 6371008.8


@register_extractor("count_within_radius")
class CountWithinRadius(AbstractFeatureExtractor):
    """Count POIs within a radius (meters) of each candidate."""

    async def compute(
        self,
        candidates: CandidateGrid,
        poi_layer: POILayer,
        params: ExtractorParams,
    ) -> np.ndarray:
        """Return the raw POI count within ``params.radius_m`` per candidate.

        Raises:
            ValueError: if ``params.radius_m`` is not set. It has no sane
                default (unlike ``k``, which defaults to 1), and dividing
                ``None`` by the Earth radius used to fail with an opaque
                ``TypeError`` deep inside this method — validated explicitly
                here for a clear, actionable error message instead.
        """
        if params.radius_m is None:
            raise ValueError(
                "count_within_radius requires ExtractorParams.radius_m to be "
                "set (e.g. ExtractorParams(radius_m=1000.0))."
            )

        from sklearn.neighbors import BallTree

        poi_coords = np.deg2rad(
            np.column_stack([poi_layer.latitudes, poi_layer.longitudes])
        )
        tree = BallTree(poi_coords, metric="haversine")

        cand_coords = np.deg2rad(
            np.column_stack([candidates.latitudes, candidates.longitudes])
        )
        radius_rad = params.radius_m / _EARTH_RADIUS_M
        counts = tree.query_radius(cand_coords, r=radius_rad, count_only=True)
        return counts.astype(float)
