"""NearestDistance extractor (FEAT-190, spec Module 5).

Distance in meters to the ``params.k``-th nearest POI. Returns a raw
distance only (spec D7) — never a normalized/utility value.

Uses ``sklearn.neighbors.BallTree(metric='haversine')`` (same as
``count_within_radius``) for accurate great-circle distances, imported
lazily inside ``compute()``.
"""
import numpy as np

from ..abstract import AbstractFeatureExtractor, register_extractor
from ..models import CandidateGrid, ExtractorParams, POILayer

# WGS-84 mean Earth radius, in meters — converts BallTree's haversine
# (radian) distances back to meters.
_EARTH_RADIUS_M = 6371008.8


@register_extractor("nearest_distance")
class NearestDistance(AbstractFeatureExtractor):
    """Distance (meters) to the k-th nearest POI for each candidate."""

    async def compute(
        self,
        candidates: CandidateGrid,
        poi_layer: POILayer,
        params: ExtractorParams,
    ) -> np.ndarray:
        """Return the raw distance (meters) to the k-th nearest POI.

        Raises:
            ValueError: if ``params.k`` exceeds the number of POIs in
                ``poi_layer`` — ``BallTree.query(k=...)`` would otherwise
                raise an opaque, low-level sklearn ``ValueError`` with no
                context about which criterion/layer caused it.
        """
        n_pois = len(poi_layer.latitudes)
        if params.k > n_pois:
            raise ValueError(
                f"nearest_distance requested k={params.k} but POI layer "
                f"{poi_layer.name!r} only has {n_pois} point(s)."
            )

        from sklearn.neighbors import BallTree

        poi_coords = np.deg2rad(
            np.column_stack([poi_layer.latitudes, poi_layer.longitudes])
        )
        tree = BallTree(poi_coords, metric="haversine")

        cand_coords = np.deg2rad(
            np.column_stack([candidates.latitudes, candidates.longitudes])
        )
        distances_rad, _ = tree.query(cand_coords, k=params.k)
        # distances_rad shape: (n_candidates, k). We want the k-th nearest
        # (the last column), in meters.
        kth_distance_rad = distances_rad[:, -1]
        return kth_distance_rad * _EARTH_RADIUS_M
