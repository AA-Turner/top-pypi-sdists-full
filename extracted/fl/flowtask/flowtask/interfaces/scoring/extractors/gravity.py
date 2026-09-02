"""Gravity extractor (FEAT-190, spec Module 5, OQ6→v1).

Gravity mass: ``Σ attribute_i · kernel(distance_i)`` over the k-nearest POIs.
Returns a raw mass value only (spec D7) — never a normalized/utility value.

If ``params.attribute`` is ``None``, every POI has weight 1 (the gravity
mass degenerates to a distance-weighted count, spec Implementation Notes).

Uses ``sklearn.neighbors.BallTree(metric='haversine')`` (same as the other
extractors) for accurate great-circle distances, imported lazily inside
``compute()``.
"""
import numpy as np

from ..abstract import AbstractFeatureExtractor, register_extractor
from ..models import CandidateGrid, ExtractorParams, POILayer

# WGS-84 mean Earth radius, in meters — converts BallTree's haversine
# (radian) distances back to meters.
_EARTH_RADIUS_M = 6371008.8


@register_extractor("gravity")
class Gravity(AbstractFeatureExtractor):
    """Gravity mass over the k-nearest POIs, with attribute weighting and
    distance decay kernel (gaussian or exponential)."""

    async def compute(
        self,
        candidates: CandidateGrid,
        poi_layer: POILayer,
        params: ExtractorParams,
    ) -> np.ndarray:
        """Return the raw gravity mass for each candidate.

        Raises:
            ValueError: if ``params.k`` exceeds the number of POIs in
                ``poi_layer``, or if ``params.attribute`` is set but not
                present in ``poi_layer.attributes`` — both used to raise
                opaque, low-level ``ValueError``/``KeyError`` exceptions
                with no context about which criterion/layer caused them.
        """
        n_pois = len(poi_layer.latitudes)
        if params.k > n_pois:
            raise ValueError(
                f"gravity requested k={params.k} but POI layer "
                f"{poi_layer.name!r} only has {n_pois} point(s)."
            )
        if params.attribute is not None and params.attribute not in poi_layer.attributes:
            raise ValueError(
                f"gravity requested attribute {params.attribute!r} but POI "
                f"layer {poi_layer.name!r} only has attributes: "
                f"{list(poi_layer.attributes.keys())}."
            )

        from sklearn.neighbors import BallTree

        poi_coords = np.deg2rad(
            np.column_stack([poi_layer.latitudes, poi_layer.longitudes])
        )
        tree = BallTree(poi_coords, metric="haversine")

        cand_coords = np.deg2rad(
            np.column_stack([candidates.latitudes, candidates.longitudes])
        )
        distances_rad, indices = tree.query(cand_coords, k=params.k)
        distances_m = distances_rad * _EARTH_RADIUS_M  # shape (n_candidates, k)

        if params.attribute is not None:
            attr_values = poi_layer.attributes[params.attribute]
            weights = attr_values[indices].astype(float)
        else:
            weights = np.ones_like(distances_m)

        bandwidth = params.bandwidth_m if params.bandwidth_m is not None else 1.0
        if params.kernel == "exponential":
            kernel_values = np.exp(-distances_m / bandwidth)
        else:
            # Default kernel is gaussian when unset.
            kernel_values = np.exp(-(distances_m ** 2) / (2.0 * bandwidth ** 2))

        mass = np.sum(weights * kernel_values, axis=1)
        return mass
